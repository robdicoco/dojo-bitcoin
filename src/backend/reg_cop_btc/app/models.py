from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    document_hash = Column(String, unique=True, index=True)
    wallet_address = Column(String)
    status = Column(String, default="Pending Payment")
    tx_id = Column(String, nullable=True)


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    document_hash = Column(String, ForeignKey("documents.document_hash"))
