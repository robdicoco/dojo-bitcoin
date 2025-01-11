# Shi(し) Satoshi - Server Info

## _Hardware_

### Configuration Summary

| Item          | Value                         |
| ------------- | ----------------------------- |
| Region        | Singapore (sg-sin)            |
| Zone          | Randon                        |
| Network Type  | VPC                           |
| VPC           | Default VPC                   |
| vSwitch       | Default vSwitch               |
| Instance Type | Universal Type (1 vCPU 1 GiB) |
| OS Image      | Ubuntu 24                     |
| System Disk   | SSD (ESSD) 20GiB              |
| Network       | 40 Gbps / 1 Gbps              |

## _VM Instance_

### Preparation

```sh
linode-cli linodes create \
  --image 'linode/ubuntu24.04' \
  --private_ip false \
  --region sg-sin-2 \
  --type g6-nanode-1 \
  --label ubuntu-sg-sin-2 \
  --tags 'nearx, bitcoin, dojo' \
  --tags dojo \
  --tags nearx \
  --tags bitcoin \
```

## _Bitcoin Node Setup_

### Preparation

#### Bitcoin user

```sh
sudo groupadd -r bitcoin
sudo useradd -r -m -g bitcoin -s /bin/bash bitcoin
```

#### OS dependencies

```sh
sudo apt install ca-certificates gnupg gpg wget jq --no-install-recommends -y
```

```sh
sudo mkdir -p /opt/bitcoin/28.1
sudo mkdir -p /opt/blockchain/bitcoin
cd /tmp
wget https://bitcoincore.org/bin/bitcoin-core-28.1/bitcoin-28.1-x86_64-linux-gnu.tar.gz
sudo tar -xzvf bitcoin-28.1-x86_64-linux-gnu.tar.gz -C /opt/bitcoin/28.1 --strip-components=1 --exclude=*-qt
sudo ln -s /opt/bitcoin/28.1 /opt/bitcoin/current
sudo rm -rf /tmp/b*
sudo chown -R bitcoin:bitcoin /opt/blockchain/bitcoin

```

```sh
sudo mkdir -p /opt/bitcoin/config
sudo cat > bitcoin.conf << EOF
datadir=/opt/blockchain/bitcoin
printtoconsole=1
regtest=1
server=1
rpcallowip=127.0.0.1
rpcuser=satoshi
rpcpassword=${BITCOIN_RPC_PASSWORD:-$(openssl rand -hex 24)}
fallbackfee=0.0001
rpcport=18332
daemon=1
EOF
```

```sh
cat > bitcoind.service << EOF
[Unit]
Description=Bitcoin Core Regtest
After=network.target

[Service]
User=bitcoin
Group=bitcoin
WorkingDirectory=/opt/blockchain/bitcoin

Type=simple
ExecStart=/opt/bitcoin/current/bin/bitcoind -conf=/opt/bitcoin/config/bitcoin.conf

[Install]
WantedBy=multi-user.target
EOF
```
