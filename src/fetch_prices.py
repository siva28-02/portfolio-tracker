import pandas as pd
import yfinance as yf
from utils import DATA_DIR, OUT_DIR, DEFAULT_START

def load_universe():
    holdings = pd.read_csv(DATA_DIR / "portfolio_holdings.csv")
    tx = pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["trade_date"])
    tickers = sorted(set(holdings["ticker"]) | set(tx["ticker"]))
    return tickers

def fetch_prices(tickers, start=DEFAULT_START):
    data = yf.download(" ".join(tickers), start=start, auto_adjust=True, progress=False)["Close"]
    data = data.reset_index().melt(id_vars=["Date"], var_name="ticker", value_name="adj_close")
    data.rename(columns={"Date": "date"}, inplace=True)
    data.dropna(subset=["adj_close"], inplace=True)
    return data

if __name__ == "__main__":
    tickers = load_universe()
    prices = fetch_prices(tickers)
    prices.to_csv(OUT_DIR / "prices_daily.csv", index=False)
    print(f"Saved {len(prices):,} rows to output/prices_daily.csv")
