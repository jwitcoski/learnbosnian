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
        "tmp": "l1-ferhadija-cafe-src.jpg",
        "commons": "File:Sarajevo_Ferhadija_2007-08-16.jpg",
    },
    {
        "tmp": "l1-boza-drinks-src.jpg",
        "commons": "File:Boza_and_Boem_šnita_in_Sarajevo.JPG",
    },
    {
        "tmp": "l1-bascarsija-people-src.jpg",
        "commons": "File:Baščaršija_(6086230081).jpg",
    },
]


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def commons_info(title: str) -> dict:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime",
            "format": "json",
        }
    )
    data = get_json("https://commons.wikimedia.org/w/api.php?" + q)
    page = next(iter(data["query"]["pages"].values()))
    ii = (page.get("imageinfo") or [{}])[0]
    meta = ii.get("extmetadata") or {}

    def g(k: str) -> str:
        return re.sub("<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()

    author = (g("Artist") or g("Credit") or "Wikimedia Commons")[:90]
    license_ = g("LicenseShortName") or g("License") or "CC"
    url = (ii.get("url") or "").split("?")[0]
    page_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(
        title.replace(" ", "_")
    )
    return {
        "author": author,
        "license": license_,
        "sourceUrl": url,
        "pageUrl": page_url,
    }


def download(url: str, out: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        out.write_bytes(r.read())


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    meta = {}
    for spec in SOURCES:
        info = commons_info(spec["commons"])
        meta[spec["tmp"]] = {**info, "commons": spec["commons"]}
        out = TMP / spec["tmp"]
        if not out.exists():
            download(info["sourceUrl"], out)
        print(spec["tmp"], Image.open(out).size)
    (TMP / "l1-sources-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
