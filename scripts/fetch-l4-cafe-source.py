#!/usr/bin/env python3
"""Download candidate source photos for Lesson 4 café-family hero."""
from __future__ import annotations

import time
import urllib.parse
import urllib.request
from pathlib import Path

TMP = Path(__file__).resolve().parents[1] / "scripts" / "_tmp_sources"
UA = "LearnBosnianBot/1.0"

CANDIDATES = [
    "File:Café_House_at_Bascarsija.jpg",
    "File:Early_Morning_in_Bascarsija_(54564806901).jpg",
    "File:Morića_Han_(1).JPG",
    "File:Zlatna_Ribica_(116653269).jpeg",
    "File:Giannini_Cafe_-_panoramio.jpg",
    "File:Restaurant_with_Cool_Decor,_Sarajevo,_Bosnia_(3802594664).jpg",
]


def download(title: str) -> Path:
    slug = title.replace("File:", "").replace("/", "_")[:60]
    out = TMP / f"l4cafe-{slug}.jpg"
    if out.exists():
        return out
    path = urllib.parse.quote(title.replace("File:", ""), safe="(),._-")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    out.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return out


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    for title in CANDIDATES:
        try:
            time.sleep(2)
            out = download(title)
            print(out.name, out.stat().st_size)
        except Exception as exc:
            print("FAIL", title, exc)


if __name__ == "__main__":
    main()
