# Grammar handbook authoring guide

**Book title:** How to Speak Bosnian: Grammar  
**Exemplar:** Chapter 1 (`content/grammar/chapter-01/chapter.json`)  
**Shorter exception:** Chapter 0. Same voice. Fewer slots. It only answers why this feels hard.

Copy Chapter 1. Do not invent a new shape. Headings on the page sound like talk. Call them Chapter 1, Chapter 2. Not Lesson. Not Day.

This book is a notebook. Book 1 is the walk through town. One weird English habit, one Bosnian fix, a small chart, some tries, a check.

About 40 minutes. Keep the same words. Kahva. Most. Kuća. Ana. Emir. Pivo. Sarajevo. Auto. More. Do not invent a new grocery list every chapter.

## Voice

Write like you are explaining coffee to a tired spouse. If a sentence could sit on a startup landing page, cut it.

**Banned in learner text**

- Can-do, objective, by the end of this chapter, you will be able to
- Unlock, journey, dive in, let’s explore, it’s important to note
- Robust, leverage, framework, mental model, the machine, the wall
- Stacked “Do not X. Do not Y. Do not Z.”
- Three parallel slogans in a row
- Phrase fragments punctuated as sentences. Bad. “Open the dictionary form. The boring form. The one in the vocab list.”
- Em dashes. Colon dumps. Semicolons
- Colons inside learner-facing sentences
- “English speakers often struggle with…”
- Fake cheer. “You’ve got this.” “Great job noticing gender.”

**Do this instead**

Every teaching block uses the same shape as Book 1 civic notes and fun facts.

1. **Thesis.** One first sentence that states the point.
2. **Support.** Two or three complete sentences with a real thing in them. Coffee. A bridge. Tata.
3. **Summary.** One closing sentence that lands the idea.

Name a Bosnian word inside a sentence and gloss it there. Rod means gender. Then move. If Book 1 already used the word, say so in a full sentence. Tables are allowed. Keep them small.

## Spoken lines and sample words

Every Bosnian line on the page needs a speaker from the Book 1 cast. Ana. Emir. Amira. Put `speaker` on `knownLine` and on every `look.items` line. The site plays the line like Book 1 dialogue.

Keep a short `vocabulary` list. Four to six sample words is enough. Not a 15-word dump. Those cards get tap-to-hear.

Put two or three of those words in `speakTargets` for Speak Check. AWS Transcribe scores the recording. Do not put Speak Check on every line.

## The nerd box

Every chapter gets **Why it's like this**. One short paragraph in the same thesis, support, summary shape. A real linguistics fact, told like a person who read one good book. The husband can skip it. A linguist should grin.

- One fact. Not a history of Slavic.
- Name the thing in English first. Then the fancy word once if you must. Gloss it.
- Tie it to today’s pattern.
- No “Interestingly.” No “scholars note.” No “it is believed.”

## Chapter bits, in this order

1. Why you are here
2. Why English lies
3. A line you already say
4. The pattern
5. How you guess (then the pests)
6. The bit that tricks you
7. Why it's like this
8. Look at these (8 to 12 spoken lines, each with a speaker)
9. Try these (8 to 10)
10. Quick check (6 multiple choice)
11. Next (a short thesis paragraph, not a slogan)

Chapter 0 may drop a full drill set. It still needs English lies, a Book 1 line with a speaker, the nerd box, a few tries, and a check.

**Never put in a grammar chapter.** Civic notes. Authentic listen. Cat-and-bazaar fun facts. Culture postcard. A 15-word vocab list. Say again. Lesson A and Lesson B.

## Images

Three pictures per chapter. Same polygon-paint treatment as Book 1. Credit the photographer with the same ref codes the site already uses. Grammar photos are `G.0a`, `G.1b`, and so on, and they link to `/attributions`. Reuse a Book 1 photo when it is already that object, and still give it a Grammar ref.

1. Hero. The chapter’s main object.
2. After the pattern.
3. After the nerd box, before the drills.

The picture has to teach the grammar. Caption is one complete sentence, then the Book 1-style credit line. If you can swap the photo into another chapter and the caption still works, pick a different photo.

No civic buildings. No pink and blue gender clipart. No whiteboard stock.

Until a new file exists, reuse a Book 1 `localPath` and keep the original author, license, and pageUrl. Set `imagesNeeded` only when nothing honest is on disk yet.

## JSON fields

See Chapter 1. Required on a normal chapter: `chapter`, `kind`, `title`, `titleEn`, `theme`, `status`, `estimatedMinutes`, the slot objects, `vocabulary`, `speakTargets`, `quiz`, `next`, `images`, `imageSlots`.
