from functools import cached_property

from .base import Contract


class ERC20Contract(Contract):
    @property
    def abi(self) -> list[dict]:
        return [
            {
                "name": "balanceOf",
                "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "name": "decimals",
                "inputs": [],
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "name": "name",
                "inputs": [],
                "outputs": [{"type": "string", "name": ""}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "name": "symbol",
                "inputs": [],
                "outputs": [{"type": "string", "name": ""}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "name": "totalSupply",
                "inputs": [],
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
        ]

    @cached_property
    def name(self) -> str:
        return self.contract.functions.name().call()

    @cached_property
    def symbol(self) -> str:
        return self.contract.functions.symbol().call()

    @cached_property
    def precision(self) -> int:
        decimals = self.contract.functions.decimals().call()
        return 10**decimals

    def total_supply(self) -> float:
        return self.contract.functions.totalSupply().call() / self.precision

    def balanceOf(self, address: str) -> float:
        return self.contract.functions.balanceOf(address).call() / self.precision
