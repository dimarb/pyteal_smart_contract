from algosdk import account, transaction, mnemonic
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
from algosdk.v2client import algod
import os
import pprint
from dotenv import load_dotenv
import base64
load_dotenv()

# Configura el cliente Algod
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # Los nodos públicos de Algorand a menudo no requieren un token

algod_client = algod.AlgodClient(algod_token, algod_address)


# Llave mnemónica de la cuenta de despliegue
mnem = os.getenv('DISPENSEER_MNEMONIC')
private_key = mnemonic.to_private_key(mnem)
sender = account.address_from_private_key(private_key)

# Código TEAL generado desde contract.py
with open("aprobal.teal", 'r') as archivo:
    approval_teal = archivo.read()

with open("clear.teal", 'r') as archivo:
    clear_state_teal = archivo.read()

# Dar formato al código TEAL como binario de la AVM (Bytecode)
approval_result = algod_client.compile(approval_teal)
approval_binary = base64.b64decode(approval_result["result"])

# Dar formato al código TEAL como binario de la AVM (Bytecode)
clear_result = algod_client.compile(clear_state_teal)
clear_binary = base64.b64decode(clear_result["result"])

# Obtener parámetros de transacción
params = algod_client.suggested_params()

# Crear la transacción de despliegue de la aplicación
txn = ApplicationCreateTxn(
    sender,
    params,
    on_complete=transaction.OnComplete.NoOpOC.real,
    approval_program=approval_binary,
    clear_program=clear_binary,
    global_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
    local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
)

# Firmar la transacción
signed_txn = txn.sign(private_key)

# Enviar la transacción a la red
tx_id = algod_client.send_transaction(signed_txn)
print(f"Transaction ID: {tx_id}")
print(f"Url de la transaccion en Pera Explorer ID: https://testnet.explorer.perawallet.app/tx/{tx_id}")
# Esperar la confirmación
transaction_response = wait_for_confirmation(algod_client, tx_id, 4)
app = transaction_response
print("Deployed Smart Contract Contract Info:")
pprint.pp(app)