from .utils import get_block_info

# TODO: replace with controller deployment blocks
start_blocks = {
    "sfrxETH": 17264365,
    "wstETH": 17432225,
    "WBTC": 17557475,
    "WETH": 17562530,
}

latest_block_number, latest_block_ts = get_block_info("latest")
default_start_block = latest_block_number - 1000
