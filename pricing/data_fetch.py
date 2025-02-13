import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    
    if data.empty:
        return None
    
    return {
        "last_price": data["Close"].iloc[-1],
        "open": data["Open"].iloc[-1],
        "high": data["High"].iloc[-1],
        "low": data["Low"].iloc[-1],
        "volume": data["Volume"].iloc[-1]
    }

# Example usage
if __name__ == "__main__":
    ticker = "AAPL"
    stock_data = get_stock_data(ticker)
    if stock_data:
        print(f"Stock Data for {ticker}: {stock_data}")
    else:
        print(f"No data available for {ticker}")
