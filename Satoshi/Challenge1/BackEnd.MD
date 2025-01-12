# Shi(し) Satoshi - Backend Info

## _Pre requisites_

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

## _Project Preparation_

Copy btc_api to run app folder

## _Local tests_

### Get Blockchain Information

```sh
curl -X GET http://127.0.0.1:5000/getblockchaininfo
```

### Get Balance of an Address

```sh
curl -X GET "http://127.0.0.1:5000/getbalance?address=bc1qp08sxlpwjd4950w2dpzxujln5chmcljyhxck6k"
curl -H "Authorization: Bearer YOUR_SECRET_API_KEY" "http://127.0.0.1:5000/getbalance?address=bc1qp08sxlpwjd4950w2dpzxujln5chmcljyhxck6k"
```

### Get Block Hash by Height

```sh
curl -X GET "http://127.0.0.1:5000/getblockhash?height=100"
```

### Get Block Information by Hash

```sh
curl -X GET "http://127.0.0.1:5000/getblock?hash=0000000000000000000000000000000000000000000000000000000000000000"
```

### Get Transaction Information by Hash

```sh
curl -X GET "http://127.0.0.1:5000/gettransaction?txid=0000000000000000000000000000000000000000000000000000000000000000"
```
