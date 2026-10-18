"""git log of data/*.csv -> history.json (recent edits made from the site), deployed with the page."""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = 50
# site commits look like "cell_stock1 G-1 삭제 (홍길동)"; developer commits have no trailing (name)
SITE_EDIT = re.compile(r"^(?P<what>.+?)\s*\((?P<who>[^()]+)\)\s*$")


def main():
    log = subprocess.run(
        ["git", "log", "-n", "500", "--format=%H%x1f%cI%x1f%s", "--", "data/"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    items = []
    for line in log.splitlines():
        sha, date, subject = line.split("\x1f", 2)
        m = SITE_EDIT.match(subject)
        if not m:
            continue
        items.append({"sha": sha, "date": date, "what": m["what"], "who": m["who"]})
        if len(items) >= LIMIT:
            break
    (ROOT / "history.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    print(f"history.json: {len(items)} edits")


if __name__ == "__main__":
    main()
