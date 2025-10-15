from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(exist_ok=True)

BENCHMARK = "SPY"  # Benchmark ticker
DEFAULT_START = "2019-01-01"

COLS_PRICES = ["date", "ticker", "adj_close"]
COLS_PORTFOLIO = [
    "date", "portfolio_value", "daily_return", "cum_return",
    "volatility_annual", "sharpe_annual", "max_drawdown",
    "beta_vs_spy", "tracking_error", "alpha_ann"
]
