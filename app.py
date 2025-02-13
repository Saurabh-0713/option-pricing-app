import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pricing.black_scholes import black_scholes_price
from pricing.greeks import black_scholes_greeks
from pricing.implied_volatility import implied_volatility
from pricing.binomial_tree import binomial_tree_price
from pricing.data_fetch import get_stock_data

st.set_page_config(page_title="Option Pricing Calculator", layout="wide")

st.title("📈 Option Pricing Calculator")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
market_type = st.sidebar.selectbox("Select Market Type", ["European (Black-Scholes)", "American (Binomial Tree)"])
use_live_data = st.sidebar.checkbox("Use Live Market Data")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")
strike_price = st.sidebar.number_input("Strike Price", min_value=0.0, value=100.0)
time_to_expiration = st.sidebar.number_input("Time to Expiration (Years)", min_value=0.01, value=1.0)
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", min_value=0.0, value=5.0) / 100
volatility = st.sidebar.number_input("Volatility (%)", min_value=0.1, value=20.0) / 100

if use_live_data:
    stock_data = get_stock_data(ticker)
    if stock_data:
        stock_price = stock_data["last_price"]
    else:
        st.sidebar.error("Failed to fetch stock data. Using default value.")
        stock_price = 100.0
else:
    stock_price = st.sidebar.number_input("Stock Price", min_value=0.0, value=100.0)

# Option Pricing Logic
if market_type == "European (Black-Scholes)":
    call_price = black_scholes_price(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, "call")
    put_price = black_scholes_price(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, "put")
else:  # American Option (Binomial Tree)
    call_price = binomial_tree_price(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, 100, "call")
    put_price = binomial_tree_price(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, 100, "put")

st.markdown(f"### Live Stock Price: ${stock_price:.2f}")
st.success(f"**Call Option Price:** ${call_price:.2f}")
st.error(f"**Put Option Price:** ${put_price:.2f}")

# Greeks (Only for Black-Scholes)
if market_type == "European (Black-Scholes)":
    st.subheader("📊 Option Greeks")
    call_greeks = black_scholes_greeks(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, "call")
    put_greeks = black_scholes_greeks(stock_price, strike_price, time_to_expiration, risk_free_rate, volatility, "put")

    greeks_table = """
    | Greek  | Call Value | Put Value |
    |--------|-----------|-----------|
    | Delta  | {:.4f}    | {:.4f}    |
    | Gamma  | {:.4f}    | {:.4f}    |
    | Theta  | {:.4f}    | {:.4f}    |
    | Vega   | {:.4f}    | {:.4f}    |
    | Rho    | {:.4f}    | {:.4f}    |
    """.format(call_greeks["Delta"], put_greeks["Delta"],
               call_greeks["Gamma"], put_greeks["Gamma"],
               call_greeks["Theta"], put_greeks["Theta"],
               call_greeks["Vega"], put_greeks["Vega"],
               call_greeks["Rho"], put_greeks["Rho"])

    st.markdown(greeks_table)

# Implied Volatility Calculation (Only for Black-Scholes)
if market_type == "European (Black-Scholes)":
    st.subheader("📉 Implied Volatility")
    market_price = st.number_input("Enter Market Price of Option", min_value=0.0, value=call_price)
    if st.button("Calculate Implied Volatility"):
        iv = implied_volatility(stock_price, strike_price, time_to_expiration, risk_free_rate, market_price, "call")
        if iv:
            st.info(f"**Implied Volatility:** {iv * 100:.2f}%")
        else:
            st.warning("Could not determine implied volatility.")

# Heatmap: Option Price vs. Spot Price & Volatility
st.subheader("📊 Option Price Sensitivity Heatmaps")

spot_prices = np.linspace(stock_price * 0.8, stock_price * 1.2, 10)
volatilities = np.linspace(0.1, 0.3, 10)

call_heatmap_data = np.zeros((len(volatilities), len(spot_prices)))
put_heatmap_data = np.zeros((len(volatilities), len(spot_prices)))

for i, v in enumerate(volatilities):
    for j, s in enumerate(spot_prices):
        call_heatmap_data[i, j] = black_scholes_price(s, strike_price, time_to_expiration, risk_free_rate, v, "call")
        put_heatmap_data[i, j] = black_scholes_price(s, strike_price, time_to_expiration, risk_free_rate, v, "put")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.heatmap(call_heatmap_data, annot=True, fmt=".2f", xticklabels=np.round(spot_prices, 2), yticklabels=np.round(volatilities, 2), cmap="viridis", ax=axes[0], annot_kws={"size": 8})
axes[0].set_title("Call Price Heatmap")
axes[0].set_xlabel("Spot Price")
axes[0].set_ylabel("Volatility")

sns.heatmap(put_heatmap_data, annot=True, fmt=".2f", xticklabels=np.round(spot_prices, 2), yticklabels=np.round(volatilities, 2), cmap="viridis", ax=axes[1], annot_kws={"size": 8})
axes[1].set_title("Put Price Heatmap")
axes[1].set_xlabel("Spot Price")
axes[1].set_ylabel("Volatility")

st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("🔹 **Developed by Saurabh**")
