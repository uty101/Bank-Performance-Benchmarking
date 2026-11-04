"""Step 3.4 test (instruction 03 Section C) and step 6.0 test (instruction 06b B.1)."""

import pandas as pd

from bpb.market import in_price_ccy, unsplit


def test_gbp_pence():
    prices = pd.DataFrame({"date": ["2025-12-31"] * 2, "ticker": ["P.L", "Q.L"], "close": [450.0, 450.0]})
    ccy = pd.DataFrame({"ticker": ["P.L", "Q.L"], "currency": ["GBp", "GBP"]})
    out = in_price_ccy(prices, ccy).set_index("ticker")
    assert out.loc["P.L", "price"] == 4.5 and out.loc["P.L", "price_ccy"] == "GBP"
    assert out.loc["Q.L", "price"] == 450.0 and out.loc["Q.L", "price_ccy"] == "GBP"


def test_unsplit():
    dates = ["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"]
    prices = pd.DataFrame({"date": dates, "ticker": "P.L", "close": [8.0, 9.0, 10.0, 11.0]})

    def after(ratio):
        splits = pd.DataFrame({"ticker": ["P.L"], "date": ["2022-01-05"], "ratio": [ratio]})
        return unsplit(prices, splits)["close"].tolist()

    assert after(0.1) == [8.0 * 0.1, 9.0 * 0.1, 10.0, 11.0]  # a 1:10 consolidation
    assert after(2.0) == [16.0, 18.0, 10.0, 11.0]  # a 2:1 split
