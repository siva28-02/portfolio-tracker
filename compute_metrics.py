import pandas as pd
import numpy as np
from utils import DATA_DIR, OUT_DIR, BENCHMARK

CLIP = 1e3  # cap daily returns

def build_positions_daily(prices, tx):
    all_days = prices["date"].drop_duplicates().sort_values()
    tickers = prices["ticker"].drop_duplicates()
    idx = pd.MultiIndex.from_product([all_days, tickers], names=["date", "ticker"])

    tx2 = tx.copy()
    tx2["fees"] = tx2.get("fees", 0.0)
    tx2 = tx2.rename(columns={"trade_date": "date"})
    tx_daily = tx2.groupby(["date", "ticker"]).agg({"quantity": "sum"}).reset_index()

    qty = (tx_daily.set_index(["date", "ticker"]).reindex(idx).fillna(0.0)
           .groupby(level=1).cumsum().reset_index())

    df_prices = prices.set_index(["date", "ticker"]).loc[idx].reset_index()
    df = df_prices.merge(qty, on=["date", "ticker"], how="left")
    df["quantity"] = df["quantity"].fillna(0.0)
    df["position_value"] = df["quantity"] * df["adj_close"]
    return df

def _safe_daily_return(values: pd.Series) -> pd.Series:
    values = pd.to_numeric(values, errors="coerce").fillna(0.0)
    prev = values.shift(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        ret = values / prev - 1.0
    # Invalid when prev<=0 or non-finite → 0
    ret = ret.where((prev > 0) & np.isfinite(ret), 0.0)
    ret = ret.replace([np.inf, -np.inf], 0.0).fillna(0.0)
    ret = ret.clip(-CLIP, CLIP).astype(float)
    return ret

def compute_portfolio_kpis(positions_daily, prices):
    pv = positions_daily.groupby("date")["position_value"].sum().reset_index(name="portfolio_value")

    pv["daily_return"] = _safe_daily_return(pv["portfolio_value"])
    pv["cum_return"] = (1.0 + pv["daily_return"]).cumprod() - 1.0

    ann_factor = np.sqrt(252.0)
    roll_std = pv["daily_return"].rolling(252).std()
    pv["volatility_annual"] = roll_std * ann_factor
    with np.errstate(divide="ignore", invalid="ignore"):
        sharpe = (pv["daily_return"].rolling(252).mean() * 252.0) / (roll_std * ann_factor)
    pv["sharpe_annual"] = sharpe.replace([np.inf, -np.inf], np.nan)

    roll_max = pv["portfolio_value"].cummax().replace(0, np.nan)
    drawdown = pv["portfolio_value"] / roll_max - 1.0
    pv["max_drawdown"] = drawdown.rolling(252, min_periods=1).min()

    # Benchmark returns
    bench = prices[prices["ticker"] == BENCHMARK][["date", "adj_close"]].rename(columns={"adj_close": "bench"})
    merged = pv.merge(bench, on="date", how="left")
    merged["bench_ret"] = _safe_daily_return(merged["bench"])

    # Rolling beta/alpha/tracking error via NumPy (no sklearn)
    betas, alphas, te = [], [], []
    window = 126
    for i in range(len(merged)):
        if i < window:
            betas.append(np.nan); alphas.append(np.nan); te.append(np.nan); continue

        y = merged["daily_return"].iloc[i-window+1:i+1].to_numpy(dtype=float)
        x = merged["bench_ret"].iloc[i-window+1:i+1].to_numpy(dtype=float)

        # strict finite-mask
        mask = np.isfinite(x) & np.isfinite(y)
        xw, yw = x[mask], y[mask]
        if len(xw) < 20:
            betas.append(np.nan); alphas.append(np.nan); te.append(np.nan); continue
        vx = xw.var()
        if np.isclose(vx, 0.0):
            betas.append(np.nan); alphas.append(np.nan); te.append(np.nan); continue

        # beta = cov(x,y)/var(x); alpha_daily = mean(y)-beta*mean(x)
        cov_xy = np.cov(xw, yw, ddof=1)[0,1]
        beta = cov_xy / vx
        alpha_daily = float(yw.mean() - beta * xw.mean())
        residuals = yw - (alpha_daily + beta * xw)

        betas.append(float(beta))
        alphas.append(float(alpha_daily * 252.0))     # annualize
        te.append(float(residuals.std(ddof=1) * np.sqrt(252.0)))  # annualized tracking error

    pv["beta_vs_spy"] = betas
    pv["tracking_error"] = te
    pv["alpha_ann"] = alphas
    return pv

if __name__ == "__main__":
    prices = pd.read_csv(OUT_DIR / "prices_daily.csv", parse_dates=["date"])
    tx = pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["trade_date"])
    positions_daily = build_positions_daily(prices, tx)
    positions_daily.to_csv(OUT_DIR / "positions_daily.csv", index=False)
    kpis = compute_portfolio_kpis(positions_daily, prices)
    kpis.to_csv(OUT_DIR / "portfolio_daily.csv", index=False)
    print("KPIs computed and saved to output/")
