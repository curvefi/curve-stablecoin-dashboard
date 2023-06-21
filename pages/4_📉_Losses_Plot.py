import pandas as pd
import plotly.express as px
import streamlit as st

from data.pages.position_plot_4 import get_collaterals, get_position_plot

# Config
st.set_page_config(page_title="Position losses plot", page_icon="📉", layout="wide")

# Title
st.title("Position losses plot")

st.caption("This plot uses a lot of web3 provider calls - might be slower than other pages.")

col1, col2, col3 = st.columns(3)

collaterals = get_collaterals()
# TODO: replace with controller deployment blocks
start_blocks = {
    "sfrxETH": 17264365,
    "wstETH": 17432225,
}

with col1:
    amm_collateral = st.selectbox("Select AMM of  position", collaterals.keys())
    selected_collateral = collaterals[amm_collateral]
with col2:
    start_block = st.number_input("Block number of position start", value=start_blocks[amm_collateral])
with col3:
    number_of_points = st.number_input("Number of points in plot", value=20)

user = st.text_input("User", placeholder="Insert address here")

if user:
    times, losses = get_position_plot(selected_collateral, user, start_block, number_of_points)
    df = pd.DataFrame(
        {
            "Times": times,
            "Losses": losses,
        }
    )
    fig = px.line(df, x="Times", y="Losses", title="Position losses")
    fig.update_layout(showlegend=False, xaxis_title="Date", yaxis_title="Loss [%]")
    fig.update_traces(hovertemplate="%{y:.10f}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
