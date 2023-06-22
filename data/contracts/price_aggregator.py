from web3.types import BlockIdentifier

from .abi.price_aggregator import abi
from .base import Contract


class PriceAggregatorContract(Contract):
    @property
    def abi(self):
        return abi

    def price(self, block_identifier: BlockIdentifier = "latest") -> float:
        return self.contract.functions.price().call(block_identifier=block_identifier) / 1e18

    async def async_price(self, block_identifier: BlockIdentifier = "latest") -> float:
        return (await self.async_contract.functions.price().call(block_identifier=block_identifier)) / 1e18
