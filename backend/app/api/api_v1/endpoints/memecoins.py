from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from app.db.session import get_db
from app.models.memecoin import Memecoin, BlockchainType, MemeStatus
from app.schemas.memecoin import (
    MemecoinCreate,
    MemecoinUpdate,
    MemecoinResponse,
    MemecoinList
)

router = APIRouter()

@router.post("/", response_model=MemecoinResponse, status_code=status.HTTP_201_CREATED)
async def create_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_in: MemecoinCreate
):
    """
    Create new memecoin to track.
    
    Parameters:
    - name: Name of the memecoin
    - symbol: Trading symbol (e.g., DOGE, SHIB)
    - contract_address: Valid blockchain contract address (42-44 chars, starts with 0x for ETH/BSC)
    - blockchain: Network type (ethereum, bsc, solana)
    """
    try:
        # Check if memecoin already exists
        db_memecoin = db.query(Memecoin).filter(
            Memecoin.contract_address == memecoin_in.contract_address
        ).first()
        if db_memecoin:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "msg": "Memecoin with this contract address already exists",
                    "memecoin_id": db_memecoin.id
                }
            )
        
        # Create new memecoin
        db_memecoin = Memecoin(
            name=memecoin_in.name,
            symbol=memecoin_in.symbol,
            contract_address=memecoin_in.contract_address,
            blockchain=memecoin_in.blockchain,
            status=MemeStatus.NEW,
            **memecoin_in.dict(exclude={'name', 'symbol', 'contract_address', 'blockchain'})
        )
        db.add(db_memecoin)
        db.commit()
        db.refresh(db_memecoin)
        return db_memecoin
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "msg": "Validation error",
                "errors": e.errors()
            }
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "Database integrity error",
                "error": str(e)
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": "An error occurred while creating memecoin",
                "error": str(e)
            }
        )

@router.get("/", response_model=List[MemecoinList])
async def list_memecoins(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    blockchain: Optional[BlockchainType] = None,
    status: Optional[MemeStatus] = None,
    min_potential_score: Optional[float] = Query(None, ge=0, le=1)
):
    """
    List all tracked memecoins with optional filters.
    """
    try:
        query = db.query(Memecoin)
        
        if blockchain:
            query = query.filter(Memecoin.blockchain == blockchain)
        if status:
            query = query.filter(Memecoin.status == status)
        if min_potential_score:
            query = query.filter(Memecoin.potential_score >= min_potential_score)
        
        memecoins = query.order_by(Memecoin.created_at.desc()).offset(skip).limit(limit).all()
        return memecoins
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching memecoins: {str(e)}"
        )

@router.get("/{memecoin_id}", response_model=MemecoinResponse)
async def get_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int = Path(..., gt=0, description="The ID of the memecoin to retrieve")
):
    """
    Get detailed information about a specific memecoin.
    """
    try:
        memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
        if not memecoin:
            raise HTTPException(status_code=404, detail="Memecoin not found")
        return memecoin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching memecoin: {str(e)}"
        )

@router.put("/{memecoin_id}", response_model=MemecoinResponse)
async def update_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int = Path(..., gt=0, description="The ID of the memecoin to update"),
    memecoin_in: MemecoinUpdate
):
    """
    Update memecoin information.
    """
    try:
        memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
        if not memecoin:
            raise HTTPException(status_code=404, detail="Memecoin not found")
        
        # Update memecoin attributes
        update_data = memecoin_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(memecoin, field, value)
        
        db.add(memecoin)
        db.commit()
        db.refresh(memecoin)
        return memecoin
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating memecoin: {str(e)}"
        )

@router.delete("/{memecoin_id}")
async def delete_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int = Path(..., gt=0, description="The ID of the memecoin to delete")
):
    """
    Delete a memecoin from tracking.
    """
    try:
        memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
        if not memecoin:
            raise HTTPException(status_code=404, detail="Memecoin not found")
        
        db.delete(memecoin)
        db.commit()
        return {"message": "Memecoin deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete memecoin due to existing references: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting memecoin: {str(e)}"
        ) 