from pydantic import BaseModel

from .contracts import (
    amms,
    collaterals,
    controller_factory,
    controllers,
    peg_keepers,
    stablecoin,
    stableswaps,
)


class Collateral(BaseModel):
    controller_collateral: list[str]
    peg_keepers_collateral: dict[str, dict[str, str]]


class Debt(BaseModel):
    controller_debt: float
    peg_keepers_debt: dict[str, dict[str, float | str]]


class OverallStats(BaseModel):
    total_supply: float
    debt: Debt
    total_collateral: Collateral


def get_overall_stats() -> OverallStats:
    total_supply = stablecoin.total_supply()
    controller_debt = controller_factory.total_debt() / stablecoin.precision

    controller_collateral = []
    for col_addr, col in collaterals.items():
        amm = amms[col_addr]
        amount = col.balanceOf(amm.address)
        controller_collateral.append(f"{amount:,.2f} {col.symbol}")

    peg_keepers_debt = {}
    peg_keepers_collateral = {}
    for pool_addr, peg_keeper in peg_keepers.items():
        stableswap = stableswaps[pool_addr]
        peg_keepers_debt[peg_keeper.address] = {
            "name": stableswap.symbol,
            "debt": peg_keeper.debt / stablecoin.precision,
        }
        peg_keepers_collateral[peg_keeper.address] = {
            "name": stableswap.symbol,
            "collateral": f"{stableswap.balanceOf(peg_keeper.address):,.2f} {stableswap.symbol}",
        }
    return OverallStats(
        total_supply=total_supply,
        debt=Debt(controller_debt=controller_debt, peg_keepers_debt=peg_keepers_debt),
        total_collateral=Collateral(
            controller_collateral=controller_collateral, peg_keepers_collateral=peg_keepers_collateral
        ),
    )


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
