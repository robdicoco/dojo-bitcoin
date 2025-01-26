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
    - Wait for mining confirmation.
    - Update the document status to "Mining Completed".
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

    # Wait for mining confirmation (simulate by mining a block)
    rpc.generatetoaddress(1, rpc.getnewaddress())

    # Update the document status
    document.status = "Mining Completed"
    document.tx_id = tx_id
    db.commit()

    return {"status": "Mining Completed", "tx_id": tx_id}
