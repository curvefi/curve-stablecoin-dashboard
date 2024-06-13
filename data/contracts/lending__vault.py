from .abi.lending__vault import abi
from .base import Contract


class LendingVaultContract(Contract):
    @property
    def abi(self):
        return abi

    @property
    def controller(self) -> str:
        return self.contract.functions.controller().call()

    @property
    def price_oracle(self) -> str:
        return self.contract.functions.price_oracle().call()
