from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv
import os

load_dotenv()

def get_bitcoin_rpc():
    rpc_user = os.getenv("BITCOIN_RPC_USER")
    rpc_password = os.getenv("BITCOIN_RPC_PASSWORD")
    rpc_host = os.getenv("BITCOIN_RPC_HOST")
    rpc_port = os.getenv("BITCOIN_RPC_PORT")
    return AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

def create_wallet(rpc):
    address = rpc.getnewaddress()
    return address

def validate_payment(rpc, address, amount):
    transactions = rpc.listtransactions()
    for tx in transactions:
        if tx["address"] == address and tx["amount"] >= amount and tx["confirmations"] > 0:
            return True
    return False

def send_op_return_transaction(rpc, document_hash):
    op_return_data = f"OP_RETURN {document_hash}"
    tx_id = rpc.sendtoaddress(rpc.getnewaddress(), 0.0001, "", "", False, True, 6, "UNSET", op_return_data)
    return tx_id

