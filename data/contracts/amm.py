from .abi.amm import abi
from .base import Contract


class AmmContract(Contract):
    @property
    def abi(self):
        return abi
