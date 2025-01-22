from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import ipaddress
import json
from decouple import config
import logging
import traceback
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from urllib.parse import quote

from restrictions import ALLOWED_IPS


# Configuration
app = Flask(__name__)
API_KEY = config("TEST_API_KEY")
RPC_USER = config("RPC_USER", default="bitcoin")  # RPC username
RPC_PASS = config("RPC_PASS")  # RPC password
RPC_HOST = config("RPC_HOST", default="127.0.0.1")  # RPC host
RPC_PORT = config("RPC_PORT", default="8332")  # RPC port
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Initialize Bitcoin Core RPC connection
def get_rpc_connection(wallet_name=None):
    try:
        # Ensure RPC_PORT is a valid integer
        port = int(RPC_PORT)
    except ValueError:
        logging.error(f"Invalid RPC_PORT value: {RPC_PORT}. Using default port.")
        port = 18443  # Default port

    # URL-encode the password to handle special characters
    encoded_password = quote(RPC_PASS, safe="")

    # Construct the RPC URL
    if wallet_name:
        rpc_url = f"http://{RPC_USER}:{encoded_password}@{RPC_HOST}:{port}/wallet/{wallet_name}"
    else:
        rpc_url = f"http://{RPC_USER}:{encoded_password}@{RPC_HOST}:{port}"

    # logging.debug(f"RPC URL: {rpc_url}")  # Log the RPC URL for debugging
    return AuthServiceProxy(rpc_url)


# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


# Helper functions
def is_allowed_ip(ip):
    """Check if the request IP is in the allowlist."""
    try:
        ip_address = ipaddress.ip_address(ip)
        for allowed_ip in ALLOWED_IPS:
            if ip_address in ipaddress.ip_network(allowed_ip):
                return True
        return False
    except ValueError:
        return False


def authenticate():
    """Send a 401 response that enables basic auth."""
    return jsonify({"message": "Authentication Required"}), 401


def requires_auth(f):
    """Decorator to check for API key in request headers."""

    def decorated_function(*args, **kwargs):
        if not DEBUG_MODE:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return authenticate()

            token = auth.split(" ")[1]
            if token != API_KEY:
                return authenticate()

            if not is_allowed_ip(request.remote_addr):
                return jsonify({"message": "Forbidden"}), 403

        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__ + "_decorated"
    return decorated_function


# def get_scriptPubKey_from_validateaddress(response_str):
#     try:
#         response_data = json.loads(response_str)
#         validation = response_data.get("isvalid")
#         if validation == True:
#             scriptPubKey = response_data.get("scriptPubKey")
#             return (True, scriptPubKey)
#         else:
#             return (False, None)
#     except json.JSONDecodeError:
#         print("Error: Invalid JSON string.")
#         return (None, None)


# def get_balance_from_scantxoutset(response_str):
#     try:
#         response_data = json.loads(response_str)
#         amount = response_data.get("total_amount")
#         return amount
#     except json.JSONDecodeError:
#         print("Error: Invalid JSON string.")
#         return "0"


# RPC-based wallet functions
@app.route("/create_wallet", methods=["POST"])
@requires_auth
def create_wallet():
    data = request.get_json()
    wallet_name = data.get("wallet_name")

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection()  # Use default RPC URL for wallet creation

        # Check if the wallet already exists
        wallets = rpc.listwallets()
        if wallet_name in wallets:
            return jsonify({"message": f"Wallet {wallet_name} already exists"}), 200

        # Create the wallet
        rpc.createwallet(wallet_name)

        # Load the wallet to ensure it's available for future RPC calls
        rpc.loadwallet(wallet_name)

        return jsonify(
            {"message": f"Wallet {wallet_name} created and loaded successfully"}
        )

    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/generate_address", methods=["POST"])
@requires_auth
def generate_address():
    data = request.get_json()
    wallet_name = data.get("wallet_name")

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        address = rpc.getnewaddress()
        return jsonify({"message": "New address generated", "address": address})

    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/get_balance", methods=["GET"])
@requires_auth
def get_balance():
    wallet_name = request.args.get("wallet_name")
    minconf = request.args.get("minconf", default=0, type=int)  # Default: 0
    include_watchonly = request.args.get(
        "include_watchonly", default=False, type=bool
    )  # Default: False
    avoid_reuse = request.args.get(
        "avoid_reuse", default=False, type=bool
    )  # Default: False

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        balance = rpc.getbalance("*", minconf, include_watchonly, avoid_reuse)
        return jsonify({"balance": balance})

    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/send_transaction", methods=["POST"])
@requires_auth
def send_transaction():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    to_address = data.get("to_address")
    amount = data.get("amount")

    if not wallet_name or not to_address or not amount:
        return (
            jsonify({"error": "Wallet name, to_address, and amount are required"}),
            400,
        )

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        txid = rpc.sendtoaddress(to_address, amount)
        return jsonify({"message": "Transaction sent successfully", "txid": txid})

    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/get_transaction_history", methods=["GET"])
@requires_auth
def get_transaction_history():
    wallet_name = request.args.get("wallet_name")

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        transactions = rpc.listtransactions(wallet_name)
        return jsonify({"transactions": transactions})

    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/mine", methods=["POST"])
@requires_auth
def mine():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    num_blocks = data.get("num_blocks", 1)

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        address = rpc.getnewaddress(wallet_name)
        block_hashes = rpc.generatetoaddress(num_blocks, address)
        return jsonify(
            {"message": "Block mined successfully", "block_hashes": block_hashes}
        )
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# ------------------


# Blockchain-related functions
@app.route("/getblockchaininfo", methods=["GET"])
@requires_auth
def get_blockchain_info():
    try:
        rpc = get_rpc_connection()
        blockchain_info = rpc.getblockchaininfo()
        return jsonify(blockchain_info)
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/getblockhash", methods=["GET"])
@requires_auth
def get_blockhash():
    block_height = request.args.get("height")

    if not block_height:
        return jsonify({"error": "Block height is required"}), 400

    try:
        rpc = get_rpc_connection()
        block_hash = rpc.getblockhash(int(block_height))
        return jsonify({"blockhash": block_hash})
    except JSONRPCException as e:
        return jsonify({"error": str(e)}), 500


# @app.route("/getbalance", methods=["GET"])
# @requires_auth
# def get_balance():
#     address = request.args.get("address")
#     if not address:
#         return jsonify({"error": "Address parameter is required"}), 400

#     result1 = subprocess.run(
#         ["bitcoin-cli", "-regtest", "validateaddress", address],
#         stdout=subprocess.PIPE,
#         text=True,
#     )

#     (isvalid, scriptPubKey) = get_scriptPubKey_from_validateaddress(result1.stdout)

#     if isvalid is None:
#         return jsonify({"error": "Internal server error"}), 500
#     elif isvalid is False:
#         return jsonify({"error": "Invalid address"}), 400
#     else:
#         data = '[{"desc": "raw(' + scriptPubKey + ')"}]'
#         result2 = subprocess.run(
#             ["bitcoin-cli", "-regtest", "scantxoutset", "start", data],
#             stdout=subprocess.PIPE,
#             text=True,
#         )
#         try:
#             balance_data = json.loads(result2.stdout)
#             balance = balance_data.get("total_amount", "0")
#             return jsonify({"balance": balance})
#         except json.JSONDecodeError:
#             return jsonify({"error": "Failed to parse balance data"}), 500


@app.route("/getblock", methods=["GET"])
@requires_auth
def get_block():
    block_hash = request.args.get("hash")

    if not block_hash:
        return jsonify({"error": "Block hash is required"}), 400

    try:
        rpc = get_rpc_connection()
        block_data = rpc.getblock(block_hash)
        return jsonify(block_data)
    except JSONRPCException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/gettransaction", methods=["GET"])
@requires_auth
def get_transaction():
    txid = request.args.get("txid")

    if not txid:
        return jsonify({"error": "Transaction ID is required"}), 400

    try:
        rpc = get_rpc_connection()  # No wallet_name needed for getrawtransaction
        raw_transaction = rpc.getrawtransaction(txid)
        decoded_transaction = rpc.decoderawtransaction(raw_transaction)
        return jsonify(decoded_transaction)
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/getrawtransaction", methods=["GET"])
@requires_auth
def get_raw_transaction():
    txid = request.args.get("txid")

    if not txid:
        return jsonify({"error": "Transaction ID is required"}), 400

    try:
        rpc = get_rpc_connection()
        raw_transaction = rpc.getrawtransaction(txid)
        return jsonify({"raw_transaction": raw_transaction})
    except JSONRPCException as e:
        return jsonify({"error": str(e)}), 500


@requires_auth
def list_wallets():
    try:
        rpc = get_rpc_connection()  # No wallet_name needed for listwallets
        wallets = rpc.listwallets()
        return jsonify({"wallets": wallets})
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/generate_multi_address", methods=["POST"])
@requires_auth
def generate_multi_address():
    data = request.get_json()
    wallet_name = data.get("wallet_name")
    num_addresses = data.get("num_addresses", 1)  # Default: 1 address

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    if num_addresses < 1 or num_addresses > 100:
        return jsonify({"error": "Number of addresses must be between 1 and 100"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        addresses = [rpc.getnewaddress() for _ in range(num_addresses)]
        return jsonify(
            {"message": "Addresses generated successfully", "addresses": addresses}
        )
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/list_addresses", methods=["GET"])
@requires_auth
def list_addresses():
    wallet_name = request.args.get("wallet_name")

    if not wallet_name:
        return jsonify({"error": "Wallet name is required"}), 400

    try:
        rpc = get_rpc_connection(wallet_name)  # Pass wallet_name to get_rpc_connection
        addresses = rpc.getaddressesbylabel(
            ""
        )  # Use default label to get all addresses
        return jsonify(
            {
                "message": "Addresses listed successfully",
                "addresses": list(addresses.keys()),
            }
        )
    except JSONRPCException as e:
        logging.error(f"RPC Error: {str(e)}")
        return jsonify({"error": f"RPC Error: {str(e)}"}), 500
    except ConnectionError as e:
        logging.error(f"Connection Error: {str(e)}")
        return jsonify({"error": "Failed to connect to Bitcoin Core RPC server"}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # context=('/home/robdc/apps/keys/server.crt', '/home/robdc/apps/keys/server.key'))
    context = (
        "/home/robdc/apps/keys/fullchain.pem",
        "/home/robdc/apps/keys/privkey.pem",
    )
    app.run(host="0.0.0.0", port=5000, debug=DEBUG_MODE, ssl_context=context)

    # app.run(debug=DEBUG_MODE)
    #  app.run(host= '0.0.0.0', port=5000, debug=DEBUG_MODE)
