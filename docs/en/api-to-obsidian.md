# API → Markdown / Obsidian

[简体中文](../zh-CN/api-to-obsidian.md)

Maintainer-authored. Prerequisites: [API access](api.md) with `notes:read`, Python 3.11+, and a local folder you control. Install `httpx==0.28.1` and set the API environment variables as described in the quickstart.

Run `python examples/export_notes.py OUTPUT_DIRECTORY`. It exports every available note as `sparkring-note-ID.md`, using ID-based filenames rather than untrusted titles. Existing files are not overwritten. To refresh a snapshot, export into a new empty directory. Copy that directory into your Obsidian vault if desired.

Data goes to your chosen local folder. Vault sync or plugins may send it elsewhere; review those settings. Exported Markdown can contain external links/images; open it in a plain-text editor first. Do not execute embedded commands.

Verify using a fictional note: confirm its title and body match, rerun and confirm existing files remain unchanged. This is a snapshot export, not a deletion-sync service. Revoke the key when finished; exported copies remain until you delete them.
