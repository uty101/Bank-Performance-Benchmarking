"""Regenerates every output from committed raw and manual files (no network): the same as `bpb build`.

usage: python scripts/run_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpb.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["build"]))
