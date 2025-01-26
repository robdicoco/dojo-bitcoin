from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document, Wallet
from ..database import get_db
from ..utils import get_bitcoin_rpc, generate_payment_address
import hashlib
from pydantic import BaseModel

router = APIRouter()


class UploadRequest(BaseModel):
    document: str
    document_hash: str


@router.post("/upload")
async def upload_document(request: UploadRequest, db: Session = Depends(get_db)):
    """
    Upload a document and its SHA-256 hash.
    - Creates a new Bitcoin wallet.
    - Returns the wallet address.
    """
    document = request.document
    document_hash = request.document_hash

    # Validate the document hash
    document_validation_hash = hashlib.sha256(document.encode()).hexdigest()
    if document_validation_hash != document_hash:
        raise HTTPException(
            status_code=400,
            detail=f"Document hash did not match. Informed: {document_hash}, expected: {document_validation_hash}",
        )

    # Check if the document hash already exists
    if db.query(Document).filter(Document.document_hash == document_hash).first():
        raise HTTPException(status_code=400, detail="Document already exists")

    # Create a new wallet
    rpc = get_bitcoin_rpc()
    address = generate_payment_address(rpc)

    # Save document and wallet to the database
    db_document = Document(document_hash=document_hash, wallet_address=address)
    db_wallet = Wallet(address=address, document_hash=document_hash)
    db.add(db_document)
    db.add(db_wallet)
    db.commit()

    return {"address": address}
