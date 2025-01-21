from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import ipaddress
import json
from decouple import config
from bitcoinlib.wallets import Wallet, wallet_delete_if_exists
from bitcoinlib.services.services import Service
import logging
import traceback

from restrictions import ALLOWED_IPS
from wallet_functions import (
    create_or_open_wallet,
    generate_address,
    list_addresses,
    get_wallet_balance,
    send_transaction,
    get_transaction_history,
    load_wallet,
    mine,
)

app = Flask(__name__)

API_KEY = config("TEST_API_KEY")
RPC_USER = config("RPC_USER", default="bitcoinlib")  # RPC username
RPC_PASS = config("RPC_PASS")  # RPC password
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

# Configure logging to capture more details
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

network = "regtest"
# Use regtest network
# service = Service(network="regtest")
service = Service(network=network, providers="bitcoind")
logging.debug("Service initialized successfully.")
print("Blockcount:", service.blockcount())

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


def get_scriptPubKey_from_validateaddress(response_str):
    try:
        response_data = json.loads(response_str)
        validation = response_data.get("isvalid")
        if validation == True:
            scriptPubKey = response_data.get("scriptPubKey")
            return (True, scriptPubKey)
        else:
            return (False, None)
    except json.JSONDecodeError:
        print("Error: Invalid JSON string.")
        return (None, None)


def get_balance_from_scantxoutset(response_str):
    try:
        response_data = json.loads(response_str)
        amount = response_data.get("total_amount")
        return amount
    except json.JSONDecodeError:
        print("Error: Invalid JSON string.")
        return "0"


def is_allowed_ip(ip):
    """Checks if the request IP is in the allowlist"""
    try:
        ip_address = ipaddress.ip_address(ip)
        for allowed_ip in ALLOWED_IPS:
            if ip_address in ipaddress.ip_network(allowed_ip):
                return True
        return False
    except ValueError:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return jsonify({"message": "Authentication Required"}), 401


def requires_auth(f):
    """Decorator to check for API key in request headers"""

    def decorated_function(*args, **kwargs):
        if not DEBUG_MODE:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return authenticate()

            token = auth.split(" ")[1]
            if token != API_KEY:
                return authenticate()

            # Check IP address
            if not is_allowed_ip(request.remote_addr):
                return jsonify({"message": "Forbidden"}), 403

        return f(*args, **kwargs)

    # Assign a unique name to the decorated function
    decorated_function.__name__ = f.__name__ + "_decorated"
    return decorated_function


@app.route("/getblockchaininfo", methods=["GET"])
@requires_auth
def get_blockchain_info():
    result = subprocess.run(
        ["bitcoin-cli", "-regtest", "getblockchaininfo"],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse blockchain info"}), 500


@app.route("/getbalance", methods=["GET"])
@requires_auth
def get_balance():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400

    result1 = subprocess.run(
        ["bitcoin-cli", "-regtest", "validateaddress", address],
        stdout=subprocess.PIPE,
        text=True,
    )

    (isvalid, scriptPubKey) = get_scriptPubKey_from_validateaddress(result1.stdout)

    if isvalid is None:
        return jsonify({"error": "Internal server error"}), 500
    elif isvalid is False:
        return jsonify({"error": "Invalid address"}), 400
    else:
        data = '[{"desc": "raw(' + scriptPubKey + ')"}]'
        result2 = subprocess.run(
            ["bitcoin-cli", "-regtest", "scantxoutset", "start", data],
            stdout=subprocess.PIPE,
            text=True,
        )
        try:
            balance_data = json.loads(result2.stdout)
            balance = balance_data.get("total_amount", "0")
            return jsonify({"balance": balance})
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse balance data"}), 500


@app.route("/getblockhash", methods=["GET"])
@requires_auth
def get_blockhash():
    block_height = request.args.get("height")
    if not block_height:
        return jsonify({"error": "Height parameter is required"}), 400

    result = subprocess.run(
        ["bitcoin-cli", "-regtest", "getblockhash", block_height],
        stdout=subprocess.PIPE,
        text=True,
    )
    return jsonify({"blockhash": result.stdout.strip()})


@app.route("/getblock", methods=["GET"])
@requires_auth
def get_block():
    block_hash = request.args.get("hash")
    if not block_hash:
        return jsonify({"error": "Hash parameter is required"}), 400

    result = subprocess.run(
        ["bitcoin-cli", "-regtest", "getblock", block_hash],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse block data"}), 500


@app.route("/gettransaction", methods=["GET"])
@requires_auth
def get_transaction():
    txid = request.args.get("txid")
    if not txid:
        return jsonify({"error": "Transaction ID parameter is required"}), 400

    result1 = subprocess.run(
        ["bitcoin-cli", "-regtest", "getrawtransaction", txid],
        stdout=subprocess.PIPE,
        text=True,
    )

    if result1.stdout == "":
        return jsonify({"error": "Invalid transaction ID"}), 400

    result2 = subprocess.run(
        ["bitcoin-cli", "-regtest", "decoderawtransaction", result1.stdout.strip("\n")],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        data = json.loads(result2.stdout)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse transaction data"}), 500


@app.route("/getrawtransaction", methods=["GET"])
@requires_auth
def get_raw_transaction():
    txid = request.args.get("txid")
    if not txid:
        return jsonify({"error": "Transaction ID parameter is required"}), 400

    result1 = subprocess.run(
        ["bitcoin-cli", "-regtest", "getrawtransaction", txid],
        stdout=subprocess.PIPE,
        text=True,
    )
    return jsonify({"raw_transaction": result1.stdout.strip()})


@app.route("/mint", methods=["GET"])
@requires_auth
def block_gen():
    try:
        data = request.get_json()
        wallet_name = data.get("wallet_name")
        password = data.get("password")
        salt = data.get("salt")

        if not wallet_name or not password or not salt:
            return (
                jsonify({"error": "Wallet name, password, and salt are required"}),
                400,
            )

        result = mine(wallet_name, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/check_balance", methods=["GET"])
@requires_auth
def check_balance():
    try:
        address = request.args.get("address")
        if not address:
            return jsonify({"error": "Address parameter is required"}), 400

        # service = Service()
        balance = service.getbalance(address)

        return jsonify({"balance": balance})
    except Exception as e:
        logging.debug(traceback.format_exc())

        return jsonify({"error": str(e)}), 500


# Create or open a wallet with BIP39 mnemonic
@app.route("/create_wallet", methods=["POST"])
def create_wallet_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")

    if not wallet_name or not password:
        return jsonify({"error": "Wallet name and password are required"}), 400

    try:
        result = create_or_open_wallet(wallet_name, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Load a wallet from an HDKey
@app.route("/load_wallet", methods=["POST"])
def load_wallet_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")

    if not wallet_name or not password or not salt:
        return jsonify({"error": "Wallet name, password, and salt are required"}), 400

    try:
        result = load_wallet(wallet_name, password, salt)

        if result is None:
            return jsonify({"error": "Wallet could not be loaded"})
        else:
            return jsonify(
                {
                    "message": "Wallet loaded successfully",
                    "wallet_name": result.name,
                    "addresses": result.addresslist(),
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Generate a new address for the wallet
@app.route("/generate_address", methods=["POST"])
def generate_address_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")
    num_addresses = data.get("num_addresses")

    if not wallet_name or not password or not salt or not num_addresses:
        return (
            jsonify(
                {
                    "error": "Wallet name, password, and salt  and num_addresses are required"
                }
            ),
            400,
        )

    if int(num_addresses) < 0:
        return jsonify({"error": "num_addresses must be 1 or higher"}), 400

    if int(num_addresses) > 30:
        return jsonify({"error": "num_addresses must be lower than 31"}), 400

    try:
        result = generate_address(wallet_name, password, salt, num_addresses)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# List all addresses in the wallet
@app.route("/list_addresses", methods=["POST"])
def list_addresses_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")

    if not wallet_name or not password or not salt:
        return jsonify({"error": "Wallet name, password, and salt are required"}), 400

    try:
        result = list_addresses(wallet_name, password, salt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get wallet balance
@app.route("/get_wallet_balance", methods=["POST"])
def get_wallet_balance_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")

    if not wallet_name or not password or not salt:
        return jsonify({"error": "Wallet name, password, and salt are required"}), 400

    try:
        result = get_wallet_balance(wallet_name, password, salt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Send a transaction
@app.route("/send_transaction", methods=["POST"])
def send_transaction_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")
    to_address = data.get("to_address")
    amount = data.get("amount")

    if not wallet_name or not password or not salt or not to_address or not amount:
        return (
            jsonify(
                {
                    "error": "Wallet name, password, salt, recipient address, and amount are required"
                }
            ),
            400,
        )

    try:
        result = send_transaction(wallet_name, password, salt, to_address, amount)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get transaction history for the wallet
@app.route("/get_transaction_history", methods=["POST"])
def get_transaction_history_route():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    password = data.get("password")
    salt = data.get("salt")

    if not wallet_name or not password or not salt:
        return jsonify({"error": "Wallet name, password, and salt are required"}), 400

    try:
        result = get_transaction_history(wallet_name, password, salt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # context=('/home/robdc/apps/keys/server.crt', '/home/robdc/apps/keys/server.key'))
    context = (
        "/home/robdc/apps/keys/fullchain.pem",
        "/home/robdc/apps/keys/privkey.pem",
    )
    app.run(host="0.0.0.0", port=5000, debug=DEBUG_MODE, ssl_context=context)

    # app.run(debug=DEBUG_MODE)
    #  app.run(host= '0.0.0.0', port=5000, debug=DEBUG_MODE)
