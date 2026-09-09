#!/usr/bin/env python3
"""Download, polygonize, and wire people images into Book 1 chapters 3–30."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "book1-people-images-manifest.json"
BOOK = ROOT / "content" / "book1"
IMG_DIR = ROOT / "frontend" / "public" / "images" / "book1"
SRC_DIR = ROOT / "scripts" / "_tmp_sources" / "people"
POLYGONIZE = ROOT / "scripts" / "polygonize-photo.py"
UA = "LearnBosnianBot/1.0 (educational)"

OVERRIDES: dict[int, dict] = {
    3: {
        "conversation": {
            "id": "admejdan-cafe",
            "commons": "File:AdmejdanSarajevo.JPG",
            "alt": "Polygon painting of people at outdoor café tables in At Mejdan park, Sarajevo",
            "credit": "At Mejdan café, Sarajevo",
            "objectPosition": "50% 42%",
        },
        "funFact": {
            "funFactTitle": "Lokum on the tray",
            "id": "bazaar-shoppers",
            "commons": "File:Baščaršija_(6086778408).jpg",
            "alt": "Polygon painting of shoppers in Baščaršija near sweets and souvenir stalls",
            "credit": "Baščaršija market, Sarajevo",
            "objectPosition": "50% 45%",
        },
    },
    30: {
        "funFact": {
            "funFactTitle": "Čestitam fits any toast",
            "id": "cafe-toast",
            "commons": "File:Giannini Cafe - panoramio.jpg",
            "alt": "Polygon painting of friends sharing drinks at an outdoor Sarajevo café",
            "credit": "Giannini café, Sarajevo",
            "objectPosition": "50% 40%",
        },
    },
}

SEMANTIC_IDS: dict[int, tuple[str, str]] = {
    3: ("admejdan-cafe", "bazaar-shoppers"),
    4: ("bascarsija-morning", "morica-han-dining"),
    5: ("mostar-stroll", "stari-most-divers"),
    6: ("travnik-streets", "neum-beach"),
    7: ("pocitelj-climb", "mostar-market"),
    8: ("sarajevo-market", "burek-stall"),
    9: ("produce-market", "fruit-stall"),
    10: ("stolac-walk", "stolac-mosque"),
    11: ("trebevic-hike", "olympic-ski"),
    12: ("vrelo-bosne-walk", "vrelo-avenue"),
    13: ("zenica-market", "zenica-street"),
    14: ("banja-luka-street", "vrbas-rafting"),
    15: ("latin-bridge", "konjic-bridge"),
    16: ("bus-station", "jablanica-lake"),
    17: ("sarajevo-restaurant", "cevapi-table"),
    18: ("football-fans", "una-walk"),
    19: ("ferhadija-walk", "sarajevo-center"),
    20: ("tram-riders", "tram-snow"),
    21: ("zlatna-ribica", "una-walk-vintage"),
    22: ("travnik-day", "travnik-mosque"),
    23: ("zenica-daily", "university-students"),
    24: ("neretva-rafting", "bjelasnica-ski"),
    25: ("inat-kuca-street", "bascarsija-cat"),
    26: ("zenica-theater", "zenica-market-hall"),
    27: ("banja-luka-tour", "law-students"),
    28: ("mostar-bridge-crowd", "neretva-riverside"),
    29: ("bascarsija-square", "bascarsija-walk"),
    30: ("markale-market", "cafe-toast"),
}


def commons_filepath(commons: str) -> str:
    name = commons.replace("File:", "")
    return (
        "https://commons.wikimedia.org/wiki/Special:FilePath/"
        + urllib.parse.quote(name, safe="(),._-")
    )


def commons_page(commons: str) -> str:
    name = commons.replace("File:", "").replace(" ", "_")
    return "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(name)


def parse_credit(spec: dict) -> tuple[str, str, str]:
    credit = spec.get("credit", "")
    if "—" in credit:
        place, rest = credit.split("—", 1)
        place = place.strip()
        rest = rest.strip()
    else:
        place = credit.strip()
        rest = ""
    author = "Wikimedia Commons"
    license_ = "CC"
    if rest:
        if " / " in rest:
            author, license_ = rest.split(" / ", 1)
            license_ = license_.split(",")[0].strip()
        else:
            author = rest.split(",")[0].strip()
    return place, author[:90], license_[:40]


def download(filepath_url: str, dest: Path, retries: int = 6) -> None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(filepath_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if len(data) < 5000:
                raise RuntimeError(f"download too small ({len(data)} bytes)")
            dest.write_bytes(data)
            return
        except Exception as exc:
            if attempt == retries - 1:
                raise
            wait = 8 * (attempt + 1)
            print(f"retry download in {wait}s ({attempt + 1}): {exc}")
            time.sleep(wait)


def polygonize(source: Path, dest: Path) -> None:
    subprocess.run(
        [sys.executable, str(POLYGONIZE), str(source), str(dest)],
        check=True,
    )


def build_image_entry(day: int, image_id: str, spec: dict, commons: str) -> dict:
    place, author, license_ = parse_credit(spec)
    entry = {
        "id": image_id,
        "alt": spec["alt"],
        "localPath": f"/images/book1/day-{day:02d}-{image_id}.png",
        "sourceUrl": commons_filepath(commons),
        "pageUrl": commons_page(commons),
        "author": author,
        "license": license_,
        "credit": place,
    }
    if spec.get("objectPosition"):
        entry["objectPosition"] = spec["objectPosition"]
    return entry


def patch_chapter(day: int, conv_img: dict, fun_img: dict, fun_title: str) -> None:
    path = BOOK / f"day-{day:02d}" / "chapter.json"
    ch = json.loads(path.read_text(encoding="utf-8"))
    images = ch.setdefault("images", [])
    existing = {i["id"]: i for i in images}
    for img in (conv_img, fun_img):
        existing[img["id"]] = img
    ch["images"] = list(existing.values())
    ch.setdefault("conversation", {})["imageId"] = conv_img["id"]
    matched = False
    for fact in ch.get("funFacts", []):
        if fact.get("title") == fun_title:
            fact["imageId"] = fun_img["id"]
            matched = True
            break
    if not matched:
        raise RuntimeError(f"Day {day}: funFact title not found: {fun_title!r}")
    path.write_text(json.dumps(ch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug_for(commons: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", commons.replace("File:", ""))[:70]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    local_only = "--local-only" in sys.argv
    from_day = int(args[0]) if args else 3
    manifest: list[dict] = json.loads(MANIFEST.read_text(encoding="utf-8"))
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    for entry in manifest:
        day = entry["day"]
        if day < from_day:
            continue
        if day in OVERRIDES:
            for key in ("conversation", "funFact"):
                if key in OVERRIDES[day]:
                    entry[key].update(OVERRIDES[day][key])

        conv_id, fun_id = SEMANTIC_IDS[day]
        entry["conversation"]["id"] = conv_id
        entry["funFact"]["id"] = fun_id

        chapter_path = BOOK / f"day-{day:02d}" / "chapter.json"
        ch = json.loads(chapter_path.read_text(encoding="utf-8"))
        conv_png = IMG_DIR / f"day-{day:02d}-{conv_id}.png"
        fun_png = IMG_DIR / f"day-{day:02d}-{fun_id}.png"
        if (
            conv_png.exists()
            and fun_png.exists()
            and ch.get("conversation", {}).get("imageId") == conv_id
        ):
            print(f"skip lesson {day}")
            continue

        ready = True
        for role in ("conversation", "funFact"):
            spec = entry[role]
            commons = spec["commons"]
            slug = slug_for(commons)
            src = SRC_DIR / f"day-{day:02d}-{slug}.jpg"
            png = IMG_DIR / f"day-{day:02d}-{spec['id']}.png"
            if not src.exists():
                if local_only:
                    print(f"missing source (local-only) day-{day:02d} {slug}")
                    ready = False
                    break
                print(f"download day-{day:02d} {slug}")
                download(commons_filepath(commons), src)
                time.sleep(8)
            if not png.exists():
                if not src.exists():
                    ready = False
                    break
                print(f"polygonize {png.name}")
                polygonize(src, png)

        if not ready:
            continue

        conv_img = build_image_entry(
            day, conv_id, entry["conversation"], entry["conversation"]["commons"]
        )
        fun_img = build_image_entry(
            day, fun_id, entry["funFact"], entry["funFact"]["commons"]
        )
        patch_chapter(day, conv_img, fun_img, entry["funFact"]["funFactTitle"])
        print(f"patched lesson {day}")

    print("done")


if __name__ == "__main__":
    main()
