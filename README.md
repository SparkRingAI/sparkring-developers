# SparkRing Developers

[简体中文](README.zh-CN.md)

Connect your SparkRing transcripts, notes, and action items to the tools you use every day.

- **REST API** — read your text with scoped, expiring personal keys.
- **MCP** — let a compatible desktop assistant read your content through the same API.
- **Workflows** — save notes in Obsidian, prepare a weekly review, or build your own integration.

## Get connected

1. In SparkRing, open **Account → Developer access**.
2. Name your key, select the text you want to share, and choose its expiry. Save the key when it appears.
3. Copy the API base URL shown on that page.
4. Follow the [API quickstart](docs/en/api.md) or [MCP setup](docs/en/mcp.md).

**Developer preview:** the API, local MCP adapter, and app key-management flow have been verified in development. Access requires a development app with the developer-access screen and an enabled service. Public production availability has not been announced.

## Build a workflow

- [API → Markdown / Obsidian](docs/en/api-to-obsidian.md)
- [Transcript → Markdown](docs/en/transcript-to-markdown.md)
- [Transcript → your chosen AI tool](docs/en/transcript-to-ai.md)

Examples use fictional text. Review content before sending it to another service. [Data and privacy](docs/en/data-and-privacy.md) explains keys, scopes, and data destinations.

## Build with us

Share recipes, ask questions in [Discussions](https://github.com/SparkRingAI/sparkring-developers/discussions), or submit an [Issue](https://github.com/SparkRingAI/sparkring-developers/issues) or pull request. You can contribute through a fork without joining our organization.

[Documentation](docs/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md)

The docs, MCP adapter, and examples here are [MIT licensed](LICENSE). That license covers this repository's content.
