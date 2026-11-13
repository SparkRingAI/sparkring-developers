"""Export a snapshot to new files; never overwrite user notes or follow redirects."""
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit
import httpx

def export(directory):
    base = os.environ["SPARKRING_API_URL"].rstrip("/")
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path != "/v1/developer":
        raise ValueError("Use the HTTPS API base URL shown in the app")
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    before = None
    seen = set()
    count = 0
    with httpx.Client(timeout=30, follow_redirects=False, trust_env=False) as client:
        while True:
            params = {"limit": 20}
            if before: params["before_id"] = before
            response = client.get(base + "/notes", params=params,
                headers={"Authorization": "Bearer " + os.environ["SPARKRING_API_KEY"]})
            if response.status_code != 200:
                raise ValueError("Export stopped (HTTP %d); existing files are safe" % response.status_code)
            page = response.json()
            for note in page["items"]:
                identifier = str(note["id"])
                if not re.fullmatch(r"[1-9][0-9]{0,18}", identifier):
                    raise ValueError("Invalid note ID")
                destination = root / ("sparkring-note-" + identifier + ".md")
                try:
                    with destination.open("x", encoding="utf-8") as output:
                        output.write("# " + note["title"].replace("\n", " ") + "\n\n" + note["markdown"] + "\n")
                    count += 1
                except FileExistsError:
                    pass
            before = page.get("next_before_id")
            if before is None: break
            if before in seen: raise ValueError("Repeated cursor; export stopped")
            seen.add(before)
    return count

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit("Usage: python examples/export_notes.py OUTPUT_DIRECTORY")
    try:
        count = export(sys.argv[1])
    except (KeyError, ValueError, OSError, httpx.HTTPError):
        raise SystemExit("Export stopped. Check configuration, permissions, and service availability. Existing files are safe.") from None
    print("Created %d note files." % count)
