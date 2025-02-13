import numpy as np

def binomial_tree_price(S, K, T, r, sigma, N, option_type):
    """
    Binomial Tree model for American option pricing.
    
    Parameters:
    S - Current stock price
    K - Strike price
    T - Time to expiration (years)
    r - Risk-free rate (as a decimal)
    sigma - Volatility (as a decimal)
    N - Number of steps in the binomial tree
    option_type - 'call' or 'put'

    Returns:
    Option price
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Initialize asset price tree
    stock_price = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            stock_price[j, i] = S * (u ** (i - j)) * (d ** j)

    # Initialize option price tree
    option_price = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        if option_type == "call":
            option_price[j, N] = max(0, stock_price[j, N] - K)
        else:
            option_price[j, N] = max(0, K - stock_price[j, N])

    # Backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_price[j, i] = np.exp(-r * dt) * (p * option_price[j, i + 1] + (1 - p) * option_price[j + 1, i + 1])
            if option_type == "call":
                option_price[j, i] = max(option_price[j, i], stock_price[j, i] - K)
            else:
                option_price[j, i] = max(option_price[j, i], K - stock_price[j, i])

    return option_price[0, 0]
