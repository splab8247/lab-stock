"""git log of data/*.csv -> history.json: recent site edits, split into freezer stock and mouse, deployed with the page."""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = 50  # per kind, so a burst of mouse edits never pushes stock edits out (and vice versa)
# site commits look like "cell_stock1 G-1 삭제 (홍길동)"; developer commits have no trailing (name)
SITE_EDIT = re.compile(r"^(?P<what>.+?)\s*\((?P<who>[^()]+)\)\s*$")
MOUSE_FILE = "data/mice.csv"
DEV_COMMIT = "Co-Authored-By: Claude"  # code/data maintenance commits, not edits made on the site


def main():
    # one block per commit: "\x1e<sha>\x1f<date>\x1f<subject>\x1f<body>\x1d" followed by the changed file names
    log = subprocess.run(
        ["git", "log", "-n", "2000", "--name-only", "--format=%x1e%H%x1f%cI%x1f%s%x1f%b%x1d", "--", "data/"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    out = {"stock": [], "mouse": []}
    for block in log.split("\x1e")[1:]:
        meta, _, tail = block.partition("\x1d")
        sha, date, subject, body = meta.strip("\n").split("\x1f", 3)
        m = SITE_EDIT.match(subject)
        if not m or DEV_COMMIT in body:  # developer commits can also end in "(...)"
            continue
        files = [f.strip() for f in tail.split("\n") if f.strip()]
        item = {"sha": sha, "date": date, "what": m["what"], "who": m["who"]}
        kinds = set()
        if MOUSE_FILE in files:
            kinds.add("mouse")
        if any(f != MOUSE_FILE for f in files):
            kinds.add("stock")
        for k in kinds:
            if len(out[k]) < LIMIT:
                out[k].append(item)
        if all(len(v) >= LIMIT for v in out.values()):
            break
    (ROOT / "history.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"history.json: stock {len(out['stock'])}, mouse {len(out['mouse'])}")


if __name__ == "__main__":
    main()
