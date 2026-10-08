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

## What Claude can and cannot open

- **Public GitHub links:** yes. Point at the files that matter (the week README links them).
- **Private repositories:** no. If a course asks you not to publish solutions, keep that repo private and upload a zip or PDF in the chat instead.
- **Large files:** keep them out of git; summarize results in the README with numbers and plots.
