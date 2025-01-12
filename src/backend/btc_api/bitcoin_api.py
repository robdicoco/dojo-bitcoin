from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import ipaddress
from decouple import config

from restrictions import ALLOWED_IPS

app = Flask(__name__)

API_KEY = config("TEST_API_KEY")
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

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
    return jsonify({'message': 'Authentication Required'}), 401


def requires_auth(f):
    """Decorator to check for API key in request headers"""
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return authenticate()
        
        token = auth.split(' ')[1]
        if token != API_KEY:
            return authenticate()
        
        # Check IP address
        if not is_allowed_ip(request.remote_addr):
            return jsonify({'message': 'Forbidden'}), 403 

        return f(*args, **kwargs)
    return decorated


@app.route('/getblockchaininfo', methods=['GET'])
def get_blockchain_info():
    result = subprocess.run(['bitcoin-cli', '-regtest', 'getblockchaininfo'], 
                           stdout=subprocess.PIPE, text=True)
    return jsonify(result.stdout)


@app.route('/getbalance', methods=['GET'])
@requires_auth
def get_balance():
    address = request.args.get('address') 
    result = subprocess.run(['bitcoin-cli', '-regtest', 'getbalance', address], 
                           stdout=subprocess.PIPE, text=True)
    return jsonify(result.stdout)


@app.route('/getblockhash', methods=['GET'])
def get_blockhash():
    block_height = request.args.get('height')
    result = subprocess.run(['bitcoin-cli', '-regtest', 'getblockhash', block_height], 
                           stdout=subprocess.PIPE, text=True)
    return jsonify(result.stdout)


@app.route('/getblock', methods=['GET'])
def get_block():
    block_hash = request.args.get('hash')
    result = subprocess.run(['bitcoin-cli', '-regtest', 'getblock', block_hash], 
                           stdout=subprocess.PIPE, text=True)
    return jsonify(result.stdout)


@app.route('/gettransaction', methods=['GET'])
def get_transaction():
    txid = request.args.get('txid')
    result = subprocess.run(['bitcoin-cli', '-regtest', 'gettransaction', txid], 
                           stdout=subprocess.PIPE, text=True)
    return jsonify(result.stdout)


if __name__ == '__main__':
    app.run(debug=True)