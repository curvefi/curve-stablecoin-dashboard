import pandas as pd
import streamlit as st

from data.postitions_3 import get_positions

# Config
st.set_page_config(page_title="Positions", page_icon="💳", layout="wide")

# Title
st.title("Positions")

# Positions
positions = get_positions()

for controller in positions:
    st.write(f"Positions for {controller.collateral} [Controller](https://etherscan.io/address/{controller.address}):")
    df = pd.DataFrame(controller.positions, columns=["user", "collateral", "stablecoin", "debt", "N"])
    st.table(df.astype(str))
