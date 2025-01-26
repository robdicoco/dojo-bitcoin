from fastapi import FastAPI
from .database import engine, Base
from .endpoints import upload, payment, transaction
from .utils import get_bitcoin_rpc
import os

app = FastAPI()

# Include the upload router
app.include_router(upload.router, tags=["upload"])
app.include_router(payment.router, prefix="/payment", tags=["payment"])
app.include_router(transaction.router, prefix="/transaction", tags=["transaction"])


# Create database tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

    # Ensure the Bitcoin wallet exists
    rpc = get_bitcoin_rpc()
    wallet_name = os.getenv("BITCOIN_WALLET_NAME", "registry_wallet")
    try:
        rpc.loadwallet(wallet_name)
    except Exception as e:
        if "Wallet file not found" in str(e):
            print(f"Wallet '{wallet_name}' not found. Creating it...")
            rpc.createwallet(wallet_name)
        elif "Wallet file verification failed" in str(e):
            print(
                f"Wallet '{wallet_name}' verification failed. Creating a new wallet..."
            )
            rpc.createwallet(wallet_name)
        else:
            raise e


@app.get("/")
def read_root():
    return {"message": "Bitcoin Challenge Backend"}
