# -*- coding: utf-8 -*-
import json, re, glob
from collections import Counter

CYR = re.compile(r"[\u0400-\u04FF]")
DASHES = re.compile(r"[\u2012\u2013\u2014\u2015]")
BAN_MARKETING = re.compile(
    r"\b(unlock|journey|dive in|let'?s explore|it'?s important to note|robust|leverage|framework|mental model|you'?ve got this|great job noticing|by the end of this chapter|you will be able to|can-do)\b",
    re.I,
)
BAN_LESSON = re.compile(r"\b(Lesson|Day|Week|Sedmica)\s*\d|\bLesson\s+[A-B]\b|\bDay\s+\d|\bWeek\s+\d", re.I)
BAN_MRVICA = re.compile(r"\bMrvica\b", re.I)
BAN_UI = re.compile(r"\b(tap the|click the|AWS|Transcribe)\b", re.I)
BAN_BIH = re.compile(r"\bBiH\b")

issues = []

def add(sev, path, evidence, fix):
    issues.append({
        "severity": sev,
        "path": path,
        "evidence": (evidence or "")[:320],
        "fix": fix,
    })

def check_text(path, text, *, bosnian_ok=False):
    if not isinstance(text, str) or not text.strip():
        return
    if CYR.search(text):
        m = CYR.search(text)
        snippet = text[max(0, m.start() - 20) : m.end() + 20]
        add("blocker", path, f"Cyrillic near: ...{snippet}...", "Replace with Latin script only")
    if DASHES.search(text):
        add("blocker", path, text.strip()[:220], "Replace em/en dash with period, comma, or parentheses")
    if ";" in text:
        add("blocker", path, text.strip()[:220], "Remove semicolon; split into sentences")
    if ":" in text:
        add("major", path, text.strip()[:240], "Remove colon from learner-facing sentence; rewrite as full sentences")
    if BAN_LESSON.search(text):
        add("blocker", path, text.strip()[:220], "Use Chapter N naming, not Lesson/Day/Week/Sedmica")
    if BAN_MRVICA.search(text):
        add("blocker", path, text.strip()[:220], "Remove Mrvica/cat plot from grammar handbook")
    if BAN_UI.search(text):
        add("major", path, text.strip()[:220], "Remove website UI / AWS jargon; keep book-safe")
    if BAN_MARKETING.search(text):
        add("major", path, text.strip()[:220], "Remove banned marketing / startup voice")
    if BAN_BIH.search(text) and not bosnian_ok:
        if re.search(r"\b(the|and|of|is|in|for|to|a|an)\b", text, re.I):
            add("major", path, text.strip()[:220], "Spell out Bosnia and Herzegovina or say Bosnian; do not use unexplained BiH")

def walk(obj, path):
    if isinstance(obj, dict):
        key = path.split(".")[-1].split("[")[0] if path else ""
        if key == "knownLine":
            speaker = obj.get("speaker")
            if not speaker:
                add("blocker", path + ".speaker", json.dumps(obj, ensure_ascii=False)[:200], "Add speaker Ana/Emir/Amira")
            elif speaker not in ("Ana", "Emir", "Amira"):
                add("blocker", path + ".speaker", str(speaker), "Speaker must be Ana, Emir, or Amira")
            for k, v in obj.items():
                if k == "speaker":
                    continue
                if k in ("bs", "text", "line") and isinstance(v, str):
                    check_text(f"{path}.{k}", v, bosnian_ok=True)
                elif isinstance(v, str):
                    check_text(f"{path}.{k}", v)
                elif isinstance(v, (dict, list)):
                    walk(v, f"{path}.{k}")
            return
        if key == "look" and "items" in obj:
            for i, item in enumerate(obj.get("items") or []):
                ip = f"{path}.items[{i}]"
                if isinstance(item, dict):
                    if not item.get("speaker"):
                        add("blocker", ip + ".speaker", json.dumps(item, ensure_ascii=False)[:200], "Add speaker Ana/Emir/Amira on every look line")
                    elif item.get("speaker") not in ("Ana", "Emir", "Amira"):
                        add("blocker", ip + ".speaker", str(item.get("speaker")), "Speaker must be Ana, Emir, or Amira")
                    for k, v in item.items():
                        if k == "speaker":
                            continue
                        if k in ("bs", "text", "line") and isinstance(v, str):
                            check_text(f"{ip}.{k}", v, bosnian_ok=True)
                        elif isinstance(v, str):
                            check_text(f"{ip}.{k}", v)
                        elif isinstance(v, (dict, list)):
                            walk(v, f"{ip}.{k}")
                elif isinstance(item, str):
                    check_text(ip, item)
            for k, v in obj.items():
                if k == "items":
                    continue
                walk(v, f"{path}.{k}")
            return
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if k in (
                "license", "sourceUrl", "pageUrl", "localPath", "author", "credit", "url",
                "audioUrl", "reviewedAt", "reviewerNotes", "status", "kind", "speakTargets",
                "correctIndex", "skill", "id", "ref", "imagesNeeded", "imageSlots", "speaker",
                "estimatedMinutes", "chapter",
            ):
                continue
            if k == "vocabulary" and isinstance(v, list):
                for i, card in enumerate(v):
                    if isinstance(card, dict):
                        for gk in ("en", "english", "gloss", "translation"):
                            if gk in card and isinstance(card[gk], str):
                                check_text(f"{p}[{i}].{gk}", card[gk])
                        for gk in ("bs", "word", "lemma"):
                            if gk in card and isinstance(card[gk], str) and CYR.search(card[gk]):
                                add("blocker", f"{p}[{i}].{gk}", card[gk], "Latin only")
                continue
            if k == "images" and isinstance(v, list):
                for i, img in enumerate(v):
                    if isinstance(img, dict) and isinstance(img.get("caption"), str):
                        check_text(f"{p}[{i}].caption", img["caption"])
                continue
            if isinstance(v, str):
                if k in (
                    "title", "titleEn", "theme", "whyHere", "englishLies", "pattern",
                    "howYouGuess", "trick", "next", "body", "prompt", "caption",
                    "explanation", "question", "q", "hint", "summary", "whyLikeThis",
                    "en", "english", "translation", "gloss", "text", "pests",
                ):
                    check_text(p, v, bosnian_ok=(k in ("bs", "text", "line") and "vocabulary" not in path))
                elif k in ("bs", "line"):
                    check_text(p, v, bosnian_ok=True)
            elif isinstance(v, (dict, list)):
                walk(v, p)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            # pests as string list
            if isinstance(item, str):
                # only if parent suggests learner text
                parent = path.split(".")[-1].split("[")[0]
                if parent in ("pests", "options", "try", "tryThese", "items"):
                    check_text(f"{path}[{i}]", item)
                elif parent in ("quiz",):
                    check_text(f"{path}[{i}]", item)
            else:
                walk(item, f"{path}[{i}]")

files = sorted(glob.glob("content/grammar/chapter-*/chapter.json"))
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    ch = data.get("chapter")
    base = f"content/grammar/chapter-{int(ch):02d}/chapter.json"
    walk(data, base)
    # pests may be list of strings under howYouGuess or top-level
    # also check howYouGuess if object
    hyg = data.get("howYouGuess")
    if isinstance(hyg, dict) and "pests" in hyg:
        for i, pest in enumerate(hyg["pests"] if isinstance(hyg["pests"], list) else []):
            if isinstance(pest, str):
                check_text(f"{base}.howYouGuess.pests[{i}]", pest)
            elif isinstance(pest, dict):
                walk(pest, f"{base}.howYouGuess.pests[{i}]")

outline = json.load(open("content/grammar/outline.json", encoding="utf-8"))
for c in outline.get("chapters", []):
    p = f"content/grammar/outline.json#chapter-{c.get('chapter')}"
    for k in ("title", "titleEn", "theme"):
        if k in c:
            check_text(f"{p}.{k}", c[k])
for k in ("title", "summary", "pedagogy", "titleBs"):
    if k in outline:
        check_text(f"content/grammar/outline.json.{k}", outline[k], bosnian_ok=(k == "titleBs"))
for part in outline.get("parts", []):
    for k in ("title", "focus"):
        if k in part:
            check_text(f"content/grammar/outline.json#part-{part.get('part')}.{k}", part[k])

print("TOTAL", len(issues))
print("BY_SEV", dict(Counter(i["severity"] for i in issues)))
noncolon = [i for i in issues if "Remove colon" not in i["fix"]]
colon = [i for i in issues if "Remove colon" in i["fix"]]
print("NONCOLON", len(noncolon))
print("COLON", len(colon))
out = {"noncolon": noncolon, "colon": colon}
json.dump(out, open("exports/_reaudit_raw_scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote exports/_reaudit_raw_scan.json")
for i in noncolon:
    print(json.dumps(i, ensure_ascii=False))
