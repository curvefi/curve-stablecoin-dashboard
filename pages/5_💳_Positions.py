import pandas as pd
import streamlit as st

from data.pages.positions_5 import get_controllers, get_positions

# Config
st.set_page_config(page_title="Positions", page_icon="💳", layout="wide")

# Title
st.title("Positions")

full = st.checkbox("Show health full=true")

# Positions
controllers = get_controllers()
if "pages" not in st.session_state:
    st.session_state.pages = {}

positions = {col_symbol: get_positions(controllers[col_symbol]["collateral"], full=full) for col_symbol in controllers}


def set_page(col_symbol: str, page: int):
    st.session_state.pages[col_symbol] = page


for col_symbol in controllers:
    if col_symbol not in st.session_state.pages:
        set_page(col_symbol, page=1)

    page = st.session_state.pages[col_symbol]
    pagination = 10
    n_loans = positions[col_symbol].n_loans

    st.write(
        f"Positions for {col_symbol} "
        f"[Controller](https://etherscan.io/address/{controllers[col_symbol]['controller']}), total: {n_loans}:"
    )
    curr_positions = positions[col_symbol].positions[(page - 1) * pagination : min(n_loans, page * pagination)]
    df = pd.DataFrame(
        [(p.i, p.user, *p.user_state, p.health) for p in curr_positions],
        columns=["n", "user", "collateral", "stablecoin", "debt", "N", "health"],
    )
    st.table(df.astype(str))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button(
            "Previous",
            key=col_symbol + "previous",
            on_click=set_page,
            kwargs={"col_symbol": col_symbol, "page": page - 1},
            disabled=page == 1,
        )

    with col2:
        st.button(
            "1",
            key=col_symbol + "1",
            on_click=set_page,
            kwargs={"col_symbol": col_symbol, "page": 1},
            disabled=page == 1,
        )

    with col3:
        st.button(
            "Last",
            key=col_symbol + "last",
            on_click=set_page,
            kwargs={"col_symbol": col_symbol, "page": n_loans // pagination + 1},
            disabled=page * pagination > n_loans,
        )
    with col4:
        st.button(
            "Next",
            key=col_symbol + "next",
            on_click=set_page,
            kwargs={"col_symbol": col_symbol, "page": page + 1},
            disabled=page * pagination > n_loans,
        )
