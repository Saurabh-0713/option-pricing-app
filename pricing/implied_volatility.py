import numpy as np
import scipy.stats as si
from scipy.optimize import brentq
from pricing.black_scholes import black_scholes_price

def implied_volatility(S, K, T, r, market_price, option_type="call"):
    def objective_function(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price
    
    try:
        iv = brentq(objective_function, 1e-6, 5.0)  # Solve for implied volatility
        return iv
    except ValueError:
        return None

# Example usage
if __name__ == "__main__":
    S = 100  # Stock price
    K = 100  # Strike price
    T = 1    # Time to expiration (years)
    r = 0.05 # Risk-free rate
    market_price = 10  # Observed option price
    
    iv = implied_volatility(S, K, T, r, market_price, "call")
    print(f"Implied Volatility: {iv:.4f}" if iv else "Could not determine IV")
