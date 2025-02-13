# Option Pricing Calculator

## Overview
This is a **Streamlit-based web application** that allows users to price European and American options using the **Black-Scholes model** and the **Binomial Tree model**, respectively. The app also calculates **Option Greeks** and **Implied Volatility**, and supports fetching live market data.

## Features
- **European Options**: Priced using the **Black-Scholes model**.
- **American Options**: Priced using the **Binomial Tree model**.
- **Option Greeks**: Delta, Gamma, Theta, Vega, and Rho.
- **Implied Volatility Calculation**.
- **Live Market Data Fetching** (via Yahoo Finance).

## Installation
```sh
# Clone the repository
git clone https://github.com/your-repo/option-pricing-app.git
cd option-pricing-app

# Install dependencies
pip install -r requirements.txt
```

## Usage
```sh
streamlit run app.py
```

## Dependencies
- `streamlit`
- `numpy`
- `scipy`
- `yfinance`

## Future Enhancements
- Option trading strategies
- Monte Carlo simulation for exotic options
- Improved UI with interactive charts

## License
This project is open-source and available under the MIT License.

---
**Developed by:** Saurabh 🚀

