"""Pulls raw data. The only module besides fetch_reports.py that touches the network (CLAUDE.md rule 8).

usage: python scripts/pull_data.py --stage eba [--stage fx ...]   (stages: eba, fx, gleif, market, yields)

Every pull writes an entry per file to data/raw/MANIFEST.json (kickoff Section 3.2).
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import shutil
import sys
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "MANIFEST.json"
DOWNLOAD = ROOT / "data" / "eba_download"  # gitignored, unfiltered originals (OPEN-02)
HEADERS = {"User-Agent": "Mozilla/5.0 (bank-performance-benchmarking data pull)"}
CHUNK = 1 << 20
BOM = b"\xef\xbb\xbf"


def load_cfg() -> dict:
    with open(ROOT / "config.toml", "rb") as f:
        return tomllib.load(f)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def download(url: str, dest: Path, attempts: int = 3) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for i in range(attempts):
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    f.writelines(r.iter_content(CHUNK))
            tmp.replace(dest)
            return
        except requests.RequestException as e:
            print(f"  attempt {i + 1} failed: {e}", file=sys.stderr)
            time.sleep(5)
    raise SystemExit(f"data pull failed: {url}")


def read_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"files": []}


def write_manifest(entries: list[dict]) -> None:
    m = read_manifest()
    by_path = {e["path"]: e for e in m["files"]}
    for e in entries:
        by_path[e["path"]] = e
    m["files"] = [by_path[k] for k in sorted(by_path)]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_bytes((json.dumps(m, indent=2, sort_keys=True) + "\n").encode("utf-8"))


# --- stage eba -------------------------------------------------------------

def period_to_date(p: str) -> str:
    """EBA Period yyyymm (a quarter-end month) to the ISO quarter-end date."""
    y, m = int(p[:4]), int(p[4:6])
    day = {3: 31, 6: 30, 9: 30, 12: 31}[m]
    return f"{y:04d}-{m:02d}-{day:02d}"


def filter_csv(src: Path, dest: Path, countries: set[str]) -> tuple[int, int, list[str]]:
    """Keeps the header and every row whose NSA (the bank's home country) is in `countries`.

    Rows are copied byte for byte. Returns (rows in, rows out, sorted distinct Period values out).
    """
    rows_in = rows_out = 0
    periods: set[str] = set()
    dest.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0 and no file name keep the gzip bytes identical across runs (rule 9)
    with (
        open(src, "rb") as fin,
        open(dest, "wb") as raw_out,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw_out, mtime=0) as fout,
    ):
        header = fin.readline()
        cols = next(csv.reader([header.removeprefix(BOM).decode("latin-1")]))
        i_nsa, i_per = cols.index("NSA"), cols.index("Period")
        fout.write(header)
        for line in fin:
            if not line.strip():
                continue
            rec = next(csv.reader([line.decode("latin-1")]))  # NSA and Period are ASCII
            if len(rec) != len(cols):
                raise SystemExit(f"{src}: row {rows_in + 2} has {len(rec)} fields, header has {len(cols)}")
            rows_in += 1
            if rec[i_nsa] in countries:
                fout.write(line)
                rows_out += 1
                periods.add(rec[i_per])
    return rows_in, rows_out, sorted(periods)


def csv_periods(path: Path) -> tuple[int, list[str]]:
    with open(path, "rb") as f:
        if f.read(len(BOM)) != BOM:
            f.seek(0)
        text = io.TextIOWrapper(f, encoding="latin-1", newline="")
        r = csv.reader(text)
        i_per = next(r).index("Period")
        n, periods = 0, set()
        for rec in r:
            if rec:
                n += 1
                periods.add(rec[i_per])
    return n, sorted(periods)


def text_encoding(path: Path) -> str:
    """utf-8 if the whole file decodes as UTF-8, else cp1252 (recorded in the manifest for readers)."""
    try:
        with open(path, encoding="utf-8") as f:
            for _ in iter(lambda: f.read(CHUNK), ""):
                pass
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


def stage_eba(cfg: dict) -> None:
    eba = cfg["eba"]
    max_bytes = eba["max_commit_mb"] * 1024 * 1024
    with open(ROOT / "data" / "manual" / "universe.csv", encoding="utf-8") as f:
        countries = {r["country"] for r in csv.DictReader(f) if r["country"] != "GB"}
    # instruction 01 Section B item 2 fixes this set
    assert countries == {"FI", "NO", "DK", "SE", "NL", "BE", "FR", "DE", "ES", "IT"}, countries
    with open(ROOT / "data" / "manual" / "eba_urls.csv", encoding="utf-8") as f:
        urls = list(csv.DictReader(f))

    entries = []
    for release in eba["releases"]:
        for name in eba["files"]:
            hits = [u for u in urls if int(u["release"]) == release and u["file"] == name]
            if len(hits) != 1:
                raise SystemExit(f"eba_urls.csv: {len(hits)} rows for {release} {name}")
            url = hits[0]["url"]
            print(f"eba {release} {name}")
            orig = DOWNLOAD / str(release) / name
            pulled = now_utc()
            download(url, orig)
            o_sha, o_bytes = sha256_file(orig), orig.stat().st_size
            if name.endswith(".csv"):
                dest = RAW / "eba" / str(release) / (name + ".gz")
                rows_in, rows_out, periods = filter_csv(orig, dest, countries)
                _, all_periods = csv_periods(orig)
                enc = text_encoding(orig)
                entries.append({
                    "path": rel(orig), "committed": False, "url": url, "pulled_utc": pulled,
                    "sha256": o_sha, "bytes": o_bytes, "rows": rows_in,
                    "first_date": period_to_date(all_periods[0]), "last_date": period_to_date(all_periods[-1]),
                    "encoding": enc,
                })
                f_bytes = dest.stat().st_size
                entries.append({
                    "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
                    "sha256": sha256_file(dest), "bytes": f_bytes, "rows": rows_out,
                    "first_date": period_to_date(periods[0]), "last_date": period_to_date(periods[-1]),
                    "filtered_from": rel(orig), "filter": "NSA in " + ",".join(sorted(countries)), "encoding": enc,
                })
                if f_bytes > max_bytes:
                    write_manifest(entries)
                    raise SystemExit(f"{rel(dest)} is {f_bytes} bytes gzipped, over max_commit_mb (rule 4)")
            else:
                dest = RAW / "eba" / str(release) / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(orig, dest)
                entries.append({
                    "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
                    "sha256": o_sha, "bytes": o_bytes, "rows": None, "first_date": None, "last_date": None,
                })
    write_manifest(entries)


# --- stage fx --------------------------------------------------------------

ECB_URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.{ccy}.EUR.SP00.A?format=csvdata"  # kickoff 3.2
FX_START, FX_END = "2020-01-01", "2026-07-31"  # instruction 01 step 1.4


def stage_fx(cfg: dict) -> None:
    entries = []
    for ccy in cfg["fx"]["currencies"]:
        url = f"{ECB_URL.format(ccy=ccy)}&startPeriod={FX_START}&endPeriod={FX_END}"
        print(f"fx {ccy}")
        dest = RAW / "fx" / f"{ccy}.csv"
        pulled = now_utc()
        download(url, dest)
        with open(dest, encoding="utf-8", newline="") as f:
            recs = list(csv.DictReader(f))
        dates = sorted(r["TIME_PERIOD"] for r in recs)
        if not dates:
            raise SystemExit(f"data pull failed: no rows for {ccy}")
        entries.append({
            "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
            "sha256": sha256_file(dest), "bytes": dest.stat().st_size, "rows": len(recs),
            "first_date": dates[0], "last_date": dates[-1], "encoding": "utf-8",
        })
    write_manifest(entries)


# --- stage gleif -------------------------------------------------------------

GLEIF_URL = "https://api.gleif.org/api/v1/lei-records"  # PLAN step 3.1 (OPEN-11 decided (a))
GLEIF_PAGE = 200


def _gleif_pick(records: list[dict], name: str, country: str) -> list[dict]:
    """The active records for a universe bank (instruction 03 step 3.1 item 1): entity status ACTIVE, registration
    ISSUED, legal address in the bank's country, and legal name equal to the universe name with its company form
    `PLC`, case and spacing normalised. GLEIF's legalName filter is a text search, so the exact name is checked
    here."""
    def norm(s: str) -> str:
        return " ".join(s.upper().split())

    want = norm(f"{name} PLC")
    return [r for r in records
            if r["attributes"]["entity"]["status"] == "ACTIVE"
            and r["attributes"]["registration"]["status"] == "ISSUED"
            and r["attributes"]["entity"]["legalAddress"]["country"] == country
            and norm(r["attributes"]["entity"]["legalName"]["name"]) == want]


def stage_gleif(cfg: dict) -> None:
    """LEIs for the UK banks from GLEIF to data/raw/gleif/{bank_id}.json (every page of the search response), and
    `lei` filled in data/manual/universe.csv. Exactly 1 active record per bank, else the pull fails (rule 4)."""
    path = ROOT / "data" / "manual" / "universe.csv"
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0])
    entries = []
    for r in rows:
        if r["country"] != "GB":
            continue
        params = {"filter[entity.legalName]": r["name"], "filter[entity.status]": "ACTIVE",
                  "filter[entity.legalAddress.country]": r["country"], "page[size]": GLEIF_PAGE, "page[number]": 1}
        pulled, records = now_utc(), []
        while True:
            resp = requests.get(GLEIF_URL, params=params, headers=HEADERS, timeout=120)
            if resp.status_code != 200:
                raise SystemExit(f"data pull failed: gleif {r['bank_id']} HTTP {resp.status_code}")
            page = resp.json()
            records += page["data"]
            if params["page[number]"] >= page["meta"]["pagination"]["lastPage"]:
                break
            params["page[number]"] += 1
        dest = RAW / "gleif" / f"{r['bank_id']}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = {"query": {k: v for k, v in params.items() if not k.startswith("page")}, "data": records}
        dest.write_bytes((json.dumps(body, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
        hits = _gleif_pick(records, r["name"], r["country"])
        if len(hits) != 1:
            raise SystemExit(f"gleif {r['bank_id']}: {len(hits)} active records named {r['name']!r} PLC (rule 4)")
        a = hits[0]["attributes"]
        r["lei"] = a["lei"]
        print(f"{r['bank_id']}: {a['entity']['legalName']['name']} {a['lei']} ({len(records)} search results)")
        entries.append({"path": rel(dest), "committed": True, "url": GLEIF_URL, "pulled_utc": pulled,
                        "sha256": sha256_file(dest), "bytes": dest.stat().st_size, "rows": len(records),
                        "first_date": None, "last_date": None, "encoding": "utf-8"})
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    path.write_bytes(buf.getvalue().encode("utf-8"))
    write_manifest(entries)


# --- stage market --------------------------------------------------------------

MARKET_START, MARKET_END = "2020-12-01", "2026-08-01"  # instruction 03 B.5: to 2026-07-31; yfinance end is exclusive


def stage_market(cfg: dict) -> None:
    """yfinance daily Close (auto_adjust=False) for every listed ticker to data/raw/market/prices.parquet (date,
    ticker, close), and each ticker's quote currency (fast_info, else info) to data/raw/market/currency.csv, so the
    GBp rule (Convention 4.12) is applied from data (instruction 03 B.5)."""
    import pandas as pd
    import yfinance as yf

    with open(ROOT / "data" / "manual" / "universe.csv", encoding="utf-8") as f:
        tickers = [r["ticker"] for r in csv.DictReader(f) if r["listed"] == "1" and r["ticker"]]
    frames, ccys = [], []
    pulled = now_utc()
    for t in tickers:
        print(f"market {t}")
        tk = yf.Ticker(t)
        h = tk.history(start=MARKET_START, end=MARKET_END, auto_adjust=False)
        if h.empty:
            raise SystemExit(f"data pull failed: no prices for {t}")
        try:
            ccy = tk.fast_info["currency"]
        except Exception:  # noqa: BLE001 - fall back to .info, as instruction 03 B.5 allows
            ccy = tk.info.get("currency")
        if not ccy:
            raise SystemExit(f"data pull failed: no currency for {t}")
        dates = pd.DatetimeIndex(h.index).tz_localize(None).normalize().strftime("%Y-%m-%d")
        frames.append(pd.DataFrame({"date": dates, "ticker": t, "close": h["Close"].astype(float).to_numpy()}))
        ccys.append({"ticker": t, "currency": ccy})
    prices = pd.concat(frames, ignore_index=True).sort_values(["ticker", "date"]).reset_index(drop=True)
    dest = RAW / "market" / "prices.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    prices.to_parquet(dest, index=False)
    cdest = RAW / "market" / "currency.csv"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["ticker", "currency"], lineterminator="\n")
    w.writeheader()
    w.writerows(ccys)
    cdest.write_bytes(buf.getvalue().encode("utf-8"))
    entries = [{"path": rel(dest), "committed": True, "url": "yfinance Ticker(t).history(start=" + MARKET_START
                + ", end=" + MARKET_END + ", auto_adjust=False)", "pulled_utc": pulled, "sha256": sha256_file(dest),
                "bytes": dest.stat().st_size, "rows": len(prices), "first_date": prices["date"].min(),
                "last_date": prices["date"].max()},
               {"path": rel(cdest), "committed": True, "url": "yfinance Ticker(t).fast_info['currency']",
                "pulled_utc": pulled, "sha256": sha256_file(cdest), "bytes": cdest.stat().st_size,
                "rows": len(ccys), "first_date": None, "last_date": None, "encoding": "utf-8"}]
    write_manifest(entries)


# --- stage yields --------------------------------------------------------------

# instruction 03b B.1: 10 year sovereign yields from central bank sources (FRED refused the connection in session 3)
ECB_IRS_URL = "https://data-api.ecb.europa.eu/service/data/IRS/M.{cc}.L.L40.CI.0000.{ccy}.N.Z?format=csvdata"
ECB_IRS_CCY = {"SE": "SEK", "DK": "DKK"}  # instruction 03b B.1: EUR for euro area members
BOE_URL = ("https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&Datefrom=01/Jan/2020"
           "&Dateto=31/Jul/2026&SeriesCodes=IUMAMNPY&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N")
NORGES_URL = ("https://data.norges-bank.no/api/data/GOVT_GENERIC_RATES/M.10Y.GBON.?format=csv&startPeriod=2020-01"
              "&endPeriod=2026-07&locale=en")
YIELDS_START, YIELDS_END = "2020-01", "2026-07"
YIELD_COLUMNS = ["period", "yield_pct", "series"]


def _get_text(url: str) -> str:
    for i in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=120)
            r.raise_for_status()
            return r.content.decode("utf-8-sig")
        except requests.RequestException as e:
            print(f"  attempt {i + 1} failed: {e}", file=sys.stderr)
            time.sleep(5)
    raise SystemExit(f"data pull failed: {url}")


def _yields_ecb(cc: str) -> tuple[str, list[dict]]:
    url = ECB_IRS_URL.format(cc=cc, ccy=ECB_IRS_CCY.get(cc, "EUR")) + f"&startPeriod={YIELDS_START}&endPeriod={YIELDS_END}"
    recs = list(csv.DictReader(io.StringIO(_get_text(url))))
    return url, [{"period": r["TIME_PERIOD"], "yield_pct": r["OBS_VALUE"], "series": r["KEY"]} for r in recs
                 if r["OBS_VALUE"] not in ("", "NaN")]


def _yields_boe() -> tuple[str, list[dict]]:
    rows = list(csv.reader(io.StringIO(_get_text(BOE_URL))))
    code = rows[0][1]
    out = []
    for d, v in rows[1:]:
        period = datetime.strptime(d.strip(), "%d %b %Y").strftime("%Y-%m")
        out.append({"period": period, "yield_pct": v.strip(), "series": f"BoE IADB {code}"})
    return BOE_URL, out


def _yields_norges() -> tuple[str, list[dict]]:
    recs = list(csv.DictReader(io.StringIO(_get_text(NORGES_URL)), delimiter=";"))
    return NORGES_URL, [{"period": r["TIME_PERIOD"], "yield_pct": r["OBS_VALUE"],
                         "series": f"Norges Bank GOVT_GENERIC_RATES M.{r['TENOR']}.{r['INSTRUMENT_TYPE']}"}
                        for r in recs if r["OBS_VALUE"]]


def stage_yields(cfg: dict) -> None:
    """Monthly 10 year sovereign yields for every [sovereign] countries entry to data/raw/yields/{CC}.csv (period,
    yield_pct, series): GB from the Bank of England (IUMAMNPY, monthly average 10 year nominal par yield), NO from
    Norges Bank (GOVT_GENERIC_RATES, 10 year government bonds, monthly), every other country from the ECB IRS
    dataset (Maastricht convergence criterion long-term yields), instruction 03b B.1."""
    entries = []
    for cc in cfg["sovereign"]["countries"]:
        print(f"yields {cc}")
        pulled = now_utc()
        url, rows = _yields_boe() if cc == "GB" else _yields_norges() if cc == "NO" else _yields_ecb(cc)
        rows = sorted((r for r in rows if YIELDS_START <= r["period"] <= YIELDS_END), key=lambda r: r["period"])
        if not rows:
            raise SystemExit(f"data pull failed: no rows for {cc}")
        dest = RAW / "yields" / f"{cc}.csv"
        dest.parent.mkdir(parents=True, exist_ok=True)
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=YIELD_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        dest.write_bytes(buf.getvalue().encode("utf-8"))
        entries.append({"path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
                        "sha256": sha256_file(dest), "bytes": dest.stat().st_size, "rows": len(rows),
                        "first_date": rows[0]["period"], "last_date": rows[-1]["period"], "encoding": "utf-8",
                        "series": rows[0]["series"]})
    write_manifest(entries)


STAGES = {"eba": stage_eba, "fx": stage_fx, "gleif": stage_gleif, "market": stage_market, "yields": stage_yields}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", action="append", required=True, choices=sorted(STAGES))
    args = ap.parse_args(argv)
    cfg = load_cfg()
    for s in args.stage:
        STAGES[s](cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
