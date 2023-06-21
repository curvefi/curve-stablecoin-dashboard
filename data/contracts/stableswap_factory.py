from functools import cached_property

from data.utils.multicall import multicall

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
        calls = [self.contract.functions.pool_list(i) for i in range(self.pool_count)]
        pools = multicall.try_aggregate(calls)
        return pools
