#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "scripts" / "_tmp_sources"
UA = "LearnBosnianBot/1.0"

SOURCES = [
    {
        "tmp": "l2-bascarsija-crowd-src.jpg",
        "commons": "File:Ba\u0161\u010dar\u0161ija_(6086230081).jpg",
    },
    {
        "tmp": "l2-sebilj-tourists-src.jpg",
        "commons": "File:Sarajevo_-_Sebilj_fountain.jpg",
    },
    {
        "tmp": "l2-ferhadija-cafe-src.jpg",
        "commons": "File:Sarajevo_Ferhadija_2007-08-16.jpg",
    },
]


def commons_info(title: str) -> dict:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "format": "json",
        }
    )
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": UA}
    )
    data = json.loads(urllib.request.urlopen(req, timeout=60).read())
    page = next(iter(data["query"]["pages"].values()))
    ii = (page.get("imageinfo") or [{}])[0]
    meta = ii.get("extmetadata") or {}

    def g(k: str) -> str:
        return re.sub("<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()

    return {
        "author": (g("Artist") or g("Credit") or "Wikimedia Commons")[:90],
        "license": g("LicenseShortName") or g("License") or "CC",
        "sourceUrl": (ii.get("url") or "").split("?")[0],
        "pageUrl": "https://commons.wikimedia.org/wiki/"
        + urllib.parse.quote(title.replace(" ", "_")),
    }


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    meta = {}
    for spec in SOURCES:
        info = commons_info(spec["commons"])
        meta[spec["tmp"]] = {**info, "commons": spec["commons"]}
        out = TMP / spec["tmp"]
        if not out.exists():
            req = urllib.request.Request(info["sourceUrl"], headers={"User-Agent": UA})
            out.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        print(spec["tmp"], Image.open(out).size)
    (TMP / "l2-sources-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
