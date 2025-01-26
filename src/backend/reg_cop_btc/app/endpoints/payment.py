from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document
from ..database import get_db
from ..utils import get_bitcoin_rpc

router = APIRouter()


@router.post("/payment-confirmation")
async def payment_confirmation(document_hash: str, db: Session = Depends(get_db)):
    """
    Check for payment events to the wallet address associated with the document.
    """
    # Fetch the document from the database
    document = (
        db.query(Document).filter(Document.document_hash == document_hash).first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get the wallet address
    wallet_address = document.wallet_address

    # Use Bitcoin RPC to check for transactions
    rpc = get_bitcoin_rpc()
    try:
        # List transactions for the wallet
        transactions = rpc.listtransactions()

        # Filter transactions for the specific address
        payment_received = False
        for tx in transactions:
            if tx.get("address") == wallet_address and tx.get("category") == "receive":
                # Check if the transaction has at least 1 confirmation
                if tx.get("confirmations", 0) >= 1:
                    payment_received = True
                    break

        if payment_received:
            # Update the document status
            document.status = "Pending Block Mining"
            db.commit()
            return {"status": "Payment Confirmed"}
        else:
            raise HTTPException(
                status_code=400, detail="Payment not found or not confirmed"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
