from pydantic import BaseModel

from .contracts import (
    amms,
    collaterals,
    controller_factory,
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
