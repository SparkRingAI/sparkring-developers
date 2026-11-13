# API → Markdown / Obsidian

[English](../en/api-to-obsidian.md)

维护者教程。前提：[API 接入](api.md)、`notes:read` 权限、Python 3.11+、你控制的本地目录。安装 `httpx==0.28.1`，按快速开始配置环境变量。

运行 `python examples/export_notes.py OUTPUT_DIRECTORY`，将所有可读取的笔记导出为 `sparkring-note-ID.md`。文件名使用 ID，不使用不可信的标题。现有文件不会覆盖；刷新快照时请导出到新的空目录。随后可将目录复制到 Obsidian 库。

数据进入你指定的本地目录；同步服务或插件可能继续上传，请检查设置。Markdown 可能含外链或图片，先用纯文本编辑器检查，不要执行其中的命令。

使用虚构笔记验证：核对标题和正文，再次运行确认现有文件不变。这是快照导出，不会同步删除。完成后可以撤销密钥，已导出的副本需要你自行删除。
