from pydantic import BaseModel

from .contracts import (
    ControllerContract,
    PegKeeperContract,
    PredefinedERC20Contract,
    StableswapContract,
    controller_factory,
    policy,
    stablecoin,
)


class Collateral(BaseModel):
    controller_collateral: list[str]
    peg_keepers_collateral: dict[str, str]


class Debt(BaseModel):
    controller_debt: float
    peg_keepers_debt: dict[str, float]


class OverallStats(BaseModel):
    total_supply: float
    debt: Debt
    total_collateral: Collateral


def get_overall_stats() -> OverallStats:
    total_supply = stablecoin.total_supply()
    controller_debt = controller_factory.total_debt() / stablecoin.precision

    controller_collateral = []
    for collateral_address in controller_factory.collaterals:
        amm = controller_factory.amms[collateral_address]
        collateral = PredefinedERC20Contract(collateral_address)
        amount = collateral.balanceOf(amm)
        controller_collateral.append(f"{amount:,.2f} {collateral.symbol}")

    peg_keepers_debt = {}
    peg_keepers_collateral = {}
    for peg_keeper_address in policy.peg_keepers:
        peg_keeper = PegKeeperContract(peg_keeper_address)
        peg_keepers_debt[peg_keeper_address] = peg_keeper.debt / stablecoin.precision
        pool = peg_keeper.pool
        stableswap = StableswapContract(pool)
        peg_keepers_collateral[
            peg_keeper_address
        ] = f"{stableswap.balanceOf(peg_keeper_address):,.2f} {stableswap.symbol}"

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
    controller_collaterals = controller_factory.collaterals
    controller_controllers = controller_factory.controllers
    controller_positions = []

    for collateral_addr in controller_collaterals:
        collateral = PredefinedERC20Contract(collateral_addr)
        collateral_symbol = collateral.symbol
        address = controller_controllers[collateral_addr]

        controller = ControllerContract(address)
        positions = []

        for i in range(controller.n_loans()):
            user = controller.loans(i)
            user_state = controller.user_state(user)
            positions.append((user, *user_state))

        controller_positions.append(
            ControllerPosition(
                address=address,
                collateral=collateral_symbol,
                positions=positions,
            )
        )

    return controller_positions
