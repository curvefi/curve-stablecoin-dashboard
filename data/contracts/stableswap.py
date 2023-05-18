from functools import cached_property

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
