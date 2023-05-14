from functools import cached_property

from .base import Contract


class StableswapFactoryContract(Contract):
    @cached_property
    def pool_count(self) -> int:
        return self.contract.functions.pool_count().call()

    @cached_property
    def pools(self) -> list[str]:
        pools = []
        for i in range(self.pool_count):
            pools.append(self.contract.functions.pool_list(i).call())
        return pools
