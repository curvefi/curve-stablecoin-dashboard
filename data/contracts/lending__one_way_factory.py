from .abi.lending__one_way_lending_factory import abi
from .base import Contract


class OneWayLendingFactoryContract(Contract):
    @property
    def abi(self):
        return abi

    @property
    def market_count(self) -> int:
        return self.contract.functions.market_count().call()

    def collateral_tokens(self, n) -> str:
        return self.contract.functions.collateral_tokens(n).call()

    def amms(self, n) -> str:
        return self.contract.functions.amms(n).call()

    def vaults(self, n) -> str:
        return self.contract.functions.vaults(n).call()
