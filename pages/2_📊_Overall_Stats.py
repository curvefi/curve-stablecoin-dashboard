import pandas as pd
import streamlit as st

from data.overall_stats_2 import get_overall_stats, get_positions

# Config
st.set_page_config(page_title="Overall Stats", page_icon=":bar_chart:", layout="wide")

# Title
st.title("Overall Stats")

stats = get_overall_stats()

col1, col2, col3 = st.columns(3)
col1.metric("Total Supply", f"{stats.total_supply:,.2f}")
col2.metric("Total Debt", f"{stats.debt.controller_debt + sum([d for d in stats.debt.peg_keepers_debt.values()]):,.2f}")
col3.metric("Total Collateral", ", ".join(stats.total_collateral.controller_collateral))


col1, col2, col3 = st.columns(3)

col2.write(
    "\n\n".join(
        [
            f"Controller debt: {stats.debt.controller_debt:,.2f}",
            *[
                f"[Peg keeper](https://etherscan.io/address/{k}) debt: {v}"
                for k, v in stats.debt.peg_keepers_debt.items()
            ],
        ]
    )
)
col3.write(
    "additional peg keepers' liquidity:\n\n"
    + "\n\n".join(
        [
            f"[Peg keeper](https://etherscan.io/address/{k}) collateral: {v}"
            for k, v in stats.total_collateral.peg_keepers_collateral.items()
        ],
    )
)

# Positions
positions = get_positions()

for controller in positions:
    st.write(f"Positions for {controller.collateral} [Controller](https://etherscan.io/address/{controller.address}):")
    df = pd.DataFrame(controller.positions, columns=["user", "collateral", "stablecoin", "debt", "N"])
    st.table(df.astype(str))
