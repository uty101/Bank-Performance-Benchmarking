"""A full build into a temporary folder, shared by the tests that read one (rule 7, OPEN-14 (a))."""

import pytest

from bpb.cli import build


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    root = tmp_path_factory.mktemp("build")
    build(root)
    return root
