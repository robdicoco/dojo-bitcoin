from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document
from ..database import get_db
from ..utils import get_bitcoin_rpc, send_op_return_transaction
import time

router = APIRouter()


@router.post("/send-transaction")
async def send_transaction(document_hash: str, db: Session = Depends(get_db)):
    # Fetch document from the database
    document = (
        db.query(Document).filter(Document.document_hash == document_hash).first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Send OP_RETURN transaction
    rpc = get_bitcoin_rpc()
    tx_id = send_op_return_transaction(rpc, document_hash)

    # Wait for mining confirmation (simulated)
    time.sleep(60)

    # Update document status
    document.status = "Mining Completed"
    document.tx_id = tx_id
    db.commit()

    return {"status": "Mining Completed", "tx_id": tx_id}
