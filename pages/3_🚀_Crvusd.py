import pandas as pd
import plotly.express as px
import streamlit as st

from data.pages.crvusd_3 import get_prices

# Config
st.set_page_config(page_title="Crvusd/USD Price Chart", page_icon="🚀", layout="wide")

# Title
st.title("Crvusd/USD Price")
st.caption("This plot uses a lot of web3 provider calls - might be slower than other pages.")

col1, col2 = st.columns(2)

with col1:
    start_block = st.number_input("Block number of start of chart", value=17264365)
with col2:
    number_of_points = st.number_input("Number of points in plot", value=20)

times, prices = get_prices(start_block, number_of_points)
df = pd.DataFrame(
    {
        "Times": times,
        "Prices": prices,
    }
)
fig = px.line(df, x="Times", y="Prices", title=None)
fig.update_layout(showlegend=False, xaxis_title="Date", yaxis_title="Price [USD]")
fig.update_traces(hovertemplate="%{y:.10f}<extra></extra>")
st.plotly_chart(fig, use_container_width=True)
