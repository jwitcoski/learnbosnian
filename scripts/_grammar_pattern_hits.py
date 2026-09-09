# -*- coding: utf-8 -*-
import json, re, glob

# Broad search across all string values in learner paths
PATTERNS = {
    "emdash": re.compile(r"[\u2012\u2013\u2014\u2015]"),
    "semicolon": re.compile(r";"),
    "mrvica": re.compile(r"Mrvica", re.I),
    "lesson_name": re.compile(r"\b(Lesson\s+(?:[0-9]+|[AB])|Day\s+\d+|Week\s+\d+|Sedmica)\b", re.I),
    "aws": re.compile(r"\b(AWS|Transcribe|tap the accent|click the)\b", re.I),
    "marketing": re.compile(r"\b(unlock|journey|dive in|let'?s explore|it'?s important to note|robust|leverage|framework|mental model|you'?ve got this|great job noticing|by the end of this chapter|you will be able to|English speakers often struggle)\b", re.I),
    "bih": re.compile(r"\bBiH\b"),
    "civic": re.compile(r"\b(Dayton|High Representative|civic|Presidency)\b", re.I),
    "cyrillic": re.compile(r"[\u0400-\u04FF]"),
    "other_cast": re.compile(r"\b(Marko|Jelena|Mirza|Sara|Maja|Ibrahim|Lejla)\b"),
}

hits = {k: [] for k in PATTERNS}

def walk_strings(obj, path, callback):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k in ("license","sourceUrl","pageUrl","localPath","author","credit","url","audioUrl","reviewedAt","reviewerNotes","status","kind","speakTargets","correctIndex","skill","id","ref","imagesNeeded","imageSlots","estimatedMinutes","chapter","pronunciation","partOfSpeech"):
                # still scan reviewerNotes? no skip
                if k == "reviewerNotes":
                    continue
                if k in ("license","sourceUrl","pageUrl","localPath","author","credit","url","audioUrl","reviewedAt","status","kind","speakTargets","correctIndex","skill","id","ref","imagesNeeded","imageSlots","estimatedMinutes","chapter"):
                    continue
            walk_strings(v, f"{path}.{k}", callback)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk_strings(v, f"{path}[{i}]", callback)
    elif isinstance(obj, str):
        callback(path, obj)

for f in sorted(glob.glob("content/grammar/chapter-*/chapter.json")):
    data = json.load(open(f, encoding="utf-8"))
    def cb(path, text):
        for name, pat in PATTERNS.items():
            if pat.search(text):
                hits[name].append((path, text[:180]))
    walk_strings(data, f.replace("\\","/"), cb)

# outline learner skim
outline = json.load(open("content/grammar/outline.json", encoding="utf-8"))
def cb2(path, text):
    for name, pat in PATTERNS.items():
        if name in ("civic",): continue
        if pat.search(text):
            hits[name].append((path, text[:180]))
walk_strings({k: outline[k] for k in outline if k in ("title","summary","chapters","parts")}, "content/grammar/outline.json", cb2)

for name, lst in hits.items():
    print(f"\n## {name} ({len(lst)})")
    for p,t in lst[:30]:
        print(p, "|", t.replace("\n"," "))
