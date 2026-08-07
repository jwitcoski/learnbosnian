# Project specs — Learn Bosnian in 30 Days

## Goals

- React website: Book 1 = Lesson 0 orientation + 30 one-hour lessons (A1 → early A2)
- Portable JSON → website, Scribus book pack, YouTube scripts, future Expo app
- Nightly cadence: AI draft → human review → publish
- Latin script only; Bosnian-focused; kilim-inspired theme
- YouTube companions for [@HowtospeakBosnian](https://www.youtube.com/@HowtospeakBosnian)

## Lesson production plan

**Canonical mold:** Lesson 1 (`content/book1/day-01/`).  
**Authoring guide:** [`content/book1/LESSON_AUTHORING_GUIDE.md`](content/book1/LESSON_AUTHORING_GUIDE.md) — fixed section recipe, video beats, review exceptions, and batch order for Lessons 4–30.

| Batch | Lessons | Status |
|-------|---------|--------|
| Exemplar | 1 | draft (mold) |
| Aligned | 2–3 | draft (same fashion) |
| A | 4–5 | draft (same fashion); 6 still outlined |
| B | 6–7 | Lesson 6 next, then Week 1 review |
| C–D | 8–14 | Week 2 + review |
| E–F | 15–21 | Week 3 + review |
| G–H | 22–30 | Week 4 + finale |

## Characters

Ana (learner), Emir (guide), Amira (café), Mrvica (cat)

## Night tracker — Book 1

| Lesson | Title | Status | Reviewer notes | YouTube |
|-----|-------|--------|----------------|---------|
| 0 | Zašto bosanski? | published | Orientation live — why Bosnian, etymology, vs HR/SR, speakers, audience | |
| 1 | Zdravo, Sarajevo! | draft | Exemplar — needs human review before publish | |
| 2 | Ja sam Ana | draft | Full draft (biti, introductions, Sebilj) — needs human review | script ready |
| 3 | Brojevi i kahva | draft | Full draft (1–20, kahva order, Amira’s) — needs human review | script ready |
| 4 | Porodica Mrvice | draft | Full draft (family, moj/moja, café family) — needs human review | script ready |
| 5 | Gdje je Mostar? | draft | Full draft (gdje/ovdje/tamo, u/na/kod, Mostar tease) — needs human review | script ready |
| 6 | Koliko je sati? | outlined | | |
| 7 | Sedmica 1 — ponavljanje | outlined | | |
| 8 | Volim burek | outlined | | |
| 9 | U prodavnici | outlined | | |
| 10 | Moja soba | outlined | | |
| 11 | Kakvo je vrijeme? | outlined | | |
| 12 | Idemo u park | outlined | | |
| 13 | Ljudi iz BiH | outlined | | |
| 14 | Sedmica 2 — ponavljanje | outlined | | |
| 15 | Desna ili lijeva? | outlined | | |
| 16 | Na autobus | outlined | | |
| 17 | Dobar tek! | outlined | | |
| 18 | Sport i hobiji | outlined | | |
| 19 | Praznici | outlined | | |
| 20 | Telefonski poziv | outlined | | |
| 21 | Sedmica 3 — ponavljanje | outlined | | |
| 22 | Jučer u Travniku | outlined | | |
| 23 | Šta si radio/radila? | outlined | | |
| 24 | Planine i rijeke | outlined | | |
| 25 | Kod doktora | outlined | | |
| 26 | Stanovanje | outlined | | |
| 27 | Posao i škola | outlined | | |
| 28 | Mostar napokon! | outlined | | |
| 29 | Pisma iz BiH | outlined | | |
| 30 | Završna proslava | outlined | | |

## Books 2–3

Teaser outlines only — see `content/book2/outline.json` and `content/book3/outline.json`.

## Completed platform work

- [x] Chapter schema + outline
- [x] Lesson UI + kilim theme
- [x] Lesson 1 exemplar (draft)
- [x] Dictionary + progress
- [x] Scribus / YouTube export scripts
- [x] App roadmap + landing CTAs
- [x] Lesson 0 orientation (why Bosnian / etymology / audience)
- [x] Lesson authoring guide (Lesson 1 mold for 4–30)
- [x] Voice recording portal (shared password, 4 voices 2F/2M) + S3/CloudFront audio + lesson tap-to-play
- [x] Recorder trim + accept-before-upload (Female 1 = vocab, Male 1 = male parts, F2/M2 if needed)

## Voice recording

- Private studio: `recorder/` (iPhone Safari MediaRecorder → trim start/end → playback → accept → S3)
- Exclusive queues: Female 1 = vocab + Ana + narrator; Male 1 = Emir; Female 2 = Amira; Male 2 = shopkeeper + Mrvica
- Playback: click vocab / dialogue in `LessonShell`
- Ops doc: [`docs/VOICE-RECORDING.md`](docs/VOICE-RECORDING.md)
- Shared password: `GornjiVakuf` — apply Terraform, share recorder URL with voice talents
