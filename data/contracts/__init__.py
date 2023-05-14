from settings import settings

from .controller_factory import ControllerFactoryContract
from .erc20 import ERC20Contract, PredefinedERC20Contract
from .peg_keeper import PegKeeperContract
from .policy import PolicyContract
from .stablecoin import StablecoinContract
from .stableswap import StableswapContract
from .stableswap_factory import StableswapFactoryContract

stablecoin = StablecoinContract(settings.Stablecoin)
controller_factory = ControllerFactoryContract(stablecoin.minter)
stableswap_factory = StableswapFactoryContract(settings.Swapfactory)
policy = PolicyContract(settings.Monetarypolicy)
