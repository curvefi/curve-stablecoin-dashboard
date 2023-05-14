from pydantic import BaseModel

from .contracts import (
    PegKeeperContract,
    PredefinedERC20Contract,
    StableswapContract,
    controller_factory,
    policy,
    stablecoin,
    stableswap_factory,
)


class Deployments(BaseModel):
    controller_factory: str
    collaterals: dict[str, str]
    controllers: dict[str, str]
    amms: dict[str, str]
    stableswaps: dict[str, str]
    peg_keepers: dict[str, str]


def get_deployments() -> Deployments:
    controller_collaterals = controller_factory.collaterals
    controller_controllers = controller_factory.controllers
    controller_amms = controller_factory.amms

    collaterals = {}
    controllers = {}
    amms = {}

    for collateral_addr in controller_collaterals:
        collateral = PredefinedERC20Contract(collateral_addr)
        symbol = collateral.symbol

        collaterals[symbol] = collateral_addr
        controllers[symbol] = controller_controllers[collateral_addr]
        amms[symbol] = controller_amms[collateral_addr]

    stableswaps = {}

    for stableswap_address in stableswap_factory.pools:
        stableswap = StableswapContract(stableswap_address)
        coins = []

        for coin_address in stableswap.coins:
            if coin_address == stablecoin.address:
                coin = stablecoin
            else:
                coin = PredefinedERC20Contract(coin_address)
            coins.append(coin.symbol)

        stableswaps["-".join(coins)] = stableswap_address

    peg_keepers = {}
    stableswaps_mapping = {value: key for key, value in stableswaps.items()}

    for peg_keeper_address in policy.peg_keepers:
        peg_keeper = PegKeeperContract(peg_keeper_address)
        pool = peg_keeper.pool
        peg_keepers[stableswaps_mapping[pool]] = peg_keeper_address

    return Deployments(
        controller_factory=controller_factory.address,
        collaterals=collaterals,
        controllers=controllers,
        amms=amms,
        stableswaps=stableswaps,
        peg_keepers=peg_keepers,
    )
