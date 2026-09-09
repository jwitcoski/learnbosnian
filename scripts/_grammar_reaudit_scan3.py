# -*- coding: utf-8 -*-
import json, re, glob, os

CYR = re.compile(r"[\u0400-\u04FF]")
DASHES = re.compile(r"[\u2012\u2013\u2014\u2015]")

paths_checked = []
all_texts = []  # (path, kind, text)

def collect(path, kind, text):
    if isinstance(text, str) and text.strip():
        all_texts.append((path, kind, text))

files = sorted(glob.glob("content/grammar/chapter-*/chapter.json"))
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    base = f.replace("\\", "/")
    paths_checked.append(data["chapter"])
    for k in ("title", "titleEn", "theme"):
        collect(f"{base}.{k}", "meta", data.get(k))
    for block in ("whyHere", "englishLies", "knownLine", "pattern", "howYouGuess", "trick", "nerd"):
        obj = data.get(block) or {}
        collect(f"{base}.{block}.heading", "heading", obj.get("heading"))
        collect(f"{base}.{block}.body", "teaching", obj.get("body"))
        if block == "knownLine":
            collect(f"{base}.knownLine.bosnian", "bosnian", obj.get("bosnian"))
            collect(f"{base}.knownLine.english", "english_line", obj.get("english"))
            collect(f"{base}.knownLine.speaker", "speaker", obj.get("speaker"))
        table = obj.get("table")
        if isinstance(table, dict):
            for i,h in enumerate(table.get("headers") or []):
                collect(f"{base}.{block}.table.headers[{i}]", "table", h)
            for ri,row in enumerate(table.get("rows") or []):
                if isinstance(row, list):
                    for ci,cell in enumerate(row):
                        collect(f"{base}.{block}.table.rows[{ri}][{ci}]", "table", cell)
    for i, card in enumerate(data.get("vocabulary") or []):
        collect(f"{base}.vocabulary[{i}].english", "vocab_en", card.get("english"))
        collect(f"{base}.vocabulary[{i}].bosnian", "bosnian", card.get("bosnian"))
        collect(f"{base}.vocabulary[{i}].example", "vocab_ex", card.get("example"))
    look = data.get("look") or {}
    for i, item in enumerate(look.get("items") or []):
        collect(f"{base}.look.items[{i}].speaker", "speaker", item.get("speaker"))
        collect(f"{base}.look.items[{i}].bosnian", "bosnian", item.get("bosnian"))
        collect(f"{base}.look.items[{i}].english", "look_en", item.get("english"))
    tr = data.get("try") or {}
    for i, item in enumerate(tr.get("items") or []):
        collect(f"{base}.try.items[{i}].prompt", "try_prompt", item.get("prompt"))
        for oi, opt in enumerate(item.get("options") or []):
            collect(f"{base}.try.items[{i}].options[{oi}]", "option", opt)
        collect(f"{base}.try.items[{i}].explanation", "try_expl", item.get("explanation"))
    quiz = data.get("quiz") or {}
    collect(f"{base}.quiz.title", "heading", quiz.get("title"))
    for i, q in enumerate(quiz.get("questions") or []):
        collect(f"{base}.quiz.questions[{i}].question", "quiz_q", q.get("question"))
        for oi, opt in enumerate(q.get("options") or []):
            collect(f"{base}.quiz.questions[{i}].options[{oi}]", "option", opt)
        collect(f"{base}.quiz.questions[{i}].explanation", "quiz_expl", q.get("explanation"))
    nxt = data.get("next") or {}
    collect(f"{base}.next.body", "teaching", nxt.get("body"))
    for i, img in enumerate(data.get("images") or []):
        collect(f"{base}.images[{i}].grammarCaption", "caption", img.get("grammarCaption"))
        collect(f"{base}.images[{i}].alt", "alt", img.get("alt"))

outline = json.load(open("content/grammar/outline.json", encoding="utf-8"))
collect("content/grammar/outline.json.title", "meta", outline.get("title"))
collect("content/grammar/outline.json.summary", "teaching", outline.get("summary"))
for c in outline.get("chapters", []):
    p = f"content/grammar/outline.json#chapter-{c['chapter']}"
    for k in ("title", "titleEn", "theme"):
        collect(f"{p}.{k}", "meta", c.get(k))
for part in outline.get("parts", []):
    p = f"content/grammar/outline.json#part-{part['part']}"
    for k in ("title", "focus"):
        collect(f"{p}.{k}", "meta", part.get(k))

# Mechanical precise report
mech = []
for path, kind, text in all_texts:
    if kind == "speaker":
        if text not in ("Ana", "Emir", "Amira"):
            mech.append(("blocker", path, text, "Speaker must be Ana/Emir/Amira"))
        continue
    if CYR.search(text):
        mech.append(("blocker", path, text, "Cyrillic"))
    if DASHES.search(text):
        mech.append(("blocker", path, text, "em/en dash"))
    if ";" in text and kind not in ("bosnian",):  # semicolons bad in learner English; bosnian unlikely
        mech.append(("blocker", path, text, "semicolon"))
    if "Mrvica" in text:
        mech.append(("blocker", path, text, "Mrvica"))
    if re.search(r"\bLesson\s+(?:[0-9]+|[AB])\b|\bDay\s+\d+\b|\bWeek\s+\d+\b|\bSedmica\b", text, re.I):
        mech.append(("blocker", path, text, "Lesson/Day/Week naming"))
    if re.search(r"\b(AWS|Transcribe|tap the|click the)\b", text, re.I):
        mech.append(("major", path, text, "UI/AWS jargon"))
    if re.search(r"\bBiH\b", text) and kind not in ("bosnian",):
        mech.append(("major", path, text, "unexplained BiH"))
    if ":" in text and kind in ("teaching", "try_expl", "quiz_expl", "caption", "try_prompt", "quiz_q", "look_en", "english_line", "vocab_en", "theme"):
        mech.append(("colon", path, text, "colon in learner sentence"))

print("TEXTS", len(all_texts))
print("MECH", len(mech))
for m in mech:
    print(m[0], m[1], "=>", m[3], "|", m[2][:160].replace("\n"," "))

# Write teaching bodies + explanations for human review
lines = []
for path, kind, text in all_texts:
    if kind in ("teaching", "try_expl", "quiz_expl", "caption", "try_prompt", "quiz_q", "theme", "meta"):
        lines.append(f"### {path} [{kind}]\n{text}\n")
open("exports/_reaudit_texts.md", "w", encoding="utf-8").write("\n".join(lines))
print("wrote exports/_reaudit_texts.md", "chars", sum(len(t) for _,_,t in all_texts))

# Missing speakers?
missing_sp = []
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    base = f.replace("\\", "/")
    kl = data.get("knownLine") or {}
    if not kl.get("speaker"):
        missing_sp.append(f"{base}.knownLine")
    for i, item in enumerate((data.get("look") or {}).get("items") or []):
        if not item.get("speaker"):
            missing_sp.append(f"{base}.look.items[{i}]")
print("MISSING_SPEAKERS", missing_sp)

# Count look items speakers
from collections import Counter
spcount = Counter()
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    spcount[data.get("knownLine",{}).get("speaker")] += 1
    for item in (data.get("look") or {}).get("items") or []:
        spcount[item.get("speaker")] += 1
print("SPEAKER_DIST", dict(spcount))
