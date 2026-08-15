# Book 1 lesson authoring guide

**Exemplar:** Lesson 1 — `content/book1/day-01/chapter.json` (+ `video-script.md`)  
**Also aligned:** Lessons 2–3 and 4–10 (same shape)  
**Exception:** Lesson 0 (orientation) and review lessons (7, 14, 21, 30) — see §5

Use this guide for **Lessons 4–30**. Do not invent a new chapter shape. Copy Lesson 1’s structure; swap language focus and story beat from `outline.json`.

---


### Copy rules (non-negotiable)

- Titles say **Lesson N** only. Never Day N, Week N, or Sedmica N in titles.
- Review lessons are titled **Ponavljanje** / **Review**, not “Week 1 review”.
- Never use em dashes (`—`) or en dashes (`–`) as punctuation in chapter JSON or video scripts.
- Never use semicolons (`;`) or colons (`:`) inside learner-facing sentences. Prefer two short sentences or a clean connector such as **and**, **so**, or **because**.
- Do not glue two phrases into one sentence with a comma (no “phrase, not a table” pairs and no comma splices). Vocatives like `Hvala, Emire.` are fine.
- Block titles use a period after the letter label: `Lesson A. Ticket phrases` (not `Lesson A:`).
- Write full sentences in culture, civic, and fun-fact bodies.
- Keep website UI tips (accent buttons) out of chapter JSON. Book export must stay book-safe.
- Civic and fun-fact bodies use **Thesis then support then summary** (complete sentences, no colon-rant endings)
- Every drafted lesson needs `civicContext` { title, body, imageId, learnMore: { label, url } } with a dedicated image. Stay on **one** documented structural pressure. The body, title, image, quiz item, and `learnMore` link must all match that same topic. Do not switch mid-panel. Body must be one paragraph.
- Every drafted lesson needs `authenticListen` (Čuj Bosnu): one song or non-course speaker clip with listen-first gist task. Rights-safe embed/`clipId` only. Not studio cast dialogue audio.
- Every `sectionQuiz` question should set `skill` (`vocabulary` | `grammar` | `dialogue` | `culture` | `listening`) for remediation links.
- **Civic backlog:** Brčko District (self-governing city-district under international supervision) is a third unit beside the two entities. Do not cram it into the Lesson 7 entities note. Draft it on Lesson 13 (identity / people of BiH) or another northern/administration lesson.

### Book 1 pedagogy lock (tourist / expat survival)

Book 1 is an **A1 present-tense survival intro** for travelers, short-stay visitors, and early expats. It is not a full grammar course and not early A2 storytelling.

| Lock | Rule |
|------|------|
| Present tense only | Teach usable present forms and polite imperatives. No past tense (perfekt), no future paradigms. Past storytelling moves to **Book 2**. |
| Chunks over tables | Keep grammar panel titles if useful. Open every grammar explanation with a **chunks-first** line (see phrase bank below). Do not repeat the same opener on every panel in a lesson. |
| Spiral frames | Every new lesson after Lesson 1 must reuse **5 to 8** high-frequency frames from earlier lessons inside Say again, blocks, dialogue, or practice. |
| Say again warm-up | Every normal lesson (and reviews) includes `sayAgain` with **exactly 4** recycled Bosnian/English lines before Lesson A. |
| Review = frame drill | Lessons **7, 14, 21, 30** drill the core frames hard. Prefer recycle cards and question switches over new systems. |
| Public politeness | Any shop, café counter, bus, clinic, or stranger scene needs at least one polite exchange (`molim`, `hvala`, or `molim vas`). Keep ja/ti as the default social voice. |
| Studio speech OK | Keep dialogue clean for recording. Do not add reduced “street” variants in Book 1. |
| Audience copy | Lesson 0 and marketing must say short-stay social survival (tourist + early expat), Latin-only Bosnian, present tense. Lesson 0 must state that Book 1 teaches ready phrases and chunks, not full grammar tables. Do not promise A2. |

## 1. Product promises (every lesson)

| Promise | Rule |
|--------|------|
| Latin only | No Cyrillic on site or in video |
| Bosnian-focused | No HR/SR comparison sidebars after Lesson 0 |
| Cast | Ana, Emir, Amira, Mrvica appear when the story beat needs them |
| Cadence | ~60 minutes study time (reviews may be lighter) |
| Companion video | 8–10 min script mirrors Lesson A → B → dialogue |
| Naming | Always **Lesson N** (not Day N) in copy and video scripts |

---

## 2. Fixed recipe (normal lesson = Lesson 1 shape)

Fill `content/book1/day-XX/chapter.json` completely before marking `draft`.

| Section | Count / rule | Notes |
|--------|----------------|-------|
| **Metadata** | `day`, `book`, `section`, `title`, `titleEn`, `theme`, `storyBeat`, `estimatedMinutes: 60` | Titles from outline; one-sentence storyBeat |
| **status** | `draft` until human review → `published` | Never publish empty stubs |
| **learningGoals** | 2–3 bullets each: vocabulary / grammar / culture | No “to be filled” |
| **vocabulary** | **12–16** entries | Each: `bosnian`, `english`, `pronunciation`, `partOfSpeech`, `example` |
| **grammar** | **2–3** panels | (1) core system (2) how-to / typing or pattern (3) optional communicative use |
| **culture** | **80–120 words** + `imageId` | Place or ritual tied to the lesson images |
| **sayAgain** | **Exactly 4** recycled lines | Warm-up before Lesson A; prior-lesson frames only |
| **lessonBlocks** | **Exactly A + B** | A = system/forms; B = communicative use in the story scene |
| **conversation** | Title, setting, **6–8 lines** | BS + EN; cast-consistent; reuse prior greetings when natural |
| **puzzles** | **2** | Prefer: match + (scramble \| truefalse \| second match) |
| **practice** | **6–8** typed items | Force accents (`čćšžđ`) when the lesson taught them |
| **funFacts** | **3–4** | Mix: culture, language tip, story beat |
| **authenticListen** | **1** Čuj Bosnu block | Song or speaker; listen-first gist; 1–3 key lines; full attribution |
| **civicContext** | **1** fact + image | Structural pressure on BiH, tied to lesson theme; full sentences; no opinion slogans |
| **resources** | Channel/video + optional map + **next lesson** link | `/learn/lesson/N` |
| **sectionQuiz** | **8–10** MCQs with `question` (not `prompt`), `passPercent: 70`, explanations + **`skill`** | Per-lesson quiz (UI label: Lesson quiz). Mix meaning, form, one culture |
| **speakTargets** | Optional `number[]` | 0-based dialogue line indexes for AI speak-check (default: up to 3 learner lines) |
| **canDoChecks** | Review lessons: **3–5** | Short self-check prompts (speak / listen / write) |
| **dictionaryEntries** | Every teaching vocab item (+ full number set if taught) | `day: N` |
| **images** | **3** polygon scenes | Hero = culture `imageId`; mid-lesson; place/object beat |
| **video-script.md** | 8–10 min, Lesson N wording | Same A/B spine as blocks |

### Section tests and Book 1 final

Separate from per-lesson `sectionQuiz`. Canonical files live in `content/book1/assessments/`:

| Assessment | File | Covers | Route |
|------------|------|--------|-------|
| Section 1 test | `section-1.json` | Lessons 1–7 | `/test/section/1` |
| Section 2 test | `section-2.json` | Lessons 8–14 | `/test/section/2` |
| Section 3 test | `section-3.json` | Lessons 15–21 | `/test/section/3` |
| Section 4 test | `section-4.json` | Lessons 22–30 | `/test/section/4` |
| Book 1 final | `final.json` | Lessons 1–30 | `/test/final` |

Each assessment needs `id`, `kind`, `coversDays`, `title`, `intro`, `passPercent`, and `questions` (with optional `remediationDay`). Review lessons link to the matching section test. Lesson 30 also links to the final.

### Lesson block writing rules

- **Block A title:** `Lesson A: …` (forms, paradigm, list)
- **Block B title:** `Lesson B: …` (use it in today’s scene)
- Body: **~100–180 words**, not essays
- **2–3 tips** each (short, actionable)
- Teach **chunks** learners can say today; postpone full case tables

### Grammar panel rules

- Examples are **sayable** (`Ja sam Ana.`, `Kahvu, molim.`)
- One panel may be “say it as a chunk” when morphology is early
- Keep explanations plain English; no linguistics degree tone
- **First sentence = chunks-first reminder.** Pick from the phrase bank; rotate so learners do not see the same line on every panel. Within one lesson, use different openers for panels A/B/C.

**Chunks-first phrase bank** (same idea, varied wording):

1. Learn this as a full phrase. Do not treat it as a table.
2. Treat this as a ready chunk you can say today.
3. Say the whole line together. Skip the full chart for now.
4. Hold this as a spoken pattern. Do not treat it as a grammar grid.
5. Learn the usable chunk first. Full tables can wait.
6. Keep this as a sayable line rather than a paradigm list.
7. Memorize the phrase shape. Leave the full table for later.
8. Take this as a speaking chunk. Do not memorize a case chart yet.
9. Practice the whole expression before you worry about paradigms.
10. Build this as a ready-made line you can reuse.
11. Store this as a phrase you can pull out in conversation.
12. Focus on the spoken chunk. Postpone the full paradigm.

### Dialogue rules

- Advance **today’s** language + one story beat
- Narrator lines: max 1–2 for comic glue (Mrvica, etc.)
- English gloss on every line
- **Voice balance:** across the 8 dialogue lines, aim for roughly equal parts for the four studio voices: Ana/Narrator (`female-1`), Emir (`male-1`), Amira (`female-2`), and Male 2 roles (`Shopkeeper` / `Clerk` / `Konobar` / `Seller` / `Passerby` / `Mrvica`). Prefer **2 lines each** when the scene allows.

### Practice / quiz rules

- Answers compared case-insensitively; still write canonical casing
- If `?` or accents are required, say so in the prompt
- Quiz explanations teach, not just “correct”
- Every quiz item sets `skill` for remediation deep links after a failed quiz

### Čuj Bosnu selection guide

| Prefer `song` when… | Prefer `speaker` when… |
|---------------------|------------------------|
| Culture, emotion, place identity, review medleys | Shop, bus, phone, directions, transactional themes |
| Sevdah / folk / pop refrain is the ear stretch | Slow interview, café/market speech, radio bite |

A1 rules: 45–90s focus excerpt; gist + 1–3 audible anchors; Latin-only on-screen lyrics; never pirate full tracks.

### Speak-check lines

Mark 2–3 dialogue lines with `speakTargets` (indexes) when you want AI coaching. Otherwise the site offers the first few non-narrator lines.

---

## 3. Video companion (every lesson)

File: `content/book1/day-XX/video-script.md`

### Beat template (match Lesson 1)

| Time | Beat | Content |
|------|------|---------|
| 0:00 | Cold open | Lesson N title BS/EN |
| 0:40 | Goals | Lesson goals |
| 1:30 | Culture hook | Place/ritual + image credit note |
| 3:00 | Lesson A | Same as block A; on-screen cards |
| 5:00 | Lesson B | Same as block B; phrase cards |
| 6:30 | Mini dialogue | Pause-and-repeat; chapter lines |
| 8:00 | Practice + CTA | Pause for site puzzle; **Next: Lesson N+1** |
| End | End screen | `/learn/lesson/N` + playlist + credits |

### Video rules

- Runtime **8–10 minutes** (reviews may be 6–8)
- **No Cyrillic** on screen
- Say **Lesson N**, not Day N
- Scenic stills from chapter images / BiH locations
- Export / publish video only when chapter status is `published` (or batch-ready at launch)

---

## 4. Bosnia geography rule (every lesson)

Do **not** default every culture hook and image set to Sarajevo + Mostar.

| Rule | Detail |
|------|--------|
| New place fact | Each lesson’s culture body and/or fun facts must teach at least one concrete place, landscape, or tradition **not already the hero of the previous lesson** |
| Image diversity | Prefer unused BiH locations; do not recycle the same café/Sebilj/Mostar bridge art across chapters |
| Accuracy | Polygon art must match a real referenced photo (tower type, river, town). No generic “Ottoman skyline” stand-ins. Generate from the Commons source photo as the **primary** `reference_image_paths` input so composition, landmarks, and layout stay recognizable. Do not invent a new scene and then attach an unrelated photo credit. Before shipping, visually compare every polygon to its credited Commons file (side by side). If the credited file is only an icon/logo crop, replace the credit with a real photo of that subject first, then regenerate. Never bolt on baklava, desks, plazas, or other props that are absent from the source photo. |
| Whole country | Over Book 1, rotate regions: central Bosnia, Herzegovina, Krajina/Una, Posavina/north, mountains, and the Neum coast — not only the two tourist capitals |
| Story can stay | Ana/Emir/Amira may remain café-based; postcards, maps, and Emir’s stories carry the wider map |

## 4. Image brief (every lesson)

Three images before or with draft:

1. **Culture hero** — matches `culture.imageId`
2. **Mid-lesson scene** — story place or action
3. **Object / detail** — food, map, ticket, nature, etc.

Each image needs: `id`, `alt`, `localPath`, source URLs, `author`, `license`, `credit` (polygon treatment note OK in attributions sync).

---

## 5. Exceptions to the normal recipe

### Lesson 0 — orientation (already done)

- ~35 minutes; up to **3** lesson blocks; denser culture; light dialogue OK
- Do not use as the mold for Lessons 4–29

### Review lessons — 7, 14, 21 (and 30)

| Adjust | Rule |
|--------|------|
| New vocab | **6–10** recycle-heavy items (or themed review list) |
| Grammar | 1–2 “remember” panels, not new systems |
| Blocks | A = frame drill with core verbs/questions; B = board game / plan / diary using those frames |
| Say again | 4 highest-value frames from the section |
| Puzzles | Prefer match + truefalse over new scramble sets |
| Quiz | **10** items spanning the section’s lessons |
| Can-do | **3–5** checks on Lessons 14, 21, 30 |
| Video | “Section review” + highlight fails + CTA to next section |

### Lesson 30 — finale

- Full A1 celebration + light new party vocab
- Quiz can be broader review; keep A+B shape
- Story: graduation / cake heist per outline

---

## 6. Production workflow

```
outline.json (title, languageFocus, storyBeat)
    → draft chapter.json to this recipe
    → video-script.md
    → 3 images + attributions
    → node scripts/sync-content.cjs
    → status: draft
    → human review
    → status: published + reviewedAt
    → YouTube export / upload
```

### Definition of done (gate before `draft` is “ready for review”)

- [ ] Outline languageFocus covered in goals + grammar + blocks
- [ ] StoryBeat visible in culture and/or dialogue
- [ ] Counts in §2 met (no empty arrays)
- [ ] Dictionary mirrors teaching vocab
- [ ] Next-lesson resource points to `/learn/lesson/N+1` (L30 → curriculum)
- [ ] Video script uses Lesson N and mirrors A/B
- [ ] `node scripts/sync-content.cjs` run
- [ ] Site lesson page shows full shell with working quiz

### Suggested batch order

| Batch | Lessons | Focus |
|-------|---------|--------|
| A | 4–6 | Finish Section 1 language path |
| B | 7 | Section 1 review |
| C | 8–13 | Section 2 daily life |
| D | 14 | Section 2 review |
| E | 15–20 | Section 3 getting around |
| F | 21 | Section 3 review |
| G | 22–29 | Section 4 travel and longer stay (**present tense only**) |
| H | 30 | Finale frame review |

Human-review each batch before filming that batch’s videos when possible; at full launch, all 30 + videos ship together.

---

## 7. Per-lesson card (copy for each new chapter)

Use outline fields; keep this checklist in reviewer notes or PR body:

```
Lesson __: ________ / ________
Section __ | Theme: ________
Language focus: ________
Story beat: ________

[ ] Metadata + goals
[ ] Vocab 12–16 + dictionary
[ ] Grammar 2–3
[ ] Culture 80–120w + imageId
[ ] Blocks A + B
[ ] Dialogue 6–8
[ ] Puzzles ×2
[ ] Practice 6–8
[ ] Fun facts 3–4
[ ] Quiz 8–10
[ ] Resources (video, next)
[ ] Images ×3
[ ] video-script.md
[ ] sync-content
```

---

## 8. Quick reference — Section 1–4 language spine

Stay faithful to `outline.json`; do not rearrange major grammar jumps.

- **Section 1:** sounds/greetings → biti → numbers/café → family/gender → places → time → review  
- **Section 2:** food → shop → home → weather → invitations → identity → review  
- **Section 3:** directions → bus → restaurant → hobbies → holidays → phone → review  
- **Section 4:** Travnik day trip (present) → daily-activity questions (present) → nature → health → housing → work → Mostar landmarks → writing → finale  

**Core spiral frames (keep returning):**  
`Ja sam…` · `Zovem se…` · `Drago mi je.` · `Volim…` · `Želim…` · `Imam…` · `Idemo…` · `Odakle si?` · `Kakvo je vrijeme?` · `Gdje je…?` · `Koliko košta?` · `Molim.` / `Hvala.` / `Molim vas.`

---

## 9. Non-goals (avoid drift)

- Do not add a third essay block on normal lessons  
- Do not open stub chapters as `draft` with empty vocab/quiz  
- Do not teach comparative BCS columns  
- Do not replace the silly story with pure drill pages  
- Do not ship video scripts that still say “Day N” or “30 Days” if site says Lesson  
- Do not teach past tense or future paradigms in Book 1 (Book 2 owns storytelling tenses)  
- Do not promise A2 on Lesson 0 or marketing pages  

When in doubt: open Lesson 1 JSON and mirror field-by-field.
