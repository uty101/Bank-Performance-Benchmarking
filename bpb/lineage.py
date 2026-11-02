"""Lineage IDs (Convention 4.13). `trace` is built in step 6.2."""

import hashlib


def lineage_id(bank_id: str, ref_date: str, field: str, family: str, locator: str) -> str:
    """First 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator`."""
    key = f"{bank_id}|{ref_date}|{field}|{family}|{locator}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
