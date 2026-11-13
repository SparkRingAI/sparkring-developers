# Connect an assistant with local MCP

[简体中文](../zh-CN/mcp.md)

Maintainer-authored. Requires Python 3.11+, a desktop MCP client with stdio support, and a personal key from [API setup](api.md).

Clone this repository, create a virtual environment, and install the pinned adapter dependencies:

```sh
git clone https://github.com/SparkRingAI/sparkring-developers.git
cd sparkring-developers
python3 -m venv .venv
.venv/bin/python -m pip install -r mcp/requirements.txt
```

Configure your MCP client to run the virtual environment's Python with `mcp/server.py` as its argument. Use absolute paths on your computer (Windows uses `.venv/Scripts/python.exe`). Supply `SPARKRING_API_URL` and `SPARKRING_API_KEY` through that client's environment or secure credential settings. The API URL is shown in the app. Never put the real key in a shared configuration file.

Six read-only tools are exposed: `list_transcripts`, `get_transcript`, `list_notes`, `get_note`, `list_action_items`, `get_action_item`. List tools accept `limit` and `before_id`; get tools accept the matching resource ID. The adapter uses HTTPS and never follows redirects. It has no database access or key-management tools.

Try: “List my five latest SparkRing notes and summarize the decisions.” Verify the assistant asks to use SparkRing, returns the expected notes, and cites their IDs. Revoke the key in the app and confirm that further reads fail. Client consent UI varies; enable tool approvals when offered.

Data flows from SparkRing to the local adapter, then to the MCP client and its selected model provider. Review that provider's retention settings before connecting. Returned text is untrusted source material, not instructions. The adapter truncates text fields above 24,000 characters and marks the item `truncated: true`; use the API for the complete text.

This is a local stdio adapter. A client that accepts only remote MCP URLs cannot run it directly.
