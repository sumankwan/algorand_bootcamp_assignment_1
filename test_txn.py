import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


passphrase = "track dwarf panic oven retreat echo daughter vague mango kick predict advice subject pause rail knife blast security fever survey reduce december kit able squeeze"
address = "KLJ35ACNKEVAP5RBVPFMOXNPGANDZJSPQXKK3OIFLYVRMCKUCERSFT3FYU"


def first_transaction_example(my_mnemonic, my_address):
    algod_address = "https://testnet-api.algonode.cloud"
    algod_client = algod.AlgodClient("", algod_address)

    print("My address: {}".format(my_address))
    private_key = mnemonic.to_private_key(my_mnemonic)
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get("amount")))

    # build transaction
    params = algod_client.suggested_params()

    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    amount = 1000000
    note = "Hello World".encode()

    unsigned_txn = transaction.PaymentTxn(
        my_address, params, receiver, amount, None, note
    )

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    print(
        "Decoded note: {}".format(
            base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()
        )
    )

    print("Starting account balance: {} microAlgos".format(account_info.get("amount")))
    print("Amount transferred: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(my_address)
    print(
        "Final account balance: {} microalgos".format(account_info.get("amount")) + "\n"
    )


first_transaction_example(passphrase, address)
