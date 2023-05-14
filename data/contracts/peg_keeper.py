from functools import cached_property

from .base import Contract


class PegKeeperContract(Contract):
    @cached_property
    def pool(self) -> str:
        return self.contract.functions.pool().call()

    @cached_property
    def debt(self) -> int:
        return self.contract.functions.debt().call()
