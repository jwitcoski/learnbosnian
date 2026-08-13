#!/usr/bin/env python3
"""Rewrite Lessons 1–10 funFacts to thesis / support / summary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FUN = {
    1: [
        {
            "title": "Baščaršija means main market",
            "body": (
                "Baščaršija is not just a pretty old-town label. "
                "The name comes from Turkish roots for the chief marketplace. "
                "Craft shops, cafés, and copper work still fill those streets today. "
                "When Ana learns greetings here, she is practicing language in a living market, not a museum set."
            ),
        },
        {
            "title": "One letter, one sound",
            "body": (
                "Bosnian spelling is mostly phonetic, which helps beginners a lot. "
                "What you see is usually what you say once the special letters click. "
                "Letters like č, ć, š, ž, and đ each carry one clear sound. "
                "That predictability is why Lesson 1 spends real time on the alphabet before long conversations."
            ),
        },
        {
            "title": "Cats of the čaršija",
            "body": (
                "Sarajevo’s old town is famous for friendly street cats. "
                "They claim doorsteps, café chairs, and warm stone with total confidence. "
                "Mrvica is fictional, but her attitude matches that local habit. "
                "If a cat joins your language practice in Baščaršija, you are having a very Sarajevo lesson."
            ),
        },
    ],
    2: [
        {
            "title": "Sebilj means a public fountain",
            "body": (
                "Sebilj started as a practical word for a public fountain kiosk. "
                "The term comes from Ottoman Turkish roots for water offered to everyone in the square. "
                "Sarajevo’s Sebilj is now a city icon and a favorite meeting point. "
                "When Emir says to meet kod Sebilja, he is using landmark language locals still rely on."
            ),
        },
        {
            "title": "sam / si / je are clitics",
            "body": (
                "The short biti forms sam, si, and je behave like little grammar hitchhikers. "
                "In longer sentences they often like the second position. "
                "Beginners do not need the full theory on day one. "
                "For now, keep clear Ja sam patterns and let fluency grow later."
            ),
        },
        {
            "title": "Drago mi je is warm, not stiff",
            "body": (
                "Drago mi je is the standard way to say nice to meet you. "
                "It sounds warm in cafés, offices, and first introductions. "
                "Ana and Emir use it because real meetings need more than a name. "
                "Learn it as a ready chunk, then say it like you mean the welcome."
            ),
        },
        {
            "title": "Pigeons optional, rendezvous required",
            "body": (
                "Meeting kod Sebilja is local shorthand for a reliable rendezvous. "
                "Landmarks beat street numbers when your phone battery dies. "
                "Pigeons and photos are optional extras around the fountain. "
                "The useful skill is knowing how Bosnians point to a place everyone can find."
            ),
        },
    ],
    3: [
        {
            "title": "kahva with an h",
            "body": (
                "In much of Bosnia and Herzegovina you will hear and see kahva. "
                "Related standards nearby may prefer kava or kafa. "
                "This course stays with the Bosnian café form you meet at Amira’s. "
                "Spell it with the h so your notebook matches the tray in front of you."
            ),
        },
        {
            "title": "Fildžan is tiny on purpose",
            "body": (
                "A fildžan is small because the coffee ritual is meant to last. "
                "You sip, talk, and pour again from the džezva. "
                "Quantity is not the point of Bosnian coffee service. "
                "Company is the point, and the tiny cup keeps you at the table."
            ),
        },
        {
            "title": "Lokum on the tray",
            "body": (
                "Sweet lokum often arrives with Bosnian coffee. "
                "Saying yes to one piece is friendly and normal. "
                "Eating the whole plate without asking is bold. "
                "Treat lokum as part of the coffee welcome, not a free dessert challenge."
            ),
        },
        {
            "title": "Mrvica means little crumb",
            "body": (
                "Mrvica literally points to a little crumb. "
                "It is a fitting name for a café cat who believes every table is hers. "
                "She appears whenever sugar, lokum, or attention is available. "
                "In this course, her name is both vocabulary and a warning about unattended snacks."
            ),
        },
    ],
    4: [
        {
            "title": "Baba and djed",
            "body": (
                "Baba and djed are everyday words for grandmother and grandfather. "
                "Families may use affectionate variants, but these two open many stories. "
                "Learners meet them early because family talk starts with the oldest generation. "
                "Learn baba and djed first, then build the rest of the family tree around them."
            ),
        },
        {
            "title": "Prijatelj vs prijateljica",
            "body": (
                "Bosnian marks the gender of friend with two clear forms. "
                "Prijatelj is masculine, and prijateljica is feminine. "
                "Ana calls Emir prijatelj and Amira prijateljica for that reason. "
                "Get the pair right early, because real friendships need the right word from day one."
            ),
        },
        {
            "title": "Mrvica means little crumb",
            "body": (
                "Mrvica means little crumb, and the café cat lives up to it. "
                "She believes every lap and every lokum crumb is hers. "
                "Family vocabulary in this lesson somehow includes one very pushy mačka. "
                "If she claims Ana, Emir will treat that adoption as official."
            ),
        },
        {
            "title": "Chosen family at the table",
            "body": (
                "Calling café regulars porodica is half joke and half truth. "
                "People share news, chairs, and kahva until the table feels like home. "
                "Warmth is part of the language lesson, not an extra decoration. "
                "When Ana uses family words at Amira’s, she is naming both blood relatives and chosen company."
            ),
        },
    ],
    5: [
        {
            "title": "Mostar means the bridge keeper",
            "body": (
                "Mostar’s name is tied to the bridge and the people who kept the crossing. "
                "The root links to most, the word for bridge. "
                "Stari Most is the famous postcard, but the whole old town carries the story. "
                "Remember the name’s meaning when you pin Mostar on the map in this lesson."
            ),
        },
        {
            "title": "Ovdje vs tamo",
            "body": (
                "Bosnian learners often mix ovdje and tamo. "
                "Ovdje means here, and tamo means there. "
                "A simple hand habit helps keep them straight, with your palm down for ovdje and a point away for tamo. "
                "Practice the pair out loud until the gestures and words stay attached."
            ),
        },
        {
            "title": "Kod plus a name",
            "body": (
                "Kod Amire is how you say you are at Amira’s place. "
                "Bosnian uses kod plus a person for homes, shops, and cafés all the time. "
                "It is shorter and more natural than building a full address every visit. "
                "Learn the pattern now, because you will reuse it for almost every friendly destination."
            ),
        },
        {
            "title": "Spoiler, softly",
            "body": (
                "Book 1 saves the real Mostar trip for later on purpose. "
                "Lesson 5 only plants the map pin and the question Gdje je Mostar? "
                "Emir’s grin is the soft spoiler that the journey is coming. "
                "For today, find the city on the map and let the visit wait."
            ),
        },
    ],
    6: [
        {
            "title": "Travnik and Vlašić",
            "body": (
                "Travnik has its own central-Bosnia weight on the map. "
                "It was a major Ottoman administrative centre under Mount Vlašić. "
                "Its sahat-kula still marks the town’s skyline. "
                "When you practice clock time, remember that BiH history is not only a Sarajevo footnote."
            ),
        },
        {
            "title": "Many sahat-kule",
            "body": (
                "Clock towers appear in towns across Bosnia and Herzegovina. "
                "Sarajevo and Travnik are only two of the places that kept a sahat-kula. "
                "Sarajevo’s tower is often remembered for once tracking lunar prayer time. "
                "That detail roots the question Koliko je sati in local history, not only in a classroom drill."
            ),
        },
        {
            "title": "Una mornings near Bihać",
            "body": (
                "In the northwest, the Una River runs clear past Bihać. "
                "Locals talk about jutro on the river with real affection. "
                "The feeling matches the love Sarajevo keeps for a slow kahva. "
                "Different place, same habit of starting the day gently."
            ),
        },
        {
            "title": "Neum touches the sea",
            "body": (
                "Bosnia and Herzegovina has a short Adriatic coastline at Neum. "
                "A plan for sutra can mean salt air, not only mountain towns. "
                "That matters when you practice danas and sutra as real calendar words. "
                "Time phrases feel more alive when they can point to an actual coast."
            ),
        },
    ],
    7: [
        {
            "title": "Jajce, town on a waterfall",
            "body": (
                "Jajce puts a waterfall inside ordinary town life. "
                "The Pliva River drops beside the old town in a rare urban cascade. "
                "The same place was also a medieval royal seat of the Bosnian kingdom. "
                "A review postcard from Jajce keeps both nature and history on Ana’s map."
            ),
        },
        {
            "title": "Blagaj and the Buna spring",
            "body": (
                "Blagaj is built around one of the region’s strongest karst springs. "
                "A Dervish tekija sits under a cliff where the Buna River bursts from the rock. "
                "The scene ties water, stone, and spiritual history into one view. "
                "Emir adds it to the review so BiH never shrinks to two tourist cities."
            ),
        },
        {
            "title": "Počitelj’s stone stack",
            "body": (
                "Počitelj climbs a Herzegovina hillside in stacked stone houses. "
                "A fortress silhouette watches over the old settlement. "
                "The town sits above the Neretva corridor as a preserved Ottoman-era place. "
                "One more postcard like this keeps Week 1 review geographically honest."
            ),
        },
        {
            "title": "Banja Luka on the mental map",
            "body": (
                "Banja Luka belongs on Ana’s mental map of the country. "
                "Farther north, the city spreads along the Vrbas with the Kastel fortress. "
                "Reviews should keep adding real towns beyond the usual postcard pair. "
                "That habit stops Bosnia and Herzegovina from shrinking to Sarajevo and Mostar alone."
            ),
        },
    ],
    # Keep 8-10 on the same mold; lightly normalize L9 fact 1 to avoid ?-split counting issues
    8: None,
    9: [
        {
            "title": "KM on the price tag",
            "body": (
                "Shop prices in Bosnia and Herzegovina are written in convertible marks, or KM. "
                "You do not need a finance lecture to use the currency in a market line. "
                "Ask Koliko košta, hear a number, and pay. "
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
    10: None,
}


def validate(text: str, label: str):
    assert "—" not in text and "–" not in text, label
    assert ": " not in text, f"colon rant in {label}"
    # Count sentences without treating ? inside quotes oddly; strip trailing punctuation
    parts = []
    buf = ""
    for ch in text:
        buf += ch
        if ch in ".!?":
            s = buf.strip()
            if s:
                parts.append(s)
            buf = ""
    if buf.strip():
        parts.append(buf.strip())
    if not (4 <= len(parts) <= 5):
        raise AssertionError(f"{label} expected 4-5 sentences, got {len(parts)}: {parts}")


def main():
    # Load existing 8 and 10 from files if marked None
    for day in range(1, 11):
        facts = FUN[day]
        if facts is None:
            c = json.loads((ROOT / f"content/book1/day-{day:02d}/chapter.json").read_text(encoding="utf-8"))
            facts = c["funFacts"]
            FUN[day] = facts
        for fact in facts:
            validate(fact["body"], f"L{day}:{fact['title']}")

        for base in (
            ROOT / f"content/book1/day-{day:02d}/chapter.json",
            ROOT / f"frontend/src/data/book1/day-{day:02d}/chapter.json",
        ):
            c = json.loads(base.read_text(encoding="utf-8"))
            c["funFacts"] = facts
            base.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("updated", base)


if __name__ == "__main__":
    main()
