# -*- coding: utf-8 -*-
import json
from pathlib import Path

audit = {
  "verdict": "needs_revision",
  "summary": "Fresh disk re-audit of grammar chapters 0-13 plus outline themes/titles. No Cyrillic, no learner-facing em/en dashes, no Lesson/Day/Week/Sedmica naming, no AWS/UI jargon, no unexplained BiH, speakers present (Ana/Emir/Amira only) on knownLine and look lines. Blockers: Mrvica still appears as a quiz distractor in chapters 0 and 13, and chapter 6 still has a learner-facing semicolon. Majors cluster in slogan-fragment drill copy and a few themes after mold polish, plus one colon gloss dump in chapter 1 whyHere.",
  "blockerCount": 4,
  "majorCount": 19,
  "minorCount": 10,
  "chaptersCovered": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
  "issues": [],
  "blockers": [],
  "nextArtifactToEdit": "content/grammar/chapter-00/chapter.json → quiz.questions[1].options[3] and quiz.questions[5].options[3] (replace Mrvica distractors; then mirror-fix chapter-13 quiz.questions[0].options[3])",
  "requiredHumanChecks": [
    "Confirm replacement distractors for the three Mrvica quiz options still keep four plausible choices and balanced correctIndex.",
    "Decide whether try prompts may keep telegraphic cues like Mid-cup. / Habit. / Ana. / Emir. or must be rewritten as full prompt sentences.",
    "After fragment/theme fixes, re-skim chapter themes against outline.json themes (several outline themes are cleaner full sentences than the chapter.json themes, especially 9 and 10).",
    "Bosnian forms were treated as intentionally retained by Fact Checker; this pass did not re-judge grammatical correctness of Bosnian examples."
  ]
}

issues = [
  {
    "severity": "blocker",
    "path": "content/grammar/chapter-00/chapter.json.quiz.questions[1].options[3]",
    "evidence": "A café scene with Mrvica",
    "fix": "Remove Mrvica/cat-plot cast from grammar handbook quiz copy; replace with a non-cat distractor."
  },
  {
    "severity": "blocker",
    "path": "content/grammar/chapter-00/chapter.json.quiz.questions[5].options[3]",
    "evidence": "A café scene with Mrvica",
    "fix": "Remove Mrvica/cat-plot cast from grammar handbook quiz copy; replace with a non-cat distractor."
  },
  {
    "severity": "blocker",
    "path": "content/grammar/chapter-13/chapter.json.quiz.questions[0].options[3]",
    "evidence": "A café scene with Mrvica",
    "fix": "Remove Mrvica/cat-plot cast from grammar handbook quiz copy; replace with a non-cat distractor."
  },
  {
    "severity": "blocker",
    "path": "content/grammar/chapter-06/chapter.json.try.items[5].explanation",
    "evidence": "Both moja and kahva stayed name-it; wanting needs moju kahvu.",
    "fix": "Remove the semicolon. Split into two full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-01/chapter.json.whyHere.body",
    "evidence": "The three pile labels are on, ona, and ono: he, she, and leftover.",
    "fix": "Remove the colon gloss dump. Rewrite as full sentences that name and gloss each label."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-01/chapter.json.try.items[4].explanation",
    "evidence": "Pest. Dad is he.",
    "fix": "Rewrite without the slogan fragment Pest. Use a full sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-01/chapter.json.try.items[5].explanation",
    "evidence": "Pest. The car is he even though it ends in o.",
    "fix": "Rewrite without the slogan fragment Pest. Use a full sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-01/chapter.json.try.items[9].explanation",
    "evidence": "The a club. Kahvu is a later job on the same she-word.",
    "fix": "Rewrite The a club. as a full teaching sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-04/chapter.json.try.items[8].explanation",
    "evidence": "Same u. Different job on the house.",
    "fix": "Rewrite the slogan fragments as one or two full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-04/chapter.json.try.items[9].explanation",
    "evidence": "One chart. Two English uses.",
    "fix": "Rewrite the slogan fragments as full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-05/chapter.json.quiz.questions[1].explanation",
    "evidence": "Vocative. Book 1 already used that shout.",
    "fix": "Replace the label-sentence Vocative. with a full explanation sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-06/chapter.json.quiz.questions[2].explanation",
    "evidence": "Same she my. The job changed, so the matching ending changed.",
    "fix": "Rewrite Same she my. as a full sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-07/chapter.json.try.items[8].explanation",
    "evidence": "Long versus short. Same person.",
    "fix": "Rewrite both slogan fragments as full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-08/chapter.json.theme",
    "evidence": "Želim, želiš, želi. The who hangs on the end of the doing-word.",
    "fix": "Turn the opening conjugation list into a full theme sentence (or fold the examples into the second sentence)."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-09/chapter.json.theme",
    "evidence": "Eat versus eat up. Two Bosnian verbs for one English verb.",
    "fix": "Rewrite as one full theme sentence. Outline already has a cleaner model."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-09/chapter.json.try.items[9].explanation",
    "evidence": "Vid. Aspect. Eat versus eat up.",
    "fix": "Replace the three slogan fragments with full thesis/support sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-10/chapter.json.theme",
    "evidence": "Sam plus -o, -la, -lo. Gender in the past.",
    "fix": "Rewrite as one full theme sentence. Outline already has a cleaner model."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-11/chapter.json.try.items[9].explanation",
    "evidence": "Ću, naredbe, and moći / morati / trebati / htjeti.",
    "fix": "Rewrite the bare list as a full explanation sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-11/chapter.json.quiz.questions[0].explanation",
    "evidence": "Budućnost, naredbe, and the modal row.",
    "fix": "Rewrite the bare list as a full explanation sentence."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-13/chapter.json.try.items[9].explanation",
    "evidence": "Piles, jobs, matching, doing-words, and little words. No new chart.",
    "fix": "Rewrite the list fragment and slogan close as full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/chapter-13/chapter.json.quiz.questions[0].explanation",
    "evidence": "Same five shelves. No sixth system.",
    "fix": "Rewrite both slogan fragments as full sentences."
  },
  {
    "severity": "major",
    "path": "content/grammar/outline.json#chapter-4.theme",
    "evidence": "Giving, liking, and in vs into.",
    "fix": "Rewrite as a full learner-facing theme sentence (chapter.json theme is already stronger)."
  },
  {
    "severity": "major",
    "path": "content/grammar/outline.json#chapter-6.theme",
    "evidence": "Moja kahva vs moju kahvu.",
    "fix": "Rewrite as a full learner-facing theme sentence (chapter.json theme is already stronger)."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-03/chapter.json.theme",
    "evidence": "Nema kahve. English of is a separate word here.",
    "fix": "Optional polish: fold the bare Bosnian example into one full theme sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-03/chapter.json.try.items[0].explanation",
    "evidence": "Nema takes the of and none form. Kahve.",
    "fix": "Optional polish: avoid a bare Bosnian token as its own explanation sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-03/chapter.json.try.items[5].explanation",
    "evidence": "He-pile things add a here. Mosta.",
    "fix": "Optional polish: avoid a bare Bosnian token as its own explanation sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-06/chapter.json.quiz.questions[4].explanation",
    "evidence": "Wrong pile. Chapter 1 filed kahva as she.",
    "fix": "Optional polish: rewrite Wrong pile. as a full sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-09/chapter.json.try.items[0].prompt",
    "evidence": "Mid-cup. I am drinking coffee.",
    "fix": "If prompts must be full sentences, rewrite the Mid-cup. cue into the prompt sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-09/chapter.json.try.items[2].prompt",
    "evidence": "Habit. I eat bread.",
    "fix": "If prompts must be full sentences, rewrite the Habit. cue into the prompt sentence."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-10/chapter.json.try.items[0].prompt",
    "evidence": "Emir. I was in Sarajevo.",
    "fix": "If prompts must be full sentences, rewrite speaker-name cues like Emir. into a full prompt."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-10/chapter.json.try.items[2].prompt",
    "evidence": "Ana. I worked today.",
    "fix": "If prompts must be full sentences, rewrite speaker-name cues like Ana. into a full prompt."
  },
  {
    "severity": "minor",
    "path": "content/grammar/chapter-11/chapter.json.try.items[3].prompt",
    "evidence": "Polite command. Work.",
    "fix": "If prompts must be full sentences, rewrite Work. into a full English cue."
  },
  {
    "severity": "minor",
    "path": "content/grammar/outline.json#chapter-7.theme",
    "evidence": "Mene vs me. After a preposition you need the long one.",
    "fix": "Optional polish: fold the opening contrast into one full theme sentence."
  },
]

audit["issues"] = issues
audit["blockers"] = [i for i in issues if i["severity"] == "blocker"]
audit["blockerCount"] = len(audit["blockers"])
audit["majorCount"] = sum(1 for i in issues if i["severity"] == "major")
audit["minorCount"] = sum(1 for i in issues if i["severity"] == "minor")

out = Path("exports/grammar-copy-reaudit.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out)
print("counts", audit["blockerCount"], audit["majorCount"], audit["minorCount"], "issues", len(issues))
print(json.dumps(audit, ensure_ascii=False))
