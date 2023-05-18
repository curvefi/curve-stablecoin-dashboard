from pathlib import Path

import dotenv
from pydantic import BaseSettings
from web3 import Web3

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    class Config:
        env_file = Path(BASE_DIR, ".env")
        dotenv.load_dotenv(env_file)

    WEB3_PROVIDER_URL: str

    Stablecoin: str = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"
    PriceOracle: str = "0x19F5B81e5325F882C9853B5585f74f751DE3896d"
    Monetarypolicy: str = "0xc684432FD6322c6D58b6bC5d28B18569aA0AD0A1"
    Swapfactory: str = "0x4F8846Ae9380B90d2E71D5e3D042dff3E7ebb40d"
    PriceAggregator: str = "0xe5Afcf332a5457E8FafCD668BcE3dF953762Dfe7"


settings = Settings()
web3_provider = Web3.HTTPProvider(settings.WEB3_PROVIDER_URL)
