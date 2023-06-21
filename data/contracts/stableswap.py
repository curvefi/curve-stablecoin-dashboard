from functools import cached_property

from web3.contract.contract import ContractFunction

from .abi.stableswap import abi
from .erc20 import ERC20Contract


class StableswapContract(ERC20Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def coins(self) -> list[str]:
        coins = []
        for i in range(2):
            coins.append(self.contract.functions.coins(i).call())
        return coins

    @cached_property
    def last_price_function(self) -> ContractFunction:
        return self.contract.functions.last_price
