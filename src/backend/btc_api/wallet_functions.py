from bitcoinlib.wallets import (
    Wallet,
    wallet_delete_if_exists,
    HDKey,
    wallet_create_or_open,
)
from bitcoinlib.mnemonic import Mnemonic
from cryptography.fernet import Fernet
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os


# Helper function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()


def derive_fernet_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte Fernet key from a user-provided password using PBKDF2HMAC.
    """
    # Convert the password to bytes
    password_bytes = password.encode()

    # Use PBKDF2HMAC to derive a key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes for Fernet
        salt=salt,
        iterations=100000,  # Adjust iterations for security
        backend=default_backend(),
    )
    key = kdf.derive(password_bytes)

    # Encode the key as URL-safe base64
    return base64.urlsafe_b64encode(key)


# Helper function to encrypt data
def encrypt_data(data, password, salt):
    # Derive the Fernet key
    fernet_key = derive_fernet_key(password, salt)
    fernet = Fernet(fernet_key)
    return fernet.encrypt(data.encode())


# Helper function to decrypt data
def decrypt_data(encrypted_data: bytes, password: str, salt: bytes) -> str:
    """
    Decrypt data using a password-derived Fernet key.
    """
    fernet_key = derive_fernet_key(password, salt)
    fernet = Fernet(fernet_key)
    return fernet.decrypt(encrypted_data).decode()


# Helper function to serialize wallet keys
def serialize_keys(db_keys):
    serialized_keys = []
    # Convert each DbKey object to a dictionary
    for db_key in db_keys:
        serialized_keys.append(
            {"id": db_key.id, "name": db_key.name, "wif": db_key.wif}
        )
    return serialized_keys


# Helper function to save wallet as encrypted JSON
def save_wallet(wallet, password):
    wallet_data = {
        "name": wallet.name,
        "keys": serialize_keys(wallet.keys()),
        "transactions": wallet.transactions(),
    }
    salt = os.urandom(16)
    encrypted_data = encrypt_data(json.dumps(wallet_data), password, salt)

    with open(f"{wallet.name}_encrypted.json", "wb") as f:
        f.write(encrypted_data)

    return salt  # Return the salt for storage


# Helper function to load wallet from encrypted JSON
def load_wallet(wallet_name, password, salt):
    with open(f"{wallet_name}_encrypted.json", "rb") as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data, password, salt)
    wallet_data = json.loads(decrypted_data)
    return Wallet(wallet_data["name"], keys=wallet_data["keys"])


# Create or open a wallet with BIP39 mnemonic
def create_or_open_wallet(wallet_name, password):
    # Generate a BIP39 mnemonic
    mnemonic = Mnemonic().generate()
    hdkey = HDKey.from_passphrase(mnemonic)

    # Create or open the wallet
    wallet = wallet_create_or_open(
        name=wallet_name,
        keys=hdkey,
        network="testnet",
        password=password,
    )

    # Save the wallet with a password and get the salt
    salt = save_wallet(wallet, password)

    return {
        "message": "Wallet created or opened successfully",
        "mnemonic": mnemonic,
        "wallet_name": wallet_name,
        "salt": salt.hex(),  # Return the salt as a hex string for storage
    }


# Generate a new address for the wallet
def generate_address(wallet_name, password, salt):
    wallet = load_wallet(wallet_name, password, salt)
    address = wallet.get_key().address
    return {
        "message": "New address generated",
        "address": address,
    }


# List all addresses in the wallet
def list_addresses(wallet_name, password, salt):
    wallet = load_wallet(wallet_name, password, salt)
    addresses = wallet.addresslist()
    return {
        "message": "Addresses listed successfully",
        "addresses": addresses,
    }


# Get wallet balance
def get_balance(wallet_name, password, salt):
    wallet = load_wallet(wallet_name, password, salt)
    balance = wallet.balance()
    return {
        "message": "Balance retrieved successfully",
        "balance": balance,
    }


# Send a transaction
def send_transaction(wallet_name, password, salt, to_address, amount):
    wallet = load_wallet(wallet_name, password, salt)
    if not to_address or not amount:
        raise Exception("Recipient address and amount are required")

    try:
        tx = wallet.send_to(to_address, amount)
        return {
            "message": "Transaction sent successfully",
            "transaction_id": tx.txid,
        }
    except Exception as e:
        raise Exception(str(e))


# Get transaction history for the wallet
def get_transaction_history(wallet_name, password, salt):
    wallet = load_wallet(wallet_name, password, salt)
    transactions = wallet.transactions()
    return {
        "message": "Transaction history retrieved successfully",
        "transactions": transactions,
    }
