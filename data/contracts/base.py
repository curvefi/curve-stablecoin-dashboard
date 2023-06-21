from abc import ABC, abstractmethod
from functools import cached_property

from web3 import AsyncWeb3, Web3
from web3.contract import AsyncContract as Web3AsyncContract
from web3.contract import Contract as Web3Contract

from settings import async_web3_provider, web3_provider


class Contract(ABC):
    def __init__(self, address: str):
        self.web3 = Web3(web3_provider)
        self.async_web3 = AsyncWeb3(async_web3_provider)
        self.address = address

    @property
    @abstractmethod
    def abi(self):
        ...

    @cached_property
    def contract(self) -> Web3Contract:
        return self.web3.eth.contract(address=self.address, abi=self.abi)

    @cached_property
    def async_contract(self) -> Web3AsyncContract:
        return self.async_web3.eth.contract(address=self.address, abi=self.abi)
