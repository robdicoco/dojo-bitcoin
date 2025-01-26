from fastapi import FastAPI
from .database import engine, Base
from .endpoints.upload import router as upload_router
from .endpoints.payment import router as payment_router
from .endpoints.transaction import router as transaction_router
from .endpoints.mining import router as mining_router
from .utils import get_bitcoin_rpc
import os

app = FastAPI()

# Include the upload router
app.include_router(upload_router, tags=["upload"])
app.include_router(payment_router, tags=["payment-confirmation"])
app.include_router(transaction_router, tags=["send-transaction"])
app.include_router(mining_router, tags=["mining-confirmation"])


# Create database tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

    # Ensure the Bitcoin wallet exists
    rpc = get_bitcoin_rpc()
    wallet_name = os.getenv("BITCOIN_WALLET_NAME", "registry_wallet")

    try:
        # Check if the wallet is already created
        wallets = rpc.listwallets()
        if wallet_name not in wallets:
            print(f"Wallet '{wallet_name}' not loaded. Creating it...")
            rpc.createwallet(wallet_name)
    except Exception as e:
        if "Wallet file not found" in str(e):
            print(f"Wallet '{wallet_name}' not found.")
            raise e
        elif "Wallet file verification failed" in str(e):
            print(
                f"Wallet '{wallet_name}' verification failed. Creating a new wallet..."
            )
            raise e
        else:
            raise e


@app.get("/")
def read_root():
    return {"message": "Bitcoin Challenge 3 Backend"}
