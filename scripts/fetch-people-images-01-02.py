#!/usr/bin/env python3
"""Download source photos for Lesson 1–2 people images."""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "frontend" / "public" / "images" / "book1"
TMP = ROOT / "scripts" / "_tmp_sources"
TMP.mkdir(parents=True, exist_ok=True)
UA = "LearnBosnianBot/1.0 (educational)"

SOURCES = [
    {
        "tmp": "day-01-street-festival-src.jpg",
        "commons": "File:Street_Food_Festival_in_Sarajevo_Old_Town.JPG",
    },
    {
        "tmp": "day-01-bazaar-people-src.jpg",
        "commons": "File:Baščaršija_(6086778408).jpg",
    },
    {
        "tmp": "day-02-sebilj-people-src.jpg",
        "url": "https://images.pexels.com/photos/28305255/pexels-photo-28305255.jpeg?auto=compress&cs=tinysrgb&w=1600",
        "author": "Adem Ayten",
        "license": "Pexels License",
        "pageUrl": "https://www.pexels.com/photo/sebil-at-turk-carsija-28305255/",
    },
    {
        "tmp": "day-02-ferhadija-people-src.jpg",
        "commons": "File:Ferhadija_street_Sarajevo.jpg",
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
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                out.write_bytes(r.read())
            return
        except Exception as e:
            print("retry", attempt, e)
            time.sleep(2**attempt)
    raise RuntimeError(f"Failed to download {url}")


def save_png(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    im.thumbnail((1600, 1600))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="PNG", optimize=True)


def main():
    meta = {}
    for spec in SOURCES:
        tmp = TMP / spec["tmp"]
        if spec.get("commons"):
            info = commons_info(spec["commons"])
            meta[spec["tmp"]] = info
            if not tmp.exists():
                download(info["sourceUrl"], tmp)
        else:
            info = {
                "author": spec["author"],
                "license": spec["license"],
                "sourceUrl": spec["url"],
                "pageUrl": spec["pageUrl"],
            }
            meta[spec["tmp"]] = info
            if not tmp.exists():
                download(spec["url"], tmp)
        print(spec["tmp"], Image.open(tmp).size, info["license"], info["author"])
    (TMP / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
