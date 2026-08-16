# YouTube vocab supplement videos

**Series:** How to Speak Bosnian (vocab + grammar drill)  
**Channel:** [@HowtospeakBosnian](https://www.youtube.com/@HowtospeakBosnian)  
**Role:** These videos are a **supplement**, not a reload of the full website lesson. They drill the lesson’s vocabulary (and a short grammar beat). Full stories, dialogue, puzzles, and culture stay on [learnbosnian.club](https://learnbosnian.club).

The longer Lesson A / B companion scripts in `content/book1/day-XX/video-script.md` remain a separate product line.

## Runtime

**5 to 10 minutes** per lesson (reviews run shorter).

| Vocab count | Typical length |
|-------------|----------------|
| 10 words | ~5 to 6 min |
| 12 to 14 | ~6 to 8 min |
| 16 | ~8 to 10 min |

## Fixed speaker template

### Intro (every video)

> Hi and welcome to How to Speak Bosnian. Today we will be going over the vocab and grammar of Lesson N, [English title]. [Bosnian title].

### Vocab drill (each word)

1. Say the Bosnian word **slowly** (twice).
2. Say the English definition **twice**.
3. Pause about one second before the next word.

### Grammar beat (short)

After the intro, before vocab: one title slide per grammar panel and **one short spoken sentence** per panel. Do not teach the full website lesson.

### Ending (every video)

> That’s all for Lesson N. Practice these words on learnbosnian.club, then continue with Lesson N+1 on the site. Hvala, and doviđenja!

Lesson 30 ending swaps the next-lesson line for a Book 1 finish CTA.

## Slide deck (CapCut / Resolve)

Yellow or gold text over muted Bosnia B-roll. Latin script only. No Cyrillic.

| Slide | On screen | Duration guide |
|-------|-----------|----------------|
| 1. Title | How to Speak Bosnian · Lesson N · BS title · EN title | 8 to 12 s (under intro) |
| 2. Agenda | Today · Vocabulary · Grammar | 5 to 8 s |
| 3+. Grammar | Panel title (large) · one tip line | ~20 to 25 s each |
| Vocab divider | Vocabulary | 3 to 5 s |
| One slide per word | Bosnian (hero) · English · pronunciation | ~18 to 22 s each |
| Closing | Hvala · learnbosnian.club · Lesson N+1 | 15 to 20 s |
| End screen | Subscribe · playlist · site link | CapCut end card |

## B-roll (rights-safe only)

Use **licensed or free** drone and street footage of Bosnia and Herzegovina (Pexels, Pixabay, Wikimedia Commons, or other clear commercial/CC licenses). Dim or blur the plate so gold text stays readable.

Do **not** rip other creators’ YouTube videos for background use. That risks copyright claims on the channel.

Rotate places across the book (Sarajevo, Mostar, Travnik, Una, mountains, Neum coast). Prefer footage that matches the lesson theme when possible.

## Source files

| File | Purpose |
|------|---------|
| `content/book1/day-XX/vocab-video-script.md` | Slide list + full narration for Lesson XX |
| `node scripts/generate-vocab-video-scripts.cjs` | Rebuild all scripts from `chapter.json` |
| `node scripts/export-youtube-vocab.cjs --day N` | CapCut pack under `exports/youtube-vocab/day-NN/` |

## Production steps

1. Confirm chapter vocab and grammar in `chapter.json` are reviewed.
2. Run `node scripts/generate-vocab-video-scripts.cjs` (or export for one day).
3. Open `exports/youtube-vocab/day-NN/` after `export-youtube-vocab.cjs`.
4. Assemble in CapCut with the master template (gold text, BiH B-roll, slow pacing).
5. Upload to playlist **How to Speak Bosnian · Vocab** with a link to `/learn/lesson/N` and B-roll credits in the description.
