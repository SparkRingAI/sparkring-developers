# 通过 API 读取自己的文字

[English](../en/api.md)

前提：SparkRing 账号、已同步的文字内容、提供 **账号 → 开发者接入** 的 App，以及已启用接口的服务。本教程由维护者编写。

## 创建密钥

按需选择 `transcripts:read`、`notes:read`、`action-items:read`。有效期为 1–90 天，默认 30 天；最多同时保留 10 个有效密钥。创建时立即保存，之后不会再次显示。可在同一页面撤销。密钥只能读取数据，不能管理密钥或修改内容。

使用 **App 页面显示的 API 基础地址**，以 `/v1/developer` 结尾。在自己的密钥管理器或进程环境中设置 `SPARKRING_API_URL` 和 `SPARKRING_API_KEY`。不要把真实值写入 Issue、聊天、源码或终端历史。

```python
import os
import httpx

with httpx.Client(timeout=30, follow_redirects=False, trust_env=False) as client:
    response = client.get(
        os.environ["SPARKRING_API_URL"].rstrip("/") + "/notes",
        headers={"Authorization": "Bearer " + os.environ["SPARKRING_API_KEY"]},
        params={"limit": 10},
    )
    response.raise_for_status()
    notes = response.json()
```

在虚拟环境安装 `httpx==0.28.1` 后运行。响应只进入当前进程；打印或发送到其他服务属于额外的数据转移。

## 接口

以下路径相对于 API 基础地址，均使用 `Authorization: Bearer <个人密钥>`。

| GET 路径 | 权限 | 内容 |
| --- | --- | --- |
| `/transcripts` 或 `/transcripts/{id}` | `transcripts:read` | ID、标题、阅读版转写、录制时间、更新时间 |
| `/notes` 或 `/notes/{id}` | `notes:read` | ID、标题、Markdown、创建时间、更新时间 |
| `/action-items` 或 `/action-items/{id}` | `action-items:read` | ID、标题、上下文、状态、计划时间、时间精度、时区、更新时间 |

列表返回 `{"items": [...], "next_before_id": "..."}`，按 ID 降序排列。`limit` 范围 1–50，默认 20；下一页将返回值作为 `before_id`。游标为 null 表示结束。ID 使用字符串，请作为不透明标识处理。分页不是增量变更订阅；需要重新读取以发现编辑或删除。已删除条目不会返回，已归档条目仍可读取。

转写优先使用润色阅读版，笔记使用保存的 Markdown。行动项包括笔记清单及待办、跟进项；状态为 `in_progress`、`done` 或 `archived`。`time_precision: date_only` 应按给定时区展示日期，不应展示为午夜截止时间。计划时间为 null 表示没有提供截止时间。

## 错误和限制

| HTTP | 含义 | 处理 |
| --- | --- | --- |
| 401 | 密钥无效、过期、撤销或账号不可用 | 检查账号，按需创建新密钥 |
| 403 | 缺少权限 | 使用包含对应读取权限的密钥 |
| 404 | 条目不存在、不属于当前用户或接口未启用 | 核对 ID 和服务状态 |
| 422 | 参数不合法 | 核对数量、ID 和类型 |
| 429 | 达到账号读取上限 | 按 `Retry-After` 等待 |
| 503 | 暂时不可用 | 稍后退避重试 |

每个账号每分钟最多读取 60 次，所有密钥共用额度。错误包含 `error_code`、`user_message`；可提供 `X-Request-ID` 帮助排查，无需发送正文或密钥。响应标记为 `no-store`。

## 验证

在自己的账号创建虚构笔记，确认接口可读取；撤销密钥后再次请求，应返回 401。选定文字只发送给已认证的调用方。接口仅提供已同步到服务端的内容，本地草稿不会出现。
