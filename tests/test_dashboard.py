"""Dashboard tests (instruction 06c B.4, instruction 06d B.3). AppTest runs the app on a loopback socket, so these 2
tests, and only these, allow 127.0.0.1 under `--disable-socket` (rule 7, amendment 53)."""

import socket

import pytest
from pytest_socket import SocketConnectBlockedError
from streamlit.testing.v1 import AppTest

from bpb.ingest import ROOT

BANKS = ["LLOY", "ISP", "SWED"]  # instruction 06c B.4
TIMEOUT = 300  # seconds per run: the first run reads every table


@pytest.mark.allow_hosts(["127.0.0.1"])
def test_dashboard_runs(built, monkeypatch):
    monkeypatch.setenv("BPB_ROOT", str(built))
    at = AppTest.from_file(str(ROOT / "bpb" / "dashboard.py"), default_timeout=TIMEOUT).run()
    for bank in BANKS:
        at.selectbox[0].set_value(bank).run()
        assert at.selectbox[0].value == bank
        assert not at.exception


@pytest.mark.allow_hosts(["127.0.0.1"])
def test_dashboard_no_external():
    with pytest.raises(SocketConnectBlockedError), socket.create_connection(("example.com", 80), timeout=5):
        pass
