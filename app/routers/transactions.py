from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TransactionRequest(BaseModel):
    title: str
    amount: float
    type: str
    date: str

@router.get("/")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    return transactions

@router.post("/")
def create_transaction(user_id: int, request: TransactionRequest, db: Session = Depends(get_db)):
    transaction = Transaction(
        user_id=user_id,
        title=request.title,
        amount=request.amount,
        type=request.type,
        date=request.date,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}