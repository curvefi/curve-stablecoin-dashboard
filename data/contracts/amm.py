from .abi.amm import abi
from .base import Contract


class AmmContract(Contract):
    @property
    def abi(self):
        return abi

    def read_user_tick_numbers(self, user: str) -> (int, int):
        return self.contract.functions.read_user_tick_numbers(user).call()
