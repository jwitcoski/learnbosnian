#!/usr/bin/env python3
"""Draft full chapter.json and video-script.md files for Lessons 11 through 15."""
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
    }
    if can_do_checks is not None:
        data["canDoChecks"] = can_do_checks
    data["section"] = section
    return data


def build_lesson_11(images: list) -> dict:
    v = [
        vocab("vrijeme", "weather", "VRYE-meh", "noun", "Vrijeme je hladno."),
        vocab("kakvo", "what kind of", "KAHK-vo", "question word", "Kakvo je vrijeme?"),
        vocab("sunce", "sun", "SOON-tseh", "noun", "Sunce sija."),
        vocab("kiša", "rain", "KEE-sha", "noun", "Pada kiša."),
        vocab("snijeg", "snow", "SNYEH-g", "noun", "Pada snijeg."),
        vocab("oblačno", "cloudy", "OH-blach-no", "adjective", "Oblačno je."),
        vocab("hladno", "cold", "HLAHD-no", "adjective", "Hladno je na planini."),
        vocab("toplo", "warm", "TOH-plo", "adjective", "Toplo je u kafiću."),
        vocab("vruće", "hot", "VROO-cheh", "adjective", "Ljeti je vruće."),
        vocab("vjetar", "wind", "VYEH-tar", "noun", "Vjetar je jak."),
        vocab("jesen", "autumn", "YEH-sen", "noun", "Jesen je hladna."),
        vocab("zima", "winter", "ZEE-ma", "noun", "Zima donosi snijeg."),
        vocab("ljeto", "summer", "LYEH-to", "noun", "Ljeto je toplo."),
        vocab("proljeće", "spring", "PROH-lyeh-cheh", "noun", "Proljeće je lijepo."),
        vocab("pada", "falls or is falling", "PAH-da", "verb form", "Kiša pada."),
        vocab("sunčano", "sunny", "SOON-cha-no", "adjective", "Sunčano je."),
    ]
    grammar = [
        {
            "title": "Kakvo je vrijeme?",
            "explanation": "Ask Kakvo je vrijeme? when you want a general weather report. Kakvo agrees with the neuter noun vrijeme. The whole question is a useful chunk that works in every season.",
            "examples": [
                {"bosnian": "Kakvo je vrijeme?", "english": "How is the weather?"},
                {"bosnian": "Kakvo je vrijeme na Trebeviću?", "english": "How is the weather on Trebević?"},
                {"bosnian": "Vrijeme je hladno.", "english": "The weather is cold."},
            ],
        },
        {
            "title": "Neuter weather descriptions",
            "explanation": "Bosnian often describes the weather with a neuter adjective followed by je. Say Hladno je, Toplo je, or Oblačno je. These short sentences do not need a separate word for it.",
            "examples": [
                {"bosnian": "Hladno je.", "english": "It is cold."},
                {"bosnian": "Toplo je.", "english": "It is warm."},
                {"bosnian": "Oblačno je.", "english": "It is cloudy."},
            ],
        },
        {
            "title": "Pada kiša and pada snijeg",
            "explanation": "Use pada with rain or snow to describe what is falling. Say Pada kiša for rain and Pada snijeg for snow. Keep each pair together so you can report a sudden change quickly.",
            "examples": [
                {"bosnian": "Pada kiša.", "english": "It is raining."},
                {"bosnian": "Pada snijeg.", "english": "It is snowing."},
                {"bosnian": "Kiša pada na Trebeviću.", "english": "Rain is falling on Trebević."},
            ],
        },
    ]
    facts = [
        {
            "title": "The cable car returned",
            "body": "The Trebević cable car connects Sarajevo with the mountain above the city. The original line was destroyed during the war, and a rebuilt service opened in 2018. The ride now gives residents and visitors quick access to forest paths and broad views. The restored cable car has again made the mountain feel close to the city.",
        },
        {
            "title": "Jahorina changes with the seasons",
            "body": "Jahorina is a mountain where the season changes the entire experience. Winter brings ski slopes and reliable snow, while warmer months bring green trails and open views. A postcard from Jahorina helps Ana compare snijeg, sunce, zima, and ljeto. The mountain makes season words visible rather than abstract.",
        },
        {
            "title": "Mountain weather moves quickly",
            "body": "Weather on Trebević can change faster than weather in the basin below. Sun can disappear behind cloud, and wind can arrive before rain. Ana learns this fact when the picnic blanket becomes wet. The ruined picnic makes Kakvo je vrijeme? a practical question.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does vrijeme mean?", ["Weather", "Picnic", "Mountain", "Season"], 0, "Vrijeme means weather.", "vocabulary"),
        quiz_question("q2", "Which sentence asks about the weather?", ["Pada kiša.", "Kakvo je vrijeme?", "Jesen je hladna.", "Vjetar je jak."], 1, "Kakvo je vrijeme? asks how the weather is.", "grammar"),
        quiz_question("q3", "Which sentence means that it is cloudy?", ["Sunčano je.", "Toplo je.", "Oblačno je.", "Pada snijeg."], 2, "Oblačno je means that it is cloudy.", "grammar"),
        quiz_question("q4", "Which season is zima?", ["Spring", "Summer", "Autumn", "Winter"], 3, "Zima means winter.", "vocabulary"),
        quiz_question("q5", "What ruined Ana and Emir's picnic?", ["Rain reached the blanket.", "Snow blocked the cable car.", "Heat melted the food.", "Wind took the postcard."], 0, "Rain reaches the blanket and ruins the picnic.", "dialogue"),
        quiz_question("q6", "Which place appears on Emir's second mountain postcard?", ["Vrelo Bosne", "Jahorina", "Brčko", "Konjic"], 1, "Jahorina appears as the second mountain place.", "culture"),
        quiz_question("q7", "Which sentence means that it is snowing?", ["Snijeg je topao.", "Zima je sunčana.", "Pada snijeg.", "Vjetar pada."], 2, "Pada snijeg means that it is snowing.", "grammar"),
        quiz_question("q8", "Why can winter air pollution linger in Sarajevo?", ["The cable car makes smoke.", "The river stops all wind.", "The mountains create summer heat.", "An inversion can trap polluted air."], 3, "A winter inversion can trap polluted air in the Sarajevo basin.", "culture"),
    ]
    return chapter(
        day=11,
        title="Kakvo je vrijeme?",
        title_en="How is the weather?",
        theme="Autumn on Trebević",
        story="Rain ruins Ana and Emir's picnic on Trebević.",
        goals={
            "vocabulary": [
                "Name common weather conditions and the four seasons.",
                "Describe sun, rain, snow, wind, warmth, and cold.",
                "Recognize weather words in a mountain forecast.",
            ],
            "grammar": [
                "Ask Kakvo je vrijeme? for a general weather report.",
                "Use neuter weather descriptions such as Hladno je and Oblačno je.",
                "Say Pada kiša and Pada snijeg when rain or snow is falling.",
            ],
            "culture": [
                "Explore autumn weather on Trebević and the Sarajevo cable car.",
                "Compare Trebević with a seasonal postcard from Jahorina.",
                "Understand why winter inversions affect air in the Sarajevo basin.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Autumn above Sarajevo",
            "body": "Trebević rises directly above Sarajevo, but its forest air can feel far from the busy basin. Ana and Emir ride the cable car with a picnic and watch autumn colors spread below them. Sunce shines at first, then vjetar bends the branches and dark clouds gather. Emir shows a Jahorina postcard while Ana practices the four seasons. Jahorina is known for winter snow, while Trebević offers a quick mountain escape from the city. When kiša soaks the blanket, Ana learns that mountain weather rewards a good forecast and a flexible plan.",
            "imageId": "trebevic-cable",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Weather and season words",
                "body": "Start with vrijeme, sunce, kiša, snijeg, and vjetar. Then add the four seasons, which are proljeće, ljeto, jesen, and zima. Look at the Trebević view and describe what you can actually see. Say Sunčano je when the sky is bright, Oblačno je when clouds cover it, and Hladno je when the mountain air bites. Ana packs for warm autumn sun, but Emir notices the wind. Their different guesses turn the vocabulary into a real forecast. The mountain gives each term a visible reference. Repeat each weather sentence aloud, then choose one season and describe its usual conditions in two short Bosnian sentences.",
                "tips": [
                    "Keep vrijeme and Kakvo je vrijeme? together as a useful question pattern.",
                    "Say the complete sentence Hladno je instead of giving only the adjective.",
                    "Use the Jahorina postcard to connect zima with snijeg.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Report a changing forecast",
                "body": "Build a weather report from short, complete sentences. Ask Kakvo je vrijeme? and answer Toplo je, Hladno je, Sunčano je, or Oblačno je. When something begins to fall, switch to Pada kiša or Pada snijeg. Ana looks at one patch of blue sky and declares success, but the clouds cross Trebević before lunch. Emir hears the first drops and says Pada kiša. The picnic moves under shelter while Mrvica, safely at home, avoids the entire problem. A quick update keeps the group prepared. Practice changing your report from sun to cloud to rain so the phrases become quick enough for a real conversation.",
                "tips": [
                    "Use a neuter adjective because vrijeme is a neuter noun.",
                    "Keep pada beside kiša or snijeg when you describe precipitation.",
                    "Answer a weather question with one clear sentence before adding details.",
                ],
            },
        ],
        conversation={
            "title": "Piknik na kiši",
            "setting": "Ana and Emir have opened a picnic blanket near the Trebević cable car.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Kakvo je vrijeme?", "english": "How is the weather?"},
                {"speaker": "Emir", "bosnian": "Sunčano je, ali vjetar je jak.", "english": "It is sunny, but the wind is strong."},
                {"speaker": "Ana", "bosnian": "Toplo je. Hajde da jedemo.", "english": "It is warm. Let us eat."},
                {"speaker": "Emir", "bosnian": "Pogledaj! Sada je oblačno.", "english": "Look! It is cloudy now."},
                {"speaker": "Ana", "bosnian": "Pada kiša! Gdje je kišobran?", "english": "It is raining! Where is the umbrella?"},
                {"speaker": "Emir", "bosnian": "Kišobran je u kafiću.", "english": "The umbrella is in the café."},
                {"speaker": "Narrator", "bosnian": "Piknik je mokar, a Ana trči prema žičari.", "english": "The picnic is wet, and Ana runs toward the cable car."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the weather",
                "prompt": "Match each Bosnian weather word with its English meaning.",
                "items": [
                    {"left": "kiša", "right": "rain"},
                    {"left": "snijeg", "right": "snow"},
                    {"left": "vjetar", "right": "wind"},
                    {"left": "sunčano", "right": "sunny"},
                    {"left": "oblačno", "right": "cloudy"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about the forecast",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Pada kiša means that it is raining.", "answer": True},
                    {"statement": "Zima means summer.", "answer": False},
                    {"statement": "Oblačno je describes cloudy weather.", "answer": True},
                    {"statement": "The picnic stays dry.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian question that asks how the weather is.", "hint": "Begin with Kakvo.", "answer": "Kakvo je vrijeme?"},
            {"id": "pr2", "prompt": "Write the Bosnian sentence for It is cold.", "hint": "Use hladno.", "answer": "Hladno je."},
            {"id": "pr3", "prompt": "Write the Bosnian sentence for It is cloudy.", "hint": "Use oblačno.", "answer": "Oblačno je."},
            {"id": "pr4", "prompt": "Write the Bosnian sentence for It is raining.", "hint": "Use pada and kiša.", "answer": "Pada kiša."},
            {"id": "pr5", "prompt": "Write the Bosnian sentence for It is snowing.", "hint": "Use pada and snijeg.", "answer": "Pada snijeg."},
            {"id": "pr6", "prompt": "Write the Bosnian word for autumn.", "hint": "The word begins with j.", "answer": "jesen"},
            {"id": "pr7", "prompt": "Write the Bosnian word for spring.", "hint": "The word begins with prol.", "answer": "proljeće"},
        ],
        facts=facts,
        resources=[
            {"label": "How To Speak Bosnian Weather", "url": "https://www.youtube.com/watch?v=NLlkMluC4jA", "note": "This speaker resource reinforces the weather phrases from Lesson 11."},
            {"label": "Next lesson", "url": "/learn/lesson/12", "note": "Lesson 12 invites Ana and Mrvica to Vrelo Bosne."},
            {"label": "Book 1 curriculum", "url": "/learn", "note": "The curriculum page lists every Book 1 lesson."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Winter inversions trap polluted air",
            "body": "Winter air pollution is a serious civic problem in the Sarajevo basin. Mountains surround the city, and cold weather can create an inversion that holds a layer of colder air near the ground. Smoke and fine particles from heating, traffic, and other sources then remain trapped instead of dispersing. Residents may face unhealthy air for several days until wind or a weather change clears the basin. The same landscape that gives the cable car its striking view can therefore make clean winter air harder to protect.",
            "imageId": "civic-sarajevo-bowl",
            "learnMore": {"label": "Wikipedia article about Sarajevo climate", "url": "https://en.wikipedia.org/wiki/Sarajevo#Climate"},
        },
        listen=authentic_listen(
            title="Čuj Bosnu with a weather lesson",
            kind="speaker",
            hook="A Bosnian teacher models weather words in a voice outside the story cast.",
            source_title="How To Speak Bosnian Weather",
            artist="How To Speak Bosnian",
            scene="Weather lesson",
            credit="How To Speak Bosnian on YouTube",
            url="https://www.youtube.com/watch?v=NLlkMluC4jA",
            prompt="Listen for a weather condition that you can report with je or pada.",
            gist_prompt="What is the speaker mainly teaching?",
            gist_options=["Weather expressions", "Shopping prices", "Room furniture", "Bridge history"],
            gist_index=0,
            target_words=["vrijeme", "kiša", "snijeg"],
            notice="Listen for the difference between an adjective with je and precipitation with pada.",
            key_lines=[
                {"bosnian": "Kakvo je vrijeme?", "english": "How is the weather?"},
                {"bosnian": "Pada kiša.", "english": "It is raining."},
            ],
            teacher_note="Pause after each model and give your own weather report.",
        ),
        speak_targets=[0, 3, 4],
        section=2,
    )


def build_lesson_12(images: list) -> dict:
    v = [
        vocab("park", "park", "park", "noun", "Park je lijep."),
        vocab("šetati", "to walk", "SHEH-ta-tee", "verb", "Volim šetati."),
        vocab("ići", "to go", "EE-chee", "verb", "Želim ići u park."),
        vocab("idem", "I am going", "EE-dem", "verb form", "Idem u park."),
        vocab("ideš", "you are going", "EE-desh", "verb form", "Ideš li sa mnom?"),
        vocab("idemo", "we are going", "EE-deh-mo", "verb form", "Idemo na Vrelo Bosne."),
        vocab("hajde", "come on or let us", "HAI-deh", "invitation", "Hajde da idemo."),
        vocab("dođi", "come", "DOH-jee", "imperative", "Dođi ovamo, Mrvice."),
        vocab("hoćeš", "you want or will you", "HOH-chesh", "verb form", "Hoćeš li šetati?"),
        vocab("trava", "grass", "TRAH-va", "noun", "Trava je zelena."),
        vocab("drvo", "tree", "DR-vo", "noun", "Drvo je visoko."),
        vocab("povodac", "leash", "POH-vo-dats", "noun", "Imam povodac za Mrvicu."),
        vocab("polako", "slowly", "POH-lah-ko", "adverb", "Hodaj polako."),
        vocab("brzo", "quickly", "BR-zoh", "adverb", "Mrvica trči brzo."),
        vocab("čekaj", "wait", "CHEH-kai", "imperative", "Čekaj, Mrvice!"),
    ]
    grammar = [
        {
            "title": "Idem, ideš, and idemo",
            "explanation": "The verb ići means to go. Use idem for I am going, ideš for you are going, and idemo for we are going. Add a destination such as u park to make each form useful.",
            "examples": [
                {"bosnian": "Idem u park.", "english": "I am going to the park."},
                {"bosnian": "Ideš li sa mnom?", "english": "Are you going with me?"},
                {"bosnian": "Idemo na Vrelo Bosne.", "english": "We are going to Vrelo Bosne."},
            ],
        },
        {
            "title": "Hajde da idemo",
            "explanation": "Use Hajde da followed by a present verb when you suggest doing something together. Hajde da idemo is a warm invitation to get moving. The pattern also works with šetamo when you suggest a walk.",
            "examples": [
                {"bosnian": "Hajde da idemo.", "english": "Let us go."},
                {"bosnian": "Hajde da šetamo.", "english": "Let us take a walk."},
                {"bosnian": "Hajde da idemo u park.", "english": "Let us go to the park."},
            ],
        },
        {
            "title": "Hoćeš li for invitations",
            "explanation": "Begin a yes or no invitation with Hoćeš li. Put an infinitive such as šetati or ići after it. Answer with Hoću when you accept or Neću when you decline.",
            "examples": [
                {"bosnian": "Hoćeš li šetati?", "english": "Do you want to walk?"},
                {"bosnian": "Hoćeš li ići u park?", "english": "Do you want to go to the park?"},
                {"bosnian": "Hoću, idemo!", "english": "I do, so let us go!"},
            ],
        },
    ]
    facts = [
        {
            "title": "The Bosna begins here",
            "body": "Vrelo Bosne is the source area of the Bosna River. Springs rise at the foot of Mount Igman and feed clear channels through the park. Paths and small bridges let visitors follow the water without leaving Ilidža. The river that names the country begins in a calm green landscape.",
        },
        {
            "title": "A long avenue leads to the springs",
            "body": "Velika aleja creates a memorable approach to Vrelo Bosne. Tall trees line the straight route from Ilidža toward the park. Visitors walk, cycle, or use traditional horse carriages along the avenue. The shaded approach turns the journey into part of the visit.",
        },
        {
            "title": "A cat rejects the leash plan",
            "body": "Mrvica treats a leash as a suggestion rather than a rule. Ana says polako, while the cat chooses brzo and heads for the grass. Emir says čekaj, but Mrvica circles a tree. The failed walk makes invitation and movement words easy to remember.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does idemo mean?", ["We are going", "I am walking", "You are waiting", "They are coming"], 0, "Idemo means that we are going.", "vocabulary"),
        quiz_question("q2", "Which sentence invites someone to walk?", ["Idem u park.", "Hoćeš li šetati?", "Čekaj kod drveta.", "Mrvica trči brzo."], 1, "Hoćeš li šetati? asks whether someone wants to walk.", "grammar"),
        quiz_question("q3", "Which word means leash?", ["trava", "drvo", "povodac", "park"], 2, "Povodac means leash.", "vocabulary"),
        quiz_question("q4", "Which word means slowly?", ["hajde", "čekaj", "brzo", "polako"], 3, "Polako means slowly.", "vocabulary"),
        quiz_question("q5", "What happens during Mrvica's park walk?", ["She tangles the leash around a tree.", "She sleeps beside the spring.", "She waits quietly by Ana.", "She rides in a carriage."], 0, "Mrvica tangles the leash around a tree.", "dialogue"),
        quiz_question("q6", "What begins at Vrelo Bosne?", ["The Vrbas River", "The Bosna River", "The Neretva River", "The Drina River"], 1, "The Bosna River begins in the spring area at Vrelo Bosne.", "culture"),
        quiz_question("q7", "Which sentence means Let us go?", ["Dođi ovamo.", "Ideš li sada?", "Hajde da idemo.", "Čekaj polako."], 2, "Hajde da idemo means Let us go.", "grammar"),
        quiz_question("q8", "What made the 2014 floods especially destructive?", ["A winter inversion", "A cable car failure", "A dry summer", "Extreme rain and swollen rivers"], 3, "Extreme rain and swollen rivers drove the destructive 2014 floods.", "culture"),
    ]
    return chapter(
        day=12,
        title="Idemo u park",
        title_en="Let's go to the park",
        theme="A walk at Vrelo Bosne",
        story="Ana tries to walk Mrvica on a leash at Vrelo Bosne.",
        goals={
            "vocabulary": [
                "Use movement words for walking, waiting, and changing speed.",
                "Name grass, a tree, and a leash during a park visit.",
                "Recognize idem, ideš, and idemo in simple plans.",
            ],
            "grammar": [
                "Choose idem, ideš, or idemo for who is going.",
                "Suggest a shared activity with Hajde da.",
                "Invite someone with a Hoćeš li question.",
            ],
            "culture": [
                "Visit Vrelo Bosne and the source of the Bosna River near Ilidža.",
                "Follow the tree-lined approach from Ilidža to the springs.",
                "Learn how the 2014 floods affected communities across the country.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Walking where the Bosna begins",
            "body": "Vrelo Bosne spreads through springs, channels, and wooded paths at the foot of Mount Igman near Ilidža. The Bosna River begins here before flowing north through the country. Ana expects a peaceful walk under tall trees, and Emir points out the long avenue that connects the park with Ilidža. Families stroll beside the water, and horse carriages still travel the shaded route. Mrvica turns the calm visit into comedy by fighting her povodac and racing across the trava. The park gives Ana a green setting for invitations, movement verbs, and one urgent command to wait.",
            "imageId": "vrelo-bosne",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Go for a walk",
                "body": "Begin with the movement verb ići and its useful forms. Say Idem u park when you are going, ask Ideš li sa mnom? when you want company, and say Idemo when the group is ready. Add šetati for walking and the destination u park. At Vrelo Bosne, Ana and Emir follow the water while Mrvica studies every patch of grass. Ana announces each plan before they move. Repeat the three forms with different speakers, then point toward a destination and say a complete sentence. The goal is to connect the person, the verb form, and the place without stopping to build a table.",
                "tips": [
                    "Use idem for yourself, ideš for one person you address, and idemo for the group.",
                    "Add u park after the verb when the park is your destination.",
                    "Say each movement sentence while you physically point in the direction of travel.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Invite and respond",
                "body": "Turn movement into a social plan with Hajde da idemo or Hoćeš li šetati? The first phrase suggests an activity for the group, while the second asks whether another person wants to join. Ana uses both patterns before attaching Mrvica's leash. The cat responds by moving brzo, not polako, and wraps the povodac around a drvo. Ana calls Dođi and Čekaj while Emir tries not to laugh. The park supplies every cue. Practice one invitation, one acceptance, and one command as a three-part exchange. Keep the tone friendly because these phrases are useful with friends during any walk, not only with a determined cat.",
                "tips": [
                    "Use Hajde da when you suggest an activity that includes you.",
                    "Use Hoćeš li followed by an infinitive when you offer a choice.",
                    "Say čekaj clearly when someone or some cat needs to wait.",
                ],
            },
        ],
        conversation={
            "title": "Mrvica u parku",
            "setting": "Ana, Emir, and Mrvica stand beside a path at Vrelo Bosne.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Hajde da idemo u park.", "english": "Let us go to the park."},
                {"speaker": "Emir", "bosnian": "Hoćeš li šetati pored vode?", "english": "Do you want to walk beside the water?"},
                {"speaker": "Ana", "bosnian": "Hoću. Imam povodac za Mrvicu.", "english": "I do. I have a leash for Mrvica."},
                {"speaker": "Emir", "bosnian": "Mrvica, polako! Drvo je ispred tebe.", "english": "Mrvica, go slowly! A tree is in front of you."},
                {"speaker": "Ana", "bosnian": "Čekaj! Ne tako brzo!", "english": "Wait! Do not go so quickly!"},
                {"speaker": "Narrator", "bosnian": "Mrvica trči oko drveta i povodac se zapetlja.", "english": "Mrvica runs around the tree, and the leash becomes tangled."},
                {"speaker": "Emir", "bosnian": "Idemo u park bez povodca drugi put.", "english": "We will go to the park without a leash next time."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match park words",
                "prompt": "Match each Bosnian park word with its English meaning.",
                "items": [
                    {"left": "šetati", "right": "to walk"},
                    {"left": "trava", "right": "grass"},
                    {"left": "drvo", "right": "tree"},
                    {"left": "povodac", "right": "leash"},
                    {"left": "čekaj", "right": "wait"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about the walk",
                "prompt": "Decide whether each sentence matches Lesson 12.",
                "items": [
                    {"statement": "Idemo means that we are going.", "answer": True},
                    {"statement": "Brzo means slowly.", "answer": False},
                    {"statement": "Vrelo Bosne is the source area of the Bosna River.", "answer": True},
                    {"statement": "Mrvica walks calmly on the leash.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian sentence for I am going to the park.", "hint": "Begin with Idem.", "answer": "Idem u park."},
            {"id": "pr2", "prompt": "Write the Bosnian phrase for We are going.", "hint": "Use the we form of ići.", "answer": "Idemo."},
            {"id": "pr3", "prompt": "Write the Bosnian invitation for Let us go.", "hint": "Begin with Hajde da.", "answer": "Hajde da idemo."},
            {"id": "pr4", "prompt": "Write the Bosnian question for Do you want to walk?", "hint": "Begin with Hoćeš li.", "answer": "Hoćeš li šetati?"},
            {"id": "pr5", "prompt": "Write the Bosnian command that tells one person to wait.", "hint": "The word begins with č.", "answer": "Čekaj."},
            {"id": "pr6", "prompt": "Write the Bosnian word for leash.", "hint": "The word begins with pov.", "answer": "povodac"},
            {"id": "pr7", "prompt": "Write the Bosnian word for slowly.", "hint": "The word begins with pol.", "answer": "polako"},
        ],
        facts=facts,
        resources=[
            {"label": "How To Speak Bosnian Imperative Mood", "url": "https://www.youtube.com/watch?v=cq9_DVwpUCY", "note": "This speaker resource models Bosnian commands and imperative forms."},
            {"label": "Next lesson", "url": "/learn/lesson/13", "note": "Lesson 13 introduces place and language conversations."},
            {"label": "Book 1 curriculum", "url": "/learn", "note": "The curriculum page lists every Book 1 lesson."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "The 2014 floods crossed local boundaries",
            "body": "The 2014 floods showed how a shared river emergency can affect much of Bosnia and Herzegovina. Exceptional rain caused rivers to rise, triggered landslides, damaged homes, and forced many people to evacuate. Towns such as Maglaj and Doboj faced severe destruction, while roads, farms, and public services failed in many other communities. Residents, rescue teams, and volunteers worked across administrative lines during the response and recovery. The disaster showed that flood preparation and river management require cooperation beyond any single municipality.",
            "imageId": "civic-floods",
            "learnMore": {"label": "Wikipedia article about the 2014 Southeast Europe floods", "url": "https://en.wikipedia.org/wiki/2014_Southeast_Europe_floods"},
        },
        listen=authentic_listen(
            title="Čuj Bosnu with imperative forms",
            kind="speaker",
            hook="A Bosnian teacher explains command forms that can guide a walk.",
            source_title="How To Speak Bosnian Imperative mood",
            artist="How To Speak Bosnian",
            scene="Imperative lesson",
            credit="How To Speak Bosnian on YouTube",
            url="https://www.youtube.com/watch?v=cq9_DVwpUCY",
            prompt="Listen for a command form that could guide Mrvica in the park.",
            gist_prompt="What grammar is the speaker mainly teaching?",
            gist_options=["Past tense stories", "Command forms", "Weather adjectives", "Possessive forms"],
            gist_index=1,
            target_words=["dođi", "čekaj", "idemo"],
            notice="Notice how a short command can sound direct while the speaker's tone remains friendly.",
            key_lines=[
                {"bosnian": "Dođi ovamo.", "english": "Come here."},
                {"bosnian": "Čekaj!", "english": "Wait!"},
            ],
            teacher_note="Repeat the command, then soften your voice as if you were speaking to a friend.",
        ),
        speak_targets=[0, 1, 4],
        section=2,
    )


def build_lesson_13(images: list) -> dict:
    v = [
        vocab("ljudi", "people", "LYOO-dee", "noun", "Ljudi razgovaraju uz kahvu."),
        vocab("zemlja", "country or land", "ZEHM-lya", "noun", "Bosna i Hercegovina je zemlja."),
        vocab("govoriti", "to speak", "goh-VOH-ree-tee", "verb", "Želim govoriti bosanski."),
        vocab("govorim", "I speak", "goh-VOH-reem", "verb form", "Govorim engleski."),
        vocab("govoriš", "you speak", "goh-VOH-reesh", "verb form", "Govoriš li bosanski?"),
        vocab("bosanski", "Bosnian", "boh-SAHN-skee", "language adjective", "Učim bosanski."),
        vocab("engleski", "English", "EHN-gleh-skee", "language adjective", "Ana govori engleski."),
        vocab("Amerikanka", "American woman", "ah-meh-ree-KAHN-ka", "noun", "Ana je Amerikanka."),
        vocab("Bosanac", "Bosnian man", "boh-SAH-nats", "noun", "On je Bosanac."),
        vocab("Bosanka", "Bosnian woman", "boh-SAHN-ka", "noun", "Ona je Bosanka."),
        vocab("odakle", "from where", "OH-dah-kleh", "question word", "Odakle si?"),
        vocab("jezik", "language", "YEH-zeek", "noun", "Bosanski jezik je lijep."),
        vocab("narod", "people or nation", "NAH-rod", "noun", "Narod ima mnogo priča."),
        vocab("ko", "who", "koh", "question word", "Ko govori bosanski?"),
    ]
    grammar = [
        {
            "title": "Govorim bosanski",
            "explanation": "Use govorim to say which language you speak. Bosnian language names usually follow the verb without an article. Replace bosanski with engleski when you describe English.",
            "examples": [
                {"bosnian": "Govorim bosanski.", "english": "I speak Bosnian."},
                {"bosnian": "Govorim engleski.", "english": "I speak English."},
                {"bosnian": "Malo govorim bosanski.", "english": "I speak a little Bosnian."},
            ],
        },
        {
            "title": "Odakle si?",
            "explanation": "Ask Odakle si? when you want to know where someone is from. Answer with Ja sam iz followed by a place. A place answer shares useful information without forcing a larger identity label.",
            "examples": [
                {"bosnian": "Odakle si?", "english": "Where are you from?"},
                {"bosnian": "Ja sam iz Amerike.", "english": "I am from America."},
                {"bosnian": "Ja sam iz Sarajeva.", "english": "I am from Sarajevo."},
            ],
        },
        {
            "title": "Ko govori?",
            "explanation": "Use ko when you ask who a person is or who does an action. Pair ko with govori to ask who speaks a language. Answer with a person's name and a complete sentence.",
            "examples": [
                {"bosnian": "Ko govori bosanski?", "english": "Who speaks Bosnian?"},
                {"bosnian": "Emir govori bosanski.", "english": "Emir speaks Bosnian."},
                {"bosnian": "Ko je iz Brčkog?", "english": "Who is from Brčko?"},
            ],
        },
    ]
    facts = [
        {
            "title": "Place can open a gentle conversation",
            "body": "A place question can begin an identity conversation without trying to define a person. Odakle si? lets someone answer with a city, region, country, or another place that matters. The answer can remain simple or lead to more detail if both speakers want it. Place and language provide a respectful starting point.",
        },
        {
            "title": "Brčko sits on the Sava",
            "body": "Brčko stands on the Sava River in the northeast of Bosnia and Herzegovina. Its river position helped make the city an important trade and transport point. The promenade gives residents a public place beside that wider regional route. The city connects local life with a river that crosses borders.",
        },
        {
            "title": "Language names can vary",
            "body": "People in Bosnia and Herzegovina may name closely related language standards in different ways. Bosnian, Croatian, and Serbian are all heard in the country, and speakers understand one another to a high degree. This lesson practices bosanski because that is the course language. Respecting the name a speaker uses keeps language learning courteous.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does ljudi mean?", ["People", "Language", "Country", "Coffee"], 0, "Ljudi means people.", "vocabulary"),
        quiz_question("q2", "Which sentence means I speak Bosnian?", ["Učim iz Bosne.", "Govorim bosanski.", "Ja sam jezik.", "Ko je bosanski?"], 1, "Govorim bosanski means I speak Bosnian.", "grammar"),
        quiz_question("q3", "Which question asks where someone is from?", ["Ko govori?", "Govoriš li?", "Odakle si?", "Koji jezik?"], 2, "Odakle si? asks where someone is from.", "grammar"),
        quiz_question("q4", "Which word means language?", ["narod", "zemlja", "ljudi", "jezik"], 3, "Jezik means language.", "vocabulary"),
        quiz_question("q5", "How does Ana describe her background?", ["She is from America and is learning Bosnian.", "She is from Brčko and teaches English.", "She is from Sarajevo and speaks no English.", "She is from Jahorina and studies weather."], 0, "Ana says she is from America and is learning Bosnian.", "dialogue"),
        quiz_question("q6", "Where is Emir from?", ["Konjic", "Sarajevo", "Banja Luka", "Ilidža"], 1, "Emir says that he is from Sarajevo.", "dialogue"),
        quiz_question("q7", "What is special about Brčko District?", ["It is only a mountain resort.", "It is one of the two entities.", "It is a self-governing district under international supervision.", "It is a neighborhood of Sarajevo."], 2, "Brčko is a self-governing district under international supervision.", "culture"),
        quiz_question("q8", "What is the lesson's approach to identity?", ["It assigns one label to everyone.", "It explains an ethnic census in detail.", "It avoids all place names.", "It begins gently with place and language."], 3, "The lesson begins gently with place and language.", "culture"),
    ]
    return chapter(
        day=13,
        title="Ljudi iz BiH",
        title_en="People from Bosnia and Herzegovina",
        theme="Place, language, and people",
        story="Ana and Emir have a gentle identity conversation over kahva.",
        goals={
            "vocabulary": [
                "Name people, country, language, and nationality terms used in simple introductions.",
                "Use govorim and govoriš when discussing languages.",
                "Ask ko and odakle questions in a respectful conversation.",
            ],
            "grammar": [
                "Say Govorim bosanski or Govorim engleski.",
                "Ask Odakle si? and answer with Ja sam iz plus a place.",
                "Use ko to ask who speaks a language or comes from a place.",
            ],
            "culture": [
                "Keep identity talk gentle by beginning with place and language.",
                "Visit Brčko as a river city in the northeast.",
                "Understand Brčko District's distinct civic position.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Kahva, language, and a view of Brčko",
            "body": "Ana and Emir talk over kahva about where they come from and which languages they speak. Ana is from America and is learning Bosnian. Emir is from Sarajevo and shows her photographs of Brčko, a river city in the northeast of Bosnia and Herzegovina. Its promenade and white mosque place the conversation in a real, diverse city. People across the country use many names for themselves, their communities, and closely related language standards. This lesson does not force those identities into one answer. It gives Ana gentle questions about place and language, then leaves room for each person to describe themselves.",
            "imageId": "brcko-promenade",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Ask about place and language",
                "body": "Begin with two questions that let another person choose how much to share. Odakle si? asks where someone is from, while Govoriš li bosanski? asks whether the person speaks Bosnian. Ana answers Ja sam iz Amerike and adds Učim bosanski. Emir answers Ja sam iz Sarajeva and says Govorim bosanski. Practice the city or country answer that is true for you. Then name a language you speak, study, or want to learn. The answer remains yours. These patterns are useful because they focus on personal experience. They do not require you to guess a stranger's identity from a name, accent, religion, or appearance.",
                "tips": [
                    "Let each person choose the place name that best answers Odakle si?",
                    "Use govorim for your own language and govoriš when addressing one person.",
                    "Avoid guessing a person's identity before they describe themselves.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Talk about people with care",
                "body": "Add ljudi, zemlja, jezik, narod, and ko to widen the conversation. Bosanac and Bosanka can describe a Bosnian man or woman, while Amerikanka describes Ana as an American woman. These words are useful, but no single label tells a person's whole story. Emir explains that people in Bosnia and Herzegovina have many names for themselves and may emphasize a city, region, community, or language. Ana keeps her questions simple and listens to the answer. Use Ko govori bosanski? in a classroom or café, then answer with a complete sentence. The best practice combines accurate grammar with room for personal choice.",
                "tips": [
                    "Treat nationality words as options that people may use for themselves.",
                    "Use place and language questions before asking for more personal detail.",
                    "Answer ko with a named person and a complete verb phrase.",
                ],
            },
        ],
        conversation={
            "title": "Razgovor uz kahvu",
            "setting": "Ana and Emir sit with kahva while Amira arranges postcards from Brčko.",
            "lines": [
                {"speaker": "Emir", "bosnian": "Ana, odakle si?", "english": "Ana, where are you from?"},
                {"speaker": "Ana", "bosnian": "Ja sam iz Amerike. Ja sam Amerikanka.", "english": "I am from America. I am an American woman."},
                {"speaker": "Amira", "bosnian": "Govoriš li bosanski?", "english": "Do you speak Bosnian?"},
                {"speaker": "Ana", "bosnian": "Malo govorim bosanski. Govorim engleski.", "english": "I speak a little Bosnian. I speak English."},
                {"speaker": "Ana", "bosnian": "Emire, odakle si ti?", "english": "Emir, where are you from?"},
                {"speaker": "Emir", "bosnian": "Ja sam iz Sarajeva. Ljudi ovdje imaju mnogo priča.", "english": "I am from Sarajevo. People here have many stories."},
                {"speaker": "Amira", "bosnian": "Pijte kahvu i slušajte jedni druge.", "english": "Drink your coffee and listen to one another."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match people and language words",
                "prompt": "Match each Bosnian word with its English meaning.",
                "items": [
                    {"left": "ljudi", "right": "people"},
                    {"left": "zemlja", "right": "country or land"},
                    {"left": "jezik", "right": "language"},
                    {"left": "govorim", "right": "I speak"},
                    {"left": "odakle", "right": "from where"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about introductions",
                "prompt": "Decide whether each sentence follows the lesson.",
                "items": [
                    {"statement": "Odakle si? asks where someone is from.", "answer": True},
                    {"statement": "Govorim means that you speak.", "answer": False},
                    {"statement": "Ana is from America and is learning Bosnian.", "answer": True},
                    {"statement": "One identity label tells every part of a person.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian sentence for I speak Bosnian.", "hint": "Begin with Govorim.", "answer": "Govorim bosanski."},
            {"id": "pr2", "prompt": "Write the Bosnian sentence for I speak English.", "hint": "Use engleski.", "answer": "Govorim engleski."},
            {"id": "pr3", "prompt": "Write the Bosnian question that asks where someone is from.", "hint": "Begin with Odakle.", "answer": "Odakle si?"},
            {"id": "pr4", "prompt": "Write the Bosnian sentence for I am from Sarajevo.", "hint": "Use Ja sam iz.", "answer": "Ja sam iz Sarajeva."},
            {"id": "pr5", "prompt": "Write the Bosnian question for Who speaks Bosnian?", "hint": "Begin with Ko.", "answer": "Ko govori bosanski?"},
            {"id": "pr6", "prompt": "Write the Bosnian word for language.", "hint": "The word begins with jez.", "answer": "jezik"},
            {"id": "pr7", "prompt": "Write the Bosnian word for people.", "hint": "The word begins with lj.", "answer": "ljudi"},
        ],
        facts=facts,
        resources=[
            {"label": "How To Speak Bosnian Countries", "url": "https://www.youtube.com/watch?v=D9t5MU-srOE", "note": "This speaker resource models country and nationality vocabulary."},
            {"label": "Next lesson", "url": "/learn/lesson/14", "note": "Lesson 14 reviews Lessons 8 through 13 at Amira's."},
            {"label": "Book 1 curriculum", "url": "/learn", "note": "The curriculum page lists every Book 1 lesson."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Brčko District has a distinct civic role",
            "body": "Brčko District has a distinct place in the constitutional structure of Bosnia and Herzegovina. It is a self-governing district held in condominium by both entities rather than governed as an ordinary municipality within either one. An international supervisory system was created to support implementation of the postwar arbitration award and the district's multiethnic institutions. Local government in Brčko therefore operates alongside an unusual national and international framework. The district shows that the country's civic map includes more than the two entities alone.",
            "imageId": "civic-brcko-map",
            "learnMore": {"label": "Wikipedia article about Brčko District", "url": "https://en.wikipedia.org/wiki/Brčko_District"},
        },
        listen=authentic_listen(
            title="Čuj Bosnu with countries and origins",
            kind="speaker",
            hook="A Bosnian teacher models country words that support gentle introductions.",
            source_title="How To Speak Bosnian Countries",
            artist="How To Speak Bosnian",
            scene="Countries and origins lesson",
            credit="How To Speak Bosnian on YouTube",
            url="https://www.youtube.com/watch?v=D9t5MU-srOE",
            prompt="Listen for a country or origin word that could answer Odakle si?",
            gist_prompt="What vocabulary is the speaker mainly teaching?",
            gist_options=["Weather conditions", "Country names", "Room furniture", "Street directions"],
            gist_index=1,
            target_words=["zemlja", "Amerika", "bosanski"],
            notice="Listen for how a place name changes after the phrase Ja sam iz.",
            key_lines=[
                {"bosnian": "Odakle si?", "english": "Where are you from?"},
                {"bosnian": "Ja sam iz Amerike.", "english": "I am from America."},
            ],
            teacher_note="Answer the question with a place that feels natural for your own introduction.",
        ),
        speak_targets=[0, 3, 4],
        section=2,
    )


def build_lesson_14(images: list) -> dict:
    v = [
        vocab("volim", "I like or I love", "VOH-leem", "verb form", "Volim ovu igru."),
        vocab("želim", "I want", "ZHEH-leem", "verb form", "Želim još kahve."),
        vocab("imam", "I have", "EE-mam", "verb form", "Imam dobru kartu."),
        vocab("vrijeme", "weather", "VRYE-meh", "noun", "Vrijeme je hladno."),
        vocab("hajde", "come on or let us", "HAI-deh", "invitation", "Hajde da igramo."),
        vocab("govorim", "I speak", "goh-VOH-reem", "verb form", "Govorim malo bosanski."),
        vocab("igra", "game", "EE-gra", "noun", "Igra je zabavna."),
        vocab("karta", "card", "KAR-ta", "noun", "Imam crvenu kartu."),
        vocab("pobjeda", "victory", "POH-byeh-da", "noun", "Pobjeda je blizu."),
        vocab("još jednom", "one more time", "yosh YED-nom", "phrase", "Igramo još jednom."),
    ]
    grammar = [
        {
            "title": "Remember your useful first-person verbs",
            "explanation": "Volim, želim, imam, and govorim let you say a great deal about yourself. Follow each verb with a familiar object or language chunk. Use them during the game to express a preference, a wish, a possession, or a language ability.",
            "examples": [
                {"bosnian": "Volim ovu igru.", "english": "I like this game."},
                {"bosnian": "Želim još kahve.", "english": "I want more coffee."},
                {"bosnian": "Imam dobru kartu.", "english": "I have a good card."},
            ],
        },
        {
            "title": "Remember questions and invitations",
            "explanation": "Use Kakvo je vrijeme? to ask about weather, Hoćeš li? to offer a choice, and Hajde da to suggest a shared action. These patterns turn separate vocabulary lists into conversation. Choose the pattern that matches whether you need information, an answer, or group action.",
            "examples": [
                {"bosnian": "Kakvo je vrijeme?", "english": "How is the weather?"},
                {"bosnian": "Hoćeš li igrati?", "english": "Do you want to play?"},
                {"bosnian": "Hajde da igramo još jednom.", "english": "Let us play one more time."},
            ],
        },
    ]
    facts = [
        {
            "title": "Kastel guards a Vrbas crossing",
            "body": "Kastel Fortress stands beside the Vrbas River in Banja Luka. The site reflects many layers of settlement and defense around an important river crossing. Its walls now frame walks, events, and public gatherings rather than military control. Kastel connects the modern city with the strategic value of the river.",
        },
        {
            "title": "The Vrbas shapes Banja Luka",
            "body": "The Vrbas River gives Banja Luka a strong natural axis. Water, bridges, and tree-lined banks shape movement through the city. Upstream canyons also support rafting and other outdoor activities. A Vrbas postcard makes the city feel connected to both urban life and mountain water.",
        },
        {
            "title": "Ferhadija was rebuilt",
            "body": "The Ferhadija Mosque is an important landmark in Banja Luka. It was destroyed during the war and later reconstructed through careful work with historical evidence and recovered stone. The reopened mosque again serves worshippers and the wider city. Its return shows how rebuilding a landmark can restore both use and memory.",
        },
    ]
    quiz = [
        quiz_question("q1", "Which sentence expresses a food preference?", ["Volim burek.", "Imam prozor.", "Pada kiša.", "Idemo u park."], 0, "Volim burek expresses a food preference.", "vocabulary"),
        quiz_question("q2", "Which phrase asks the price?", ["Dobar tek.", "Koliko košta?", "Kakvo je vrijeme?", "Odakle si?"], 1, "Koliko košta? asks how much something costs.", "vocabulary"),
        quiz_question("q3", "Which sentence means I have a room?", ["Želim sobu.", "Volim sobu.", "Imam sobu.", "Idem u sobu."], 2, "Imam sobu means that I have a room.", "grammar"),
        quiz_question("q4", "Which sentence means that it is raining?", ["Kiša je ljeto.", "Sunčano je.", "Hladno je.", "Pada kiša."], 3, "Pada kiša means that it is raining.", "grammar"),
        quiz_question("q5", "Which phrase suggests going together?", ["Hajde da idemo.", "Ja sam iz parka.", "Govorim polako.", "Imam povodac."], 0, "Hajde da idemo suggests that the group should go.", "grammar"),
        quiz_question("q6", "Which question asks where someone is from?", ["Ko govori?", "Odakle si?", "Imaš li kartu?", "Hoćeš li igrati?"], 1, "Odakle si? asks where someone is from.", "grammar"),
        quiz_question("q7", "What does karta mean in the game scene?", ["Table", "Coffee", "Card", "Victory"], 2, "Karta means card in the board-game scene.", "vocabulary"),
        quiz_question("q8", "Which phrase asks for another round?", ["Dobar tek.", "Čekaj polako.", "Govorim engleski.", "Još jednom."], 3, "Još jednom means one more time.", "dialogue"),
        quiz_question("q9", "Which Banja Luka landmark stands beside the Vrbas?", ["Kastel Fortress", "Latin Bridge", "Vrelo Bosne", "Trebević cable car"], 0, "Kastel Fortress stands beside the Vrbas River.", "culture"),
        quiz_question("q10", "What is one major cause of demographic decline?", ["More board games", "Sustained emigration", "Warmer weather", "Longer park walks"], 1, "Sustained emigration contributes to demographic decline.", "culture"),
    ]
    return chapter(
        day=14,
        title="Ponavljanje",
        title_en="Review",
        theme="Board-game night at Amira's",
        story="A board game makes Ana reuse language from Lessons 8 through 13.",
        goals={
            "vocabulary": [
                "Reuse high-value words from food, shopping, home, weather, park, and identity lessons.",
                "Add igra, karta, pobjeda, and još jednom for game night.",
            ],
            "grammar": [
                "Combine volim, želim, imam, and govorim with familiar words.",
                "Reuse weather questions, invitations, and place questions in conversation.",
                "Choose a complete sentence instead of answering with an isolated word.",
            ],
            "culture": [
                "Visit Banja Luka through Kastel Fortress, the Vrbas River, and Ferhadija Mosque.",
                "Connect a relaxed game night with the wider movement of people away from the country.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Postcards from Banja Luka at game night",
            "body": "Amira covers the café table with a board game, snacks, and postcards from Banja Luka. One card shows Kastel Fortress beside the Vrbas River, where old walls meet a lively modern city. Another shows Ferhadija Mosque, reconstructed after its wartime destruction and reopened as a place of worship. Ana must answer a language question before every move. She asks about food, prices, rooms, weather, invitations, and places of origin. Emir wants pobjeda, while Mrvica wants the moving pieces. The Banja Luka postcards turn review night into another journey beyond Sarajevo.",
            "imageId": "kastel",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Build with familiar verbs",
                "body": "Review the four first-person forms that have carried Ana through recent lessons. Volim states a preference, želim states a wish, imam states possession, and govorim names a language you speak. Draw a card and complete its prompt with one of those verbs. You might say Volim sirnicu, Želim vodu, Imam malu sobu, or Govorim malo bosanski. Amira awards a game piece only for a complete, sayable sentence. Emir tries to win by speaking faster, but accuracy matters more than speed. Every card brings an old pattern back. Repeat any difficult sentence još jednom, then change one word so the pattern becomes flexible rather than memorized.",
                "tips": [
                    "Choose the verb by meaning before you add the familiar object.",
                    "Say the complete sentence aloud before you move your game piece.",
                    "Repeat a difficult pattern još jednom with one word changed.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Connect questions across lessons",
                "body": "Use the board to move between six conversation settings. Ask Koliko košta? at the shop, Kakvo je vrijeme? on Trebević, Hoćeš li šetati? at Vrelo Bosne, and Odakle si? over kahva. A room square requires an imam sentence, and a food square requires volim or želim. Ana discovers that the patterns support one another because each question invites a short, complete answer. Mrvica knocks over the weather cards, so the final round mixes every topic. Take one card from two different lessons and build a tiny exchange. The review succeeds when you can switch contexts without returning to English instructions.",
                "tips": [
                    "Listen to the question word before you choose your answer pattern.",
                    "Answer with a complete sentence even when one word might be understood.",
                    "Mix two lesson topics when a single topic feels too easy.",
                ],
            },
        ],
        conversation={
            "title": "Još jednom",
            "setting": "Amira's café table holds a board, cards, kahva, and one curious cat.",
            "lines": [
                {"speaker": "Amira", "bosnian": "Hajde da igramo. Ana, uzmi kartu.", "english": "Let us play. Ana, take a card."},
                {"speaker": "Ana", "bosnian": "Pitanje glasi Kakvo je vrijeme?", "english": "The question asks how the weather is."},
                {"speaker": "Emir", "bosnian": "Hladno je. Sada ja imam kartu.", "english": "It is cold. Now I have a card."},
                {"speaker": "Emir", "bosnian": "Ana, odakle si i šta govoriš?", "english": "Ana, where are you from, and what do you speak?"},
                {"speaker": "Ana", "bosnian": "Ja sam iz Amerike i govorim engleski.", "english": "I am from America, and I speak English."},
                {"speaker": "Narrator", "bosnian": "Mrvica gura figuru preko cilja.", "english": "Mrvica pushes a game piece across the finish."},
                {"speaker": "Amira", "bosnian": "Mrvica ima pobjedu. Igramo još jednom.", "english": "Mrvica has the victory. We are playing one more time."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the review verbs",
                "prompt": "Match each Bosnian form with the idea it expresses.",
                "items": [
                    {"left": "volim", "right": "I like"},
                    {"left": "želim", "right": "I want"},
                    {"left": "imam", "right": "I have"},
                    {"left": "govorim", "right": "I speak"},
                    {"left": "hajde", "right": "let us"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false across the review",
                "prompt": "Decide whether each sentence correctly reviews Lessons 8 through 13.",
                "items": [
                    {"statement": "Koliko košta? asks about price.", "answer": True},
                    {"statement": "Soba means weather.", "answer": False},
                    {"statement": "Hajde da idemo suggests going together.", "answer": True},
                    {"statement": "Odakle si? asks what someone wants to buy.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write a complete Bosnian sentence that says you like burek.", "hint": "Begin with Volim.", "answer": "Volim burek."},
            {"id": "pr2", "prompt": "Write a complete Bosnian sentence that says you want water.", "hint": "Use Želim and vodu.", "answer": "Želim vodu."},
            {"id": "pr3", "prompt": "Write a complete Bosnian sentence that says you have a room.", "hint": "Use Imam and sobu.", "answer": "Imam sobu."},
            {"id": "pr4", "prompt": "Write the Bosnian question that asks how the weather is.", "hint": "Begin with Kakvo.", "answer": "Kakvo je vrijeme?"},
            {"id": "pr5", "prompt": "Write the Bosnian invitation for Let us go.", "hint": "Begin with Hajde da.", "answer": "Hajde da idemo."},
            {"id": "pr6", "prompt": "Write a complete Bosnian sentence that says you speak Bosnian.", "hint": "Begin with Govorim.", "answer": "Govorim bosanski."},
            {"id": "pr7", "prompt": "Write the Bosnian phrase for one more time.", "hint": "The second word is jednom.", "answer": "još jednom"},
            {"id": "pr8", "prompt": "Write the Bosnian word for victory.", "hint": "The word begins with pob.", "answer": "pobjeda"},
        ],
        facts=facts,
        resources=[
            {"label": "Dino Merlin sings Sredinom", "url": "https://www.youtube.com/watch?v=9NADgl_ukEE", "note": "This song provides the listening focus for the Lesson 14 review."},
            {"label": "Next lesson", "url": "/learn/lesson/15", "note": "Lesson 15 follows Ana through Sarajevo with direction phrases."},
            {"label": "Book 1 curriculum", "url": "/learn", "note": "The curriculum page lists every Book 1 lesson."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Emigration is reshaping the population",
            "body": "Sustained emigration is reshaping communities across Bosnia and Herzegovina. Many younger adults leave for education, higher wages, or more predictable careers elsewhere in Europe and beyond. Low birth rates and an aging population deepen the decline, while official statistics struggle to measure everyone who has moved. Families maintain strong ties across borders, but schools, workplaces, and smaller towns can lose people faster than they replace them. Demographic decline is therefore not an abstract number because it changes who remains to build local institutions and community life.",
            "imageId": "civic-emigration",
            "learnMore": {"label": "Wikipedia article about demographics in Bosnia and Herzegovina", "url": "https://en.wikipedia.org/wiki/Demographics_of_Bosnia_and_Herzegovina"},
        },
        listen=authentic_listen(
            title="Čuj Bosnu with Dino Merlin",
            kind="song",
            hook="A Dino Merlin song gives the review a natural Bosnian pop voice.",
            source_title="Dino Merlin Sredinom",
            artist="Dino Merlin",
            scene="Bosnian pop song",
            credit="Dino Merlin on YouTube",
            url="https://www.youtube.com/watch?v=9NADgl_ukEE",
            prompt="Listen for repeated sounds or familiar small words without trying to translate every lyric.",
            gist_prompt="What kind of listening experience does the clip provide?",
            gist_options=["A weather forecast", "A park command lesson", "A Bosnian pop song", "A shop dialogue"],
            gist_index=2,
            target_words=["sredinom", "ja", "ti"],
            notice="Let the melody carry you while you notice any short word you already recognize.",
            key_lines=[
                {"bosnian": "Sredinom", "english": "The title means through the middle."},
                {"bosnian": "Dino Merlin", "english": "The singer's name is Dino Merlin."},
            ],
            teacher_note="Success means catching an anchor word in natural music, not decoding the whole song.",
        ),
        speak_targets=[0, 3, 6],
        can_do_checks=[
            {"id": "cd1", "kind": "speak", "prompt": "I can say one complete sentence with volim, želim, or imam."},
            {"id": "cd2", "kind": "speak", "prompt": "I can ask a weather, invitation, or origin question aloud."},
            {"id": "cd3", "kind": "listen", "prompt": "I can identify the topic of a familiar short exchange."},
            {"id": "cd4", "kind": "listen", "prompt": "I can catch at least one familiar word in a Bosnian song."},
            {"id": "cd5", "kind": "write", "prompt": "I can write a two-line exchange using material from two lessons."},
        ],
        section=2,
    )


def build_lesson_15(images: list) -> dict:
    v = [
        vocab("desna", "right", "DEHS-na", "adjective", "Desna ulica vodi do mosta."),
        vocab("lijeva", "left", "LYEH-va", "adjective", "Lijeva strana je uz rijeku."),
        vocab("pravo", "straight ahead", "PRAH-vo", "adverb", "Idite pravo."),
        vocab("skreni", "turn", "SKREH-nee", "informal imperative", "Skreni lijevo."),
        vocab("ulica", "street", "OO-lee-tsa", "noun", "Ova ulica je kratka."),
        vocab("most", "bridge", "mohst", "noun", "Most je blizu."),
        vocab("blizu", "near", "BLEE-zoo", "adverb", "Latinska ćuprija je blizu."),
        vocab("daleko", "far", "DAH-leh-ko", "adverb", "Konjic nije daleko."),
        vocab("ispred", "in front of", "EES-pred", "preposition", "Kafić je ispred mosta."),
        vocab("iza", "behind", "EE-za", "preposition", "Muzej je iza ugla."),
        vocab("idite", "go", "EE-dee-teh", "polite imperative", "Idite pravo, molim vas."),
        vocab("molim vas", "please", "MOH-leem vahs", "polite phrase", "Pomozite mi, molim vas."),
    ]
    grammar = [
        {
            "title": "Skreni and idite",
            "explanation": "Use skreni when you tell one familiar person to turn. Use idite when you address a stranger politely or speak to more than one person. Add a direction word to make the instruction complete.",
            "examples": [
                {"bosnian": "Skreni lijevo.", "english": "Turn left."},
                {"bosnian": "Idite pravo.", "english": "Go straight."},
                {"bosnian": "Idite desno.", "english": "Go right."},
            ],
        },
        {
            "title": "Polite directions with molim vas",
            "explanation": "Molim vas adds please when you speak politely to a stranger or a group. Pair it with the polite imperative idite. A calm tone and the polite form make a direction sound helpful rather than abrupt.",
            "examples": [
                {"bosnian": "Idite pravo, molim vas.", "english": "Go straight, please."},
                {"bosnian": "Skrenite lijevo, molim vas.", "english": "Turn left, please."},
                {"bosnian": "Pomozite mi, molim vas.", "english": "Please help me."},
            ],
        },
        {
            "title": "Locate a landmark",
            "explanation": "Use blizu and daleko to describe distance. Use ispred for in front of and iza for behind. Connect these words to a visible landmark such as a bridge, street, café, or museum.",
            "examples": [
                {"bosnian": "Most je blizu.", "english": "The bridge is near."},
                {"bosnian": "Kafić je ispred mosta.", "english": "The café is in front of the bridge."},
                {"bosnian": "Muzej je iza ugla.", "english": "The museum is behind the corner."},
            ],
        },
    ]
    facts = [
        {
            "title": "Latin Bridge carries layered history",
            "body": "Latin Bridge crosses the Miljacka River in central Sarajevo. A nearby street corner became internationally known after the 1914 assassination of Archduke Franz Ferdinand. The bridge itself has older Ottoman roots and has served ordinary city movement for generations. It is both an everyday crossing and a landmark tied to world history.",
        },
        {
            "title": "Konjic rebuilt an older crossing",
            "body": "The old stone bridge in Konjic crosses the Neretva River. The original Ottoman bridge was destroyed during the Second World War, and a careful reconstruction opened in 2009. Its stone arch again links the two sides of the town center. The restored crossing gives direction practice a second bridge beyond Sarajevo.",
        },
        {
            "title": "Lijeva keeps its full spelling",
            "body": "The Bosnian word for left is lijeva in the feminine form used with strana or ulica. The ije sequence is important in the course spelling. Saying the word slowly helps the middle sound remain audible. Accurate lijeva keeps a left turn from becoming a spelling shortcut.",
        },
    ]
    quiz = [
        quiz_question("q1", "What does pravo mean in a direction?", ["Straight ahead", "Behind", "Near", "Right"], 0, "Pravo means straight ahead in a direction.", "vocabulary"),
        quiz_question("q2", "Which instruction tells one familiar person to turn left?", ["Idite pravo.", "Skreni lijevo.", "Most je blizu.", "Ulica je desna."], 1, "Skreni lijevo tells one familiar person to turn left.", "grammar"),
        quiz_question("q3", "Which word means bridge?", ["ulica", "ispred", "most", "daleko"], 2, "Most means bridge.", "vocabulary"),
        quiz_question("q4", "Which phrase means behind?", ["desna", "blizu", "ispred", "iza"], 3, "Iza means behind.", "vocabulary"),
        quiz_question("q5", "Where is Ana trying to go?", ["She is trying to reach Latin Bridge.", "She is trying to reach Jahorina.", "She is trying to reach Vrelo Bosne.", "She is trying to reach Brčko."], 0, "Ana is trying to reach Latin Bridge.", "dialogue"),
        quiz_question("q6", "Which form is polite or plural?", ["skreni", "idite", "lijeva", "pravo"], 1, "Idite is a polite or plural command form.", "grammar"),
        quiz_question("q7", "Which other bridge appears on a postcard?", ["The bridge at Brčko", "The bridge at Mostar", "The old bridge at Konjic", "The bridge at Doboj"], 2, "The old stone bridge at Konjic appears on the postcard.", "culture"),
        quiz_question("q8", "Why must travelers respect marked mine areas?", ["The signs mark private cafés.", "The paths close for weather.", "The bridges need tickets.", "Landmines can remain lethal for decades."], 3, "Landmines can remain lethal for decades after a war ends.", "culture"),
    ]
    return chapter(
        day=15,
        title="Desna ili lijeva?",
        title_en="Right or left?",
        theme="Directions near Latin Bridge",
        story="Ana gets lost near Latin Bridge and asks for polite directions.",
        goals={
            "vocabulary": [
                "Use right, left, and straight-ahead words to follow a route.",
                "Locate a street, bridge, café, or museum with distance and position words.",
                "Add molim vas when asking a stranger for help.",
            ],
            "grammar": [
                "Use skreni for an informal singular direction.",
                "Use idite and other polite forms with a stranger or group.",
                "Describe landmarks with blizu, daleko, ispred, and iza.",
            ],
            "culture": [
                "Navigate near Latin Bridge in Sarajevo.",
                "Compare Latin Bridge with the old stone bridge in Konjic.",
                "Understand why marked landmine areas still restrict movement.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Two bridges and two city routes",
            "body": "Ana loses her bearings near Latin Bridge, where the Miljacka River bends through central Sarajevo. The stone bridge is easy to recognize, but the streets around it still send her in circles. Emir has also given her a postcard of the old bridge in Konjic, a graceful reconstructed Ottoman crossing over the Neretva. The two bridges belong to different rivers and different city stories. Ana asks a passerby for help with molim vas, then follows pravo, desna, and lijeva carefully. Directions become memorable when a real landmark waits at the end of the route.",
            "imageId": "latin-bridge",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A: Follow the route",
                "body": "Stand at an imaginary street corner near Latin Bridge and listen for three core directions. Pravo sends you straight ahead, desno sends you right, and lijevo sends you left. The vocabulary list gives desna and lijeva because they can describe a feminine noun such as ulica or strana, while the direction phrases use desno and lijevo. Add most and ulica so each instruction points toward something visible. Ana checks every bridge against her Konjic postcard and briefly follows the wrong river. Trace a route with your finger while saying each turn. Movement makes the contrast between right, left, and straight much easier to retain.",
                "tips": [
                    "Keep the full ije spelling in lijeva and lijevo.",
                    "Use pravo when the route continues straight ahead.",
                    "Connect every turn to a visible street or bridge.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B: Ask and answer politely",
                "body": "Use a polite form when you ask a stranger for directions. Begin with Oprostite or Molim vas, then listen for idite, skrenite, blizu, daleko, ispred, or iza. A friend may tell Ana Skreni lijevo, but a passerby can say Idite pravo, molim vas. The difference marks the relationship and number of people, not a different route. Ana repeats each instruction to confirm it before walking away. Courtesy helps the exchange move smoothly. Practice a short exchange in which one person asks for the bridge and another gives two steps. End with Hvala so the interaction sounds complete and courteous in a real Sarajevo street.",
                "tips": [
                    "Use idite or skrenite when you address a stranger politely.",
                    "Repeat the route in your own words before you begin walking.",
                    "Finish a request for help with molim vas and a response with hvala.",
                ],
            },
        ],
        conversation={
            "title": "Gdje je Latinska ćuprija?",
            "setting": "Ana stands at the wrong corner near the Miljacka River and asks a passerby for help.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Oprostite, gdje je Latinska ćuprija, molim vas?", "english": "Excuse me, where is Latin Bridge, please?"},
                {"speaker": "Emir", "bosnian": "Idite pravo do ulice.", "english": "Go straight to the street."},
                {"speaker": "Ana", "bosnian": "Onda desno ili lijevo?", "english": "Then should I go right or left?"},
                {"speaker": "Emir", "bosnian": "Skrenite lijevo. Most je blizu.", "english": "Turn left. The bridge is near."},
                {"speaker": "Ana", "bosnian": "Je li muzej ispred mosta?", "english": "Is the museum in front of the bridge?"},
                {"speaker": "Emir", "bosnian": "Muzej je iza vas, a most je ispred vas.", "english": "The museum is behind you, and the bridge is in front of you."},
                {"speaker": "Narrator", "bosnian": "Ana zahvaljuje i konačno ide prema pravom mostu.", "english": "Ana says thank you and finally walks toward the correct bridge."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match direction words",
                "prompt": "Match each Bosnian direction word with its English meaning.",
                "items": [
                    {"left": "desna", "right": "right"},
                    {"left": "lijeva", "right": "left"},
                    {"left": "pravo", "right": "straight ahead"},
                    {"left": "ispred", "right": "in front of"},
                    {"left": "iza", "right": "behind"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about directions",
                "prompt": "Decide whether each sentence correctly describes Lesson 15.",
                "items": [
                    {"statement": "Idite can be a polite or plural command.", "answer": True},
                    {"statement": "Daleko means near.", "answer": False},
                    {"statement": "Ana is looking for Latin Bridge.", "answer": True},
                    {"statement": "The postcard bridge is in Mostar.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian instruction that tells one familiar person to turn left.", "hint": "Use skreni and lijevo.", "answer": "Skreni lijevo."},
            {"id": "pr2", "prompt": "Write the polite Bosnian instruction for Go straight.", "hint": "Begin with Idite.", "answer": "Idite pravo."},
            {"id": "pr3", "prompt": "Write the Bosnian sentence for The bridge is near.", "hint": "Use most and blizu.", "answer": "Most je blizu."},
            {"id": "pr4", "prompt": "Write the Bosnian phrase for in front of.", "hint": "The word begins with isp.", "answer": "ispred"},
            {"id": "pr5", "prompt": "Write the Bosnian phrase for behind.", "hint": "The word begins with i.", "answer": "iza"},
            {"id": "pr6", "prompt": "Write the polite Bosnian phrase for please.", "hint": "The second word is vas.", "answer": "molim vas"},
            {"id": "pr7", "prompt": "Write the Bosnian word for street.", "hint": "The word begins with ul.", "answer": "ulica"},
        ],
        facts=facts,
        resources=[
            {"label": "How To Speak Bosnian Directions", "url": "https://www.youtube.com/watch?v=sWbg301Ujjg", "note": "This speaker resource reinforces street direction phrases."},
            {"label": "Book 1 curriculum", "url": "/learn", "note": "The curriculum page lists every Book 1 lesson."},
            {"label": "Return to Lesson 14", "url": "/learn/lesson/14", "note": "Lesson 14 reviews the language that leads into this section."},
        ],
        quiz=quiz,
        images=images,
        civic={
            "title": "Landmines still restrict safe movement",
            "body": "Landmines and other unexploded ordnance still restrict movement in parts of Bosnia and Herzegovina. Mines were placed around former front lines, roads, fields, and settlements during the war, and floods or erosion can shift dangerous devices from recorded locations. Clearance teams have removed many hazards, but the work is slow, technical, and expensive. Residents and hikers must obey warning signs, stay on known routes, and never enter a marked area. A direction is therefore a safety instruction when contaminated land remains nearby.",
            "imageId": "civic-mines",
            "learnMore": {"label": "Wikipedia article about landmines in Bosnia and Herzegovina", "url": "https://en.wikipedia.org/wiki/Land_mines_in_Bosnia_and_Herzegovina"},
        },
        listen=authentic_listen(
            title="Čuj Bosnu with street directions",
            kind="speaker",
            hook="A Bosnian teacher models direction language in a voice outside the story cast.",
            source_title="HOW TO SPEAK BOSNIAN Lesson Directions",
            artist="How To Speak Bosnian",
            scene="Street directions lesson",
            credit="How To Speak Bosnian on YouTube",
            url="https://www.youtube.com/watch?v=sWbg301Ujjg",
            prompt="Listen for right, left, or straight ahead in the speaker's route.",
            gist_prompt="What is the speaker mainly teaching?",
            gist_options=["Food orders", "Street directions", "Weather reports", "Language names"],
            gist_index=1,
            target_words=["desno", "lijevo", "pravo"],
            notice="Listen for the direction word at the end of each short command.",
            key_lines=[
                {"bosnian": "Skreni lijevo.", "english": "Turn left."},
                {"bosnian": "Idite pravo.", "english": "Go straight."},
            ],
            teacher_note="Point in the matching direction as soon as you hear each target word.",
        ),
        speak_targets=[0, 2, 3],
        section=3,
    )


VIDEO_11 = """
# Lesson 11 video script for Kakvo je vrijeme?
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 11: How is the weather?
- BS: Kakvo je vrijeme?
- Background: The cable car climbs Trebević in autumn.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 11 is Kakvo je vrijeme? Ana and Emir plan an autumn picnic on Trebević, but the mountain has another forecast.
**On screen:** Kakvo je vrijeme? | Lesson 11

### 0:40 Goals
**Narration:** In this lesson, you learn weather words, the four seasons, and short reports with je and pada.
**On screen:** vrijeme | seasons | Hladno je | Pada kiša

### 1:30 Culture hook
**Narration:** The cable car rises from the Sarajevo basin into the forest of Trebević. A Jahorina postcard shows how another nearby mountain changes from green trails to winter snow.
**On screen:** Trebević | Jahorina | image credits

### 3:00 Lesson A: Weather and season words
**Narration:** Say vrijeme, sunce, kiša, snijeg, and vjetar. Then say proljeće, ljeto, jesen, and zima. Use a complete sentence for every condition.
**On screen:** sunce | kiša | snijeg | vjetar

### 5:00 Lesson B: Report a changing forecast
**Narration:** Ask Kakvo je vrijeme? Answer Hladno je, Toplo je, or Oblačno je. Say Pada kiša when rain begins and Pada snijeg when snow begins.
**On screen:** Kakvo je vrijeme? | Oblačno je | Pada kiša

### 6:30 Mini dialogue
**Narration:** Ana calls the weather warm just before the clouds arrive. Repeat the dialogue and listen for the moment when the picnic plan changes.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and give a three-sentence forecast for the image. Continue with Lesson 12, Idemo u park.
**On screen:** Practice the forecast | Next lesson is Idemo u park.

## End screen
- Link to website `/learn/lesson/11`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_12 = """
# Lesson 12 video script for Idemo u park
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 12: Let's go to the park
- BS: Idemo u park
- Background: Water and trees at Vrelo Bosne.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 12 is Idemo u park. Ana brings Mrvica to Vrelo Bosne, and one small leash creates a very large problem.
**On screen:** Idemo u park | Lesson 12

### 0:40 Goals
**Narration:** In this lesson, you learn movement verbs, friendly invitations, and commands that might persuade a cat to wait.
**On screen:** idem | idemo | Hajde da | Čekaj

### 1:30 Culture hook
**Narration:** Vrelo Bosne lies near Ilidža at the foot of Mount Igman. Clear springs gather here and begin the Bosna River.
**On screen:** Vrelo Bosne | Ilidža | image credits

### 3:00 Lesson A: Go for a walk
**Narration:** Use idem for yourself, ideš for one person you address, and idemo for the group. Add u park when the park is your destination.
**On screen:** Idem u park. | Ideš li? | Idemo.

### 5:00 Lesson B: Invite and respond
**Narration:** Say Hajde da idemo when you suggest going together. Ask Hoćeš li šetati? when you want to offer a walk.
**On screen:** Hajde da idemo. | Hoćeš li šetati?

### 6:30 Mini dialogue
**Narration:** Mrvica chooses brzo instead of polako and wraps the leash around a tree. Repeat Ana's commands with a friendly but clear voice.
**On screen:** Polako! | Čekaj! | Dialogue lines appear in two languages.

### 8:00 Practice prompt
**Narration:** Pause and invite someone to walk, accept the invitation, and say where you are going. Continue with Lesson 13, Ljudi iz BiH.
**On screen:** Practice an invitation | Next lesson is Ljudi iz BiH.

## End screen
- Link to website `/learn/lesson/12`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_13 = """
# Lesson 13 video script for Ljudi iz BiH
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 13: People from Bosnia and Herzegovina
- BS: Ljudi iz BiH
- Background: The promenade beside the Sava in Brčko.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 13 is Ljudi iz BiH. Ana and Emir share kahva and begin a gentle conversation about place and language.
**On screen:** Ljudi iz BiH | Lesson 13

### 0:40 Goals
**Narration:** In this lesson, you learn to say which language you speak, ask where someone is from, and listen without forcing a label.
**On screen:** Govorim bosanski. | Odakle si? | Ko?

### 1:30 Culture hook
**Narration:** Emir's postcards show Brčko on the Sava River. Its promenade, mosque, and distinct civic position widen Ana's map of the country.
**On screen:** Brčko | Sava River | image credits

### 3:00 Lesson A: Ask about place and language
**Narration:** Ask Odakle si? Answer Ja sam iz and add a place. Say Govorim bosanski or Govorim engleski to name a language you speak.
**On screen:** Odakle si? | Ja sam iz... | Govorim...

### 5:00 Lesson B: Talk about people with care
**Narration:** People in Bosnia and Herzegovina use many names for themselves. Begin with place and language, respect the answer, and let the other person choose how much to share.
**On screen:** Place | Language | Listen with respect

### 6:30 Mini dialogue
**Narration:** Ana says she is from America and is learning Bosnian. Repeat the exchange, then answer the same questions with information that is true for you.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and make a two-line introduction with a place and a language. Continue with Lesson 14, Ponavljanje.
**On screen:** Practice an introduction | Next lesson is Ponavljanje.

## End screen
- Link to website `/learn/lesson/13`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_14 = """
# Lesson 14 video script for Ponavljanje
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 14: Review
- BS: Ponavljanje
- Background: Kastel Fortress beside the Vrbas in Banja Luka.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 14 is Ponavljanje. Board-game night at Amira's turns six lessons into one contest, and Mrvica intends to win.
**On screen:** Ponavljanje | Lesson 14

### 0:40 Goals
**Narration:** In this lesson, you reuse food, shopping, room, weather, invitation, and identity language in complete sentences.
**On screen:** volim | želim | imam | govorim

### 1:30 Culture hook
**Narration:** Postcards bring Banja Luka to the game table. Kastel stands beside the Vrbas, and the reconstructed Ferhadija Mosque carries both living worship and restored memory.
**On screen:** Banja Luka | Kastel | Ferhadija | image credits

### 3:00 Lesson A: Build with familiar verbs
**Narration:** Use volim for a preference, želim for a wish, imam for possession, and govorim for a language. Draw a card and say one complete sentence.
**On screen:** Volim... | Želim... | Imam... | Govorim...

### 5:00 Lesson B: Connect questions across lessons
**Narration:** Switch between Koliko košta?, Kakvo je vrijeme?, Hoćeš li šetati?, and Odakle si? Listen to the question before you choose your answer.
**On screen:** Price | Weather | Invitation | Place

### 6:30 Mini dialogue
**Narration:** Ana and Emir answer their cards, but Mrvica pushes a game piece across the finish. Repeat the exchange and ask for one more round.
**On screen:** Još jednom. | Dialogue lines appear in two languages.

### 8:00 Practice prompt
**Narration:** Pause and combine material from two different lessons in one short exchange. Continue with Lesson 15, Desna ili lijeva?
**On screen:** Mix two lessons | Next lesson is Desna ili lijeva?

## End screen
- Link to website `/learn/lesson/14`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_15 = """
# Lesson 15 video script for Desna ili lijeva?
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 15: Right or left?
- BS: Desna ili lijeva?
- Background: Latin Bridge crosses the Miljacka in Sarajevo.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 15 is Desna ili lijeva? Ana can see the river, but she still cannot find the correct bridge.
**On screen:** Desna ili lijeva? | Lesson 15

### 0:40 Goals
**Narration:** In this lesson, you learn right, left, and straight ahead, then use polite commands to ask a stranger for help.
**On screen:** desno | lijevo | pravo | molim vas

### 1:30 Culture hook
**Narration:** Latin Bridge anchors the Sarajevo route. A postcard of the reconstructed old stone bridge in Konjic adds a second river crossing without taking the lesson to Mostar.
**On screen:** Latin Bridge | Konjic | image credits

### 3:00 Lesson A: Follow the route
**Narration:** Say pravo for straight ahead. Use desno for a right turn and lijevo for a left turn. Connect each instruction to a street or bridge.
**On screen:** pravo | desno | lijevo

### 5:00 Lesson B: Ask and answer politely
**Narration:** A friend can say Skreni lijevo. A stranger can answer Idite pravo, molim vas. The polite form changes the relationship, not the route.
**On screen:** Skreni lijevo. | Idite pravo, molim vas.

### 6:30 Mini dialogue
**Narration:** Ana asks for Latin Bridge and repeats the route before walking. Point in each direction as you repeat the dialogue.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and give a polite two-step route to a nearby landmark. Then review the section and check what you can now say without notes.
**On screen:** Give a route | Review Lessons 11 through 15.

## End screen
- Link to website `/learn/lesson/15`
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
            allowed_title = dotted == "lesson13.title" and value == "Ljudi iz BiH"
            if not image_metadata and ("—" in value or "–" in value):
                issues.append((dotted, "contains a prohibited dash"))
            if not image_metadata and re.search(r"\bBiH\b", value) and not allowed_title:
                issues.append((dotted, "contains unexplained BiH"))

    for lesson in lessons:
        walk(lesson, [f"lesson{lesson['day']}"])
    for day, video in videos.items():
        if "—" in video or "–" in video:
            issues.append((f"video{day}", "contains a prohibited dash"))
        cleaned = video.replace("Ljudi iz BiH", "")
        if re.search(r"\bBiH\b", cleaned):
            issues.append((f"video{day}", "contains unexplained BiH"))
    if issues:
        for path, message in issues:
            print("validation issue", path, message)
    else:
        print("validation passed with no prohibited learner strings")
    return len(issues)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Lesson 11 images")
    imgs11 = [
        img_try("trebevic-cable", "A cable car climbs Trebević above Sarajevo.", "day-11-trebevic-cable.png", ["File:Trebević Cable Car in Sarajevo 01.jpg", "File:Sarajevo cable car.jpg"]),
        img_try("trebevic-view", "Sarajevo appears below the Trebević cable car.", "day-11-trebevic-view.png", ["File:Sarajevo from the cable car.jpg", "File:Sarajevo cable car.jpg"]),
        img_try("jahorina", "Jahorina mountain rises under a broad sky.", "day-11-jahorina.png", ["File:Jahorina mountain 2018.jpg", "File:Planina Jahorina.jpg"]),
        img_try("civic-sarajevo-bowl", "The Sarajevo basin lies between surrounding mountains.", "day-11-civic-sarajevo-bowl.png", ["File:Sarajevo – Cable Car and bypass.jpg", "File:Sarajevo from the cable car.jpg"]),
    ]
    print("Downloading Lesson 12 images")
    imgs12 = [
        img_try("vrelo-bosne", "Water flows through the green spring area at Vrelo Bosne.", "day-12-vrelo-bosne.png", ["File:Vrelo Bosne, Sarajevo.jpg", "File:Vrelo Bosne (1).jpg"]),
        img_try("vrelo-park", "A wooded path crosses Vrelo Bosne Park.", "day-12-vrelo-park.png", ["File:Vrelo Bosne Park in Sarajevo.JPG", "File:Vrelo Bosne (1).jpg"]),
        img_try("bosna-river", "The Bosna River begins among channels at Vrelo Bosne.", "day-12-bosna-river.png", ["File:River Bosna at Vrelo Bosne Park in Sarajevo.JPG", "File:Vrelo Bosne, Sarajevo.jpg"]),
        img_try("civic-floods", "Floodwater covers a community during the 2014 floods.", "day-12-civic-floods.png", ["File:2014 floods in Bosnia.jpg", "File:Maglaj 2014.jpg", "File:Bosnia and Herzegovina floods 2014.jpg", "File:Floods in Doboj 2014.jpg", "File:Floods in Bosnia Doboj 2.jpg", "File:Floods in Bosnia Doboj.jpg"]),
    ]
    print("Downloading Lesson 13 images")
    imgs13 = [
        img_try("brcko-promenade", "People walk along the promenade in Brčko.", "day-13-brcko-promenade.png", ["File:Brčansko šetalište.jpg", "File:Brčko.jpg"]),
        img_try("brcko-mosque", "The white mosque stands in Brčko.", "day-13-brcko-mosque.png", ["File:Bijela džamija Brčko2.jpg", "File:Brčko.jpg"]),
        img_try("brcko-city", "Lights shine across Brčko at night.", "day-13-brcko-city.png", ["File:Brčko.jpg", "File:Brčko noću.jpg"]),
        img_try("civic-brcko-map", "A map marks Brčko District within Bosnia and Herzegovina.", "day-13-civic-brcko-map.png", ["File:Brcko District in Bosnia and Herzegovina.svg"]),
    ]
    print("Downloading Lesson 14 images")
    imgs14 = [
        img_try("kastel", "Kastel Fortress stands beside the Vrbas in Banja Luka.", "day-14-kastel.png", ["File:Tvrđava Kastel Banja Luka.jpg"]),
        img_try("ferhadija", "Ferhadija Mosque rises in Banja Luka.", "day-14-ferhadija.png", ["File:NKD138 Ferhadija Dzamija 1.jpg", "File:Ferhadija (Banja Luka) 2.jpg"]),
        img_try("vrbas", "The Vrbas River flows through Banja Luka.", "day-14-vrbas.png", ["File:Vrbas Banja Luka.jpg", "File:River Vrbas in Banja Luka.jpg", "File:Vrbas from Kastel Banja Luka 2019.jpg"]),
        img_try("civic-emigration", "Travelers move through Sarajevo International Airport.", "day-14-civic-emigration.png", ["File:Sarajevo International Airport.jpg", "File:Bus station Banja Luka.jpg", "File:Sarajevo International Airport (SJJ).jpg"]),
    ]
    print("Downloading Lesson 15 images")
    imgs15 = [
        img_try("latin-bridge", "Latin Bridge crosses the Miljacka River in Sarajevo.", "day-15-latin-bridge.png", ["File:Latin Bridge in Sarajevo.jpg", "File:LatinBridgeSarajevo.JPG"]),
        img_try("latin-bridge-2", "The stone arches of Latin Bridge span the river.", "day-15-latin-bridge-2.png", ["File:LatinBridgeSarajevo.JPG", "File:The Latin Bridge, Sarajevo.jpg"]),
        img_try("konjic-bridge", "The old stone bridge crosses the Neretva in Konjic.", "day-15-konjic-bridge.png", ["File:Konjic Stari most 7.jpg"]),
        img_try("civic-mines", "A warning sign marks landmine danger.", "day-15-civic-mines.png", ["File:Landmine warning sign in BiH.jpg"]),
    ]

    lessons = [
        build_lesson_11(imgs11),
        build_lesson_12(imgs12),
        build_lesson_13(imgs13),
        build_lesson_14(imgs14),
        build_lesson_15(imgs15),
    ]
    videos = {
        11: VIDEO_11,
        12: VIDEO_12,
        13: VIDEO_13,
        14: VIDEO_14,
        15: VIDEO_15,
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
