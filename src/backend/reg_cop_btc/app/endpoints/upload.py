from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Document, Wallet
from ..database import get_db
from ..utils import get_bitcoin_rpc, create_wallet
import hashlib

router = APIRouter()


@router.post("/upload")
async def upload_document(document: str, db: Session = Depends(get_db)):
    # Generate SHA-256 hash
    document_hash = hashlib.sha256(document.encode()).hexdigest()

    # Check if document already exists
    if db.query(Document).filter(Document.document_hash == document_hash).first():
        raise HTTPException(status_code=400, detail="Document already exists")

    # Create a new wallet
    rpc = get_bitcoin_rpc()
    address = create_wallet(rpc)

    # Save document and wallet to the database
    db_document = Document(document_hash=document_hash, wallet_address=address)
    db_wallet = Wallet(address=address, document_hash=document_hash)
    db.add(db_document)
    db.add(db_wallet)
    db.commit()

    return {"address": address, "hash": document_hash}
