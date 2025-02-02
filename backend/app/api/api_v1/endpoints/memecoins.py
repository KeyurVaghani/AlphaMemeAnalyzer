from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.memecoin import Memecoin, BlockchainType, MemeStatus
from app.schemas.memecoin import (
    MemecoinCreate,
    MemecoinUpdate,
    MemecoinResponse,
    MemecoinList
)

router = APIRouter()

@router.post("/", response_model=MemecoinResponse)
def create_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_in: MemecoinCreate
):
    """
    Create new memecoin to track.
    """
    # Check if memecoin already exists
    db_memecoin = db.query(Memecoin).filter(
        Memecoin.contract_address == memecoin_in.contract_address
    ).first()
    if db_memecoin:
        raise HTTPException(
            status_code=400,
            detail="Memecoin with this contract address already exists"
        )
    
    # Create new memecoin
    db_memecoin = Memecoin(
        name=memecoin_in.name,
        symbol=memecoin_in.symbol,
        contract_address=memecoin_in.contract_address,
        blockchain=memecoin_in.blockchain,
        status=MemeStatus.NEW
    )
    db.add(db_memecoin)
    db.commit()
    db.refresh(db_memecoin)
    return db_memecoin

@router.get("/", response_model=List[MemecoinList])
def list_memecoins(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    blockchain: Optional[BlockchainType] = None,
    status: Optional[MemeStatus] = None,
    min_potential_score: Optional[float] = None
):
    """
    List all tracked memecoins with optional filters.
    """
    query = db.query(Memecoin)
    
    if blockchain:
        query = query.filter(Memecoin.blockchain == blockchain)
    if status:
        query = query.filter(Memecoin.status == status)
    if min_potential_score:
        query = query.filter(Memecoin.potential_score >= min_potential_score)
    
    memecoins = query.offset(skip).limit(limit).all()
    return memecoins

@router.get("/{memecoin_id}", response_model=MemecoinResponse)
def get_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int
):
    """
    Get detailed information about a specific memecoin.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    return memecoin

@router.put("/{memecoin_id}", response_model=MemecoinResponse)
def update_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int,
    memecoin_in: MemecoinUpdate
):
    """
    Update memecoin information.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    # Update memecoin attributes
    for field, value in memecoin_in.dict(exclude_unset=True).items():
        setattr(memecoin, field, value)
    
    db.add(memecoin)
    db.commit()
    db.refresh(memecoin)
    return memecoin

@router.delete("/{memecoin_id}")
def delete_memecoin(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int
):
    """
    Delete a memecoin from tracking.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    db.delete(memecoin)
    db.commit()
    return {"message": "Memecoin deleted successfully"}

@router.get("/", response_model=List[MemecoinResponse])
def get_memecoins(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve memecoins with pagination.
    """
    memecoins = db.query(Memecoin).offset(skip).limit(limit).all()
    return memecoins

@router.post("/", response_model=MemecoinResponse)
def create_memecoin(
    memecoin: MemecoinCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new memecoin.
    """
    db_memecoin = Memecoin(**memecoin.dict())
    db.add(db_memecoin)
    db.commit()
    db.refresh(db_memecoin)
    return db_memecoin

@router.get("/{memecoin_id}", response_model=MemecoinResponse)
def get_memecoin(
    memecoin_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific memecoin by ID.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    return memecoin

@router.put("/{memecoin_id}", response_model=MemecoinResponse)
def update_memecoin(
    memecoin_id: int,
    memecoin_update: MemecoinUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a memecoin.
    """
    db_memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not db_memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    for field, value in memecoin_update.dict(exclude_unset=True).items():
        setattr(db_memecoin, field, value)
    
    db.commit()
    db.refresh(db_memecoin)
    return db_memecoin 