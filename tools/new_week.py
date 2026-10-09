#!/usr/bin/env python3
"""Scaffold a week folder from the curriculum.

Usage:
    python tools/new_week.py s01w01        # Semester 1, week 1

In a semester repo (a SEMESTER file at the root holds its number), weeks are
created at the top level as week-YY/, and only that semester's weeks are allowed.
Without a SEMESTER file, weeks go to semester-XX/week-YY/.

Each week folder gets:
    README.md        checklist of the week's research items, with links and hours,
                     plus the industry studio listed there (own pace, not part of the week)
    notes/           one notes file per lecture or reading
    problem-sets/    put LaTeX/PDF solutions (and test-out attempts) here
    code/            small labs and exercises (bigger projects get their own repo)
    studio/          industry-studio memo, in the first week of each studio
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


def is_studio(item: dict) -> bool:
    return item.get("track") == "industry" or item["type"] == "Industry studio"


def studio_info(week: dict, studio_items: list) -> dict | None:
    """Studio number, title and first week; read from the curriculum, with a fallback for older exports."""
    if week.get("studio"):
        return week["studio"]
    if not studio_items:
        return None
    m = re.match(r"Studio (\d+): ([^.]+)\.", studio_items[0]["task"])
    n = int(m.group(1)) if m else 0
    first = week["week"] if week["week"] % 2 == 1 else week["week"] - 1
    return {"number": n, "title": m.group(2) if m and first == week["week"] else f"Studio {n}", "first_week": first,
            "review_as": f"studio S{week['semester']}-{n}"}


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
    required = [i for i in week["items"] if not i["optional"] and not is_studio(i)]
    optional = [i for i in week["items"] if i["optional"] and not is_studio(i)]
    studio_items = [i for i in week["items"] if is_studio(i)]
    studio = studio_info(week, studio_items)
    research_hours = week["hours"] if "studio_hours" in week or not studio_items else round(
        sum(i["hours"] for i in required), 1)

    lines = [
        f"# {label}: {week['title']}",
        "",
        f"**Goal:** {week['goal']}  ",
        f"**Planned hours:** {research_hours} (research program; the studio below is extra, at your own pace)  "
        if studio_items else f"**Planned hours:** {research_hours}  ",
        f"**Program page:** {DATA['program']}",
        "",
        "## Checklist",
        "",
        "Tick each item when it is done. If you test out of an item (lectures, readings, assignments and quizzes",
        "from courses), tick it, add *(tested out)* to the line, keep the attempt in `problem-sets/` or `code/`,",
        "and write the cheat sheet in the item's notes file.",
        "",
    ]
    for it in required:
        link = f" ([link]({it['url']}))" if it["url"] else ""
        lines.append(f"- [ ] **{it['type']}** · {it['course']}: {it['task']} · {it['hours']} h{link}")
    if optional:
        lines += ["", "### Optional (not counted)", ""]
        for it in optional:
            lines.append(f"- [ ] {it['task']}")

    memo_rel = None
    if studio:
        n, first = studio["number"], studio["first_week"]
        memo_rel = (f"studio/studio-{n}-memo.md" if first == week["week"]
                    else f"../week-{first:02d}/studio/studio-{n}-memo.md")
        lines += [
            "",
            f"## Industry studio {n}: {studio['title']} (own pace; not part of this week)",
            "",
            "Do it whenever you have time; it is never part of the weekly submission. When the memo is done,",
            f"submit it from the studio's card under Industry studios on the program page and ask for “review {studio['review_as']}”.",
            f"Memo: [{memo_rel}]({memo_rel})",
            "",
        ]
        for it in studio_items:
            if it["optional"]:
                lines.append(f"- [ ] {it['task']} (not counted)")
            else:
                lines.append(f"- [ ] {it['task']} · {it['hours']} h")

    lines += [
        "",
        "## Deliverables",
        "",
        "| Item | Where it lives |",
        "| --- | --- |",
        "| Lecture and reading notes (and cheat sheets for tested-out items) | [notes/](notes/) |",
        "| Problem-set solutions and test-out attempts | [problem-sets/](problem-sets/) |",
        "| Code for labs and exercises | [code/](code/) or a linked repo |",
    ]
    if memo_rel:
        folder_rel = memo_rel.rsplit("/", 1)[0] + "/"
        lines.append(f"| Industry studio memo and prototype (own pace, submitted separately) | [{folder_rel}]({folder_rel}) |")
    lines += ["| Reflection | [reflection.md](reflection.md) |", ""]
    write_once(folder / "README.md", "\n".join(lines))

    note_tpl = (TEMPLATES / "lecture-notes.md").read_text(encoding="utf-8")
    for it in week["items"]:
        if it["type"] in ("Lecture", "Reading"):
            name = slug(f"{it['course'].split('(')[0]} {it['task']}") + ".md"
            body = note_tpl.format(title=it["task"], course=it["course"], url=it["url"] or "-")
            write_once(folder / "notes" / name, body)

    for sub in ("problem-sets", "code"):
        write_once(folder / sub / ".gitkeep", "")

    if studio and studio["first_week"] == week["week"]:
        memo = (TEMPLATES / "decision-memo.md").read_text(encoding="utf-8")
        write_once(folder / "studio" / f"studio-{studio['number']}-memo.md",
                   memo.format(n=studio["number"], title=studio["title"], week_id=label))

    refl = (TEMPLATES / "reflection.md").read_text(encoding="utf-8")
    write_once(folder / "reflection.md", refl.format(week_id=label))
    print(f"\nDone. Open {folder.relative_to(ROOT)}/README.md and work down the checklist.")


if __name__ == "__main__":
    main()
