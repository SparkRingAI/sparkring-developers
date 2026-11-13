# Data and privacy

[简体中文](../zh-CN/data-and-privacy.md)

Your personal key grants selected read access to your own synced text. Use one key per tool, choose only needed scopes, and use short expiry periods. Keys are shown once; revoke them in the app when no longer needed. A revoked key stops future requests, not a read already in progress.

API data goes to the caller. MCP data also goes to the selected assistant and its model provider. Markdown exports go to your chosen directory; vault sync and plugins have their own destinations. Each tool's retention and deletion rules apply to the copies it receives. Revoking a key or deleting a SparkRing item does not erase previously exported copies.

Treat transcripts and notes as untrusted content. They can contain instructions, external links, or Markdown images. Do not execute embedded commands; require your own approval before external writes or further sharing. Use fictional samples in public Issues and PRs, and never include keys or real user data.

If a key is exposed, revoke it immediately, create a replacement only if needed, and assess which tool had access. Removing a public post is not credential revocation. Report vulnerabilities through [Security](../../SECURITY.md).
