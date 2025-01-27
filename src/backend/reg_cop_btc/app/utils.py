from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv
from decimal import Decimal, getcontext
import os

load_dotenv()

# Set decimal precision
getcontext().prec = 8


def get_bitcoin_rpc():
    rpc_user = os.getenv("BITCOIN_RPC_USER")
    rpc_password = os.getenv("BITCOIN_RPC_PASSWORD")
    rpc_host = os.getenv("BITCOIN_RPC_HOST")
    rpc_port = os.getenv("BITCOIN_RPC_PORT")
    wallet_name = os.getenv("BITCOIN_WALLET_NAME", "mywallet")  # Default wallet name
    return AuthServiceProxy(
        f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
    )


def generate_payment_address(rpc):
    """
    Create a new Bitcoin wallet and return the address.
    """
    address = rpc.getnewaddress()
    return address


def validate_payment(rpc, address, amount):
    transactions = rpc.listtransactions()
    for tx in transactions:
        if (
            tx["address"] == address
            and tx["amount"] >= amount
            and tx["confirmations"] > 0
        ):
            return True
    return False


def send_op_return_transaction(rpc, document_hash):
    """
    Send a transaction with the document hash in the OP_RETURN field.
    """
    # Get a new address to send the transaction from
    sender_address = "bcrt1q2dgnl09a0kfwca23333tyhrly2r3c4grtp35kc"

    SATOSHI = Decimal("0.00000001")

    # Get unspent transaction outputs (UTXOs) for the sender address
    utxos = rpc.listunspent(0, 9999999)

    if not utxos:
        raise Exception("No UTXOs found for the sender address. Fund the wallet first.")

    # Sort UTXOs by amount (largest first)
    utxos.sort(key=lambda x: x["amount"], reverse=True)

    # Select UTXOs until the total input value is sufficient
    total_input = Decimal("0")
    selected_utxos = []
    for utxo in utxos:
        total_input += Decimal(str(utxo["amount"]))
        selected_utxos.append(utxo)

        # Stop if we have enough inputs
        if total_input >= Decimal(
            "0.0001"
        ):  # Minimum input value to cover fee and dust
            break

    # Check if the total input is sufficient
    if total_input < Decimal("0.0001"):
        raise Exception(
            "Insufficient funds to cover the transaction fee and dust threshold."
        )

    # Create the OP_RETURN output
    op_return_data = f"OP_RETURN {document_hash}"
    op_return_script = f"6a{len(op_return_data.encode('utf-8')).to_bytes(1, 'big').hex()}{op_return_data.encode('utf-8').hex()}"

    # Create the raw transaction
    outputs = {
        "data": op_return_script,  # OP_RETURN output
    }

    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]} for utxo in selected_utxos]

    # Estimate the transaction size
    raw_tx = rpc.createrawtransaction(inputs, outputs)
    tx_size = len(raw_tx) // 2  # Size in bytes (hex string length / 2)

    # Get the fee rate (satoshis per byte)
    try:
        fee_rate = Decimal(str(rpc.estimatesmartfee(6)["feerate"]))  # 6 blocks target
        if fee_rate <= 0:
            fee_rate = Decimal(
                "0.00000001"
            )  # Default to 1 satoshi/byte if no fee estimate is available
    except KeyError:
        # If estimatesmartfee fails, use a default fee rate for Regtest
        fee_rate = Decimal("0.00000001")  # 1 satoshi/byte

    # Calculate the fee
    fee = Decimal(tx_size) * fee_rate * Decimal("100000000")  # Convert to satoshis

    # Ensure the fee meets the minimum relay fee requirement
    min_relay_fee = Decimal("0.00000198")  # 198 satoshis (minimum relay fee)
    if fee < min_relay_fee:
        fee = (
            min_relay_fee  # Use the minimum relay fee if the calculated fee is too low
        )

    # Ensure the total input is sufficient to cover the fee
    if total_input < (fee / Decimal("100000000")):
        raise Exception("Insufficient funds to cover the transaction fee.")

    # Adjust the change output to account for the fee
    change_amount = total_input - (fee / Decimal("100000000")) - (100 * SATOSHI)
    outputs[sender_address] = change_amount

    # Dust threshold (546 satoshis or 0.00000546 BTC)
    dust_threshold = Decimal("0.00000546")

    if (
        change_amount > dust_threshold
    ):  # Only add a change output if the amount is above the dust threshold
        outputs[sender_address] = change_amount
    else:
        # If the change amount is below the dust threshold, include it as part of the fee
        fee = total_input * Decimal(
            "100000000"
        )  # Convert the entire input amount to satoshis for the fee
        outputs[sender_address] = Decimal("0.0")

    # Recreate the raw transaction with the updated outputs
    raw_tx = rpc.createrawtransaction(inputs, outputs)

    decoded_tx = rpc.decoderawtransaction(raw_tx)

    # Sign the raw transaction
    signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

    if not signed_tx["complete"]:
        raise Exception("Failed to sign the transaction.")

    # Broadcast the signed transaction
    tx_id = rpc.sendrawtransaction(signed_tx["hex"])

    return tx_id


def check_mining_confirmation(rpc, tx_id):
    """
    Check if the transaction has been confirmed (mined into a block).
    """
    try:
        tx_info = rpc.gettransaction(tx_id)
        if tx_info.get("confirmations", 0) >= 1:
            return True
        return False
    except Exception as e:
        raise e
