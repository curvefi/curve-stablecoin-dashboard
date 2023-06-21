import cachetools.func
from pydantic import BaseModel

from data.contracts import collaterals, controllers, stablecoin
from data.utils.multicall import multicall


def get_controllers() -> dict:
    return {
        col.symbol: {"controller": controllers[col_addr].address, "collateral": col.address}
        for col_addr, col in collaterals.items()
    }


class Position(BaseModel):
    i: int
    user: str
    user_state: tuple[float, float, float, int]
    health: float


class Positions(BaseModel):
    n_loans: int
    positions: list[Position]


@cachetools.func.ttl_cache(maxsize=None, ttl=3 * 60)
def get_positions(collateral_address: str, full: bool) -> Positions:
    col = collaterals[collateral_address]
    controller = controllers[collateral_address]
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

    for i, user in enumerate(users):
        user_state = user_states[i]
        user_state[0] = user_state[0] / col.precision
        user_state[1] = user_state[1] / stablecoin.precision
        user_state[2] = user_state[2] / stablecoin.precision

        positions.append(Position(i=i, user=user, user_state=user_states[i], health=healths[i] * 100 / 1e18))

    positions = sorted(positions, key=lambda x: x.health)
    return Positions(n_loans=n_loans, positions=positions)
