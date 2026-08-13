#!/usr/bin/env python3
"""Draft full chapter.json + video-script.md for Lessons 8–10 and fetch images."""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "frontend" / "public" / "images" / "book1"
UA = "LearnBosnianBot/1.0 (educational content draft)"


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

    author = g("Artist") or g("Credit") or "Wikimedia Commons"
    # keep author short
    author = re.sub(r"\s+", " ", author)[:90]
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


def download_png(commons_title: str, out_name: str) -> dict:
    info = commons_info(commons_title)
    out = IMG_DIR / out_name
    if out.exists() and out.stat().st_size > 1000:
        return info
    import time

    raw = None
    last_err = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(info["sourceUrl"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read()
            break
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    if raw is None:
        raise RuntimeError(f"Failed download {commons_title}: {last_err}")
    tmp = out.with_suffix(".tmp")
    tmp.write_bytes(raw)
    im = Image.open(tmp).convert("RGB")
    # Cap long edge for web
    im.thumbnail((1600, 1600))
    im.save(out, format="PNG", optimize=True)
    tmp.unlink(missing_ok=True)
    return info


def img_entry(id_: str, alt: str, filename: str, commons_title: str) -> dict:
    info = download_png(commons_title, filename)
    credit = (
        f"Based on photo: {commons_title.replace('File:', '')}. "
        f"{info['author']} / Wikimedia Commons ({info['license']})"
    )
    return {
        "id": id_,
        "alt": alt,
        "localPath": f"/images/book1/{filename}",
        "sourceUrl": info["sourceUrl"],
        "pageUrl": info["pageUrl"],
        "author": info["author"],
        "license": info["license"],
        "credit": credit,
    }


def vocab(bs, en, pron, pos, ex):
    return {
        "bosnian": bs,
        "english": en,
        "pronunciation": pron,
        "partOfSpeech": pos,
        "example": ex,
    }


def dict_entry(day, bs, en, pron, pos, ex):
    return {
        "day": day,
        "bosnian": bs,
        "english": en,
        "pronunciation": pron,
        "partOfSpeech": pos,
        "example": ex,
    }


def write_chapter(day: int, data: dict):
    path = ROOT / "content" / "book1" / f"day-{day:02d}" / "chapter.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path)


def write_video(day: int, text: str):
    path = ROOT / "content" / "book1" / f"day-{day:02d}" / "video-script.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def build_lesson_8(images: list) -> dict:
    v = [
        vocab("burek", "meat pastry (Bosnian: meat only)", "BOO-rek", "noun", "Volim burek."),
        vocab("sirnica", "cheese pita", "SEER-nee-tsa", "noun", "Želim sirnicu."),
        vocab("zeljanica", "spinach/greens pita", "zel-YA-nee-tsa", "noun", "Zeljanica je dobra."),
        vocab("hljeb", "bread", "hlyeb", "noun", "Hljeb, molim."),
        vocab("jogurt", "yogurt", "YO-goort", "noun", "Jogurt uz burek."),
        vocab("meso", "meat", "MEH-so", "noun", "Burek je s mesom."),
        vocab("sir", "cheese", "seer", "noun", "Sirnica ima sir."),
        vocab("voće", "fruit", "VO-che", "noun", "Voće je svježe."),
        vocab("povrće", "vegetables", "POV-rche", "noun", "Povrće na pijaci."),
        vocab("volim", "I love / I like", "VO-leem", "verb", "Volim burek."),
        vocab("ne volim", "I do not like", "neh VO-leem", "phrase", "Ne volim luk."),
        vocab("ukusno", "tasty / delicious", "OO-koos-no", "adjective", "Ukusno!"),
        vocab("gladan", "hungry (m.)", "GLAH-dan", "adjective", "Ja sam gladan."),
        vocab("gladna", "hungry (f.)", "GLAHD-na", "adjective", "Ja sam gladna."),
        vocab("pita", "phyllo pie (general)", "PEE-ta", "noun", "Pita je topla."),
        vocab("dobar tek", "enjoy your meal", "DOH-bar tek", "phrase", "Dobar tek!"),
    ]
    return {
        "day": 8,
        "book": 1,
        "week": 2,
        "title": "Volim burek",
        "titleEn": "I love burek",
        "theme": "Street food",
        "status": "draft",
        "reviewedAt": None,
        "reviewerNotes": "Full draft to Lesson 1 exemplar bar. ready for human review before publish.",
        "estimatedMinutes": 60,
        "storyBeat": "Ana’s food disasters begin with burek. Emir teaches likes and a gentle accusative chunk.",
        "learningGoals": {
            "vocabulary": [
                "Food words: burek, sirnica, zeljanica, hljeb, jogurt",
                "Likes: volim / ne volim",
                "Hungry: gladan / gladna; ukusno; dobar tek"
            ],
            "grammar": [
                "Volim + object chunk (accusative singular intro)",
                "Ne volim for polite dislike",
                "Gender on gladan / gladna"
            ],
            "culture": [
                "In BiH, burek means meat. cheese pie is sirnica",
                "Livno highland food postcard beyond the café street"
            ]
        },
        "vocabulary": v,
        "grammar": [
            {
                "title": "Volim + object",
                "explanation": "Volim means I love or I like. Put the food after it as a ready chunk: Volim burek. Volim kahvu. For many feminine food nouns ending in -a, the spoken object often ends in -u: Volim sirnicu. Volim zeljanicu. Learn the pairs as phrases first. Do not memorize a full case table today.",
                "examples": [
                    {"bosnian": "Volim burek.", "english": "I love burek."},
                    {"bosnian": "Volim sirnicu.", "english": "I love cheese pita."},
                    {"bosnian": "Volim kahvu.", "english": "I love coffee."}
                ]
            },
            {
                "title": "Ne volim",
                "explanation": "Add ne before volim to say you do not like something: Ne volim luk. Ne volim čaj. Keep it soft and clear. You can still be polite while you refuse a filling.",
                "examples": [
                    {"bosnian": "Ne volim luk.", "english": "I do not like onion."},
                    {"bosnian": "Ne volim čaj.", "english": "I do not like tea."}
                ]
            },
            {
                "title": "Gladan / gladna",
                "explanation": "Match the adjective to who is speaking. Emir says Ja sam gladan. Ana says Ja sam gladna. Then order food and finish with Dobar tek!",
                "examples": [
                    {"bosnian": "Ja sam gladan.", "english": "I am hungry. (m.)"},
                    {"bosnian": "Ja sam gladna.", "english": "I am hungry. (f.)"},
                    {"bosnian": "Dobar tek!", "english": "Enjoy your meal!"}
                ]
            }
        ],
        "culture": {
            "title": "Burek is meat, and Livno sends cheese",
            "body": "On a Bosnian street, burek means a meat pita. Ask for cheese and you want sirnica. Spinach or greens mean zeljanica. Emir takes Ana to a buregdžinica near Amira’s, then shows a postcard from Livno in western Bosnia: highland pastures famous for Livanjski sir. The café is HQ, but the country’s food map is wider than one warm tray. Today Ana learns to say what she loves before the first bite turns into a flaky disaster.",
            "imageId": "livno-town"
        },
        "lessonBlocks": [
            {
                "id": "a",
                "title": "Lesson A: Food words on the tray",
                "body": "Name the classics: burek (meat), sirnica (cheese), zeljanica (greens), pita as the general phyllo pie word. Add hljeb, jogurt, meso, sir, voće, povrće. Say each twice. Mark the BiH spelling hljeb. Emir points at the tray and refuses the tourist trap sentence burek sa sirom. In Bosnian that fight is real: burek is with meat.",
                "tips": [
                    "burek = meat; sirnica = cheese; zeljanica = greens",
                    "Type hljeb with lj, not a soft English h-leb guess"
                ]
            },
            {
                "id": "b",
                "title": "Lesson B: Volim / ne volim at the counter",
                "body": "Build today’s kit: Volim burek. Volim sirnicu. Ne volim luk. Ja sam gladna / gladan. Ukusno! Dobar tek! Ana tries a too-hot bite, drops flakes on Mrvica, and still finishes the sentence. Food disasters are allowed. Silent pointing is not the goal.",
                "tips": [
                    "Chunk: Volim… / Ne volim… / Dobar tek!",
                    "Use gladna if you are Ana; gladan if you are Emir"
                ]
            }
        ],
        "conversation": {
            "title": "Burek katastrofa",
            "setting": "A busy buregdžinica near Amira’s. Steam, trays, Mrvica lurking for crumbs.",
            "lines": [
                {"speaker": "Emir", "bosnian": "Ana, jesi gladna?", "english": "Ana, are you hungry?"},
                {"speaker": "Ana", "bosnian": "Da! Ja sam gladna. Volim burek!", "english": "Yes! I am hungry. I love burek!"},
                {"speaker": "Emir", "bosnian": "Dobro. Burek je s mesom. Ne sa sirom.", "english": "Good. Burek is with meat. Not with cheese."},
                {"speaker": "Ana", "bosnian": "A sirnica?", "english": "And sirnica?"},
                {"speaker": "Emir", "bosnian": "Sirnica je sa sirom. Zeljanica je sa zeljem.", "english": "Sirnica is with cheese. Zeljanica is with greens."},
                {"speaker": "Ana", "bosnian": "Ja volim sirnicu. Ne volim luk.", "english": "I love sirnica. I do not like onion."},
                {"speaker": "Amira", "bosnian": "Dobar tek! Jogurt?", "english": "Enjoy your meal! Yogurt?"},
                {"speaker": "Narrator", "bosnian": "Ana jede prebrzo. Mrvica jede mrvice.", "english": "Ana eats too fast. Mrvica eats the crumbs."}
            ]
        },
        "puzzles": [
            {
                "id": "p1",
                "type": "match",
                "title": "Match the food",
                "prompt": "Match each Bosnian food word to English.",
                "items": [
                    {"left": "burek", "right": "meat pastry"},
                    {"left": "sirnica", "right": "cheese pita"},
                    {"left": "zeljanica", "right": "greens pita"},
                    {"left": "hljeb", "right": "bread"},
                    {"left": "jogurt", "right": "yogurt"}
                ]
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false: food rules",
                "prompt": "Mark each sentence true or false for BiH usage in this lesson.",
                "items": [
                    {"statement": "In BiH, burek means a meat pita.", "answer": True},
                    {"statement": "Sirnica is a cheese pita.", "answer": True},
                    {"statement": "Volim means I do not like.", "answer": False},
                    {"statement": "Ana says Ja sam gladna.", "answer": True}
                ]
            }
        ],
        "practice": [
            {"id": "pr1", "prompt": "Write I love burek.", "hint": "Volim…", "answer": "Volim burek"},
            {"id": "pr2", "prompt": "Write I love sirnica (object form with -u).", "hint": "Volim sirnicu", "answer": "Volim sirnicu"},
            {"id": "pr3", "prompt": "Write I do not like onion (luk).", "hint": "Ne volim…", "answer": "Ne volim luk"},
            {"id": "pr4", "prompt": "Write I am hungry (feminine, like Ana).", "hint": "Ja sam…", "answer": "Ja sam gladna"},
            {"id": "pr5", "prompt": "Write I am hungry (masculine, like Emir).", "hint": "Ja sam…", "answer": "Ja sam gladan"},
            {"id": "pr6", "prompt": "Write the BiH spelling for bread.", "hint": "hl-", "answer": "hljeb"},
            {"id": "pr7", "prompt": "Write Enjoy your meal!", "hint": "Two words", "answer": "Dobar tek"},
            {"id": "pr8", "prompt": "Write tasty / delicious.", "hint": "u…", "answer": "ukusno"}
        ],
        "funFacts": [
            {
                "title": "No cheese in the word burek",
                "body": "In Bosnia and Herzegovina, asking for burek sa sirom is a classic tourist tell. Locals hear burek as meat. Cheese pie is sirnica."
            },
            {
                "title": "Livanjski sir",
                "body": "Livno’s highland cheese tradition sits west of Sarajevo’s street trays. Emir’s postcard is a reminder that dairy fame is not only a city story."
            },
            {
                "title": "Jogurt is a partner",
                "body": "Warm burek often arrives with jogurt. The pair cools the bite and turns a snack into a small ritual."
            },
            {
                "title": "Mrvica tax",
                "body": "Any flaky pita near Mrvica becomes a shared meal whether you planned it or not."
            }
        ],
        "resources": [
            {
                "label": "How to speak Bosnian (YouTube)",
                "url": "https://www.youtube.com/@HowtospeakBosnian",
                "note": "Companion video for Lesson 8"
            },
            {
                "label": "Next: Lesson 9: U prodavnici",
                "url": "/learn/lesson/9",
                "note": "Shopping phrases with Emir"
            },
            {
                "label": "Book 1 curriculum",
                "url": "/learn",
                "note": "See all lessons"
            }
        ],
        "sectionQuiz": {
            "title": "Lesson 8 section quiz",
            "passPercent": 70,
            "questions": [
                {
                    "id": "q1",
                    "prompt": "What does burek mean in BiH in this lesson?",
                    "options": ["Any pita", "Meat pastry", "Only cheese pie", "Only bread"],
                    "correctIndex": 1,
                    "explanation": "Here burek is the meat pita. Cheese is sirnica.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q2",
                    "prompt": "How do you say I love burek?",
                    "options": ["Ne volim burek.", "Volim burek.", "Ja sam burek.", "Dobar tek burek."],
                    "correctIndex": 1,
                    "explanation": "Volim + food object.",
                    "skill": "grammar"
                },
                {
                    "id": "q3",
                    "prompt": "Which word is the cheese pita?",
                    "options": ["zeljanica", "hljeb", "sirnica", "jogurt"],
                    "correctIndex": 2,
                    "explanation": "Sirnica is cheese. Zeljanica is greens.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q4",
                    "prompt": "Ana is hungry. What does she say?",
                    "options": ["Ja sam gladan.", "Ja sam gladna.", "Ja sam burek.", "Ne volim gladna."],
                    "correctIndex": 1,
                    "explanation": "Feminine speaker uses gladna.",
                    "skill": "grammar"
                },
                {
                    "id": "q5",
                    "prompt": "What does Ne volim luk mean?",
                    "options": ["I love onion.", "I do not like onion.", "Onion is bread.", "Bring yogurt."],
                    "correctIndex": 1,
                    "explanation": "Ne volim = I do not like.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q6",
                    "prompt": "Livno is famous in this lesson’s postcard for…",
                    "options": ["A sea bridge", "Highland cheese country", "Only coffee cups", "Airport gates"],
                    "correctIndex": 1,
                    "explanation": "Livanjski sir and highland pastures widen the food map.",
                    "skill": "culture"
                },
                {
                    "id": "q7",
                    "prompt": "Emir says burek is…",
                    "options": ["sa sirom", "s mesom", "sa voćem", "sa čajem"],
                    "correctIndex": 1,
                    "explanation": "Burek is with meat.",
                    "skill": "dialogue"
                },
                {
                    "id": "q8",
                    "prompt": "What phrase means Enjoy your meal?",
                    "options": ["Dobar dan", "Dobar tek", "Molim", "Hvala"],
                    "correctIndex": 1,
                    "explanation": "Dobar tek is the meal wish.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q9",
                    "prompt": "In Dino Merlin’s Burek, food names show up as…",
                    "options": ["Airport codes only", "Proud everyday Bosnian kitchen words", "Silent captions only", "English menus only"],
                    "correctIndex": 1,
                    "explanation": "Listen for food vocabulary riding a pop hook.",
                    "skill": "listening"
                }
            ]
        },
        "dictionaryEntries": [dict_entry(8, x["bosnian"], x["english"], x["pronunciation"], x["partOfSpeech"], x["example"]) for x in v],
        "images": images,
        "imagesNeeded": False,
        "imageBriefs": [],
        "civicContext": {
            "title": "Local food culture, imported staples",
            "body": "Bosnia and Herzegovina still depends heavily on imported food even though street food and home cooking are central to daily life. After the war, fragmented farmland and weak agricultural investment slowed the recovery of domestic production, so bakeries and shops often stock flour, oil, dairy, and other staples from abroad. Local pita culture is strong, but the grocery supply behind it is still shaped by that import dependence.",
            "imageId": "civic-livno-valley",
            "learnMore": {
                "label": "Wikipedia: Agriculture in Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Agriculture_in_Bosnia_and_Herzegovina"
            }
        },
        "authenticListen": {
            "title": "Čuj Bosnu: Dino Merlin sings Burek",
            "kind": "song",
            "hook": "A famous pop anthem stacks Bosnian food words. Listen for burek, pita, and the kitchen pride in the chorus.",
            "source": {
                "title": "Dino Merlin - Burek (Official Video) [2004]",
                "artistOrSpeaker": "Dino Merlin",
                "regionOrScene": "Bosnian kitchen / pop",
                "license": "YouTube Terms of Service (embed)",
                "credit": "Dino Merlin official video on YouTube",
                "pageUrl": "https://www.youtube.com/watch?v=e7JXd8Qavpk",
                "embedUrl": "https://www.youtube.com/watch?v=e7JXd8Qavpk"
            },
            "durationHint": "45–90 seconds",
            "listenTask": {
                "prompt": "Listen for food words like burek or pita in the chorus energy.",
                "gistQuestion": {
                    "prompt": "What fits the clip’s mood?",
                    "options": [
                        "Silent library rules",
                        "Proud, playful listing of Bosnian food culture",
                        "Only weather report",
                        "Airport security lecture"
                    ],
                    "correctIndex": 1
                },
                "targetWords": ["burek", "pita", "kahva"],
                "noticePrompt": "Food vocabulary can ride music. You do not need every lyric to catch the kitchen words."
            },
            "reveal": {
                "keyLines": [
                    {"bosnian": "Burek, pita zeljanica…", "english": "Burek, spinach pita…"},
                    {"bosnian": "Fildžan, džezva… kahva", "english": "Cup, pot… coffee"}
                ],
                "teacherNote": "If the full verse flies by, you still practiced listening for food anchors."
            }
        },
        "speakTargets": [1, 5, 6]
    }


def null_none():
    return None


def build_lesson_9(images: list) -> dict:
    v = [
        vocab("prodavnica", "shop / store", "pro-DAV-nee-tsa", "noun", "Idemo u prodavnicu."),
        vocab("pijaca", "market", "pee-YA-tsa", "noun", "Na pijaci ima voća."),
        vocab("željeti", "to want", "ZHE-lye-tee", "verb", "Želim jabuku."),
        vocab("želim", "I want", "ZHE-leem", "verb form", "Želim hljeb."),
        vocab("molim", "please / you’re welcome", "MO-leem", "particle", "Hljeb, molim."),
        vocab("hvala", "thank you", "HVAH-la", "interjection", "Hvala!"),
        vocab("koliko košta", "how much does it cost", "KOH-lee-koh KOSH-ta", "phrase", "Koliko košta?"),
        vocab("kilogram", "kilogram", "KEE-lo-gram", "noun", "Jedan kilogram."),
        vocab("jabuka", "apple", "YA-boo-ka", "noun", "Želim jabuku."),
        vocab("banana", "banana", "ba-NA-na", "noun", "Dvije banane."),
        vocab("voda", "water", "VO-da", "noun", "Vodu, molim."),
        vocab("mlijeko", "milk", "MLYE-ko", "noun", "Mlijeko, molim."),
        vocab("novac", "money", "NO-vats", "noun", "Imam novac."),
        vocab("jeftino", "cheap", "YEF-tee-no", "adverb/adj", "To je jeftino."),
        vocab("skupo", "expensive", "SKOO-po", "adverb/adj", "To je skupo."),
        vocab("kesa", "bag", "KEH-sa", "noun", "Kesa, molim."),
    ]
    return {
        "day": 9,
        "book": 1,
        "week": 2,
        "title": "U prodavnici",
        "titleEn": "At the shop",
        "theme": "Market day",
        "status": "draft",
        "reviewedAt": None,
        "reviewerNotes": "Full draft to Lesson 1 exemplar bar. ready for human review before publish.",
        "estimatedMinutes": 60,
        "storyBeat": "Ana shops with Emir and practices želim, molim, hvala, and prices.",
        "learningGoals": {
            "vocabulary": [
                "Shop and market: prodavnica, pijaca, kesa, novac",
                "Foods to buy: jabuka, banana, voda, mlijeko",
                "Price talk: koliko košta, jeftino, skupo"
            ],
            "grammar": [
                "Želim + object chunks",
                "Polite kit: molim / hvala",
                "Koliko košta? for price questions"
            ],
            "culture": [
                "Market energy in Tuzla, a northern city beyond Sarajevo’s old bazaar",
                "Small polite routines keep the queue moving"
            ]
        },
        "vocabulary": v,
        "grammar": [
            {
                "title": "Želim + object",
                "explanation": "Želim means I want. Use it at the counter: Želim jabuku. Želim hljeb. Želim vodu. Feminine -a nouns often take -u in this chunk. Keep the list short and sayable.",
                "examples": [
                    {"bosnian": "Želim jabuku.", "english": "I want an apple."},
                    {"bosnian": "Želim vodu.", "english": "I want water."},
                    {"bosnian": "Želim hljeb.", "english": "I want bread."}
                ]
            },
            {
                "title": "Molim and hvala",
                "explanation": "Molim softens a request (Hljeb, molim.) and can also answer thank you as you’re welcome. Hvala is thank you. Stack them: Hvala! Molim!",
                "examples": [
                    {"bosnian": "Hljeb, molim.", "english": "Bread, please."},
                    {"bosnian": "Hvala!", "english": "Thank you!"},
                    {"bosnian": "Molim!", "english": "You’re welcome!"}
                ]
            },
            {
                "title": "Koliko košta?",
                "explanation": "Ask the price with Koliko košta? Answer with a number and KM if you know it, or just react: To je jeftino. To je skupo.",
                "examples": [
                    {"bosnian": "Koliko košta?", "english": "How much does it cost?"},
                    {"bosnian": "To je jeftino.", "english": "That is cheap."},
                    {"bosnian": "To je skupo.", "english": "That is expensive."}
                ]
            }
        ],
        "culture": {
            "title": "Market day energy in Tuzla",
            "body": "Sarajevo’s Baščaršija is only one shopping map. Emir shows Ana photos from Tuzla in the northeast: an old-town street, a public fountain, and the everyday habit of buying fruit by the kilogram. A prodavnica can be a tiny corner shop. A pijaca is the open market where voices, scales, and kesa bags do the work. Today’s language is short on purpose. You want something, you ask the price, you say hvala.",
            "imageId": "tuzla-fountain"
        },
        "lessonBlocks": [
            {
                "id": "a",
                "title": "Lesson A: Shop words that move",
                "body": "Learn the places: prodavnica (shop) and pijaca (market). Add bag and money: kesa, novac. Then stock the basket: jabuka, banana, voda, mlijeko, plus hljeb from yesterday. Practice pointing and naming before you speak full sentences. Emir makes Ana say mlijeko with lj, not a soft English milk guess.",
                "tips": [
                    "prodavnica = shop; pijaca = market",
                    "Type mlijeko with lj"
                ]
            },
            {
                "id": "b",
                "title": "Lesson B: Želim, molim, hvala",
                "body": "Run the counter script: Želim jabuku, molim. Koliko košta? Hvala! Grab a kesa. Decide jeftino or skupo. Ana almost pays with the wrong coins, Emir laughs, and Mrvica somehow appears near the fruit crate as if she has a loyalty card.",
                "tips": [
                    "Kit: Želim… molim. / Koliko košta? / Hvala!",
                    "React with jeftino or skupo after the price"
                ]
            }
        ],
        "conversation": {
            "title": "Na pijaci",
            "setting": "A small market street. Scales, fruit crates, a shopkeeper with little patience and a good heart.",
            "lines": [
                {"speaker": "Emir", "bosnian": "Idemo u prodavnicu. Pa na pijacu.", "english": "Let’s go to the shop. Then to the market."},
                {"speaker": "Ana", "bosnian": "Želim jabuku, molim.", "english": "I want an apple, please."},
                {"speaker": "Shopkeeper", "bosnian": "Dobro. Koliko?", "english": "Good. How many?"},
                {"speaker": "Ana", "bosnian": "Dvije jabuke. Koliko košta?", "english": "Two apples. How much does it cost?"},
                {"speaker": "Shopkeeper", "bosnian": "Tri KM. Jeftino!", "english": "Three KM. Cheap!"},
                {"speaker": "Ana", "bosnian": "Hvala! Kesa, molim.", "english": "Thank you! A bag, please."},
                {"speaker": "Emir", "bosnian": "I mlijeko? Ja želim mlijeko.", "english": "And milk? I want milk."},
                {"speaker": "Narrator", "bosnian": "Mrvica gleda banane. Emir: Ne.", "english": "Mrvica stares at the bananas. Emir: No."}
            ]
        },
        "puzzles": [
            {
                "id": "p1",
                "type": "match",
                "title": "Match shop words",
                "prompt": "Match Bosnian to English.",
                "items": [
                    {"left": "prodavnica", "right": "shop"},
                    {"left": "pijaca", "right": "market"},
                    {"left": "kesa", "right": "bag"},
                    {"left": "hvala", "right": "thank you"},
                    {"left": "skupo", "right": "expensive"}
                ]
            },
            {
                "id": "p2",
                "type": "scramble",
                "title": "Unscramble the request",
                "prompt": "Unscramble to make today’s phrases.",
                "items": [
                    {"scrambled": "jabuku Želim molim", "answer": "želim jabuku molim"},
                    {"scrambled": "košta Koliko", "answer": "koliko košta"},
                    {"scrambled": "mlijeko Želim", "answer": "želim mlijeko"}
                ]
            }
        ],
        "practice": [
            {"id": "pr1", "prompt": "Write I want an apple (object form).", "hint": "Želim jabuku", "answer": "Želim jabuku"},
            {"id": "pr2", "prompt": "Write Bread, please.", "hint": "…, molim", "answer": "Hljeb, molim"},
            {"id": "pr3", "prompt": "Write How much does it cost?", "hint": "Koliko…", "answer": "Koliko košta"},
            {"id": "pr4", "prompt": "Write thank you.", "hint": "h…", "answer": "hvala"},
            {"id": "pr5", "prompt": "Write the BiH spelling for milk.", "hint": "mlj-", "answer": "mlijeko"},
            {"id": "pr6", "prompt": "Write That is expensive.", "hint": "To je…", "answer": "To je skupo"},
            {"id": "pr7", "prompt": "Write That is cheap.", "hint": "To je…", "answer": "To je jeftino"},
            {"id": "pr8", "prompt": "Write A bag, please.", "hint": "Kesa…", "answer": "Kesa, molim"}
        ],
        "funFacts": [
            {
                "title": "KM on the price tag",
                "body": "Prices are in convertible marks (KM). You do not need a finance lecture to ask Koliko košta? and understand the number."
            },
            {
                "title": "Tuzla’s other fame",
                "body": "Tuzla is known for salt and for a large urban center in the northeast. A market day there feels different from Baščaršija tourist lanes."
            },
            {
                "title": "Molim does double duty",
                "body": "Molim can mean please in a request and you’re welcome after hvala. Context tells you which one you heard."
            },
            {
                "title": "Kesa is not optional",
                "body": "Asking for a bag is normal. It is also a clean way to practice molim one more time before you leave."
            }
        ],
        "resources": [
            {
                "label": "How to speak Bosnian (YouTube)",
                "url": "https://www.youtube.com/@HowtospeakBosnian",
                "note": "Companion video for Lesson 9"
            },
            {
                "label": "Next: Lesson 10: Moja soba",
                "url": "/learn/lesson/10",
                "note": "Home words above Amira’s café"
            },
            {
                "label": "Book 1 curriculum",
                "url": "/learn",
                "note": "See all lessons"
            }
        ],
        "sectionQuiz": {
            "title": "Lesson 9 section quiz",
            "passPercent": 70,
            "questions": [
                {
                    "id": "q1",
                    "prompt": "What is a prodavnica?",
                    "options": ["A waterfall", "A shop", "A bridge", "A clock tower"],
                    "correctIndex": 1,
                    "explanation": "Prodavnica means shop/store.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q2",
                    "prompt": "How do you say I want milk?",
                    "options": ["Volim mlijeko samo", "Želim mlijeko.", "Ne volim vodu.", "To je skupo mlijeko samo"],
                    "correctIndex": 1,
                    "explanation": "Želim + object.",
                    "skill": "grammar"
                },
                {
                    "id": "q3",
                    "prompt": "Koliko košta? asks about…",
                    "options": ["The time", "The price", "The weather", "Your name"],
                    "correctIndex": 1,
                    "explanation": "It means how much does it cost?",
                    "skill": "vocabulary"
                },
                {
                    "id": "q4",
                    "prompt": "Which word means thank you?",
                    "options": ["molim", "hvala", "kesa", "skupo"],
                    "correctIndex": 1,
                    "explanation": "Hvala = thank you.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q5",
                    "prompt": "Tuzla appears in this lesson as…",
                    "options": ["A southern sea port only", "A northeast city with market energy", "Only a desert", "A fictional café name"],
                    "correctIndex": 1,
                    "explanation": "The culture hook widens the map to Tuzla.",
                    "skill": "culture"
                },
                {
                    "id": "q6",
                    "prompt": "Ana asks for a bag. What does she say?",
                    "options": ["Kesa, molim.", "Skupo, molim.", "Gladan, molim.", "Burek, hvala samo."],
                    "correctIndex": 0,
                    "explanation": "Kesa, molim.",
                    "skill": "dialogue"
                },
                {
                    "id": "q7",
                    "prompt": "To je skupo means…",
                    "options": ["That is cheap.", "That is expensive.", "That is water.", "That is an apple."],
                    "correctIndex": 1,
                    "explanation": "Skupo = expensive.",
                    "skill": "grammar"
                },
                {
                    "id": "q8",
                    "prompt": "Which spelling is the BiH form for milk?",
                    "options": ["mleko only", "mlijeko", "mliko", "milk-o"],
                    "correctIndex": 1,
                    "explanation": "This course uses mlijeko.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q9",
                    "prompt": "In the shopping listen clip, you mainly train…",
                    "options": ["Silent reading only", "Hearing price and want phrases in real teaching speech", "Swimming verbs", "Past tense only"],
                    "correctIndex": 1,
                    "explanation": "Čuj Bosnu here targets shop phrases.",
                    "skill": "listening"
                }
            ]
        },
        "dictionaryEntries": [dict_entry(9, x["bosnian"], x["english"], x["pronunciation"], x["partOfSpeech"], x["example"]) for x in v],
        "images": images,
        "imagesNeeded": False,
        "imageBriefs": [],
        "civicContext": {
            "title": "Tuzla’s factories closed faster than new jobs arrived",
            "body": "Tuzla was one of Bosnia and Herzegovina’s major industrial and energy centers, with mining, chemicals, and related plants employing large parts of the region. After the war, many of those workplaces shrank or closed through damage, privatization, and market collapse, leaving long stretches of unemployment and insecure work. Markets and small shops kept daily life moving, but they did not replace the steady industrial wages that once supported whole neighborhoods.",
            "imageId": "civic-tuzla-museum",
            "learnMore": {
                "label": "Wikipedia: Tuzla",
                "url": "https://en.wikipedia.org/wiki/Tuzla"
            }
        },
        "authenticListen": {
            "title": "Čuj Bosnu: shopping phrases in lesson speech",
            "kind": "speaker",
            "hook": "Hear how much is… and other everyday shopping phrases outside our studio cast.",
            "source": {
                "title": "bs learn A1 Book 1 Ch.20: How much is ...? | everyday shopping phrases",
                "artistOrSpeaker": "SynapseLingo",
                "regionOrScene": "Shop / prices",
                "license": "YouTube Terms of Service (embed)",
                "credit": "SynapseLingo Bosnian shopping phrases on YouTube",
                "pageUrl": "https://www.youtube.com/watch?v=zExUj5IIobY",
                "embedUrl": "https://www.youtube.com/watch?v=zExUj5IIobY"
            },
            "durationHint": "45–90 seconds",
            "listenTask": {
                "prompt": "Listen for price or wanting phrases you can reuse at a counter.",
                "gistQuestion": {
                    "prompt": "What is the clip mainly teaching?",
                    "options": [
                        "Mountain climbing only",
                        "Everyday shopping / price language",
                        "Presidential elections",
                        "Silent meditation"
                    ],
                    "correctIndex": 1
                },
                "targetWords": ["koliko", "košta", "želim"],
                "noticePrompt": "Even if the teacher’s pace differs from Emir’s, hunt for the same kit: want, please, price."
            },
            "reveal": {
                "keyLines": [
                    {"bosnian": "Koliko košta?", "english": "How much does it cost?"},
                    {"bosnian": "Želim…", "english": "I want…"}
                ],
                "teacherNote": "Reuse those anchors at a real pijaca."
            }
        },
        "speakTargets": [1, 3, 5]
    }


def build_lesson_10(images: list) -> dict:
    v = [
        vocab("soba", "room", "SO-ba", "noun", "Moja soba je mala."),
        vocab("kuća", "house", "KOO-cha", "noun", "To je lijepa kuća."),
        vocab("stan", "apartment", "stahn", "noun", "Stan je iznad kafića."),
        vocab("vrata", "door", "VRAH-ta", "noun", "Vrata su otvorena."),
        vocab("prozor", "window", "PRO-zor", "noun", "Prozor je velik."),
        vocab("krevet", "bed", "KREH-vet", "noun", "Krevet je udoban."),
        vocab("sto", "table", "stoh", "noun", "Sto je mali."),
        vocab("stolica", "chair", "STO-lee-tsa", "noun", "Stolica je crvena."),
        vocab("lampa", "lamp", "LAHM-pa", "noun", "Lampa je nova."),
        vocab("imati", "to have", "EE-ma-tee", "verb", "Imam sobu."),
        vocab("imam", "I have", "EE-mam", "verb form", "Imam krevet."),
        vocab("imaš", "you have", "EE-mash", "verb form", "Imaš sto?"),
        vocab("velik", "big (m.)", "VEH-lik", "adjective", "Prozor je velik."),
        vocab("mala", "small (f.)", "MAH-la", "adjective", "Soba je mala."),
        vocab("lijepa", "beautiful (f.)", "LYE-pa", "adjective", "Kuća je lijepa."),
        vocab("udoban", "comfortable (m.)", "OO-do-ban", "adjective", "Krevet je udoban."),
    ]
    return {
        "day": 10,
        "book": 1,
        "week": 2,
        "title": "Moja soba",
        "titleEn": "My room",
        "theme": "Room above the café",
        "status": "draft",
        "reviewedAt": None,
        "reviewerNotes": "Full draft to Lesson 1 exemplar bar. ready for human review before publish.",
        "estimatedMinutes": 60,
        "storyBeat": "Ana settles into the room above Amira’s and learns imati plus simple adjective agreement.",
        "learningGoals": {
            "vocabulary": [
                "Home words: soba, kuća, stan, vrata, prozor",
                "Furniture: krevet, sto, stolica, lampa",
                "Size/comfort: velik, mala, lijepa, udoban"
            ],
            "grammar": [
                "Imam / imaš (have)",
                "Adjective agreement intro with room words",
                "Moja soba as a possessive chunk"
            ],
            "culture": [
                "Living above a café as a classic small-city arrangement",
                "Stolac and Radimlja as a stone-house postcard from Herzegovina"
            ]
        },
        "vocabulary": v,
        "grammar": [
            {
                "title": "Imam / imaš",
                "explanation": "Imati means to have. Today’s forms: Imam (I have) and imaš (you have). Imam sobu. Imam krevet. Imaš lampu? Keep objects as chunks.",
                "examples": [
                    {"bosnian": "Imam sobu.", "english": "I have a room."},
                    {"bosnian": "Imam krevet.", "english": "I have a bed."},
                    {"bosnian": "Imaš sto?", "english": "Do you have a table?"}
                ]
            },
            {
                "title": "Moja soba",
                "explanation": "Soba is feminine, so moja soba is the natural chunk. Pair it with short descriptions: Moja soba je mala. Moja soba je lijepa.",
                "examples": [
                    {"bosnian": "Moja soba je mala.", "english": "My room is small."},
                    {"bosnian": "Moja soba je lijepa.", "english": "My room is beautiful."}
                ]
            },
            {
                "title": "Adjective agreement intro",
                "explanation": "Match the adjective shape to the noun you see. Feminine soba/kuća often take -a forms: mala, lijepa. Masculine prozor/krevet take forms like velik, udoban. Learn today’s pairs by ear.",
                "examples": [
                    {"bosnian": "Prozor je velik.", "english": "The window is big."},
                    {"bosnian": "Krevet je udoban.", "english": "The bed is comfortable."},
                    {"bosnian": "Kuća je lijepa.", "english": "The house is beautiful."}
                ]
            }
        ],
        "culture": {
            "title": "A room upstairs, and stone houses farther south",
            "body": "Ana’s new address is simple: a small soba above Amira’s café, with a window over the street and a door that never quite keeps Mrvica out. Emir widens the home idea with a postcard from Stolac in Herzegovina, where stone houses and the Radimlja stećci necropolis sit in open light. Home language can start in one rented room and still point to older ways of living on the land.",
            "imageId": "stolac-radimlja"
        },
        "lessonBlocks": [
            {
                "id": "a",
                "title": "Lesson A: Name the room",
                "body": "Walk the space: soba, vrata, prozor, krevet, sto, stolica, lampa. Add kuća and stan for the wider home map. Ana touches each object and says the word twice. Emir refuses English escape hatches. If you live above a café, you still need Bosnian for the furniture.",
                "tips": [
                    "soba = room; stan = apartment; kuća = house",
                    "Point and name before you make long sentences"
                ]
            },
            {
                "id": "b",
                "title": "Lesson B: Imam and short descriptions",
                "body": "Build: Imam sobu. Imam krevet. Moja soba je mala. Prozor je velik. Krevet je udoban. Ana hangs a tiny Livno cheese postcard next to a Stolac photo, then discovers Mrvica already claimed the pillow. Ownership is a spectrum.",
                "tips": [
                    "Kit: Imam… / Moja soba je… / … je velik/mala/udoban",
                    "Match mala/lijepa to feminine soba/kuća"
                ]
            }
        ],
        "conversation": {
            "title": "Iznad kafića",
            "setting": "Ana’s room above Amira’s. Soft street noise, one suitcase, one judgmental cat.",
            "lines": [
                {"speaker": "Amira", "bosnian": "Ovo je tvoja soba.", "english": "This is your room."},
                {"speaker": "Ana", "bosnian": "Hvala! Moja soba je mala, ali lijepa.", "english": "Thank you! My room is small, but beautiful."},
                {"speaker": "Emir", "bosnian": "Imaš krevet? Sto? Stolicu?", "english": "Do you have a bed? A table? A chair?"},
                {"speaker": "Ana", "bosnian": "Imam krevet. Imam sto. Imam stolicu.", "english": "I have a bed. I have a table. I have a chair."},
                {"speaker": "Amira", "bosnian": "Prozor je velik. Dobro za zrak.", "english": "The window is big. Good for air."},
                {"speaker": "Ana", "bosnian": "Krevet je udoban. Volim moju sobu!", "english": "The bed is comfortable. I love my room!"},
                {"speaker": "Narrator", "bosnian": "Mrvica sjedi na jastuku. To je sada njen sto.", "english": "Mrvica sits on the pillow. That is her table now."},
                {"speaker": "Emir", "bosnian": "Ona ima sobu. Ti imaš sobu. Super!", "english": "She has a room. You have a room. Great!"}
            ]
        },
        "puzzles": [
            {
                "id": "p1",
                "type": "match",
                "title": "Match home words",
                "prompt": "Match Bosnian to English.",
                "items": [
                    {"left": "soba", "right": "room"},
                    {"left": "prozor", "right": "window"},
                    {"left": "krevet", "right": "bed"},
                    {"left": "stolica", "right": "chair"},
                    {"left": "lampa", "right": "lamp"}
                ]
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false: room talk",
                "prompt": "Mark each sentence true or false for this lesson.",
                "items": [
                    {"statement": "Imam means I have.", "answer": True},
                    {"statement": "Moja soba is a natural feminine chunk.", "answer": True},
                    {"statement": "Kuća means window.", "answer": False},
                    {"statement": "Stolac appears as a Herzegovina postcard place.", "answer": True}
                ]
            }
        ],
        "practice": [
            {"id": "pr1", "prompt": "Write I have a room (object chunk).", "hint": "Imam sobu", "answer": "Imam sobu"},
            {"id": "pr2", "prompt": "Write My room is small.", "hint": "Moja soba je…", "answer": "Moja soba je mala"},
            {"id": "pr3", "prompt": "Write The window is big.", "hint": "Prozor je…", "answer": "Prozor je velik"},
            {"id": "pr4", "prompt": "Write The bed is comfortable.", "hint": "Krevet je…", "answer": "Krevet je udoban"},
            {"id": "pr5", "prompt": "Write Do you have a table?", "hint": "Imaš…", "answer": "Imaš sto"},
            {"id": "pr6", "prompt": "Write the word for chair.", "hint": "sto-", "answer": "stolica"},
            {"id": "pr7", "prompt": "Write The house is beautiful.", "hint": "Kuća je…", "answer": "Kuća je lijepa"},
            {"id": "pr8", "prompt": "Write I have a lamp (object with -u).", "hint": "Imam lampu", "answer": "Imam lampu"}
        ],
        "funFacts": [
            {
                "title": "Upstairs from the kahva",
                "body": "Living above a café is a practical city pattern: short commute, strong coffee smell, and neighbors who already know your order."
            },
            {
                "title": "Stećci near Stolac",
                "body": "Radimlja’s medieval tombstones near Stolac are a Herzegovina landmark. Emir uses them as a postcard, not a history exam."
            },
            {
                "title": "Stan vs kuća",
                "body": "Stan is an apartment. Kuća is a house. Ana has a soba inside Amira’s world either way."
            },
            {
                "title": "Cat property law",
                "body": "If Mrvica sits on it, local custom says the pillow has a new owner."
            }
        ],
        "resources": [
            {
                "label": "How to speak Bosnian (YouTube)",
                "url": "https://www.youtube.com/@HowtospeakBosnian",
                "note": "Companion video for Lesson 10"
            },
            {
                "label": "How to speak Bosnian: living room furniture",
                "url": "https://www.youtube.com/watch?v=lTp-jz2azsI",
                "note": "Extra furniture listening"
            },
            {
                "label": "Next: Lesson 11: Kakvo je vrijeme?",
                "url": "/learn/lesson/11",
                "note": "Weather on Trebević"
            },
            {
                "label": "Book 1 curriculum",
                "url": "/learn",
                "note": "See all lessons"
            }
        ],
        "sectionQuiz": {
            "title": "Lesson 10 section quiz",
            "passPercent": 70,
            "questions": [
                {
                    "id": "q1",
                    "prompt": "What does soba mean?",
                    "options": ["Soup", "Room", "Bridge", "Market"],
                    "correctIndex": 1,
                    "explanation": "Soba = room.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q2",
                    "prompt": "Imam krevet means…",
                    "options": ["I want a bed.", "I have a bed.", "The bed is big.", "Open the door."],
                    "correctIndex": 1,
                    "explanation": "Imam = I have.",
                    "skill": "grammar"
                },
                {
                    "id": "q3",
                    "prompt": "Which chunk fits a feminine room?",
                    "options": ["Moj soba", "Moja soba", "Moj prozor soba", "Imaš soba moj"],
                    "correctIndex": 1,
                    "explanation": "Moja soba.",
                    "skill": "grammar"
                },
                {
                    "id": "q4",
                    "prompt": "Prozor means…",
                    "options": ["Door", "Window", "Lamp", "Chair"],
                    "correctIndex": 1,
                    "explanation": "Prozor = window.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q5",
                    "prompt": "Stolac / Radimlja appears as…",
                    "options": ["A Sarajevo tram line", "A Herzegovina stone-house postcard place", "A coffee brand only", "A sea port"],
                    "correctIndex": 1,
                    "explanation": "The culture hook points south to Stolac.",
                    "skill": "culture"
                },
                {
                    "id": "q6",
                    "prompt": "Ana says her room is…",
                    "options": ["mala, ali lijepa", "samo skupo", "samo burek", "samo pijaca"],
                    "correctIndex": 0,
                    "explanation": "Small but beautiful.",
                    "skill": "dialogue"
                },
                {
                    "id": "q7",
                    "prompt": "Which word means chair?",
                    "options": ["sto", "stolica", "stan", "soba"],
                    "correctIndex": 1,
                    "explanation": "Stolica = chair. Sto = table.",
                    "skill": "vocabulary"
                },
                {
                    "id": "q8",
                    "prompt": "Krevet je udoban means…",
                    "options": ["The bed is comfortable.", "The door is new.", "The lamp is expensive.", "The house is far."],
                    "correctIndex": 0,
                    "explanation": "Udoban = comfortable.",
                    "skill": "grammar"
                },
                {
                    "id": "q9",
                    "prompt": "The furniture listen resource helps you…",
                    "options": ["Ignore home words", "Hear living-room vocabulary in another teacher voice", "Learn only past tense", "Skip adjectives"],
                    "correctIndex": 1,
                    "explanation": "Extra listening on furniture names.",
                    "skill": "listening"
                }
            ]
        },
        "dictionaryEntries": [dict_entry(10, x["bosnian"], x["english"], x["pronunciation"], x["partOfSpeech"], x["example"]) for x in v],
        "images": images,
        "imagesNeeded": False,
        "imageBriefs": [],
        "civicContext": {
            "title": "Return and property claims are still unfinished",
            "body": "The war displaced hundreds of thousands of people from their homes across Bosnia and Herzegovina. Annex 7 of the Dayton Peace Agreement promised the right to return and reclaim property, but many restitution cases, damaged apartments, and contested ownership claims remained unresolved for years. Even today, some families are still waiting for permanent housing solutions that the peace settlement said should come much sooner.",
            "imageId": "civic-apartment",
            "learnMore": {
                "label": "Wikipedia: Residential property in Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Annex_7_of_the_Dayton_Agreement"
            }
        },
        "authenticListen": {
            "title": "Čuj Bosnu: living-room furniture words",
            "kind": "speaker",
            "hook": "Hear furniture and room vocabulary from the How to speak Bosnian channel.",
            "source": {
                "title": "HOW TO SPEAK BOSNIAN   Living Room Furniture",
                "artistOrSpeaker": "How to speak Bosnian",
                "regionOrScene": "Home / living room",
                "license": "YouTube Terms of Service (embed)",
                "credit": "How to speak Bosnian on YouTube",
                "pageUrl": "https://www.youtube.com/watch?v=lTp-jz2azsI",
                "embedUrl": "https://www.youtube.com/watch?v=lTp-jz2azsI"
            },
            "durationHint": "45–90 seconds",
            "listenTask": {
                "prompt": "Listen for furniture names you can point to in Ana’s room.",
                "gistQuestion": {
                    "prompt": "What is the clip mainly about?",
                    "options": [
                        "Airport departures",
                        "Living-room / furniture vocabulary",
                        "Only political debates",
                        "Swimming lessons"
                    ],
                    "correctIndex": 1
                },
                "targetWords": ["soba", "sto", "stolica"],
                "noticePrompt": "Pause and repeat any noun you can already see in the room above Amira’s."
            },
            "reveal": {
                "keyLines": [
                    {"bosnian": "sto / stolica", "english": "table / chair"},
                    {"bosnian": "Moja soba…", "english": "My room…"}
                ],
                "teacherNote": "Map each heard noun onto Ana’s small upstairs space."
            }
        },
        "speakTargets": [1, 3, 5]
    }


VIDEO_8 = """
# Lesson 8 video script: Volim burek
**Length target:** 8. 10 minutes
**Style:** Scenic Bosnian stills + yellow/gold on-screen text (channel style)
**Status:** Export when chapter is `published`

## Thumbnail text
- EN: Lesson 8: I love burek
- BS: Volim burek
- Background: warm pita tray

## Narration + on-screen cues

### 0:00 Cold open
**Narration:** Lesson 8: Volim burek. I love burek. Ana is hungry. Emir has rules. And Mrvica has crumbs.
**On screen:** Volim burek | Lesson 8

### 0:40 Goals
**Narration:** Today you learn food words, volim and ne volim, and how to say you are hungry.
**On screen:** Goals · burek/sirnica · volim · gladan/gladna

### 1:30 Culture hook
**Narration:** In Bosnia and Herzegovina, burek means meat. Cheese pie is sirnica. Emir also flashes a Livno postcard. highland cheese country west of the café street.
**On screen:** burek = meat · Livno · (credit image)

### 3:00 Lesson A: Food on the tray
**Narration:** Burek, sirnica, zeljanica, hljeb, jogurt. Say them twice. Remember hljeb.
**On screen (cards):** burek | sirnica | zeljanica | hljeb | jogurt

### 5:00 Lesson B: Volim / ne volim
**Narration:** Volim burek. Volim sirnicu. Ne volim luk. Ja sam gladna. Dobar tek!
**On screen:** Volim… · Ne volim… · Dobar tek!

### 6:30 Mini dialogue
**Narration:** Ana orders too confidently and eats too fast. Pause and repeat the chapter lines.
**On screen:** Dialogue lines from chapter (BS + EN)

### 8:00 Practice prompt
**Narration:** Pause and match food words. Next: Lesson 9: U prodavnici. Shopping with Emir.
**On screen:** Practice · Next: U prodavnici | Subscribe · learnbosnian site

## End screen
- Link to website `/learn/lesson/8`
- Playlist: Learn Bosnian: Book 1
- Image credits in description
"""

VIDEO_9 = """
# Lesson 9 video script: U prodavnici
**Length target:** 8. 10 minutes
**Style:** Scenic Bosnian stills + yellow/gold on-screen text (channel style)
**Status:** Export when chapter is `published`

## Thumbnail text
- EN: Lesson 9: At the shop
- BS: U prodavnici
- Background: market fruit crates

## Narration + on-screen cues

### 0:00 Cold open
**Narration:** Lesson 9: U prodavnici. At the shop. Ana needs fruit, milk, and a bag. Emir needs patience.
**On screen:** U prodavnici | Lesson 9

### 0:40 Goals
**Narration:** Today: želim, molim, hvala, and Koliko košta?
**On screen:** Goals · želim · molim/hvala · prices

### 1:30 Culture hook
**Narration:** Not only Baščaršija. Emir shows Tuzla market energy in the northeast. Prodavnica is the shop. Pijaca is the open market.
**On screen:** Tuzla · pijaca · (credit image)

### 3:00 Lesson A: Shop words
**Narration:** Prodavnica, pijaca, kesa, novac, jabuka, banana, voda, mlijeko.
**On screen (cards):** prodavnica | pijaca | kesa | jabuka | mlijeko

### 5:00 Lesson B: Counter kit
**Narration:** Želim jabuku, molim. Koliko košta? Hvala! To je jeftino. To je skupo.
**On screen:** Želim… molim · Koliko košta? · Hvala!

### 6:30 Mini dialogue
**Narration:** Ana buys apples and almost loses the bananas to Mrvica. Pause and repeat.
**On screen:** Dialogue lines from chapter (BS + EN)

### 8:00 Practice prompt
**Narration:** Unscramble the requests. Next: Lesson 10: Moja soba.
**On screen:** Practice · Next: Moja soba | Subscribe · learnbosnian site

## End screen
- Link to website `/learn/lesson/9`
- Playlist: Learn Bosnian: Book 1
- Image credits in description
"""

VIDEO_10 = """
# Lesson 10 video script: Moja soba
**Length target:** 8. 10 minutes
**Style:** Scenic Bosnian stills + yellow/gold on-screen text (channel style)
**Status:** Export when chapter is `published`

## Thumbnail text
- EN: Lesson 10: My room
- BS: Moja soba
- Background: window light in a small room

## Narration + on-screen cues

### 0:00 Cold open
**Narration:** Lesson 10: Moja soba. My room. Ana moves in above Amira’s café. Mrvica moves in two minutes later.
**On screen:** Moja soba | Lesson 10

### 0:40 Goals
**Narration:** Home words, imam and imaš, and short descriptions like mala and udoban.
**On screen:** Goals · soba/krevet · imam · adjectives

### 1:30 Culture hook
**Narration:** A room above a café is home base. Emir adds a Stolac postcard. stone houses and Radimlja light in Herzegovina.
**On screen:** Stolac · Radimlja · (credit image)

### 3:00 Lesson A: Name the room
**Narration:** Soba, vrata, prozor, krevet, sto, stolica, lampa. Stan and kuća for the wider map.
**On screen (cards):** soba | prozor | krevet | sto | stolica

### 5:00 Lesson B: Imam + descriptions
**Narration:** Imam sobu. Moja soba je mala. Prozor je velik. Krevet je udoban.
**On screen:** Imam… · Moja soba je… · velik/mala/udoban

### 6:30 Mini dialogue
**Narration:** Amira hands over the key. Ana claims the room. Mrvica claims the pillow. Pause and repeat.
**On screen:** Dialogue lines from chapter (BS + EN)

### 8:00 Practice prompt
**Narration:** Match home words. Next: Lesson 11: Kakvo je vrijeme?
**On screen:** Practice · Next: Kakvo je vrijeme? | Subscribe · learnbosnian site

## End screen
- Link to website `/learn/lesson/10`
- Playlist: Learn Bosnian: Book 1
- Image credits in description
"""


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Lesson 8 images…")
    imgs8 = [
        img_entry("livno-town", "Livno townscape in western Bosnia", "day-08-livno.png", "File:Livno.jpg"),
        img_entry("burek-tray", "Tray of baked meat burek", "day-08-burek.png", "File:Burek photo Moma SM.jpg"),
        img_entry("market-fruit", "Fruit crates at a Sarajevo market", "day-08-fruit.png", "File:Fruit market in Sarajevo (3887505834).jpg"),
        img_entry("civic-livno-valley", "Livno valley landscape", "day-08-civic-livno.png", "File:Livno (38263993931).jpg"),
    ]
    print("Downloading Lesson 9 images…")
    imgs9 = [
        img_entry("tuzla-fountain", "Public fountain in Tuzla", "day-09-tuzla-fountain.png", "File:Public fountain, Tuzla, Bosnia.jpg"),
        img_entry("tuzla-old-town", "Tuzla old town street", "day-09-tuzla-street.png", "File:WV banner NE Bosnia Tuzla old town.jpg"),
        img_entry("sarajevo-market", "Open market stalls in Sarajevo", "day-09-market.png", "File:Sarajevo Markt01.jpg"),
        img_entry("civic-tuzla-museum", "Museum of East Bosnia in Tuzla", "day-09-civic-tuzla.png", "File:Museum of East Bosnia, Tuzla.jpg"),
    ]
    print("Downloading Lesson 10 images…")
    imgs10 = [
        img_entry("stolac-radimlja", "Radimlja stećci necropolis near Stolac", "day-10-radimlja.png", "File:Radimlja necropolis near Stolac.JPG"),
        img_entry("radimlja-detail", "Stećak detail at Radimlja", "day-10-radimlja-detail.png", "File:13st Radimlja.jpg"),
        img_entry("konjic-town", "Konjic town in central Bosnia", "day-10-konjic.png", "File:Konjic, Bosnia and Herzegovina.jpg"),
        img_entry("civic-apartment", "Apartment building in Sarajevo", "day-10-civic-apartment.png", "File:Apartment building in Sarajevo.jpg"),
    ]

    write_chapter(8, build_lesson_8(imgs8))
    write_chapter(9, build_lesson_9(imgs9))
    write_chapter(10, build_lesson_10(imgs10))
    write_video(8, VIDEO_8)
    write_video(9, VIDEO_9)
    write_video(10, VIDEO_10)
    print("done")


if __name__ == "__main__":
    main()
