import cachetools.func
from pydantic import BaseModel

from data.contracts import (
    LendingPriceOracleContract,
    lending_collaterals,
    lending_controllers,
    lending_vaults,
)
from data.utils.multicall import multicall


def get_controllers() -> dict:
    return {
        col.symbol: {"controller": lending_controllers[col_addr].address, "collateral": col.address}
        for col_addr, col in lending_collaterals.items()
    }


class Position(BaseModel):
    i: int
    user: str
    user_state: tuple[float, float, float, int]
    collateral_usd: float
    health: float


class Positions(BaseModel):
    n_loans: int
    positions: list[Position]


@cachetools.func.ttl_cache(maxsize=None, ttl=3 * 60)
def get_positions(collateral_address: str, full: bool) -> Positions:
    col = lending_collaterals[collateral_address]
    controller = lending_controllers[collateral_address]
    vault = lending_vaults[collateral_address]
    price_oracle = LendingPriceOracleContract(vault.price_oracle)
    n_loans = controller.n_loans()
    positions = []

    calls = []
    for i in range(n_loans):
        calls.append(controller.contract.functions.loans(i))
    users = multicall.try_aggregate(calls)

    calls = []
    for user in users:
        calls.append(controller.contract.functions.user_state(user))
    user_states = multicall.try_aggregate(calls)

    calls = []
    for user in users:
        calls.append(controller.contract.functions.health(user, full))
    healths = multicall.try_aggregate(calls)

    oracle_price = price_oracle.price()

    for i, user in enumerate(users):
        user_state = user_states[i]
        user_state[0] = user_state[0] / col.precision
        user_state[1] = user_state[1] / 10**18
        user_state[2] = user_state[2] / 10**18

        positions.append(
            Position(
                i=i,
                user=user,
                user_state=user_states[i],
                collateral_usd=user_states[i][0] * oracle_price / 10**18 + user_states[i][1],
                health=healths[i] * 100 / 1e18,
            )
        )

    positions = sorted(positions, key=lambda x: x.health)
    return Positions(n_loans=n_loans, positions=positions)
