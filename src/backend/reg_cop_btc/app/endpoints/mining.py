from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..models import Document
from ..database import get_db
from ..utils import get_bitcoin_rpc, check_mining_confirmation
from pydantic import BaseModel

router = APIRouter()


class MiningConfirmationRequest(BaseModel):
    tx_id: str


@router.post("/mining-confirmation")
async def mining_confirmation(
    request: MiningConfirmationRequest, db: Session = Depends(get_db)
):
    """
    Check if the transaction has been confirmed (mined into a block).
    - Update the document status to "Mining Completed".
    """
    tx_id = request.tx_id

    # Fetch the document from the database
    document = db.query(Document).filter(Document.tx_id == tx_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check for mining confirmation
    rpc = get_bitcoin_rpc()
    try:
        if check_mining_confirmation(rpc, tx_id):
            # Update the document status
            document.status = "Mining Completed"
            db.commit()
            return {"status": "Mining Completed"}
        else:
            raise HTTPException(status_code=400, detail="Transaction not yet confirmed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
