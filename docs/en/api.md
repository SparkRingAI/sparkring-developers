# Read your text with the API

[简体中文](../zh-CN/api.md)

Prerequisites: a SparkRing account, synced text, an app with **Account → Developer access**, and an enabled service. This guide is maintainer-authored.

## Create a key

Choose only the scopes your tool needs: `transcripts:read`, `notes:read`, `action-items:read`. Keys expire after 1–90 days (30 by default). At most 10 active keys are allowed. Save the value when created; it cannot be displayed again. You can revoke a key from the same screen. A key cannot manage keys or edit your content.

Use the **API base URL shown in the app**, ending in `/v1/developer`. Set `SPARKRING_API_URL` and `SPARKRING_API_KEY` in your local secret manager or process environment. Do not paste real values into Issues, chat, source files, or shell history.

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

Install `httpx==0.28.1` in a virtual environment to run the example. The response stays in your process; printing it or sending it to another service is a separate transfer.

## Endpoints

Paths below are relative to your API base URL. All accept `Authorization: Bearer <personal key>`.

| GET path | Scope | Content |
| --- | --- | --- |
| `/transcripts` or `/transcripts/{id}` | `transcripts:read` | ID, title, reading text, capture time, update time |
| `/notes` or `/notes/{id}` | `notes:read` | ID, title, Markdown, creation time, update time |
| `/action-items` or `/action-items/{id}` | `action-items:read` | ID, title, context, status, scheduled time, time precision, timezone, update time |

Lists return `{"items": [...], "next_before_id": "..."}`. They sort by descending ID, accept `limit` (1–50, default 20), and accept the returned `before_id` for the next page. A null cursor means the end. IDs are strings: treat them as opaque identifiers. Pagination is not a change feed; re-read items to see edits and removals. Deleted items are excluded; archived items remain available.

Transcript text uses the polished reading copy when available. Notes contain the saved Markdown. Action items include note checklist entries and to-dos/follow-ups; status is `in_progress`, `done`, or `archived`. For `time_precision: date_only`, display a date in the supplied timezone, not a midnight deadline. A null scheduled time means no deadline was provided.

## Errors and limits

| HTTP | Meaning | Next step |
| --- | --- | --- |
| 401 | Invalid, expired, revoked key or unavailable account | Check your account and create a replacement key if needed |
| 403 | Required scope missing | Use a key with the relevant read scope |
| 404 | Item absent/not owned, or access not enabled | Check the ID or service availability |
| 422 | Invalid parameters | Check limits, IDs, and request types |
| 429 | Account read limit reached | Respect `Retry-After` |
| 503 | Temporarily unavailable | Retry later with backoff |

Read limits are 60 requests per account per minute, shared across keys. Errors include `error_code` and `user_message`; `X-Request-ID` can help support investigate without sharing content or keys. Responses are marked `no-store`.

## Verify

Create a fictional note in your own account. Confirm it appears, then revoke the key and confirm that another request returns 401. The API sends selected text only to the authenticated caller. Only synced server-side content is available; a local-only draft will not appear.
