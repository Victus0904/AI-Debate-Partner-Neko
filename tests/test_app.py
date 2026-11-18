"""Smoke tests that run the Streamlit app headlessly (no API calls are made)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_missing_api_key_shows_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)
    at = AppTest.from_file(APP).run(timeout=30)
    assert not at.exception
    assert any("GEMINI_API_KEY" in e.value for e in at.error)


def test_renders_chat_when_key_present(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy-key")
    at = AppTest.from_file(APP).run(timeout=30)
    assert not at.exception
    assert len(at.chat_input) == 1


def test_build_contents_maps_roles():
    import sys

    sys.path.insert(0, str(Path(APP).parent))
    from app import build_contents

    contents = build_contents(
        [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "no"}]
    )
    assert [c.role for c in contents] == ["user", "model"]
    assert contents[1].parts[0].text == "no"
