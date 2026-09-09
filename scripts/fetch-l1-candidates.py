#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

TMP = Path(__file__).resolve().parents[1] / "scripts" / "_tmp_sources"
UA = "LearnBosnianBot/1.0"

CANDIDATES = [
    "File:Sarajevo_Ferhadija_2007-08-16.jpg",
    "File:Ba\u0161\u010dar\u0161ija_(6086230081).jpg",
    "File:Ba\u0161\u010dar\u0161ija_square.jpg",
    "File:Boza_and_Boem_\u0161nita_in_Sarajevo.JPG",
    "File:Restaurant_with_Cool_Decor,_Sarajevo,_Bosnia_(3802594664).jpg",
]


def commons_url(title: str) -> str:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }
    )
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": UA}
    )
    data = json.loads(urllib.request.urlopen(req, timeout=60).read())
    page = next(iter(data["query"]["pages"].values()))
    return page["imageinfo"][0]["url"].split("?")[0]


def slug(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", title.replace("File:", ""))


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    for title in CANDIDATES:
        url = commons_url(title)
        out = TMP / f"cand-{slug(title)}"
        if not out.exists():
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            out.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        im = Image.open(out)
        print(f"{out.name}\t{im.size}\t{title}")


if __name__ == "__main__":
    main()
