import pandas as pd
import plotly.express as px
import streamlit as st

from data.pages.overall_stats_2 import get_overall_stats

# Config
st.set_page_config(page_title="Overall Stats", page_icon=":bar_chart:", layout="wide")

# Title
st.title("Overall Stats")

stats = get_overall_stats()

col1, col2 = st.columns([0.5, 0.5])
with col1:
    st.metric("Total Supply", f"{stats.total_supply:,.2f}")
with col2:
    st.metric("Peg", f"{stats.peg}")

column_sizes = [0.5, 0.5]
col1, col2 = st.columns(column_sizes)
col1.metric(
    "Total Debt", f"{stats.debt.controller_debt + sum([d['debt'] for d in stats.debt.peg_keepers_debt.values()]):,.2f}"
)
col2.metric("Total Collateral", "; ".join(stats.total_collateral.controller_collateral))


col1, col2 = st.columns(column_sizes)
col1.write(
    "\n\n".join(
        [
            f"Controller debt: {stats.debt.controller_debt:,.2f}",
            *[
                f"[{v['name']} PG](https://etherscan.io/address/{k}) debt: {v['debt']:,.2f}"
                for k, v in stats.debt.peg_keepers_debt.items()
            ],
        ]
    )
)
col2.write(
    "additional peg keepers' liquidity:\n\n"
    + "\n\n".join(
        [
            f"[{v['name']} PG](https://etherscan.io/address/{k}) collateral: {v['collateral']}"
            for k, v in stats.total_collateral.peg_keepers_collateral.items()
        ],
    )
)

prices = pd.DataFrame(
    {
        "Stableswap": [stats.prices[address]["name"] for address in stats.prices],
        "Prices": [stats.prices[address]["price"] for address in stats.prices],
    }
)
fig = px.bar(prices, x="Stableswap", y="Prices", color="Stableswap", title="Stableswaps prices", log_y=True)
fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Price [USD]")
fig.update_traces(hovertemplate="%{y:.10f}<extra></extra>")
st.plotly_chart(fig, use_container_width=True, theme=None)
