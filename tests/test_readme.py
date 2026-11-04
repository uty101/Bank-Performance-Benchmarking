"""Step 6.4 tests (instruction 06 B.4)."""

import re

import pandas as pd

from bpb.ingest import ROOT
from scripts.write_readme_tables import README, blocks, read_blocks

DASHES = re.compile("[–—]")
BANNED = re.compile(r"\b(robust|resilient|rigorous|leveraging|grounded)\b", re.IGNORECASE)
LIMIT = 15000  # instruction 06 B.4: under 15 KB


def _written(built) -> list:
    return [README, *sorted((ROOT / "docs").glob("*.md")), *sorted((built / "outputs" / "tables").glob("*.html"))]


def test_tables_match(built):
    text = README.read_bytes().decode("utf-8")
    assert read_blocks(text) == {k: v.strip() for k, v in blocks(built).items()}
    assert len(text.encode("utf-8")) < LIMIT


def test_no_dashes(built):
    assert [p.name for p in _written(built) if DASHES.search(p.read_text(encoding="utf-8"))] == []


def test_no_banned_words(built):
    assert [p.name for p in _written(built) if BANNED.search(p.read_text(encoding="utf-8"))] == []


def test_answers_cover_every_question(built):
    answers = pd.read_csv(built / "outputs" / "tables" / "answers.csv")
    assert sorted(answers["question"].unique()) == [1, 2, 3, 4, 5]
    assert answers[["claim", "source"]].notna().all().all()
