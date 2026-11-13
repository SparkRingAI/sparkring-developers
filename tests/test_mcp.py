import importlib.util
from pathlib import Path
import os
import sys

import httpx
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sparkring_adapter", ROOT / "mcp/server.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

@pytest.fixture(autouse=True)
def configuration(monkeypatch):
    monkeypatch.setenv("SPARKRING_API_URL", "https://api.example.test/v1/developer")
    monkeypatch.setenv("SPARKRING_API_KEY", "srk_fictional_test_value")

@pytest.mark.asyncio
async def test_fixed_destination_and_field_filter(monkeypatch):
    seen = []
    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"items": [{"id": "1", "title": "Garden", "markdown": "x" * 25000, "internal": "DO_NOT_RETURN"}], "next_before_id": None})
    original = httpx.AsyncClient
    monkeypatch.setattr(adapter.httpx, "AsyncClient", lambda **kwargs: original(transport=httpx.MockTransport(handler), **kwargs))
    result = await adapter.list_notes(limit=5)
    assert str(seen[0].url) == "https://api.example.test/v1/developer/notes?limit=5"
    assert seen[0].headers["Authorization"] == "Bearer srk_fictional_test_value"
    assert len(result["items"][0]["markdown"]) == 24000
    assert result["items"][0]["truncated"] is True
    assert "DO_NOT_RETURN" not in str(result)
    with pytest.raises(ValueError): await adapter.get_note("../../keys")
    assert len(seen) == 1

@pytest.mark.asyncio
async def test_redirect_and_error_bodies_are_not_exposed(monkeypatch):
    original = httpx.AsyncClient
    seen = []
    def handler(request):
        seen.append(request)
        return httpx.Response(302, headers={"Location": "https://elsewhere.example.test/"}, text="PRIVATE_BODY")
    monkeypatch.setattr(adapter.httpx, "AsyncClient", lambda **kwargs: original(transport=httpx.MockTransport(handler), **kwargs))
    with pytest.raises(ValueError) as error: await adapter.list_notes()
    assert "HTTP 302" in str(error.value)
    assert "PRIVATE_BODY" not in str(error.value)
    assert len(seen) == 1

@pytest.mark.parametrize("url", ["http://api.example.test/v1/developer", "https://user:pass@api.example.test/v1/developer", "https://api.example.test/v1/developer?token=x", "https://api.example.test/api"])
def test_reject_unsafe_configuration(monkeypatch, url):
    monkeypatch.setenv("SPARKRING_API_URL", url)
    with pytest.raises(ValueError): adapter.configuration()

@pytest.mark.asyncio
async def test_real_stdio_handshake_and_tool_contract():
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "mcp/server.py")], env={
        **os.environ, "SPARKRING_API_URL": "https://api.example.test/v1/developer", "SPARKRING_API_KEY": "srk_fictional_test_value",
    })
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            assert {tool.name for tool in tools} == {"list_notes", "get_note", "list_transcripts", "get_transcript", "list_action_items", "get_action_item"}
            for tool in tools:
                assert tool.annotations.readOnlyHint is True
                assert "token" not in tool.inputSchema["properties"]
                assert "url" not in tool.inputSchema["properties"]
            result = await session.call_tool("get_note", {"note_id": "../keys"})
            assert result.isError
