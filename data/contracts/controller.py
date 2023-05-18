from .abi.controller import abi
from .base import Contract


class ControllerContract(Contract):
    @property
    def abi(self):
        return abi

    def n_loans(self) -> int:
        return self.contract.functions.n_loans().call()

    def loans(self, n_loan: int) -> str:
        return self.contract.functions.loans(n_loan).call()

    def user_prices(
        self, user: str
    ) -> (float, float,):
        upper, lower = self.contract.functions.user_prices(user).call()
        upper, lower = upper / 1e18, lower / 1e18
        return lower, upper

    def user_state(self, user: str) -> (float, float, float, int):
        # collateral, stablecoin, debt, N
        return self.contract.functions.user_state(user).call()
