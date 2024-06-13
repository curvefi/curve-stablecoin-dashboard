from .abi.lending__price_oracle import abi
from .base import Contract


class LendingPriceOracleContract(Contract):
    @property
    def abi(self):
        return abi

    def price(self) -> str:
        return self.contract.functions.price().call()
