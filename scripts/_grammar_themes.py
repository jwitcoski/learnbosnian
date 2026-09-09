# -*- coding: utf-8 -*-
import json, glob

def has_tiny(ex):
    parts = [p.strip() for p in ex.replace("!", ".").replace("?", ".").split(".") if p.strip()]
    return any(len(p.split()) <= 3 for p in parts)

print("=== CHAPTER THEMES ===")
for f in sorted(glob.glob("content/grammar/chapter-*/chapter.json")):
    d = json.load(open(f, encoding="utf-8"))
    print(f"ch{d['chapter']:02d}: {d.get('theme')}")
print("\n=== OUTLINE THEMES ===")
o = json.load(open("content/grammar/outline.json", encoding="utf-8"))
for c in o["chapters"]:
    print(f"ch{c['chapter']:02d}: {c.get('theme')}")
print("\n=== NEXT BODIES ===")
for f in sorted(glob.glob("content/grammar/chapter-*/chapter.json")):
    d = json.load(open(f, encoding="utf-8"))
    print(f"ch{d['chapter']:02d}: {(d.get('next') or {}).get('body')}")
print("\n=== SHORT / TINY-SENTENCE EXPLANATIONS ===")
for f in sorted(glob.glob("content/grammar/chapter-*/chapter.json")):
    d = json.load(open(f, encoding="utf-8"))
    for i, item in enumerate((d.get("try") or {}).get("items") or []):
        ex = item.get("explanation") or ""
        if len(ex) < 70 or has_tiny(ex):
            print(f"ch{d['chapter']:02d} try[{i}] ({len(ex)}): {ex}")
    for i, q in enumerate((d.get("quiz") or {}).get("questions") or []):
        ex = q.get("explanation") or ""
        if len(ex) < 70 or has_tiny(ex):
            print(f"ch{d['chapter']:02d} quiz[{i}] ({len(ex)}): {ex}")
