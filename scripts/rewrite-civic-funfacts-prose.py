#!/usr/bin/env python3
"""Rewrite civicContext + funFacts into thesis / support / summary prose."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Bosnia today: thesis + 2-3 support + summary. No colon-rant endings.
CIVIC = {
    0: {
        "title": "A state built so one entity can block the rest",
        "body": (
            "Bosnia and Herzegovina’s postwar constitution makes national decision-making easy to block. "
            "Dayton divided the country into two entities, the Federation of Bosnia and Herzegovina and Republika Srpska, and many state decisions require agreement across that structure. "
            "The design helped stop the war, but it also lets obstruction at entity level delay reforms needed for EU accession. "
            "Learning the language therefore starts inside a country whose basic map is still a postwar power-sharing machine."
        ),
        "learnMore": {
            "label": "Wikipedia: Political divisions of Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Political_divisions_of_Bosnia_and_Herzegovina",
        },
    },
    1: {
        "title": "International oversight still sits above elected offices",
        "body": (
            "Bosnia and Herzegovina still has an internationally appointed High Representative with powers that can override local politics. "
            "The Office of the High Representative was created after the 1995 Dayton Peace Agreement to oversee civilian implementation of the deal. "
            "Under the Bonn Powers, that office can impose laws and remove public officials. "
            "In plain terms, final legal authority does not always rest with voters and elected institutions alone."
        ),
        "learnMore": {
            "label": "Wikipedia: High Representative for Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/High_Representative_for_Bosnia_and_Herzegovina",
        },
    },
    2: {
        "title": "Who is allowed to hold the highest offices",
        "body": (
            "Bosnia and Herzegovina’s constitution still blocks some citizens from the highest state offices because of ethnicity. "
            "Key posts such as the tripartite Presidency and seats in the House of Peoples are reserved for Bosniacs, Croats, and Serbs as constituent peoples. "
            "Jews, Roma, and other citizens outside those labels cannot hold those offices. "
            "The European Court of Human Rights ruled against that exclusion in Sejdić and Finci in 2009, and the judgment has still not been fully implemented."
        ),
        "learnMore": {
            "label": "Wikipedia: Sejdić and Finci v. Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Sejdi%C4%87_and_Finci_v._Bosnia_and_Herzegovina",
        },
    },
    3: {
        "title": "A currency without normal monetary freedom",
        "body": (
            "Daily life in Bosnia and Herzegovina runs on a currency system that limits national monetary freedom by design. "
            "The convertible mark is managed through a currency-board arrangement tied to the euro. "
            "That setup helps keep prices more stable, but it also means the state cannot run flexible monetary policy the way many countries do. "
            "Café prices and wages therefore sit inside a postwar economic structure that traded policy freedom for stability."
        ),
        "learnMore": {
            "label": "Wikipedia: Bosnia and Herzegovina convertible mark",
            "url": "https://en.wikipedia.org/wiki/Bosnia_and_Herzegovina_convertible_mark",
        },
    },
    4: {
        "title": "Three presidents share one top office",
        "body": (
            "Bosnia and Herzegovina’s top executive is split along ethnic lines by design. "
            "The Presidency has three members, one Bosniak, one Croat, and one Serb, under the Dayton settlement that ended the war. "
            "That shared office is meant to keep each constituent people represented at the highest level of the state. "
            "Family talk at a café table therefore happens in a country where even the top job is a three-person arrangement, not a single national president."
        ),
        "learnMore": {
            "label": "Wikipedia: Presidency of Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Presidency_of_Bosnia_and_Herzegovina",
        },
    },
    5: {
        "title": "Mostar went twelve years without local elections",
        "body": (
            "Mostar is a map lesson and a civic warning at the same time. "
            "Disputes over ethnically engineered election rules left the city without local elections from 2008 to 2020. "
            "Ordinary municipal democracy froze while courts and politicians fought over power-sharing formulas. "
            "Asking where Mostar is on the map also means remembering that postwar rules can stop a city from voting for more than a decade."
        ),
        "learnMore": {
            "label": "Wikipedia: Mostar",
            "url": "https://en.wikipedia.org/wiki/Mostar",
        },
    },
    6: {
        "title": "A country with almost no sea door of its own",
        "body": (
            "Bosnia and Herzegovina has almost no independent door to the sea. "
            "Its only coastline is the short stretch at Neum, and much Adriatic freight still depends on access through Croatia. "
            "Croatia’s Pelješac Bridge, opened in 2022, connects Croatian territory around Neum, while traders in Bosnia and Herzegovina still face foreign customs regimes rather than a full national deep-water port system. "
            "A weekend plan for the coast therefore sits inside a larger dependence on a neighbor for much of the country’s maritime trade access."
        ),
        "learnMore": {
            "label": "Wikipedia: Neum",
            "url": "https://en.wikipedia.org/wiki/Neum",
        },
    },
    7: {
        "title": "Two schools under one roof",
        "body": (
            "In parts of Bosnia and Herzegovina, children from different ethnic communities still attend school under a segregated model often called two schools under one roof. "
            "Students may share one building while using separate entrances, teachers, classrooms, and history lessons. "
            "International monitors have documented the practice for years as everyday discrimination in education. "
            "The result is that children in the same town can grow up learning different versions of the past inside the same walls."
        ),
        "learnMore": {
            "label": "Wikipedia: Two schools under one roof",
            "url": "https://en.wikipedia.org/wiki/Two_schools_under_one_roof",
        },
    },
    8: {
        "title": "Local food culture, imported staples",
        "body": (
            "Bosnia and Herzegovina’s food culture is local, but many grocery staples still come from abroad. "
            "After the war, fragmented farmland and weak agricultural investment slowed the recovery of domestic production. "
            "Bakeries and shops often stock flour, oil, dairy, and other basics from imports even while street pita culture thrives. "
            "Loving burek is part of daily life, and that daily life still depends on a supply chain that is only partly grown at home."
        ),
        "learnMore": {
            "label": "Wikipedia: Agriculture in Bosnia and Herzegovina",
            "url": "https://en.wikipedia.org/wiki/Agriculture_in_Bosnia_and_Herzegovina",
        },
    },
    9: {
        "title": "Tuzla’s factories closed faster than new jobs arrived",
        "body": (
            "Tuzla’s postwar story is one of industrial jobs disappearing faster than steady replacements arrived. "
            "The city was a major mining, chemical, and energy center that employed large parts of the region. "
            "After the war, many plants shrank or closed through damage, privatization, and market collapse, leaving long stretches of unemployment and insecure work. "
            "Markets and small shops kept daily shopping alive, but they did not replace the industrial wages that once supported whole neighborhoods."
        ),
        "learnMore": {
            "label": "Wikipedia: Tuzla",
            "url": "https://en.wikipedia.org/wiki/Tuzla",
        },
    },
    10: {
        "title": "Return and property claims are still unfinished",
        "body": (
            "Housing return after the war remains an unfinished national task in Bosnia and Herzegovina. "
            "Hundreds of thousands of people were displaced from their homes. "
            "Annex 7 of the Dayton Peace Agreement promised the right to return and reclaim property, but many restitution cases, damaged apartments, and contested ownership claims stayed unresolved for years. "
            "Even now, some families are still waiting for permanent housing solutions that the peace settlement said should arrive much sooner."
        ),
        "learnMore": {
            "label": "Wikipedia: Annex 7 of the Dayton Agreement",
            "url": "https://en.wikipedia.org/wiki/Annex_7_of_the_Dayton_Agreement",
        },
    },
}

# Fun facts for 8-10: each item = thesis + support + summary (complete sentences, no colon rants)
FUN = {
    8: [
        {
            "title": "No cheese in the word burek",
            "body": (
                "In Bosnia and Herzegovina, burek means a meat pita. "
                "Tourists often ask for burek sa sirom and reveal that they learned a different regional habit. "
                "Locals treat cheese pie as sirnica instead. "
                "If you want to sound local in this lesson, keep burek for meat and sirnica for cheese."
            ),
        },
        {
            "title": "Livanjski sir",
            "body": (
                "Livno is famous for highland cheese, not only for mountain views. "
                "Livanjski sir comes from western Bosnia pastures with a long dairy tradition. "
                "Emir’s postcard uses that fame to pull Ana’s food map outside one city street. "
                "When you learn food words today, remember that BiH dairy pride has regional addresses."
            ),
        },
        {
            "title": "Jogurt is a partner",
            "body": (
                "Warm burek often arrives with jogurt on purpose. "
                "The cool yogurt balances the hot pastry and slows the first bite. "
                "People treat the pair as a small everyday ritual, not a random side. "
                "If you order burek, expect jogurt to feel like part of the meal."
            ),
        },
        {
            "title": "Mrvica tax",
            "body": (
                "Any flaky pita near Mrvica becomes a shared meal. "
                "Crumbs fall, the cat arrives, and ownership of the snack gets renegotiated immediately. "
                "Ana learns food words while losing pastry in real time. "
                "In this course, feeding the café cat is unofficial vocabulary practice."
            ),
        },
    ],
    9: [
        {
            "title": "KM on the price tag",
            "body": (
                "Shop prices in Bosnia and Herzegovina are written in convertible marks, or KM. "
                "You do not need a finance lecture to use the currency in a market line. "
                "Ask Koliko košta?, hear a number, and pay. "
                "For this lesson, KM is simply the money word that makes shopping phrases real."
            ),
        },
        {
            "title": "Tuzla’s other fame",
            "body": (
                "Tuzla is a major northeast city with its own market rhythm. "
                "It is known for salt heritage and for a large urban center that is not Baščaršija. "
                "A shopping day there feels local and practical rather than tourist-postcard. "
                "That is why Emir uses Tuzla photos when Ana practices prodavnica language."
            ),
        },
        {
            "title": "Molim does double duty",
            "body": (
                "Molim is one of the most useful shop words in Bosnian. "
                "It can soften a request as please, and it can answer hvala as you’re welcome. "
                "Context tells you which meaning you just heard. "
                "Learn both uses now, because you will meet them in every polite purchase."
            ),
        },
        {
            "title": "Kesa is not optional",
            "body": (
                "Asking for a kesa is a normal end to a purchase. "
                "Fruit, bread, and bottles are easier to carry in a bag, and clerks expect the request. "
                "Saying Kesa, molim also gives you one more clean practice of molim. "
                "Leave the counter with the bag and the phrase both under control."
            ),
        },
    ],
    10: [
        {
            "title": "Upstairs from the kahva",
            "body": (
                "Living above a café is a practical city pattern in Bosnia and Herzegovina. "
                "The commute is short, the coffee smell is strong, and neighbors already know your order. "
                "Ana’s soba above Amira’s puts her inside that everyday arrangement. "
                "Home vocabulary in this lesson starts in a real upstairs room, not a textbook floor plan."
            ),
        },
        {
            "title": "Stećci near Stolac",
            "body": (
                "Radimlja near Stolac is one of Herzegovina’s clearest outdoor history classrooms. "
                "Medieval stećci tombstones stand in open light among stone-house country. "
                "Emir uses the place as a postcard that widens Ana’s idea of home beyond one rented room. "
                "When you learn soba and kuća today, Stolac reminds you that home also has deep local roots."
            ),
        },
        {
            "title": "Stan vs kuća",
            "body": (
                "Bosnian separates apartment living from house living with clear everyday words. "
                "Stan means apartment, and kuća means house. "
                "Ana has a soba, a room, inside Amira’s world either way. "
                "Keep the three terms straight so you can describe where someone actually lives."
            ),
        },
        {
            "title": "Cat property law",
            "body": (
                "Mrvica follows a simple property rule. "
                "If she sits on a pillow, the pillow has a new owner. "
                "Ana can claim the room with imam, but the cat still claims the soft furniture. "
                "In this lesson, home vocabulary includes negotiating space with one very confident mačka."
            ),
        },
    ],
}


def validate_block(text: str, label: str):
    assert "—" not in text and "–" not in text, label
    # allow rare colon in times/ratios only; ban colon-rant style by forbidding ': ' mid prose for civic/fun
    if ": " in text:
        raise AssertionError(f"colon rant in {label}: {text}")
    sentences = [s.strip() for s in text.replace("?", ".").replace("!", ".").split(".") if s.strip()]
    if not (4 <= len(sentences) <= 5):
        raise AssertionError(f"{label} expected 4-5 sentences, got {len(sentences)}: {sentences}")


def main():
    for day, civic in CIVIC.items():
        validate_block(civic["body"], f"civic-{day}")
        for base in (
            ROOT / f"content/book1/day-{day:02d}/chapter.json",
            ROOT / f"frontend/src/data/book1/day-{day:02d}/chapter.json",
        ):
            c = json.loads(base.read_text(encoding="utf-8"))
            old = c.get("civicContext") or {}
            c["civicContext"] = {
                "title": civic["title"],
                "body": civic["body"],
                "imageId": old.get("imageId"),
                "learnMore": old.get("learnMore") or civic["learnMore"],
            }
            if day in FUN:
                for fact in FUN[day]:
                    validate_block(fact["body"], f"fun-{day}-{fact['title']}")
                c["funFacts"] = FUN[day]
            base.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("updated", base)

    # CONTENT-STYLE recipe
    style = ROOT / "CONTENT-STYLE.md"
    text = style.read_text(encoding="utf-8")
    marker = "## Bosnia today and fun facts prose"
    recipe = """## Bosnia today and fun facts prose

Write complete thoughts. Do not rant in fragments, slogan stubs, or colon-led trailers.

**Shape for every `civicContext.body` and every fun-fact `body`:**

1. **Thesis** — one clear first sentence that states the point
2. **Support** — two or three sentences with concrete facts or examples
3. **Summary** — one closing sentence that lands the idea

Keep the lesson link light and factual. Prefer plain speech over clever asides.
"""
    if marker in text:
        # replace existing section if present
        pass
    else:
        # insert after chapter checklist item about bosnia today / before Quiz quality
        needle = "## Quiz quality"
        if needle in text:
            text = text.replace(needle, recipe + "\n" + needle)
        else:
            text += "\n" + recipe
        style.write_text(text, encoding="utf-8")
        print("updated CONTENT-STYLE.md")

    guide = ROOT / "content/book1/LESSON_AUTHORING_GUIDE.md"
    g = guide.read_text(encoding="utf-8")
    if "Thesis → support → summary" not in g:
        g = g.replace(
            "- Every drafted lesson needs `civicContext`",
            "- Civic and fun-fact bodies use **Thesis → support → summary** (complete sentences, no colon-rant endings)\n- Every drafted lesson needs `civicContext`",
        )
        guide.write_text(g, encoding="utf-8")
        print("updated LESSON_AUTHORING_GUIDE.md")
        fg = ROOT / "frontend/src/data/book1/LESSON_AUTHORING_GUIDE.md"
        if fg.exists():
            fg.write_text(g, encoding="utf-8")


if __name__ == "__main__":
    main()
