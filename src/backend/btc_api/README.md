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

### **Environment Variables**:

    -   Create a `.env` file in the root directory with the following variables:

```env
TEST_API_KEY=your_api_key_here
DEBUG_MODE=True
```

### Start the Bitcoin node:

```bash
bitcoind -regtest -daemon
```

### Set Environment Variables:

Create a .env file in the application root directory:

    TEST_API_KEY=your_api_token
    DEBUG_MODE=True

### **SSL Certificates**:

Ensure you have SSL certificates (`fullchain.pem` and `privkey.pem`) in the specified directory (`/home/robdc/apps/keys/`).

## How to Run

Start the Flask server:

```bash
uv run bitcoin_api.py
```

### Access the API endpoints at the following URLs Endpoints:

#### 1. **Get Blockchain Info**

-   **Endpoint**: `/getblockchaininfo`
-   **Method**: `GET`
-   **Description**: Retrieves information about the blockchain.
-   **Example**:

```bash
   curl -X GET "https://localhost:5000/getblockchaininfo" \
        -H "Authorization: Bearer your_api_key_here"
```

#### 2. **Get Balance**

-   **Endpoint**: `/getbalance`
-   **Method**: `GET`
-   **Description**: Retrieves the balance of a Bitcoin address.
-   **Parameters**:

    -   `address`: The Bitcoin address to check the balance for.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/getbalance?address=myp2pkhaddress" \
        -H "Authorization: Bearer your_api_key_here"
```

### 3. **Get Block Hash**

-   **Endpoint**: `/getblockhash`
-   **Method**: `GET`
-   **Description**: Retrieves the block hash for a given block height.
-   **Parameters**:

    -   `height`: The block height.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/getblockhash?height=100" \
        -H "Authorization: Bearer your_api_key_here"
```

---

### 4. **Get Block**

-   **Endpoint**: `/getblock`
-   **Method**: `GET`
-   **Description**: Retrieves block information for a given block hash.
-   **Parameters**:

    -   `hash`: The block hash.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/getblock?hash=blockhash123" \
        -H "Authorization: Bearer your_api_key_here"
```

---

### 5. **Get Transaction**

-   **Endpoint**: `/gettransaction`
-   **Method**: `GET`
-   **Description**: Retrieves transaction details for a given transaction ID.
-   **Parameters**:

    -   `txid`: The transaction ID.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/gettransaction?txid=txid123" \
        -H "Authorization: Bearer your_api_key_here"
```

---

### 6. **Get Raw Transaction**

-   **Endpoint**: `/getrawtransaction`
-   **Method**: `GET`
-   **Description**: Retrieves the raw transaction data for a given transaction ID.
-   **Parameters**:

    -   `txid`: The transaction ID.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/getrawtransaction?txid=txid123" \
        -H "Authorization: Bearer your_api_key_here"
```

---

### 7. **Generate Bitcoin Addresses**

-   **Endpoint**: `/generate_addresses`
-   **Method**: `POST`
-   **Description**: Generates one or more Bitcoin addresses.
-   **Request Body**:

```json
{
    "count": 3,
    "wallet_name": "my_wallet"
}
```

-   **Example**:

```bash
   curl -X POST "https://localhost:5000/generate_addresses" \
        -H "Authorization: Bearer your_api_key_here" \
        -H "Content-Type: application/json" \
        -d '{"count": 3, "wallet_name": "my_wallet"}'
```

---

### 8. **Check Wallet Balance**

-   **Endpoint**: `/check_balance`
-   **Method**: `GET`
-   **Description**: Checks the balance of a Bitcoin address using `bitcoinlib`.
-   **Parameters**:

    -   `address`: The Bitcoin address to check the balance for.

-   **Example**:

```bash
   curl -X GET "https://localhost:5000/check_balance?address=myp2pkhaddress" \
        -H "Authorization: Bearer your_api_key_here"
```

---

### 9. **Send Transaction**

-   **Endpoint**: `/send_transaction`
-   **Method**: `POST`
-   **Description**: Sends Bitcoin from one address to another.
-   **Request Body**:

```json
{
    "from_address": "sender_address",
    "to_address": "receiver_address",
    "amount": 0.01
}
```

-   **Example**:

```bash
   curl -X POST "https://localhost:5000/send_transaction" \
        -H "Authorization: Bearer your_api_key_here" \
        -H "Content-Type: application/json" \
        -d '{"from_address": "sender_address", "to_address": "receiver_address", "amount": 0.01}'
```

---

## Running the API

1.  Start the Flask server:

```bash
   python app.py
```

2.  The API will be available at:

```bash

   https://localhost:5000
```

---

## Notes

-   **Authentication**: All endpoints require an API key passed in the `Authorization` header as a Bearer token.
-   **Rate Limiting**: The API is rate-limited to 5 requests per minute by default.
-   **SSL**: The API uses SSL for secure communication. Ensure your certificates are correctly configured.

---

## Example Workflow

1.  **Generate Addresses**:

```bash
   curl -X POST "https://localhost:5000/generate_addresses" \
        -H "Authorization: Bearer your_api_key_here" \
        -H "Content-Type: application/json" \
        -d '{"count": 2, "wallet_name": "my_wallet"}'
```

2.  **Check Balance**:

```bash
   curl -X GET "https://localhost:5000/check_balance?address=myp2pkhaddress" \
        -H "Authorization: Bearer your_api_key_here"
```

3.  **Send Transaction**:

```bash
   curl -X POST "https://localhost:5000/send_transaction" \
        -H "Authorization: Bearer your_api_key_here" \
        -H "Content-Type: application/json" \
        -d '{"from_address": "sender_address", "to_address": "receiver_address", "amount": 0.01}'
```

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

```bash
   git checkout -b my-feature
```

Submit a pull request with your contributions.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Useful Links:

• [Official Bitcoin RPC Documentation](https://developer.bitcoin.org/reference/rpc/)
• [Flask Documentation](https://flask.palletsprojects.com/)
