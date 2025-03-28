from tronpy import Tron
from tronpy.providers import HTTPProvider


def get_tron_wallet_data(address: str) -> dict:
    client = Tron(HTTPProvider("https://api.shasta.trongrid.io"))  # Для testnet
    account = client.get_account(address)

    return {
        "address": address,
        "bandwidth": account.get("bandwidth", 0),
        "energy": account.get("energy", 0),
        "trx_balance": account.get("balance", 0),
    }
