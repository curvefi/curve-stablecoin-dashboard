from pydantic import BaseModel

from .contracts import collaterals, controllers, stablecoin


def get_controllers() -> dict:
    return {
        col.symbol: {"controller": controllers[col_addr].address, "collateral": col.address}
        for col_addr, col in collaterals.items()
    }


class Positions(BaseModel):
    n_loans: int
    positions: list[tuple]


def get_positions(collateral_address: str, pagination: int = 10, page: int = 1) -> Positions:
    col = collaterals[collateral_address]
    controller = controllers[collateral_address]
    n_loans = controller.n_loans()
    positions = []

    for i in range((page - 1) * pagination, min(n_loans, page * pagination + 1)):
        user = controller.loans(i)
        user_state = controller.user_state(user)
        user_state[0] = user_state[0] / col.precision
        user_state[1] = user_state[1] / stablecoin.precision
        user_state[2] = user_state[2] / stablecoin.precision
        positions.append((i, user, *user_state))

    return Positions(n_loans=n_loans, positions=positions)
