import streamlit as st

from settings import settings

# Config
st.set_page_config(page_title="Curve Stablecoin", page_icon="〽️", layout="wide")

# Title
st.title("Curve Stablecoin Monitoring Tool")

st.subheader("Codebase")
st.write(
    """
    [Github](https://github.com/curvefi/curve-stablecoin)

    [Deployment](https://github.com/curvefi/curve-stablecoin/blob/master/deployment-logs/mainnet.log)
    """
)

# Deployments
st.subheader("Main Configuration")

col1, col2 = st.columns(2)

with col1:
    st.write("Stablecoin:")
    st.write("Price Oracle:")
    st.write("Monetary policy:")
    st.write("Swap factory:")
    st.write("Price Aggregator:")

with col2:
    st.write(f"[{settings.Stablecoin}](https://etherscan.io/address/{settings.Stablecoin})")
    st.write(f"[{settings.PriceOracle}](https://etherscan.io/address/{settings.PriceOracle})")
    st.write(f"[{settings.Monetarypolicy}](https://etherscan.io/address/{settings.Monetarypolicy})")
    st.write(f"[{settings.Swapfactory}](https://etherscan.io/address/{settings.Swapfactory})")
    st.write(f"[{settings.PriceAggregator}](https://etherscan.io/address/{settings.PriceAggregator})")
