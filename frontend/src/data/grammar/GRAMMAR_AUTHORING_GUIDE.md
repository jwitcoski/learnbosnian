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
- Em dashes. Colon dumps. Semicolons
- Colons inside learner-facing sentences
- “English speakers often struggle with…”
- Fake cheer. “You’ve got this.” “Great job noticing gender.”

**Do this instead**

- Talk. Short sentences. One idea each.
- Name a real thing. Coffee. A bridge. Tata.
- One joke, maybe. Then stop.
- Gloss the Bosnian word once, in the sentence. Rod means gender. Then move.
- If Book 1 already used the word, say so in one line.
- Tables are allowed. Keep them small. Three piles. Not seven cases.
- If an English speaker has to ask how they know, the last letter is the answer.

## The nerd box

Every chapter gets **Why it's like this**. One short paragraph. A real linguistics fact, told like a person who read one good book. The husband can skip it. A linguist should grin.

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
8. Look at these (8 to 12 short lines)
9. Try these (8 to 10)
10. Quick check (6 multiple choice)
11. Next (one sentence)

Chapter 0 may drop guess, pests, and a full drill set. It still needs English lies, a Book 1 line, the nerd box, a few tries, and a check.

**Never put in a grammar chapter.** Civic notes. Authentic listen. Cat-and-bazaar fun facts. Culture postcard. A 15-word vocab list. Say again. Lesson A and Lesson B.

## Images

Three pictures per chapter. Same polygon-paint treatment as Book 1. Credit the photographer. Reuse a Book 1 photo when it is already that object.

1. Hero. The chapter’s main object.
2. After the pattern.
3. After the nerd box, before the drills.

The picture has to teach the grammar. Caption is one grammar line, then the place credit. If you can swap the photo into another chapter and the caption still works, pick a different photo.

No civic buildings. No pink and blue gender clipart. No whiteboard stock.

Until a new file exists, reuse a Book 1 `localPath` and keep the original author, license, and pageUrl. Set `imagesNeeded` only when nothing honest is on disk yet.

## JSON fields

See Chapter 1. Required on a normal chapter: `chapter`, `kind`, `title`, `titleEn`, `theme`, `status`, `estimatedMinutes`, the slot objects, `quiz`, `next`, `images`, `imageSlots`.
