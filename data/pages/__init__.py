from data.contracts import collaterals, lending_collaterals


def get_collaterals() -> dict:
    return {col.symbol: col_addr for col_addr, col in collaterals.items()}


def get_lending_collaterals() -> dict:
    return {col.symbol: col_addr for col_addr, col in lending_collaterals.items()}
