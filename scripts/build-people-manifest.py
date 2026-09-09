#!/usr/bin/env python3
"""Build scripts/book1-people-images-manifest.json for Book 1 days 3-30."""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "book1-people-images-manifest.json"
CHAPTERS = ROOT / "scripts" / "_tmp_sources" / "chapters-03-30.json"
USED_URLS = ROOT / "scripts" / "_tmp_sources" / "used-urls.txt"
UA = "LearnBosnianBot/1.0 (educational; learnbosnian-project)"
DELAY = 2.5

BLOCKED_BASENAMES = {
    "sarajevo_ferhadija_2007-08-16.jpg",
    "street_food_festival_in_sarajevo_old_town.jpg",
    "baščaršija_(6086230081).jpg",
    "bascarsija_(6086230081).jpg",
    "day_in_sarajevo.jpg",
    "sarajevo_-_sebilj_fountain.jpg",
    "baščaršija_sarajevo.jpg",
    "bascarsija.jpg",
    "mostar_-_cafe_coco_loco_(49033682451).jpg",
    "morića_han_(1).jpg",
    "morica_han_(1).jpg",
}

# Final curated assignments (commons titles verified or from Commons search)
LESSONS: list[dict] = [
    {
        "day": 3,
        "conversation": "File:Lutvina kahva (2351368919).jpg",
        "conversation_alt": "Guests sit at outdoor tables outside Lutvina kahva in Sarajevo",
        "conversation_credit": "Lutvina kahva, Sarajevo",
        "conversation_objectPosition": "50% 40%",
        "funFactTitle": "Lokum on the tray",
        "funFact": "File:Boza and Boem šnita in Sarajevo.JPG",
        "funFact_alt": "Friends share sweets and drinks at a Sarajevo café table",
        "funFact_credit": "Café treats, Sarajevo",
    },
    {
        "day": 4,
        "conversation": "File:Early Morning in Bascarsija (54564806901).jpg",
        "conversation_alt": "Morning regulars gather at café tables in Baščaršija",
        "conversation_credit": "Morning café, Baščaršija",
        "funFactTitle": "Chosen family at the table",
        "funFact": "File:Morica Han.jpg",
        "funFact_alt": "People dine inside the historic Morića Han caravanserai in Sarajevo",
        "funFact_credit": "Morića Han, Sarajevo",
    },
    {
        "day": 5,
        "conversation": "File:Old town, Mostar (15) (29225114223).jpg",
        "conversation_alt": "Tourists walk through Mostar's old town streets",
        "conversation_credit": "Mostar old town",
        "funFactTitle": "Mostar means the bridge keeper",
        "funFact": "File:Mostar - Bosnia - Divers.jpg",
        "funFact_alt": "Divers and onlookers gather near Stari Most in Mostar",
        "funFact_credit": "Stari Most, Mostar",
    },
    {
        "day": 6,
        "conversation": "File:Travnik Altstadt 2.JPG",
        "conversation_alt": "Visitors walk the old streets of Travnik beneath the clock tower",
        "conversation_credit": "Travnik old town",
        "funFactTitle": "Neum touches the sea",
        "funFact": "File:Feral Beach on the souther side of Neum peninsula, 2024.jpg",
        "funFact_alt": "Families relax on the Adriatic beach at Neum",
        "funFact_credit": "Neum beach",
    },
    {
        "day": 7,
        "conversation": "File:Počitelj - panoramio (1).jpg",
        "conversation_alt": "Visitors climb the stone terraces of Počitelj",
        "conversation_credit": "Počitelj old town",
        "funFactTitle": "Počitelj\u2019s stone stack",
        "funFact": "File:Market street in Mostar old town (8) (29226494924).jpg",
        "funFact_alt": "Shoppers browse a market lane in an old Bosnian town",
        "funFact_credit": "Old-town market street",
    },
    {
        "day": 8,
        "conversation": "File:Fruit market in Sarajevo (3887505834).jpg",
        "conversation_alt": "Shoppers browse fruit crates at a Sarajevo market",
        "conversation_credit": "Sarajevo market",
        "funFactTitle": "Jogurt is a partner",
        "funFact": "File:Burek in Sarajevo.jpg",
        "funFact_alt": "A vendor serves fresh burek to waiting customers",
        "funFact_credit": "Burek stall, Sarajevo",
    },
    {
        "day": 9,
        "conversation": "File:City Produce Market (6042748651).jpg",
        "conversation_alt": "People shop at an open produce market in Bosnia",
        "conversation_credit": "Produce market",
        "funFactTitle": "Tuzla\u2019s other fame",
        "funFact": "File:Fruit stall, Sarajevo (3887477230).jpg",
        "funFact_alt": "A fruit seller tends a colorful stall at the market",
        "funFact_credit": "Market stall",
    },
    {
        "day": 10,
        "conversation": "File:Stari grad Stolac (02).JPG",
        "conversation_alt": "People stroll through stone lanes in Stolac",
        "conversation_credit": "Stolac old town",
        "funFactTitle": "Stećci near Stolac",
        "funFact": "File:Painted Mosque, Stolac (5458592551).jpg",
        "funFact_alt": "Visitors pause near the Painted Mosque in Stolac",
        "funFact_credit": "Painted Mosque, Stolac",
    },
    {
        "day": 11,
        "conversation": "File:Sarajevo (16616142640).jpg",
        "conversation_alt": "Hikers pause on a misty Trebević trail above Sarajevo",
        "conversation_credit": "Trebević hillside",
        "funFactTitle": "Jahorina changes with the seasons",
        "funFact": "File:Cross-country ski area from the Sarajevo Olympics (3887479130).jpg",
        "funFact_alt": "Skiers cross a snowy plateau on an Olympic mountain",
        "funFact_credit": "Olympic ski area, Bosnia",
    },
    {
        "day": 12,
        "conversation": "File:Vrelo Bosne (1).jpg",
        "conversation_alt": "Families walk the tree-lined paths at Vrelo Bosne",
        "conversation_credit": "Vrelo Bosne Park",
        "funFactTitle": "A long avenue leads to the springs",
        "funFact": "File:Sarajevo (2671671915).jpg",
        "funFact_alt": "Visitors stroll the long avenue toward the Bosna springs",
        "funFact_credit": "Vrelo Bosne avenue",
    },
    {
        "day": 13,
        "conversation": "File:Du côté du marché -ZENICA (BiH).JPG",
        "conversation_alt": "People gather at an open market in Zenica",
        "conversation_credit": "Zenica market",
        "funFactTitle": "Brčko sits on the Sava",
        "funFact": "File:Zenica 2006 2.jpg",
        "funFact_alt": "Pedestrians walk a busy Zenica street",
        "funFact_credit": "Zenica city center",
    },
    {
        "day": 14,
        "conversation": "File:Banja Luka Бања Лука, Bosnia and Herzegovina Босна и Херцеговина - 53033304725.jpg",
        "conversation_alt": "Pedestrians walk a central street in Banja Luka",
        "conversation_credit": "Banja Luka city center",
        "funFactTitle": "The Vrbas shapes Banja Luka",
        "funFact": "File:Rafting Vrbas (5984391544).jpg",
        "funFact_alt": "Rafting guides and tourists paddle the Vrbas near Banja Luka",
        "funFact_credit": "Vrbas River, Banja Luka",
    },
    {
        "day": 15,
        "conversation": "File:The Latin Bridge, Sarajevo.jpg",
        "conversation_alt": "Tourists pause on Latin Bridge in Sarajevo",
        "conversation_credit": "Latin Bridge, Sarajevo",
        "funFactTitle": "Konjic rebuilt an older crossing",
        "funFact": "File:Konjic, Bosnia and Herzegovina.jpg",
        "funFact_alt": "People cross the old stone bridge in Konjic",
        "funFact_credit": "Konjic old town",
    },
    {
        "day": 16,
        "conversation": "File:Sarajevo Bus-Station 2011-10-19.jpg",
        "conversation_alt": "Travelers wait with bags at Sarajevo bus station",
        "conversation_credit": "Sarajevo bus station",
        "funFactTitle": "Jablanica sits on the lake road",
        "funFact": "File:Jablanica lake.jpg",
        "funFact_alt": "Tourists enjoy the shoreline of Jablaničko jezero",
        "funFact_credit": "Jablaničko jezero",
    },
    {
        "day": 17,
        "conversation": "File:Restaurant with Cool Decor, Sarajevo, Bosnia (3802594664).jpg",
        "conversation_alt": "Diners share a meal at a Sarajevo restaurant",
        "conversation_credit": "Sarajevo restaurant",
        "funFactTitle": "Klepe come with sauce and garlic",
        "funFact": "File:Cevapi s kajmakom.jpg",
        "funFact_alt": "A shared plate of ćevapi arrives at a Bosnian table",
        "funFact_credit": "Restaurant table, Bosnia",
    },
    {
        "day": 18,
        "conversation": "File:Bosnia Soccer Fans at King Baudouin Stadium Brussels.jpg",
        "conversation_alt": "Bosnia and Herzegovina football supporters cheer in the stands",
        "conversation_credit": "Football supporters",
        "funFactTitle": "Štrbački buk shows the Una",
        "funFact": "File:Una River Water Falls - Flickr - TKnoxB.jpg",
        "funFact_alt": "Visitors walk beside the emerald Una near Štrbački buk",
        "funFact_credit": "Una River, northwest Bosnia",
    },
    {
        "day": 19,
        "conversation": "File:Ferhadija street Sarajevo.jpg",
        "conversation_alt": "Pedestrians walk along Ferhadija street in Sarajevo",
        "conversation_credit": "Ferhadija, Sarajevo",
        "funFactTitle": "Two landmarks, one center",
        "funFact": "File:1997 in Sarajevo 010.jpg",
        "funFact_alt": "People gather in Sarajevo's central pedestrian zone",
        "funFact_credit": "Sarajevo city center",
    },
    {
        "day": 20,
        "conversation": "File:Sarajevo Tram-505 Line-3 2011-11-13.jpg",
        "conversation_alt": "Passengers board a tram on a Sarajevo street",
        "conversation_credit": "Sarajevo tram",
        "funFactTitle": "Trams frame everyday calls",
        "funFact": "File:Early 2012 European cold wave in Sarajevo (6818394925).jpg",
        "funFact_alt": "Pedestrians wait beside a tram on a snowy Sarajevo street",
        "funFact_credit": "Tram stop, Sarajevo",
    },
    {
        "day": 21,
        "conversation": "File:Zlatna Ribica (116653269).jpeg",
        "conversation_alt": "A solo visitor reads over coffee at Zlatna Ribica café",
        "conversation_credit": "Zlatna Ribica, Sarajevo",
        "funFactTitle": "Una and Bihać suit a quiet weekend",
        "funFact": "File:Durch Bosnien und die Herzegovina kreuz und quer; Wanderungen (1897) (14758911236).jpg",
        "funFact_alt": "Travelers walk beside a river in northwest Bosnia",
        "funFact_credit": "Una region walk",
    },
    {
        "day": 22,
        "conversation": "File:Travnik Altstadt 3.JPG",
        "conversation_alt": "People walk the colorful streets of Travnik",
        "conversation_credit": "Travnik old town",
        "funFactTitle": "Sulejmanija stands out for color",
        "funFact": "File:Travnik mosque 01.jpg",
        "funFact_alt": "Visitors gather near the colorful Sulejmanija mosque in Travnik",
        "funFact_credit": "Sulejmanija, Travnik",
    },
    {
        "day": 23,
        "conversation": "File:Dans les Rues de Zenica.JPG",
        "conversation_alt": "People chat along a busy street in Zenica",
        "conversation_credit": "Zenica street",
        "funFactTitle": "Šta radiš? Opens honest daily talk",
        "funFact": "File:NHQSa speaks with university students (5018704).jpg",
        "funFact_alt": "University students talk together on campus in Sarajevo",
        "funFact_credit": "University students, Sarajevo",
    },
    {
        "day": 24,
        "conversation": "File:Rafting on the Neretva River (3886718503).jpg",
        "conversation_alt": "Rafting guides and tourists paddle the emerald Neretva River",
        "conversation_credit": "Neretva River rafting",
        "funFactTitle": "1984 Olympics left two ski stories",
        "funFact": "File:Start of olympic downhill on Bjelasnica.jpg",
        "funFact_alt": "Skiers gather at the start of an Olympic downhill on Bjelašnica",
        "funFact_credit": "Bjelašnica ski slopes",
    },
    {
        "day": 25,
        "conversation": "File:Sarajevo - Inat kuća (49104054186).jpg",
        "conversation_alt": "A worried pet owner hurries through Sarajevo's old town toward help",
        "conversation_credit": "Sarajevo old town",
        "funFactTitle": "Vet clinics use the same polite frames",
        "funFact": "File:Cat in Baščaršija (6086310911).jpg",
        "funFact_alt": "Mrvica the café cat weaves between shoppers in Baščaršija",
        "funFact_credit": "Baščaršija street",
    },
    {
        "day": 26,
        "conversation": "File:Theater in Zenica from side.jpg",
        "conversation_alt": "Residents walk past the theater during a flat viewing in Zenica",
        "conversation_credit": "Zenica city center",
        "funFactTitle": "Zenica mixes industry and student life",
        "funFact": "File:Zenica, tržiště.jpg",
        "funFact_alt": "Shoppers browse stalls at Zenica's open market",
        "funFact_credit": "Zenica market",
    },
    {
        "day": 27,
        "conversation": "File:Banja Luka Бања Лука, Bosnia and Herzegovina Босна и Херцеговина - 53033036144.jpg",
        "conversation_alt": "A guide leads a morning tour group through Banja Luka",
        "conversation_credit": "Banja Luka city tour",
        "funFactTitle": "Radim is a daily anchor",
        "funFact": "File:NHQSa Commander speaks with law students (5229623).jpg",
        "funFact_alt": "Law students study together at a Bosnian university",
        "funFact_credit": "University law students",
    },
    {
        "day": 28,
        "conversation": "File:Mostar, Bosnia and Herzegovina 31 July 2022 - 02.jpg",
        "conversation_alt": "A crowd watches the green Neretva flow beneath Stari Most",
        "conversation_credit": "Stari Most, Mostar",
        "funFactTitle": "Neretva color surprises newcomers",
        "funFact": "File:View downstream from the bridge Mostar (4060081447).jpg",
        "funFact_alt": "People stroll along the green Neretva in Mostar",
        "funFact_credit": "Neretva riverside, Mostar",
    },
    {
        "day": 29,
        "conversation": "File:Baščaršija square.jpg",
        "conversation_alt": "Shoppers and vendors fill Baščaršija square in Sarajevo",
        "conversation_credit": "Baščaršija square",
        "funFactTitle": "Razglednica beats a long email for tone",
        "funFact": "File:Baščaršija, Sarajevo 71000, Bosnia and Herzegovina - panoramio (1).jpg",
        "funFact_alt": "Pedestrians walk Baščaršija with souvenir stalls and cafés",
        "funFact_credit": "Baščaršija walk",
    },
    {
        "day": 30,
        "conversation": "File:Sarajevo - Gradska tržnica Markale (49094480891).jpg",
        "conversation_alt": "Friends meet at a lively Sarajevo market before a celebration",
        "conversation_credit": "Markale market, Sarajevo",
        "funFactTitle": "Čestitam fits any toast",
        "funFact": "File:Cheers.jpg",
        "funFact_alt": "Raised glasses toast a celebration",
        "funFact_credit": "Celebration toast",
    },
]


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def normalize_basename(url_or_name: str) -> str:
    name = url_or_name.rsplit("/", 1)[-1].lower()
    return urllib.parse.unquote(name)


def load_used() -> set[str]:
    used: set[str] = set()
    if USED_URLS.exists():
        for line in read_text_auto(USED_URLS).splitlines():
            line = line.strip()
            if line:
                used.add(normalize_basename(line))
    for ch_path in sorted((ROOT / "content" / "book1").glob("day-*/chapter.json")):
        ch = json.loads(ch_path.read_text(encoding="utf-8"))
        for img in ch.get("images") or []:
            if img.get("sourceUrl"):
                used.add(normalize_basename(img["sourceUrl"]))
    return used


def api(params: dict) -> dict:
    time.sleep(DELAY)
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def batch_info(titles: list[str]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i : i + 40]
        data = api(
            {
                "action": "query",
                "titles": "|".join(chunk),
                "prop": "imageinfo",
                "iiprop": "url|extmetadata|mime",
            }
        )
        for _pid, page in data["query"]["pages"].items():
            if "missing" in page:
                continue
            ii = (page.get("imageinfo") or [{}])[0]
            if not ii.get("url"):
                continue
            title = page["title"]
            if not title.startswith("File:"):
                title = "File:" + title
            meta = ii.get("extmetadata") or {}

            def g(k: str) -> str:
                return re.sub("<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()

            author = (g("Artist") or g("Credit") or "Wikimedia Commons")[:90]
            license_ = g("LicenseShortName") or g("License") or "CC"
            source_url = ii["url"].split("?")[0]
            result[title] = {
                "author": author,
                "license": license_,
                "sourceUrl": source_url,
                "pageUrl": "https://commons.wikimedia.org/wiki/"
                + urllib.parse.quote(title.replace(" ", "_")),
            }
    return result


def slug_id(day: int, commons: str, prefix: str = "") -> str:
    base = commons.replace("File:", "")
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:40]
    return f"day-{day:02d}-{prefix}{slug}" if prefix else f"day-{day:02d}-{slug}"


def main() -> None:
    chapters = json.loads(CHAPTERS.read_text(encoding="utf-8"))
    chapter_map = {c["day"]: c for c in chapters}
    used_basenames = load_used()

    titles = []
    for lesson in LESSONS:
        titles.append(lesson["conversation"])
        titles.append(lesson["funFact"])
    info_map = batch_info(titles)

    manifest: list[dict] = []
    funfact_mismatches: list[dict] = []
    problems: list[dict] = []
    seen_commons: set[str] = set()
    seen_urls: set[str] = set()

    for lesson in LESSONS:
        day = lesson["day"]
        ch = chapter_map[day]
        fft = lesson["funFactTitle"]
        if fft not in ch["funFacts"]:
            funfact_mismatches.append({"day": day, "titles": ch["funFacts"], "assigned": fft})

        entry: dict = {"day": day}
        for slot, key in [("conversation", "conversation"), ("funFact", "funFact")]:
            commons = lesson[key]
            info = info_map.get(commons)
            if not info:
                problems.append({"day": day, "slot": slot, "issue": "missing_on_commons", "commons": commons})
                continue
            base = normalize_basename(info["sourceUrl"])
            if base in used_basenames or base in BLOCKED_BASENAMES:
                problems.append({"day": day, "slot": slot, "issue": "already_used", "commons": commons})
                continue
            if commons in seen_commons:
                problems.append({"day": day, "slot": slot, "issue": "duplicate_commons", "commons": commons})
                continue
            if base in seen_urls:
                problems.append({"day": day, "slot": slot, "issue": "duplicate_url", "commons": commons})
                continue
            seen_commons.add(commons)
            seen_urls.add(base)

            prefix = "ff-" if slot == "funFact" else ""
            obj: dict = {
                "id": slug_id(day, commons, prefix),
                "commons": commons,
                "alt": lesson[f"{slot}_alt"],
                "credit": f"{lesson[f'{slot}_credit']} — {info['author']} / {info['license']}, via Wikimedia Commons",
            }
            pos_key = f"{slot}_objectPosition"
            if pos_key in lesson:
                obj["objectPosition"] = lesson[pos_key]
            if slot == "funFact":
                obj = {"funFactTitle": fft, **obj}
            entry[slot if slot == "conversation" else "funFact"] = obj
        manifest.append(entry)

    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "lessons": len(manifest),
        "complete": sum(1 for e in manifest if "conversation" in e and "funFact" in e),
        "funfact_mismatches": funfact_mismatches,
        "problems": problems,
        "missing_commons": [p for p in problems if p["issue"] == "missing_on_commons"],
    }
    (ROOT / "scripts" / "_tmp_sources" / "manifest-build-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
