from functools import cached_property
from typing import Iterable

from web3.contract import ContractEvent
from web3.types import BlockIdentifier, EventData

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

    def user_health(self, user: str, full: bool, block_identifier: BlockIdentifier = "latest") -> float:
        return self.contract.functions.health(user, full).call(block_identifier=block_identifier) * 100 / 1e18

    def user_debt(self, user: str, block_identifier: BlockIdentifier = "latest") -> float:
        return self.contract.functions.debt(user).call(block_identifier=block_identifier)

    ### Events ###
    @cached_property
    def borrow_event(self) -> ContractEvent:
        return self.contract.events.Borrow

    @cached_property
    def repay_event(self) -> ContractEvent:
        return self.contract.events.Repay

    @cached_property
    def remove_collateral_event(self) -> ContractEvent:
        return self.contract.events.RemoveCollateral

    @cached_property
    def liquidate_event(self) -> ContractEvent:
        return self.contract.events.Liquidate

    def get_borrow_events(self, fromBlock: BlockIdentifier, toBlock: BlockIdentifier) -> Iterable[EventData]:
        return self.borrow_event.getLogs(fromBlock=fromBlock, toBlock=toBlock)

    def get_repay_events(self, fromBlock: BlockIdentifier, toBlock: BlockIdentifier) -> Iterable[EventData]:
        return self.repay_event.getLogs(fromBlock=fromBlock, toBlock=toBlock)

    def get_remove_collateral_events(self, fromBlock: BlockIdentifier, toBlock: BlockIdentifier) -> Iterable[EventData]:
        return self.remove_collateral_event.getLogs(fromBlock=fromBlock, toBlock=toBlock)

    def get_liquidate_events(self, fromBlock: BlockIdentifier, toBlock: BlockIdentifier) -> Iterable[EventData]:
        return self.liquidate_event.getLogs(fromBlock=fromBlock, toBlock=toBlock)

    def get_position_change_evens(self, fromBlock: BlockIdentifier, toBlock: BlockIdentifier) -> Iterable[EventData]:
        events = list()
        events.extend(self.get_borrow_events(fromBlock, toBlock))
        events.extend(self.get_repay_events(fromBlock, toBlock))
        events.extend(self.get_remove_collateral_events(fromBlock, toBlock))
        return events
