from data.contracts import collaterals


def get_collaterals() -> dict:
    return {col.symbol: col_addr for col_addr, col in collaterals.items()}
