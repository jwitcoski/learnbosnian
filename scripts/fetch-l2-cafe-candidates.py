#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

TMP = Path(__file__).resolve().parents[1] / "scripts" / "_tmp_sources"
UA = "LearnBosnianBot/1.0"

CANDIDATES = [
    "File:Mostar_-_Cafe_Coco_Loco_(49033682451).jpg",
    "File:Restaurant_with_Cool_Decor,_Sarajevo,_Bosnia_(3802594664).jpg",
    "File:Lutvina_kahva_(2351368919).jpg",
    "File:Travnik,_Bosnia_and_Herzegovina_(4862014296).jpg",
    "File:Banja_Luka_-_Kazandziluk_(2019).jpg",
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
    if "missing" in page:
        raise RuntimeError(f"Missing: {title}")
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


def slug(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", title.replace("File:", ""))[:80]


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    for title in CANDIDATES:
        try:
            info = commons_info(title)
            out = TMP / f"l2cafe-{slug(title)}.jpg"
            if not out.exists():
                for attempt in range(5):
                    try:
                        req = urllib.request.Request(
                            info["sourceUrl"], headers={"User-Agent": UA}
                        )
                        out.write_bytes(urllib.request.urlopen(req, timeout=120).read())
                        break
                    except Exception:
                        time.sleep(2**attempt)
            if out.exists():
                print(out.name, Image.open(out).size, info["license"], title)
        except Exception as e:
            print("FAIL", title, e)


if __name__ == "__main__":
    main()
