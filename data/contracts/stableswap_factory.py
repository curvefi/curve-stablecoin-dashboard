from functools import cached_property

from .abi.stableswap_factory import abi
from .base import Contract


class StableswapFactoryContract(Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def pool_count(self) -> int:
        return self.contract.functions.pool_count().call()

    @cached_property
    def pools(self) -> list[str]:
        pools = []
        for i in range(self.pool_count):
            pools.append(self.contract.functions.pool_list(i).call())
        return pools
