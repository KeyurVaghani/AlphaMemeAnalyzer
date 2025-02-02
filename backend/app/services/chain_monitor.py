from typing import Dict, List, Optional
from web3 import Web3
from eth_typing import Address
from app.core.config import settings
from app.models.chain_analysis import ChainAnalysis
from app.models.memecoin import BlockchainType
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime, timedelta

class ChainMonitor:
    def __init__(self):
        # Initialize Web3 providers
        self.eth_w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"))
        self.bsc_w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        
        # Load smart money wallets
        self.smart_money_wallets = self._load_smart_money_wallets()
        
        # Standard token ABI for basic interactions
        self.token_abi = json.loads('[{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')

    async def analyze_chain_metrics(
        self,
        db: Session,
        memecoin_id: int,
        contract_address: str,
        blockchain: BlockchainType
    ) -> Dict:
        """
        Analyze on-chain metrics for a memecoin
        """
        try:
            # Select appropriate Web3 instance
            w3 = self.eth_w3 if blockchain == BlockchainType.ETHEREUM else self.bsc_w3
            
            # Create contract instance
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=self.token_abi)
            
            # Get basic contract info
            total_supply = contract.functions.totalSupply().call()
            
            # Analyze holders
            holder_data = await self._analyze_holders(w3, contract, contract_address)
            
            # Analyze liquidity
            liquidity_data = await self._analyze_liquidity(w3, contract_address, blockchain)
            
            # Track smart money movements
            smart_money_data = await self._track_smart_money(w3, contract_address)
            
            # Analyze contract security
            security_data = await self._analyze_contract_security(w3, contract_address)
            
            # Create chain analysis record
            analysis = ChainAnalysis(
                memecoin_id=memecoin_id,
                liquidity_usd=liquidity_data['liquidity_usd'],
                liquidity_change_24h=liquidity_data['liquidity_change_24h'],
                liquidity_locked_ratio=liquidity_data['locked_ratio'],
                lock_duration_days=liquidity_data['lock_duration'],
                total_holders=holder_data['total_holders'],
                holder_change_24h=holder_data['holder_change_24h'],
                top_10_holders_ratio=holder_data['top_10_ratio'],
                whale_wallets=holder_data['whale_wallets'],
                smart_money_inflow=smart_money_data['inflow'],
                smart_money_wallets=smart_money_data['wallets'],
                smart_money_confidence=smart_money_data['confidence'],
                contract_verified=security_data['verified'],
                mint_disabled=security_data['mint_disabled'],
                ownership_renounced=security_data['ownership_renounced'],
                security_score=security_data['security_score'],
                risk_factors=security_data['risk_factors']
            )
            
            db.add(analysis)
            db.commit()
            
            return {
                "holder_data": holder_data,
                "liquidity_data": liquidity_data,
                "smart_money_data": smart_money_data,
                "security_data": security_data
            }
            
        except Exception as e:
            print(f"Chain analysis error: {str(e)}")
            return self._empty_metrics()

    async def _analyze_holders(self, w3: Web3, contract, contract_address: str) -> Dict:
        """
        Analyze holder distribution and changes
        """
        try:
            # Get current holders
            transfer_filter = contract.events.Transfer.create_filter(fromBlock=w3.eth.block_number - 6500)  # ~24h
            transfers = transfer_filter.get_all_entries()
            
            # Get unique holders
            holders = set()
            for transfer in transfers:
                holders.add(transfer.args.to)
                holders.add(transfer.args.from_)
            
            # Get balances for top holders
            holder_balances = []
            for holder in holders:
                balance = contract.functions.balanceOf(holder).call()
                if balance > 0:
                    holder_balances.append((holder, balance))
            
            # Sort by balance
            holder_balances.sort(key=lambda x: x[1], reverse=True)
            
            # Calculate metrics
            total_holders = len([h for h in holder_balances if h[1] > 0])
            top_10_balance = sum(b for _, b in holder_balances[:10])
            total_supply = contract.functions.totalSupply().call()
            top_10_ratio = top_10_balance / total_supply if total_supply > 0 else 0
            
            # Identify whale wallets (>1% of supply)
            whale_threshold = total_supply * 0.01
            whale_wallets = [
                {
                    "address": h[0],
                    "balance": h[1],
                    "percentage": (h[1] / total_supply) * 100
                }
                for h in holder_balances
                if h[1] >= whale_threshold
            ]
            
            return {
                "total_holders": total_holders,
                "holder_change_24h": len(transfers),
                "top_10_ratio": top_10_ratio,
                "whale_wallets": whale_wallets
            }
        except Exception as e:
            print(f"Holder analysis error: {str(e)}")
            return {
                "total_holders": 0,
                "holder_change_24h": 0,
                "top_10_ratio": 0,
                "whale_wallets": []
            }

    async def _analyze_liquidity(self, w3: Web3, contract_address: str, blockchain: BlockchainType) -> Dict:
        """
        Analyze liquidity metrics
        """
        try:
            # Get liquidity data from DEX (example with Uniswap V2)
            factory_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"  # Uniswap V2 Factory
            factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"stateMutability":"view","type":"function"}]')
            
            factory = w3.eth.contract(address=factory_address, abi=factory_abi)
            
            # Get WETH pair
            weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
            pair_address = factory.functions.getPair(contract_address, weth_address).call()
            
            if pair_address == "0x0000000000000000000000000000000000000000":
                return self._empty_liquidity_metrics()
            
            # Get pair data
            pair_abi = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"name":"_reserve0","type":"uint112"},{"name":"_reserve1","type":"uint112"},{"name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')
            pair = w3.eth.contract(address=pair_address, abi=pair_abi)
            
            # Get reserves
            reserves = pair.functions.getReserves().call()
            
            # Calculate liquidity value
            eth_price = self._get_eth_price()  # Implement price oracle
            liquidity_usd = (reserves[1] * eth_price * 2) / 1e18  # Assuming WETH is token1
            
            return {
                "liquidity_usd": liquidity_usd,
                "liquidity_change_24h": 0,  # Implement historical comparison
                "locked_ratio": 0.8,  # Implement liquidity lock checking
                "lock_duration": 180  # days
            }
        except Exception as e:
            print(f"Liquidity analysis error: {str(e)}")
            return self._empty_liquidity_metrics()

    async def _track_smart_money(self, w3: Web3, contract_address: str) -> Dict:
        """
        Track smart money wallet movements
        """
        try:
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=self.token_abi)
            
            smart_money_data = {
                "inflow": 0.0,
                "wallets": [],
                "confidence": 0.0
            }
            
            for wallet in self.smart_money_wallets:
                balance = contract.functions.balanceOf(wallet).call()
                if balance > 0:
                    smart_money_data["wallets"].append({
                        "address": wallet,
                        "balance": balance
                    })
                    smart_money_data["inflow"] += balance
            
            total_supply = contract.functions.totalSupply().call()
            smart_money_data["confidence"] = len(smart_money_data["wallets"]) / len(self.smart_money_wallets)
            
            return smart_money_data
        except Exception as e:
            print(f"Smart money tracking error: {str(e)}")
            return {
                "inflow": 0.0,
                "wallets": [],
                "confidence": 0.0
            }

    async def _analyze_contract_security(self, w3: Web3, contract_address: str) -> Dict:
        """
        Analyze contract security metrics
        """
        try:
            # Check contract verification
            verified = self._check_contract_verification(contract_address)
            
            # Check for mint function
            contract_code = w3.eth.get_code(Web3.to_checksum_address(contract_address))
            mint_disabled = b"mint" not in contract_code.lower()
            
            # Check ownership
            ownership_renounced = self._check_ownership_renounced(w3, contract_address)
            
            # Calculate security score
            security_score = 0.0
            security_score += 0.4 if verified else 0
            security_score += 0.3 if mint_disabled else 0
            security_score += 0.3 if ownership_renounced else 0
            
            # Identify risk factors
            risk_factors = []
            if not verified:
                risk_factors.append("Contract not verified")
            if not mint_disabled:
                risk_factors.append("Mint function present")
            if not ownership_renounced:
                risk_factors.append("Ownership not renounced")
            
            return {
                "verified": verified,
                "mint_disabled": mint_disabled,
                "ownership_renounced": ownership_renounced,
                "security_score": security_score,
                "risk_factors": risk_factors
            }
        except Exception as e:
            print(f"Security analysis error: {str(e)}")
            return {
                "verified": False,
                "mint_disabled": False,
                "ownership_renounced": False,
                "security_score": 0.0,
                "risk_factors": ["Analysis failed"]
            }

    def _load_smart_money_wallets(self) -> List[str]:
        """
        Load known smart money wallet addresses
        """
        # TODO: Implement wallet loading from database or config
        return [
            "0x000000000000000000000000000000000000dead",  # Example addresses
            "0x000000000000000000000000000000000000beef"
        ]

    def _get_eth_price(self) -> float:
        """
        Get current ETH price
        """
        # TODO: Implement price oracle
        return 2000.0  # Example price

    def _check_contract_verification(self, contract_address: str) -> bool:
        """
        Check if contract is verified on blockchain explorer
        """
        # TODO: Implement verification check using Etherscan/BSCScan API
        return True

    def _check_ownership_renounced(self, w3: Web3, contract_address: str) -> bool:
        """
        Check if contract ownership is renounced
        """
        # TODO: Implement ownership check
        return True

    def _empty_metrics(self) -> Dict:
        """
        Return empty metrics structure
        """
        return {
            "holder_data": {
                "total_holders": 0,
                "holder_change_24h": 0,
                "top_10_ratio": 0,
                "whale_wallets": []
            },
            "liquidity_data": self._empty_liquidity_metrics(),
            "smart_money_data": {
                "inflow": 0.0,
                "wallets": [],
                "confidence": 0.0
            },
            "security_data": {
                "verified": False,
                "mint_disabled": False,
                "ownership_renounced": False,
                "security_score": 0.0,
                "risk_factors": []
            }
        }

    def _empty_liquidity_metrics(self) -> Dict:
        """
        Return empty liquidity metrics
        """
        return {
            "liquidity_usd": 0.0,
            "liquidity_change_24h": 0.0,
            "locked_ratio": 0.0,
            "lock_duration": 0
        } 