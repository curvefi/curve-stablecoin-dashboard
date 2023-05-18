from functools import cached_property

from .abi.controller_factory import abi
from .base import Contract


class ControllerFactoryContract(Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def n_collaterals(self) -> int:
        return self.contract.functions.n_collaterals().call()

    @cached_property
    def collaterals(self) -> list[str]:
        cols = []
        for i in range(self.n_collaterals):
            cols.append(self.contract.functions.collaterals(i).call())
        return cols

    @cached_property
    def controllers(self) -> dict[str, str]:
        contrs = {}
        for col in self.collaterals:
            contrs[col] = self.contract.functions.get_controller(col).call()
        return contrs

    @cached_property
    def amms(self) -> dict[str, str]:
        amms = {}
        for col in self.collaterals:
            amms[col] = self.contract.functions.get_amm(col).call()

        return amms

    def total_debt(self) -> int:
        return self.contract.functions.total_debt().call()
