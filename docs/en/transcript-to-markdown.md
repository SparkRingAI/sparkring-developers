# Transcript → Markdown / Obsidian

[简体中文](../zh-CN/transcript-to-markdown.md) · [All docs](../README.md)

Status: manual recipe. Maintainer-authored. No API, automation, account linking, or plugin is required.

## Prerequisites and data destination

Use any text editor, or an existing Obsidian vault if you already use Obsidian. Start with the [fictional transcript](../../examples/fictional-transcript.txt). To use your own content later, your app version must offer **Copy transcript** for a recording with a completed transcript.

Data path: **SparkRing → system clipboard → the note or vault you select**. The fictional-sample path starts with this repository instead. The clipboard, editor, and vault are separate storage locations. A cloud-synced vault, clipboard history, or cross-device clipboard can create additional copies; review those settings before using personal content.

## Steps

1. Open the sample and copy its three speaker lines. With your own recording, open its detail page, choose **… → Copy transcript**, then inspect the pasted text before sharing it further. The copied text may be the displayed, refined transcript; it is not a guarantee of a verbatim original.
2. In a text editor create `garden-meetup.md`, or create a new note in your chosen Obsidian vault.
3. Add the title `# Garden meetup` and the heading `## Transcript`, then paste the three lines below it. Keep the speaker labels.
4. Add `## Action items`. Manually record only tasks supported by the text: Speaker 1 drafts the invitation; Speaker 2 checks the seed list. Leave dates unspecified, because none are stated.
5. Save and reopen the note. Compare it with the [example result](../../examples/fictional-note.md). If using Obsidian, open its reading view to check the headings and checklist.

## Verify and recover

- All three speaker lines should match the sample, including speaker attribution.
- There should be two unchecked tasks, with no invented date or participant name.
- A local editor should be sufficient for the sample; no request to SparkRing or another service is needed by these steps.
- If **Copy transcript** is missing or disabled, check that a transcript is visible and check your app version. Continue with the sample rather than extracting app credentials or calling undocumented endpoints.
- If formatting is lost, paste as plain text. If your destination syncs automatically, remove unintended copies using that service's controls.

Deleting the source recording does not delete the note, clipboard history, synced copies, or backups. Manage those copies separately. Share only fictional examples in public contributions.
