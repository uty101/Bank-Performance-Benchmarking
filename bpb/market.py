"""Share prices from data/raw/market (instruction 03 B.5; Convention 4.12)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PENCE = "GBp"  # Convention 4.12 and Correction 7: yfinance quotes LSE prices in pence
PENCE_PER_POUND = 100  # Convention 4.12: divided by 100


def in_price_ccy(prices: pd.DataFrame, currency: pd.DataFrame) -> pd.DataFrame:
    """prices (date, ticker, close) with each ticker's yfinance currency (ticker, currency): adds `price`, the close
    in price currency, divided by 100 when the currency is GBp, and `price_ccy` (GBP for GBp)."""
    out = prices.merge(currency, on="ticker", how="left", validate="many_to_one")
    pence = out["currency"] == PENCE
    out["price"] = out["close"].where(~pence, out["close"] / PENCE_PER_POUND)
    out["price_ccy"] = out["currency"].where(~pence, "GBP")
    return out


def unsplit(prices: pd.DataFrame, splits: pd.DataFrame) -> pd.DataFrame:
    """prices (date, ticker, close) back on the shares of their own date (instruction 06 A.1 item 1): yfinance's Close is
    adjusted for splits, so the unadjusted close at t is Close(t) x the product of every ratio in `splits` (ticker, date,
    ratio) dated after t. A consolidation has a ratio below 1."""
    out = prices.copy()
    for s in splits.itertuples(index=False):
        before = (out["ticker"] == s.ticker) & (out["date"] < s.date)
        out.loc[before, "close"] = out.loc[before, "close"] * s.ratio
    return out


def load_prices(raw_root: Path) -> pd.DataFrame:
    raw = Path(raw_root) / "market"
    return in_price_ccy(unsplit(pd.read_parquet(raw / "prices.parquet"), pd.read_csv(raw / "splits.csv")),
                        pd.read_csv(raw / "currency.csv", dtype=str, keep_default_na=False))
