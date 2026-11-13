# 使用本地 MCP 连接助手

[English](../en/mcp.md)

本教程由维护者编写。需要 Python 3.11+、支持 stdio 的桌面 MCP 客户端，以及按 [API 指南](api.md)创建的个人密钥。

克隆仓库，创建虚拟环境并安装固定版本依赖：

```sh
git clone https://github.com/SparkRingAI/sparkring-developers.git
cd sparkring-developers
python3 -m venv .venv
.venv/bin/python -m pip install -r mcp/requirements.txt
```

在 MCP 客户端中配置虚拟环境的 Python 为启动命令，参数为 `mcp/server.py`。使用自己电脑上的绝对路径；Windows 的解释器路径是 `.venv/Scripts/python.exe`。通过客户端的环境变量或安全凭据配置提供 `SPARKRING_API_URL` 和 `SPARKRING_API_KEY`，API 地址从 App 复制。不要将真实密钥放入共享配置文件。

提供六个只读工具：`list_transcripts`、`get_transcript`、`list_notes`、`get_note`、`list_action_items`、`get_action_item`。列表工具接受 `limit` 和 `before_id`，详情工具接受对应条目的 ID。适配器使用 HTTPS、不跟随重定向，也没有数据库访问或密钥管理工具。

尝试：“列出我最新的五篇 SparkRing 笔记并总结决策。”验证助手请求使用 SparkRing、返回预期笔记并注明 ID。在 App 撤销密钥后，确认后续读取失败。各客户端授权界面不同；支持时请开启工具调用审批。

数据从 SparkRing 进入本地适配器，再进入 MCP 客户端及其选定的模型服务。连接前检查对方的数据保留设置。返回文字是待分析资料，不是可执行指令。超过 24,000 字符的文本字段会被截断，并带有 `truncated: true`；完整文字可通过 API 获取。

这是本地 stdio 适配器。仅支持远程 MCP URL 的客户端无法直接运行它。
