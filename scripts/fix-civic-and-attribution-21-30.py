#!/usr/bin/env python3
"""Fix Lessons 21-30 civic prose and restore Commons-based image attributions."""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "LearnBosnianBot/1.0 (educational content attribution)"

CIVICS = {
    21: {
        "title": "Private rural bus lines collapse when routes stop paying",
        "body": (
            "Rural public transport in Bosnia and Herzegovina still depends heavily on private operators rather than a stable statewide network. "
            "When a mountain or village route stops turning a profit, companies cancel the line instead of absorbing the loss. "
            "Many smaller places then lose daily service with no public replacement on the same timetable. "
            "The result is a patchwork map where market math decides who can still reach work, school, or a clinic by bus."
        ),
        "learnMore": {
            "label": "Wikipedia article about transport in Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Transport_in_Bosnia_and_Herzegovina",
        },
        "quiz": {
            "question": "What happens when private rural bus lines stop paying?",
            "options": [
                "Operators often cancel the route with no public replacement",
                "The state always adds a free replacement coach",
                "Every village gains a new rail link",
                "Ticket prices fall to zero by law",
            ],
            "correctIndex": 0,
            "explanation": "Unprofitable private rural lines are often canceled, leaving villages without reliable public transport.",
            "skill": "culture",
        },
    },
    22: {
        "title": "Winding roads and fast driving keep traffic deaths high",
        "body": (
            "Road travel in Bosnia and Herzegovina remains far more dangerous than the European average. "
            "Mountain corridors use tight curves, mixed truck traffic, and limited overtaking space. "
            "High speeds among young drivers on those routes raise crash risk further. "
            "WHO country profiles still place the national traffic death rate among the worst in Europe, so a day trip can sit on infrastructure that has not caught up with safety needs."
        ),
        "learnMore": {
            "label": "WHO road safety country profile for Bosnia and Herzegovina",
            "url": "https://www.who.int/publications/m/item/road-safety-bih-2023-country-profile",
        },
        "quiz": {
            "question": "Why do traffic death rates stay high on many Bosnian roads?",
            "options": [
                "Winding mountain routes combine with fast and risky driving",
                "All highways are finished and fully lit",
                "Cars are banned from mountain roads",
                "Speed limits are enforced on every curve",
            ],
            "correctIndex": 0,
            "explanation": "Sharp mountain roads plus fast driving help keep traffic deaths among the highest in Europe.",
            "skill": "culture",
        },
    },
    23: {
        "title": "BHRT debt and RTRS fee withholding keep Eurovision closed",
        "body": (
            "Bosnia and Herzegovina is absent from Eurovision because the European Broadcasting Union sanctioned the state broadcaster BHRT over unpaid membership debts. "
            "Those debts grew after Radio-Television of Republika Srpska (RTRS) withheld large shares of the television licence fee that law says should reach BHRT. "
            "Courts have ordered repayment, yet years of missing transfers left BHRT unable to clear what it owes the EBU. "
            "Until that funding fight is settled, the country stays locked out of the contest and other EBU services."
        ),
        "learnMore": {
            "label": "Eurovoix report on BHRT debts, RTRS fees, and EBU sanctions",
            "url": "https://eurovoix.com/2026/02/27/bhrt-halts-most-programming-as-debts-grow/",
        },
        "quiz": {
            "question": "Why does BHRT remain sanctioned and keep the country out of Eurovision?",
            "options": [
                "Unpaid EBU debts tied to withheld RTRS licence-fee transfers",
                "A permanent ban on Balkan music contests",
                "A lack of singers in Sarajevo",
                "A rule against public broadcasters",
            ],
            "correctIndex": 0,
            "explanation": "EBU sanctions follow unpaid BHRT debts that grew as RTRS withheld licence-fee money owed to the state broadcaster.",
            "skill": "culture",
        },
    },
    24: {
        "title": "Jahorina booms while Bjelašnica and Igman Olympic sites lag",
        "body": (
            "The 1984 Winter Olympics left Bosnia and Herzegovina with ski venues that later split across entity lines. "
            "Jahorina hosted women's alpine events and now sits in Republika Srpska, where postwar investment rebuilt lifts, hotels, and a busy tourist season. "
            "Bjelašnica and Igman hosted men's events on what became Federation territory and took heavier wartime damage with weaker recovery spending. "
            "The same Games therefore left one Olympic mountain as a major ski destination while neighboring host slopes still look neglected."
        ),
        "learnMore": {
            "label": "Wikipedia article about Jahorina",
            "url": "https://en.wikipedia.org/wiki/Jahorina",
        },
        "quiz": {
            "question": "What civic gap does the Olympic ski comparison describe?",
            "options": [
                "Jahorina grew into a major resort while Bjelašnica and Igman lagged after the war",
                "All three mountains closed permanently in 1985",
                "Only Igman hosts World Cup races every month",
                "Ski tourism is banned in Republika Srpska",
            ],
            "correctIndex": 0,
            "explanation": "Postwar investment favored Jahorina in Republika Srpska while Bjelašnica and Igman on the Federation side recovered more slowly.",
            "skill": "culture",
        },
    },
    25: {
        "title": "The 2013 JMBG deadlock blocked newborn passports and care abroad",
        "body": (
            "In 2013 a Constitutional Court ruling and a parliamentary fight over the unique citizen number (JMBG) froze new registrations in Bosnia and Herzegovina. "
            "Newborns without that number could not obtain passports or the papers needed for medical travel. "
            "Cases such as Belmina Ibrisević, who needed treatment abroad, turned the paperwork fight into a public emergency and sparked the Baby Revolution protests. "
            "Ethnic bargaining over ID rules therefore put infant health behind political deadlock."
        ),
        "learnMore": {
            "label": "Al Jazeera opinion on Bosnia's babies in limbo",
            "url": "https://www.aljazeera.com/opinions/2013/6/20/bosnias-babies-in-limbo",
        },
        "quiz": {
            "question": "What was the 2013 JMBG crisis about?",
            "options": [
                "Political deadlock left newborns without ID numbers needed for passports and care abroad",
                "A new tax on all baby names",
                "A hospital strike over café hours",
                "A ban on veterinary clinics",
            ],
            "correctIndex": 0,
            "explanation": "Without JMBG numbers, newborns could not get passports or travel for urgent treatment until politicians settled the law.",
            "skill": "culture",
        },
    },
    26: {
        "title": "Returnees in Republika Srpska still face hostile local pressure",
        "body": (
            "Minority return to Republika Srpska remains unfinished three decades after the war. "
            "Bosniak returnees often meet segregated schooling, job barriers, and political rhetoric that treats them as outsiders in their own towns. "
            "International monitors keep documenting property disputes and intimidation around returnee communities. "
            "Legal rights to reclaim a house therefore collide with daily pressure that shrinks who can safely stay."
        ),
        "learnMore": {
            "label": "Wikipedia article on return of refugees and IDPs in Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Return_of_refugees_and_IDPs_in_Bosnia_and_Herzegovina",
        },
        "quiz": {
            "question": "What civic pressure does this housing lesson highlight?",
            "options": [
                "Returnee minorities in Republika Srpska still face hostile local conditions",
                "Every returnee receives free luxury flats",
                "Housing markets ignore wartime history",
                "Entity borders ban all rentals",
            ],
            "correctIndex": 0,
            "explanation": "Bosniak and other minority returnees in Republika Srpska still report hostility, segregation, and local pressure around daily life.",
            "skill": "culture",
        },
    },
    27: {
        "title": "Republika Srpska leaders keep challenging state courts and police",
        "body": (
            "Leaders in Republika Srpska repeatedly push secessionist rhetoric against the shared state of Bosnia and Herzegovina. "
            "Entity officials have refused or delayed compliance with state-level court decisions and have built parallel political calendars. "
            "Challenges to joint police and judicial authority keep constitutional fights in the daily news. "
            "Work and school routines therefore run under a government layer that still contests the state's right to decide."
        ),
        "learnMore": {
            "label": "Wikipedia article on proposed secession of Republika Srpska",
            "url": "https://en.wikipedia.org/wiki/Proposed_secession_of_Republika_Srpska",
        },
        "quiz": {
            "question": "What civic topic does this lesson highlight?",
            "options": [
                "Republika Srpska leaders challenge state judicial and police authority while floating secession",
                "Entity leaders dissolved all schools",
                "State courts control every local café menu",
                "Police forces merged into one EU agency",
            ],
            "correctIndex": 0,
            "explanation": "Secessionist rhetoric and resistance to state-level courts and police remain a documented structural pressure.",
            "skill": "culture",
        },
    },
    28: {
        "title": "Međugorje drives Croatian identity tourism without full miracle recognition",
        "body": (
            "Međugorje became a mass pilgrimage site after claims of Marian apparitions began in 1981. "
            "The Catholic Church has allowed pastoral care and organized pilgrimages while withholding a classic declaration that the apparitions are authenticated supernatural miracles. "
            "Hotels, buses, and shrine commerce still fill Herzegovina with Croatian and international Catholic visitors. "
            "Local identity and tourism therefore lean on a shrine whose spiritual status remains carefully limited by Rome."
        ),
        "learnMore": {
            "label": "Wikipedia article on Međugorje",
            "url": "https://en.wikipedia.org/wiki/Medjugorje",
        },
        "quiz": {
            "question": "What civic topic ties to Herzegovina pilgrimage tourism?",
            "options": [
                "Međugorje draws huge pilgrim traffic while the Church stops short of full miracle authentication",
                "The Vatican named Međugorje a mandatory annual pilgrimage for all Catholics",
                "Pilgrimage buses are banned in Herzegovina",
                "Međugorje has no hotels or visitors",
            ],
            "correctIndex": 0,
            "explanation": "Pilgrimage tourism and Croatian identity commerce grew around Međugorje even though Rome has not fully authenticated the apparitions as miracles.",
            "skill": "culture",
        },
    },
    29: {
        "title": "Genocide denial and war-criminal glorification remain elite politics",
        "body": (
            "Denial of the Srebrenica genocide remains common among nationalist political elites in Bosnia and Herzegovina. "
            "Convicted war criminals are still praised in murals, rallies, and campaign messaging. "
            "Tribunal judgments and memorial facts collide with public rhetoric that minimizes or rejects the genocide finding. "
            "Memory of the worst crime of the war therefore stays contested in everyday politics rather than settled history."
        ),
        "learnMore": {
            "label": "Wikipedia article on Bosnian genocide denial",
            "url": "https://en.wikipedia.org/wiki/Bosnian_genocide_denial",
        },
        "quiz": {
            "question": "What civic pressure does this lesson highlight?",
            "options": [
                "Nationalist elites still deny the Srebrenica genocide and glorify convicted war criminals",
                "All parties accept tribunal judgments without debate",
                "Memorial sites are closed to the public",
                "War crimes trials never took place",
            ],
            "correctIndex": 0,
            "explanation": "Genocide denial and glorification of convicted war criminals remain widespread in nationalist elite politics.",
            "skill": "culture",
        },
    },
    30: {
        "title": "Sanctioned Night Wolves still parade through Republika Srpska",
        "body": (
            "The Russian Night Wolves motorcycle club is linked to the Kremlin and faces United States and European Union sanctions. "
            "Club members and a local branch still appear at Republika Srpska events in Banja Luka and related entity-day parades. "
            "Political hosts treat the rides as welcome spectacle even while state security concerns restrict some Russian leaders from entry. "
            "Authoritarian soft power therefore parks on entity streets inside a country that Dayton framed as one democratic state."
        ),
        "learnMore": {
            "label": "RFE/RL report on Night Wolves in Republika Srpska",
            "url": "https://www.rferl.org/a/russia-motorcycle-night-wolves-republika-srpska/32215945.html",
        },
        "quiz": {
            "question": "What civic topic appears in this finale?",
            "options": [
                "Sanctioned Night Wolves still parade with political welcome in Republika Srpska",
                "All motorcycle clubs are banned nationwide",
                "Night Wolves only appear in Sarajevo cafés",
                "EU sanctions dissolved the club worldwide",
            ],
            "correctIndex": 0,
            "explanation": "Despite international sanctions, Night Wolves members continue to appear at Republika Srpska political events.",
            "skill": "culture",
        },
    },
}

# imageId -> Commons File: title to attribute as polygon source
IMAGE_SOURCES = {
    21: {
        "weekend-map": "File:Una near Bihać 2.jpg",
        "una-postcard": "File:Una River Bihac 2.jpg",
        "cafe-plan": "File:Bosnian coffee.jpg",
        "civic-rural-bus": "File:Sarajevo bus station 2.jpg",
    },
    22: {
        "travnik-mosque": "File:Travnik mosque 03.jpg",
        "travnik-street": "File:Travnik Altstadt 3.JPG",
        "travnik-tower": "File:Travnik fortress.jpg",
        "civic-winding-road": "File:Highway banja luka gradiska1.JPG",
    },
    23: {
        "daily-cafe": "File:Bosnian coffee.jpg",
        "zenica-postcard": "File:Theater in Zenica from side.jpg",
        "activity-cards": "File:Bilino Polje Stadium Zenica.jpg",
        "civic-eurovision-debt": "File:National Museum of Bosnia and Herzegovina.jpg",
    },
    24: {
        "una-river": "File:Štrbački buk.jpg",
        "bjelasnica-ridge": "File:Bjelašnica2.jpg",
        "jahorina-ski": "File:Jahorina ski-lifts.jpg",
        "civic-olympic-ski-gap": "File:Jahorina mountain 2017.jpg",
    },
    25: {
        "clinic-door": "File:Dubrave Gornje - Pharmacy (2019).jpg",
        "pharmacy-shelf": "File:Dubrave Gornje - Pharmacy (2019).jpg",
        "mrvica-vet": "File:Cat November 2010-1a.jpg",
        "civic-jmbg": "File:Parliament of Bosnia and Herzegovina.jpg",
    },
    26: {
        "flat-kitchen": "File:Kitchen.jpg",
        "apartment-door": "File:Door in Sarajevo.jpg",
        "furniture-corner": "File:Living room.jpg",
        "civic-returnee-pressure": "File:Destroyed house in Bosnia.jpg",
    },
    27: {
        "guide-badge": "File:Sarajevo map.jpg",
        "classroom-desk": "File:Classroom.jpg",
        "office-tram": "File:Sarajevo tram.jpg",
        "civic-rs-secession": "File:Banja Luka downtown.jpg",
    },
    28: {
        "stari-most": "File:Mostar Stari Most BW 2024-10-01 12-58-38.jpg",
        "neretva-green": "File:Neretva River in Mostar.jpg",
        "mostar-old-town": "File:Mostar Old Town Panorama 2007.jpg",
        "civic-medjugorje": "File:Cross on Križevac in Međugorje.jpg",
    },
    29: {
        "postcard-desk": "File:Postcard.jpg",
        "stamp-envelope": "File:Envelope.jpg",
        "ferhadija-letter": "File:Ferhadija Street Sarajevo.jpg",
        "civic-genocide-denial": "File:Srebrenica massacre memorial gravestones 2009 3.jpg",
    },
    30: {
        "party-table": "File:Birthday cake.jpg",
        "cake-heist": "File:Cat November 2010-1a.jpg",
        "friends-toast": "File:Toast (drink).jpg",
        "civic-night-wolves": "File:Banja Luka downtown.jpg",
    },
}

# Better-validated commons titles tried in order per image id (fallbacks)
FALLBACKS = {
    "cafe-plan": [
        "File:Bosanska kahva.jpg",
        "File:Coffee in Sarajevo.jpg",
        "File:Kahva.jpg",
    ],
    "daily-cafe": [
        "File:Bosanska kahva.jpg",
        "File:Coffee in Sarajevo.jpg",
    ],
    "travnik-tower": [
        "File:Travnik Castle.jpg",
        "File:Stari grad Travnik.jpg",
        "File:Travnik.jpg",
    ],
    "activity-cards": [
        "File:Bilino Polje.jpg",
        "File:NK Čelik Zenica.jpg",
        "File:Zenica.jpg",
    ],
    "civic-eurovision-debt": [
        "File:RTV Building Sarajevo.jpg",
        "File:Sarajevo City Hall.jpg",
        "File:Vijećnica.jpg",
    ],
    "una-river": [
        "File:Strbacki buk.jpg",
        "File:Una River.jpg",
        "File:Una near Bihać 2.jpg",
    ],
    "flat-kitchen": [
        "File:Kitchen interior.jpg",
        "File:Modern kitchen.jpg",
    ],
    "apartment-door": [
        "File:Wooden door.jpg",
        "File:Apartment door.jpg",
        "File:Door.jpg",
    ],
    "furniture-corner": [
        "File:Sofa.jpg",
        "File:Living room interior.jpg",
    ],
    "civic-returnee-pressure": [
        "File:War damaged house Bosnia.jpg",
        "File:Destroyed house in Mostar.jpg",
        "File:Ruined house.jpg",
    ],
    "guide-badge": [
        "File:Tourist map.jpg",
        "File:Map of Sarajevo.jpg",
        "File:OpenStreetMap.jpg",
    ],
    "classroom-desk": [
        "File:School desk.jpg",
        "File:Empty classroom.jpg",
    ],
    "office-tram": [
        "File:Tram in Sarajevo.jpg",
        "File:Sarajevo tram Line 3.jpg",
        "File:Sarajevo tram.jpg",
    ],
    "civic-rs-secession": [
        "File:Banja Luka.jpg",
        "File:Krajina square Banja Luka.jpg",
        "File:Banja Luka City Hall.jpg",
    ],
    "neretva-green": [
        "File:Neretva.jpg",
        "File:Neretva Mostar.jpg",
        "File:Mostar Neretva.jpg",
    ],
    "postcard-desk": [
        "File:Writing desk.jpg",
        "File:Desk with paper.jpg",
        "File:Fountain pen and paper.jpg",
    ],
    "stamp-envelope": [
        "File:Airmail envelope.jpg",
        "File:Postage stamp.jpg",
        "File:Letter and stamp.jpg",
    ],
    "ferhadija-letter": [
        "File:Ferhadija.jpg",
        "File:Sarajevo Ferhadija.jpg",
        "File:Pedestrian street Sarajevo.jpg",
    ],
    "party-table": [
        "File:Cake on table.jpg",
        "File:Party table.jpg",
        "File:Celebration cake.jpg",
    ],
    "friends-toast": [
        "File:Cheers.jpg",
        "File:People toasting.jpg",
        "File:Raising glasses.jpg",
    ],
    "civic-night-wolves": [
        "File:Banja Luka.jpg",
        "File:Motorcycles.jpg",
        "File:Motorcycle parade.jpg",
    ],
    "mrvica-vet": [
        "File:Domestic cat.jpg",
        "File:Cat portrait.jpg",
    ],
    "cake-heist": [
        "File:Domestic cat.jpg",
        "File:Cat portrait.jpg",
    ],
    "pharmacy-shelf": [
        "File:Pharmacy.jpg",
        "File:Medicine bottles.jpg",
    ],
    "clinic-door": [
        "File:Clinic.jpg",
        "File:Hospital entrance.jpg",
        "File:Dubrave Gornje - Pharmacy (2019).jpg",
    ],
    "civic-jmbg": [
        "File:Parliament building Sarajevo.jpg",
        "File:Bosnia and Herzegovina parliament.jpg",
        "File:Building of the Parliamentary Assembly of Bosnia and Herzegovina.jpg",
    ],
}


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def commons_info(title: str) -> dict | None:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime",
            "iiurlwidth": 1600,
            "format": "json",
        }
    )
    data = get_json("https://commons.wikimedia.org/w/api.php?" + q)
    page = next(iter(data["query"]["pages"].values()))
    if page.get("missing") is not None or "imageinfo" not in page:
        return None
    ii = page["imageinfo"][0]
    meta = ii.get("extmetadata") or {}

    def g(k: str) -> str:
        return re.sub("<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()

    author = g("Artist") or g("Credit") or "Wikimedia Commons"
    author = re.sub(r"\s+", " ", author)[:90]
    license_ = g("LicenseShortName") or g("License") or "CC"
    url = (ii.get("url") or "").split("?")[0]
    if not url:
        return None
    page_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(
        title.replace(" ", "_")
    )
    return {
        "author": author,
        "license": license_,
        "sourceUrl": url,
        "pageUrl": page_url,
        "commonsTitle": title,
    }


def search_commons(query: str, limit: int = 5) -> list[str]:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": limit,
            "format": "json",
        }
    )
    data = get_json("https://commons.wikimedia.org/w/api.php?" + q)
    return [h["title"] for h in data["query"]["search"]]


def resolve_source(image_id: str, preferred: str) -> dict:
    candidates = [preferred] + FALLBACKS.get(image_id, [])
    # also try a plain search from the image id words
    try:
        candidates.extend(search_commons(image_id.replace("-", " ") + " Bosnia", 4))
    except Exception:
        pass
    seen = set()
    for title in candidates:
        if not title or title in seen:
            continue
        seen.add(title)
        if not title.startswith("File:"):
            title = "File:" + title
        info = commons_info(title)
        if info:
            return info
    raise RuntimeError(f"No Commons source found for {image_id} (tried {preferred})")


def apply_credit(image: dict, info: dict) -> None:
    fname = info["commonsTitle"].replace("File:", "")
    image["sourceUrl"] = info["sourceUrl"]
    image["pageUrl"] = info["pageUrl"]
    image["author"] = info["author"]
    image["license"] = info["license"]
    image["credit"] = (
        f"Polygon painting based on the photo {fname}. "
        f"{info['author']} / Wikimedia Commons ({info['license']})"
    )


def patch_civic_quiz(chapter: dict, day: int) -> None:
    quiz_spec = CIVICS[day]["quiz"]
    questions = chapter.get("sectionQuiz", {}).get("questions", [])
    # replace existing civic-ish question or append
    civic_re = re.compile(
        r"civic|sanction|Eurovision|BHRT|bus lines|traffic|Jahorina|JMBG|returnee|"
        r"secession|Međugorje|Medjugorje|genocide|Night Wolves|Olympic|rural",
        re.I,
    )
    replaced = False
    for i, q in enumerate(questions):
        blob = json.dumps(q, ensure_ascii=False)
        if civic_re.search(blob) and q.get("skill") in (None, "culture", "listening"):
            # prefer culture civic items
            if "culture" in blob.lower() or civic_re.search(q.get("question", "")):
                questions[i] = {
                    "id": q.get("id", f"q-civic-{day}"),
                    **quiz_spec,
                }
                replaced = True
                break
    if not replaced:
        # find last culture question or append
        for i, q in enumerate(questions):
            if q.get("skill") == "culture" and civic_re.search(q.get("question", "")):
                questions[i] = {"id": q.get("id", f"q-civic-{day}"), **quiz_spec}
                replaced = True
                break
    if not replaced:
        questions.append({"id": f"q-civic-{day}", **quiz_spec})
    chapter["sectionQuiz"]["questions"] = questions


def main() -> None:
    cache: dict[str, dict] = {}
    for day in range(21, 31):
        path = ROOT / "content" / "book1" / f"day-{day:02d}" / "chapter.json"
        chapter = json.loads(path.read_text(encoding="utf-8"))
        civic = CIVICS[day]
        chapter["civicContext"] = {
            "title": civic["title"],
            "body": civic["body"],
            "imageId": chapter["civicContext"]["imageId"],
            "learnMore": civic["learnMore"],
        }
        patch_civic_quiz(chapter, day)

        sources = IMAGE_SOURCES[day]
        for image in chapter["images"]:
            preferred = sources[image["id"]]
            key = preferred
            if key not in cache:
                print(f"resolve day {day} {image['id']} <- {preferred}")
                try:
                    cache[key] = resolve_source(image["id"], preferred)
                except Exception as e:
                    # last resort search by alt keywords
                    print("  retry search", e)
                    hits = search_commons(image["id"].replace("-", " "), 8)
                    found = None
                    for h in hits:
                        found = commons_info(h)
                        if found:
                            break
                    if not found:
                        raise
                    cache[key] = found
            apply_credit(image, cache[key])
            print("  ->", image["credit"][:110])

        path.write_text(
            json.dumps(chapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("wrote", path)


if __name__ == "__main__":
    main()
