"""config.toml as frozen dataclasses, one per table (kickoff Section 6.1)."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass(frozen=True)
class Run:
    seed: int


@dataclass(frozen=True)
class Sources:
    eba_first: str
    eba_last: str
    report_dates_eu: tuple[str, ...]
    report_first_uk: str
    latest: str


@dataclass(frozen=True)
class Eba:
    releases: tuple[int, ...]
    files: tuple[str, ...]
    max_commit_mb: int


@dataclass(frozen=True)
class Fx:
    currencies: tuple[str, ...]


@dataclass(frozen=True)
class Sovereign:
    countries: tuple[str, ...]
    benchmark: str


@dataclass(frozen=True)
class Checks:
    bs_tol: float
    income_tol: float
    cet1_tol_bps: float
    seam_capital_tol: float
    outlier_z: float


@dataclass(frozen=True)
class Merger:
    merger_materiality: float


@dataclass(frozen=True)
class Peers:
    first_year: int
    k_range: tuple[int, ...]
    min_cluster_size: int
    stability_reps: int
    stability_flag: float
    peer_seed: int


@dataclass(frozen=True)
class Bench:
    min_peers: int
    bench_reps: int
    bench_seed: int
    ci: float


@dataclass(frozen=True)
class Gaps:
    sized: tuple[str, ...]
    hand_check_banks: tuple[str, ...]
    hand_check_tol_eur: float


@dataclass(frozen=True)
class Drivers:
    tol_pts: float


@dataclass(frozen=True)
class Valuation:
    growth: float
    ci: float
    cooks_factor: float


@dataclass(frozen=True)
class TaxFallback:
    GB: float
    SE: float
    NO: float
    DK: float
    FI: float
    NL: float
    BE: float
    FR: float
    DE: float
    ES: float
    IT: float


@dataclass(frozen=True)
class Tolerances:
    ratio_recompute: float
    fx_roundtrip: float


@dataclass(frozen=True)
class Config:
    run: Run
    sources: Sources
    eba: Eba
    fx: Fx
    sovereign: Sovereign
    checks: Checks
    merger: Merger
    peers: Peers
    bench: Bench
    gaps: Gaps
    drivers: Drivers
    valuation: Valuation
    tax_fallback: TaxFallback
    tolerances: Tolerances
    root: Path  # the directory holding config.toml; every repo path is relative to it


def _build(cls, table: dict):
    names = {f.name for f in fields(cls)}
    if set(table) != names:
        raise ValueError(f"{cls.__name__}: keys {sorted(table)} != {sorted(names)}")
    return cls(**{k: tuple(v) if isinstance(v, list) else v for k, v in table.items()})


def load_config(path: str | Path = "config.toml") -> Config:
    path = Path(path).resolve()
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    tables = {f.name: f.type for f in fields(Config) if f.name != "root"}
    if set(raw) != set(tables):
        raise ValueError(f"config tables {sorted(raw)} != {sorted(tables)}")
    classes = {c.__name__: c for c in (Run, Sources, Eba, Fx, Sovereign, Checks, Merger, Peers, Bench,
                                       Gaps, Drivers, Valuation, TaxFallback, Tolerances)}
    built = {name: _build(classes[typ], raw[name]) for name, typ in tables.items()}
    return Config(**built, root=path.parent)
