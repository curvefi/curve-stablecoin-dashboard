from web3.types import BlockIdentifier

from .abi.amm import abi
from .base import Contract


class AmmContract(Contract):
    @property
    def abi(self):
        return abi

    def read_user_tick_numbers(self, user: str, block_identifier: BlockIdentifier = "latest") -> (int, int):
        return self.contract.functions.read_user_tick_numbers(user).call(block_identifier=block_identifier)
