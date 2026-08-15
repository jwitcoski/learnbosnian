#!/usr/bin/env python3
"""Assemble Lessons 21-30 chapter.json + video-script.md from data modules and polygon images."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from _lessons_21_25_data import LESSONS as L21
from _lessons_21_25_data import VIDEOS as V21
from _lessons_26_30_data import LESSONS as L26
from _lessons_26_30_data import VIDEOS as V26

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "frontend" / "public" / "images" / "book1"
ASSET_DIR = Path("/opt/cursor/artifacts/assets")

LESSONS = {**L21, **L26}
VIDEOS = {**V21, **V26}

# id -> (filename, alt)
IMAGE_META: dict[int, list[tuple[str, str, str]]] = {
    21: [
        ("weekend-map", "day-21-weekend-map.png", "Polygon painting of a weekend map beside the Una River."),
        ("una-postcard", "day-21-una-postcard.png", "Polygon painting of an Una River postcard view near Bihać."),
        ("cafe-plan", "day-21-cafe-plan.png", "Polygon painting of a café table used for weekend planning."),
        ("civic-rural-bus", "day-21-civic-rural-bus.png", "Polygon painting of an empty rural bus stop in a Bosnian village."),
    ],
    22: [
        ("travnik-mosque", "day-22-travnik-mosque.png", "Polygon painting of a colorful mosque in Travnik old town."),
        ("travnik-street", "day-22-travnik-street.png", "Polygon painting of a narrow Travnik street."),
        ("travnik-tower", "day-22-travnik-tower.png", "Polygon painting of the Travnik fortress tower on a hill."),
        ("civic-winding-road", "day-22-civic-winding-road.png", "Polygon painting of a winding mountain road with fast traffic risk."),
    ],
    23: [
        ("daily-cafe", "day-23-daily-cafe.png", "Polygon painting of a busy café where people talk about daily plans."),
        ("zenica-postcard", "day-23-zenica-postcard.png", "Polygon painting of a Zenica valley postcard."),
        ("activity-cards", "day-23-activity-cards.png", "Polygon painting of activity cards on a wooden table."),
        ("civic-eurovision-debt", "day-23-civic-eurovision-debt.png", "Polygon painting of a dim stage standing for Eurovision absence and BHRT debt."),
    ],
    24: [
        ("una-river", "day-24-una-river.png", "Polygon painting of the turquoise Una River canyon."),
        ("bjelasnica-ridge", "day-24-bjelasnica-ridge.png", "Polygon painting of a rocky Bjelašnica ridge."),
        ("jahorina-ski", "day-24-jahorina-ski.png", "Polygon painting of busy ski slopes on Jahorina."),
        ("civic-olympic-ski-gap", "day-24-civic-olympic-ski-gap.png", "Polygon painting contrasting lively Jahorina with neglected Olympic ski sites."),
    ],
    25: [
        ("clinic-door", "day-25-clinic-door.png", "Polygon painting of a small clinic door on a Bosnian street."),
        ("pharmacy-shelf", "day-25-pharmacy-shelf.png", "Polygon painting of a pharmacy shelf with medicine bottles."),
        ("mrvica-vet", "day-25-mrvica-vet.png", "Polygon painting of Mrvica the cat at a vet exam table."),
        ("civic-jmbg", "day-25-civic-jmbg.png", "Polygon painting of newborn paperwork and passport delay."),
    ],
    26: [
        ("flat-kitchen", "day-26-flat-kitchen.png", "Polygon painting of a bright flat kitchen."),
        ("apartment-door", "day-26-apartment-door.png", "Polygon painting of an apartment door and keys."),
        ("furniture-corner", "day-26-furniture-corner.png", "Polygon painting of a furnished room corner."),
        ("civic-returnee-pressure", "day-26-civic-returnee-pressure.png", "Polygon painting of a quiet returnee house under local pressure."),
    ],
    27: [
        ("guide-badge", "day-27-guide-badge.png", "Polygon painting of a tour guide badge and map."),
        ("classroom-desk", "day-27-classroom-desk.png", "Polygon painting of a classroom desk and notebook."),
        ("office-tram", "day-27-office-tram.png", "Polygon painting of a tram commute toward work."),
        ("civic-rs-secession", "day-27-civic-rs-secession.png", "Polygon painting of institutional tension around entity challenges to state authority."),
    ],
    28: [
        ("stari-most", "day-28-stari-most.png", "Polygon painting of Stari Most over the Neretva in Mostar."),
        ("neretva-green", "day-28-neretva-green.png", "Polygon painting of green Neretva river water."),
        ("mostar-old-town", "day-28-mostar-old-town.png", "Polygon painting of Mostar old-town roofs and alleys."),
        ("civic-medjugorje", "day-28-civic-medjugorje.png", "Polygon painting of a Međugorje hillside cross and pilgrimage path."),
    ],
    29: [
        ("postcard-desk", "day-29-postcard-desk.png", "Polygon painting of a postcard writing desk."),
        ("stamp-envelope", "day-29-stamp-envelope.png", "Polygon painting of a stamped envelope on a table."),
        ("ferhadija-letter", "day-29-ferhadija-letter.png", "Polygon painting of letter writing near Ferhadija."),
        ("civic-genocide-denial", "day-29-civic-genocide-denial.png", "Polygon painting of the Srebrenica memorial cemetery in solemn light."),
    ],
    30: [
        ("party-table", "day-30-party-table.png", "Polygon painting of a graduation party table."),
        ("cake-heist", "day-30-cake-heist.png", "Polygon painting of Mrvica stealing cake at the party."),
        ("friends-toast", "day-30-friends-toast.png", "Polygon painting of friends toasting at the finale party."),
        ("civic-night-wolves", "day-30-civic-night-wolves.png", "Polygon painting of a motorcycle parade mood in Banja Luka."),
    ],
}


def ensure_image(filename: str) -> Path:
    dest = IMG_DIR / filename
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    src = ASSET_DIR / filename
    if src.exists():
        shutil.copy2(src, dest)
        return dest
    raise FileNotFoundError(f"Missing image asset for {filename}")


def img_entry(image_id: str, filename: str, alt: str) -> dict:
    ensure_image(filename)
    return {
        "id": image_id,
        "alt": alt,
        "localPath": f"/images/book1/{filename}",
        "sourceUrl": "",
        "pageUrl": "",
        "author": "Course polygon art",
        "license": "Course original",
        "credit": "Original polygon painting for Learn Bosnian Book 1.",
    }


def write_chapter(day: int, data: dict) -> None:
    path = ROOT / "content" / "book1" / f"day-{day:02d}" / "chapter.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path)


def write_video(day: int, text: str) -> None:
    path = ROOT / "content" / "book1" / f"day-{day:02d}" / "video-script.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    # Copy any newly generated assets first
    for src in ASSET_DIR.glob("day-2*.png"):
        if src.name.startswith("day-2") or src.name.startswith("day-30"):
            dest = IMG_DIR / src.name
            if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(src, dest)

    for day in range(21, 31):
        chapter = json.loads(json.dumps(LESSONS[day]))  # deep copy
        images = [img_entry(i, f, a) for i, f, a in IMAGE_META[day]]
        chapter["images"] = images
        chapter["imagesNeeded"] = False
        chapter["status"] = "draft"
        if not chapter.get("reviewerNotes"):
            chapter["reviewerNotes"] = (
                "This full draft is ready for human review before publication."
            )
        write_chapter(day, chapter)
        write_video(day, VIDEOS[day])

    print("done lessons 21-30")


if __name__ == "__main__":
    main()
