from functools import cached_property

from web3.constants import ADDRESS_ZERO
from web3.types import BlockIdentifier

from data.utils.multicall import multicall

from .abi.policy import abi
from .base import Contract


class PolicyContract(Contract):
    @property
    def abi(self):
        return abi

    @cached_property
    def peg_keepers(self) -> list[str]:
        calls = [self.contract.functions.peg_keepers(i) for i in range(10)]
        pools = multicall.try_aggregate(calls)
        return [p for p in pools if p != ADDRESS_ZERO]

    def rate(self, block_identifier: BlockIdentifier = "latest") -> float:
        return self.contract.functions.rate().call(block_identifier=block_identifier)

    async def async_rate(self, block_identifier: BlockIdentifier = "latest") -> float:
        return await self.async_contract.functions.rate().call(block_identifier=block_identifier)
