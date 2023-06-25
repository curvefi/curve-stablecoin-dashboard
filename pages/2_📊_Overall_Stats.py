import pandas as pd
import plotly.express as px
import streamlit as st

from data.pages.overall_stats_2 import get_overall_stats

# Config
st.set_page_config(page_title="Overall Stats", page_icon=":bar_chart:", layout="wide")

# Title
st.title("Overall Stats")

stats = get_overall_stats()

col1, col2 = st.columns([0.4, 0.6])
with col1:
    st.metric("Total Supply", f"{stats.total_supply:,.2f}")
with col2:
    st.metric("Peg", f"{stats.peg}")

column_sizes = [0.4, 0.6]
col1, col2 = st.columns(column_sizes)
col1.metric(
    "Total Debt", f"{stats.debt.controller_debt + sum([d['debt'] for d in stats.debt.peg_keepers_debt.values()]):,.2f}"
)
with col2:
    st.write("Total Collateral")
    columns = st.columns(len(stats.total_collateral.controller_collateral))
    for i, controller_collateral in enumerate(stats.total_collateral.controller_collateral):
        with columns[i]:
            st.header(controller_collateral)


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

prices_data = [stats.prices[address]["price"] for address in stats.prices]

prices = pd.DataFrame(
    {
        "Stableswap": [stats.prices[address]["name"] for address in stats.prices],
        "Prices": prices_data,
    }
)
fig = px.bar(prices, x="Stableswap", y="Prices", color="Stableswap", title="Stableswaps prices")
fig.update_layout(
    showlegend=False,
    xaxis_title=None,
    yaxis_title="Price [USD]",
    yaxis_range=[min(prices_data) * 0.999, max(prices_data) * 1.001],
)
fig.update_traces(hovertemplate="%{y:.10f}<extra></extra>")
st.plotly_chart(fig, use_container_width=True)
