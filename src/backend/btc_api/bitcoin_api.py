from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import ipaddress
import json
from decouple import config
from bitcoinrpc.authproxy import (
    AuthServiceProxy,
)  # Replace bitcoinlib with python-bitcoinrpc
from urllib.parse import quote

from restrictions import ALLOWED_IPS

app = Flask(__name__)

API_KEY = config("TEST_API_KEY")
RPC_USER = config("RPC_USER", default="bitcoinlib")  # RPC username
RPC_PASS = config("RPC_PASS")  # RPC password
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Initialize RPC connection
encoded_rpc_pass = quote(RPC_PASS)
rpc_connection = AuthServiceProxy(
    f"http://{RPC_USER}:{encoded_rpc_pass}@127.0.0.1:18443/"
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
    try:
        blockchain_info = rpc_connection.getblockchaininfo()
        return jsonify(blockchain_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getbalance", methods=["GET"])
@requires_auth
def get_balance():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400

    try:
        # Validate address
        validate_address = rpc_connection.validateaddress(address)
        if not validate_address.get("isvalid"):
            return jsonify({"error": "Invalid address"}), 400

        # Get balance
        balance = rpc_connection.getreceivedbyaddress(
            address, 0
        )  # 0 for minimum confirmations
        return jsonify({"balance": balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getblockhash", methods=["GET"])
@requires_auth
def get_blockhash():
    block_height = request.args.get("height")
    if not block_height:
        return jsonify({"error": "Height parameter is required"}), 400

    try:
        block_hash = rpc_connection.getblockhash(int(block_height))
        return jsonify({"blockhash": block_hash})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getblock", methods=["GET"])
@requires_auth
def get_block():
    block_hash = request.args.get("hash")
    if not block_hash:
        return jsonify({"error": "Hash parameter is required"}), 400

    try:
        block_info = rpc_connection.getblock(block_hash)
        return jsonify(block_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/gettransaction", methods=["GET"])
@requires_auth
def get_transaction():
    txid = request.args.get("txid")
    if not txid:
        return jsonify({"error": "Transaction ID parameter is required"}), 400

    try:
        transaction_info = rpc_connection.getrawtransaction(
            txid, 1
        )  # 1 for verbose output
        return jsonify(transaction_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getrawtransaction", methods=["GET"])
@requires_auth
def get_raw_transaction():
    txid = request.args.get("txid")
    if not txid:
        return jsonify({"error": "Transaction ID parameter is required"}), 400

    try:
        raw_transaction = rpc_connection.getrawtransaction(txid)
        return jsonify({"raw_transaction": raw_transaction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_addresses", methods=["POST"])
@requires_auth
def generate_addresses():
    try:
        data = request.get_json()
        count = data.get("count", 1)

        addresses = []
        for _ in range(count):
            address = rpc_connection.getnewaddress()
            addresses.append(address)

        return jsonify({"addresses": addresses})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/check_balance", methods=["GET"])
@requires_auth
def check_balance():
    try:
        address = request.args.get("address")
        if not address:
            return jsonify({"error": "Address parameter is required"}), 400

        balance = rpc_connection.getreceivedbyaddress(
            address, 0
        )  # 0 for minimum confirmations
        return jsonify({"balance": balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/send_transaction", methods=["POST"])
@requires_auth
def send_transaction():
    try:
        data = request.get_json()
        from_address = data.get("from_address")
        to_address = data.get("to_address")
        amount = data.get("amount")

        if not from_address or not to_address or not amount:
            return (
                jsonify({"error": "from_address, to_address, and amount are required"}),
                400,
            )

        # Send transaction
        txid = rpc_connection.sendtoaddress(to_address, amount)
        return jsonify({"txid": txid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # context=('/home/robdc/apps/keys/server.crt', '/home/robdc/apps/keys/server.key'))
    # context = (
    #     "/home/robdc/apps/keys/fullchain.pem",
    #     "/home/robdc/apps/keys/privkey.pem",
    # )
    # app.run(host="0.0.0.0", port=5000, debug=DEBUG_MODE, ssl_context=context)

    app.run(debug=DEBUG_MODE)
    #  app.run(host= '0.0.0.0', port=5000, debug=DEBUG_MODE)
