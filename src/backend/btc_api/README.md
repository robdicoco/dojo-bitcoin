# Shi(し) Satoshi - Backend Info

## Description:

This repository contains a Python API for interacting with a Bitcoin node in regtest mode. The API provides endpoints for querying blockchain information, transactions, and address balances using Bitcoin Core. This project was developed as part of the Shi Satoshi - NearX Challenge on the Bitcoin Dojo.

## Prerequisites

-   Python: Version 3.10 or higher.
-   Bitcoin Core: Configured in regtest
    mode.
-   Python Libraries: Install the dependencies listed in the
    pyproject.toml file.
-   Operating System Dependencies:
    -   Make sure the following packages are installed:
        -   ca-certificates
        -   gnupg
        -   gpg
        -   wget
        -   jq

## Setup

### Clone the Repository:

```sh
git clone https://github.com/robdicoco/dojo-bitcoin.git
cd dojo-bitcoin/src/backend/btc_api
```

### Set up the Python Environment:

```bash
uv venv --python 3.10
```

### Set up Bitcoin Core:

Make sure the bitcoin.conf file is configured in the data directory:

    regtest=1
    server=1
    rpcuser=satoshi
    rpcpassword=password123

### Start the Bitcoin node:

```bash
bitcoind -regtest -daemon
```

### Set Environment Variables:

Create a .env file in the application root directory:

    TEST_API_KEY=your_api_token
    DEBUG_MODE=True

## How to Run

Start the Flask server:
uv run bitcoin_api.py

### Access the API endpoints at the following URLs Endpoints:

#### Query Blockchain Information:

Returns general information about the blockchain in regtest mode.

    GET /getblockchaininfo

#### Query Address Balance:

Requires a valid address as a parameter.
Returns the balance associated with the given address.

    GET /getbalance?address=<address>

#### Get Block Hash:

Requires the block number as a parameter.
Returns the hash of the corresponding block.

    GET /getblockhash?height=<block_number>

#### Get Block Information:

Requires the block hash as a parameter.
Returns detailed information about the block.

    GET /getblock?hash=<block_hash>

#### Query Transaction:

Requires the transaction ID as a parameter.
Returns transaction details.

    GET /gettransaction?txid=<transaction_id>

## Project Structure

    btc_api/
    ├── btc_api.py # Main file containing the API
    ├── hello.py # Initial test script
    ├── restrictions.py # Allowed IPs configuration
    ├── pyproject.toml # Python environment configuration
    └── README.md # Project documentation

## Contributing

Fork the repository.
Create a branch for your changes:

    git checkout -b my-feature

Submit a pull request with your contributions.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Useful Links:

• [Official Bitcoin RPC Documentation](https://developer.bitcoin.org/reference/rpc/)
• [Flask Documentation](https://flask.palletsprojects.com/)
