# -*- coding: utf-8 -*-
import json, glob
for f in sorted(glob.glob("content/grammar/chapter-*/chapter.json")):
    d=json.load(open(f,encoding="utf-8"))
    print(f"=== ch{d['chapter']:02d} captions/alt ===")
    for i,img in enumerate(d.get("images") or []):
        print(f"  [{i}] caption: {img.get('grammarCaption')}")
        print(f"       alt: {img.get('alt')}")
