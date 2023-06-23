import plotly.graph_objects as go
import streamlit as st

from data.pages import get_collaterals
from data.pages.position_plot_6 import get_position_plot
from data.utils.constants import start_blocks

# Config
st.set_page_config(page_title="Position losses plot", page_icon="📉", layout="wide")

# Title
st.title("Position losses plot")

st.caption("This plot uses a lot of web3 provider calls - might be slower than other pages.")

col1, col2, col3 = st.columns(3)

collaterals = get_collaterals()

with col1:
    amm_collateral = st.selectbox("Select AMM of  position", collaterals.keys())
    selected_collateral = collaterals[amm_collateral]
with col2:
    start_block = st.number_input("Block number of position start", value=start_blocks[amm_collateral])
with col3:
    number_of_points = st.number_input("Number of points in plot", value=30)

user = st.text_input("User", placeholder="Insert address here")

if user:
    position = get_position_plot(selected_collateral, user, start_block, number_of_points)

    fig = go.Figure(
        data=[
            go.Scatter(x=position.times, y=position.losses, name="losses", mode="lines"),
            go.Scatter(x=position.times, y=position.prices, name="collateral price", yaxis="y2", mode="lines"),
            go.Scatter(
                x=position.events.x,
                y=position.events.y,
                mode="markers+text",
                text=position.events.text,
                textposition="top center",
                name="Events",
            ),
        ]
    )
    liquidation_ranges = [
        {
            "type": "rect",
            "xref": "x",
            "yref": "y",
            "x0": sl[0],
            "y0": "0",
            "x1": sl[1],
            "y1": max(position.losses),
            "fillcolor": "lightpink",
            "opacity": 0.3,
            "line_width": 0,
            "layer": "below",
        }
        for sl in position.soft_liquidation
    ]
    liquidation_ranges.extend(
        [
            {
                "type": "rect",
                "xref": "x",
                "yref": "y",
                "x0": sl[0],
                "y0": "0",
                "x1": sl[1],
                "y1": max(position.losses),
                "fillcolor": "red",
                "opacity": 0.2,
                "line_width": 0,
                "layer": "below",
            }
            for sl in position.hard_liquidation
        ]
    )

    fig.update_layout(
        title="Position losses",
        xaxis_title="Dates",
        yaxis_title="Position losses [%]",
        yaxis2=dict(title="Collateral Prices [crvUSD]", overlaying="y", side="right"),
        legend=dict(x=0, y=1, xanchor="left", yanchor="top"),
        font=dict(family="Courier New, monospace"),
        shapes=liquidation_ranges,
    )
    fig.update_traces(hovertemplate="%{y:.3f}<extra></extra>", line=dict(width=3))

    st.plotly_chart(fig, use_container_width=True)
