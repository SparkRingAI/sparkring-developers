#!/usr/bin/env python3
"""Offline publication hygiene checks; no credentials, network, or writes.

Review changes to this script before running it on an untrusted contribution.
Findings contain locations and rule names, never matched content.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SELF = "scripts/check_docs.py"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}
SPECIAL_FILES = {"LICENSE", ".gitignore", ".github/CODEOWNERS"}
REQUIRED = {
    "README.md", "README.zh-CN.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "SECURITY.md", "AGENTS.md", "LICENSE", "docs/README.md",
    ".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/ISSUE_TEMPLATE/01-docs.yml",
    ".github/ISSUE_TEMPLATE/02-workflow.yml", ".github/ISSUE_TEMPLATE/03-interface.yml",
    "examples/fictional-transcript.txt", "examples/fictional-note.md",
    "recipes/TEMPLATE.md", "maintainers/README.md",
    "maintainers/repository-settings.json", "maintainers/branch-rules.json", SELF,
}
PAIRED_PAGES = (
    "transcript-to-markdown.md", "transcript-to-ai.md",
    "api.md", "mcp.md", "api-to-obsidian.md", "data-and-privacy.md",
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
OWN_ORG_URL = re.compile(
    r"https?://(?:github\.com|raw\.githubusercontent\.com)/SparkRingAI/([^\s/#)]+)",
    re.IGNORECASE,
)
INDICATORS = {
    "sparkring-personal-key": re.compile(r"\bsrk_[A-Za-z0-9_-]{43}\b"),
    "private-key-block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "signed-or-session-url": re.compile(r"https?://[^\s]+[?&](?:X-Goog-Signature|X-Amz-Signature|upload_id)=", re.I),
    "local-absolute-path": re.compile(r"/(?:Users|home)/[\w.-]+/"),
    "private-network-url": re.compile(r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)(?=[:/\s]|$)", re.I),
    "cloud-object-path": re.compile(r"\bgs://[A-Za-z0-9]"),
}
findings: set[tuple[str, str]] = set()


def fail(location: str, rule: str) -> None:
    findings.add((location, rule))


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise RuntimeError("Git inspection failed; details withheld to avoid disclosure")
    return result.stdout


def validate_path(name: str) -> None:
    path = Path(name)
    parts = path.parts
    if path.is_absolute() or ".." in parts:
        fail(name, "path-outside-repository")
    if name.startswith(".github/workflows/"):
        fail(name, "workflow-not-allowed")
    if name not in SPECIAL_FILES and path.suffix not in TEXT_SUFFIXES:
        fail(name, "non-text-or-unapproved-file-type")
    lowered = name.lower()
    if path.name.startswith(".env") or any(
        marker in lowered for marker in (
            "scan-report", "gitleaks-report", "private-patterns", "release_review",
            "release-review", "review-evidence", "service-account", "credentials.json",
        )
    ):
        fail(name, "private-artifact-not-allowed")


def validate_content(location: str, content: bytes, private_patterns: list[str]) -> str | None:
    if b"\0" in content:
        fail(location, "binary-content")
        return None
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        fail(location, "non-utf8-content")
        return None
    for line_no, line in enumerate(text.splitlines(), 1):
        loc = f"{location}:{line_no}"
        for rule, indicator in INDICATORS.items():
            if indicator.search(line):
                fail(loc, rule)
        for match in OWN_ORG_URL.finditer(line):
            if match.group(1).lower().removesuffix(".git") != "sparkring-developers":
                fail(loc, "other-organization-repository-link")
        if any(pattern.casefold() in line.casefold() for pattern in private_patterns):
            fail(loc, "private-identifier")
    return text


def heading_ids(text: str) -> set[str]:
    result: set[str] = set()
    counts: dict[str, int] = {}
    fenced = False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
        if fenced:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            slug = re.sub(r"[^\w\-\s]", "", match.group(1).lower()).replace(" ", "-")
            occurrence = counts.get(slug, 0)
            counts[slug] = occurrence + 1
            result.add(f"{slug}-{occurrence}" if occurrence else slug)
    return result


def validate_links(name: str, text: str, files: dict[str, str]) -> int:
    checked = 0
    # Ignore code fences; example syntax is not a link contract.
    text_without_code = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)
    for match in MARKDOWN_LINK.finditer(text_without_code):
        target = match.group(1).strip()
        if target.startswith("<") and ">" in target:
            target = target[1:target.index(">")]
        else:
            target = target.split(' "', 1)[0]
        parsed = urlsplit(target)
        if parsed.scheme:
            if parsed.scheme != "https":
                fail(name, "non-https-external-link")
            continue
        if parsed.netloc or parsed.path.startswith("/"):
            fail(name, "absolute-link")
            continue
        resolved = (ROOT / name).parent.joinpath(unquote(parsed.path)).resolve() if parsed.path else ROOT / name
        if not resolved.is_relative_to(ROOT):
            fail(name, "link-outside-repository")
            continue
        relative = resolved.relative_to(ROOT).as_posix()
        if relative not in files:
            fail(name, "missing-local-link-target")
        elif parsed.fragment and unquote(parsed.fragment) not in heading_ids(files[relative]):
            fail(name, "missing-heading-fragment")
        checked += 1
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-patterns", type=Path, help="External file of non-secret literal identifiers")
    args = parser.parse_args()
    private_patterns: list[str] = []
    if args.private_patterns:
        pattern_file = args.private_patterns.resolve()
        if pattern_file.is_relative_to(ROOT):
            parser.error("The private pattern file must be outside this repository")
        private_patterns = [line.strip() for line in pattern_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not private_patterns:
            parser.error("The private pattern list must not be empty")

    names = sorted(set(git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0")) - {""})
    files: dict[str, str] = {}
    for name in names:
        validate_path(name)
        path = ROOT / name
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            fail(name, "symlink-or-outside-path")
            continue
        if not path.is_file():
            fail(name, "missing-file-or-submodule")
            continue
        value = validate_content(name, path.read_bytes(), private_patterns)
        if value is not None:
            files[name] = value
            if path.suffix == ".json":
                try:
                    json.loads(value)
                except json.JSONDecodeError:
                    fail(name, "invalid-json")

    required = REQUIRED | {f"docs/{language}/{page}" for language in ("en", "zh-CN") for page in PAIRED_PAGES}
    for name in required - files.keys():
        fail(name, "missing-required-page")
    links = sum(validate_links(name, text, files) for name, text in files.items() if name.endswith(".md"))
    for page in PAIRED_PAGES:
        for language, other in (("en", "zh-CN"), ("zh-CN", "en")):
            name = f"docs/{language}/{page}"
            if f"../{other}/{page}" not in files.get(name, ""):
                fail(name, "missing-paired-translation-link")

    # Inspect paths in every reachable tree as well as deleted/changed blobs.
    commits = git("rev-list", "--all").decode().splitlines()
    for commit in commits:
        for item in git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
            if not item:
                continue
            metadata, raw_path = item.split(b"\t", 1)
            name = raw_path.decode("utf-8")
            validate_path(name)
            if metadata.split()[0] not in (b"100644", b"100755"):
                fail(f"history:{commit[:12]}:{name}", "historical-symlink-or-submodule")

    blobs = 0
    for item in git("rev-list", "--objects", "--all").decode().splitlines():
        oid = item.split(" ", 1)[0]
        if git("cat-file", "-t", oid).strip() == b"blob":
            validate_content(f"history:{oid[:12]}", git("cat-file", "blob", oid), private_patterns)
            blobs += 1

    if findings:
        for location, rule in sorted(findings):
            print(f"FAIL {location}: {rule}", file=sys.stderr)
        print(f"FAILED: {len(findings)} finding(s); matched content withheld", file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} text files, {links} local links, {len(commits)} commits, {blobs} history blobs")
    print("External links, translation meaning, confidentiality, app builds, and remote permissions require separate review.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, UnicodeError, ValueError):
        print("FAIL: inspection could not complete; no content or credentials printed", file=sys.stderr)
        raise SystemExit(1)
