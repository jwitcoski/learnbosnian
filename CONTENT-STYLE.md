# Content style guide — Learn Bosnian in 30 Days (Book 1)

## Language rules

- **Lesson titles only:** Say Lesson N. Do not put Day, Week, Sedmica, or “30 days” in lesson titles or lesson hero labels.
- **Curriculum groups:** Call groups **Section 1**, **Section 2**, etc. on the Learn page and in learner-facing copy. Do not label them Week 1 / Week 2.
- **No em dashes:** Do not use — or – as punctuation in learner-facing copy, titles, fun facts, dialogue, or video narration. Use full sentences with periods, commas, colons, or parentheses.
- **Full sentences:** Culture bodies, civic notes, fun facts, and `lessonBlocks` bodies must be complete sentences. No slogan fragments. Do not dump gloss lists after a colon (`Name the classics: burek (meat), sirnica (cheese)…`). Write one claim per sentence, then name the Bosnian word inside that sentence.
- **Book vs website:** Chapter JSON is book-safe. Do not put “tap the accent buttons” or other website-only UI instructions in chapter content. Website components may show accent-button help on their own.

- **Latin script only.** Never teach or display Cyrillic.
- Teach **standard Bosnian** forms used in everyday speech in Bosnia and Herzegovina.
- Do **not** add “also in Croatian…” or “Serbian says…” sidebars. Stay Bosnian-focused.
- **Exception for Lesson 0 only:** a short, respectful orientation may explain how Bosnian relates to Croatian/Serbian (mutual intelligibility, separate standards, identity). Do not teach Croatian or Serbian forms. Lessons 1 to 30 stay Bosnian-only.
- Prefer common Bosnian spellings: *kahva*, *hljeb*, *mlijeko*, *općina* when those are the natural forms in Bosnia and Herzegovina.
- **No unexplained BiH:** Do not write `BiH` in learner-facing English as if everyone knows the joke. Spell out **Bosnia and Herzegovina**, or say **Bosnian** for language/spelling (`Bosnian spelling`, not `BiH spelling`). Lesson 0 may teach the abbreviation BiH once, with a plain gloss. Bosnian lesson titles may keep BiH when that is the real local short form (`Ljudi iz BiH`), but the English title must spell the country out.
- Gloss every new Bosnian word in English the first time it appears in a section.
- Keep grammar bites small: one main idea per lesson block.

## Cast bible

| Character | Role | Personality |
|-----------|------|-------------|
| **Ana** | Tourist / learner | Curious, slightly clumsy with pronunciation, warm |
| **Emir** | Local guide | Patient, funny, proud of Sarajevo |
| **Amira** | Café owner | Practical, generous with coffee and advice |
| **Mrvica** | Cat | Steals scenes, food, and occasionally the plot |

Story spine: Ana arrives in Bosnia and Herzegovina; Emir shows her around; Amira’s café is home base; Mrvica causes mild chaos every few chapters.

## Chapter section checklist

Every chapter JSON must include (even review lessons):

1. Goals board (vocab + grammar + culture)
2. Culture / place hook
3. Lesson A
4. Fun quiz / puzzle
5. Lesson B + conversation (cast)
6. Practice questions
7. Fun facts (2–3)
8. Čuj Bosnu (`authenticListen`): one authentic song or non-course speaker clip with listen-first gist task (not studio cast audio)
9. More practice / game
10. Additional resources
11. Section quiz (4 options, balanced correctIndex); every question sets `skill`
12. Dictionary entries for all new words
13. Bosnia today (civicContext): one paragraph on a fact-based structural pressure on BiH, tied to the lesson theme, with its own image and a Wikipedia or news `learnMore` link

## Bosnia today and fun facts prose

Write complete thoughts. Do not rant in fragments, slogan stubs, or colon-led trailers.
The same ban applies to `lessonBlocks[].body`: no note-taking shorthand, no `Label: item, item, item` dumps, and no trailer after a colon that should have been its own sentence.

**Shape for every `civicContext.body` and every fun-fact `body`:**

1. **Thesis** — one clear first sentence that states the point
2. **Support** — two or three sentences with concrete facts or examples
3. **Summary** — one closing sentence that lands the idea

Keep the lesson link light and factual. Prefer plain speech over clever asides.

## Quiz quality

- Four options of similar length
- Roughly balanced A/B/C/D correct answers across a chapter
- Explanations reinforce the lesson’s goal, not trivia
- Tag each question with `skill`: `vocabulary` | `grammar` | `dialogue` | `culture` | `listening` so failed quizzes can deep-link Review Words / Grammar / Dialogue

## Čuj Bosnu (authenticListen)

- Required on drafted lessons (same bar as civicContext)
- `kind`: `song` or `speaker` (never course Ana/Emir/Amira studio lines)
- Rights-safe embed or clip only; store `license`, `credit`, `pageUrl` like images
- A1 gist task: listen first, then MCQ; reveal 1–3 key lines after listen
- Mix songs and speakers across the section; tie clip to lesson theme or place

## Images

- **Geographic diversity:** Do not recycle Sarajevo/Mostar café-and-bridge art every lesson. Prefer accurate, newly credited places across BiH (central Bosnia, Herzegovina, Una/Krajina, north, mountains, Neum coast). Culture hooks and fun facts should teach a fresh place fact, not rehash Sebilj/Stari Most.

- Free licenses only (Wikimedia Commons, Unsplash, Pexels)
- Always store `author`, `license`, `sourceUrl` / `pageUrl`, and display credit
- If missing: set `imagesNeeded: true` and add `imageBriefs` for the human reviewer
- Keep the running citation list up to date:
  - Chapter photos: add them under `images[]` in `chapter.json` (auto-harvested)
  - Homepage / other site photos: add them to `content/attributions.json`
  - Run `node scripts/sync-content.cjs` — writes `frontend/src/data/attributions.json`
  - Public page: `/attributions`

## Status workflow

`outlined` → `draft` → `in_review` → `published`

Only `published` chapters appear as open lessons on the website.
