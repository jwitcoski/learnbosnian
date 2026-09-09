# -*- coding: utf-8 -*-
import json, glob, re
from pathlib import Path

# Print structure of ch00, ch01, ch06, ch07
for n in [0,1,6,7,13]:
    data = json.load(open(f"content/grammar/chapter-{n:02d}/chapter.json", encoding="utf-8"))
    print("="*60, f"CHAPTER {n}")
    for k,v in data.items():
        t = type(v).__name__
        if isinstance(v, str):
            print(f"  {k}: str[{len(v)}] {v[:80]!r}")
        elif isinstance(v, dict):
            print(f"  {k}: dict keys={list(v.keys())}")
            for kk,vv in v.items():
                if isinstance(vv, str):
                    print(f"    .{kk}: str[{len(vv)}] {vv[:100]!r}")
                elif isinstance(vv, list):
                    print(f"    .{kk}: list[{len(vv)}] sample={type(vv[0]).__name__ if vv else None}")
                    if vv and isinstance(vv[0], dict):
                        print(f"      item0 keys={list(vv[0].keys())}")
                elif isinstance(vv, dict):
                    print(f"    .{kk}: dict keys={list(vv.keys())}")
                else:
                    print(f"    .{kk}: {type(vv).__name__}={vv!r}"[:120])
        elif isinstance(v, list):
            print(f"  {k}: list[{len(v)}]")
            if v and isinstance(v[0], dict):
                print(f"    item0 keys={list(v[0].keys())}")
        else:
            print(f"  {k}: {t}={v!r}")
