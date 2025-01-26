from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document
from ..database import get_db
from ..utils import get_bitcoin_rpc, validate_payment

router = APIRouter()


@router.post("/payment-confirmation")
async def payment_confirmation(document_hash: str, db: Session = Depends(get_db)):
    # Fetch document from the database
    document = (
        db.query(Document).filter(Document.document_hash == document_hash).first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Validate payment
    rpc = get_bitcoin_rpc()
    if validate_payment(rpc, document.wallet_address, 0.0001):
        document.status = "Pending Block Mining"
        db.commit()
        return {"status": "Payment Confirmed"}

    raise HTTPException(status_code=400, detail="Payment not found")
