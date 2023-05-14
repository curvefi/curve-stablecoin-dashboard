from functools import cached_property

from .erc20 import ERC20Contract


class StableswapContract(ERC20Contract):
    @cached_property
    def coins(self) -> list[str]:
        coins = []
        for i in range(2):
            coins.append(self.contract.functions.coins(i).call())
        return coins
