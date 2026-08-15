# Project specs — Learn Bosnian in 30 Days

## Goals

- React website: Book 1 = Lesson 0 orientation + 30 one-hour **A1 present-tense** survival lessons (tourist / early expat)
- Past-tense storytelling and heavier grammar wait for **Book 2**
- Portable JSON → website, Scribus book pack, YouTube scripts, future Expo app
- Nightly cadence: AI draft → human review → publish
- Latin script only; Bosnian-focused; kilim-inspired theme
- YouTube companions for [@HowtospeakBosnian](https://www.youtube.com/@HowtospeakBosnian)

## Pedagogy locks (Book 1)

- Present tense only (no perfekt / future paradigms)
- Spiral frames + **Say again** warm-up (4 recycled lines) every drafted lesson
- Reviews 7 / 14 / 21 / 30 are frame drills
- Grammar panels keep labels, but open with a chunks-first reminder from the phrase bank in `LESSON_AUTHORING_GUIDE.md`. Rotate wording so panels do not all sound the same. Learner prose avoids semicolons, colons inside sentences, and comma-glued phrase pairs.
- Lesson 0 states that Book 1 teaches ready phrases and present-tense chunks rather than full case tables. Deeper grammar waits for Book 2.
- Public scenes include at least one polite exchange (`molim` / `hvala` / `molim vas`)
- Studio-clean dialogue is OK. Do not add reduced street variants in Book 1.

## Lesson production plan

**Canonical mold:** Lesson 1 (`content/book1/day-01/`).  
**Authoring guide:** [`content/book1/LESSON_AUTHORING_GUIDE.md`](content/book1/LESSON_AUTHORING_GUIDE.md) — fixed section recipe, video beats, review exceptions, and batch order for Lessons 4–30.

| Batch | Lessons | Status |
|-------|---------|--------|
| Exemplar | 1 | draft (mold) |
| Aligned | 2–3 | draft (same fashion) |
| A | 4–6 | draft (same fashion) |
| B | 7 | draft (review) |
| C | 8–10 | draft (same fashion) |
| D | 11–15 | draft (weather, park, people, review, directions) |
| E | 16–20 | draft (bus, restaurant, hobbies, holidays, phone) |
| F | 21 | outlined (section 3 review) |
| G–H | 22–30 | Section 4 travel/longer stay (present only) + finale |

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
| 6 | Koliko je sati? | draft | Time + weekdays; culture widened to Travnik/Una/Neum (not Sarajevo-only) — needs human review | script ready |
| 7 | Ponavljanje | draft | Review + Jajce/Blagaj/Počitelj postcards — needs human review | script ready |
| 8 | Volim burek | draft | Full draft (food, volim/ne volim, Livno postcard) — needs human review | script ready |
| 9 | U prodavnici | draft | Full draft (shopping, želim, Tuzla market) — needs human review | script ready |
| 10 | Moja soba | draft | Full draft (home, imati, Stolac/Radimlja) — needs human review | script ready |
| 11 | Kakvo je vrijeme? | draft | Full draft (weather, Trebević/Jahorina, inversion civic) — needs human review | script ready |
| 12 | Idemo u park | draft | Full draft (invitations, Vrelo Bosne, 2014 floods civic) — needs human review | script ready |
| 13 | Ljudi iz BiH | draft | Full draft (place/language identity, Brčko, district civic) — needs human review | script ready |
| 14 | Ponavljanje | draft | Review of Lessons 8 to 13 plus Banja Luka postcards — needs human review | script ready |
| 15 | Desna ili lijeva? | draft | Full draft (directions, Latin Bridge/Konjic, landmine civic) — needs human review | script ready |
| 16 | Na autobus | draft | Civic locked to Corridor Vc only | script ready |
| 17 | Dobar tek! | draft | Civic locked to neighbor dual citizenship only | script ready |
| 18 | Sport i hobiji | draft | Civic locked to cantonal universities and private colleges | script ready |
| 19 | Praznici | draft | Civic locked to Gulf-funded mosque reconstruction | script ready |
| 20 | Telefonski poziv | draft | Civic locked to Southern Interconnection gas deal | script ready |
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
- [x] Pedagogy upgrades: Čuj Bosnu authenticListen, quiz remediation links, speak-check (Transcribe+Nova), review deck, can-do checks, listen-first vocab
- [x] Recorder trim + accept-before-upload (Female 1 = vocab, Male 1 = male parts, F2/M2 if needed)
- [x] Lessons 8–10 full drafts (food, shop, home)
- [x] Lessons 11–15 full drafts (weather, park, people, review, directions)

## Voice recording

- Private studio: `recorder/` (iPhone Safari MediaRecorder → trim start/end → playback → accept → S3)
- Exclusive queues: Female 1 = vocab + Ana + narrator; Male 1 = Emir; Female 2 = Amira; Male 2 = shopkeeper + Mrvica
- Playback: click vocab / dialogue in `LessonShell`
- Ops doc: [`docs/VOICE-RECORDING.md`](docs/VOICE-RECORDING.md)
- Shared password: `GornjiVakuf` — apply Terraform, share recorder URL with voice talents
