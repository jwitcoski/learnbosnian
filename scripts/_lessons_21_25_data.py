"""Lesson data for Book 1 Lessons 21-25. Exports LESSONS and VIDEOS for chapter builder."""
from __future__ import annotations


def vocab(bs: str, en: str, pron: str, pos: str, ex: str) -> dict:
    return {
        "bosnian": bs,
        "english": en,
        "pronunciation": pron,
        "partOfSpeech": pos,
        "example": ex,
    }


def dict_entry(day: int, item: dict) -> dict:
    return {
        "day": day,
        "bosnian": item["bosnian"],
        "english": item["english"],
        "pronunciation": item["pronunciation"],
        "partOfSpeech": item["partOfSpeech"],
        "example": item["example"],
    }


def quiz_question(id_, question, options, correct_index, explanation, skill):
    return {
        "id": id_,
        "question": question,
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


def say_again(lines):
    return {
        "title": "Say again",
        "intro": "Warm up with four frames you already know.",
        "lines": [{"bosnian": bs, "english": en} for bs, en in lines],
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
    civic,
    listen,
    speak_targets,
    section,
    say_again_data,
    image_briefs,
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
        "dictionaryEntries": [dict_entry(day, item) for item in vocabulary],
        "images": [],
        "imagesNeeded": False,
        "imageBriefs": image_briefs,
        "civicContext": civic,
        "authenticListen": listen,
        "speakTargets": speak_targets,
        "section": section,
        "sayAgain": say_again_data,
    }
    if can_do_checks is not None:
        data["canDoChecks"] = can_do_checks
    return data


def build_lesson_21() -> dict:
    v = [
        vocab("idemo", "let us go", "EE-deh-mo", "verb form", "Hajde da idemo."),
        vocab("karta", "ticket or card", "KAR-ta", "noun", "Treba mi karta."),
        vocab("hoću", "I want", "HO-choo", "verb form", "Hoću vikend samo."),
        vocab("često", "often", "CHEH-sto", "adverb", "Često zovem Amiru."),
        vocab("telefon", "telephone", "teh-leh-FON", "noun", "Gdje je telefon?"),
        vocab("vikend", "weekend", "VEE-kend", "noun", "Planiram vikend."),
        vocab("plan", "plan", "plan", "noun", "Imam plan za vikend."),
        vocab("još jednom", "one more time", "yosh YED-nom", "phrase", "Reci još jednom."),
        vocab("autobus", "bus", "OW-toh-boos", "noun", "Autobus ide u Bihać."),
        vocab("račun", "bill", "RAH-choon", "noun", "Račun, molim."),
    ]
    grammar = [
        {
            "title": "Remember Treba mi and Hoću",
            "explanation": (
                "Learn this as a full phrase. Do not treat it as a table. "
                "Treba mi names a need right now. Hoću names a wish. "
                "Keep both chunks in the present and add one familiar object after each verb."
            ),
            "examples": [
                {"bosnian": "Treba mi karta.", "english": "I need a ticket."},
                {"bosnian": "Hoću vikend samo.", "english": "I want a weekend alone."},
                {"bosnian": "Treba mi telefon.", "english": "I need a phone."},
            ],
        },
        {
            "title": "Remember price, place, and weather questions",
            "explanation": (
                "Hold this as a spoken pattern. Do not treat it as a grammar grid. "
                "Koliko košta? asks about price. Gdje je? asks about place. "
                "Kakvo je vrijeme? asks about weather. Choose the question that matches your weekend plan."
            ),
            "examples": [
                {"bosnian": "Koliko košta karta?", "english": "How much does the ticket cost?"},
                {"bosnian": "Gdje je autobus?", "english": "Where is the bus?"},
                {"bosnian": "Kakvo je vrijeme?", "english": "How is the weather?"},
            ],
        },
    ]
    culture_body = (
        "Ana spreads a weekend map beside her coffee and a postcard from Una or Bihać. "
        "The river towns of northwest Bosnia and Herzegovina offer waterfalls, old bridges, and quiet walks that suit a solo traveler. "
        "Jajce appears on another card with its fortress above the Pliva waterfall. "
        "Ana checks the weather, counts her budget, and writes a short plan on a napkin. "
        "A weekend alone still needs polite questions at a café and a ticket counter. "
        "The postcard places turn review frames into a real trip idea beyond Sarajevo."
    )
    block_a = (
        "This review drills frames from Lessons 15 through 20. "
        "Start with Treba mi and Hoću. Say Treba mi karta and Hoću vikend samo as full lines. "
        "Add telefon, plan, and vikend to your weekend story. "
        "Practice Koliko košta? before you buy a bus ticket. "
        "Ana sits at Amira's café with a map and a Una postcard. "
        "She names what she needs and what she wants without opening a new grammar chart. "
        "Repeat each frame još jednom until the need and wish sound automatic."
    )
    block_b = (
        "Now switch among three question frames. "
        "Ask Gdje je autobus? at the station. Ask Kakvo je vrijeme? before a mountain walk. "
        "Finish café talk with Račun, molim when you pay. "
        "Emir and Amira help Ana test her solo plan while Mrvica watches the sugar bowl. "
        "Mix idemo with a place name and često with a habit from earlier lessons. "
        "The review works when you can change frames without English coaching. "
        "Stay in the present tense for every answer."
    )
    civic_body = (
        "Private rural bus lines across Bosnia and Herzegovina often shut down when routes stop paying. "
        "Villages that once relied on minibuses can lose reliable public transport without a replacement. "
        "Ana reads a news note about canceled mountain lines while she plans a weekend ticket. "
        "A solo trip still depends on roads and buses that do not reach every community. "
        "Transport gaps show how market pressure can leave rural residents stranded."
    )
    return chapter(
        day=21,
        title="Ponavljanje",
        title_en="Review",
        theme="Ana plans a solo weekend",
        story="Ana plans a solo weekend and drills frames from Lessons 15 through 20 at Amira's café.",
        goals={
            "vocabulary": [
                "Recycle idemo, karta, hoću, telefon, vikend, and plan for weekend talk.",
                "Reuse često, autobus, račun, and još jednom in café and travel frames.",
            ],
            "grammar": [
                "Drill Treba mi and Hoću as present need and wish chunks.",
                "Switch among Koliko košta?, Gdje je?, and Kakvo je vrijeme?",
            ],
            "culture": [
                "Plan a solo weekend with postcards from Una, Bihać, or Jajce.",
                "Treat review as frame practice rather than a new grammar system.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Weekend planning with northwest postcards",
            "body": culture_body,
            "imageId": "una-postcard",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A. Drill need and wish frames",
                "body": block_a,
                "tips": [
                    "Keep Treba mi and Hoću with the object in one breath.",
                    "Say each frame još jednom before you switch to a question.",
                    "Stay in present tense for every weekend line.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B. Switch travel questions at the café",
                "body": block_b,
                "tips": [
                    "Hear the question word before you choose your answer.",
                    "Add molim or hvala in every shop and café exchange.",
                    "Mix two old topics when one frame feels too easy.",
                ],
            },
        ],
        conversation={
            "title": "Plan za vikend",
            "setting": "Ana, Emir, and Amira sit at a café table with a map, postcards, and one curious cat.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Imam plan za vikend. Hoću ići sama.", "english": "I have a plan for the weekend. I want to go alone."},
                {"speaker": "Emir", "bosnian": "Treba ti karta i dobar telefon.", "english": "You need a ticket and a good phone."},
                {"speaker": "Amira", "bosnian": "Pogledaj ovu kartu. Una je lijepa.", "english": "Look at this card. Una is beautiful."},
                {"speaker": "Mrvica", "bosnian": "Mjau! Ja ostajem ovdje.", "english": "Meow! I am staying here."},
                {"speaker": "Ana", "bosnian": "Kakvo je vrijeme za planinu?", "english": "How is the weather for the mountains?"},
                {"speaker": "Emir", "bosnian": "Često je hladno. Gdje je autobus?", "english": "It is often cold. Where is the bus?"},
                {"speaker": "Amira", "bosnian": "Hajde da idemo sutra. Račun, molim?", "english": "Let us go tomorrow. The bill, please?"},
                {"speaker": "Mrvica", "bosnian": "Mjau! Još jednom kahvu!", "english": "Meow! Coffee one more time!"},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the review frames",
                "prompt": "Match each Bosnian chunk with its English meaning.",
                "items": [
                    {"left": "treba mi", "right": "I need"},
                    {"left": "hoću", "right": "I want"},
                    {"left": "koliko košta", "right": "how much does it cost"},
                    {"left": "kakvo je vrijeme", "right": "how is the weather"},
                    {"left": "još jednom", "right": "one more time"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false on the weekend review",
                "prompt": "Decide whether each sentence correctly reviews Lessons 15 through 20.",
                "items": [
                    {"statement": "Treba mi karta means I need a ticket.", "answer": True},
                    {"statement": "Kakvo je vrijeme? asks about price.", "answer": False},
                    {"statement": "Gdje je autobus? asks about place.", "answer": True},
                    {"statement": "Račun, molim asks for the bill.", "answer": True},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian chunk for I need a ticket.", "hint": "Begin with Treba mi.", "answer": "Treba mi karta."},
            {"id": "pr2", "prompt": "Write the Bosnian for I want a weekend alone.", "hint": "Use Hoću and vikend.", "answer": "Hoću vikend samo."},
            {"id": "pr3", "prompt": "Write the polite price question for a ticket.", "hint": "Begin with Koliko.", "answer": "Koliko košta karta?"},
            {"id": "pr4", "prompt": "Write the Bosnian question that asks how the weather is.", "hint": "Begin with Kakvo.", "answer": "Kakvo je vrijeme?"},
            {"id": "pr5", "prompt": "Write the Bosnian for Where is the bus?", "hint": "Begin with Gdje je.", "answer": "Gdje je autobus?"},
            {"id": "pr6", "prompt": "Write the Bosnian invitation Let us go.", "hint": "Begin with Hajde da.", "answer": "Hajde da idemo."},
            {"id": "pr7", "prompt": "Write the Bosnian for The bill, please.", "hint": "Use Račun and molim.", "answer": "Račun, molim."},
        ],
        facts=[
            {
                "title": "Una and Bihać suit a quiet weekend",
                "body": "The Una River region in northwest Bosnia and Herzegovina offers green water and old towns like Bihać. A solo traveler can plan walks and river views without a big city crowd. Ana's postcard keeps the place visible while she reviews travel frames.",
            },
            {
                "title": "Jajce adds a waterfall stop",
                "body": "Jajce sits above the Pliva waterfall and often appears on traveler postcards. The fortress and old town give Ana a second weekend option beyond the Una valley. Place names turn review vocabulary into real destinations.",
            },
            {
                "title": "Treba mi stays a survival chunk",
                "body": "Treba mi plus a noun is one of the fastest ways to name a need at a counter. You do not need a full conjugation chart to buy a bus ticket. Pair the chunk with molim and you sound ready for travel talk.",
            },
            {
                "title": "Solo weekends still need polite frames",
                "body": "Traveling alone does not mean traveling without manners. Račun, molim and hvala keep café and ticket talk friendly. Book 1 stays practical by mixing need, wish, and polite questions in one review night.",
            },
        ],
        resources=[
            {"label": "Learn Bosnian: Telling Time", "url": "https://www.youtube.com/watch?v=0xiYbtHQaDc", "note": "Clock phrases help you read weekend departure boards."},
            {"label": "Next lesson", "url": "/learn/lesson/22", "note": "Lesson 22 walks Travnik with sightseeing chunks."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the review."},
        ],
        quiz=[
            quiz_question("q1", "What does hoću express in weekend planning?", ["I want", "I need", "I hear", "I pay"], 0, "Hoću means I want.", "grammar"),
            quiz_question("q2", "Which chunk means I need a ticket?", ["Hoću vikend.", "Treba mi karta.", "Kakvo je vrijeme?", "Račun, molim."], 1, "Treba mi karta means I need a ticket.", "grammar"),
            quiz_question("q3", "Which question asks about price?", ["Gdje je autobus?", "Koliko košta karta?", "Kakvo je vrijeme?", "Hajde da idemo."], 1, "Koliko košta karta? asks about price.", "grammar"),
            quiz_question("q4", "Which question asks about weather?", ["Kakvo je vrijeme?", "Koliko košta?", "Gdje je telefon?", "Još jednom."], 0, "Kakvo je vrijeme? asks about weather.", "grammar"),
            quiz_question("q5", "What does vikend mean?", ["weekend", "phone", "bill", "bus"], 0, "Vikend means weekend.", "vocabulary"),
            quiz_question("q6", "Which postcard region does Ana consider?", ["Una or Bihać", "Only Neum beach", "Only Jahorina ski", "Only Mostar bridge"], 0, "Ana considers Una or Bihać for a solo trip.", "culture"),
            quiz_question("q7", "What happens when private rural bus lines shut down?", ["Villages can lose reliable transport", "Tickets become free", "All buses run faster", "Phones stop working"], 0, "Canceled rural lines can strand villages without replacement service.", "culture"),
            quiz_question("q8", "Which line asks for the bill?", ["Račun, molim.", "Treba mi karta.", "Često zovem.", "Imam plan."], 0, "Račun, molim asks for the bill.", "dialogue"),
            quiz_question("q9", "What does još jednom mean?", ["one more time", "every day", "never again", "right now"], 0, "Još jednom means one more time.", "vocabulary"),
            quiz_question("q10", "Who stays at the café while Ana plans to travel?", ["Mrvica", "The bus driver", "A doctor", "A seller in Travnik"], 0, "Mrvica stays at the café in the dialogue.", "dialogue"),
        ],
        civic={
            "title": "Rural bus lines shut down as unprofitable routes",
            "body": civic_body,
            "imageId": "civic-rural-bus",
            "learnMore": {
                "label": "Wikipedia article about transport in Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Transport_in_Bosnia_and_Herzegovina",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with clock phrases for weekend departures",
            kind="speaker",
            hook="A teacher models time phrases you can reuse when you plan a bus trip.",
            source_title="Learn Bosnian: Telling Time (Sati i Minuti)",
            artist="Lingo Hero",
            scene="Clock and schedule language",
            credit="Lingo Hero on YouTube",
            url="https://www.youtube.com/watch?v=0xiYbtHQaDc",
            prompt="Listen for a time phrase you could place beside a weekend departure.",
            gist_prompt="What is the speaker mainly teaching?",
            gist_options=["Telling time and clock language", "Football rules", "Holiday greetings", "Phone emergencies"],
            gist_index=0,
            target_words=["sati", "koliko"],
            notice="You do not need every number. Catch the question shape for time.",
            key_lines=[
                {"bosnian": "Koliko je sati?", "english": "What time is it?"},
                {"bosnian": "Hajde da idemo.", "english": "Let us go."},
            ],
            teacher_note="After the clip, say one weekend plan line with a time you know.",
        ),
        speak_targets=[0, 4, 6],
        section=3,
        say_again_data=say_again([
            ("Treba mi karta.", "I need a ticket."),
            ("Koliko košta karta?", "How much does the ticket cost?"),
            ("Kakvo je vrijeme?", "How is the weather?"),
            ("Račun, molim.", "The bill, please."),
        ]),
        image_briefs=[
            "weekend-map: Ana spreads a map for solo weekend planning",
            "una-postcard: Postcard of Una River or Bihać for culture hero",
            "cafe-plan: Café table with weekend plan notes and coffee",
            "civic-rural-bus: Rural minibus on a mountain road for civic panel",
        ],
        can_do_checks=[
            {"id": "cd1", "kind": "speak", "prompt": "I can say Treba mi or Hoću with one familiar object."},
            {"id": "cd2", "kind": "speak", "prompt": "I can ask Koliko košta?, Gdje je?, or Kakvo je vrijeme? aloud."},
            {"id": "cd3", "kind": "listen", "prompt": "I can hear a time phrase in the Čuj Bosnu clip."},
            {"id": "cd4", "kind": "write", "prompt": "I can write a complete weekend plan sentence in the present tense."},
        ],
    )


def build_lesson_22() -> dict:
    v = [
        vocab("vidim", "I see", "VEE-deem", "verb form", "Vidim džamiju."),
        vocab("ovo je", "this is", "OH-vo yeh", "phrase", "Ovo je stari grad."),
        vocab("tamo je", "there is or it is there", "TA-mo yeh", "phrase", "Tamo je kula."),
        vocab("džamija", "mosque", "JAH-mee-ya", "noun", "Ovo je džamija."),
        vocab("kula", "tower", "KOO-la", "noun", "Tamo je kula."),
        vocab("šetamo", "we walk", "SHEH-ta-mo", "verb form", "Šetamo kroz grad."),
        vocab("grad", "town or city", "grad", "noun", "Travnik je lijep grad."),
        vocab("stari", "old", "STAH-ree", "adjective", "Stari grad je blizu."),
        vocab("ulica", "street", "OO-lee-tsa", "noun", "Ulica je uska."),
        vocab("pogled", "view", "POH-gled", "noun", "Pogled je lijep."),
        vocab("Sulejmanija", "Sulejmanija Mosque", "soo-leh-MAH-nee-ya", "proper noun", "Ovo je Sulejmanija."),
        vocab("Travnik", "Travnik", "TRAV-neek", "proper noun", "Danas smo u Travniku."),
        vocab("vizir", "vizier", "VEE-zeer", "noun", "Travnik je grad vizira."),
        vocab("šetam", "I walk", "SHEH-tam", "verb form", "Šetam uz zid."),
    ]
    grammar = [
        {
            "title": "Vidim and ovo je for what you see",
            "explanation": (
                "Treat this as a ready chunk you can say today. "
                "Vidim means I see. Ovo je means this is. "
                "Point at a building and name it in one short present-tense line."
            ),
            "examples": [
                {"bosnian": "Vidim džamiju.", "english": "I see a mosque."},
                {"bosnian": "Ovo je Sulejmanija.", "english": "This is Sulejmanija."},
                {"bosnian": "Ovo je stari grad.", "english": "This is the old town."},
            ],
        },
        {
            "title": "Tamo je and šetamo for place talk",
            "explanation": (
                "Learn the usable chunk first. Full tables can wait. "
                "Tamo je points to something farther away. Šetamo means we walk. "
                "Use both chunks while you move through a town in the present."
            ),
            "examples": [
                {"bosnian": "Tamo je kula.", "english": "There is a tower."},
                {"bosnian": "Šetamo kroz grad.", "english": "We walk through the town."},
                {"bosnian": "Danas smo u Travniku.", "english": "Today we are in Travnik."},
            ],
        },
        {
            "title": "Naming landmarks in the present",
            "explanation": (
                "Take this as a speaking chunk. Do not memorize a case chart yet. "
                "Combine vidim, ovo je, and tamo je with džamija, kula, and grad. "
                "Keep every sightseeing line in the present tense."
            ),
            "examples": [
                {"bosnian": "Vidim kulu.", "english": "I see a tower."},
                {"bosnian": "Ovo je džamija.", "english": "This is a mosque."},
                {"bosnian": "Pogled je lijep.", "english": "The view is beautiful."},
            ],
        },
    ]
    culture_body = (
        "Travnik was once the seat of Ottoman viziers in central Bosnia and Herzegovina. "
        "The old town climbs a hillside above the Plava Voda spring and keeps narrow streets full of color. "
        "Sulejmanija Mosque stands with painted details that travelers photograph from every angle. "
        "Ana and Emir walk the stone lanes and name what they see in short present-tense lines. "
        "A vizier town feels like a living museum where every corner offers a new view. "
        "Travnik rewards slow walking and polite greetings with locals."
    )
    block_a = (
        "Start with vidim and ovo je. Point at Sulejmanija and say Ovo je Sulejmanija. "
        "Add džamija, kula, and stari grad as landmark nouns you can name today. "
        "Practice Vidim džamiju and Ovo je stari grad while you stand on a real or imagined corner. "
        "Ana walks beside Emir and tests each chunk before she takes a photo. "
        "Keep every sentence in the present tense. "
        "Sightseeing works best when you say the whole line together rather than hunting for a case ending."
    )
    block_b = (
        "Move with tamo je and šetamo. Say Tamo je kula when the tower sits uphill. "
        "Invite a friend with Hajde da šetamo kroz grad. "
        "Amira joins by phone and asks what Ana sees right now. "
        "A passerby in Travnik points toward the old walls with a short polite answer. "
        "Mix ulica and pogled when you describe the walk. "
        "End with one postcard line that names Travnik as a vizier town."
    )
    civic_body = (
        "Winding mountain roads across Bosnia and Herzegovina combine sharp curves with fast local driving. "
        "Teenage drivers on rural routes add risk on roads that already climb steep hills. "
        "Traffic accident rates in the country remain among the highest in Europe. "
        "Ana notices guardrails and tight turns on the road into Travnik. "
        "Road safety is a daily civic pressure for anyone who travels by car or bus."
    )
    return chapter(
        day=22,
        title="Danas u Travniku",
        title_en="Today in Travnik",
        theme="Day trip to Travnik in the present",
        story="Ana and Emir walk Travnik and name what they see while Amira calls from the café.",
        goals={
            "vocabulary": [
                "Name mosques, towers, streets, and views with vidim, ovo je, and tamo je.",
                "Use šetamo and Travnik landmark words in present-tense sightseeing talk.",
            ],
            "grammar": [
                "Point and name with vidim and ovo je.",
                "Place distant sights with tamo je and move with šetamo.",
            ],
            "culture": [
                "Visit Travnik as a historic vizier town with colorful Sulejmanija Mosque.",
                "Walk the old town and describe what you see in short present lines.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Travnik as a vizier town with colorful mosque",
            "body": culture_body,
            "imageId": "travnik-mosque",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A. Point and name what you see",
                "body": block_a,
                "tips": [
                    "Point at a photo while you say ovo je.",
                    "Keep vidim and the landmark in one short line.",
                    "Stay in present tense for every sightseeing sentence.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B. Walk the old town together",
                "body": block_b,
                "tips": [
                    "Use tamo je when the sight sits farther uphill.",
                    "Invite a friend with Hajde da šetamo.",
                    "Add molim or hvala when a passerby helps you.",
                ],
            },
        ],
        conversation={
            "title": "Šetnja kroz Travnik",
            "setting": "Ana and Emir walk Travnik's old town while Amira listens on the phone and a passerby points the way.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Ovo je Sulejmanija. Vidim lijepu džamiju.", "english": "This is Sulejmanija. I see a beautiful mosque."},
                {"speaker": "Emir", "bosnian": "Da. Tamo je kula iznad grada.", "english": "Yes. There is a tower above the town."},
                {"speaker": "Amira", "bosnian": "Alo? Šta vidite sada?", "english": "Hello? What do you see now?"},
                {"speaker": "Passerby", "bosnian": "Stari grad je blizu. Šetajte pravo.", "english": "The old town is nearby. Walk straight."},
                {"speaker": "Ana", "bosnian": "Hvala! Šetamo kroz usku ulicu.", "english": "Thank you! We walk through a narrow street."},
                {"speaker": "Emir", "bosnian": "Pogled je prekrasan. Ovo je grad vizira.", "english": "The view is wonderful. This is a vizier town."},
                {"speaker": "Amira", "bosnian": "Pošaljite mi kartu iz Travnika.", "english": "Send me a card from Travnik."},
                {"speaker": "Passerby", "bosnian": "Dobar dan. Uživajte u šetnji.", "english": "Good day. Enjoy the walk."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the sightseeing chunks",
                "prompt": "Match each Bosnian chunk with its English meaning.",
                "items": [
                    {"left": "vidim", "right": "I see"},
                    {"left": "ovo je", "right": "this is"},
                    {"left": "tamo je", "right": "there is"},
                    {"left": "džamija", "right": "mosque"},
                    {"left": "kula", "right": "tower"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false in Travnik",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Ovo je means this is.", "answer": True},
                    {"statement": "Šetamo means we walk.", "answer": True},
                    {"statement": "Travnik was never a vizier town.", "answer": False},
                    {"statement": "Sulejmanija is a mosque in Travnik.", "answer": True},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian for I see a mosque.", "hint": "Begin with Vidim.", "answer": "Vidim džamiju."},
            {"id": "pr2", "prompt": "Write the Bosnian for This is Sulejmanija.", "hint": "Use Ovo je.", "answer": "Ovo je Sulejmanija."},
            {"id": "pr3", "prompt": "Write the Bosnian for There is a tower.", "hint": "Begin with Tamo je.", "answer": "Tamo je kula."},
            {"id": "pr4", "prompt": "Write the Bosnian for We walk through the town.", "hint": "Use Šetamo and kroz grad.", "answer": "Šetamo kroz grad."},
            {"id": "pr5", "prompt": "Write the Bosnian for Today we are in Travnik.", "hint": "Begin with Danas smo u.", "answer": "Danas smo u Travniku."},
            {"id": "pr6", "prompt": "Write the Bosnian word for street.", "hint": "It begins with uli.", "answer": "ulica"},
            {"id": "pr7", "prompt": "Write the Bosnian for The view is beautiful.", "hint": "Use Pogled je lijep.", "answer": "Pogled je lijep."},
        ],
        facts=[
            {
                "title": "Travnik was a vizier seat",
                "body": "Ottoman viziers once governed from Travnik in central Bosnia and Herzegovina. The town keeps that history in its old walls and titles. Learners hear vizir as a cultural keyword rather than a grammar item.",
            },
            {
                "title": "Sulejmanija stands out for color",
                "body": "Sulejmanija Mosque is famous for painted details that catch the eye on a hillside walk. Ana names it with ovo je before she takes a photo. Colorful mosques make present-tense sightseeing memorable.",
            },
            {
                "title": "Ovo je works like a pointing finger",
                "body": "Ovo je plus a landmark is the fastest way to name what stands in front of you. You do not need a full case chart to start a Travnik walk. Point, name, and keep moving.",
            },
            {
                "title": "Mountain roads need careful driving",
                "body": "Roads into towns like Travnik often wind through hills. Fast driving on curves raises accident risk across the country. Travelers notice guardrails and tight turns on the way in.",
            },
        ],
        resources=[
            {"label": "Bosnian Coffee with local guides", "url": "https://www.youtube.com/watch?v=wFGbkVzNCFU", "note": "Café hospitality speech supports polite town greetings."},
            {"label": "Next lesson", "url": "/learn/lesson/23", "note": "Lesson 23 asks what people do today."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after Travnik."},
        ],
        quiz=[
            quiz_question("q1", "What does vidim mean?", ["I see", "I walk", "I want", "I need"], 0, "Vidim means I see.", "vocabulary"),
            quiz_question("q2", "Which phrase means this is?", ["tamo je", "ovo je", "šetamo", "hvala"], 1, "Ovo je means this is.", "grammar"),
            quiz_question("q3", "Which landmark is in Travnik?", ["Sulejmanija Mosque", "Stari Most in Mostar", "Neum beach only", "Bilino Polje stadium"], 0, "Sulejmanija Mosque is in Travnik.", "culture"),
            quiz_question("q4", "What does šetamo mean?", ["we walk", "I see", "this is", "goodbye"], 0, "Šetamo means we walk.", "vocabulary"),
            quiz_question("q5", "Why are traffic accident rates high on mountain roads?", ["Winding roads and fast driving add risk", "There are no cars in Bosnia and Herzegovina", "All roads are straight highways", "Buses never use mountain routes"], 0, "Winding roads and fast local driving raise accident risk.", "culture"),
            quiz_question("q6", "Which line points to a distant tower?", ["Tamo je kula.", "Ovo je kula.", "Račun, molim.", "Koliko košta?"], 0, "Tamo je kula points to a distant tower.", "grammar"),
            quiz_question("q7", "What was Travnik known for historically?", ["A vizier seat", "A coastal port", "An airport hub", "A ski jump only"], 0, "Travnik was known as a vizier town.", "culture"),
            quiz_question("q8", "Who asks what Ana and Emir see on the phone?", ["Amira", "Mrvica", "A doctor", "A bus clerk"], 0, "Amira asks what they see during the call.", "dialogue"),
            quiz_question("q9", "What does džamija mean?", ["mosque", "tower", "street", "view"], 0, "Džamija means mosque.", "vocabulary"),
        ],
        civic={
            "title": "Winding mountain roads and high traffic accident rates",
            "body": civic_body,
            "imageId": "civic-winding-road",
            "learnMore": {
                "label": "Wikipedia article about transport in Bosnia and Herzegovina",
                "url": "https://en.wikipedia.org/wiki/Transport_in_Bosnia_and_Herzegovina",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with café greetings for town walks",
            kind="speaker",
            hook="Local guides model polite greetings you can reuse when a passerby helps you in Travnik.",
            source_title="Bosnian Coffee with Local Guides",
            artist="How to speak Bosnian",
            scene="Café hospitality and greetings",
            credit="How to speak Bosnian on YouTube",
            url="https://www.youtube.com/watch?v=wFGbkVzNCFU",
            prompt="Listen for a greeting or thanks line you could say after a passerby helps you.",
            gist_prompt="What kind of speech does the clip mainly model?",
            gist_options=["Café hospitality and greetings", "Bus ticket prices only", "Ski resort ads only", "Hospital forms only"],
            gist_index=0,
            target_words=["hvala", "dobar"],
            notice="Catch one polite word you can reuse on a town walk.",
            key_lines=[
                {"bosnian": "Dobar dan.", "english": "Good day."},
                {"bosnian": "Hvala!", "english": "Thank you!"},
            ],
            teacher_note="After the clip, greet an imagined passerby and name one landmark with ovo je.",
        ),
        speak_targets=[0, 4, 5],
        section=4,
        say_again_data=say_again([
            ("Gdje je Mostar?", "Where is Mostar?"),
            ("Hajde da idemo.", "Let us go."),
            ("Kakvo je vrijeme?", "How is the weather?"),
            ("Hvala!", "Thank you!"),
        ]),
        image_briefs=[
            "travnik-mosque: Sulejmanija Mosque with colorful details for culture hero",
            "travnik-street: Narrow old-town street in Travnik for mid-lesson scene",
            "travnik-tower: Hilltop tower above Travnik for place beat",
            "civic-winding-road: Winding mountain road with guardrails for civic panel",
        ],
    )


def build_lesson_23() -> dict:
    v = [
        vocab("radim", "I work or I do", "RAH-deem", "verb form", "Radim danas."),
        vocab("radiš", "you work or you do", "RAH-deesh", "verb form", "Šta radiš danas?"),
        vocab("radi", "he or she works", "RAH-dee", "verb form", "Emir radi danas."),
        vocab("šta radiš", "what do you do", "shta RAH-deesh", "phrase", "Šta radiš danas?"),
        vocab("volim da", "I like to", "VOH-leem da", "phrase", "Volim da šetam."),
        vocab("danas", "today", "DAH-nas", "adverb", "Šta radiš danas?"),
        vocab("sada", "now", "SAH-da", "adverb", "Sada radim."),
        vocab("posao", "work or job", "POH-sa-oh", "noun", "Posao je dobar."),
        vocab("škola", "school", "SHKOH-la", "noun", "Idem u školu."),
        vocab("kuhati", "to cook", "koo-HAH-tee", "verb", "Volim da kuhati."),
        vocab("čitati", "to read", "chee-TAH-tee", "verb", "Volim da čitati."),
        vocab("odmor", "rest or break", "OD-mor", "noun", "Trebam odmor."),
        vocab("ritam", "rhythm", "REE-tam", "noun", "Ritam dana je miran."),
        vocab("Zenica", "Zenica", "ZEH-nee-tsa", "proper noun", "Zenica je industrijski grad."),
    ]
    grammar = [
        {
            "title": "Radim, radiš, and radi in the present",
            "explanation": (
                "Say the whole line together. Skip the full chart for now. "
                "Radim means I work or I do. Radiš asks or states what you do. "
                "Radi covers he or she does. Keep all three in the present tense."
            ),
            "examples": [
                {"bosnian": "Radim danas.", "english": "I work today."},
                {"bosnian": "Šta radiš?", "english": "What do you do?"},
                {"bosnian": "Emir radi danas.", "english": "Emir works today."},
            ],
        },
        {
            "title": "Šta radiš? as a daily question",
            "explanation": (
                "Keep this as a sayable line rather than a paradigm list. "
                "Šta radiš? opens talk about today's activity. "
                "Answer with radim plus one verb or place you already know."
            ),
            "examples": [
                {"bosnian": "Šta radiš danas?", "english": "What do you do today?"},
                {"bosnian": "Radim i učim.", "english": "I work and study."},
                {"bosnian": "Sada radim.", "english": "I am working now."},
            ],
        },
        {
            "title": "Volim da plus a light verb",
            "explanation": (
                "Memorize the phrase shape. Leave the full table for later. "
                "Volim da plus a verb names something you like to do. "
                "Use it after you answer šta radiš with a habit you enjoy."
            ),
            "examples": [
                {"bosnian": "Volim da šetam.", "english": "I like to walk."},
                {"bosnian": "Volim da čitam.", "english": "I like to read."},
                {"bosnian": "Volim da kuvam.", "english": "I like to cook."},
            ],
        },
    ]
    culture_body = (
        "After the Travnik trip Ana asks friends what they do on a normal day in Bosnia and Herzegovina. "
        "Morning coffee, work or school, and an evening walk shape a rhythm that feels familiar across towns. "
        "Zenica appears on a postcard from an industrial city on the Bosna River, far from Sarajevo's tourist streets. "
        "Tešanj offers another northern postcard with quiet stone lanes and local crafts. "
        "Daily life is not only sightseeing. "
        "People answer šta radiš? with honest present-tense lines about work, rest, and small pleasures."
    )
    block_a = (
        "Learn radim, radiš, and radi as three present activity chunks. "
        "Ask Šta radiš danas? and answer with one clear verb. "
        "Add danas and sada to keep the talk in the present moment. "
        "Ana meets Emir after Travnik and compares schedules over coffee. "
        "Practice Radim danas and Šta radiš? until the question sounds natural. "
        "Do not open a full conjugation chart. Say the whole line together."
    )
    block_b = (
        "Add volim da plus a light verb for habits you enjoy. "
        "Say Volim da šetam or Volim da čitam after you name today's work. "
        "Amira describes café rhythm while a seller names what he does at the market. "
        "Mix posao, škola, and odmor when you talk about a full day. "
        "Keep public scenes polite with molim and hvala. "
        "End with one postcard line about Zenica or Tešanj to widen the map beyond the capital."
    )
    civic_body = (
        "Bosnia and Herzegovina remains absent from the Eurovision Song Contest because BHRT stays sanctioned by the European Broadcasting Union. "
        "The public broadcaster carries unpaid debt that blocks full membership rights. "
        "Without a settled agreement, the country cannot return to the contest stage. "
        "Ana hears fans discuss the gap while she asks friends about weekend music habits. "
        "A cultural stage abroad can stay closed when institutional debt goes unresolved."
    )
    return chapter(
        day=23,
        title="Šta radiš?",
        title_en="What do you do?",
        theme="Daily activity questions after the trip",
        story="After Travnik, Ana asks what everyone does today and what they like to do.",
        goals={
            "vocabulary": [
                "Use radim, radiš, and radi to talk about present activities.",
                "Ask Šta radiš? and answer with danas, sada, posao, and škola.",
            ],
            "grammar": [
                "Keep radim, radiš, and radi in the present tense.",
                "Add volim da plus a light verb for habits you enjoy.",
            ],
            "culture": [
                "Notice daily life rhythm in Bosnia and Herzegovina after a trip.",
                "Widen the map with Zenica or Tešanj on a postcard.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Daily rhythm with a Zenica or Tešanj postcard",
            "body": culture_body,
            "imageId": "zenica-postcard",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A. Ask what someone does today",
                "body": block_a,
                "tips": [
                    "Ask Šta radiš? before you offer your own answer.",
                    "Keep radim and danas in one short line.",
                    "Stay in present tense for every activity sentence.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B. Add habits with volim da",
                "body": block_b,
                "tips": [
                    "Follow radim with volim da for a habit you enjoy.",
                    "Reuse molim and hvala in market and café scenes.",
                    "Name one northern town from the postcard on the table.",
                ],
            },
        ],
        conversation={
            "title": "Šta radiš danas?",
            "setting": "Ana, Emir, and Amira talk at the café while a seller passes with market goods.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Šta radiš danas, Emire?", "english": "What do you do today, Emir?"},
                {"speaker": "Emir", "bosnian": "Radim danas. Posao je dobar.", "english": "I work today. The job is good."},
                {"speaker": "Amira", "bosnian": "Ja radim u kafiću. Sada je miran ritam.", "english": "I work in the café. Now the rhythm is calm."},
                {"speaker": "Seller", "bosnian": "Ja radim na pijaci. Prodajem voće.", "english": "I work at the market. I sell fruit."},
                {"speaker": "Ana", "bosnian": "Volim da šetam poslije posla.", "english": "I like to walk after work."},
                {"speaker": "Emir", "bosnian": "Volim da čitam i slušam muziku.", "english": "I like to read and listen to music."},
                {"speaker": "Amira", "bosnian": "Pogledaj kartu iz Zenice. Lijep grad.", "english": "Look at the card from Zenica. A nice town."},
                {"speaker": "Seller", "bosnian": "Dobar dan. Trebam odmor sada.", "english": "Good day. I need a break now."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the activity forms",
                "prompt": "Match each Bosnian form with its English meaning.",
                "items": [
                    {"left": "radim", "right": "I work or I do"},
                    {"left": "radiš", "right": "you work or you do"},
                    {"left": "šta radiš", "right": "what do you do"},
                    {"left": "volim da", "right": "I like to"},
                    {"left": "danas", "right": "today"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about daily talk",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Šta radiš? asks about today's activity.", "answer": True},
                    {"statement": "Volim da šetam means I like to walk.", "answer": True},
                    {"statement": "Zenica appears on a lesson postcard.", "answer": True},
                    {"statement": "BHRT can join Eurovision freely while sanctioned.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian question What do you do today?", "hint": "Begin with Šta radiš.", "answer": "Šta radiš danas?"},
            {"id": "pr2", "prompt": "Write the Bosnian for I work today.", "hint": "Use Radim danas.", "answer": "Radim danas."},
            {"id": "pr3", "prompt": "Write the Bosnian for I like to walk.", "hint": "Use Volim da šetam.", "answer": "Volim da šetam."},
            {"id": "pr4", "prompt": "Write the Bosnian for I like to read.", "hint": "Use Volim da čitam.", "answer": "Volim da čitam."},
            {"id": "pr5", "prompt": "Write the Bosnian for Now I work.", "hint": "Begin with Sada.", "answer": "Sada radim."},
            {"id": "pr6", "prompt": "Write the Bosnian word for school.", "hint": "It begins with ško.", "answer": "škola"},
            {"id": "pr7", "prompt": "Write the Bosnian for I need a break.", "hint": "Use Trebam odmor.", "answer": "Trebam odmor."},
            {"id": "pr8", "prompt": "Write the Bosnian for Emir works today.", "hint": "Use Emir radi danas.", "answer": "Emir radi danas."},
        ],
        facts=[
            {
                "title": "Šta radiš? opens honest daily talk",
                "body": "Šta radiš? is a friendly present-tense question after a trip or on a normal morning. The answer can name work, school, or rest. Book 1 keeps the exchange short and sayable.",
            },
            {
                "title": "Zenica widens the map beyond Sarajevo",
                "body": "Zenica sits on the Bosna River as an industrial city with its own daily rhythm. A postcard keeps the place visible without turning the lesson into a grammar tour. Northern towns balance capital-focused stories.",
            },
            {
                "title": "Volim da adds a habit after work talk",
                "body": "Volim da plus a verb lets you name a pleasure after you name a duty. Walk, read, or cook in one light line. The pattern stays in the present and avoids a full infinitive chart.",
            },
            {
                "title": "Eurovision stays closed while BHRT debt remains",
                "body": "Fans in Bosnia and Herzegovina follow Eurovision even when the country cannot compete. BHRT sanctions over unpaid debt keep the broadcaster off the contest stage. Culture abroad can mirror institutional pressure at home.",
            },
        ],
        resources=[
            {"label": "Beba Selimović - Bosno moja", "url": "https://www.youtube.com/watch?v=OXul62dILOo", "note": "A warm Bosnia song fits daily rhythm listening."},
            {"label": "Next lesson", "url": "/learn/lesson/24", "note": "Lesson 24 names mountains and rivers."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after daily talk practice."},
        ],
        quiz=[
            quiz_question("q1", "What does šta radiš mean?", ["what do you do", "how much does it cost", "where is it", "good day"], 0, "Šta radiš means what do you do.", "grammar"),
            quiz_question("q2", "Which form means I work or I do?", ["radim", "radiš", "radi", "volim"], 0, "Radim means I work or I do.", "grammar"),
            quiz_question("q3", "Which line says I like to walk?", ["Volim da šetam.", "Šta radiš?", "Račun, molim.", "Tamo je kula."], 0, "Volim da šetam means I like to walk.", "grammar"),
            quiz_question("q4", "Which town appears on a lesson postcard?", ["Zenica", "Only Neum", "Only Travnik", "Only Brčko"], 0, "Zenica appears on a lesson postcard.", "culture"),
            quiz_question("q5", "Why is Bosnia and Herzegovina absent from Eurovision?", ["BHRT remains sanctioned by the EBU over debt", "The country has no musicians", "Eurovision banned all Balkan states", "BHRT never existed"], 0, "BHRT sanctions over unpaid debt block Eurovision participation.", "culture"),
            quiz_question("q6", "What does danas mean?", ["today", "yesterday", "tomorrow", "never"], 0, "Danas means today.", "vocabulary"),
            quiz_question("q7", "What does the seller do at the market?", ["Sells fruit", "Drives a bus", "Treats patients", "Skis on Jahorina"], 0, "The seller says he sells fruit at the market.", "dialogue"),
            quiz_question("q8", "Which line names a calm café rhythm?", ["Sada je miran ritam.", "Tamo je kula.", "Koliko košta karta?", "Boli me glava."], 0, "Amira says the rhythm is calm now.", "dialogue"),
            quiz_question("q9", "What does posao mean?", ["work or job", "school", "river", "tower"], 0, "Posao means work or job.", "vocabulary"),
        ],
        civic={
            "title": "BHRT stays sanctioned and Bosnia and Herzegovina misses Eurovision",
            "body": civic_body,
            "imageId": "civic-eurovision-debt",
            "learnMore": {
                "label": "Eurovoix article on BHRT EBU sanctions",
                "url": "https://eurovoix.com/2023/11/13/bosnia-herzegovina-bhrt-remains-sanctioned-by-the-ebu/",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with Bosno moja for daily rhythm",
            kind="song",
            hook="A warm Bosnia song gives daily talk a natural listening anchor.",
            source_title="Beba Selimović - Bosno moja",
            artist="Beba Selimović",
            scene="Bosnian song for weekend leisure",
            credit="Beba Selimović on YouTube",
            url="https://www.youtube.com/watch?v=OXul62dILOo",
            prompt="Listen for a place name or short word you recognize without translating every lyric.",
            gist_prompt="What kind of listening experience does the clip provide?",
            gist_options=["A warm Bosnian song", "A bus ticket lesson", "A hospital intake form", "A ski lift announcement"],
            gist_index=0,
            target_words=["bosno", "moja"],
            notice="Let the melody carry you while you notice one familiar sound.",
            key_lines=[
                {"bosnian": "Bosno moja", "english": "My Bosnia"},
                {"bosnian": "Šta radiš danas?", "english": "What do you do today?"},
            ],
            teacher_note="After the clip, answer šta radiš? with one radim line and one volim da line.",
        ),
        speak_targets=[0, 4, 5],
        section=4,
        say_again_data=say_again([
            ("Ovo je Sulejmanija.", "This is Sulejmanija."),
            ("Šetamo kroz grad.", "We walk through the town."),
            ("Često zovem Amiru.", "I often call Amira."),
            ("Hvala!", "Thank you!"),
        ]),
        image_briefs=[
            "daily-cafe: Café table where friends compare daily schedules",
            "zenica-postcard: Postcard of Zenica on the Bosna River for culture hero",
            "activity-cards: Simple activity cards with radim and volim da prompts",
            "civic-eurovision-debt: Eurovision stage or BHRT broadcast theme for civic panel",
        ],
    )


def build_lesson_24() -> dict:
    v = [
        vocab("planina", "mountain", "plah-NEE-na", "noun", "Ovo je planina."),
        vocab("rijeka", "river", "ree-YEH-ka", "noun", "Rijeka je hladna."),
        vocab("jezero", "lake", "YEH-zeh-ro", "noun", "Jezero je mirno."),
        vocab("šuma", "forest", "SHOO-ma", "noun", "Šuma je zelena."),
        vocab("visoko", "high", "VEE-so-ko", "adverb", "Planina je visoko."),
        vocab("nisko", "low", "NEES-ko", "adverb", "Rijeka teče nisko."),
        vocab("veći", "bigger", "VEH-chee", "adjective", "Una je veća rijeka."),
        vocab("manji", "smaller", "MAHN-yee", "adjective", "Potok je manji."),
        vocab("Una", "Una River", "OO-na", "proper noun", "Una je lijepa rijeka."),
        vocab("Neretva", "Neretva River", "neh-RET-va", "proper noun", "Neretva ide kroz kanjon."),
        vocab("Bjelašnica", "Bjelašnica", "byeh-LASH-nee-tsa", "proper noun", "Bjelašnica je visoka."),
        vocab("Jahorina", "Jahorina", "ya-hoh-REE-na", "proper noun", "Jahorina je ski centar."),
        vocab("priroda", "nature", "pree-ROH-da", "noun", "Volim prirodu."),
        vocab("voda", "water", "VOH-da", "noun", "Voda je čista."),
    ]
    grammar = [
        {
            "title": "Nature nouns in short present lines",
            "explanation": (
                "Practice the whole expression before you worry about paradigms. "
                "Planina, rijeka, jezero, and šuma name the landscape around you. "
                "Pair each noun with ovo je or vidim in a present-tense line."
            ),
            "examples": [
                {"bosnian": "Ovo je planina.", "english": "This is a mountain."},
                {"bosnian": "Vidim rijeku.", "english": "I see a river."},
                {"bosnian": "Šuma je zelena.", "english": "The forest is green."},
            ],
        },
        {
            "title": "Visoko and nisko as place chunks",
            "explanation": (
                "Build this as a ready-made line you can reuse. "
                "Visoko means high and nisko means low. "
                "Use them to describe mountains and river valleys without a full comparative chart."
            ),
            "examples": [
                {"bosnian": "Planina je visoko.", "english": "The mountain is high."},
                {"bosnian": "Rijeka teče nisko.", "english": "The river runs low."},
                {"bosnian": "Bjelašnica je visoka.", "english": "Bjelašnica is high."},
            ],
        },
        {
            "title": "Veći and manji as light comparison phrases",
            "explanation": (
                "Store this as a phrase you can pull out in conversation. "
                "Veći means bigger and manji means smaller. "
                "Use them as fixed chunks with rijeka or planina rather than opening a full adjective table."
            ),
            "examples": [
                {"bosnian": "Una je veća rijeka.", "english": "Una is a bigger river."},
                {"bosnian": "Potok je manji.", "english": "The stream is smaller."},
                {"bosnian": "Jezero je manje od mora.", "english": "The lake is smaller than the sea."},
            ],
        },
    ]
    culture_body = (
        "Bosnia and Herzegovina holds dramatic nature within a small map. "
        "The Una River runs emerald green through the northwest while the Neretva carves a deep canyon toward the south. "
        "Bjelašnica rises near Sarajevo with rocky ridges that hosted men's Olympic ski events in 1984. "
        "Jahorina in Republika Srpska remains a busy winter resort linked to women's Olympic skiing from the same Games. "
        "Ana spreads postcards of rivers and peaks across the café table. "
        "Nature vocabulary turns travel dreams into names learners can say today."
    )
    block_a = (
        "Start with planina, rijeka, jezero, and šuma. "
        "Say Ovo je planina and Vidim rijeku while you look at a map or postcard. "
        "Add Una and Neretva as place names you can pronounce with confidence. "
        "Ana and Emir compare northwest rivers with southern canyons. "
        "Keep every description in the present tense. "
        "Nature talk works best when you name one feature per short line."
    )
    block_b = (
        "Add visoko, nisko, veći, and manji as comparison chunks. "
        "Say Bjelašnica je visoka and Una je veća rijeka without opening a full grammar grid. "
        "Mention Jahorina as a ski name learners hear in winter travel stories. "
        "Amira pours coffee while Mrvica bats at a pinecone near a nature photo. "
        "Mix priroda and voda when you describe why you like a walk. "
        "End with one line that names a place you want to visit this year."
    )
    civic_body = (
        "Jahorina in Republika Srpska grew into a major ski destination after the 1984 Winter Olympics women's events. "
        "Bjelašnica and Igman on the Federation side hosted men's Olympic skiing but often look neglected by comparison. "
        "Investment and maintenance diverged across entity lines after the Games. "
        "Ana reads about lift lines on Jahorina beside photos of quiet Bjelašnica slopes. "
        "Olympic heritage can boom in one place while a nearby host mountain fades."
    )
    return chapter(
        day=24,
        title="Planine i rijeke",
        title_en="Mountains and rivers",
        theme="Una, Neretva, Bjelašnica",
        story="Ana and Emir name rivers and mountains across Bosnia and Herzegovina on a nature day.",
        goals={
            "vocabulary": [
                "Name planina, rijeka, jezero, šuma, and priroda in present lines.",
                "Place Una, Neretva, Bjelašnica, and Jahorina on the nature map.",
            ],
            "grammar": [
                "Describe height with visoko and nisko as chunks.",
                "Use veći and manji in light comparison phrases.",
            ],
            "culture": [
                "Connect emerald Una water and Neretva canyon stories.",
                "Notice 1984 Olympic mountains Jahorina and Bjelašnica.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Rivers and Olympic peaks across the map",
            "body": culture_body,
            "imageId": "una-river",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A. Name mountains and rivers",
                "body": block_a,
                "tips": [
                    "Point at a map while you say ovo je.",
                    "Keep one nature noun per short sentence.",
                    "Stay in present tense for every description.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B. Compare height and size",
                "body": block_b,
                "tips": [
                    "Use veći and manji as fixed chunks with rijeka.",
                    "Say Bjelašnica and Jahorina aloud several times.",
                    "Add volim prirodu when you name a favorite place.",
                ],
            },
        ],
        conversation={
            "title": "Priroda na stolu",
            "setting": "Ana and Emir spread nature postcards at the café while Amira listens and Mrvica plays with a pinecone.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Ovo je Una. Rijeka je veća i zelena.", "english": "This is Una. The river is bigger and green."},
                {"speaker": "Emir", "bosnian": "Vidim Neretvu na karti. Kanjon je dubok.", "english": "I see Neretva on the map. The canyon is deep."},
                {"speaker": "Amira", "bosnian": "Volim prirodu u Bosni i Hercegovini.", "english": "I love nature in Bosnia and Herzegovina."},
                {"speaker": "Mrvica", "bosnian": "Mjau! Šuma je zanimljiva.", "english": "Meow! The forest is interesting."},
                {"speaker": "Ana", "bosnian": "Bjelašnica je visoka planina.", "english": "Bjelašnica is a high mountain."},
                {"speaker": "Emir", "bosnian": "Jahorina je poznata za skijanje.", "english": "Jahorina is famous for skiing."},
                {"speaker": "Amira", "bosnian": "Jezero je manje od mora, ali mirno.", "english": "The lake is smaller than the sea, but calm."},
                {"speaker": "Mrvica", "bosnian": "Mjau! Voda je hladna.", "english": "Meow! The water is cold."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the nature words",
                "prompt": "Match each Bosnian nature word with its English meaning.",
                "items": [
                    {"left": "planina", "right": "mountain"},
                    {"left": "rijeka", "right": "river"},
                    {"left": "jezero", "right": "lake"},
                    {"left": "šuma", "right": "forest"},
                    {"left": "voda", "right": "water"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false about nature day",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Una is a river in northwest Bosnia and Herzegovina.", "answer": True},
                    {"statement": "Veći means smaller.", "answer": False},
                    {"statement": "Jahorina hosted women's Olympic skiing in 1984.", "answer": True},
                    {"statement": "Neretva is only a lake name.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian for This is a mountain.", "hint": "Use Ovo je planina.", "answer": "Ovo je planina."},
            {"id": "pr2", "prompt": "Write the Bosnian for I see a river.", "hint": "Begin with Vidim.", "answer": "Vidim rijeku."},
            {"id": "pr3", "prompt": "Write the Bosnian for The forest is green.", "hint": "Use Šuma je zelena.", "answer": "Šuma je zelena."},
            {"id": "pr4", "prompt": "Write the Bosnian for Bjelašnica is high.", "hint": "Use Bjelašnica je visoka.", "answer": "Bjelašnica je visoka."},
            {"id": "pr5", "prompt": "Write the Bosnian for Una is a bigger river.", "hint": "Use Una je veća rijeka.", "answer": "Una je veća rijeka."},
            {"id": "pr6", "prompt": "Write the Bosnian word for lake.", "hint": "It begins with jez.", "answer": "jezero"},
            {"id": "pr7", "prompt": "Write the Bosnian for I love nature.", "hint": "Use Volim prirodu.", "answer": "Volim prirodu."},
        ],
        facts=[
            {
                "title": "Una runs emerald in the northwest",
                "body": "The Una River is famous for green water and waterfalls near Bihać. Travelers name it early when they plan nature trips. Ana's postcard keeps the river on the lesson table.",
            },
            {
                "title": "Neretva cuts a southern canyon",
                "body": "The Neretva flows through a dramatic canyon toward the Adriatic region. It connects mountain stories with southern travel dreams. River names widen the map beyond one city.",
            },
            {
                "title": "1984 Olympics left two ski stories",
                "body": "Sarajevo hosted the 1984 Winter Olympics on nearby mountains. Jahorina and Bjelašnica still appear in winter travel talk today. Olympic names give learners cultural hooks for nature vocabulary.",
            },
            {
                "title": "Veći and manji stay light in Book 1",
                "body": "Book 1 treats veći and manji as sayable comparison chunks rather than a full adjective system. Pair them with rijeka or jezero in one short line. Present-tense nature talk stays practical.",
            },
        ],
        resources=[
            {"label": "Beba Selimović - Bosno moja", "url": "https://www.youtube.com/watch?v=OXul62dILOo", "note": "A Bosnia song supports nature-day listening."},
            {"label": "Next lesson", "url": "/learn/lesson/25", "note": "Lesson 25 visits the doctor after Mrvica and a pinecone."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after nature vocabulary."},
        ],
        quiz=[
            quiz_question("q1", "What does planina mean?", ["mountain", "river", "lake", "forest"], 0, "Planina means mountain.", "vocabulary"),
            quiz_question("q2", "Which river is famous for green water in the northwest?", ["Una", "Neretva only in the sea", "No rivers exist", "Only the Adriatic"], 0, "Una is famous for green water in the northwest.", "culture"),
            quiz_question("q3", "What does veći mean as a light comparison chunk?", ["bigger", "smaller", "colder", "faster"], 0, "Veći means bigger.", "grammar"),
            quiz_question("q4", "Which mountain hosted women's Olympic skiing in 1984?", ["Jahorina", "Only Bjelašnica for all events", "Only Neum beach", "Only Travnik tower"], 0, "Jahorina hosted women's Olympic skiing in 1984.", "culture"),
            quiz_question("q5", "What civic gap does the lesson describe?", ["Jahorina booms while Bjelašnica and Igman look neglected", "All ski lifts closed forever", "Una stopped flowing", "Neretva became a desert"], 0, "Investment diverged between Jahorina and Federation Olympic sites.", "culture"),
            quiz_question("q6", "What does šuma mean?", ["forest", "ticket", "bill", "phone"], 0, "Šuma means forest.", "vocabulary"),
            quiz_question("q7", "Which line says I love nature?", ["Volim prirodu.", "Račun, molim.", "Šta radiš?", "Tamo je kula."], 0, "Volim prirodu means I love nature.", "dialogue"),
            quiz_question("q8", "What does nisko mean?", ["low", "high", "big", "green"], 0, "Nisko means low.", "vocabulary"),
            quiz_question("q9", "Which river appears with a deep canyon?", ["Neretva", "Una only as a lake", "No southern rivers", "Only the Una in the north"], 0, "Neretva appears with a deep canyon.", "culture"),
        ],
        civic={
            "title": "Jahorina booms while Bjelašnica and Igman Olympic sites lag",
            "body": civic_body,
            "imageId": "civic-olympic-ski-gap",
            "learnMore": {
                "label": "Wikipedia article about Jahorina",
                "url": "https://en.wikipedia.org/wiki/Jahorina",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with Bosno moja for nature feeling",
            kind="song",
            hook="A Bosnia song gives river-and-mountain day a listening anchor.",
            source_title="Beba Selimović - Bosno moja",
            artist="Beba Selimović",
            scene="Bosnian landscape mood",
            credit="Beba Selimović on YouTube",
            url="https://www.youtube.com/watch?v=OXul62dILOo",
            prompt="Listen for a landscape mood without translating every lyric.",
            gist_prompt="What kind of clip supports a nature day?",
            gist_options=["A warm Bosnia song", "A bus departure board", "A restaurant bill lesson", "A phone emergency call"],
            gist_index=0,
            target_words=["bosno", "rijeka"],
            notice="Catch one sound that fits rivers or mountains in your imagination.",
            key_lines=[
                {"bosnian": "Bosno moja", "english": "My Bosnia"},
                {"bosnian": "Volim prirodu.", "english": "I love nature."},
            ],
            teacher_note="After the clip, name one river and one mountain from the lesson aloud.",
        ),
        speak_targets=[0, 4, 5],
        section=4,
        say_again_data=say_again([
            ("Šta radiš danas?", "What do you do today?"),
            ("Volim da šetam.", "I like to walk."),
            ("Vidim džamiju.", "I see a mosque."),
            ("Kakvo je vrijeme?", "How is the weather?"),
        ]),
        image_briefs=[
            "una-river: Emerald Una River water for culture hero",
            "bjelasnica-ridge: Bjelašnica rocky ridge near Sarajevo for mid-lesson scene",
            "jahorina-ski: Jahorina ski slopes for winter place beat",
            "civic-olympic-ski-gap: Split image of busy Jahorina lift and quiet Bjelašnica slope for civic panel",
        ],
    )


def build_lesson_25() -> dict:
    v = [
        vocab("glava", "head", "GLAH-va", "noun", "Boli me glava."),
        vocab("stomak", "stomach", "STOH-mak", "noun", "Boli me stomak."),
        vocab("temperatura", "temperature or fever", "tehm-peh-rah-TOO-ra", "noun", "Imam temperaturu."),
        vocab("lijek", "medicine", "LYEH-yek", "noun", "Treba mi lijek."),
        vocab("boli me", "it hurts me or I have pain in", "BOH-lee meh", "phrase", "Boli me glava."),
        vocab("doktor", "doctor", "DOK-tor", "noun", "Gdje je doktor?"),
        vocab("apoteka", "pharmacy", "ah-poh-TEH-ka", "noun", "Apoteka je blizu."),
        vocab("boli", "hurts", "BOH-lee", "verb form", "Boli me noga."),
        vocab("umoran", "tired (m.)", "oo-MOR-an", "adjective", "Mrvica je umorna."),
        vocab("pomoć", "help", "POH-myoch", "noun", "Treba mi pomoć."),
        vocab("zdravo", "healthy or hello", "ZDRAH-vo", "adjective", "Nadam se da si zdrav."),
        vocab("šmrka", "pinecone", "SHMR-ka", "noun", "Mrvica jede šmrku."),
        vocab("klinika", "clinic", "KLEE-nee-ka", "noun", "Klinika je otvorena."),
        vocab("molim vas", "please (formal)", "MOH-leem vas", "phrase", "Pomoć, molim vas."),
    ]
    grammar = [
        {
            "title": "Boli me plus a body part",
            "explanation": (
                "Focus on the spoken chunk. Postpone the full paradigm. "
                "Boli me means something hurts me. Add glava, stomak, or another body word right after the chunk. "
                "Keep the line in the present when you describe pain today."
            ),
            "examples": [
                {"bosnian": "Boli me glava.", "english": "My head hurts."},
                {"bosnian": "Boli me stomak.", "english": "My stomach hurts."},
                {"bosnian": "Boli me noga.", "english": "My leg hurts."},
            ],
        },
        {
            "title": "Treba mi lijek and clinic phrases",
            "explanation": (
                "Learn this as a full phrase. Do not treat it as a table. "
                "Treba mi lijek names a need at a pharmacy or clinic. "
                "Add molim vas when you speak to a doctor or pharmacist."
            ),
            "examples": [
                {"bosnian": "Treba mi lijek.", "english": "I need medicine."},
                {"bosnian": "Gdje je doktor?", "english": "Where is the doctor?"},
                {"bosnian": "Pomoć, molim vas.", "english": "Help, please."},
            ],
        },
        {
            "title": "Polite health visit language",
            "explanation": (
                "Hold this as a spoken pattern. Do not treat it as a grammar grid. "
                "Use molim vas and hvala at a clinic or pharmacy counter. "
                "Name symptoms with boli me and stay calm in the present tense."
            ),
            "examples": [
                {"bosnian": "Imam temperaturu.", "english": "I have a fever."},
                {"bosnian": "Doktor, boli me stomak.", "english": "Doctor, my stomach hurts."},
                {"bosnian": "Hvala, doktore.", "english": "Thank you, doctor."},
            ],
        },
    ]
    culture_body = (
        "A polite health visit in Bosnia and Herzegovina starts with a clear greeting and a calm symptom line. "
        "Patients say boli me plus the body part rather than a long medical lecture. "
        "Pharmacies and small clinics expect please and thank you at the counter. "
        "Ana brings Mrvica to a vet clinic after the cat swallows part of a pinecone on a nature walk. "
        "The staff treat the visit seriously even when the patient is small and furry. "
        "Clear present-tense phrases help both human and pet care sound respectful."
    )
    block_a = (
        "Learn glava, stomak, temperatura, and lijek as health nouns you can say today. "
        "Practice Boli me glava and Imam temperaturu as full present-tense lines. "
        "Add doktor and apoteka when you ask where to get help. "
        "Ana carries Mrvica toward a clinic door after the pinecone incident. "
        "Keep symptoms short and clear. "
        "A vet visit uses the same polite frames as a human clinic in Book 1."
    )
    block_b = (
        "Use Treba mi lijek and Pomoć, molim vas at the counter. "
        "The doctor asks what hurts and Ana answers with boli me lines for the cat. "
        "Emir waits outside while Amira brings water and calm words. "
        "Finish with Hvala, doktore when the visit ends. "
        "Health talk stays in the present tense without past storytelling. "
        "Repeat each symptom line još jednom until it sounds steady and polite."
    )
    civic_body = (
        "In 2013 political deadlock in Bosnia and Herzegovina left newborns without unique ID numbers called JMBG. "
        "Without those numbers infants could not receive passports or travel abroad for urgent medical care. "
        "The Belmina case drew protests known as the Baby Revolution when treatment abroad was blocked. "
        "Ana reads a short note about the crisis while she waits with Mrvica at the clinic. "
        "Identity paperwork can become a life-or-death barrier when institutions stop cooperating."
    )
    return chapter(
        day=25,
        title="Kod doktora",
        title_en="At the doctor",
        theme="Mrvica vs pinecone (vet subplot)",
        story="Mrvica swallows part of a pinecone and Ana brings the cat to a vet clinic for help.",
        goals={
            "vocabulary": [
                "Name glava, stomak, temperatura, lijek, and doktor in health talk.",
                "Use boli me and Treba mi lijek at a clinic or pharmacy.",
            ],
            "grammar": [
                "Describe pain with boli me plus a body part.",
                "Ask for help politely with molim vas at a health visit.",
            ],
            "culture": [
                "Practice polite pharmacy and clinic phrases in present tense.",
                "Treat a vet visit with the same calm respect as human care.",
            ],
        },
        vocabulary=v,
        grammar=grammar,
        culture={
            "title": "Polite words at the pharmacy and clinic",
            "body": culture_body,
            "imageId": "clinic-door",
        },
        blocks=[
            {
                "id": "a",
                "title": "Lesson A. Name pain and symptoms",
                "body": block_a,
                "tips": [
                    "Keep boli me and the body part in one breath.",
                    "Stay calm and use present-tense symptom lines.",
                    "Add molim vas when you ask for help.",
                ],
            },
            {
                "id": "b",
                "title": "Lesson B. Ask for medicine and thank the doctor",
                "body": block_b,
                "tips": [
                    "Use Treba mi lijek at a pharmacy counter.",
                    "Say Hvala, doktore before you leave.",
                    "Repeat a symptom line još jednom if the room is noisy.",
                ],
            },
        ],
        conversation={
            "title": "Mrvica i šmrka",
            "setting": "Ana brings Mrvica to a vet clinic while Emir and Amira wait nearby and the doctor examines the cat.",
            "lines": [
                {"speaker": "Ana", "bosnian": "Doktore, Mrvica je bolesna. Boli je stomak.", "english": "Doctor, Mrvica is sick. Her stomach hurts."},
                {"speaker": "Doctor", "bosnian": "Razumijem. Imam temperaturu kod nje?", "english": "I understand. Does she have a fever?"},
                {"speaker": "Emir", "bosnian": "Da. Treba nam pomoć sada.", "english": "Yes. We need help now."},
                {"speaker": "Amira", "bosnian": "Ana, diži glavu. Diši polako.", "english": "Ana, lift your head. Breathe slowly."},
                {"speaker": "Ana", "bosnian": "Mrvica ima šmrku u stomaku.", "english": "Mrvica has a pinecone in her stomach."},
                {"speaker": "Doctor", "bosnian": "Treba lijek i odmor. Apoteka je pored klinike.", "english": "She needs medicine and rest. The pharmacy is beside the clinic."},
                {"speaker": "Emir", "bosnian": "Hvala, doktore. Idemo u apoteku.", "english": "Thank you, doctor. We are going to the pharmacy."},
                {"speaker": "Amira", "bosnian": "Sretno, Mrvico. Sada si mirnija.", "english": "Good luck, Mrvica. You are calmer now."},
            ],
        },
        puzzles=[
            {
                "id": "p1",
                "type": "match",
                "title": "Match the health words",
                "prompt": "Match each Bosnian health word with its English meaning.",
                "items": [
                    {"left": "glava", "right": "head"},
                    {"left": "stomak", "right": "stomach"},
                    {"left": "lijek", "right": "medicine"},
                    {"left": "doktor", "right": "doctor"},
                    {"left": "boli me", "right": "it hurts me"},
                ],
            },
            {
                "id": "p2",
                "type": "truefalse",
                "title": "True or false at the clinic",
                "prompt": "Decide whether each sentence matches the lesson.",
                "items": [
                    {"statement": "Boli me glava means my head hurts.", "answer": True},
                    {"statement": "Apoteka means pharmacy.", "answer": True},
                    {"statement": "Mrvica has a pinecone in her stomach.", "answer": True},
                    {"statement": "The 2013 JMBG crisis helped newborns travel easily.", "answer": False},
                ],
            },
        ],
        practice=[
            {"id": "pr1", "prompt": "Write the Bosnian for My head hurts.", "hint": "Use Boli me glava.", "answer": "Boli me glava."},
            {"id": "pr2", "prompt": "Write the Bosnian for My stomach hurts.", "hint": "Use Boli me stomak.", "answer": "Boli me stomak."},
            {"id": "pr3", "prompt": "Write the Bosnian for I need medicine.", "hint": "Use Treba mi lijek.", "answer": "Treba mi lijek."},
            {"id": "pr4", "prompt": "Write the Bosnian for Where is the doctor?", "hint": "Begin with Gdje je.", "answer": "Gdje je doktor?"},
            {"id": "pr5", "prompt": "Write the Bosnian for Help, please.", "hint": "Use Pomoć, molim vas.", "answer": "Pomoć, molim vas."},
            {"id": "pr6", "prompt": "Write the Bosnian for I have a fever.", "hint": "Use Imam temperaturu.", "answer": "Imam temperaturu."},
            {"id": "pr7", "prompt": "Write the Bosnian word for pharmacy.", "hint": "It begins with apo.", "answer": "apoteka"},
            {"id": "pr8", "prompt": "Write the Bosnian for Thank you, doctor.", "hint": "Use Hvala, doktore.", "answer": "Hvala, doktore."},
        ],
        facts=[
            {
                "title": "Boli me is a fast symptom chunk",
                "body": "Boli me plus a body part lets you name pain without a long grammar chart. Clinics and pharmacies hear this pattern often. Book 1 keeps health talk practical and present tense.",
            },
            {
                "title": "Vet clinics use the same polite frames",
                "body": "Pet owners in Bosnia and Herzegovina bring cats and dogs to clinics with the same please-and-thank-you habits as human visits. Mrvica's pinecone plot keeps the scene light while the language stays serious.",
            },
            {
                "title": "Apoteka sits beside many clinics",
                "body": "Learners often need medicine right after a short exam. Apoteka is a high-value word for travelers who get a simple prescription. Pair it with gdje je for a useful location question.",
            },
            {
                "title": "JMBG deadlock endangered infants in 2013",
                "body": "Political gridlock once blocked newborns from receiving ID numbers needed for passports and care abroad. Protests called the Baby Revolution pushed leaders to face the harm. Identity rules can touch life-and-death travel for families.",
            },
        ],
        resources=[
            {"label": "Bosnian Grammar: How to Say I am", "url": "https://www.youtube.com/watch?v=CUUGzc3C1G8", "note": "Introduction chunks help you greet clinic staff calmly."},
            {"label": "Next lesson", "url": "/learn/lesson/26", "note": "Lesson 26 looks at housing and longer stays."},
            {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after health phrases."},
        ],
        quiz=[
            quiz_question("q1", "What does boli me glava mean?", ["My head hurts", "I need a ticket", "I like to walk", "This is a mosque"], 0, "Boli me glava means my head hurts.", "grammar"),
            quiz_question("q2", "Which word means medicine?", ["lijek", "karta", "kula", "šuma"], 0, "Lijek means medicine.", "vocabulary"),
            quiz_question("q3", "What happened to Mrvica?", ["She has a pinecone in her stomach", "She bought a bus ticket", "She won a game", "She called Eurovision"], 0, "Mrvica has a pinecone in her stomach.", "dialogue"),
            quiz_question("q4", "What does apoteka mean?", ["pharmacy", "mountain", "river", "weekend"], 0, "Apoteka means pharmacy.", "vocabulary"),
            quiz_question("q5", "What was the 2013 JMBG crisis about?", ["Newborns lacked ID numbers for passports and care abroad", "All pharmacies closed", "Cats could not visit vets", "Buses became free"], 0, "Deadlock blocked unique ID numbers for newborns.", "culture"),
            quiz_question("q6", "Which line asks for help politely?", ["Pomoć, molim vas.", "Šta radiš?", "Una je veća rijeka.", "Hajde da idemo."], 0, "Pomoć, molim vas asks for help politely.", "grammar"),
            quiz_question("q7", "Who examines Mrvica?", ["The doctor", "A bus clerk", "A market seller", "A ski lift operator"], 0, "The doctor examines Mrvica at the clinic.", "dialogue"),
            quiz_question("q8", "What does temperatura mean in this lesson?", ["fever or temperature", "ticket price", "tower view", "forest walk"], 0, "Temperatura means fever or temperature here.", "vocabulary"),
            quiz_question("q9", "Where is the pharmacy according to the doctor?", ["Beside the clinic", "On Jahorina ski slope", "In the Una River", "At the Eurovision stage"], 0, "The doctor says the pharmacy is beside the clinic.", "dialogue"),
        ],
        civic={
            "title": "2013 JMBG deadlock left newborns without ID numbers",
            "body": civic_body,
            "imageId": "civic-jmbg",
            "learnMore": {
                "label": "Al Jazeera opinion on Bosnia's babies in limbo",
                "url": "https://www.aljazeera.com/opinions/2013/6/20/bosnias-babies-in-limbo",
            },
        },
        listen=authentic_listen(
            title="Čuj Bosnu with Ja sam for calm clinic greetings",
            kind="speaker",
            hook="Self-introduction chunks help you greet clinic staff before you name a symptom.",
            source_title="Bosnian Grammar. How to Say I am (Ja sam) - Introducing Yourself",
            artist="Lingo Hero",
            scene="Self-introduction for calm health visits",
            credit="Lingo Hero on YouTube",
            url="https://www.youtube.com/watch?v=CUUGzc3C1G8",
            prompt="Listen for Ja sam and imagine greeting clinic staff calmly.",
            gist_prompt="What is the speaker teaching?",
            gist_options=["How to say I am and introduce yourself", "How to ski Jahorina only", "How to order klepe only", "How to read bus boards only"],
            gist_index=0,
            target_words=["ja", "sam"],
            notice="A calm greeting comes before symptom lines at a clinic.",
            key_lines=[
                {"bosnian": "Ja sam Ana.", "english": "I am Ana."},
                {"bosnian": "Pomoć, molim vas.", "english": "Help, please."},
            ],
            teacher_note="After the clip, say Ja sam… then one boli me line for a symptom.",
        ),
        speak_targets=[0, 4, 6],
        section=4,
        say_again_data=say_again([
            ("Treba mi pomoć.", "I need help."),
            ("Gdje je apoteka?", "Where is the pharmacy?"),
            ("Volim prirodu.", "I love nature."),
            ("Hvala!", "Thank you!"),
        ]),
        image_briefs=[
            "clinic-door: Clinic entrance where Ana brings Mrvica for culture hero",
            "pharmacy-shelf: Pharmacy shelf with medicine boxes for mid-lesson scene",
            "mrvica-vet: Mrvica at the vet exam table for story beat",
            "civic-jmbg: Protest or newborn identity documents theme for JMBG civic panel",
        ],
    )


LESSONS: dict[int, dict] = {
    21: build_lesson_21(),
    22: build_lesson_22(),
    23: build_lesson_23(),
    24: build_lesson_24(),
    25: build_lesson_25(),
}


VIDEO_21 = """
# Lesson 21 video script for Ponavljanje
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 21: Review
- BS: Ponavljanje
- Background: Ana plans a solo weekend with a map and Una postcard.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 21 is Ponavljanje. Ana plans a solo weekend and drills frames from Lessons 15 through 20.
**On screen:** Ponavljanje | Lesson 21

### 0:40 Goals
**Narration:** You recycle Treba mi, Hoću, and three question frames for travel, place, and weather.
**On screen:** Treba mi | Hoću | Koliko košta?

### 1:30 Culture hook
**Narration:** Postcards from Una, Bihać, or Jajce turn review night into a real trip idea beyond Sarajevo.
**On screen:** Una | Jajce | weekend map | image credits

### 3:00 Lesson A. Drill need and wish frames
**Narration:** Say Treba mi karta and Hoću vikend samo as full present-tense lines at the café table.
**On screen:** Treba mi karta. | Hoću vikend samo.

### 5:00 Lesson B. Switch travel questions
**Narration:** Ask Koliko košta?, Gdje je autobus?, and Kakvo je vrijeme? while Mrvica stays behind.
**On screen:** Gdje je autobus? | Kakvo je vrijeme?

### 6:30 Mini dialogue
**Narration:** Ana, Emir, Amira, and Mrvica plan the weekend over coffee and postcards.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and say one need line and one question line aloud. Continue with Lesson 22, Danas u Travniku.
**On screen:** Drill two frames | Next lesson is Danas u Travniku

## End screen
- Link to website `/learn/lesson/21`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_22 = """
# Lesson 22 video script for Danas u Travniku
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 22: Today in Travnik
- BS: Danas u Travniku
- Background: Sulejmanija Mosque above Travnik old town.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 22 is Danas u Travniku. Ana and Emir walk the vizier town and name what they see.
**On screen:** Danas u Travniku | Lesson 22

### 0:40 Goals
**Narration:** You learn vidim, ovo je, tamo je, and šetamo for present-tense sightseeing.
**On screen:** vidim | ovo je | šetamo

### 1:30 Culture hook
**Narration:** Travnik keeps Ottoman vizier history and a colorful Sulejmanija Mosque on the hillside.
**On screen:** Sulejmanija | stari grad | image credits

### 3:00 Lesson A. Point and name what you see
**Narration:** Say Ovo je Sulejmanija and Vidim džamiju while you walk the old streets.
**On screen:** Ovo je Sulejmanija. | Vidim džamiju.

### 5:00 Lesson B. Walk the old town together
**Narration:** Use Tamo je kula and Šetamo kroz grad while Amira listens on the phone.
**On screen:** Tamo je kula. | Šetamo kroz grad.

### 6:30 Mini dialogue
**Narration:** A passerby points toward the old town while Ana and Emir describe the view.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and name two landmarks with ovo je and tamo je. Continue with Lesson 23, Šta radiš?
**On screen:** Name two sights | Next lesson is Šta radiš?

## End screen
- Link to website `/learn/lesson/22`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_23 = """
# Lesson 23 video script for Šta radiš?
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 23: What do you do?
- BS: Šta radiš?
- Background: Café table with a Zenica postcard and activity cards.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 23 is Šta radiš? After Travnik, Ana asks what everyone does today.
**On screen:** Šta radiš? | Lesson 23

### 0:40 Goals
**Narration:** You learn radim, radiš, radi, and volim da for daily activity talk in the present.
**On screen:** radim | radiš | volim da

### 1:30 Culture hook
**Narration:** Daily rhythm in Bosnia and Herzegovina widens with a Zenica or Tešanj postcard on the table.
**On screen:** Zenica | daily café | image credits

### 3:00 Lesson A. Ask what someone does today
**Narration:** Ask Šta radiš danas? and answer with Radim danas in one clear line.
**On screen:** Šta radiš danas? | Radim danas.

### 5:00 Lesson B. Add habits with volim da
**Narration:** Add Volim da šetam or Volim da čitam after you name today's work.
**On screen:** Volim da šetam. | Volim da čitam.

### 6:30 Mini dialogue
**Narration:** Emir, Amira, and a market seller compare schedules while Ana names her habits.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and answer šta radiš? with one radim line and one volim da line. Continue with Lesson 24, Planine i rijeke.
**On screen:** Two activity lines | Next lesson is Planine i rijeke

## End screen
- Link to website `/learn/lesson/23`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_24 = """
# Lesson 24 video script for Planine i rijeke
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 24: Mountains and rivers
- BS: Planine i rijeke
- Background: Emerald Una River beside mountain postcards.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 24 is Planine i rijeke. Ana and Emir name rivers and peaks across Bosnia and Herzegovina.
**On screen:** Planine i rijeke | Lesson 24

### 0:40 Goals
**Narration:** You learn planina, rijeka, jezero, šuma, and light comparison chunks visoko, nisko, veći, and manji.
**On screen:** planina | rijeka | veći | manji

### 1:30 Culture hook
**Narration:** Una, Neretva, Bjelašnica, and Jahorina connect nature day with Olympic mountain memory.
**On screen:** Una | Neretva | Jahorina | image credits

### 3:00 Lesson A. Name mountains and rivers
**Narration:** Say Ovo je planina and Vidim rijeku while you spread postcards on the café table.
**On screen:** Ovo je planina. | Vidim rijeku.

### 5:00 Lesson B. Compare height and size
**Narration:** Use Bjelašnica je visoka and Una je veća rijeka without opening a full grammar chart.
**On screen:** Bjelašnica je visoka. | Una je veća rijeka.

### 6:30 Mini dialogue
**Narration:** Mrvica bats at a pinecone while the friends compare rivers, forests, and ski names.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and name one river and one mountain from the lesson. Continue with Lesson 25, Kod doktora.
**On screen:** Name river and mountain | Next lesson is Kod doktora

## End screen
- Link to website `/learn/lesson/24`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEO_25 = """
# Lesson 25 video script for Kod doktora
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN: Lesson 25: At the doctor
- BS: Kod doktora
- Background: Clinic door with Mrvica and a pinecone on a nature walk.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 25 is Kod doktora. Mrvica eats a pinecone and Ana brings the cat to a vet clinic.
**On screen:** Kod doktora | Lesson 25

### 0:40 Goals
**Narration:** You learn boli me, glava, stomak, temperatura, lijek, and polite clinic phrases.
**On screen:** boli me | lijek | doktor

### 1:30 Culture hook
**Narration:** Polite health visits in Bosnia and Herzegovina start with calm greetings and short symptom lines.
**On screen:** apoteka | clinic | image credits

### 3:00 Lesson A. Name pain and symptoms
**Narration:** Say Boli me glava and Imam temperaturu as present-tense health chunks.
**On screen:** Boli me glava. | Imam temperaturu.

### 5:00 Lesson B. Ask for medicine and thank the doctor
**Narration:** Use Treba mi lijek and Pomoć, molim vas at the clinic and pharmacy counter.
**On screen:** Treba mi lijek. | Hvala, doktore.

### 6:30 Mini dialogue
**Narration:** The doctor examines Mrvica while Emir and Amira stay calm outside the exam room.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and say one boli me line and one polite help line. Continue with Lesson 26, Stanovanje.
**On screen:** Symptom and help lines | Next lesson is Stanovanje

## End screen
- Link to website `/learn/lesson/25`
- Playlist: Learn Bosnian Book 1
- Image credits appear in the description.
"""


VIDEOS: dict[int, str] = {
    21: VIDEO_21,
    22: VIDEO_22,
    23: VIDEO_23,
    24: VIDEO_24,
    25: VIDEO_25,
}

