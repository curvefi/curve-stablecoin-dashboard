import streamlit as st

from data.pages.deployments_1 import get_deployments
from settings import settings

deployments = get_deployments()


def format_name_address(mapping: dict[str, str]) -> str:
    s = ", ".join([f"[{k}](https://etherscan.io/address/{v})" for k, v in mapping.items()])
    return s


# Config
st.set_page_config(page_title="Deployments", page_icon="⚙️", layout="wide")

# Deployments
st.subheader("Deployment")

col1, col2 = st.columns(2)

with col1:
    st.write("Stablecoin:")
    st.write("Minter:")
    st.write("Collaterals:")
    st.write("AMMs:")
    st.write("Controllers:")
    st.write("Price Oracle:")
    st.write("Monetary policy:")
    st.write("Swap factory:")
    st.write("Price Aggregator:")
    st.write("Stablecoin pools:")
    st.write("PegKeepers:")

with col2:
    st.write(f"[{settings.Stablecoin}](https://etherscan.io/address/{settings.Stablecoin})")
    st.write(f"[{deployments.controller_factory}](https://etherscan.io/address/{deployments.controller_factory})")
    st.write(format_name_address(deployments.collaterals))
    st.write(format_name_address(deployments.amms))
    st.write(format_name_address(deployments.controllers))
    st.write(f"[{settings.PriceOracle}](https://etherscan.io/address/{settings.PriceOracle})")
    st.write(f"[{settings.Monetarypolicy}](https://etherscan.io/address/{settings.Monetarypolicy})")
    st.write(f"[{settings.Swapfactory}](https://etherscan.io/address/{settings.Swapfactory})")
    st.write(f"[{settings.PriceAggregator}](https://etherscan.io/address/{settings.PriceAggregator})")
    st.write(format_name_address(deployments.stableswaps))
    st.write(format_name_address(deployments.peg_keepers))
