# Curve Stablecoin dashboard

Full DApp local dashboard for CRVUSD stats

## Quickstart

### Install packages using poetry

```shell
pip install poetry==1.4.1
poetry install
```

### Settings

Put settings file ("_.env_") into [parent](.) directory.
[Example](./.env-example) defines all required parameters, 
external web3 provider.

Other settings such as addresses of contracts are set in [settings](./settings.py)

### Run project locally

```shell
streamlit run Dashboard.py
```

Dashboard will be available at http://localhost:8502 (browser opens automatically).

## Features

- Deployments, contract addresses for Controllers, Stableswaps, AMMs and other
- Total dept, total collateral, prices
- Plots for CRVUSD/USD and borrow rates
- Positions, health and losses calculator
