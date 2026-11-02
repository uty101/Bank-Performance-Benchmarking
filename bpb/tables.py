"""Output table writing (rule 9: float format %.10g, LF line endings, UTF-8, no index column)."""

from pathlib import Path

import pandas as pd


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = df.to_csv(index=False, float_format="%.10g", lineterminator="\n")
    path.write_bytes(text.encode("utf-8"))
    return path
