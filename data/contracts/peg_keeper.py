from functools import cached_property

from .abi.peg_keeper import abi
from .base import Contract


class PegKeeperContract(Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def pool(self) -> str:
        return self.contract.functions.pool().call()

    @cached_property
    def debt(self) -> int:
        return self.contract.functions.debt().call()
