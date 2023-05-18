from functools import cached_property

from .abi.stablecoin import abi
from .erc20 import ERC20Contract


class StablecoinContract(ERC20Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def minter(self) -> str:
        return self.contract.functions.minter().call()
