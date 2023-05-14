from functools import cached_property

from .erc20 import ERC20Contract


class StablecoinContract(ERC20Contract):
    @cached_property
    def minter(self) -> str:
        return self.contract.functions.minter().call()
