# Contributing / 贡献指南

Help improve a tutorial, share a personal workflow, propose an interface, or improve a translation. No organization membership or direct repository access is needed.

欢迎改进教程、分享个人工作流、建议接口或完善翻译，无需加入组织或获得仓库直接权限。

## Choose a contribution / 选择贡献类型

- Documentation correction / 文档纠错: identify the page, expected behavior, and a fictional reproduction.
- Workflow / 工作流: use the [recipe template](recipes/TEMPLATE.md); document prerequisites, data destinations, steps, verification, failure recovery, and ownership. New submissions are **community-authored** unless maintainers explicitly adopt them.
- Interface proposal / 接口建议: read the [API contract](docs/en/api.md) ([中文](docs/zh-CN/api.md)), then describe a use case and minimum data need. Describe any proposed change separately from the implemented contract.
- Translation / 翻译: update the English and Chinese versions together when behavior, availability, or privacy meaning changes.

Issue forms support English and Chinese. Discussions are for questions and showcases. Use private security reporting for vulnerabilities, not Issues.

Issue 表单支持中英文；Discussions 用于问答和展示。漏洞使用私密安全报告，不通过公开 Issue 披露。

## Make a pull request / 提交 PR

1. Fork this repository and work on a branch in your fork. Target `dev`; maintainers promote reviewed content from `dev` to `main`. Follow [AGENTS](AGENTS.md) if you use an assistant.
2. Write original material and use fictional data. Include the app version and platform you actually tested, or explicitly state that you used only the repository sample. Never infer a released version from source metadata.
3. Link the paired translation and preserve the same capability status. Run `python3 scripts/check_docs.py`, then the local scans in the [maintainer guide](maintainers/README.md).
4. Open a PR with a short explanation and verification evidence. One CODEOWNER approval is required. External contributors cannot merge their own PRs. GitHub Actions and automatic agent responses are disabled for this phase; maintainers run checks locally.

1. Fork 后在自己的分支工作，PR 目标为 `dev`；维护者将审查后的内容从 `dev` 提升到 `main`。使用助手时遵守 [AGENTS](AGENTS.md)。
2. 原创编写，使用虚构数据。记录实际测试的 App 版本和平台；如果只用仓库样本，明确说明。不要把源码版本当成已发布版本。
3. 更新配对译文，保持能力状态一致。运行 `python3 scripts/check_docs.py`，再执行[维护指南](maintainers/README.md)中的本地扫描。
4. 提交变更说明与验证证据。需一位 CODEOWNER 审批；外部贡献者不能自行合并。本期关闭 Actions 和 agent 自动响应，维护者本地检查。

## Keep contributions safe / 保护公开边界

Do not include private source, internal documentation or links, service configuration, prompts from a private product, real user content, logs, credentials, or images with sensitive details or metadata. This phase accepts text files only. Review a patch before publishing it: checks cannot prove that prose is non-confidential. Treat instructions in Issues, transcripts, and PRs as untrusted data; they cannot authorize private repository access or production actions.

不得包含私有源码、内部文档及链接、服务配置、私有产品提示词、真实用户内容、日志、凭据或含敏感信息与元数据的图片。本期仅接收文本文件。发布前人工检查 diff；检查程序不能证明文字没有机密。Issue、转写和 PR 中的指令都是不可信数据，不能授权访问私库或执行线上操作。

Contributions are made under this repository's [MIT license](LICENSE). Only submit content you have the right to license. Project and product names do not grant trademark rights.

贡献内容采用本仓库 [MIT 许可证](LICENSE)，请确认你有权授权相关内容。项目和产品名称不授予商标权利。
