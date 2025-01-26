from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document
from ..database import get_db
from ..utils import get_bitcoin_rpc, send_op_return_transaction
import time
from pydantic import BaseModel

router = APIRouter()


class SendTransactionRequest(BaseModel):
    document_hash: str


@router.post("/send-transaction")
async def send_transaction(
    request: SendTransactionRequest, db: Session = Depends(get_db)
):
    """
    Send a transaction with the document hash in the OP_RETURN field.
    - Returns the transaction ID (tx_id).
    """
    document_hash = request.document_hash

    # Fetch the document from the database
    document = (
        db.query(Document).filter(Document.document_hash == document_hash).first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Send the OP_RETURN transaction
    rpc = get_bitcoin_rpc()
    try:
        tx_id = send_op_return_transaction(rpc, document_hash)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Update the document with the transaction ID
    document.tx_id = tx_id
    db.commit()

    return {"tx_id": tx_id}
