"""ECB reference rates and conversion to and from EUR (Convention 4.6, instruction 01 step 1.4)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


def ecb_rates(raw_root: Path) -> pd.DataFrame:
    """Daily ECB reference rates from data/raw/fx/{CCY}.csv: date, ccy, per_eur (units of ccy per 1 EUR)."""
    frames = []
    for path in sorted((Path(raw_root) / "fx").glob("*.csv")):
        d = pd.read_csv(path, usecols=["TIME_PERIOD", "CURRENCY", "OBS_VALUE"], dtype={"OBS_VALUE": float})
        frames.append(pd.DataFrame({"date": pd.to_datetime(d["TIME_PERIOD"]), "ccy": d["CURRENCY"],
                                    "per_eur": d["OBS_VALUE"]}))
    rates = pd.concat(frames, ignore_index=True).dropna(subset=["per_eur"])
    return rates.sort_values(["ccy", "date"]).reset_index(drop=True)


def period_start(on: date | str, rolling: bool) -> pd.Timestamp:
    """Start of the P&L period ending at `on` (instruction 01 step 1.4).

    Year to date: 1 Jan of the date's year. Rolling 12 months at 30 Jun of y: 1 Jul of y - 1.
    """
    d = pd.Timestamp(on)
    return pd.Timestamp(d.year - 1, 7, 1) if rolling else pd.Timestamp(d.year, 1, 1)


def rate(ccy: str, on: date | str, kind: str, rates: pd.DataFrame, start: date | str | None) -> float:
    """Units of `ccy` per EUR. kind "bs": the last published rate on or before `on`. kind "pl": the mean of the
    published daily rates d with start <= d <= on. EUR is 1."""
    if ccy == "EUR":
        return 1.0
    r = rates[rates["ccy"] == ccy]
    on = pd.Timestamp(on)
    if kind == "bs":
        r = r[r["date"] <= on]
        if r.empty:
            raise ValueError(f"no {ccy} rate on or before {on.date()}")
        return float(r["per_eur"].iloc[-1])
    if kind == "pl":
        if start is None:
            raise ValueError("a P&L conversion needs period_start")
        r = r[(r["date"] >= pd.Timestamp(start)) & (r["date"] <= on)]
        if r.empty:
            raise ValueError(f"no {ccy} rates from {start} to {on.date()}")
        return float(r["per_eur"].mean())
    raise ValueError(f"kind must be 'bs' or 'pl', not {kind!r}")


def to_eur(value: float, ccy: str, date: date, kind: str, rates: pd.DataFrame, period_start: date | None) -> float:
    return value / rate(ccy, date, kind, rates, period_start)


def from_eur(value: float, ccy: str, date: date, kind: str, rates: pd.DataFrame, period_start: date | None) -> float:
    return value * rate(ccy, date, kind, rates, period_start)
