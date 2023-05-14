import json
from functools import cached_property

import requests
from web3 import Web3
from web3.contract import Contract as Web3Contract

from settings import settings, web3_provider


class Contract:
    def __init__(self, address: str):
        self.web3 = Web3(web3_provider)
        self.address = address

    @cached_property
    def abi(self) -> list[dict]:
        url = (
            f"https://api.etherscan.io/api?module=contract&action=getabi&address={self.address}"
            f"&apikey={settings.ETHERSCAN_TOKEN}"
        )
        return json.loads(requests.get(url).json()["result"])

    @cached_property
    def contract(self) -> Web3Contract:
        return self.web3.eth.contract(address=self.address, abi=self.abi)
