from pydantic import BaseModel

from .contracts import collaterals, controllers, stablecoin


class ControllerPosition(BaseModel):
    address: str
    collateral: str
    positions: list[tuple]


def get_positions() -> list[ControllerPosition]:
    controller_positions = []

    for col_addr, col in collaterals.items():
        collateral_symbol = col.symbol
        controller = controllers[col_addr]
        positions = []

        for i in range(controller.n_loans()):
            user = controller.loans(i)
            user_state = controller.user_state(user)
            user_state[0] = user_state[0] / col.precision
            user_state[1] = user_state[1] / stablecoin.precision
            user_state[2] = user_state[2] / stablecoin.precision
            positions.append((user, *user_state))

        controller_positions.append(
            ControllerPosition(
                address=controller.address,
                collateral=collateral_symbol,
                positions=positions,
            )
        )

    return controller_positions
