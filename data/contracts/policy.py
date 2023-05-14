from functools import cached_property

from web3.constants import ADDRESS_ZERO

from .base import Contract


class PolicyContract(Contract):
    @cached_property
    def peg_keepers(self) -> list[str]:
        peg_keepers = []
        i = 0
        while True:
            curr = self.contract.functions.peg_keepers(i).call()

            if curr != ADDRESS_ZERO:
                peg_keepers.append(curr)
                i += 1
            else:
                break

        return peg_keepers
