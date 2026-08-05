# Nightly chapter SOP

One chapter per night. Same rhythm as the SAA “Night N” study plan.

## Flow

1. **Draft (AI)** — Write `content/book1/day-NN/chapter.json` from [outline.json](../content/book1/outline.json) and [CONTENT-STYLE.md](../CONTENT-STYLE.md). Add `video-script.md` and cited images. Set `status: "draft"`.
2. **Human review** — Use the checklist below. Either approve or request fixes.
3. **Publish** — Set `status: "published"`, update [project_specs.md](../project_specs.md), commit, deploy. Site shows the day as open.
4. **YouTube (optional same night)** — Run `node scripts/export-youtube.cjs --day N`, assemble in CapCut, upload to playlist *Learn Bosnian in 30 Days — Book 1*.

## Human review checklist

- [ ] Latin script only; Bosnian (BiH) wording; no Croatian/Serbian teaching asides
- [ ] Learning goals match vocabulary + grammar actually taught
- [ ] Conversation advances Ana / Emir / Amira / Mrvica story
- [ ] Puzzles and section quiz are fair; options similar length
- [ ] Culture notes accurate and respectful
- [ ] Images have licenses + credits (or `imagesNeeded` + briefs filled)
- [ ] Dictionary entries cover every new word
- [ ] `video-script.md` present for post-approve export

## Status values

| Status | Meaning |
|--------|---------|
| `outlined` | Title + theme only |
| `draft` | Full chapter written, not reviewed |
| `in_review` | Waiting on human |
| `published` | Live on site |

## Tracking

Update the night table in `project_specs.md` after each status change.
