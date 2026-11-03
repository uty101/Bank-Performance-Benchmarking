"""Step 3.4 test (instruction 03 Section C)."""

import pandas as pd

from bpb.market import in_price_ccy


def test_gbp_pence():
    prices = pd.DataFrame({"date": ["2025-12-31"] * 2, "ticker": ["P.L", "Q.L"], "close": [450.0, 450.0]})
    ccy = pd.DataFrame({"ticker": ["P.L", "Q.L"], "currency": ["GBp", "GBP"]})
    out = in_price_ccy(prices, ccy).set_index("ticker")
    assert out.loc["P.L", "price"] == 4.5 and out.loc["P.L", "price_ccy"] == "GBP"
    assert out.loc["Q.L", "price"] == 450.0 and out.loc["Q.L", "price_ccy"] == "GBP"
