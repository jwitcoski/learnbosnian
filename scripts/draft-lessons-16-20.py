#!/usr/bin/env python3
"""Draft full chapter.json and video-script.md files for Lessons 16 through 20."""
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
FAILED_IMAGE_ATTEMPTS: list[str] = []


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
            "iiurlwidth": 1600,
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
        "downloadUrl": ii.get("thumburl") or url,
        "pageUrl": page_url,
    }


def download_png(commons_title: str, out_name: str) -> dict:
    info = commons_info(commons_title)
    if not info["sourceUrl"]:
        raise FileNotFoundError(f"Commons file does not exist: {commons_title}")
    out = IMG_DIR / out_name
    if out.exists() and out.stat().st_size > 1000:
        return info
    import time

    raw = None
    last_err = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(
                info["downloadUrl"], headers={"User-Agent": UA}
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read()
            break
        except Exception as e:
            last_err = e
            time.sleep(2**attempt)
    if raw is None:
        raise RuntimeError(f"Failed download {commons_title}: {last_err}")
    tmp = out.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        im = Image.open(tmp).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(out, format="PNG", optimize=True)
    finally:
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
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote", path)


def write_video(day: int, text: str):
    path = ROOT / "content" / "book1" / f"day-{day:02d}" / "video-script.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def img_try(id_: str, alt: str, filename: str, titles: list[str]) -> dict:
    """Try Commons file titles in order and return the first successful image."""
    errors = []
    for title in titles:
        try:
            image = img_entry(id_, alt, filename, title)
            print(f"downloaded {filename} from {title}")
            return image
        except Exception as exc:
            message = f"{filename} from {title}: {exc}"
            FAILED_IMAGE_ATTEMPTS.append(message)
            errors.append(message)
            print("image candidate failed", message)
    raise RuntimeError("All Commons candidates failed:\n" + "\n".join(errors))


def quiz_question(id_, prompt, options, correct_index, explanation, skill):
    return {
        "id": id_,
        "question": prompt,
        "options": options,
        "correctIndex": correct_index,
        "explanation": explanation,
        "skill": skill,
    }


def authentic_listen(
    *,
    title,
    kind,
    hook,
    source_title,
    artist,
    scene,
    credit,
    url,
    prompt,
    gist_prompt,
    gist_options,
    gist_index,
    target_words,
    notice,
    key_lines,
    teacher_note,
):
    return {
        "title": title,
        "kind": kind,
        "hook": hook,
        "source": {
            "title": source_title,
            "artistOrSpeaker": artist,
            "regionOrScene": scene,
            "license": "YouTube Terms of Service (embed)",
            "credit": credit,
            "pageUrl": url,
            "embedUrl": url,
        },
        "durationHint": "45-90 seconds",
        "listenTask": {
            "prompt": prompt,
            "gistQuestion": {
                "prompt": gist_prompt,
                "options": gist_options,
                "correctIndex": gist_index,
            },
            "targetWords": target_words,
            "noticePrompt": notice,
        },
        "reveal": {
            "keyLines": key_lines,
            "teacherNote": teacher_note,
        },
    }


def chapter(
    *,
    day,
    title,
    title_en,
    theme,
    story,
    goals,
    vocabulary,
    grammar,
    culture,
    blocks,
    conversation,
    puzzles,
    practice,
    facts,
    resources,
    quiz,
    images,
    civic,
    listen,
    speak_targets,
    section,
    say_again,
    can_do_checks=None,
):
    data = {
        "day": day,
        "book": 1,
        "title": title,
        "titleEn": title_en,
        "theme": theme,
        "status": "draft",
        "reviewedAt": None,
        "reviewerNotes": "This full draft is ready for human review before publication.",
        "estimatedMinutes": 60,
        "storyBeat": story,
        "learningGoals": goals,
        "vocabulary": vocabulary,
        "grammar": grammar,
        "culture": culture,
        "lessonBlocks": blocks,
        "conversation": conversation,
        "puzzles": puzzles,
        "practice": practice,
        "funFacts": facts,
        "resources": resources,
        "sectionQuiz": {
            "title": f"Lesson {day} section quiz",
            "passPercent": 70,
            "questions": quiz,
        },
        "dictionaryEntries": [
            dict_entry(
                day,
                item["bosnian"],
                item["english"],
                item["pronunciation"],
                item["partOfSpeech"],
                item["example"],
            )
            for item in vocabulary
        ],
        "images": images,
        "imagesNeeded": False,
        "imageBriefs": [],
        "civicContext": civic,
        "authenticListen": listen,
        "speakTargets": speak_targets,
        "section": section,
        "sayAgain": say_again,
    }
    if can_do_checks is not None:
        data["canDoChecks"] = can_do_checks
    return data


def say_again(lines):
    return {
        "title": "Say again",
        "intro": "Warm up with four frames you already know.",
        "lines": [{"bosnian": bs, "english": en} for bs, en in lines],
    }


def build_lesson_16(images: list) -> dict:
    v = [
        vocab("autobus", "bus", "OW-toh-boos", "noun", "Autobus ide do Neuma."),
        vocab("karta", "ticket", "KAR-ta", "noun", "Treba mi karta."),
        vocab("stanica", "station", "STA-nee-tsa", "noun", "Stanica je blizu."),
        vocab("vozač", "driver", "VO-zach", "noun", "Vozač čeka putnike."),
        vocab("sjedalo", "seat", "SYEH-da-lo", "noun", "Imam sjedalo uz prozor."),
        vocab("prozor", "window", "PRO-zor", "noun", "Sjedalo uz prozor je lijepo."),
        vocab("dolazak", "arrival", "DO-la-zak", "noun", "Dolazak je u pet sati."),
        vocab("odlazak", "departure", "OD-la-zak", "noun", "Odlazak je uskoro."),
        vocab("treba mi", "I need", "TREH-ba mee", "phrase", "Treba mi karta za Neum."),
        vocab("trebaš", "you need", "TREH-bash", "verb form", "Trebaš kartu, molim."),
        vocab("koliko košta", "how much does it cost", "KO-lee-ko KOSH-ta", "phrase", "Koliko košta karta?"),
        vocab("jednosmjerna", "one-way", "YED-no-smyeh-rna", "adjective", "Jednosmjerna karta, molim."),
        vocab("povratna", "return", "POV-rat-na", "adjective", "Povratna karta, molim."),
        vocab("more", "sea", "MO-reh", "noun", "Želim more u Neumu."),
    ]
    grammar = [
        {
            "title": "Treba mi and trebaš",
            "explanation": "Learn this as a phrase, not a table. Treba mi means I need and takes the thing you need right after it. Trebaš means you need when you speak to one familiar person. Keep the chunk together and stay in the present.",
            "examples": [
                {"bosnian": "Treba mi karta.", "english": "I need a ticket."},
                {"bosnian": "Treba mi autobus.", "english": "I need a bus."},
                {"bosnian": "Trebaš kartu, molim.", "english": "You need a ticket, please."},
            ],
        },
        {
            "title": "Ticket questions at the counter",
            "explanation": "Treat this as a ready chunk you can say today. Ask Koliko košta karta? for the price. Add jednosmjerna or povratna before karta to choose one-way or return. Finish with molim when you speak to the clerk.",
            "examples": [
                {"bosnian": "Koliko košta karta?", "english": "How much does the ticket cost?"},
                {"bosnian": "Jednosmjerna karta, molim.", "english": "A one-way ticket, please."},
                {"bosnian": "Povratna karta, molim.", "english": "A return ticket, please."},
            ],
        },
        {
            "title": "Station timing chunks",
            "explanation": "Say the whole line together; skip the full chart for now. Use odlazak for departure and dolazak for arrival. Pair each word with a clock time you already know. These present-tense lines help you read a board without learning a new tense.",
            "examples": [
                {"bosnian": "Odlazak je uskoro.", "english": "Departure is soon."},
                {"bosnian": "Dolazak je u pet sati.", "english": "Arrival is at five o'clock."},
                {"bosnian": "Autobus ide do Neuma.", "english": "The bus goes to Neum."},
            ],
        },
    ]
    culture_body = (
        "Sarajevo's main bus station sends coaches and minibuses toward lakes and the coast. "
        "Ana buys a ticket while Emir points to a postcard of Jablaničko Lake, the blue water that often appears on the road south. "
        "Their bigger dream is Neum, the short Adriatic stretch that gives Bosnia and Herzegovina a seaside town. "
        "From the window seat they imagine salt air after mountain tunnels and lake curves. "
        "Station boards list odlazak times while travelers clutch coffee and bags. "
        "A clear ticket phrase turns a coast dream into a real departure from the crowded hall. "
    )
    assert 80 <= len(culture_body.split()) <= 120, len(culture_body.split())
    block_a = (
        "Start with autobus, karta, and stanica so the station feels familiar before the doors open. "
        "Add vozač, sjedalo, and prozor so the ride has concrete nouns you can point to. "
        "Practice Treba mi karta until the need chunk sounds automatic at a busy counter. "
        "Then ask Koliko košta karta? "
        "and choose jednosmjerna or povratna before you pay. "
        "Ana stands at the Sarajevo counter with Emir and imagines the lake stop near Jablanica. "
        "The coast dream needs a ticket first, not a full travel grammar chart for every case. "
        "Say each counter line twice, then point to the board and name odlazak or dolazak in a full sentence. "
    )
    block_b = (
        "Move from the counter to the seat once the ticket is in your hand. "
        "Say Imam sjedalo uz prozor when you claim a window and want the lake view later. "
        "Reuse Molim and Hvala with the clerk, then tell a friend Trebaš kartu before the doors close. "
        "Ana wants Neum, Emir wants the lake view, and Mrvica stays home with Amira for the day. "
        "Keep every sentence in the present so you can buy and board today without past or future charts. "
        "Practice a short chain aloud: need, price, ticket type, seat, thank you, and one calm boarding sentence. "
        "Repeat the chain until boarding feels easy. "
    )
    assert 100 <= len(block_a.split()) <= 180, len(block_a.split())
    assert 100 <= len(block_b.split()) <= 180, len(block_b.split())
    civic_body = (
        "Road travel across Bosnia and Herzegovina still crosses entity and canton boundaries that shape daily movement. "
        "Corridor A1 and related motorway projects aim to connect the coast with inland cities, yet unfinished segments and entity-level planning create friction for drivers and coaches. "
        "A ticket to Neum can mean changing roads, signs, and even the feel of administration along the way. "
        "Learners who travel by bus notice that geography and governance sit on the same map. "
        "Better corridors reduce isolation, but fragmented responsibility remains a structural travel pressure."
    )
    facts = [
        {
            "title": "Neum is the short coast",
            "body": "Neum is the Adriatic town that gives Bosnia and Herzegovina a coastline. The stretch is short compared with neighboring countries, yet it still offers beaches and seafood. Travelers often reach it by road from inland cities. The coast dream in this lesson is therefore a real destination, not only a postcard fantasy.",
        },
        {
            "title": "Jablanica sits on the lake road",
            "body": "Jablaničko Lake appears on many southbound routes from Sarajevo. The water sits in a mountain corridor and often becomes a rest stop in travelers' stories. Emir's postcard keeps the lake visible while Ana buys tickets. The stop reminds learners that the coast journey includes inland beauty.",
        },
        {
            "title": "Treba mi is a survival chunk",
            "body": "Treba mi plus a noun is one of the fastest ways to name a need at a counter. You do not need a full conjugation chart to buy a ticket. Pair the chunk with molim and you sound ready for a clerk. Present-tense survival phrases keep Book 1 practical.",
        },
        {
            "title": "Window seats teach prozor",
            "body": "Sjedalo uz prozor turns furniture words into travel comfort. Learners already know short location phrases, and the window seat makes them memorable. Ana chooses the view toward lake and coast. The ride becomes vocabulary practice with a real landscape.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does karta mean at the station?", ["Ticket", "Driver", "Window", "Lake"], 0, "Karta means ticket in this travel context.", "vocabulary"),
        quiz_question("q2", "Which chunk means I need a ticket?", ["Koliko košta karta?", "Treba mi karta.", "Odlazak je uskoro.", "Imam sjedalo."], 1, "Treba mi karta means I need a ticket.", "grammar"),
        quiz_question("q3", "Which word means departure?", ["dolazak", "stanica", "odlazak", "sjedalo"], 2, "Odlazak means departure.", "vocabulary"),
        quiz_question("q4", "Which ticket is a return ticket?", ["jednosmjerna", "povratna", "prozor", "vozač"], 1, "Povratna means return.", "vocabulary"),
        quiz_question("q5", "What coast town do Ana and Emir dream about?", ["Neum", "Brčko", "Zenica", "Livno"], 0, "They dream about Neum on the Adriatic coast.", "dialogue"),
        quiz_question("q6", "How do you politely ask the price?", ["Trebaš kartu.", "Autobus ide.", "Koliko košta karta?", "Dolazak je u pet sati."], 2, "Koliko košta karta? asks the price.", "grammar"),
        quiz_question("q7", "Which lake appears on the route postcard?", ["Jablaničko Lake", "Una only", "Pliva only", "The Adriatic itself"], 0, "Jablaničko Lake appears on Emir's postcard.", "culture"),
        quiz_question("q8", "Why can bus travel feel complicated across the country?", ["Only one road exists.", "Entity and corridor planning can fragment routes.", "Tickets are free.", "Buses never leave Sarajevo."], 1, "Entity borders and unfinished corridors create travel friction.", "culture"),
        quiz_question("q9", "Which sentence claims a window seat?", ["Imam sjedalo uz prozor.", "Treba mi more.", "Vozač čeka.", "Stanica je daleko."], 0, "Imam sjedalo uz prozor claims a window seat.", "listening"),
    ]
    return chapter(
        day=16,
        title="Na autobus",
        title_en="On the bus",
        theme="Bus tickets and coast dreams",
        story="Ana and Emir buy bus tickets and dream of Jablanica lake views and Neum on the coast.",
        goals={
            "vocabulary": [
                "Buy a bus ticket with karta, stanica, and price phrases.",
                "Name seat, window, driver, departure, and arrival words.",
                "Talk about a coast trip toward Neum.",
            ],
            "grammar": [
                "Use Treba mi and trebaš as present need chunks.",
                "Ask Koliko košta karta? and choose jednosmjerna or povratna.",
                "Read odlazak and dolazak on a station board.",
            ],
            "culture": [
                "Start from the Sarajevo bus station toward lake and coast.",
                "Picture Jablaničko Lake on the southbound road.",
                "Notice how road corridors and entity borders affect travel.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "From the station toward lake and coast",
            "body": culture_body,
            "imageId": "sarajevo-bus-station",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Ticket counter phrases",
                "body": block_a,
                "tips": [
                    "Keep Treba mi and the noun together as one chunk.",
                    "Add molim when you speak to the ticket clerk.",
                    "Choose jednosmjerna or povratna before you pay.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Board and dream of Neum",
                "body": block_b,
                "tips": [
                    "Reuse Hvala after you receive the ticket.",
                    "Practice sjedalo uz prozor before you sit.",
                    "Stay in present tense even when you talk about the coast dream.",
                ],
            },
        ],
        conversation={
            "title": "Karta za more",
            "setting": "Ana and Emir stand at the Sarajevo bus station ticket counter.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Treba mi karta za Neum, molim.", "english": "I need a ticket to Neum, please."},
                {"speaker": "Clerk", "bosnian": "Jednosmjerna ili povratna?", "english": "One-way or return?"},
                {"speaker": "Emir", "bosnian": "Povratna, molim. Koliko košta karta?", "english": "Return, please. How much does the ticket cost?"},
                {"speaker": "Clerk", "bosnian": "Evo karte. Odlazak je uskoro.", "english": "Here is the ticket. Departure is soon."},
                {"speaker": "Ana", "bosnian": "Hvala! Imam sjedalo uz prozor?", "english": "Thank you! Do I have a window seat?"},
                {"speaker": "Emir", "bosnian": "Da. Želim vidjeti Jablanicu i more.", "english": "Yes. I want to see Jablanica and the sea."},
                {"speaker": "Ana", "bosnian": "Hajde da idemo na autobus.", "english": "Let us go to the bus."},
                {"speaker": "Narrator", "bosnian": "Mrvica spava kod Amire, daleko od autobusa.", "english": "Mrvica sleeps at Amira's, far from the bus."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match travel words",
                "prompt": "Match each Bosnian travel word with its English meaning.",
                "items": [
                    {"left": "karta", "right": "ticket"},
                    {"left": "stanica", "right": "station"},
                    {"left": "odlazak", "right": "departure"},
                    {"left": "dolazak", "right": "arrival"},
                    {"left": "more", "right": "sea"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false on the bus",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Treba mi karta means I need a ticket.", "answer": True},
                    {"statement": "Jednosmjerna means a return ticket.", "answer": False},
                    {"statement": "Neum is on the Adriatic coast.", "answer": True},
                    {"statement": "Odlazak means arrival.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian chunk for I need a ticket.", "hint": "Begin with Treba mi.", "answer": "Treba mi karta."},
            {"id": "pr2", "prompt": "Write the polite price question for a ticket.", "hint": "Begin with Koliko.", "answer": "Koliko košta karta?"},
            {"id": "pr3", "prompt": "Write the Bosnian for A return ticket, please.", "hint": "Use povratna and molim.", "answer": "Povratna karta, molim."},
            {"id": "pr4", "prompt": "Write the Bosnian for Departure is soon.", "hint": "Use odlazak.", "answer": "Odlazak je uskoro."},
            {"id": "pr5", "prompt": "Write the Bosnian for I have a window seat.", "hint": "Use sjedalo and prozor.", "answer": "Imam sjedalo uz prozor."},
            {"id": "pr6", "prompt": "Write the Bosnian word for bus.", "hint": "It begins with auto.", "answer": "autobus"},
            {"id": "pr7", "prompt": "Write the Bosnian word for station.", "hint": "It begins with sta.", "answer": "stanica"},
        ],
        facts=facts,
        resources=[
            {"label": "Learn Bosnian: Telling Time", "url": "https://www.youtube.com/watch?v=0xiYbtHQaDc", "note": "Clock phrases help you read departure boards at the station."},
            {"label": "Next lesson", "url": "/learn/lesson/17", "note": "Lesson 17 takes Ana and Emir into a restaurant debate."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the lesson."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Fragmented roads and coast access",
            "body": civic_body,
            "imageId": "civic-a1-corridor",
            "learnMore": {
                "label": "Wikipedia article about A1 motorway in Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/A1_(Bosnia_and_Herzegovina)",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with clock phrases for departures",
            kind="speaker",
            hook="A teacher models time phrases you can reuse when a bus board lists the hour.",
            source_title="Learn Bosnian: Telling Time (Sati i Minuti)",
            artist="Lingo Hero",
            scene="Clock and schedule language",
            credit="Lingo Hero on YouTube",
            url="https://www.youtube.com/watch?v=0xiYbtHQaDc",
            prompt="Listen for a time phrase you could place beside odlazak or dolazak.",
            gist_prompt="What is the speaker mainly teaching?",
            gist_options=["Telling time and clock language", "Football rules", "Holiday greetings", "Phone emergencies"],
            gist_index=0,
            target_words=["sati", "koliko"],
            notice="You do not need every number. Catch the question shape for time.",
            key_lines=[
                {"bosnian": "Koliko je sati?", "english": "What time is it?"},
                {"bosnian": "Odlazak je uskoro.", "english": "Departure is soon."},
            ],
            teacher_note="After the clip, say one departure sentence with a time you know.",
        ),
        speak_targets=[0, 2, 4],
        section=3,
        say_again=say_again(
            [
                ("Kakvo je vrijeme?", "How is the weather?"),
                ("Idite pravo, molim vas.", "Go straight, please."),
                ("Hajde da idemo.", "Let us go."),
                ("Hvala!", "Thank you!"),
            ]
        ),
    )


def build_lesson_17(images: list) -> dict:
    v = [
        vocab("restoran", "restaurant", "reh-sto-RAN", "noun", "Idemo u restoran."),
        vocab("jelovnik", "menu", "yeh-LOV-neek", "noun", "Jelovnik je na stolu."),
        vocab("konobar", "waiter", "ko-NO-bar", "noun", "Konobar dolazi."),
        vocab("klepe", "Bosnian dumplings", "KLEH-peh", "noun", "Hoću klepe."),
        vocab("japrak", "stuffed vine leaves", "YAH-prak", "noun", "Hoću japrak."),
        vocab("narudžba", "order", "nah-ROOJ-ba", "noun", "Narudžba je gotova."),
        vocab("račun", "bill", "RAH-choon", "noun", "Račun, molim."),
        vocab("hoću", "I want", "HO-choo", "verb form", "Hoću klepe, molim."),
        vocab("hoćeš", "you want", "HO-chesh", "verb form", "Hoćeš li japrak?"),
        vocab("hoćemo", "we want", "HO-cheh-mo", "verb form", "Hoćemo jesti."),
        vocab("ukusan", "tasty (m.)", "OO-koo-san", "adjective", "Japrak je ukusan."),
        vocab("ukusna", "tasty (f.)", "OO-koos-na", "adjective", "Juha je ukusna."),
        vocab("dobar tek", "enjoy your meal", "DO-bar tek", "phrase", "Dobar tek!"),
        vocab("još", "more or another", "yosh", "adverb", "Još hlijeba, molim."),
    ]
    grammar = [
        {
            "title": "Hoću, hoćeš, hoćemo",
            "explanation": "Hold this as a spoken pattern, not a grammar grid. Hoću means I want, hoćeš asks or states what you want, and hoćemo covers we want. Keep these present forms as restaurant chunks. Do not expand into past or future paradigms yet.",
            "examples": [
                {"bosnian": "Hoću klepe.", "english": "I want klepe."},
                {"bosnian": "Hoćeš li japrak?", "english": "Do you want japrak?"},
                {"bosnian": "Hoćemo jesti.", "english": "We want to eat."},
            ],
        },
        {
            "title": "Ordering with molim and račun",
            "explanation": "Learn the usable chunk first; full tables can wait. Place the food word first, then molim. When you finish, say Račun, molim for the bill. Politeness keeps a public restaurant scene smooth.",
            "examples": [
                {"bosnian": "Klepe, molim.", "english": "Klepe, please."},
                {"bosnian": "Japrak, molim.", "english": "Japrak, please."},
                {"bosnian": "Račun, molim.", "english": "The bill, please."},
            ],
        },
        {
            "title": "Dobar tek at the table",
            "explanation": "Keep this as a sayable line rather than a paradigm list. Dobar tek wishes someone an enjoyable meal. Say it when food arrives, then answer with Hvala. The phrase works among friends and with restaurant staff.",
            "examples": [
                {"bosnian": "Dobar tek!", "english": "Enjoy your meal!"},
                {"bosnian": "Dobar tek, Ana!", "english": "Enjoy your meal, Ana!"},
                {"bosnian": "Hvala, dobar tek!", "english": "Thanks, enjoy your meal!"},
            ],
        },
    ]
    culture_body = (
        "Sarajevo restaurants still argue gently about favorite trays when friends share a table. "
        "Klepe are soft dumplings often served with sauce and garlic yogurt energy on a busy night. "
        "Japrak wraps rice and meat in vine leaves and arrives as neat rolls that invite a slow bite. "
        "Ana and Emir open a jelovnik and turn the debate into practice with hoću and hoćeš. "
        "A Visoko postcard on the table reminds them that food stories travel beyond one city street. "
        "Saying Dobar tek seals the meal as a shared social moment before anyone reaches for the bill. "
    )
    assert 80 <= len(culture_body.split()) <= 120, len(culture_body.split())
    block_a = (
        "Learn restoran, jelovnik, konobar, klepe, and japrak first so the room has clear names. "
        "Then lock the present chunks Hoću, Hoćeš li, and Hoćemo as ready wanting lines. "
        "Ana wants klepe. "
        "Emir wants japrak. "
        "Their friendly disagreement is the lesson engine. "
        "Point at the menu and say the food word with molim instead of inventing long sentences. "
        "Stay in the present so the order is ready for a real waiter tonight without extra paradigms. "
        "Repeat each dish name twice, then switch roles so both of you can ask and answer with hoćeš. "
        "Keep the wanting chunks short and reusable at the table. "
    )
    block_b = (
        "Build the full table flow from greeting to goodbye in short present lines. "
        "Greet, order with hoću, wish Dobar tek, ask for još if you need bread, then call for račun. "
        "Reuse Hvala after every helpful move from the konobar so politeness stays audible. "
        "Amira may appear with an opinion, and Mrvica watches for crumbs under the table as always. "
        "The Visoko postcard keeps the meal tied to a wider map of Bosnian kitchens beyond Sarajevo. "
        "Practice the debate until both dishes feel easy to pronounce and easy to defend with a smile. "
        "End by asking for the bill with a calm polite voice. "
    )
    assert 100 <= len(block_a.split()) <= 180, len(block_a.split())
    assert 100 <= len(block_b.split()) <= 180, len(block_b.split())
    civic_body = (
        "Hospitality and food service are visible parts of recovery and everyday economy in Bosnia and Herzegovina. "
        "Cafés and restaurants create jobs, welcome return visits, and keep local recipes in public life after years of disruption. "
        "A simple order for klepe or japrak supports kitchens that teach taste and employ neighbors on ordinary evenings. "
        "Tourism and local dining both matter, yet wages and seasonal demand can stay uneven across towns. "
        "Learners who eat out practice language inside a sector that helps cities feel open, busy, and welcoming again. "
    )
    facts = [
        {
            "title": "Klepe invite sauce and garlic",
            "body": "Klepe are boiled dumplings that often arrive with a savory sauce. Many diners add garlic yogurt flavor at the table. The dish feels homey even in a busy restaurant. Ana's order makes the soft dumpling a speaking target.",
        },
        {
            "title": "Japrak wraps the vine leaf",
            "body": "Japrak uses vine leaves around a rice and meat filling. The rolls cook slowly and taste bright with lemon or sauce. Emir defends japrak as the wiser tray. The debate keeps both food names active.",
        },
        {
            "title": "Visoko sits on the food map",
            "body": "A postcard from Visoko reminds diners that Bosnian kitchens are not only Sarajevo scenes. Towns across the country share related stuffed and dough dishes with local twists. The card widens the meal without leaving the table. Geography becomes part of the restaurant chat.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does jelovnik mean?", ["Menu", "Bill", "Waiter", "Dumpling"], 0, "Jelovnik means menu.", "vocabulary"),
        quiz_question("q2", "Which form means I want?", ["hoćeš", "hoću", "hoćemo", "račun"], 1, "Hoću means I want.", "grammar"),
        quiz_question("q3", "Which dish uses vine leaves?", ["klepe", "burek", "japrak", "jogurt"], 2, "Japrak uses vine leaves.", "vocabulary"),
        quiz_question("q4", "How do you ask for the bill?", ["Dobar tek!", "Hoćemo jesti.", "Još hlijeba.", "Račun, molim."], 3, "Račun, molim asks for the bill.", "grammar"),
        quiz_question("q5", "What do Ana and Emir debate?", ["Klepe versus japrak", "Bus versus tram", "Snow versus rain", "Left versus right"], 0, "They debate klepe versus japrak.", "dialogue"),
        quiz_question("q6", "What does Dobar tek mean?", ["Where is the station?", "Enjoy your meal!", "I need a ticket.", "Who is calling?"], 1, "Dobar tek means enjoy your meal.", "vocabulary"),
        quiz_question("q7", "Which town appears on the postcard?", ["Visoko", "Neum", "Zenica", "Brčko"], 0, "Visoko appears on the postcard.", "culture"),
        quiz_question("q8", "Why do restaurants matter beyond the plate?", ["They erase all travel rules.", "They support jobs and public hospitality.", "They replace schools.", "They ban tourist menus."], 1, "Food service supports jobs and hospitality in recovery.", "culture"),
        quiz_question("q9", "Which sentence orders klepe politely?", ["Hoću klepe, molim.", "Klepe je račun.", "Hoćeš li stanica?", "Dobar tek je jelovnik."], 0, "Hoću klepe, molim is a polite order.", "listening"),
    ]
    return chapter(
        day=17,
        title="Dobar tek!",
        title_en="Enjoy your meal!",
        theme="Restaurant debate over klepe and japrak",
        story="Ana and Emir debate klepe versus japrak at a Sarajevo restaurant.",
        goals={
            "vocabulary": [
                "Order klepe or japrak from a restaurant menu.",
                "Use waiter, bill, and meal-wish words at the table.",
                "Describe food as ukusan or ukusna.",
            ],
            "grammar": [
                "Use hoću, hoćeš, and hoćemo as present wanting chunks.",
                "Order with molim and ask for račun politely.",
                "Say Dobar tek when the food arrives.",
            ],
            "culture": [
                "Compare klepe and japrak as beloved Bosnian dishes.",
                "Keep Visoko on the wider food map with a postcard.",
                "Notice hospitality as part of everyday recovery.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Klepe, japrak, and a full table",
            "body": culture_body,
            "imageId": "klepe-sarajevo",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Wanting food with htjeti chunks",
                "body": block_a,
                "tips": [
                    "Say Hoću plus the dish as one ready line.",
                    "Use Hoćeš li for a friendly question.",
                    "Keep htjeti in the present only.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: From order to račun",
                "body": block_b,
                "tips": [
                    "Add molim to every order and to Račun, molim.",
                    "Answer Dobar tek with Hvala.",
                    "Name both dishes so the debate stays balanced.",
                ],
            },
        ],
        conversation={
            "title": "Klepe ili japrak?",
            "setting": "Ana and Emir sit in a busy Sarajevo restaurant with a Visoko postcard on the table.",
            "lines": [
                {"speaker": "Konobar", "bosnian": "Izvolite. Jelovnik je tu.", "english": "Here you are. The menu is here."},
                {"speaker": "Ana", "bosnian": "Hoću klepe, molim.", "english": "I want klepe, please."},
                {"speaker": "Emir", "bosnian": "A ja hoću japrak, molim.", "english": "And I want japrak, please."},
                {"speaker": "Ana", "bosnian": "Hoćeš li probati klepe?", "english": "Do you want to try klepe?"},
                {"speaker": "Emir", "bosnian": "Možda. Japrak je ukusan!", "english": "Maybe. Japrak is tasty!"},
                {"speaker": "Konobar", "bosnian": "Dobar tek!", "english": "Enjoy your meal!"},
                {"speaker": "Ana", "bosnian": "Hvala! Račun, molim, poslije.", "english": "Thank you! The bill, please, afterward."},
                {"speaker": "Narrator", "bosnian": "Mrvica čeka mrvice pod stolom.", "english": "Mrvica waits for crumbs under the table."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match restaurant words",
                "prompt": "Match each Bosnian restaurant word with its English meaning.",
                "items": [
                    {"left": "jelovnik", "right": "menu"},
                    {"left": "konobar", "right": "waiter"},
                    {"left": "račun", "right": "bill"},
                    {"left": "klepe", "right": "dumplings"},
                    {"left": "japrak", "right": "stuffed vine leaves"},
                ],
            },
            {
                "id": "p2",
                "type": "scramble",
                "title": "Unscramble the order",
                "prompt": "Unscramble to make today's polite restaurant phrases.",
                "items": [
                    {
                        "scrambled": "klepe Hoću molim",
                        "answer": "hoću klepe molim",
                    },
                    {
                        "scrambled": "molim Račun",
                        "answer": "račun molim",
                    },
                    {
                        "scrambled": "tek Dobar",
                        "answer": "dobar tek",
                    },
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write I want klepe, please. in Bosnian.", "hint": "Begin with Hoću.", "answer": "Hoću klepe, molim."},
            {"id": "pr2", "prompt": "Write Do you want japrak? in Bosnian.", "hint": "Begin with Hoćeš li.", "answer": "Hoćeš li japrak?"},
            {"id": "pr3", "prompt": "Write The bill, please. in Bosnian.", "hint": "Use račun.", "answer": "Račun, molim."},
            {"id": "pr4", "prompt": "Write Enjoy your meal! in Bosnian.", "hint": "Two words.", "answer": "Dobar tek!"},
            {"id": "pr5", "prompt": "Write We want to eat. in Bosnian.", "hint": "Use hoćemo.", "answer": "Hoćemo jesti."},
            {"id": "pr6", "prompt": "Write the Bosnian word for menu.", "hint": "It begins with jel.", "answer": "jelovnik"},
            {"id": "pr7", "prompt": "Write the Bosnian word for waiter.", "hint": "It begins with kon.", "answer": "konobar"},
            {"id": "pr8", "prompt": "Write Japrak is tasty. in Bosnian (masculine form).", "hint": "Use ukusan.", "answer": "Japrak je ukusan."},
        ],
        facts=facts,
        resources=[
            {"label": "Bosnian Coffee with local guides", "url": "https://www.youtube.com/watch?v=wFGbkVzNCFU", "note": "Café hospitality speech supports restaurant listening."},
            {"label": "Next lesson", "url": "/learn/lesson/18", "note": "Lesson 18 moves into sports and hobbies."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Find more everyday speaker models on the channel."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Hospitality keeps cities open",
            "body": civic_body,
            "imageId": "civic-food-economy",
            "learnMore": {
                "label": "Wikipedia article about cuisine of Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Bosnia_and_Herzegovina_cuisine",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu in café hospitality speech",
            kind="speaker",
            hook="A Sarajevo guide talks through coffee hospitality, a close cousin of restaurant politeness.",
            source_title="Bosnian Coffee - Explore Sarajevo with Local Guides",
            artist="Meet Bosnia Tours (Edin)",
            scene="Café and hospitality talk",
            credit="Meet Bosnia Tours on YouTube",
            url="https://www.youtube.com/watch?v=wFGbkVzNCFU",
            prompt="Listen for warm hosting language and any food or coffee ritual cues.",
            gist_prompt="Where does this speech feel at home?",
            gist_options=["A café or hospitality scene", "A football locker room only", "A silent library exam", "A mountain weather robot"],
            gist_index=0,
            target_words=["kahva", "molim"],
            notice="Catch the polite hosting mood even if some talk is bilingual.",
            key_lines=[
                {"bosnian": "Izvolite.", "english": "Here you are / please have it."},
                {"bosnian": "Dobar tek!", "english": "Enjoy your meal!"},
            ],
            teacher_note="After listening, place an order with hoću and molim.",
        ),
        speak_targets=[1, 2, 5],
        section=3,
        say_again=say_again(
            [
                ("Treba mi karta.", "I need a ticket."),
                ("Koliko košta karta?", "How much does the ticket cost?"),
                ("Volim burek.", "I love burek."),
                ("Molim.", "Please."),
            ]
        ),
    )


def build_lesson_18(images: list) -> dict:
    v = [
        vocab("sport", "sport", "sport", "noun", "Sport je zabavan."),
        vocab("hobi", "hobby", "HO-bee", "noun", "Moj hobi je šetnja."),
        vocab("fudbal", "football", "FOOD-bal", "noun", "Volim fudbal."),
        vocab("igrati", "to play", "EE-gra-tee", "verb", "Volim igrati fudbal."),
        vocab("igram", "I play", "EE-gram", "verb form", "Igram fudbal."),
        vocab("gledati", "to watch", "GLEH-da-tee", "verb", "Volim gledati fudbal."),
        vocab("gledam", "I watch", "GLEH-dam", "verb form", "Gledam utakmicu."),
        vocab("utakmica", "match", "oo-TAK-mee-tsa", "noun", "Utakmica je danas."),
        vocab("često", "often", "CHES-to", "adverb", "Često igram fudbal."),
        vocab("ponekad", "sometimes", "PO-ne-kad", "adverb", "Ponekad gledam utakmicu."),
        vocab("rijeka", "river", "REE-ye-ka", "noun", "Rijeka Una je lijepa."),
        vocab("šetnja", "walk", "SHET-nya", "noun", "Šetnja uz rijeku je mirna."),
        vocab("trčati", "to run", "TR-cha-tee", "verb", "Volim trčati."),
        vocab("tim", "team", "teem", "noun", "Moj tim igra dobro."),
    ]
    grammar = [
        {
            "title": "Igram and gledam",
            "explanation": "Memorize the phrase shape; leave the full table for later. Igram covers I play, and gledam covers I watch. Add fudbal or utakmica to finish the chunk. These present forms are enough for a stadium chat today.",
            "examples": [
                {"bosnian": "Igram fudbal.", "english": "I play football."},
                {"bosnian": "Gledam utakmicu.", "english": "I watch the match."},
                {"bosnian": "Volim igrati fudbal.", "english": "I like to play football."},
            ],
        },
        {
            "title": "Često and ponekad",
            "explanation": "Take this as a speaking chunk, not a case chart. Place često or ponekad before the verb to show how often you do something. Često means often, and ponekad means sometimes. Keep the rest of the sentence in the present.",
            "examples": [
                {"bosnian": "Često igram fudbal.", "english": "I often play football."},
                {"bosnian": "Ponekad gledam utakmicu.", "english": "I sometimes watch the match."},
                {"bosnian": "Često idem na šetnju.", "english": "I often go for a walk."},
            ],
        },
        {
            "title": "Hobby lines with volim",
            "explanation": "Practice the whole expression before you worry about paradigms. Reuse Volim plus an activity noun or infinitive. Pair sports with river walks so hobbies feel wider than one stadium. Short present lines keep the chat friendly.",
            "examples": [
                {"bosnian": "Volim fudbal.", "english": "I love football."},
                {"bosnian": "Volim šetnju.", "english": "I love walks."},
                {"bosnian": "Moj hobi je šetnja.", "english": "My hobby is walking."},
            ],
        },
    ]
    culture_body = (
        "Zenica's Bilino Polje stadium gives football a loud local home on match days. "
        "Ana and Emir talk about the tim, the utakmica, and who watches versus who plays. "
        "A second postcard shows Štrbački buk on the Una River, where water crashes white over stone. "
        "Weekend life can mean a packed stand one afternoon and a river walk the next morning. "
        "Crowds chant, then later the path grows quiet beside the water. "
        "Hobby words stay honest when they include both the stadium noise and the calm path. "
    )
    assert 80 <= len(culture_body.split()) <= 120, len(culture_body.split())
    block_a = (
        "Begin with sport, hobi, fudbal, utakmica, and tim so the stadium vocabulary is concrete. "
        "Then practice Igram and Gledam as separate present chunks you can finish with a noun. "
        "Ana often watches. "
        "Emir sometimes plays. "
        "Frequency words često and ponekad make the difference clear. "
        "Say each sentence while pointing to the Bilino Polje image so the place anchors the verb. "
        "Do not build a full verb chart yet; reuse the ready lines until they feel automatic. "
        "Finish Lesson A by telling a partner how often you watch and how often you play in two short lines. "
        "Keep both frequency words active in your answers. "
    )
    block_b = (
        "Move from the stadium to the river postcard without dropping the football words you just learned. "
        "Use Volim šetnju and Rijeka Una je lijepa to balance the match talk with outdoor calm. "
        "Ask a friend Hoćeš li gledati utakmicu? "
        "and answer with često or ponekad plus a present verb. "
        "Amira prefers the waterfall walk, while Mrvica prefers any path that might hide snacks. "
        "Close by naming one sport habit and one nature habit in the present tense only. "
        "The goal is a weekend self-portrait you can say aloud, not a list of abstract hobby nouns. "
        "Repeat your two habits until they sound natural. "
    )
    assert 100 <= len(block_a.split()) <= 180, len(block_a.split())
    assert 100 <= len(block_b.split()) <= 180, len(block_b.split())
    civic_body = (
        "Many young people from Bosnia and Herzegovina leave for study or work abroad, and stadium crowds feel that absence. "
        "Remittances and return visits keep ties alive, yet local clubs and weekend hobbies also need people who stay. "
        "An airport departure hall can mark opportunity and loss at the same time. "
        "Sports talk therefore sits beside a civic question about who remains to play, coach, and watch. "
        "Learners should hear both the joy of a match and the pressure of emigration."
    )
    facts = [
        {
            "title": "Bilino Polje anchors Zenica football",
            "body": "Bilino Polje is the main football stadium in Zenica. National and club matches have made the ground familiar across the country. The wide stands give learners a clear sports image beyond Sarajevo. Saying utakmica beside this ground makes the word feel loud and real.",
        },
        {
            "title": "Štrbački buk shows the Una",
            "body": "Štrbački buk is a waterfall stretch on the Una River near the northwestern border area. White water over wide stone shelves draws walkers and photographers. The postcard balances stadium noise with river calm. Hobby vocabulary needs both kinds of weekend.",
        },
        {
            "title": "Često beats a long chart",
            "body": "Frequency adverbs let beginners tell the truth about habits without new tenses. Često and ponekad fit in front of present verbs you already know. The pattern is small and reusable. Honesty about how often you play keeps conversation human.",
        },
        {
            "title": "Hobi can be quiet",
            "body": "Not every hobby is a competitive sport. Šetnja along a river counts, and so does watching from the stands. Book 1 keeps the word open on purpose. Learners should claim the activity they will actually repeat.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does utakmica mean?", ["Team", "Match", "River", "Hobby"], 1, "Utakmica means match.", "vocabulary"),
        quiz_question("q2", "Which sentence means I play football?", ["Gledam fudbal.", "Igram fudbal.", "Rijeka je hobi.", "Ponekad je tim."], 1, "Igram fudbal means I play football.", "grammar"),
        quiz_question("q3", "Which word means often?", ["ponekad", "često", "šetnja", "tim"], 1, "Često means often.", "vocabulary"),
        quiz_question("q4", "Which place is the Zenica stadium?", ["Bilino Polje", "Latin Bridge", "Neum beach", "Ferhadija"], 0, "Bilino Polje is the Zenica stadium.", "culture"),
        quiz_question("q5", "What second landscape balances the football chat?", ["A Una River waterfall walk", "A desert dune", "A desert stadium", "A closed airport only"], 0, "Štrbački buk on the Una balances the chat.", "dialogue"),
        quiz_question("q6", "Which sentence means I sometimes watch the match?", ["Često igram fudbal.", "Ponekad gledam utakmicu.", "Volim račun.", "Treba mi karta."], 1, "Ponekad gledam utakmicu uses sometimes plus watch.", "grammar"),
        quiz_question("q7", "What does gledam mean?", ["I watch", "I run", "I need", "I order"], 0, "Gledam means I watch.", "vocabulary"),
        quiz_question("q8", "What civic pressure sits beside youth sports?", ["Young people leaving for work or study abroad", "Too many waterfalls", "Free tickets only", "No football words"], 0, "Youth emigration for work or study is a related civic pressure.", "culture"),
        quiz_question("q9", "Which line names a walking hobby?", ["Moj hobi je šetnja.", "Račun, molim.", "Jednosmjerna karta.", "Ko je tamo?"], 0, "Moj hobi je šetnja names walking as a hobby.", "listening"),
    ]
    return chapter(
        day=18,
        title="Sport i hobiji",
        title_en="Sports and hobbies",
        theme="Football chat and river walks",
        story="Ana and Emir compare football at Bilino Polje with quiet walks by the Una.",
        goals={
            "vocabulary": [
                "Talk about football, matches, teams, and hobbies.",
                "Use river and walk words for a nature hobby.",
                "Contrast playing and watching with igrati and gledati forms.",
            ],
            "grammar": [
                "Use igram and gledam in the present.",
                "Add često and ponekad to describe habits.",
                "Reuse Volim with sports and walks.",
            ],
            "culture": [
                "Visit Bilino Polje in Zenica through the lesson images.",
                "Add Štrbački buk on the Una as a postcard walk.",
                "Understand youth emigration as a pressure beside local sports life.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Stadium noise and river calm",
            "body": culture_body,
            "imageId": "bilino-polje",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Play, watch, and how often",
                "body": block_a,
                "tips": [
                    "Keep igram and gledam as separate ready chunks.",
                    "Put često or ponekad before the verb.",
                    "Name the team or match to finish the line.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: From stands to river path",
                "body": block_b,
                "tips": [
                    "Balance football lines with šetnja vocabulary.",
                    "Ask Hoćeš li gledati utakmicu? in a friendly voice.",
                    "Claim one hobby you will actually repeat.",
                ],
            },
        ],
        conversation={
            "title": "Utakmica ili šetnja?",
            "setting": "Ana and Emir look at a Bilino Polje photo and an Una waterfall postcard.",
            "lines": [
                {"speaker": "Emir", "bosnian": "Često gledam fudbal u Zenici.", "english": "I often watch football in Zenica."},
                {"speaker": "Ana", "bosnian": "Ja ponekad gledam utakmicu.", "english": "I sometimes watch a match."},
                {"speaker": "Emir", "bosnian": "Igram u parku, ali volim i stadion.", "english": "I play in the park, but I also love the stadium."},
                {"speaker": "Ana", "bosnian": "Moj hobi je šetnja uz rijeku.", "english": "My hobby is a walk by the river."},
                {"speaker": "Amira", "bosnian": "Štrbački buk je prelijep, molim vas pogledajte!", "english": "Štrbački buk is beautiful, please look!"},
                {"speaker": "Emir", "bosnian": "Hoćeš li ići na utakmicu?", "english": "Do you want to go to the match?"},
                {"speaker": "Ana", "bosnian": "Možda. Hvala na ideji!", "english": "Maybe. Thanks for the idea!"},
                {"speaker": "Narrator", "bosnian": "Mrvica bira šetnju, jer ima mirisa.", "english": "Mrvica chooses the walk, because there are smells."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match hobby words",
                "prompt": "Match each Bosnian word with its English meaning.",
                "items": [
                    {"left": "fudbal", "right": "football"},
                    {"left": "utakmica", "right": "match"},
                    {"left": "često", "right": "often"},
                    {"left": "ponekad", "right": "sometimes"},
                    {"left": "šetnja", "right": "walk"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about hobbies",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Igram means I play.", "answer": True},
                    {"statement": "Ponekad means often.", "answer": False},
                    {"statement": "Bilino Polje is in Zenica.", "answer": True},
                    {"statement": "Štrbački buk is a desert stadium.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write I play football. in Bosnian.", "hint": "Begin with Igram.", "answer": "Igram fudbal."},
            {"id": "pr2", "prompt": "Write I watch the match. in Bosnian.", "hint": "Use gledam.", "answer": "Gledam utakmicu."},
            {"id": "pr3", "prompt": "Write I often play football. in Bosnian.", "hint": "Start with Često.", "answer": "Često igram fudbal."},
            {"id": "pr4", "prompt": "Write I sometimes watch the match. in Bosnian.", "hint": "Start with Ponekad.", "answer": "Ponekad gledam utakmicu."},
            {"id": "pr5", "prompt": "Write My hobby is walking. in Bosnian.", "hint": "Use hobi and šetnja.", "answer": "Moj hobi je šetnja."},
            {"id": "pr6", "prompt": "Write the Bosnian word for team.", "hint": "Three letters.", "answer": "tim"},
            {"id": "pr7", "prompt": "Write I love football. in Bosnian.", "hint": "Use Volim.", "answer": "Volim fudbal."},
        ],
        facts=facts,
        resources=[
            {"label": "Beba Selimović - Bosno moja", "url": "https://www.youtube.com/watch?v=OXul62dILOo", "note": "A warm Bosnia song for weekend leisure listening."},
            {"label": "Next lesson", "url": "/learn/lesson/19", "note": "Lesson 19 practices inclusive holiday greetings."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Keep browsing speaker models after practice."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Youth leave, weekend ties remain",
            "body": civic_body,
            "imageId": "civic-emigration-airport",
            "learnMore": {
                "label": "Wikipedia article about demographics of Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Demographics_of_Bosnia_and_Herzegovina",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with a weekend leisure song",
            kind="song",
            hook="A classic love-of-Bosnia song stretches the ear for leisure and belonging after sports talk.",
            source_title="Beba Selimović - Bosno moja, divna, mila",
            artist="Beba Selimović",
            scene="Weekend leisure and belonging",
            credit="Beba Selimović performance on YouTube",
            url="https://www.youtube.com/watch?v=OXul62dILOo",
            prompt="Listen for Bosna or warm chorus energy rather than every lyric.",
            gist_prompt="What kind of clip is this?",
            gist_options=["A traditional song about Bosnia", "A ticket-machine tutorial", "A silent spreadsheet", "Only stadium whistle sounds"],
            gist_index=0,
            target_words=["Bosna", "volim"],
            notice="Leisure listening can be emotional. Catch mood plus any familiar word.",
            key_lines=[
                {"bosnian": "Bosno moja…", "english": "My Bosnia…"},
                {"bosnian": "Volim fudbal.", "english": "I love football."},
            ],
            teacher_note="After the song, say one sport habit and one walk habit.",
        ),
        speak_targets=[0, 3, 5],
        section=3,
        say_again=say_again(
            [
                ("Hoću klepe, molim.", "I want klepe, please."),
                ("Dobar tek!", "Enjoy your meal!"),
                ("Hajde da idemo.", "Let us go."),
                ("Volim burek.", "I love burek."),
            ]
        ),
    )


def build_lesson_19(images: list) -> dict:
    v = [
        vocab("praznik", "holiday", "PRAZ-neek", "noun", "Danas je praznik."),
        vocab("Bajram", "Eid", "BAI-ram", "noun", "Sretan Bajram!"),
        vocab("Božić", "Christmas", "BO-zheech", "noun", "Sretan Božić!"),
        vocab("Nova godina", "New Year", "NO-va go-DEE-na", "noun phrase", "Sretna Nova godina!"),
        vocab("sretan", "happy (m.)", "SREH-tan", "adjective", "Sretan praznik!"),
        vocab("sretna", "happy (f.)", "SREH-tna", "adjective", "Sretna Nova godina!"),
        vocab("čestitka", "greeting card", "ches-TEET-ka", "noun", "Imam čestitku."),
        vocab("svijeća", "candle", "SVYE-cha", "noun", "Svijeća gori."),
        vocab("svjetla", "lights", "SVYET-la", "noun", "Svjetla su lijepa."),
        vocab("tržnica", "market", "TRZH-nee-tsa", "noun", "Idemo na tržnicu."),
        vocab("dar", "gift", "dar", "noun", "Ovo je mali dar."),
        vocab("porodica", "family", "po-RO-dee-tsa", "noun", "Porodica se okuplja."),
        vocab("zajedno", "together", "za-YED-no", "adverb", "Slavimo zajedno."),
        vocab("čestitam", "I congratulate / I greet", "ches-TEE-tam", "verb form", "Čestitam Bajram!"),
    ]
    grammar = [
        {
            "title": "Sretan and sretna greetings",
            "explanation": "Build this as a ready-made line you can reuse. Sretan pairs with masculine holiday names such as Bajram and Božić. Sretna pairs with feminine phrases such as Nova godina. Learn each full greeting as one chunk.",
            "examples": [
                {"bosnian": "Sretan Bajram!", "english": "Happy Eid!"},
                {"bosnian": "Sretan Božić!", "english": "Merry Christmas!"},
                {"bosnian": "Sretna Nova godina!", "english": "Happy New Year!"},
            ],
        },
        {
            "title": "Čestitam plus the holiday",
            "explanation": "Store this as a phrase you can pull out in conversation. Čestitam plus the holiday name is a warm congratulation. Keep the present form and smile with your voice. The chunk works across different communities.",
            "examples": [
                {"bosnian": "Čestitam Bajram!", "english": "Eid greetings!"},
                {"bosnian": "Čestitam Božić!", "english": "Christmas greetings!"},
                {"bosnian": "Čestitam Novu godinu!", "english": "New Year greetings!"},
            ],
        },
        {
            "title": "Inclusive holiday talk",
            "explanation": "Focus on the spoken chunk; postpone the full paradigm. Name more than one holiday so your greetings stay inclusive. Add zajedno when people celebrate side by side on the same street. Present-tense wishes are enough for market conversations.",
            "examples": [
                {"bosnian": "Sretan praznik!", "english": "Happy holiday!"},
                {"bosnian": "Slavimo zajedno.", "english": "We celebrate together."},
                {"bosnian": "Svjetla su lijepa.", "english": "The lights are beautiful."},
            ],
        },
    ]
    culture_body = (
        "Holiday lights on Ferhadija turn central Sarajevo into a shared evening walk for many neighbors. "
        "Nearby, Gazi Husrev-beg's Mosque and the Sacred Heart Cathedral stand as reminders that communities mark the calendar in different ways. "
        "Ana practices Sretan Bajram, Sretan Božić, and Sretna Nova godina without ranking the days. "
        "A market stall sells čestitke while svjetla glitter above the crowd and music spills from cafés. "
        "Inclusive greetings keep friendship open through the season and make the street feel wider. "
        "One polite wish can travel farther than a perfect grammar explanation. "
    )
    assert 80 <= len(culture_body.split()) <= 120, len(culture_body.split())
    block_a = (
        "Learn the three core wishes first: Sretan Bajram, Sretan Božić, and Sretna Nova godina. "
        "Notice sretan versus sretna and keep each greeting whole as one spoken chunk. "
        "Add Čestitam Bajram as a second warm pattern you can hand to family or friends. "
        "Ana repeats the greetings while Emir points to mosque and cathedral photos on the same city map. "
        "The goal is respectful fluency in public, not a theology lecture or a comparison chart. "
        "Say each wish twice, then switch which holiday you greet so your mouth stays flexible. "
        "Keep the tone warm and the chunks complete. "
        "Say the lines out loud twice before you move on. "
    )
    block_b = (
        "Take the greetings into a market scene with svjetla, dar, and čestitka in your pocket vocabulary. "
        "Say Molim and Hvala at the stall, then wish the seller a holiday that fits the moment. "
        "Amira likes Nova godina lights; Emir talks about Bajram visits; Ana sends a Božić card to family abroad. "
        "Practice switching greetings so you can answer whoever you meet on Ferhadija after dark. "
        "End with Slavimo zajedno as a friendly present-tense line that leaves room for difference. "
        "A card plus a spoken wish is enough to make the season feel shared without forcing one calendar. "
        "Practice one card message before you leave the stall. "
    )
    assert 100 <= len(block_a.split()) <= 180, len(block_a.split())
    assert 100 <= len(block_b.split()) <= 180, len(block_b.split())
    civic_body = (
        "Sarajevo's religious architecture makes pluralism visible in daily walking distance through the historic center. "
        "Mosques and churches share nearby streets, so holiday seasons often overlap in lights, markets, and public greetings. "
        "That closeness can be beautiful and also politically sensitive after conflict, which is why careful words matter. "
        "Learners who offer inclusive greetings practice a civic skill by recognizing neighbors without erasing difference. "
        "Shared streets work best when language leaves room for more than one celebration on the same winter night. "
    )
    facts = [
        {
            "title": "Ferhadija is a holiday promenade",
            "body": "Ferhadija Street fills with evening walkers when lights go up for winter seasons. Shops, cafés, and market energy make greetings useful in motion. The pedestrian flow is part of the city's social weather. Practicing wishes here feels natural rather than staged.",
        },
        {
            "title": "Two landmarks, one center",
            "body": "Gazi Husrev-beg's Mosque and the Sacred Heart Cathedral stand in the wider downtown story of Sarajevo. Their nearness teaches that holidays are plural in public life. Photos of both places help learners avoid a single-community frame. Respect starts with accurate naming.",
        },
        {
            "title": "Čestitka carries a written wish",
            "body": "A čestitka is a greeting card you can hand over with a spoken line. Writing Sretan Bajram or Sretan Božić reinforces the chunk. Small gifts and cards keep contact warm across distance. The object makes the phrase memorable.",
        },
    ]
    quiz = [
        quiz_question("q1", "Which greeting matches Eid?", ["Sretan Bajram!", "Sretan Božić!", "Sretna Nova godina!", "Račun, molim."], 0, "Sretan Bajram greets Eid.", "vocabulary"),
        quiz_question("q2", "Which form fits Nova godina?", ["sretan", "sretna", "često", "tim"], 1, "Sretna pairs with Nova godina.", "grammar"),
        quiz_question("q3", "What does čestitka mean?", ["Candle", "Greeting card", "Stadium", "Ticket"], 1, "Čestitka means greeting card.", "vocabulary"),
        quiz_question("q4", "Which street hosts the holiday walk in this lesson?", ["Ferhadija", "Only a highway shoulder", "Only an airport runway", "Only a ski slope"], 0, "Ferhadija hosts the holiday walk.", "culture"),
        quiz_question("q5", "Why does the lesson teach more than one greeting?", ["To keep holiday talk inclusive", "To erase all holidays", "To avoid markets", "To replace family names"], 0, "Multiple greetings keep talk inclusive.", "dialogue"),
        quiz_question("q6", "Which sentence means We celebrate together?", ["Slavimo zajedno.", "Treba mi karta.", "Igram fudbal.", "Hoću klepe."], 0, "Slavimo zajedno means we celebrate together.", "grammar"),
        quiz_question("q7", "Which landmark is a cathedral in the lesson images?", ["Sacred Heart Cathedral", "Bilino Polje", "Neum beach", "Jablanica lake only"], 0, "Sacred Heart Cathedral appears among the images.", "culture"),
        quiz_question("q8", "What does svjetla mean?", ["Lights", "Gifts", "Buses", "Menus"], 0, "Svjetla means lights.", "vocabulary"),
        quiz_question("q9", "Which civic idea fits the mosque and cathedral pairing?", ["Plural communities share public space", "Only one faith may use streets", "Holidays are illegal", "Markets ban greetings"], 0, "Plural communities sharing space is the civic thread.", "culture"),
        quiz_question("q10", "Which line is a New Year wish?", ["Sretna Nova godina!", "Sretan Bajram!", "Jednosmjerna karta.", "Ko je tamo?"], 0, "Sretna Nova godina is the New Year wish.", "listening"),
    ]
    return chapter(
        day=19,
        title="Praznici",
        title_en="Holidays",
        theme="Holiday lights and inclusive greetings",
        story="Ana practices Bajram, Božić, and New Year greetings under Ferhadija lights.",
        goals={
            "vocabulary": [
                "Offer Bajram, Božić, and New Year greetings.",
                "Name lights, candles, markets, gifts, and cards.",
                "Use family and together words in holiday talk.",
            ],
            "grammar": [
                "Match sretan and sretna to the holiday phrase.",
                "Use Čestitam plus a holiday name.",
                "Keep inclusive present-tense wishes ready.",
            ],
            "culture": [
                "Walk Ferhadija during lighted holiday evenings.",
                "Recognize mosque and cathedral landmarks in one city center.",
                "Understand pluralism as a civic skill in greeting choices.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Lights, markets, and shared greetings",
            "body": culture_body,
            "imageId": "ferhadija-lights",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Three holiday wishes",
                "body": block_a,
                "tips": [
                    "Memorize each full greeting as one chunk.",
                    "Watch sretan versus sretna before you speak.",
                    "Practice all three so you can answer different neighbors.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Market politeness and cards",
                "body": block_b,
                "tips": [
                    "Use molim and hvala at the market stall.",
                    "Hand over a čestitka with a spoken wish.",
                    "Say Slavimo zajedno when the mood is shared.",
                ],
            },
        ],
        conversation={
            "title": "Svjetla na Ferhadiji",
            "setting": "Ana, Emir, and Amira walk Ferhadija under holiday lights near market stalls.",
            "lines": [
                {"speaker": "Amira", "bosnian": "Svjetla su lijepa večeras!", "english": "The lights are beautiful this evening!"},
                {"speaker": "Ana", "bosnian": "Sretna Nova godina unaprijed!", "english": "Happy New Year in advance!"},
                {"speaker": "Emir", "bosnian": "Sretan Bajram porodici, molim vas.", "english": "Happy Eid to the family, please."},
                {"speaker": "Seller", "bosnian": "Hvala! Želite čestitku?", "english": "Thank you! Would you like a greeting card?"},
                {"speaker": "Ana", "bosnian": "Da, molim. Sretan Božić pišem majci.", "english": "Yes, please. I am writing Merry Christmas to my mother."},
                {"speaker": "Amira", "bosnian": "Slavimo zajedno u gradu.", "english": "We celebrate together in the city."},
                {"speaker": "Emir", "bosnian": "Evo malog dara. Hvala vam!", "english": "Here is a small gift. Thank you!"},
                {"speaker": "Narrator", "bosnian": "Mrvica gleda svijeću i mirne korake.", "english": "Mrvica watches a candle and the calm steps."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match holiday greetings",
                "prompt": "Match each Bosnian greeting with its English meaning.",
                "items": [
                    {"left": "Sretan Bajram!", "right": "Happy Eid!"},
                    {"left": "Sretan Božić!", "right": "Merry Christmas!"},
                    {"left": "Sretna Nova godina!", "right": "Happy New Year!"},
                    {"left": "čestitka", "right": "greeting card"},
                    {"left": "svjetla", "right": "lights"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about holidays",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Sretna Nova godina uses the feminine form sretna.", "answer": True},
                    {"statement": "The lesson teaches only one community greeting.", "answer": False},
                    {"statement": "Ferhadija can host lighted evening walks.", "answer": True},
                    {"statement": "Čestitam Bajram is a warm greeting chunk.", "answer": True},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write Happy Eid! in Bosnian.", "hint": "Use Sretan.", "answer": "Sretan Bajram!"},
            {"id": "pr2", "prompt": "Write Merry Christmas! in Bosnian.", "hint": "Use Božić.", "answer": "Sretan Božić!"},
            {"id": "pr3", "prompt": "Write Happy New Year! in Bosnian.", "hint": "Use Sretna.", "answer": "Sretna Nova godina!"},
            {"id": "pr4", "prompt": "Write We celebrate together. in Bosnian.", "hint": "Use zajedno.", "answer": "Slavimo zajedno."},
            {"id": "pr5", "prompt": "Write The lights are beautiful. in Bosnian.", "hint": "Use svjetla.", "answer": "Svjetla su lijepa."},
            {"id": "pr6", "prompt": "Write the Bosnian word for greeting card.", "hint": "It begins with čest.", "answer": "čestitka"},
            {"id": "pr7", "prompt": "Write Eid greetings! with Čestitam.", "hint": "Begin with Čestitam.", "answer": "Čestitam Bajram!"},
        ],
        facts=facts,
        resources=[
            {"label": "Tebi majko misli lete", "url": "https://www.youtube.com/watch?v=QkvCVZqRYFY", "note": "A warm family song fits holiday feeling and čestitke."},
            {"label": "Next lesson", "url": "/learn/lesson/20", "note": "Lesson 20 practices phone phrases when Mrvica goes missing."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Continue with speaker models after the market scene."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Plural streets need plural greetings",
            "body": civic_body,
            "imageId": "civic-pluralism",
            "learnMore": {
                "label": "Wikipedia article about Sacred Heart Cathedral, Sarajevo",
                "url": "https://en.wikipedia.org/wiki/Sacred_Heart_Cathedral,_Sarajevo",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with a warm family song",
            kind="song",
            hook="Holiday cards often travel toward family. Listen for warm majka feeling in a song voice outside the cast.",
            source_title="Tebi majko misli lete - Sementa Rajhard",
            artist="Sementa Rajhard",
            scene="Family warmth for holiday cards",
            credit="Sementa Rajhard performance on YouTube",
            url="https://www.youtube.com/watch?v=QkvCVZqRYFY",
            prompt="Listen for majka or a warm family-directed tone.",
            gist_prompt="What fits the clip's mood?",
            gist_options=["Warm song aimed at mother or family feeling", "Only bus engine noise", "A cooking timer only", "Silent chess analysis"],
            gist_index=0,
            target_words=["majka", "porodica"],
            notice="You can miss full lyrics and still catch the family warmth.",
            key_lines=[
                {"bosnian": "Majko…", "english": "Mother…"},
                {"bosnian": "Sretan praznik!", "english": "Happy holiday!"},
            ],
            teacher_note="After the song, say one greeting you would write on a čestitka.",
        ),
        speak_targets=[1, 2, 4],
        section=3,
        say_again=say_again(
            [
                ("Često igram fudbal.", "I often play football."),
                ("Moj hobi je šetnja.", "My hobby is walking."),
                ("Dobar tek!", "Enjoy your meal!"),
                ("Hvala!", "Thank you!"),
            ]
        ),
    )


def build_lesson_20(images: list) -> dict:
    v = [
        vocab("telefon", "telephone", "teh-leh-FON", "noun", "Gdje je telefon?"),
        vocab("poziv", "call", "PO-zeev", "noun", "Imam važan poziv."),
        vocab("alo", "hello (on phone)", "AH-lo", "interjection", "Alo?"),
        vocab("ko", "who", "ko", "question word", "Ko je tamo?"),
        vocab("šta", "what", "shta", "question word", "Šta se desi?"),
        vocab("kada", "when", "KA-da", "question word", "Kada dolaziš?"),
        vocab("zašto", "why", "ZA-shto", "question word", "Zašto zoveš?"),
        vocab("broj", "number", "broi", "noun", "Koji je broj?"),
        vocab("javiti se", "to answer or get in touch", "YA-vee-tee se", "verb phrase", "Javi se uskoro."),
        vocab("čujem", "I hear", "CHOO-yem", "verb form", "Čujem te dobro."),
        vocab("hitno", "urgent", "HEEL-no", "adverb", "Hitno je!"),
        vocab("nestala", "missing (f.)", "neh-STA-la", "adjective", "Mrvica je nestala!"),
        vocab("tramvaj", "tram", "TRAM-vai", "noun", "Tramvaj ide kroz grad."),
        vocab("veza", "connection", "VEH-za", "noun", "Imamo dobru vezu."),
    ]
    grammar = [
        {
            "title": "Phone openers: Alo and Ko je tamo?",
            "explanation": "Learn this as a phrase, not a table. Start a call with Alo? then ask Ko je tamo? when you need the name. Keep both chunks short and clear. Present-tense phone talk is enough for an urgent cat emergency.",
            "examples": [
                {"bosnian": "Alo?", "english": "Hello?"},
                {"bosnian": "Ko je tamo?", "english": "Who is there?"},
                {"bosnian": "Ja sam Ana.", "english": "I am Ana."},
            ],
        },
        {
            "title": "Šta, kada, and zašto",
            "explanation": "Hold this as a spoken pattern, not a grammar grid. Use šta for what, kada for when, and zašto for why. Pair each question word with a present verb you already know. The set helps you gather facts fast on a call.",
            "examples": [
                {"bosnian": "Šta se desi?", "english": "What is happening?"},
                {"bosnian": "Kada dolaziš?", "english": "When are you coming?"},
                {"bosnian": "Zašto zoveš?", "english": "Why are you calling?"},
            ],
        },
        {
            "title": "Urgent present chunks",
            "explanation": "Say the whole line together; skip the full chart for now. Hitno je! flags urgency. Nestala describes a feminine missing subject such as Mrvica. Add Molim vas when you ask a stranger for help by phone or on the street.",
            "examples": [
                {"bosnian": "Hitno je!", "english": "It is urgent!"},
                {"bosnian": "Mrvica je nestala!", "english": "Mrvica is missing!"},
                {"bosnian": "Pomozite, molim vas!", "english": "Help, please!"},
            ],
        },
    ]
    culture_body = (
        "Sarajevo trams slide past cafés where people still step outside to finish a call in clearer air. "
        "Ana phones Emir when Mrvica disappears near the tracks, and every question word suddenly matters. "
        "Ko, šta, kada, and zašto turn panic into a usable checklist she can repeat under stress. "
        "Mobile connection is ordinary now, yet the voice on the line still carries care across a noisy street. "
        "A clear Alo? "
        "can start both small talks and true emergencies before anyone explains the problem. "
        "Phone survival phrases belong beside tram noise, not only beside a quiet classroom desk. "
    )
    assert 80 <= len(culture_body.split()) <= 120, len(culture_body.split())
    block_a = (
        "Lock the phone kit: telefon, poziv, alo, broj, and veza before the emergency story begins. "
        "Practice Alo? "
        "and Ko je tamo? "
        "until both openers sound natural on the first try. "
        "Then drill šta, kada, and zašto with short present answers so facts arrive in order. "
        "Ana calls from near a tram stop while Emir asks for details without wasting time. "
        "Keep the lines sharp; a missing cat does not wait for a full grammar chart. "
        "Record yourself asking all four question words, then answer each one in one calm present sentence. "
        "Keep the checklist order steady under pressure. "
        "Say the lines out loud twice before you move on. "
    )
    block_b = (
        "Build the emergency call as a sequence you can run even when you feel rushed. "
        "Say Hitno je! "
        "then Mrvica je nestala! "
        "then ask for help with molim vas in a clear voice. "
        "Reuse Čujem te dobro when the connection is clear and you need to slow the other person down. "
        "Amira joins the search on another line, and the tram keeps moving beside the café windows. "
        "Close the call with a plan in the present: Idemo sad. "
        "Practice until the question words feel like a calm checklist rather than a scramble of panic. "
        "Repeat the full call once without looking at notes. "
    )
    assert 100 <= len(block_a.split()) <= 180, len(block_a.split())
    assert 100 <= len(block_b.split()) <= 180, len(block_b.split())
    civic_body = (
        "Families spread across countries stay connected through calls, messages, and remittances sent home. "
        "A phone line can carry birthday wishes, job news, and urgent help requests in the same afternoon. "
        "For many households in Bosnia and Herzegovina, diaspora contact is part of weekly life rather than a rare event. "
        "Mobile networks make that contact faster, yet cost and distance still shape who can talk and how often. "
        "Lesson 20 treats the phone as both a language tool and a civic lifeline."
    )
    facts = [
        {
            "title": "Alo is the phone hello",
            "body": "Bosnian phone calls often open with Alo? rather than a street greeting. The short sound checks the line and invites the other person to speak. Learners should keep it separate from Zdravo. The channel of speech changes the first word.",
        },
        {
            "title": "Trams frame everyday calls",
            "body": "Sarajevo trams run through central corridors where people move between errands and cafés. Taking a call beside the tracks is a normal city picture. The tram image keeps the emergency story local and mobile. Noise on the line becomes part of the listening task.",
        },
        {
            "title": "Question words form a checklist",
            "body": "Ko, šta, kada, and zašto help a panicked speaker slow down. Each word requests one kind of fact. Used together, they organize an urgent conversation. Book 1 teaches them as present-tense tools, not as abstract grammar labels.",
        },
        {
            "title": "Mrvica keeps stakes personal",
            "body": "A missing cat is a comic emergency with real feeling. The cast cares, so learners care enough to repeat the lines. Personal stakes make phone phrases stick. Humor and urgency can share the same call.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does Alo? mean on the phone?", ["Hello?", "Ticket please", "Enjoy your meal", "Turn left"], 0, "Alo? is the phone hello.", "vocabulary"),
        quiz_question("q2", "Which word asks who?", ["šta", "kada", "ko", "zašto"], 2, "Ko asks who.", "grammar"),
        quiz_question("q3", "Which word asks why?", ["zašto", "tramvaj", "broj", "veza"], 0, "Zašto asks why.", "vocabulary"),
        quiz_question("q4", "What happened to Mrvica?", ["She is missing.", "She bought tickets.", "She cooked japrak.", "She scored a goal."], 0, "Mrvica is missing in the story.", "dialogue"),
        quiz_question("q5", "Which sentence flags urgency?", ["Hitno je!", "Sretan Bajram!", "Ponekad gledam.", "Povratna karta."], 0, "Hitno je! flags urgency.", "grammar"),
        quiz_question("q6", "What does čujem mean?", ["I hear", "I play", "I order", "I depart"], 0, "Čujem means I hear.", "vocabulary"),
        quiz_question("q7", "Which city vehicle appears in the culture scene?", ["Tram", "Submarine", "Helicopter taxi only", "Cable ferry only"], 0, "The tram appears in the Sarajevo phone scene.", "culture"),
        quiz_question("q8", "Why do phones matter for diaspora families?", ["They help people stay connected across countries.", "They replace all roads.", "They ban remittances.", "They end holidays."], 0, "Phones help diaspora families stay connected.", "culture"),
        quiz_question("q9", "Which polite ask fits an urgent stranger call?", ["Pomozite, molim vas!", "Dobar tek japrak.", "Često igram.", "Jednosmjerna karta."], 0, "Pomozite, molim vas! is a polite urgent ask.", "listening"),
    ]
    return chapter(
        day=20,
        title="Telefonski poziv",
        title_en="Phone call",
        theme="Emergency cat phone call",
        story="Ana calls Emir in a panic when Mrvica goes missing near the tram line.",
        goals={
            "vocabulary": [
                "Open and continue a phone call with alo, broj, and veza.",
                "Use ko, šta, kada, and zašto to gather facts.",
                "Describe an urgent missing-pet problem.",
            ],
            "grammar": [
                "Use Alo? and Ko je tamo? as phone openers.",
                "Ask šta, kada, and zašto in the present.",
                "Signal urgency with Hitno je! and polite help requests.",
            ],
            "culture": [
                "Place phone talk beside Sarajevo tram streets.",
                "Treat clear connection as part of city life.",
                "Link phone habits to diaspora care and remittance ties.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Calls beside the tram",
            "body": culture_body,
            "imageId": "sarajevo-tram",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Phone questions that gather facts",
                "body": block_a,
                "tips": [
                    "Start with Alo? before you ask anything else.",
                    "Use one question word at a time.",
                    "Answer with a short present-tense sentence.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: The Mrvica emergency call",
                "body": block_b,
                "tips": [
                    "Say Hitno je! early if the problem is urgent.",
                    "Add molim vas when you ask for help.",
                    "Confirm the connection with Čujem te dobro.",
                ],
            },
        ],
        conversation={
            "title": "Gdje je Mrvica?",
            "setting": "Ana calls Emir from a café near a Sarajevo tram stop after Mrvica disappears.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Alo? Emire, hitno je!", "english": "Hello? Emir, it is urgent!"},
                {"speaker": "Emir", "bosnian": "Alo, Ana! Ko je s tobom?", "english": "Hello, Ana! Who is with you?"},
                {"speaker": "Ana", "bosnian": "Mrvica je nestala! Šta radim?", "english": "Mrvica is missing! What do I do?"},
                {"speaker": "Emir", "bosnian": "Gdje je sada? Jesi li kod tramvaja?", "english": "Where is she now? Are you by the tram?"},
                {"speaker": "Ana", "bosnian": "Sad, kod tramvaja. Zašto trči tako brzo?", "english": "Now, by the tram. Why does she run so fast?"},
                {"speaker": "Emir", "bosnian": "Čujem te dobro. Idemo sad, molim te, čekaj!", "english": "I hear you well. We are going now, please wait!"},
                {"speaker": "Amira", "bosnian": "Ja zovem komšije. Pomozite, molim vas!", "english": "I am calling the neighbors. Help, please!"},
                {"speaker": "Narrator", "bosnian": "Mrvica sjedi iza kantice i mirno trepće.", "english": "Mrvica sits behind a bin and blinks calmly."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match phone words",
                "prompt": "Match each Bosnian phone word with its English meaning.",
                "items": [
                    {"left": "alo", "right": "hello (on phone)"},
                    {"left": "ko", "right": "who"},
                    {"left": "šta", "right": "what"},
                    {"left": "kada", "right": "when"},
                    {"left": "zašto", "right": "why"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false on the call",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Alo? is a common phone opener.", "answer": True},
                    {"statement": "Zašto means when.", "answer": False},
                    {"statement": "Mrvica is missing in the dialogue.", "answer": True},
                    {"statement": "Hitno je! signals urgency.", "answer": True},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian phone hello.", "hint": "One short word with a question mark.", "answer": "Alo?"},
            {"id": "pr2", "prompt": "Write Who is there? in Bosnian.", "hint": "Begin with Ko.", "answer": "Ko je tamo?"},
            {"id": "pr3", "prompt": "Write Why are you calling? in Bosnian.", "hint": "Begin with Zašto.", "answer": "Zašto zoveš?"},
            {"id": "pr4", "prompt": "Write It is urgent! in Bosnian.", "hint": "Use hitno.", "answer": "Hitno je!"},
            {"id": "pr5", "prompt": "Write Mrvica is missing! in Bosnian.", "hint": "Use nestala.", "answer": "Mrvica je nestala!"},
            {"id": "pr6", "prompt": "Write I hear you well. in Bosnian.", "hint": "Begin with Čujem.", "answer": "Čujem te dobro."},
            {"id": "pr7", "prompt": "Write Help, please! in Bosnian (polite).", "hint": "Use molim vas.", "answer": "Pomozite, molim vas!"},
            {"id": "pr8", "prompt": "Write the Bosnian word for tram.", "hint": "It begins with tram.", "answer": "tramvaj"},
        ],
        facts=facts,
        resources=[
            {"label": "Bosnian Grammar: How to Say I am", "url": "https://www.youtube.com/watch?v=CUUGzc3C1G8", "note": "Self-introduction chunks help you answer Ko je tamo?"},
            {"label": "Next lesson", "url": "/learn/lesson/21", "note": "Lesson 21 reviews frames from Lessons 15 to 20."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Keep a speaker playlist ready after the phone emergency."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Calls that hold families together",
            "body": civic_body,
            "imageId": "civic-diaspora-calls",
            "learnMore": {
                "label": "Wikipedia article about remittance",
                "url": "https://en.wikipedia.org/wiki/Remittance",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with introduction chunks for callers",
            kind="speaker",
            hook="A teacher models Ja sam lines you can reuse when someone asks who is calling.",
            source_title="Bosnian Grammar: How to Say 'I am' (Ja sam) - Introducing Yourself",
            artist="Lingo Hero",
            scene="Self-introduction for phone identity",
            credit="Lingo Hero on YouTube",
            url="https://www.youtube.com/watch?v=CUUGzc3C1G8",
            prompt="Listen for Ja sam and name yourself as if you are answering a call.",
            gist_prompt="What is the speaker teaching?",
            gist_options=["How to say I am and introduce yourself", "How to buy bus tickets only", "How to ski Jahorina only", "How to bake only hljeb"],
            gist_index=0,
            target_words=["ja", "sam"],
            notice="On a phone call, Ja sam plus your name answers Ko je tamo?",
            key_lines=[
                {"bosnian": "Ja sam Ana.", "english": "I am Ana."},
                {"bosnian": "Ko je tamo?", "english": "Who is there?"},
            ],
            teacher_note="After the clip, rehearse Alo? then Ja sam… then your urgent line.",
        ),
        speak_targets=[0, 2, 5],
        section=3,
        say_again=say_again(
            [
                ("Sretan Bajram!", "Happy Eid!"),
                ("Sretan Božić!", "Merry Christmas!"),
                ("Molim vas.", "Please."),
                ("Gdje je Mostar?", "Where is Mostar?"),
            ]
        ),
    )


VIDEO_16 = """
# Lesson 16 video script for Na autobus
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 16: On the bus
- BS: Na autobus
- Background: Coaches wait at the Sarajevo bus station.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 16 is Na autobus. Ana and Emir buy tickets and dream of lake water near Jablanica and the coast at Neum.
**On screen:** Na autobus | Lesson 16

### 0:40 Goals
**Narration:** You learn ticket words, Treba mi chunks, and price questions so you can board with confidence.
**On screen:** karta | Treba mi | Koliko košta?

### 1:30 Culture hook
**Narration:** The Sarajevo bus station starts the journey. A postcard of Jablaničko Lake appears on the road south, and Neum waits as the short Adriatic dream.
**On screen:** Sarajevo station | Jablanica | Neum | image credits

### 3:00 Lesson A: Ticket counter phrases
**Narration:** Say Treba mi karta. Ask Koliko košta karta? Choose jednosmjerna or povratna, then add molim.
**On screen:** Treba mi karta. | Povratna karta, molim.

### 5:00 Lesson B: Board and claim a seat
**Narration:** Read odlazak and dolazak on the board. Claim Imam sjedalo uz prozor, thank the clerk, and keep the coast dream in the present.
**On screen:** odlazak | dolazak | sjedalo uz prozor

### 6:30 Mini dialogue
**Narration:** Ana buys a return ticket with Emir and checks the window seat before boarding.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and buy an imaginary ticket aloud. Continue with Lesson 17, Dobar tek!
**On screen:** Buy a ticket | Next lesson is Dobar tek!

## End screen
- Link to website `/learn/lesson/16`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_17 = """
# Lesson 17 video script for Dobar tek!
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 17: Enjoy your meal!
- BS: Dobar tek!
- Background: A Sarajevo restaurant table with klepe and japrak.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 17 is Dobar tek! Ana wants klepe. Emir wants japrak. The debate becomes your restaurant practice.
**On screen:** Dobar tek! | Lesson 17

### 0:40 Goals
**Narration:** You learn hoću, hoćeš, and hoćemo as present wanting chunks, then order politely and ask for the bill.
**On screen:** hoću | hoćeš | račun, molim

### 1:30 Culture hook
**Narration:** Sarajevo kitchens argue kindly about favorite trays. A Visoko postcard widens the food map beyond one street.
**On screen:** klepe | japrak | Visoko | image credits

### 3:00 Lesson A: Wanting food with htjeti chunks
**Narration:** Say Hoću klepe. Ask Hoćeš li japrak? Keep htjeti in the present and skip the full chart.
**On screen:** Hoću klepe. | Hoćeš li japrak?

### 5:00 Lesson B: From order to račun
**Narration:** Add molim to every order. Wish Dobar tek when the plates arrive, then finish with Račun, molim.
**On screen:** Dobar tek! | Račun, molim.

### 6:30 Mini dialogue
**Narration:** The waiter takes both orders while Mrvica waits for crumbs under the table.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and order your dish with hoću and molim. Continue with Lesson 18, Sport i hobiji.
**On screen:** Place an order | Next lesson is Sport i hobiji

## End screen
- Link to website `/learn/lesson/17`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_18 = """
# Lesson 18 video script for Sport i hobiji
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 18: Sports and hobbies
- BS: Sport i hobiji
- Background: Bilino Polje stadium opens wide in Zenica.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 18 is Sport i hobiji. Football at Bilino Polje meets a quiet Una River walk on a postcard.
**On screen:** Sport i hobiji | Lesson 18

### 0:40 Goals
**Narration:** You learn igram and gledam, then add često and ponekad to tell the truth about your habits.
**On screen:** igram | gledam | često | ponekad

### 1:30 Culture hook
**Narration:** Zenica's stadium gives the match a loud home. Štrbački buk on the Una gives the weekend a second mood.
**On screen:** Bilino Polje | Una | Štrbački buk | image credits

### 3:00 Lesson A: Play, watch, and how often
**Narration:** Say Igram fudbal and Gledam utakmicu. Place često or ponekad before the verb.
**On screen:** Često igram fudbal. | Ponekad gledam utakmicu.

### 5:00 Lesson B: From stands to river path
**Narration:** Balance the stadium with Moj hobi je šetnja. Ask a friend about the match, then claim a walk.
**On screen:** Moj hobi je šetnja. | Hoćeš li gledati utakmicu?

### 6:30 Mini dialogue
**Narration:** Ana, Emir, and Amira compare the match and the waterfall walk while Mrvica chooses smells over scores.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and say one sport habit and one nature habit. Continue with Lesson 19, Praznici.
**On screen:** Name two hobbies | Next lesson is Praznici

## End screen
- Link to website `/learn/lesson/18`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_19 = """
# Lesson 19 video script for Praznici
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 19: Holidays
- BS: Praznici
- Background: Holiday lights glitter along Ferhadija in Sarajevo.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 19 is Praznici. Ana practices inclusive greetings under market lights on Ferhadija.
**On screen:** Praznici | Lesson 19

### 0:40 Goals
**Narration:** You learn Sretan Bajram, Sretan Božić, and Sretna Nova godina, then use čestitka and dar at a stall.
**On screen:** Sretan Bajram! | Sretan Božić! | Sretna Nova godina!

### 1:30 Culture hook
**Narration:** Mosque and cathedral landmarks remind you that many communities share the same city center. Inclusive greetings keep friendship open.
**On screen:** Ferhadija | mosque | cathedral | image credits

### 3:00 Lesson A: Three holiday wishes
**Narration:** Match sretan and sretna to the holiday name. Add Čestitam Bajram as a second warm chunk.
**On screen:** sretan | sretna | Čestitam Bajram!

### 5:00 Lesson B: Market politeness and cards
**Narration:** Buy a čestitka with molim, wish the seller well, and say Slavimo zajedno when the street feels shared.
**On screen:** čestitka | molim | Slavimo zajedno.

### 6:30 Mini dialogue
**Narration:** Ana, Emir, and Amira exchange Bajram, Božić, and New Year lines at a lighted stall.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and say all three greetings aloud. Continue with Lesson 20, Telefonski poziv.
**On screen:** Three greetings | Next lesson is Telefonski poziv

## End screen
- Link to website `/learn/lesson/19`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_20 = """
# Lesson 20 video script for Telefonski poziv
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 20: Phone call
- BS: Telefonski poziv
- Background: A Sarajevo tram passes while Ana makes an urgent call.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 20 is Telefonski poziv. Mrvica is missing, and Ana needs every phone question she can remember.
**On screen:** Telefonski poziv | Lesson 20

### 0:40 Goals
**Narration:** You learn Alo?, Ko je tamo?, and the question set šta, kada, and zašto for a clear urgent call.
**On screen:** Alo? | ko | šta | kada | zašto

### 1:30 Culture hook
**Narration:** Trams and cafés frame everyday mobile talk in Sarajevo. A good connection can carry both jokes and true emergencies.
**On screen:** tramvaj | telefon | image credits

### 3:00 Lesson A: Phone questions that gather facts
**Narration:** Open with Alo? Ask Ko je tamo? Then gather facts with šta, kada, and zašto in the present.
**On screen:** Alo? | Ko je tamo? | Zašto zoveš?

### 5:00 Lesson B: The Mrvica emergency call
**Narration:** Say Hitno je! and Mrvica je nestala! Ask for help with molim vas, then confirm Čujem te dobro.
**On screen:** Hitno je! | Mrvica je nestala! | Pomozite, molim vas!

### 6:30 Mini dialogue
**Narration:** Ana calls Emir by the tram. Amira phones the neighbors. Mrvica is already behind a bin.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and rehearse a thirty-second urgent call. Continue with Lesson 21 for review.
**On screen:** Make the call | Next lesson is Ponavljanje

## End screen
- Link to website `/learn/lesson/20`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


def validate(lessons: list[dict], videos: dict[int, str]) -> int:
    """Print prohibited learner strings and return the number of issues."""
    issues: list[tuple[str, str]] = []

    def walk(value, path):
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, path + [str(key)])
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + [str(index)])
        elif isinstance(value, str):
            dotted = ".".join(path)
            image_metadata = "images" in path
            if not image_metadata and ("—" in value or "–" in value):
                issues.append((dotted, "contains a prohibited dash"))
            if not image_metadata and re.search(r"\bBiH\b", value):
                issues.append((dotted, "contains unexplained BiH"))

    for lesson in lessons:
        walk(lesson, [f"lesson{lesson['day']}"])
    for day, video in videos.items():
        if "—" in video or "–" in video:
            issues.append((f"video{day}", "contains a prohibited dash"))
        if re.search(r"\bBiH\b", video):
            issues.append((f"video{day}", "contains unexplained BiH"))
    if issues:
        for path, message in issues:
            print("validation issue", path, message)
    else:
        print("validation passed with no prohibited learner strings")
    return len(issues)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Lesson 16 images")
    imgs16 = [
        img_try(
            "sarajevo-bus-station",
            "Coaches wait outside the Sarajevo bus station.",
            "day-16-sarajevo-bus-station.png",
            [
                "File:Sarajevo bus station 2.jpg",
                "File:Sarajevo Bus-Station 2011-10-19.jpg",
            ],
        ),
        img_try(
            "jablanica-lake",
            "Blue water fills Jablaničko Lake among the hills.",
            "day-16-jablanica-lake.png",
            ["File:Jablaničko jezero 1.jpg", "File:Jablaničko jezero.jpg"],
        ),
        img_try(
            "neum-coast",
            "A beach curves along the Adriatic at Neum.",
            "day-16-neum-coast.png",
            ["File:Zenit Beach in Neum, 2024 1.jpg", "File:Neum.jpg"],
        ),
        img_try(
            "civic-a1-corridor",
            "A motorway corridor cuts through hills in Bosnia and Herzegovina.",
            "day-16-civic-a1-corridor.png",
            [
                "File:BiH Autoput A1.jpg",
                "File:Autobahn-Sarajevo.jpg",
                "File:Map Bih entities.png",
            ],
        ),
    ]
    print("Downloading Lesson 17 images")
    imgs17 = [
        img_try(
            "klepe-sarajevo",
            "A plate of klepe is served in Sarajevo.",
            "day-17-klepe-sarajevo.png",
            ["File:Klepe Sarajevo Bosnia (10675888145).jpg"],
        ),
        img_try(
            "japrak-dish",
            "Stuffed vine leaves are arranged as japrak.",
            "day-17-japrak-dish.png",
            ["File:Japrak 1.jpg", "File:Japrak me oriz.jpg"],
        ),
        img_try(
            "visoko-postcard",
            "Visoko spreads across hills below a wide sky.",
            "day-17-visoko-postcard.png",
            [
                "File:Visoko.jpg",
                "File:Plateu leading to the Old town of Visoki.jpg",
            ],
        ),
        img_try(
            "civic-food-economy",
            "A generous plate of ćevapi with kajmak represents local food service.",
            "day-17-civic-food-economy.png",
            [
                "File:Cevapi s kajmakom.jpg",
                "File:Burek in Sarajevo.jpg",
            ],
        ),
    ]
    print("Downloading Lesson 18 images")
    imgs18 = [
        img_try(
            "bilino-polje",
            "Bilino Polje stadium opens wide under a bright sky.",
            "day-18-bilino-polje.png",
            [
                "File:Bilino Polje Stadium (wide angle).jpg",
                "File:Stadion Bilino Polje.jpg",
            ],
        ),
        img_try(
            "bilino-polje-stands",
            "The stands of Bilino Polje face the green pitch.",
            "day-18-bilino-polje-stands.png",
            [
                "File:Stadion Bilino Polje.jpg",
                "File:Bilino Polje Stadium (wide angle).jpg",
            ],
        ),
        img_try(
            "strbacki-buk",
            "White water pours over stone shelves at Štrbački buk.",
            "day-18-strbacki-buk.png",
            [
                "File:Štrbački buk 1.jpg",
                "File:Una River Water Falls - Flickr - TKnoxB.jpg",
            ],
        ),
        img_try(
            "civic-emigration-airport",
            "Travelers move through Sarajevo International Airport.",
            "day-18-civic-emigration-airport.png",
            ["File:Sarajevo International Airport (SJJ).jpg", "File:Sarajevo International Airport.jpg"],
        ),
    ]
    print("Downloading Lesson 19 images")
    imgs19 = [
        img_try(
            "ferhadija-lights",
            "People walk Ferhadija Street in central Sarajevo.",
            "day-19-ferhadija-lights.png",
            ["File:Ferhadija, Sarajevo, 2023.01.22 2.jpg", "File:Ferhadija street Sarajevo.jpg"],
        ),
        img_try(
            "gazi-husrev-beg",
            "Gazi Husrev-beg's Mosque rises in Sarajevo.",
            "day-19-gazi-husrev-beg.png",
            ["File:Gazi Husrev-beg's Mosque. Sarajevo 04.jpg", "File:Gazi Husrev-beg Mosque.jpg"],
        ),
        img_try(
            "sacred-heart",
            "Sacred Heart Cathedral stands in Sarajevo.",
            "day-19-sacred-heart.png",
            ["File:Sarajevo Sacred Heart Cathedral IMG 1245.jpg", "File:Sacred Heart Cathedral Sarajevo.jpg"],
        ),
        img_try(
            "civic-pluralism",
            "Sacred Heart Cathedral marks one of Sarajevo's shared religious landmarks.",
            "day-19-civic-pluralism.png",
            [
                "File:Sarajevo Sacred Heart Cathedral IMG 1245.jpg",
                "File:Bosnia and Herzegovina 2013 Ethnic composition by municipality.png",
            ],
        ),
    ]
    print("Downloading Lesson 20 images")
    imgs20 = [
        img_try(
            "sarajevo-tram",
            "A blue Sarajevo tram travels along a city street.",
            "day-20-sarajevo-tram.png",
            [
                "File:Sarajevo tram 706.jpg",
                "File:Sarajevo Tram-505 Line-3 2011-11-13.jpg",
            ],
        ),
        img_try(
            "sarajevo-tram-city-hall",
            "A tram passes near Sarajevo City Hall.",
            "day-20-sarajevo-tram-city-hall.png",
            [
                "File:Sarajevo Tram City-Hall.jpg",
                "File:Sarajevo tram 706.jpg",
            ],
        ),
        img_try(
            "ferhadija-connection",
            "Pedestrians move along Ferhadija while the city stays connected.",
            "day-20-ferhadija-connection.png",
            [
                "File:Ferhadija, Sarajevo, 2023.01.22 2.jpg",
                "File:Ferhadija street Sarajevo.jpg",
            ],
        ),
        img_try(
            "civic-diaspora-calls",
            "A chart shows remittance costs as a share of money sent home.",
            "day-20-civic-diaspora-calls.png",
            [
                "File:Remittance-costs-as-share-of-amount-remitted.png",
                "File:Sarajevo International Airport (SJJ).jpg",
                "File:Mobile Network Tower.jpg",
            ],
        ),
    ]

    lessons = [
        build_lesson_16(imgs16),
        build_lesson_17(imgs17),
        build_lesson_18(imgs18),
        build_lesson_19(imgs19),
        build_lesson_20(imgs20),
    ]
    videos = {
        16: VIDEO_16,
        17: VIDEO_17,
        18: VIDEO_18,
        19: VIDEO_19,
        20: VIDEO_20,
    }
    issue_count = validate(lessons, videos)
    if issue_count:
        raise ValueError(f"Validation found {issue_count} prohibited learner strings.")
    for lesson in lessons:
        write_chapter(lesson["day"], lesson)
    for day, text in videos.items():
        write_video(day, text)
    if FAILED_IMAGE_ATTEMPTS:
        print("Image candidates that failed before an alternate succeeded:")
        for failure in FAILED_IMAGE_ATTEMPTS:
            print(failure)
    else:
        print("All first-choice image downloads succeeded.")
    print("done")


if __name__ == "__main__":
    main()

