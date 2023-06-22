import pandas as pd
import plotly.express as px
import streamlit as st

from data.pages.policy_rate_4 import get_rates

# Config
st.set_page_config(page_title="Monetary policy rate", page_icon="📝", layout="wide")

# Title
st.title("Monetary policy rate for borrowing")
st.caption("This plot uses a lot of web3 provider calls - might be slower than other pages.")

col1, col2 = st.columns(2)

with col1:
    start_block = st.number_input("Block number of position start", value=17264365)
with col2:
    number_of_points = st.number_input("Number of points in plot", value=20)


times, rates = get_rates(start_block, number_of_points)
df = pd.DataFrame(
    {
        "Times": times,
        "Rates": rates,
    }
)
fig = px.line(df, x="Times", y="Rates", title=None)
fig.update_layout(showlegend=False, xaxis_title="Date", yaxis_title="Borrow Rate [%]")
fig.update_traces(hovertemplate="%{y:.10f}<extra></extra>")
st.plotly_chart(fig, use_container_width=True)
