from abc import ABC, abstractmethod
from functools import cached_property

from web3 import Web3
from web3.contract import Contract as Web3Contract

from settings import web3_provider


class Contract(ABC):
    def __init__(self, address: str):
        self.web3 = Web3(web3_provider)
        self.address = address

    @property
    @abstractmethod
    def abi(self):
        ...

    @cached_property
    def contract(self) -> Web3Contract:
        return self.web3.eth.contract(address=self.address, abi=self.abi)
