# Copy audit — Learn Bosnian (English chrome)

**Status:** Audit only. No application files edited yet. Waiting for approval.

**Voice target:** Warm, practical, confident, welcoming. Like a good language teacher speaking to a beginner. Respectful of Bosnia and Herzegovina. No fluency promises. No em dashes.

**Out of this pass (unless you say otherwise):**
- Bosnian words, glosses, grammar examples, dialogue lines, quiz *item* text, culture/civic lesson bodies, fun facts
- Photo credit lines that must stay accurate for licenses (author, license, source)
- Unused Landy template JSON / leftover `translation.json` keys that are not rendered
- Recorder studio and backend API messages

**Terminology snapshot (current usage):**

| Concept | Terms in use today | Proposed house term |
| --- | --- | --- |
| Unit of study | Lesson (UI), chapter (footer/content) | **Lesson** in learner UI; keep “chapter” for publishing SOP only |
| Word list | Dictionary (nav), Mini-dictionary (page/footer) | Pick one (see Questions) |
| End-of-section check | section test | **section test** (keep) |
| End-of-lesson check | Lesson quiz / section quiz (JSON titles) | **Lesson quiz** |
| Curriculum index | Learn (nav), Curriculum (footer/links) | **Curriculum** in links; nav can stay **Learn** |
| Speaking tool | Speak Check / AI Speak Check / AI check | **Speak Check** |

---

## Proposed changes

| File | Current text | Proposed text | Why it changed |
| --- | --- | --- | --- |
| `frontend/public/index.html` | `Learn Bosnian language with interactive lessons` | `A1 Bosnian for short stays and early life in Bosnia and Herzegovina. Latin script, present tense, story-led lessons.` | Meta description was generic template SEO. Says what the course actually is. |
| `frontend/public/index.html` | `Learn Bosnian - Interactive Language Learning` (og/twitter title) | `Learn Bosnian` | Brand-first. “Interactive Language Learning” is empty marketing. |
| `frontend/public/index.html` | `Learn Bosnian language with interactive lessons and exercises.` | Same as new meta description above | Matches title/description; drops filler “interactive…exercises.” |
| `frontend/public/index.html` | `You need to enable JavaScript to run this app.` | `Enable JavaScript to use Learn Bosnian.` | Softer, product-named, less “app template.” |
| `frontend/public/manifest.json` | `Learn Bosnian Language App` | `Learn Bosnian` | Drop “Language App”; keep brand short on home screen. |
| `frontend/src/pages/Home/index.tsx` | `A1 present-tense Bosnian for short stays and early expat life: order food, find your way, meet people, and stay in Latin script with Ana, Emir, Amira, and Mrvica.` | `Present-tense A1 Bosnian for short stays and early life here. Order food, ask directions, meet people. Latin script only. Ana, Emir, Amira, and Mrvica walk you through it.` | Clearer for beginners. “Early expat life” is insider jargon. Colon dump becomes short sentences. |
| `frontend/src/pages/Home/index.tsx` | `See curriculum` | `Browse curriculum` | Slightly warmer action; still short. (Or keep “See curriculum” if you prefer.) |
| `frontend/src/pages/Home/index.tsx` | `One clear path` | `One path, reviewed as it goes live` | Current headline is vague. New one states the real differentiator (reviewed publishing). |
| `frontend/src/pages/Home/index.tsx` | `Every chapter is drafted and reviewed before it goes live. Sit with a džezva of kahva and follow the same lesson shape every time — goals, culture, practice, and a quiz.` | `Each lesson is drafted and reviewed before it goes live. Same shape every time: goals, culture, practice, and a quiz. Make a džezva of kahva and settle in.` | Removes em dash. Swaps “chapter” → “lesson.” Keeps kahva warmth without stacking clauses. |
| `frontend/src/pages/Home/index.tsx` | `Open the curriculum` | `Open curriculum` | Shorter button. |
| `frontend/src/pages/Home/index.tsx` | `Same lesson shape every time` | `What you do in each lesson` | Headline was restating the previous section. This one sets up the list. |
| `frontend/src/pages/Home/index.tsx` | `Goals, culture, vocab, grammar, Say again warm-up, a puzzle, conversation, practice, fun facts, another game, resources, then a section quiz.` | `Goals, culture, words, grammar, a Say again warm-up, a puzzle, conversation, practice, fun facts, a game, resources, then the lesson quiz.` | Scannable, consistent “lesson quiz,” slightly less breathless. |
| `frontend/src/pages/Home/index.tsx` | `Dialogues with recurring characters — then record yourself for AI Speak Check (Amazon Transcribe + Bedrock coaching).` | `Dialogues with the same characters. Then record yourself for Speak Check, which listens and coaches your pronunciation.` | Removes em dash and AWS brand stack from the hero pillars. Product benefit first. |
| `frontend/src/pages/Home/index.tsx` | `Matching, unscramble, and quizzes for brains that tire of dry drills.` | `Matching, unscramble, and quizzes when you want a break from drills.` | Less cute; clearer. |
| `frontend/src/pages/Home/index.tsx` | `A growing mini-dictionary of every word you learn, ready when you need it.` | `A mini-dictionary that grows with each published lesson.` | More accurate; less brochure tone. |
| `frontend/src/pages/Home/index.tsx` | `Follow the story through Bosnia` | `Follow the story across Bosnia and Herzegovina` | Spells out the country; matches CONTENT-STYLE. |
| `frontend/src/pages/Home/index.tsx` | `Walk Baščaršija with Ana, drink kahva at Amira’s, get lost with Emir, and let Mrvica steal the scene. Book 1 is tourist and early-expat survival across Bosnia and Herzegovina, all in the present tense.` | `Walk Baščaršija with Ana. Drink kahva at Amira’s. Get a little lost with Emir. Let Mrvica steal the scene. Book 1 is survival Bosnian for travelers and new arrivals, all in the present tense.` | Breaks the stack of clauses. Softens “early-expat survival” without tourist cliché overload. |
| `frontend/src/pages/Home/index.tsx` | `Browse the book series` | `See the book series` | Matches nav “Books”; still clear. |
| `frontend/src/pages/Home/index.tsx` | `Watch along on YouTube` | `Watch on YouTube` | Drop filler “along.” |
| `frontend/src/pages/Home/index.tsx` | `Join learners on How to speak Bosnian. Each Book 1 chapter has a companion video with scenic stills, clear text, and optional narration.` | `The channel is How to speak Bosnian. Most Book 1 lessons have a companion video: stills, on-screen text, and optional narration.` | Removes vague “Join learners.” “Most” avoids overclaiming if not every lesson is filmed yet (confirm). |
| `frontend/src/pages/Home/index.tsx` | `Open YouTube channel` | `Open the channel` | Shorter; heading already says YouTube. |
| `frontend/src/pages/Home/index.tsx` | `Questions about the books, school use, or a chapter draft? Send a note.` | `Questions about the books, classroom use, or a lesson draft? Send a note.` | “School use” → “classroom use”; “chapter” → “lesson” for learners. |
| `frontend/src/components/Footer/index.tsx` | `Book 1 with human-reviewed chapters. Latin script only. Culture, puzzles, and a cat named Mrvica.` | `Book 1 lessons, reviewed before they go live. Latin script only. Culture, puzzles, and a cat named Mrvica.` | Same facts, less brochure stacking of “human-reviewed chapters.” |
| `frontend/src/components/Footer/index.tsx` | `Contact Us` | `Contact` | Drop corporate Title Case. |
| `frontend/src/components/Footer/index.tsx` | `Lesson 0 orientation` | `Lesson 0` | Nav already implies orientation; shorter. |
| `frontend/src/components/Footer/index.tsx` | `Cite photos for print` | `Photo credits` | Matches page purpose; clearer for web readers. |
| `frontend/src/pages/Learn/index.tsx` | `Start with Lesson 0 (why Bosnian?), then follow Ana, Emir, Amira, and Mrvica through Bosnia and Herzegovina. New chapters publish after human review.` | `Start with Lesson 0 (Why Bosnian?). Then follow Ana, Emir, Amira, and Mrvica across Bosnia and Herzegovina. New lessons go live after review.` | Consistent Lesson casing; drop vague “human review” stacking while keeping the fact. |
| `frontend/src/pages/Learn/index.tsx` | `Coming soon · Lesson {n}` | `Lesson {n} · coming soon` | Puts lesson number first for scanning. |
| `frontend/src/pages/Day/index.tsx` | `Lesson {n} — {title} is coming soon. Status: {status}.` | `Lesson {n} ({title}) is not live yet.` | Removes em dash and internal `status` jargon from the learner banner. |
| `frontend/src/pages/Quiz/index.tsx` | `Quiz unlocks when Lesson {day} is available.` | `This quiz opens when Lesson {day} is live.` | Plainer. |
| `frontend/src/pages/Quiz/index.tsx` | `Lesson {day} quiz — {title}` | `Lesson {day} quiz: {title}` | No em dash. |
| `frontend/src/pages/Books/index.tsx` | `Three-book series` | `The book series` | Less brochure; still clear. |
| `frontend/src/pages/Books/index.tsx` | `A path from first greetings to confident conversation — website, print (Scribus), and YouTube companions.` | `From first greetings toward fuller conversation. Website lessons, print (Scribus), and YouTube companions.` | Removes fluency-adjacent “confident conversation” and the em dash. |
| `frontend/src/pages/Books/index.tsx` | `Book 1 — {title}` | `Book 1: {title}` | No em dash. |
| `frontend/src/pages/Books/index.tsx` | `Level A1. Thirty one-hour present-tense survival chapters for travelers and early expats. Cast: Ana, Emir, Amira, Mrvica.` | `Level A1. Thirty present-tense lessons (about an hour each) for travelers and new arrivals. Cast: Ana, Emir, Amira, Mrvica.` | “Chapters” → “lessons”; “early expats” → “new arrivals.” |
| `frontend/src/pages/Books/index.tsx` | `Start Book 1 →` | `Start Book 1` | Arrow is decorative; keep text action-only (or keep → if house style likes it). |
| `content/book2/outline.json` (and synced `frontend/src/data/book2/outline.json`) | `Learn Bosnian — Book 2: Go Further` | `Learn Bosnian: Book 2, Go Further` | No em dash. |
| `content/book2/outline.json` | `Past and future storytelling, deeper cases, aspect pairs, and richer regional travel with Ana, Emir, Amira, and Mrvica.` | `Past and future storytelling, more cases, aspect pairs, and wider travel with Ana, Emir, Amira, and Mrvica.` | “Richer” is soft marketing; “wider” is concrete. |
| `content/book2/outline.json` | `Book 2 owns past-tense storytelling after Book 1 stays present-tense only. Full chapter list lands after Book 1 is published night-by-night.` | `Book 2 picks up past tense after Book 1 stays present-tense only. The full lesson list will land after Book 1 is published.` | Drop “owns” and “night-by-night” insider voice for learners. |
| `content/book3/outline.json` | `Learn Bosnian — Book 3: Speak with Confidence` | `Learn Bosnian: Book 3, Speak Clearly` (or keep title pending Question) | “Speak with Confidence” is motivational marketing. |
| `content/book3/outline.json` | `Advanced conversation, writing, and cultural nuance. Grammar handbook style chapters plus long-form dialogues.` | `Longer conversation, writing, and cultural detail. Handbook-style grammar lessons plus longer dialogues.` | Less academic brochure; still accurate. |
| `content/book3/outline.json` | `Capstone project: Ana’s year in BiH` | `Capstone project: Ana’s year in Bosnia and Herzegovina` | Spell out country in learner-facing English (CONTENT-STYLE). |
| `content/book3/outline.json` | `Teaser only until Books 1–2 are complete.` | `Outline only until Books 1 and 2 are complete.` | En dash → “and”; “Teaser” is marketing. |
| `frontend/src/pages/Dictionary/index.tsx` | `Words from published and previewable chapters. Grows each night as Book 1 is reviewed. Latin script only.` | `Words from lessons you can open now. The list grows as Book 1 lessons are reviewed and published. Latin script only.` | Avoids promising a literal nightly update if that is process, not a guarantee. |
| `frontend/src/pages/Dictionary/index.tsx` | `Search Bosnian or English…` | `Search Bosnian or English` | Ellipsis optional; keep if you like search-field convention. |
| `content/attributions.json` intro (synced to frontend data) | `Running register of every photo used on the site and in Book 1. Use this list when citing images for print, Scribus export, or YouTube descriptions. Chapter images are harvested automatically from each chapter.json; homepage and other site assets are listed here by hand.` | `Every photo used on the site and in Book 1, listed for citation. Use this when you credit images for print, Scribus export, or YouTube. Lesson images come from each lesson’s chapter file; homepage photos are added by hand.` | Plainer; less “running register” legalese. |
| `frontend/src/pages/Attributions/index.tsx` | `This page is the running total. When you export Scribus or YouTube packs, pull credits from here or from each chapter’s images[] block.` | `Use this page as the master list. For Scribus or YouTube packs, take credits from here or from each lesson’s image list.` | Hides `images[]` code speak from learners/creators who are not engineers. |
| `frontend/src/components/lesson/LessonShell.tsx` | `Start here when you can. Then return for words, dialogue, and practice on this page.` | `Watch when you can, then come back for words, dialogue, and practice on this page.` | More direct. |
| `frontend/src/components/lesson/LessonShell.tsx` | `Tap any word to hear it. Loop and slow speed help with shadowing.` | `Tap a word to hear it. Use Loop and slower speed when you want to shadow.` | Clearer verbs. |
| `frontend/src/components/lesson/LessonShell.tsx` | `Play the full scene once (cover the English with your hand if you can), then tap individual lines. Use Speak on the highlighted lines.` | `Play the full scene once. Cover the English if you can. Then tap lines one by one. Use Speak on the highlighted lines.` | Short sentences; easier on mobile. |
| `frontend/src/components/lesson/LessonShell.tsx` | `More practice: game` | `Practice game` | Less label-y. |
| `frontend/src/components/lesson/LessonShell.tsx` | `Additional resources` | `More resources` | Shorter. |
| `frontend/src/components/lesson/LessonShell.tsx` | `Or open the dedicated quiz page: Lesson {n} quiz` | `Open the full-page quiz: Lesson {n} quiz` | Clearer. |
| `frontend/src/components/lesson/SectionQuiz.tsx` | `Quiz arrives when this chapter is fully drafted.` | `This quiz will appear when the lesson is fully drafted.` | “Arrives” is cute; “chapter” → “lesson.” |
| `frontend/src/components/lesson/SectionQuiz.tsx` | ` — no answer selected` / ` — right answer:` | `. No answer selected` / `. Right answer:` | No em dash (AssessmentQuiz already uses periods). |
| `frontend/src/components/lesson/SectionQuiz.tsx` | `Lesson complete!` | `Lesson complete.` | Keeps warmth without the bang. |
| `frontend/src/components/lesson/SectionQuiz.tsx` | `Review these sections, then submit again.` | `Review the linked parts, then submit again.` | “Sections” collides with curriculum Sections 1–4. |
| `frontend/src/components/lesson/AssessmentQuiz.tsx` | `This test is not ready yet.` | `This test is not ready yet. Check back after the lessons it covers are live.` | Adds next step. |
| `frontend/src/components/lesson/AssessmentQuiz.tsx` | `Book 1 final passed!` / `Section test passed!` | `Book 1 final passed.` / `Section test passed.` | Same tone rule as lesson quiz. |
| `frontend/src/components/lesson/PracticeList.tsx` | `Incorrect — answer: {answer}` | `Incorrect. Answer: {answer}` | No em dash. |
| `frontend/src/components/lesson/PuzzleGame.tsx` | `Incorrect — {label}` | `Incorrect. {label}` | No em dash. |
| `frontend/src/components/lesson/PuzzleGame.tsx` | `— choose —` | `Choose…` | No em dash; normal placeholder. |
| `frontend/src/components/lesson/ReviewDeck.tsx` | `A few words from this lesson plus earlier misses. Flip, then mark how it went.` | `A few words from this lesson, plus ones you missed before. Flip the card, then mark how it went.` | Slightly clearer. |
| `frontend/src/components/lesson/ReviewDeck.tsx` | `Review round complete. Come back next lesson for more.` | `Round done. Come back next lesson for more.` | Shorter. |
| `frontend/src/components/lesson/CanDoChecklist.tsx` | `Nice. You claimed this lesson’s can-dos.` | `Nice. You marked every can-do for this lesson.` | “Claimed” sounds like a badge system you do not have. |
| `frontend/src/components/lesson/SpeakPractice.tsx` | `Speak check is unavailable right now. Compare with the teacher audio.` | `Speak Check is unavailable right now. Listen to the teacher audio and compare by ear.` | Consistent product name; clearer next step. |
| `frontend/src/components/lesson/SpeakPractice.tsx` | `AI check ({n} left)` / `AI checks used` | `Speak Check ({n} left)` / `Speak Check used up` | One product name. |
| `frontend/src/components/lesson/SpeakPractice.tsx` | `Heard via Amazon Transcribe (bs-BA); coaching from Amazon Bedrock (Nova).` | `Checked with speech recognition and short coaching notes.` | Learners need trust, not a cloud architecture footnote. Keep tech detail in docs if needed. |
| `frontend/src/components/lesson/SpeakPractice.tsx` | `AI check: your take → S3 → Amazon Transcribe → Amazon Bedrock.` | `Speak Check listens to your recording and sends back short tips.` | Same reason. |
| `frontend/src/components/lesson/SpeakPractice.tsx` | `Microphone not available in this browser.` | `This browser can’t use your microphone. Try Chrome or Safari, or check site permissions.` | Explains what to do next. |
| `frontend/src/components/lesson/AuthenticListenPanel.tsx` | `Gist unlocked` / `I listened. Unlock gist` / `Start the video, then unlock gist` | `Gist ready` / `I listened. Show gist` / `Start the video, then show the gist` | “Unlock” sounds like gamification; “show” matches the action. |
| `frontend/src/components/lesson/AuthenticListenPanel.tsx` | `Not quite. Aim for: {option}` | `Not quite. The better answer is: {option}` | Clearer for beginners. |
| `frontend/src/common/utils/useForm.tsx` | `There was an error sending your message, please try again later.` | `We couldn’t send your message. Wait a moment and try again.` | Warmer; says what to do. |
| `frontend/src/common/utils/useForm.tsx` | `Your message has been sent!` | `Message sent. Thanks.` | Less bang; still warm. |
| `frontend/src/common/utils/useForm.tsx` | `Failed to submit form. Please try again later.` | `Something went wrong on submit. Try again in a moment.` | Same tone as other error. |
| `frontend/src/common/utils/validationRules.ts` | `Email address is required` / `Email address is invalid` | `Email is required` / `Enter a valid email` | Shorter mobile copy. |
| `frontend/src/components/ContactForm/index.tsx` + `locales/en/translation.json` | Labels resolve via `t("name")` / `t("email")` / `t("message")` (keys missing; placeholders work) | Wire labels to `Name` / `Email` / `Message` (or add matching keys) | Bug: learners may see raw `name` / `email` / `message` as labels. |
| Assessment intros (`content/book1/assessments/*.json`) | `Pass with 70% or higher.` (repeated) | Keep fact; optional soften to `You need 70% or higher to pass.` | Already clear; only tone polish if desired. |
| `content/book1/outline.json` section 0 focus | `What Bosnian is, where the name comes from, who speaks it, and who this course is for` | Keep (already plain and good) | No change needed. |
| Header CTA | `Start Lesson 0` | Keep | Strong, specific, consistent with product. |

---

## Em dash sweep (learner-facing chrome)

CONTENT-STYLE and this brief ban em dashes in learner-facing copy. These UI strings still use `—` (or title-style em dashes) and should be normalized in the same pass:

- Home path + Speak pillar bodies
- Books intro and Book 1 heading
- Day locked banner; Quiz page title
- SectionQuiz feedback fragments
- PracticeList / PuzzleGame incorrect feedback and `— choose —`
- Book 2 / Book 3 titles in outline JSON
- Attribution `whereUsed` labels like `Book 1 · Lesson 0 — Why Bosnian?` → `Book 1 · Lesson 0: Why Bosnian?` (credit accuracy unchanged)

Do **not** change em dashes inside third-party photo credit strings if they are part of an upstream attribution format you must preserve; prefer colon only in *our* composed labels.

---

## Already in good shape (keep)

- Brand `Learn Bosnian` as the hero H1
- Footer warmth (`…and a cat named Mrvica`)
- `Say zdravo` contact heading
- Nav labels Learn / Dictionary / Books / YouTube
- Speak / Play / Remember pillar labels (short and useful)
- Most lesson chrome headings: Lesson goals, Grammar, Practice, Fun facts, Bosnia today
- Review deck grades `Again` / `Got it`
- Can-do help: `Honest self-check…`
- Accent-button help under practice inputs

---

## Questions before changing

1. **Dictionary vs Mini-dictionary:** Nav says Dictionary; page/footer say Mini-dictionary. Which house term should we standardize on?
2. **Lesson vs chapter in learner UI:** Publishing docs say “chapter.” Should every learner-facing string say **lesson** only?
3. **YouTube claim:** Is it true that *each* Book 1 chapter has a companion video, or only published ones / most of them? Proposed copy says “Most…” until confirmed.
4. **“Grows each night”:** Is nightly publish a promise we want on the Dictionary page, or internal SOP only?
5. **Book 3 title:** Keep **Speak with Confidence**, or rename to something less motivational (e.g. **Speak Clearly**, **Book 3**, **Go Deeper**)?
6. **Speak Check tech disclosure:** OK to hide Amazon Transcribe / Bedrock / S3 from the lesson UI and keep that in docs, or do you want a short “uses Amazon speech tools” trust line?
7. **Hero secondary CTA:** Prefer **See curriculum**, **Browse curriculum**, or **View lessons**?
8. **Scope for a later pass:** Should we also tone-edit English pedagogical bodies (`culture.body`, `civicContext`, grammar explanations, quiz explanations), or keep this PR to chrome/marketing/UI states only?
9. **Contact form labels:** Confirm you want the label bug fixed in the same copy pass (recommended).
10. **Unused Landy strings** in `translation.json` / `*Content.json`: delete in a cleanup PR, or leave untouched?

---

## Highest-impact themes (for the summary)

1. Replace generic SEO/meta and “interactive language learning” with specific Book 1 positioning.
2. Tighten the homepage lede and pillars; remove AWS pipeline talk from marketing surfaces.
3. Kill em dashes and outcome-y phrasing (“confident conversation,” “Speak with Confidence”).
4. Align terminology (lesson/chapter, Dictionary/Mini-dictionary, Speak Check).
5. Make errors and locked states explain the next step in plain second person.
