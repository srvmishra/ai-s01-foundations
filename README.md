# AI research program: Semester 1, Mathematical foundations

One repository per semester; weeks live at the top level (`week-01/`, `week-02/`, …).
When the semester is finished, it is imported into the umbrella repo `ai-research-program` with `git subtree`.

- **Program (weekly plan, progress, reviews):** https://claude.ai/artifact/R24uA75qfq5tCrgoCbxBSq

## Layout

```
ai-s01-foundations/
├── SEMESTER                 the semester number (1); the scaffolding script reads it
├── week-01/
│   ├── README.md            checklist for the week (generated)
│   ├── notes/               one file per lecture or reading
│   ├── problem-sets/        LaTeX source + PDF of solutions
│   ├── code/                small labs and exercises
│   ├── studio/              industry-studio decision memo
│   └── reflection.md
├── templates/               notes, proof set, memo, reflection, project README
├── tools/new_week.py        scaffold a week: python tools/new_week.py s01w02
├── tools/curriculum.json    the full program, exported from the page
├── pyproject.toml           Python environment (uv)
└── .gitignore               keeps data, weights and logs out of git
```

## Weekly routine (one branch per week)

```bash
git switch main && git pull
git switch -c s01w02
python tools/new_week.py s01w02
# work down week-02/README.md, committing often
git push -u origin s01w02
# open a pull request s01w02 -> main on GitHub and merge it, then:
git switch main && git pull
git tag s01w02-submitted && git push --tags
```

Then follow SUBMITTING.md.

## Starting the next semester

Copy this repo's `templates/`, `tools/`, `pyproject.toml` and `.gitignore` into a new repo (for example `ai-s02-llms`), put `2` in its `SEMESTER` file, and scaffold `s02w01`.
