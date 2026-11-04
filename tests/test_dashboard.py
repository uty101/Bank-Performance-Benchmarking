"""Step 6.2: the dashboard runs on a build and reads no input outside it."""

from streamlit.testing.v1 import AppTest

from bpb.ingest import ROOT


def test_dashboard_runs(built, monkeypatch):
    monkeypatch.setenv("BPB_ROOT", str(built))
    app = AppTest.from_file(str(ROOT / "bpb" / "dashboard.py"), default_timeout=300).run()
    assert not app.exception
    assert [s.value for s in app.subheader][:2] == ["KPIs", "5 year trends"]
    app.selectbox[0].set_value("CAG").run()  # unlisted, with no decomposition at any date
    assert not app.exception
