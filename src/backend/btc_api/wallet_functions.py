from bitcoinlib.wallets import Wallet, wallet_delete_if_exists, HDKey
from bitcoinlib.mnemonic import Mnemonic

# Global wallet variable to maintain session
current_wallet = None


# Helper function to encrypt and save wallet
def save_wallet(wallet, password):
    wallet.export_to_encrypted_json(password, filename=f"{wallet.name}_encrypted.json")


# Helper function to load wallet from encrypted file
def load_wallet(wallet_name, password):
    return Wallet.import_from_encrypted_json(wallet_name, password)


# Create a new wallet with BIP39 mnemonic
def create_wallet(wallet_name, password):
    global current_wallet

    # Generate a BIP39 mnemonic
    mnemonic = Mnemonic().generate()
    hdkey = HDKey.from_passphrase(mnemonic)

    # Create a new wallet
    wallet_delete_if_exists(wallet_name)  # Delete if wallet already exists
    current_wallet = Wallet.create(wallet_name, keys=hdkey, network="testnet")

    # Save the wallet with a password
    save_wallet(current_wallet, password)

    return {
        "message": "Wallet created successfully",
        "mnemonic": mnemonic,
        "wallet_name": wallet_name,
    }


# Load a wallet from an HDKey
def load_wallet_route(wallet_name, password):
    global current_wallet

    try:
        current_wallet = load_wallet(wallet_name, password)
        return {
            "message": "Wallet loaded successfully",
            "wallet_name": wallet_name,
        }
    except Exception as e:
        raise Exception(str(e))


# Generate a new address for the wallet
def generate_address():
    global current_wallet
    if not current_wallet:
        raise Exception("No wallet loaded")

    address = current_wallet.get_key().address
    return {
        "message": "New address generated",
        "address": address,
    }


# List all addresses in the wallet
def list_addresses():
    global current_wallet
    if not current_wallet:
        raise Exception("No wallet loaded")

    addresses = current_wallet.addresslist()
    return {
        "message": "Addresses listed successfully",
        "addresses": addresses,
    }


# Get wallet balance
def get_balance():
    global current_wallet
    if not current_wallet:
        raise Exception("No wallet loaded")

    balance = current_wallet.balance()
    return {
        "message": "Balance retrieved successfully",
        "balance": balance,
    }


# Send a transaction
def send_transaction(to_address, amount):
    global current_wallet
    if not current_wallet:
        raise Exception("No wallet loaded")

    if not to_address or not amount:
        raise Exception("Recipient address and amount are required")

    try:
        tx = current_wallet.send_to(to_address, amount)
        return {
            "message": "Transaction sent successfully",
            "transaction_id": tx.txid,
        }
    except Exception as e:
        raise Exception(str(e))


# Get transaction history for the wallet
def get_transaction_history():
    global current_wallet
    if not current_wallet:
        raise Exception("No wallet loaded")

    transactions = current_wallet.transactions()
    return {
        "message": "Transaction history retrieved successfully",
        "transactions": transactions,
    }
