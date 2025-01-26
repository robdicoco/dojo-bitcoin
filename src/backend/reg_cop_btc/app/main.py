from fastapi import FastAPI
from .database import engine, Base
from .endpoints import upload, payment, transaction

app = FastAPI()

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(payment.router, prefix="/payment", tags=["payment"])
app.include_router(transaction.router, prefix="/transaction", tags=["transaction"])

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Copyright Registration with Bitcoin Backend"}
