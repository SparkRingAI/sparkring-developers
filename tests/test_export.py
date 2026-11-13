"""Exercise exports without real credentials, network access, or user notes."""
import importlib.util
from pathlib import Path

import httpx
import pytest

spec = importlib.util.spec_from_file_location(
    "export_notes", Path(__file__).resolve().parents[1] / "examples/export_notes.py"
)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


@pytest.fixture
def transport(monkeypatch):
    monkeypatch.setenv("SPARKRING_API_URL", "https://api.example.test/v1/developer")
    monkeypatch.setenv("SPARKRING_API_KEY", "fictional-test-key")
    original = httpx.Client

    def install(handler):
        monkeypatch.setattr(exporter.httpx, "Client", lambda **kwargs: original(
            transport=httpx.MockTransport(handler), **kwargs
        ))

    return install


def test_pagination_and_existing_notes_remain_untouched(tmp_path, transport):
    existing = tmp_path / "sparkring-note-3.md"
    existing.write_text("My own edited note", encoding="utf-8")
    calls = []

    def handler(request):
        calls.append(request)
        cursor = request.url.params.get("before_id")
        return httpx.Response(200, json={
            "items": [{"id": "2" if cursor else "3", "title": "Garden\nplan", "markdown": "Plant herbs."}],
            "next_before_id": None if cursor else "3",
        })

    transport(handler)
    assert exporter.export(tmp_path) == 1
    assert len(calls) == 2
    assert calls[1].url.params["before_id"] == "3"
    assert existing.read_text() == "My own edited note"
    assert (tmp_path / "sparkring-note-2.md").read_text() == "# Garden plan\n\nPlant herbs.\n"
    assert exporter.export(tmp_path) == 0


def test_path_injection_and_redirect_are_rejected(tmp_path, transport):
    transport(lambda request: httpx.Response(200, json={"items": [
        {"id": "../../outside", "title": "Garden", "markdown": "Herbs"}
    ], "next_before_id": None}))
    with pytest.raises(ValueError, match="Invalid note ID"):
        exporter.export(tmp_path)
    assert list(tmp_path.iterdir()) == []

    calls = []
    def redirect(request):
        calls.append(request)
        return httpx.Response(302, headers={"Location": "https://elsewhere.example.test"}, text="PRIVATE_BODY")
    transport(redirect)
    with pytest.raises(ValueError, match="HTTP 302") as error:
        exporter.export(tmp_path)
    assert "PRIVATE_BODY" not in str(error.value)
    assert len(calls) == 1


def test_repeated_cursor_stops_export(tmp_path, transport):
    transport(lambda request: httpx.Response(200, json={"items": [], "next_before_id": "1"}))
    with pytest.raises(ValueError, match="Repeated cursor"):
        exporter.export(tmp_path)
