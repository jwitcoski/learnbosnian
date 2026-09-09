# -*- coding: utf-8 -*-
import json, re, glob
from collections import Counter, defaultdict

CYR = re.compile(r"[\u0400-\u04FF]")
DASHES = re.compile(r"[\u2012\u2013\u2014\u2015]")
# also ASCII hyphen used as em-dash surrogate between clauses? only flag spaced " - " maybe later
BAN_MARKETING = re.compile(
    r"\b(unlock|journey|dive in|let'?s explore|it'?s important to note|robust|leverage|framework|mental model|you'?ve got this|great job noticing|by the end of this chapter|you will be able to|can-do|objective)\b",
    re.I,
)
BAN_LESSON = re.compile(r"\bLesson\s+(?:[0-9]+|[AB])\b|\bDay\s+\d+\b|\bWeek\s+\d+\b|\bSedmica\b", re.I)
BAN_MRVICA = re.compile(r"\bMrvica\b", re.I)
BAN_UI = re.compile(r"\b(tap the|click the|AWS|Transcribe)\b", re.I)
BAN_BIH = re.compile(r"\bBiH\b")
# fragment heuristic: short sentence without verb-ish words, or slogan list
VERBISH = re.compile(r"\b(is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|can|could|should|must|may|might|need|needs|means|mean|say|says|said|learn|learns|use|uses|keep|keeps|show|shows|file|files|dress|dresses|pick|picks|want|wants|live|lives|sit|sits|take|takes|give|gives|call|calls|put|puts|come|comes|go|goes|work|works|hear|hears|see|sees|know|knows|teach|teaches|refuse|refuses|force|forces|stay|stays|become|becomes|open|opens|walk|walks|hang|hangs|ride|rides|match|matches|park|parks|lean|leans|stand|stands|follow|follows|name|names|ignore|ignores|prove|proves|trip|trips|treat|treats|invent|invents|ask|asks|broke|broken)\b", re.I)

issues = []

def add(sev, path, evidence, fix):
    issues.append({
        "severity": sev,
        "path": path,
        "evidence": (evidence or "").replace("\n", " ")[:360],
        "fix": fix,
    })

def check_text(path, text, *, bosnian_ok=False, is_heading=False, is_option=False, is_table_cell=False):
    if not isinstance(text, str) or not text.strip():
        return
    t = text.strip()
    if CYR.search(t):
        m = CYR.search(t)
        snippet = t[max(0, m.start() - 20) : m.end() + 20]
        add("blocker", path, f"Cyrillic near: ...{snippet}...", "Replace with Latin script only")
    if DASHES.search(t):
        add("blocker", path, t[:240], "Replace em/en dash with period, comma, or parentheses")
    if ";" in t:
        add("blocker", path, t[:240], "Remove semicolon; split into sentences")
    # colon ban for learner-facing sentences (not table headers necessarily - still learner facing)
    if ":" in t and not is_heading:
        # allow ratio times? still ban per guide
        add("major", path, t[:260], "Remove colon from learner-facing sentence; rewrite as full sentences")
    if BAN_LESSON.search(t):
        add("blocker", path, t[:240], "Use Chapter N naming, not Lesson/Day/Week/Sedmica")
    if BAN_MRVICA.search(t):
        add("blocker", path, t[:240], "Remove Mrvica/cat plot from grammar handbook")
    if BAN_UI.search(t):
        add("major", path, t[:240], "Remove website UI / AWS jargon; keep book-safe")
    if BAN_MARKETING.search(t):
        add("major", path, t[:240], "Remove banned marketing / startup voice")
    if BAN_BIH.search(t) and not bosnian_ok:
        # English learner text
        if re.search(r"[A-Za-z]{3,}", t) and not bosnian_ok:
            # if it's an English gloss/prose field
            add("major", path, t[:240], "Spell out Bosnia and Herzegovina or say Bosnian; do not use unexplained BiH")
    # fragment check for teaching bodies (not options/table/headings/bosnian)
    if not (is_heading or is_option or is_table_cell or bosnian_ok):
        # split sentences
        parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", t) if p.strip()]
        # flag if many ultra-short slogan fragments
        slogans = []
        for p in parts:
            words = re.findall(r"[A-Za-z']+", p)
            if len(words) <= 5 and not VERBISH.search(p) and not p.endswith("?"):
                # might be fragment
                if p[0].isupper() and not p.endswith(".") and len(words) >= 2:
                    slogans.append(p)
            # phrase fragments punctuated as sentences: no verb
            if p.endswith(".") and len(words) <= 8 and not VERBISH.search(p) and not re.search(r"[žćčšđŽĆČŠĐ]", p):
                # English-looking fragment
                if words and words[0][0].isupper():
                    slogans.append(p)
        if len(slogans) >= 2:
            add("major", path, "Fragment slogans: " + " | ".join(slogans[:4]), "Rewrite as full thesis/support/summary sentences")

def audit_chapter(path, data):
    base = path.replace("\\", "/")
    # titles
    for k in ("title", "titleEn", "theme"):
        if isinstance(data.get(k), str):
            check_text(f"{base}.{k}", data[k], bosnian_ok=(k == "title"))
    # teaching blocks
    for block in ("whyHere", "englishLies", "knownLine", "pattern", "howYouGuess", "trick", "nerd"):
        obj = data.get(block)
        if not isinstance(obj, dict):
            continue
        if isinstance(obj.get("heading"), str):
            check_text(f"{base}.{block}.heading", obj["heading"], is_heading=True)
        if isinstance(obj.get("body"), str):
            check_text(f"{base}.{block}.body", obj["body"])
        if block == "knownLine":
            sp = obj.get("speaker")
            if not sp:
                add("blocker", f"{base}.knownLine.speaker", json.dumps(obj, ensure_ascii=False)[:200], "Add speaker Ana/Emir/Amira")
            elif sp not in ("Ana", "Emir", "Amira"):
                add("blocker", f"{base}.knownLine.speaker", str(sp), "Speaker must be Ana, Emir, or Amira")
            if isinstance(obj.get("bosnian"), str):
                check_text(f"{base}.knownLine.bosnian", obj["bosnian"], bosnian_ok=True)
            if isinstance(obj.get("english"), str):
                check_text(f"{base}.knownLine.english", obj["english"])
        # tables
        table = obj.get("table")
        if isinstance(table, dict):
            for i, h in enumerate(table.get("headers") or []):
                if isinstance(h, str):
                    check_text(f"{base}.{block}.table.headers[{i}]", h, is_table_cell=True)
            for ri, row in enumerate(table.get("rows") or []):
                if isinstance(row, list):
                    for ci, cell in enumerate(row):
                        if isinstance(cell, str):
                            check_text(f"{base}.{block}.table.rows[{ri}][{ci}]", cell, is_table_cell=True)
                elif isinstance(row, dict):
                    for ck, cv in row.items():
                        if isinstance(cv, str):
                            check_text(f"{base}.{block}.table.rows[{ri}].{ck}", cv, is_table_cell=True)
    # vocabulary english
    for i, card in enumerate(data.get("vocabulary") or []):
        if not isinstance(card, dict):
            continue
        if isinstance(card.get("english"), str):
            check_text(f"{base}.vocabulary[{i}].english", card["english"])
        if isinstance(card.get("bosnian"), str):
            check_text(f"{base}.vocabulary[{i}].bosnian", card["bosnian"], bosnian_ok=True)
        if isinstance(card.get("example"), str):
            # example may be Bosnian or mixed - check cyrillic/dashes/semi
            check_text(f"{base}.vocabulary[{i}].example", card["example"], bosnian_ok=True)
        if isinstance(card.get("pronunciation"), str):
            check_text(f"{base}.vocabulary[{i}].pronunciation", card["pronunciation"])
    # look items
    look = data.get("look") or {}
    if isinstance(look.get("heading"), str):
        check_text(f"{base}.look.heading", look["heading"], is_heading=True)
    for i, item in enumerate(look.get("items") or []):
        if not isinstance(item, dict):
            continue
        sp = item.get("speaker")
        if not sp:
            add("blocker", f"{base}.look.items[{i}].speaker", json.dumps(item, ensure_ascii=False)[:200], "Add speaker Ana/Emir/Amira on every look line")
        elif sp not in ("Ana", "Emir", "Amira"):
            add("blocker", f"{base}.look.items[{i}].speaker", str(sp), "Speaker must be Ana, Emir, or Amira")
        if isinstance(item.get("bosnian"), str):
            check_text(f"{base}.look.items[{i}].bosnian", item["bosnian"], bosnian_ok=True)
        if isinstance(item.get("english"), str):
            check_text(f"{base}.look.items[{i}].english", item["english"])
    # try
    tr = data.get("try") or {}
    if isinstance(tr.get("heading"), str):
        check_text(f"{base}.try.heading", tr["heading"], is_heading=True)
    for i, item in enumerate(tr.get("items") or []):
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("prompt"), str):
            check_text(f"{base}.try.items[{i}].prompt", item["prompt"])
        for oi, opt in enumerate(item.get("options") or []):
            if isinstance(opt, str):
                check_text(f"{base}.try.items[{i}].options[{oi}]", opt, is_option=True)
        if isinstance(item.get("explanation"), str):
            check_text(f"{base}.try.items[{i}].explanation", item["explanation"])
    # quiz
    quiz = data.get("quiz") or {}
    if isinstance(quiz.get("title"), str):
        check_text(f"{base}.quiz.title", quiz["title"], is_heading=True)
    for i, q in enumerate(quiz.get("questions") or []):
        if not isinstance(q, dict):
            continue
        if isinstance(q.get("question"), str):
            check_text(f"{base}.quiz.questions[{i}].question", q["question"])
        for oi, opt in enumerate(q.get("options") or []):
            if isinstance(opt, str):
                check_text(f"{base}.quiz.questions[{i}].options[{oi}]", opt, is_option=True)
        if isinstance(q.get("explanation"), str):
            check_text(f"{base}.quiz.questions[{i}].explanation", q["explanation"])
    # next
    nxt = data.get("next")
    if isinstance(nxt, dict) and isinstance(nxt.get("body"), str):
        check_text(f"{base}.next.body", nxt["body"])
    elif isinstance(nxt, str):
        check_text(f"{base}.next", nxt)
    # images captions + alt (alt is learner-ish / a11y - include grammarCaption; alt maybe)
    for i, img in enumerate(data.get("images") or []):
        if not isinstance(img, dict):
            continue
        if isinstance(img.get("grammarCaption"), str):
            check_text(f"{base}.images[{i}].grammarCaption", img["grammarCaption"])
        if isinstance(img.get("alt"), str):
            check_text(f"{base}.images[{i}].alt", img["alt"])
        # credit often has structural info - skip per user (licenses/URLs). credit line might be learner facing with G.0a
        if isinstance(img.get("credit"), str):
            # only flag dashes/semi/cyrillic/mrvica, not colon in Photo: style? credit may have colons - user said skip licenses; credit is attribution. Skip credit to avoid noise.
            pass

files = sorted(glob.glob("content/grammar/chapter-*/chapter.json"))
covered = []
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    covered.append(data.get("chapter"))
    audit_chapter(f, data)

# outline learner-facing themes/titles only
outline = json.load(open("content/grammar/outline.json", encoding="utf-8"))
for c in outline.get("chapters", []):
    p = f"content/grammar/outline.json#chapter-{c.get('chapter')}"
    for k in ("title", "titleEn", "theme"):
        if isinstance(c.get(k), str):
            check_text(f"{p}.{k}", c[k], bosnian_ok=(k == "title"))
if isinstance(outline.get("title"), str):
    check_text("content/grammar/outline.json.title", outline["title"])
# summary may be learner-facing book blurb
if isinstance(outline.get("summary"), str):
    check_text("content/grammar/outline.json.summary", outline["summary"])
for part in outline.get("parts", []):
    p = f"content/grammar/outline.json#part-{part.get('part')}"
    for k in ("title", "focus"):
        if isinstance(part.get(k), str):
            check_text(f"{p}.{k}", part[k])

# dump all teaching bodies for manual fragment/colon review
bodies = []
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    ch = data["chapter"]
    for block in ("whyHere", "englishLies", "knownLine", "pattern", "howYouGuess", "trick", "nerd"):
        obj = data.get(block) or {}
        if isinstance(obj.get("body"), str):
            bodies.append({"ch": ch, "block": block, "body": obj["body"]})
    if isinstance((data.get("next") or {}).get("body"), str):
        bodies.append({"ch": ch, "block": "next", "body": data["next"]["body"]})
    for i, img in enumerate(data.get("images") or []):
        if img.get("grammarCaption"):
            bodies.append({"ch": ch, "block": f"images[{i}].grammarCaption", "body": img["grammarCaption"]})

json.dump({"issues": issues, "bodies": bodies, "covered": covered}, open("exports/_reaudit_raw_scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("TOTAL", len(issues))
print("BY_SEV", dict(Counter(i["severity"] for i in issues)))
print("COVERED", covered)
for i in issues:
    print(json.dumps(i, ensure_ascii=False))
