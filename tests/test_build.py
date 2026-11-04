"""Step 6.3 test (instruction 06 B.3): a build is byte identical from run to run."""

import hashlib

from bpb.cli import build


def _hashes(root) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_build_twice_identical(built, tmp_path):
    build(tmp_path)
    first, second = _hashes(built), _hashes(tmp_path)
    assert sorted(first) == sorted(second)
    assert [name for name in first if first[name] != second[name]] == []
