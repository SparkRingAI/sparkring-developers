# SparkRing 开发者社区

[English](README.md)

把 SparkRing 的转写、笔记和行动项接入你每天使用的工具。

- **REST API**：通过有权限范围和有效期的个人密钥读取自己的文字数据。
- **MCP**：让支持本地 MCP 的桌面助手通过同一 API 读取内容。
- **工作流**：保存到 Obsidian、准备周回顾，或共创自己的接入方案。

## 开始接入

1. 在 SparkRing 中打开 **账号 → 开发者接入**。
2. 为密钥命名，选择允许读取的内容和有效期；创建后立即保存密钥。
3. 复制该页面显示的 API 基础地址。
4. 按照 [API 快速开始](docs/zh-CN/api.md)或 [MCP 配置](docs/zh-CN/mcp.md)接入。

**开发者预览：** API、本地 MCP 适配器和 App 密钥管理流程已在开发环境验证。接入需要带开发者接入页面的开发版 App，以及已启用的服务。目前尚未宣布生产环境公开可用。

## 创建工作流

- [API → Markdown / Obsidian](docs/zh-CN/api-to-obsidian.md)
- [转写 → Markdown](docs/zh-CN/transcript-to-markdown.md)
- [转写 → 自选 AI 工具](docs/zh-CN/transcript-to-ai.md)

示例使用虚构内容。将内容交给其他服务前先检查。[数据与隐私](docs/zh-CN/data-and-privacy.md)说明密钥、权限和数据去向。

## 一起共创

欢迎在 [Discussions](https://github.com/SparkRingAI/sparkring-developers/discussions) 分享工作流，在 [Issues](https://github.com/SparkRingAI/sparkring-developers/issues) 提问或提交 PR。通过 fork 即可参与，无需加入组织。

[文档](docs/README.md) · [贡献指南](CONTRIBUTING.md) · [安全报告](SECURITY.md) · [行为准则](CODE_OF_CONDUCT.md)

文档、MCP 适配器和示例采用 [MIT 许可证](LICENSE)，授权范围限于本仓库内容。
