from settings import settings

from .amm import AmmContract
from .controller import ControllerContract
from .controller_factory import ControllerFactoryContract
from .erc20 import ERC20Contract
from .peg_keeper import PegKeeperContract
from .policy import PolicyContract
from .price_aggregator import PriceAggregatorContract
from .stablecoin import StablecoinContract
from .stableswap import StableswapContract
from .stableswap_factory import StableswapFactoryContract

# Predefined settings
stablecoin = StablecoinContract(settings.Stablecoin)
stableswap_factory = StableswapFactoryContract(settings.Swapfactory)
policy = PolicyContract(settings.Monetarypolicy)
price_aggregator = PriceAggregatorContract(settings.PriceAggregator)

# Imported values
controller_factory = ControllerFactoryContract(stablecoin.minter)
collaterals: dict[str, ERC20Contract] = {col: ERC20Contract(col) for col in controller_factory.collaterals}
controllers: dict[str, ControllerContract] = {
    col: ControllerContract(con_addr) for col, con_addr in controller_factory.controllers.items()
}
amms: dict[str, AmmContract] = {col: AmmContract(amm_addr) for col, amm_addr in controller_factory.amms.items()}

stableswaps: dict[str, StableswapContract] = {
    st_addr: StableswapContract(st_addr) for st_addr in stableswap_factory.pools
}
peg_keepers: dict[str, PegKeeperContract] = {
    PegKeeperContract(pg_addr).pool: PegKeeperContract(pg_addr) for pg_addr in policy.peg_keepers
}
