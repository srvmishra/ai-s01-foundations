# Submitting a week for review

## 1. Freeze a snapshot

```bash
# merge the week's pull request on GitHub first, then:
git switch main && git pull
git tag s01w01-submitted
git push --tags
```

The tag means the review looks at exactly what you submitted, even if you keep working.
Link to the tagged folder, for example:
`https://github.com/<you>/ai-s01-foundations/tree/s01w01-submitted/week-01`

## 2. Fill in the week on the program page

- **Notes link:** the tagged week folder above.
- **Repo links:** one per line, for any separate project repos (link the tag or a specific commit).
- **Reflection:** a few honest lines (the full version is in `reflection.md`).

Press **Submit week**.

## 3. Ask for the review in chat

Say "review S1 W1". Claude reads your saved submission, opens the public links, quizzes you, and writes the review back onto the page.

## Testing out of material you already know

Lectures, readings, assignments and quizzes from courses can be tested out; projects, program items
(proof sets, code labs, exams, capstones) and industry studios cannot.

1. Try the three hardest problems first, in about 45 minutes and without notes. For a coding exercise, write its hardest part and get it passing.
2. If the attempt is clean, save it in the week's `problem-sets/` (or `code/`), for example `problem-sets/mml-ch2-3-testout.pdf`.
3. Write a one-page formula cheat sheet in the item's notes file (the "Formula cheat sheet" section).
4. On the program page press **Test out** on the item, tick it in the week README with *(tested out)*, and list it under "Tested out" in `reflection.md`.

The weekly oral includes two or three questions on tested-out items. If one goes badly, the item goes back to not started.

## Submitting an industry studio (own pace)

Studios are never part of the weekly submission, and their progress is tracked separately. Do them on
leave days, long weekends or holidays, each on a short branch of its own:

```bash
git switch main && git pull
git switch -c s01-studio1
# If the studio's first week has no folder yet, scaffold it: python tools/new_week.py s01w01
# Memo: week-01/studio/studio-1-memo.md; prototype code in the same studio/ folder
# (or its own repo if it is large)
git push -u origin s01-studio1
# open the pull request, merge it, then:
git switch main && git pull
git tag s01-studio1-submitted && git push --tags
```

On the program page, open the studio's card under **Industry studios**, paste the memo link from the tag
(for example `https://github.com/<you>/ai-s01-foundations/blob/s01-studio1-submitted/week-01/studio/studio-1-memo.md`), add any repo links, press **Submit studio**, then say "review studio S1-1" in chat.
The review appears on the studio's card and never affects the weekly reviews.

## What Claude can and cannot open

- **Public GitHub links:** yes. Point at the files that matter (the week README links them).
- **Private repositories:** no. If a course asks you not to publish solutions, keep that repo private and upload a zip or PDF in the chat instead.
- **Large files:** keep them out of git; summarize results in the README with numbers and plots.
