#!/usr/bin/env python3
"""Scaffold a week folder from the curriculum.

Usage:
    python tools/new_week.py s01w01        # Semester 1, week 1

In a semester repo (a SEMESTER file at the root holds its number), weeks are
created at the top level as week-YY/, and only that semester's weeks are allowed.
Without a SEMESTER file, weeks go to semester-XX/week-YY/.

Each week folder gets:
    README.md        checklist of every item, with links and hours
    notes/           one notes file per lecture or reading
    problem-sets/    put LaTeX/PDF solutions here
    code/            small labs and exercises (bigger projects get their own repo)
    studio/          industry-studio memo, if the week has one
    reflection.md    filled in before you submit
Existing files are never overwritten.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "curriculum.json").read_text(encoding="utf-8"))
TEMPLATES = ROOT / "templates"


def slug(text: str, n: int = 80) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:n].rstrip("-") or "item"


def write_once(path: Path, content: str) -> None:
    if path.exists():
        print(f"  keep  {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  new   {path.relative_to(ROOT)}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    week_id = sys.argv[1].lower()
    week = next((w for w in DATA["weeks"] if w["id"] == week_id), None)
    if week is None:
        sys.exit(f"Unknown week {week_id!r}. Use the form s01w01.")

    sem_file = ROOT / "SEMESTER"
    if sem_file.exists():
        sem = int(sem_file.read_text().strip())
        if week["semester"] != sem:
            sys.exit(f"This repo is for Semester {sem}; {week_id} belongs to Semester {week['semester']}.")
        folder = ROOT / f"week-{week['week']:02d}"
    else:
        folder = ROOT / f"semester-{week['semester']:02d}" / f"week-{week['week']:02d}"
    label = f"S{week['semester']} W{week['week']}"
    required = [i for i in week["items"] if not i["optional"]]
    optional = [i for i in week["items"] if i["optional"]]

    lines = [
        f"# {label}: {week['title']}",
        "",
        f"**Goal:** {week['goal']}  ",
        f"**Planned hours:** {week['hours']}  ",
        f"**Program page:** {DATA['program']}",
        "",
        "## Checklist",
        "",
    ]
    for it in required:
        link = f" ([link]({it['url']}))" if it["url"] else ""
        lines.append(f"- [ ] **{it['type']}** · {it['course']}: {it['task']} · {it['hours']} h{link}")
    if optional:
        lines += ["", "### Optional (GPU tiers; not counted)", ""]
        for it in optional:
            lines.append(f"- [ ] {it['task']}")
    lines += [
        "",
        "## Deliverables",
        "",
        "| Item | Where it lives |",
        "| --- | --- |",
        "| Lecture and reading notes | [notes/](notes/) |",
        "| Problem-set solutions | [problem-sets/](problem-sets/) |",
        "| Code for labs and exercises | [code/](code/) or a linked repo |",
        "| Industry studio memo | [studio/](studio/) |",
        "| Reflection | [reflection.md](reflection.md) |",
        "",
    ]
    write_once(folder / "README.md", "\n".join(lines))

    note_tpl = (TEMPLATES / "lecture-notes.md").read_text(encoding="utf-8")
    for it in week["items"]:
        if it["type"] in ("Lecture", "Reading"):
            name = slug(f"{it['course'].split('(')[0]} {it['task']}") + ".md"
            body = note_tpl.format(title=it["task"], course=it["course"], url=it["url"] or "-")
            write_once(folder / "notes" / name, body)

    for sub in ("problem-sets", "code"):
        write_once(folder / sub / ".gitkeep", "")

    studio = [i for i in required if i["type"] == "Industry studio"]
    if studio:
        m = re.match(r"Studio (\d+): ([^.]+)\.", studio[0]["task"])
        n, title = (m.group(1), m.group(2)) if m else ("?", "studio")
        memo = (TEMPLATES / "decision-memo.md").read_text(encoding="utf-8")
        write_once(folder / "studio" / f"studio-{n}-memo.md", memo.format(n=n, title=title, week_id=label))

    refl = (TEMPLATES / "reflection.md").read_text(encoding="utf-8")
    write_once(folder / "reflection.md", refl.format(week_id=label))
    print(f"\nDone. Open {folder.relative_to(ROOT)}/README.md and work down the checklist.")


if __name__ == "__main__":
    main()
