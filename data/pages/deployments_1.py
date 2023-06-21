from pydantic import BaseModel

from data.contracts import (
    ERC20Contract,
    amms,
    collaterals,
    controller_factory,
    controllers,
    peg_keepers,
    stablecoin,
    stableswaps,
)


class Deployments(BaseModel):
    controller_factory: str
    collaterals: dict[str, str]
    controllers: dict[str, str]
    amms: dict[str, str]
    stableswaps: dict[str, str]
    peg_keepers: dict[str, str]


def get_deployments() -> Deployments:
    collateral_addresses = {collateral.symbol: collateral.address for collateral in collaterals.values()}
    controllers_addresses = {collaterals[col].symbol: contr.address for col, contr in controllers.items()}
    amms_addresses = {collaterals[col].symbol: amm.address for col, amm in amms.items()}

    stableswaps_addresses = {}
    for stableswap in stableswaps.values():
        coins = []
        for coin_address in stableswap.coins:
            if coin_address == stablecoin.address:
                coin = stablecoin
            else:
                coin = ERC20Contract(coin_address)
            coins.append(coin.symbol)
        stableswaps_addresses["-".join(coins)] = stableswap.address

    peg_keepers_addresses = {}
    stableswaps_mapping = {value: key for key, value in stableswaps_addresses.items()}
    for pool, peg_keeper in peg_keepers.items():
        peg_keepers_addresses[stableswaps_mapping[pool]] = peg_keeper.address

    return Deployments(
        controller_factory=controller_factory.address,
        collaterals=collateral_addresses,
        controllers=controllers_addresses,
        amms=amms_addresses,
        stableswaps=stableswaps_addresses,
        peg_keepers=peg_keepers_addresses,
    )
