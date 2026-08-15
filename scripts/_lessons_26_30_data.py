"""Book 1 Lessons 26-30 chapter data and video scripts for Learn Bosnian."""
from __future__ import annotations

PHRASE_BANK = [
    "Learn this as a full phrase. Do not treat it as a table.",
    "Treat this as a ready chunk you can say today.",
    "Say the whole line together. Skip the full chart for now.",
    "Hold this as a spoken pattern. Do not treat it as a grammar grid.",
    "Learn the usable chunk first. Full tables can wait.",
    "Keep this as a sayable line rather than a paradigm list.",
    "Memorize the phrase shape. Leave the full table for later.",
    "Take this as a speaking chunk. Do not memorize a case chart yet.",
    "Practice the whole expression before you worry about paradigms.",
    "Build this as a ready-made line you can reuse.",
    "Store this as a phrase you can pull out in conversation.",
    "Focus on the spoken chunk. Postpone the full paradigm.",
]


def vocab(bs: str, en: str, pron: str, pos: str, ex: str) -> dict:
    return {
        "bosnian": bs,
        "english": en,
        "pronunciation": pron,
        "partOfSpeech": pos,
        "example": ex,
    }


def grammar(title: str, opener_idx: int, body: str, examples: list[tuple[str, str]]) -> dict:
    return {
        "title": title,
        "explanation": f"{PHRASE_BANK[opener_idx - 1]} {body}",
        "examples": [{"bosnian": b, "english": e} for b, e in examples],
    }


def quiz_q(qid: str, question: str, options: list[str], correct: int, explanation: str, skill: str) -> dict:
    return {
        "id": qid,
        "question": question,
        "options": options,
        "correctIndex": correct,
        "explanation": explanation,
        "skill": skill,
    }


def say_again(lines: list[tuple[str, str]]) -> dict:
    return {
        "title": "Say again",
        "intro": "Warm up with four frames you already know.",
        "lines": [{"bosnian": b, "english": e} for b, e in lines],
    }


def authentic_listen(
    title: str,
    kind: str,
    hook: str,
    source_title: str,
    speaker: str,
    scene: str,
    url: str,
    gist_prompt: str,
    gist_options: list[str],
    gist_index: int,
    listen_prompt: str,
    target_words: list[str],
    notice: str,
    key_lines: list[tuple[str, str]],
    teacher_note: str,
) -> dict:
    return {
        "title": title,
        "kind": kind,
        "hook": hook,
        "source": {
            "title": source_title,
            "artistOrSpeaker": speaker,
            "regionOrScene": scene,
            "license": "YouTube Terms of Service (embed)",
            "credit": f"{speaker} on YouTube",
            "pageUrl": url,
            "embedUrl": url,
        },
        "durationHint": "45-90 seconds",
        "listenTask": {
            "prompt": listen_prompt,
            "gistQuestion": {
                "prompt": gist_prompt,
                "options": gist_options,
                "correctIndex": gist_index,
            },
            "targetWords": target_words,
            "noticePrompt": notice,
        },
        "reveal": {
            "keyLines": [{"bosnian": b, "english": e} for b, e in key_lines],
            "teacherNote": teacher_note,
        },
    }


def civic(title: str, body: str, image_id: str, label: str, url: str) -> dict:
    return {
        "title": title,
        "body": body,
        "imageId": image_id,
        "learnMore": {"label": label, "url": url},
    }


def chapter(
    day: int,
    title: str,
    title_en: str,
    theme: str,
    story: str,
    goals: dict,
    vocabulary: list[dict],
    grammar_panels: list[dict],
    culture_title: str,
    culture_body: str,
    culture_image: str,
    blocks: list[dict],
    conversation: dict,
    puzzles: list[dict],
    practice: list[dict],
    facts: list[dict],
    resources: list[dict],
    quiz: list[dict],
    civic_ctx: dict,
    listen: dict,
    speak_targets: list[int],
    section: int,
    say_again_block: dict,
    image_briefs: list[str],
    can_do_checks: list[dict] | None = None,
) -> dict:
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
        "grammar": grammar_panels,
        "culture": {"title": culture_title, "body": culture_body, "imageId": culture_image},
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
            {
                "day": day,
                "bosnian": item["bosnian"],
                "english": item["english"],
                "pronunciation": item["pronunciation"],
                "partOfSpeech": item["partOfSpeech"],
                "example": item["example"],
            }
            for item in vocabulary
        ],
        "images": [],
        "imagesNeeded": False,
        "imageBriefs": image_briefs,
        "civicContext": civic_ctx,
        "authenticListen": listen,
        "speakTargets": speak_targets,
        "section": section,
        "sayAgain": say_again_block,
    }
    if can_do_checks is not None:
        data["canDoChecks"] = can_do_checks
    return data


LESSON_26 = chapter(
    day=26,
    title="Stanovanje",
    title_en="Housing",
    theme="Looking at a longer stay",
    story="Ana and Emir visit a Zenica flat with Amira and almost sign a monthly lease with the landlord.",
    goals={
        "vocabulary": [
            "Name stan, soba, kirija, and namještaj for a rental visit.",
            "Use može and moraš as present permission and obligation chunks.",
            "Ask Koliko je kirija? and talk about a monthly stay.",
        ],
        "grammar": [
            "Use Može? and Može. as quick permission lines.",
            "Say moraš with rent and contract nouns in the present.",
            "Describe a flat with ima and soba phrases.",
        ],
        "culture": [
            "Picture apartment hunting in Zenica near schools and tram lines.",
            "Treat a hallway tour as polite present-tense practice.",
            "Notice how returnees and young families compete for the same flats.",
        ],
    },
    vocabulary=[
        vocab("stan", "apartment", "stahn", "noun", "Stan je sunčan."),
        vocab("soba", "room", "SO-ba", "noun", "Soba je velika."),
        vocab("kirija", "rent", "KEE-rya", "noun", "Kirija je mjesečno."),
        vocab("namještaj", "furniture", "nah-MYEH-shtai", "noun", "Namještaj je star."),
        vocab("kuhinja", "kitchen", "koo-HEE-nya", "noun", "Kuhinja je čista."),
        vocab("kupatilo", "bathroom", "koo-pa-TEE-lo", "noun", "Kupatilo je malo."),
        vocab("ključ", "key", "klyooch", "noun", "Gdje je ključ?"),
        vocab("ugovor", "contract", "OO-goh-vor", "noun", "Trebam ugovor."),
        vocab("može", "it is OK or allowed", "MO-zheh", "phrase", "Može. Ulazite."),
        vocab("moraš", "you must", "MO-rash", "verb form", "Moraš platiti kiriju."),
        vocab("mjesečno", "monthly", "myeh-SEHCH-no", "adverb", "Plaćam mjesečno."),
        vocab("pogledati", "to look at", "poh-gleh-DA-tee", "verb", "Želim pogledati stan."),
        vocab("iznajmiti", "to rent", "eez-nai-MEE-tee", "verb", "Želim iznajmiti stan."),
        vocab("koliko je kirija", "how much is the rent", "KO-lee-ko yeh KEE-rya", "phrase", "Koliko je kirija?"),
    ],
    grammar_panels=[
        grammar(
            "Može permission chunks",
            1,
            "Može? asks if something is allowed. Može. answers yes in one calm word. Ne može. refuses without a tense chart. Pair the chunk with ulazite or sjedite when you visit a flat.",
            [
                ("Može? Mogu pogledati stan?", "May I? Can I look at the apartment?"),
                ("Može. Ulazite.", "Yes. Come in."),
                ("Ne može. Nema ključa.", "Not allowed. There is no key."),
            ],
        ),
        grammar(
            "Moraš obligation lines",
            4,
            "Moraš tells one person what they must do now. Add platiti kiriju or imati ugovor right after the chunk. Stay in the present so the landlord talk stays practical.",
            [
                ("Moraš platiti kiriju.", "You must pay the rent."),
                ("Moraš imati ugovor.", "You must have a contract."),
                ("Moraš biti tačan.", "You must be on time."),
            ],
        ),
        grammar(
            "Rent question shape",
            8,
            "Ask Koliko je kirija? when you stand in the hallway. Answer Kirija je mjesečno. Add a number later. The question shape matters more than every case ending today.",
            [
                ("Koliko je kirija?", "How much is the rent?"),
                ("Kirija je mjesečno.", "The rent is monthly."),
                ("Kirija je tri stotine.", "The rent is three hundred."),
            ],
        ),
    ],
    culture_title="Flat hunting in Zenica",
    culture_body=(
        "In Zenica many newcomers hunt flats through word of mouth, online ads, and quick visits after work. "
        "Ana and Emir climb a staircase in a block near the steelworks and imagine a longer stay beyond the guest room above the café. "
        "The landlord opens a bright kitchen and points to a corner where a sofa already waits. "
        "Kirija is discussed in marks per month on a handwritten note taped to the door. "
        "Young families and returnees often compete for the same two-room flats near schools and tram lines. "
        "A polite visit with molim and clear questions about rent can turn a hallway tour into a serious conversation about keys."
    ),
    culture_image="flat-kitchen",
    blocks=[
        {
            "id": "a",
            "title": "Lesson A. Permission and rent questions",
            "body": (
                "Start with stan, soba, and kirija so the hallway has real nouns before you step inside. "
                "Practice Može? Mogu pogledati stan? until the permission chunk sounds natural at a closed door. "
                "Ask Koliko je kirija? while you still wear your shoes in the corridor. "
                "Add kuhinja and kupatilo as you walk through each room. "
                "Ana repeats mjesečno with the landlord while Emir counts windows and checks the light. "
                "Keep može and moraš as spoken lines rather than a modal verb table. "
                "Point at namještaj in the corner and say ima mali sto. "
                "Reuse molim when you enter and hvala when you leave each room. "
                "Say each rent question twice, then thank the landlord with hvala before you step back into the stairwell."
            ),
            "tips": [
                "Keep Može? and the follow-up question in one breath.",
                "Pair kirija with mjesečno when you talk about monthly pay.",
                "Stay in the present even when you plan a longer stay.",
            ],
        },
        {
            "id": "b",
            "title": "Lesson B. Almost signing the lease",
            "body": (
                "Move from the tour to the table where an ugovor waits beside a pen. "
                "Say Moraš platiti kiriju when the landlord explains house rules in plain language. "
                "Describe namještaj with ima and lijep when you point at the sofa corner. "
                "Amira asks about ključ and Ana says Želim iznajmiti stan for three months. "
                "Emir checks that kuhinja i kupatilo su čisti before he nods toward the balcony. "
                "Reuse molim and hvala with the landlord so the scene stays polite end to end. "
                "Practice a short chain aloud. Permission, rent, room names, obligation, thanks, and one calm goodbye at the door. "
                "Repeat the chain until signing feels possible even if you still need one night to decide."
            ),
            "tips": [
                "Reuse Imam from earlier lessons when you claim a favorite room.",
                "Say namještaj slowly. It is a long but useful word.",
                "End with hvala even if you need time to decide.",
            ],
        },
    ],
    conversation={
        "title": "Pogled stana u Zenici",
        "setting": "Ana, Emir, and Amira visit a Zenica flat with the landlord before a possible longer stay.",
        "lines": [
            {"speaker": "Ana", "bosnian": "Dobar dan. Može? Mogu pogledati stan?", "english": "Good day. May I? Can I look at the apartment?"},
            {"speaker": "Landlord", "bosnian": "Može. Ulazite. Ovo je kuhinja.", "english": "Yes. Come in. This is the kitchen."},
            {"speaker": "Emir", "bosnian": "Koliko je kirija mjesečno?", "english": "How much is the rent monthly?"},
            {"speaker": "Amira", "bosnian": "Soba je sunčana. Imam dobar osjećaj.", "english": "The room is sunny. I have a good feeling."},
            {"speaker": "Ana", "bosnian": "Želim iznajmiti stan na tri mjeseca.", "english": "I want to rent the apartment for three months."},
            {"speaker": "Landlord", "bosnian": "Moraš platiti kiriju prvog u mjesecu.", "english": "You must pay the rent on the first of the month."},
            {"speaker": "Emir", "bosnian": "Imamo ugovor i ključ danas?", "english": "Do we have a contract and key today?"},
            {"speaker": "Amira", "bosnian": "Hvala. Razmislimo do večeri.", "english": "Thank you. We will think until evening."},
        ],
    },
    puzzles=[
        {
            "id": "p1",
            "type": "match",
            "title": "Match housing words",
            "prompt": "Match each Bosnian housing word with its English meaning.",
            "items": [
                {"left": "kirija", "right": "rent"},
                {"left": "namještaj", "right": "furniture"},
                {"left": "kuhinja", "right": "kitchen"},
                {"left": "ključ", "right": "key"},
                {"left": "ugovor", "right": "contract"},
            ],
        },
        {
            "id": "p2",
            "type": "truefalse",
            "title": "True or false at the flat",
            "prompt": "Decide whether each sentence matches the lesson.",
            "items": [
                {"statement": "Može. Ulazite. means yes, come in.", "answer": True},
                {"statement": "Moraš platiti kiriju means you must pay the rent.", "answer": True},
                {"statement": "Kupatilo means kitchen.", "answer": False},
                {"statement": "Koliko je kirija? asks about rent.", "answer": True},
            ],
        },
    ],
    practice=[
        {"id": "pr1", "prompt": "Write the Bosnian for May I look at the apartment?", "hint": "Begin with Može?", "answer": "Može? Mogu pogledati stan?"},
        {"id": "pr2", "prompt": "Write the Bosnian for How much is the rent?", "hint": "Use kirija.", "answer": "Koliko je kirija?"},
        {"id": "pr3", "prompt": "Write the Bosnian for You must pay the rent.", "hint": "Begin with Moraš.", "answer": "Moraš platiti kiriju."},
        {"id": "pr4", "prompt": "Write the Bosnian for The kitchen is clean.", "hint": "Use kuhinja and čista.", "answer": "Kuhinja je čista."},
        {"id": "pr5", "prompt": "Write the Bosnian word for furniture.", "hint": "It begins with nam.", "answer": "namještaj"},
        {"id": "pr6", "prompt": "Write the Bosnian for I want to rent the apartment.", "hint": "Use Želim iznajmiti stan.", "answer": "Želim iznajmiti stan."},
        {"id": "pr7", "prompt": "Write the Bosnian for Yes. Come in.", "hint": "Use Može and ulazite.", "answer": "Može. Ulazite."},
    ],
    facts=[
        {"title": "Zenica mixes industry and student life", "body": "Zenica sits in central Bosnia and Herzegovina with factories, university students, and tram lines that shape daily housing hunts. Flats near campus and the steelworks turn over quickly. Learners who visit a block staircase practice real city vocabulary rather than only café small talk."},
        {"title": "Kirija is often monthly", "body": "Rent talk in Bosnia and Herzegovina usually centers on a monthly kirija figure. Landlords may write the number on a note or say it in the hallway. Learning Koliko je kirija? prepares you for that first practical question."},
        {"title": "Može is a door opener", "body": "Može? at a doorway is faster than a long grammar explanation. The answer Može. invites you inside with one calm word. Present permission chunks keep housing visits friendly."},
        {"title": "Namještaj can be light", "body": "Some flats come with basic namještaj while others are empty. A sofa corner and kitchen table are enough to describe a place today. Point and name rather than memorizing a furniture catalog."},
    ],
    resources=[
        {"label": "Learn Bosnian house vocabulary (YouTube)", "url": "https://www.youtube.com/watch?v=lTp-jz2azsI", "note": "Room and house words support flat visits."},
        {"label": "Next lesson", "url": "/learn/lesson/27", "note": "Lesson 27 follows Emir at work and Ana at school."},
        {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the lesson."},
    ],
    quiz=[
        quiz_q("q1", "What does kirija mean?", ["Rent", "Key", "Kitchen", "Contract"], 0, "Kirija means rent.", "vocabulary"),
        quiz_q("q2", "Which line asks permission to enter?", ["Moraš platiti kiriju.", "Može? Mogu pogledati stan?", "Kuhinja je čista.", "Namještaj je star."], 1, "Može? Mogu pogledati stan? asks permission.", "grammar"),
        quiz_q("q3", "What does moraš platiti kiriju mean?", ["You must pay the rent.", "The rent is monthly.", "The key is here.", "Come in."], 0, "Moraš platiti kiriju means you must pay the rent.", "grammar"),
        quiz_q("q4", "Which room word means bathroom?", ["kuhinja", "kupatilo", "soba", "stan"], 1, "Kupatilo means bathroom.", "vocabulary"),
        quiz_q("q5", "Where does the culture scene take place?", ["Zenica", "Neum beach only", "Jajce waterfall only", "Brčko port"], 0, "The flat hunt is set in Zenica.", "culture"),
        quiz_q("q6", "Who speaks as the landlord in the dialogue?", ["Landlord", "Mrvica", "Clerk", "Driver"], 0, "The landlord shows the kitchen and explains rent.", "dialogue"),
        quiz_q("q7", "What civic pressure does this housing lesson highlight?", ["Returnee Bosniaks in Republika Srpska face hostile community pressure", "All rents are free nationwide", "Only Sarajevo has apartments", "Contracts are illegal"], 0, "Returnees especially Bosniaks in Republika Srpska can face hostile community environments.", "culture"),
        quiz_q("q8", "Which word means furniture?", ["ključ", "namještaj", "ugovor", "mjesečno"], 1, "Namještaj means furniture.", "vocabulary"),
        quiz_q("q9", "What does Ana want to do for three months?", ["Rent the apartment", "Buy a bus ticket", "Jump from Stari Most", "Write a novel"], 0, "Ana wants to rent the apartment for three months.", "dialogue"),
    ],
    civic_ctx=civic(
        "Returnee housing still meets quiet hostility",
        "Thousands of Bosniaks who returned to homes in Republika Srpska after the war still meet cold stares, segregated schools, and political rhetoric that treats them as guests rather than citizens. International monitors document pressure on minority communities through blocked employment, disputed property cases, and symbols that celebrate wartime actors. Return is legal on paper, yet daily life can shrink to a few safe streets and family visits. Housing hunts in mixed towns therefore carry quiet fear beneath the rent question. Learners who rent a flat hear how peace agreements and neighborly politeness do not erase structural hostility overnight.",
        "civic-returnee-pressure",
        "Wikipedia article on return of refugees and IDPs in Bosnia and Herzegovina",
        "https://en.wikipedia.org/wiki/Return_of_refugees_and_IDPs_in_Bosnia_and_Herzegovina",
    ),
    listen=authentic_listen(
        "Čuj Bosnu with house and room words",
        "speaker",
        "A short lesson models room vocabulary you can reuse when you tour a flat.",
        "Learn Bosnian - House vocabulary",
        "Learn Bosnian with Elma",
        "Home and room language",
        "https://www.youtube.com/watch?v=lTp-jz2azsI",
        "What is the speaker mainly teaching?",
        ["House and room vocabulary", "Football scores", "Holiday greetings", "Phone emergencies"],
        0,
        "Listen for a room word you could point to during a flat visit.",
        ["soba", "stan"],
        "You do not need every case ending. Catch one room noun you recognize.",
        [("Moja soba je mala.", "My room is small."), ("Stan je sunčan.", "The apartment is sunny.")],
        "After the clip, name one room in your imaginary flat aloud.",
    ),
    speak_targets=[0, 4],
    section=4,
    say_again_block=say_again([
        ("Moja soba je mala.", "My room is small."),
        ("Stan je iznad kafića.", "The apartment is above the café."),
        ("Koliko košta?", "How much does it cost?"),
        ("Hvala, molim.", "Thank you, please."),
    ]),
    image_briefs=[
        "Polygon scene of a bright flat kitchen in Zenica for culture hero flat-kitchen.",
        "Apartment door with a handwritten rent note for apartment-door.",
        "Sofa corner with light namještaj for furniture-corner.",
        "Documentary still on returnee housing pressure for civic-returnee-pressure.",
    ],
)

LESSON_27 = chapter(
    day=27,
    title="Posao i škola",
    title_en="Work and school",
    theme="Emir's guide shift and Ana's study plan",
    story="Emir leads a morning tour in Banja Luka while Ana maps a quiet study week at the university library.",
    goals={
        "vocabulary": [
            "Name posao, škola, radim, and učim for daily routines.",
            "Introduce kolega and student for people at work and campus.",
            "Describe a simple weekday plan in the present.",
        ],
        "grammar": [
            "Use radim and učim as steady present routine verbs.",
            "Ask Gdje radiš? and answer with a workplace chunk.",
            "Link škola plans with želim and danas.",
        ],
        "culture": [
            "Picture campus life in Banja Luka or Mostar without repeating Sarajevo café beats.",
            "Treat guide work and student schedules as parallel routines.",
            "Notice how trams and offices frame a workday postcard.",
        ],
    },
    vocabulary=[
        vocab("posao", "job or work", "PO-sao", "noun", "Posao je dobar."),
        vocab("škola", "school", "SHKOH-la", "noun", "Škola je blizu."),
        vocab("radim", "I work", "RA-deem", "verb form", "Radim svaki dan."),
        vocab("učim", "I study", "OO-cheem", "verb form", "Učim bosanski."),
        vocab("kolega", "colleague", "koh-LEH-ga", "noun", "Kolega je ljubazan."),
        vocab("student", "student", "stoo-DENT", "noun", "Student uči mnogo."),
        vocab("profesor", "professor", "proh-feh-SOR", "noun", "Profesor je strogi."),
        vocab("kancelarija", "office", "kan-tseh-LA-rya", "noun", "Kancelarija je mala."),
        vocab("biblioteka", "library", "bee-blee-oh-TEH-ka", "noun", "Biblioteka je tiha."),
        vocab("raspored", "schedule", "rahs-POR-ed", "noun", "Raspored je pun."),
        vocab("danas", "today", "DA-nahs", "adverb", "Danas radim."),
        vocab("svaki dan", "every day", "SVA-kee dahn", "phrase", "Učim svaki dan."),
        vocab("gdje radiš", "where do you work", "gdyeh RAH-deesh", "phrase", "Gdje radiš?"),
        vocab("imam pauzu", "I have a break", "EE-mam POW-zoo", "phrase", "Imam pauzu u podne."),
    ],
    grammar_panels=[
        grammar(
            "Radim routine lines",
            2,
            "Radim tells what you do for work in the present. Add svaki dan or danas after the verb. Keep the line short so guide shifts and office talk stay sayable.",
            [
                ("Radim kao vodič.", "I work as a guide."),
                ("Radim u kancelariji.", "I work in the office."),
                ("Danas radim rano.", "Today I work early."),
            ],
        ),
        grammar(
            "Učim study chunks",
            5,
            "Učim names what you study now. Pair it with bosanski, u biblioteci, or sa kolegom. Present study plans need no past tense storytelling.",
            [
                ("Učim bosanski.", "I study Bosnian."),
                ("Učim u biblioteci.", "I study in the library."),
                ("Učim svaki dan.", "I study every day."),
            ],
        ),
        grammar(
            "Workplace question shape",
            11,
            "Ask Gdje radiš? to learn where someone works. Answer with u plus a place chunk. The question shape opens polite small talk on a tram or campus path.",
            [
                ("Gdje radiš?", "Where do you work?"),
                ("Radim u turističkoj kancelariji.", "I work in the tourist office."),
                ("Radim kao vodič u Banjoj Luci.", "I work as a guide in Banja Luka."),
            ],
        ),
    ],
    culture_title="Campus and office postcard from Banja Luka",
    culture_body=(
        "Banja Luka mixes tram lines, café breaks, and a university campus where students carry notebooks beside the Vrbas River. "
        "Emir wears a guide badge for morning groups while Ana borrows a desk in the library for Bosnian homework. "
        "Office workers share quick coffee with kolega before the next meeting. "
        "Students compare raspored notes in the hallway and say učim prije ispita. "
        "A mid-size city workday feels calmer than capital rush yet still full of schedules. "
        "Present tense lines about radim and učim let you join that routine without a career memoir."
    ),
    culture_image="guide-badge",
    blocks=[
        {
            "id": "a",
            "title": "Lesson A. Work and study verbs",
            "body": (
                "Open with posao and škola so work and campus share one lesson frame. "
                "Practice Radim kao vodič until Emir's guide shift sounds natural on a busy morning. "
                "Add učim bosanski for Ana's study plan at the biblioteka after lunch. "
                "Name kolega and student when you point at people in the hallway between classes. "
                "Ask Gdje radiš? on the tram and answer with a place chunk that names your office or campus building. "
                "Keep radim and učim as present lines rather than a full conjugation chart on the wall. "
                "Say danas and svaki dan to anchor time without opening future tables. "
                "Say each routine sentence twice, then add hvala when a colleague opens the door for you."
            ),
            "tips": [
                "Pair radim with a place chunk u plus location.",
                "Say učim with the subject you study today.",
                "Reuse molim when you ask a colleague for help.",
            ],
        },
        {
            "id": "b",
            "title": "Lesson B. Schedules on a busy day",
            "body": (
                "Move from verbs to a full weekday raspored on paper beside your coffee cup. "
                "Say Imam pauzu u podne when Emir rests between tour groups in the old town. "
                "Ana tells Amira Želim učiti u biblioteci danas while notebooks stack on the desk. "
                "Emir meets a kolega near the kancelarija and shares a quick plan for the afternoon shift. "
                "Students pass with knjige while a tram bell rings outside the faculty window. "
                "Reuse hvala and vidimo se when the shift ends and the library lamps glow. "
                "Practice a short chain aloud. Work verb, study verb, schedule noun, break phrase, thanks, and one calm goodbye. "
                "Repeat the chain until your own weekday story feels sayable in Bosnian."
            ),
            "tips": [
                "Point at a clock when you say danas or u podne.",
                "Keep answers in the present even for future plans.",
                "Use student and profesor to widen campus talk.",
            ],
        },
    ],
    conversation={
        "title": "Radni dan i biblioteka",
        "setting": "Emir finishes a guide morning in Banja Luka while Ana and Amira plan study time and a colleague shares the office schedule.",
        "lines": [
            {"speaker": "Emir", "bosnian": "Danas radim kao vodič. Imam pun raspored.", "english": "Today I work as a guide. I have a full schedule."},
            {"speaker": "Ana", "bosnian": "Ja učim u biblioteci poslije podne.", "english": "I study in the library after noon."},
            {"speaker": "Amira", "bosnian": "Gdje radiš danas, Emire?", "english": "Where do you work today, Emir?"},
            {"speaker": "Kolega", "bosnian": "Radimo u kancelariji do pet sati.", "english": "We work in the office until five o'clock."},
            {"speaker": "Ana", "bosnian": "Profesor je strogi, ali studenti pomažu.", "english": "The professor is strict, but students help."},
            {"speaker": "Emir", "bosnian": "Imam pauzu. Hajde na kafu.", "english": "I have a break. Let us get coffee."},
            {"speaker": "Kolega", "bosnian": "Dobar plan. Vidimo se u školi.", "english": "Good plan. See you at school."},
            {"speaker": "Amira", "bosnian": "Želim učiti bosanski svaki dan.", "english": "I want to study Bosnian every day."},
        ],
    },
    puzzles=[
        {
            "id": "p1",
            "type": "match",
            "title": "Match work and school words",
            "prompt": "Match each Bosnian word with its English meaning.",
            "items": [
                {"left": "posao", "right": "job"},
                {"left": "učim", "right": "I study"},
                {"left": "kolega", "right": "colleague"},
                {"left": "biblioteka", "right": "library"},
                {"left": "raspored", "right": "schedule"},
            ],
        },
        {
            "id": "p2",
            "type": "truefalse",
            "title": "True or false on routines",
            "prompt": "Decide whether each sentence matches the lesson.",
            "items": [
                {"statement": "Radim means I work.", "answer": True},
                {"statement": "Biblioteka means office.", "answer": False},
                {"statement": "Gdje radiš? asks where someone works.", "answer": True},
                {"statement": "Student means professor.", "answer": False},
            ],
        },
    ],
    practice=[
        {"id": "pr1", "prompt": "Write the Bosnian for I work as a guide.", "hint": "Use Radim kao vodič.", "answer": "Radim kao vodič."},
        {"id": "pr2", "prompt": "Write the Bosnian for I study Bosnian.", "hint": "Use Učim.", "answer": "Učim bosanski."},
        {"id": "pr3", "prompt": "Write the Bosnian for Where do you work?", "hint": "Two words.", "answer": "Gdje radiš?"},
        {"id": "pr4", "prompt": "Write the Bosnian for I have a break at noon.", "hint": "Use Imam pauzu u podne.", "answer": "Imam pauzu u podne."},
        {"id": "pr5", "prompt": "Write the Bosnian word for colleague.", "hint": "It begins with kol.", "answer": "kolega"},
        {"id": "pr6", "prompt": "Write the Bosnian for Today I work early.", "hint": "Begin with Danas.", "answer": "Danas radim rano."},
        {"id": "pr7", "prompt": "Write the Bosnian for I study in the library.", "hint": "Use biblioteka.", "answer": "Učim u biblioteci."},
    ],
    facts=[
        {"title": "Banja Luka trams frame the commute", "body": "Banja Luka workers and students often meet on trams between campus and downtown offices. A guide badge and a notebook bag fit the same morning rhythm. Present tense commute talk keeps the city feel real."},
        {"title": "Radim is a daily anchor", "body": "Radim plus a role or place tells people what you do now. Guides, clerks, and office staff all reuse the same short line. You do not need every case ending to sound employed."},
        {"title": "Biblioteka hours teach patience", "body": "University libraries in Bosnia and Herzegovina can be quiet islands on a loud day. Ana's study plan shows how učim fits academic life without a grammar lecture."},
        {"title": "Kolega opens office small talk", "body": "Naming a kolega humanizes workplace scenes. One polite question about posao can start a friendly break. Keep the tone present and practical."},
    ],
    resources=[
        {"label": "Learn Bosnian telling time (YouTube)", "url": "https://www.youtube.com/watch?v=0xiYbtHQaDc", "note": "Clock phrases help you read work and class schedules."},
        {"label": "Next lesson", "url": "/learn/lesson/28", "note": "Lesson 28 reaches Mostar and the Neretva."},
        {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the lesson."},
    ],
    quiz=[
        quiz_q("q1", "What does radim mean?", ["I work", "I study", "I rent", "I jump"], 0, "Radim means I work.", "vocabulary"),
        quiz_q("q2", "Which line says I study Bosnian?", ["Radim kao vodič.", "Učim bosanski.", "Imam pauzu.", "Gdje radiš?"], 1, "Učim bosanski means I study Bosnian.", "grammar"),
        quiz_q("q3", "What does biblioteka mean?", ["Library", "Office", "Tram", "Contract"], 0, "Biblioteka means library.", "vocabulary"),
        quiz_q("q4", "Where does Emir work as a guide?", ["Banja Luka", "Neum only", "Berlin", "Dublin"], 0, "Emir guides in Banja Luka.", "dialogue"),
        quiz_q("q5", "Which question asks where someone works?", ["Gdje radiš?", "Koliko je kirija?", "Može? Mogu pogledati stan?", "Kakvo je vrijeme?"], 0, "Gdje radiš? asks where you work.", "grammar"),
        quiz_q("q6", "What does kolega mean?", ["Colleague", "Student", "Landlord", "Driver"], 0, "Kolega means colleague.", "vocabulary"),
        quiz_q("q7", "What civic topic does this lesson highlight?", ["Republika Srpska leaders push secessionist rhetoric against state authority", "All schools are closed forever", "Guides are illegal", "Libraries ban Bosnian books"], 0, "Leaders in Republika Srpska continually challenge state-level judicial and police authority.", "culture"),
        quiz_q("q8", "What does Ana do after noon?", ["Studies in the library", "Jumps from Stari Most", "Rents a flat in Zenica", "Buys bus tickets"], 0, "Ana studies in the library after noon.", "dialogue"),
        quiz_q("q9", "Which phrase means I have a break?", ["Imam pauzu", "Imam ugovor", "Imam kiriju", "Imam kartu"], 0, "Imam pauzu means I have a break.", "grammar"),
    ],
    civic_ctx=civic(
        "Republika Srpska rhetoric keeps challenging state authority",
        "Political leaders in Republika Srpska repeatedly float secessionist language and resist rulings from state-level courts and police structures in Bosnia and Herzegovina. Entity institutions celebrate parallel holidays and symbols while ministers question binding decisions from Sarajevo. For young workers and students, that friction shows up as competing news headlines above the same tram line. A routine workday therefore sits inside a constitutional tug-of-war that is louder than a campus schedule yet just as daily.",
        "civic-rs-secession",
        "Wikipedia article on proposed secession of Republika Srpska",
        "https://en.wikipedia.org/wiki/Proposed_secession_of_Republika_Srpska",
    ),
    listen=authentic_listen(
        "Čuj Bosnu with clock phrases for schedules",
        "speaker",
        "A teacher models clock language you can place beside radim and učim.",
        "Learn Bosnian. Telling Time (Sati i Minuti)",
        "Lingo Hero",
        "Clock and schedule language",
        "https://www.youtube.com/watch?v=0xiYbtHQaDc",
        "What is the speaker mainly teaching?",
        ["Telling time and clock language", "Cooking burek", "Phone emergencies", "Holiday greetings"],
        0,
        "Listen for a time phrase you could place beside Imam pauzu.",
        ["sati", "koliko"],
        "Catch the question shape for time rather than every number.",
        [("Koliko je sati?", "What time is it?"), ("Imam pauzu u podne.", "I have a break at noon.")],
        "After the clip, say one work or study line with a time word you know.",
    ),
    speak_targets=[0, 5],
    section=4,
    say_again_block=say_again([
        ("Danas radim.", "Today I work."),
        ("Učim bosanski.", "I study Bosnian."),
        ("Gdje je stanica?", "Where is the station?"),
        ("Hajde da idemo.", "Let us go."),
    ]),
    image_briefs=[
        "Guide badge and morning group in Banja Luka for guide-badge.",
        "Classroom desk with notebooks for classroom-desk.",
        "Office window beside a tram line for office-tram.",
        "News still on Republika Srpska political rally for civic-rs-secession.",
    ],
)

LESSON_28 = chapter(
    day=28,
    title="Mostar napokon!",
    title_en="Mostar at last!",
    theme="Finally Mostar and the cold Neretva dare",
    story="The friends reach Mostar, walk the old town, and debate a jump from Stari Most while the green Neretva flows below.",
    goals={
        "vocabulary": [
            "Name Stari most, Neretva, and most as landmark words.",
            "Use idemo and želim for present travel plans.",
            "React to a skok dare with Neću and present fear lines.",
        ],
        "grammar": [
            "Use Idemo plus destination as a movement chunk.",
            "Say Želim skočiti and Neću! as wanting and refusing lines.",
            "Describe the bridge with je lijep and visok.",
        ],
        "culture": [
            "Picture Stari Most diving tradition and old town stone streets.",
            "Treat the Neretva color as a Herzegovina postcard.",
            "Keep travel talk in the present without past hero stories.",
        ],
    },
    vocabulary=[
        vocab("Mostar", "Mostar", "MOH-star", "proper noun", "Mostar je lijep."),
        vocab("Stari most", "Old Bridge", "STAH-ree most", "noun", "Stari most je visok."),
        vocab("most", "bridge", "most", "noun", "Most je star."),
        vocab("Neretva", "Neretva River", "neh-RET-vah", "proper noun", "Neretva je zelena."),
        vocab("skok", "jump", "skok", "noun", "Skok je opasan."),
        vocab("idemo", "we are going or let us go", "EE-deh-moh", "phrase", "Idemo u Mostar."),
        vocab("želim", "I want", "ZHEH-leem", "verb form", "Želim vidjeti most."),
        vocab("neću", "I do not want to", "NEH-choo", "verb form", "Neću skočiti!"),
        vocab("stari grad", "old town", "STAH-ree grad", "noun", "Stari grad je pun turista."),
        vocab("rijeka", "river", "RYE-ka", "noun", "Rijeka je hladna."),
        vocab("visok", "high or tall", "VEE-sok", "adjective", "Most je visok."),
        vocab("hladan", "cold", "HLA-dahn", "adjective", "Neretva je hladna."),
        vocab("turista", "tourist", "too-REE-sta", "noun", "Turista slika most."),
        vocab("opasan", "dangerous", "oh-PAH-sahn", "adjective", "Skok je opasan."),
    ],
    grammar_panels=[
        grammar(
            "Idemo movement chunk",
            3,
            "Idemo opens a group move in the present. Add u Mostar or na most right after the chunk. Everyone can echo the line on the road south.",
            [
                ("Idemo u Mostar.", "We are going to Mostar."),
                ("Idemo na Stari most.", "We are going to the Old Bridge."),
                ("Idemo polako.", "We are going slowly."),
            ],
        ),
        grammar(
            "Želim wanting lines",
            6,
            "Želim tells what you want now. Add vidjeti most or skočiti as a second verb chunk. Stay in the present so the dare stays playful rather than a saga.",
            [
                ("Želim vidjeti Stari most.", "I want to see the Old Bridge."),
                ("Želim skočiti.", "I want to jump."),
                ("Želim fotografiju.", "I want a photo."),
            ],
        ),
        grammar(
            "Neću refusal chunk",
            9,
            "Neću refuses in one sharp present line. Add skočiti when the Neretva looks too cold. Pair it with opasan for a clear no.",
            [
                ("Neću skočiti!", "I do not want to jump!"),
                ("Neću! Voda je hladna.", "I do not want to! The water is cold."),
                ("Neću. Skok je opasan.", "I do not want to. The jump is dangerous."),
            ],
        ),
    ],
    culture_title="Stari Most and the diving tradition",
    culture_body=(
        "Mostar's Stari Most arches over the green Neretva and anchors the old town skyline. "
        "Young divers train for summer leaps while tourists crowd the stone streets with cameras. "
        "The bridge is more than a photo stop. It is a living ritual that needs calm water and steady nerves. "
        "Ana wants the view while Emir jokes about a skok and Amira keeps both feet on the parapet. "
        "Cold spring water reminds you that courage and weather both matter. "
        "Present tense travel lines let you enjoy the scene without retelling every wartime chapter on the bridge."
    ),
    culture_image="stari-most",
    blocks=[
        {
            "id": "a",
            "title": "Lesson A. Arrival and landmark names",
            "body": (
                "Start with Mostar, Stari most, and Neretva so the map has names before the first photo. "
                "Practice Idemo u Mostar as the group steps off the bus near the old town gate. "
                "Describe visok most and zelena rijeka with short adjective lines you can say while walking. "
                "Point at turista with a camera and say Stari grad je pun ljudi on a sunny afternoon. "
                "Ana repeats želim vidjeti most while Emir looks at the cold water below the parapet. "
                "Keep landmark nouns in the present so the old town feels immediate rather than historical homework. "
                "Reuse molim when you buy water from a seller on the stone street. "
                "Say each place name twice, then add hvala and continue toward the bridge center."
            ),
            "tips": [
                "Stress Stari most as two words learners recognize.",
                "Pair rijeka with hladna when you touch the parapet.",
                "Reuse idemo from earlier invitation lessons.",
            ],
        },
        {
            "id": "b",
            "title": "Lesson B. The jump dare",
            "body": (
                "Move from sightseeing to the playful skok dare above the Neretva. "
                "Emir says Želim skočiti while tourists watch from the stone wall in the breeze. "
                "Ana answers Neću! Voda je hladna and Amira agrees skok je opasan for spring travelers. "
                "A passerby laughs and points at trained divers who wait for warmer summer water. "
                "Keep želim and neću as present lines without future or past storytelling on the parapet. "
                "Practice a short chain aloud. Movement chunk, want line, refuse line, cold water, danger word, thanks. "
                "Repeat the chain until you can enjoy the view without feeling pushed to jump today."
            ),
            "tips": [
                "Say Neću! sharply when you refuse the dare.",
                "Use opasan once so the refusal sounds serious.",
                "Stay polite with molim when you talk to strangers.",
            ],
        },
    ],
    conversation={
        "title": "Hladna Neretva",
        "setting": "Ana, Emir, and Amira stand on Stari Most while a passerby watches the cold Neretva below.",
        "lines": [
            {"speaker": "Ana", "bosnian": "Konačno smo u Mostaru. Stari most je lijep.", "english": "We are finally in Mostar. The Old Bridge is beautiful."},
            {"speaker": "Emir", "bosnian": "Idemo bliže. Želim vidjeti Neretvu.", "english": "Let us go closer. I want to see the Neretva."},
            {"speaker": "Amira", "bosnian": "Rijeka je zelena i hladna danas.", "english": "The river is green and cold today."},
            {"speaker": "Passerby", "bosnian": "Ljeto je za skok. Sada je opasno.", "english": "Summer is for jumping. Now it is dangerous."},
            {"speaker": "Emir", "bosnian": "Želim skočiti. Samo malo!", "english": "I want to jump. Just a little!"},
            {"speaker": "Ana", "bosnian": "Neću skočiti! Voda je prehladna.", "english": "I do not want to jump! The water is too cold."},
            {"speaker": "Amira", "bosnian": "Neću ni ja. Hajde slikati most.", "english": "Me neither. Let us photograph the bridge."},
            {"speaker": "Passerby", "bosnian": "Dobar izbor. Most čeka sunce.", "english": "Good choice. The bridge waits for sun."},
        ],
    },
    puzzles=[
        {
            "id": "p1",
            "type": "match",
            "title": "Match Mostar words",
            "prompt": "Match each Bosnian word with its English meaning.",
            "items": [
                {"left": "most", "right": "bridge"},
                {"left": "rijeka", "right": "river"},
                {"left": "skok", "right": "jump"},
                {"left": "hladan", "right": "cold"},
                {"left": "idemo", "right": "we are going"},
            ],
        },
        {
            "id": "p2",
            "type": "truefalse",
            "title": "True or false in Mostar",
            "prompt": "Decide whether each sentence matches the lesson.",
            "items": [
                {"statement": "Neretva is the river below Stari Most.", "answer": True},
                {"statement": "Neću skočiti means I want to jump.", "answer": False},
                {"statement": "Idemo u Mostar means we are going to Mostar.", "answer": True},
                {"statement": "Skok is safe in cold spring water.", "answer": False},
            ],
        },
    ],
    practice=[
        {"id": "pr1", "prompt": "Write the Bosnian for We are going to Mostar.", "hint": "Use Idemo u Mostar.", "answer": "Idemo u Mostar."},
        {"id": "pr2", "prompt": "Write the Bosnian for I want to see the Old Bridge.", "hint": "Use Želim vidjeti.", "answer": "Želim vidjeti Stari most."},
        {"id": "pr3", "prompt": "Write the Bosnian for I do not want to jump!", "hint": "Use Neću skočiti.", "answer": "Neću skočiti!"},
        {"id": "pr4", "prompt": "Write the Bosnian for The river is cold.", "hint": "Use rijeka and hladna.", "answer": "Rijeka je hladna."},
        {"id": "pr5", "prompt": "Write the Bosnian word for bridge.", "hint": "One syllable.", "answer": "most"},
        {"id": "pr6", "prompt": "Write the Bosnian for The jump is dangerous.", "hint": "Use skok and opasan.", "answer": "Skok je opasan."},
        {"id": "pr7", "prompt": "Write the Bosnian for The Old Bridge is high.", "hint": "Use Stari most and visok.", "answer": "Stari most je visok."},
        {"id": "pr8", "prompt": "Write the Bosnian for Let us go slowly.", "hint": "Use Idemo polako.", "answer": "Idemo polako."},
    ],
    facts=[
        {"title": "Stari Most is a living symbol", "body": "The Old Bridge in Mostar is a UNESCO landmark rebuilt after wartime destruction. Divers and tourists share the same stone view. Learners name it in the present as a place they can visit today."},
        {"title": "Neretva color surprises newcomers", "body": "The Neretva often looks emerald from the parapet. Cold spring water keeps dare jokes short. Hladna rijeka is a useful pair for travel talk."},
        {"title": "Summer diving is seasonal", "body": "Trained divers collect tips for summer leaps. Winter and spring jumps are unsafe for tourists. The passerby line keeps that tradition factual."},
        {"title": "Idemo fits group travel", "body": "Friends echo idemo when they move together through the old town. It reuses an invitation frame from earlier lessons with a new destination."},
    ],
    resources=[
        {"label": "Mostar walking tour (YouTube)", "url": "https://www.youtube.com/watch?v=vxdZQeN6c7A", "note": "Place atmosphere for Stari Most and the old town."},
        {"label": "Next lesson", "url": "/learn/lesson/29", "note": "Lesson 29 sends postcards from Bosnia and Herzegovina."},
        {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the lesson."},
    ],
    quiz=[
        quiz_q("q1", "What river flows under Stari Most?", ["Neretva", "Sava", "Una", "Drina"], 0, "The Neretva flows under Stari Most.", "culture"),
        quiz_q("q2", "Which line means we are going to Mostar?", ["Idemo u Mostar.", "Neću skočiti!", "Radim kao vodič.", "Kirija je mjesečno."], 0, "Idemo u Mostar means we are going to Mostar.", "grammar"),
        quiz_q("q3", "What does Neću skočiti mean?", ["I do not want to jump", "I want to jump", "I work today", "The bridge is high"], 0, "Neću skočiti refuses the jump.", "grammar"),
        quiz_q("q4", "Which adjective means cold?", ["hladan", "visok", "opasan", "zelena"], 0, "Hladan means cold.", "vocabulary"),
        quiz_q("q5", "Who warns that summer is for jumping?", ["Passerby", "Landlord", "Clerk", "Professor"], 0, "A passerby warns about seasonal diving.", "dialogue"),
        quiz_q("q6", "What does želim vidjeti most mean?", ["I want to see the bridge", "I refuse to jump", "I study Bosnian", "I pay rent"], 0, "Želim vidjeti most means I want to see the bridge.", "grammar"),
        quiz_q("q7", "What civic topic ties to Herzegovina pilgrimage tourism?", ["Međugorje Marian apparitions are not church-certified miracles", "All bridges are closed", "Mostar bans tourists", "Neretva is dry year round"], 0, "Međugorje draws pilgrimage tourism while church authorities have not affirmed the apparitions as certified miracles.", "culture"),
        quiz_q("q8", "What does skok mean?", ["Jump", "Bridge", "River", "Ticket"], 0, "Skok means jump.", "vocabulary"),
        quiz_q("q9", "How do Ana and Amira respond to Emir's dare?", ["They refuse because the water is cold", "They jump immediately", "They rent a flat", "They buy bus tickets"], 0, "Ana and Amira refuse because the water is cold and dangerous.", "dialogue"),
    ],
    civic_ctx=civic(
        "Međugorje pilgrimage sits beside careful church judgment",
        "Međugorje in Herzegovina draws millions of Catholic pilgrims and shapes Croatian identity tourism across the region. Since the 1980s reports of Marian apparitions made the village a global faith destination with hotels and tour buses. The Catholic Church allows limited pastoral care and organized pilgrimages yet has not declared the apparitions authenticated miracles under its formal rules. Pilgrimage energy therefore runs ahead of official doctrine while local economies depend on visitors who mix prayer with nationalist symbolism.",
        "civic-medjugorje",
        "Wikipedia article on Međugorje",
        "https://en.wikipedia.org/wiki/Medjugorje",
    ),
    listen=authentic_listen(
        "Čuj Bosnu on the Mostar old bridge",
        "speaker",
        "A walking tour names Stari Most so your ear catches place words before you visit.",
        "Mostar Bosnia 4K Walking Tour | Old Bridge Mostar",
        "Urban Walking Tour",
        "Mostar / Stari Most",
        "https://www.youtube.com/watch?v=vxdZQeN6c7A",
        "What place atmosphere does the clip mainly show?",
        ["Mostar old town and Stari Most", "A ski resort", "A bus station only", "An office hallway"],
        0,
        "Listen for a place name or bridge word you recognize.",
        ["Mostar", "most"],
        "Catch one landmark word rather than every guide sentence.",
        [("Stari most je lijep.", "The Old Bridge is beautiful."), ("Idemo u Mostar.", "We are going to Mostar.")],
        "After the clip, say one travel line with Mostar or most.",
    ),
    speak_targets=[0, 5],
    section=4,
    say_again_block=say_again([
        ("Idemo u Mostar.", "We are going to Mostar."),
        ("Želim vidjeti more.", "I want to see the sea."),
        ("Hajde da idemo.", "Let us go."),
        ("Kakvo je vrijeme?", "How is the weather?"),
    ]),
    image_briefs=[
        "Stari Most arch over the Neretva for stari-most.",
        "Green Neretva water from the parapet for neretva-green.",
        "Cobblestone old town street for mostar-old-town.",
        "Međugorje pilgrimage crowd scene for civic-medjugorje.",
    ],
)

# LESSON_29 and LESSON_30 plus VIDEOS follow in next append.

LESSON_29 = chapter(
    day=29,
    title="Pisma iz BiH",
    title_en="Letters from Bosnia and Herzegovina",
    theme="Ana writes home",
    story="Ana sits in Sarajevo and writes a postcard home with i, ali, and zato linking her present thoughts.",
    goals={
        "vocabulary": [
            "Use pismo, razglednica, and pošta for mail chunks.",
            "Link ideas with i, ali, and zato in short present lines.",
            "Describe Sarajevo sights Ana shares with family abroad.",
        ],
        "grammar": [
            "Build postcard lines with i for addition.",
            "Contrast with ali in one calm present sentence.",
            "Explain a reason with zato in the present.",
        ],
        "culture": [
            "Picture diaspora mail and postcards from Sarajevo.",
            "Mention a memorial visit lightly without owning civic denial content.",
            "Treat letter writing as slow present-tense practice.",
        ],
    },
    vocabulary=[
        vocab("pismo", "letter", "PEES-moh", "noun", "Pišem pismo."),
        vocab("razglednica", "postcard", "raz-GLED-nee-tsa", "noun", "Šaljem razglednicu."),
        vocab("pošta", "post office or mail", "POSH-ta", "noun", "Pošta je blizu."),
        vocab("marka", "stamp", "MAR-ka", "noun", "Treba mi marka."),
        vocab("koverat", "envelope", "KOH-veh-raht", "noun", "Koverat je mali."),
        vocab("adresa", "address", "ah-DREH-sa", "noun", "Ovo je adresa."),
        vocab("poruka", "message", "poh-ROO-ka", "noun", "Poruka je kratka."),
        vocab("i", "and", "ee", "conjunction", "Volim Sarajevo i Mostar."),
        vocab("ali", "but", "AH-lee", "conjunction", "Hladno je, ali lijepo."),
        vocab("zato", "therefore or so", "ZAH-toh", "conjunction", "Zato pišem pismo."),
        vocab("pišem", "I write", "PEE-shem", "verb form", "Pišem pismo danas."),
        vocab("šaljem", "I send", "SHAL-yem", "verb form", "Šaljem razglednicu."),
        vocab("porodica", "family", "poh-ROH-dee-tsa", "noun", "Porodica je daleko."),
        vocab("sjećanje", "memory", "SYEH-chah-nyeh", "noun", "Imam lijepo sjećanje."),
    ],
    grammar_panels=[
        grammar(
            "I linking lines",
            10,
            "Use i to add one more fact in the same present mood. Keep both sides short so a postcard stays readable on a small card.",
            [
                ("Volim kafu i burek.", "I like coffee and burek."),
                ("Pišem pismo i šaljem razglednicu.", "I write a letter and send a postcard."),
                ("Sarajevo je velik i lijep.", "Sarajevo is big and beautiful."),
            ],
        ),
        grammar(
            "Ali contrast chunk",
            7,
            "Ali introduces a contrast without a new tense. Place it between two present facts. The second half often carries the surprise.",
            [
                ("Vrijeme je hladno, ali idem u grad.", "The weather is cold, but I go to the city."),
                ("Želim skočiti, ali neću.", "I want to jump, but I do not want to."),
                ("Grad je bučan, ali siguran.", "The city is loud, but safe."),
            ],
        ),
        grammar(
            "Zato reason line",
            12,
            "Zato gives a simple reason in the present. Use it after a fact your family should understand. One reason per sentence keeps the postcard honest.",
            [
                ("Volim Bosnu i Hercegovinu. Zato pišem.", "I love Bosnia and Herzegovina. That is why I write."),
                ("Sjećanje je jako. Zato šaljem poruku.", "The memory is strong. That is why I send a message."),
                ("Učim bosanski. Zato ostajem.", "I study Bosnian. That is why I stay."),
            ],
        ),
    ],
    culture_title="Postcards and diaspora mail from Sarajevo",
    culture_body=(
        "Families abroad still light up when a razglednica arrives from Sarajevo with a familiar skyline and cramped handwriting. "
        "Ana writes at a small desk near Ferhadija while the tram bell drifts through the window. "
        "She mentions coffee, stone streets, and a quiet memorial memory she carries today rather than a history lecture. "
        "Diaspora relatives read slowly and answer with their own short lines. "
        "Mail is slower than a chat app yet carries tone in every i and ali. "
        "A present tense postcard keeps Ana connected without promising fluent novels overnight."
    ),
    culture_image="postcard-desk",
    blocks=[
        {
            "id": "a",
            "title": "Lesson A. Postcard nouns and verbs",
            "body": (
                "Start with pismo, razglednica, and pošta so the desk has real mail nouns before you write. "
                "Practice Pišem pismo and Šaljem razglednicu as steady present lines at Ana's small table. "
                "Add marka and koverat when you walk to the post office window on Ferhadija. "
                "Ana copies adresa carefully for family abroad and checks the zip line twice. "
                "Name poruka when the card space runs out and you need a shorter thought. "
                "Keep pišem and šaljem as spoken verbs rather than a full conjugation grid at the counter. "
                "Say each mail line twice, then add molim when you buy a marka from the seller."
            ),
            "tips": [
                "Spell adresa slowly at the post office.",
                "Pair razglednica with šaljem in one breath.",
                "Reuse molim when you buy a marka.",
            ],
        },
        {
            "id": "b",
            "title": "Lesson B. I, ali, and zato on the card",
            "body": (
                "Move from nouns to linked ideas on the postcard back in cramped handwriting. "
                "Write Sarajevo je hladno, ali lijep with ali between two present facts your parents understand. "
                "Add Volim grad i učim bosanski with i for a gentle list of good news. "
                "Close with Zato pišem pismo when you explain why the card exists in the mailbox today. "
                "Ana mentions porodica daleko and one calm sjećanje from a memorial she respects. "
                "Amira suggests a shorter poruka for the small space above the skyline photo. "
                "Practice a three-line postcard aloud. Greeting, linked fact, zato closing, then hvala at the post office door."
            ),
            "tips": [
                "Keep ali contrasts short on a small card.",
                "Use zato once so the ending feels clear.",
                "Stay in the present even when memory is heavy.",
            ],
        },
    ],
    conversation={
        "title": "Razglednica za porodicu",
        "setting": "Ana writes a postcard in Sarajevo while Emir and Amira buy stamps from a seller at the post office.",
        "lines": [
            {"speaker": "Ana", "bosnian": "Pišem razglednicu za porodicu.", "english": "I am writing a postcard for my family."},
            {"speaker": "Emir", "bosnian": "Šaljem i pismo sa markom.", "english": "I am sending a letter with a stamp too."},
            {"speaker": "Amira", "bosnian": "Sarajevo je hladno, ali lijepo danas.", "english": "Sarajevo is cold, but beautiful today."},
            {"speaker": "Ana", "bosnian": "Volim grad i učim bosanski.", "english": "I love the city and I study Bosnian."},
            {"speaker": "Seller", "bosnian": "Treba vam marka? Molim.", "english": "Do you need a stamp? Please."},
            {"speaker": "Amira", "bosnian": "Da, molim. Poruka mora biti kratka.", "english": "Yes, please. The message must be short."},
            {"speaker": "Seller", "bosnian": "Evo marke. Sretan put poruci.", "english": "Here is the stamp. Safe journey to the message."},
            {"speaker": "Emir", "bosnian": "Zato pišemo često. Hvala.", "english": "That is why we write often. Thank you."},
        ],
    },
    puzzles=[
        {
            "id": "p1",
            "type": "match",
            "title": "Match mail words",
            "prompt": "Match each Bosnian mail word with its English meaning.",
            "items": [
                {"left": "razglednica", "right": "postcard"},
                {"left": "marka", "right": "stamp"},
                {"left": "koverat", "right": "envelope"},
                {"left": "adresa", "right": "address"},
                {"left": "poruka", "right": "message"},
            ],
        },
        {
            "id": "p2",
            "type": "truefalse",
            "title": "True or false on linking words",
            "prompt": "Decide whether each sentence matches the lesson.",
            "items": [
                {"statement": "Ali introduces a contrast.", "answer": True},
                {"statement": "Zato gives a simple reason.", "answer": True},
                {"statement": "Pišem means I send.", "answer": False},
                {"statement": "I means and.", "answer": True},
            ],
        },
    ],
    practice=[
        {"id": "pr1", "prompt": "Write the Bosnian for I write a letter.", "hint": "Use Pišem pismo.", "answer": "Pišem pismo."},
        {"id": "pr2", "prompt": "Write the Bosnian for I send a postcard.", "hint": "Use Šaljem razglednicu.", "answer": "Šaljem razglednicu."},
        {"id": "pr3", "prompt": "Write the Bosnian for The weather is cold, but beautiful.", "hint": "Use ali.", "answer": "Vrijeme je hladno, ali lijepo."},
        {"id": "pr4", "prompt": "Write the Bosnian for I love the city and I study Bosnian.", "hint": "Use i twice.", "answer": "Volim grad i učim bosanski."},
        {"id": "pr5", "prompt": "Write the Bosnian for That is why I write.", "hint": "Begin with Zato.", "answer": "Zato pišem."},
        {"id": "pr6", "prompt": "Write the Bosnian word for stamp.", "hint": "It begins with mar.", "answer": "marka"},
        {"id": "pr7", "prompt": "Write the Bosnian for I need a stamp.", "hint": "Use Treba mi marka.", "answer": "Treba mi marka."},
        {"id": "pr8", "prompt": "Write the Bosnian for The message is short.", "hint": "Use poruka and kratka.", "answer": "Poruka je kratka."},
    ],
    facts=[
        {"title": "Ferhadija still frames mail walks", "body": "Ana writes near Ferhadija where tram bells and shop fronts mix on one street. A postcard from that desk carries city rhythm in a few lines."},
        {"title": "Razglednica beats a long email for tone", "body": "A handwritten razglednica shows effort diaspora families notice. Short Bosnian lines with i and ali feel personal on a small card."},
        {"title": "Zato closes a thought cleanly", "body": "One zato sentence explains why Ana writes without a grammar lecture. Present reasons keep the postcard readable."},
        {"title": "Memorial visits can stay quiet", "body": "Ana mentions a memorial memory lightly in culture while civic content elsewhere covers denial politics. Letter tone stays respectful and brief."},
    ],
    resources=[
        {"label": "Learn Bosnian greetings (YouTube)", "url": "https://www.youtube.com/watch?v=QkvCVZqRYFY", "note": "Opening lines help postcard greetings."},
        {"label": "Next lesson", "url": "/learn/lesson/30", "note": "Lesson 30 is the Book 1 graduation party."},
        {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Browse more speaker models after you finish the lesson."},
    ],
    quiz=[
        quiz_q("q1", "What does razglednica mean?", ["Postcard", "Stamp", "Bridge", "Rent"], 0, "Razglednica means postcard.", "vocabulary"),
        quiz_q("q2", "Which conjunction means but?", ["i", "ali", "zato", "molim"], 1, "Ali means but.", "grammar"),
        quiz_q("q3", "What does zato pišem mean?", ["That is why I write", "I send a stamp", "The river is cold", "I work today"], 0, "Zato pišem means that is why I write.", "grammar"),
        quiz_q("q4", "Where does Ana write?", ["Sarajevo", "Neum beach only", "Berlin", "Dublin"], 0, "Ana writes in Sarajevo.", "dialogue"),
        quiz_q("q5", "What does šaljem mean?", ["I send", "I jump", "I rent", "I refuse"], 0, "Šaljem means I send.", "vocabulary"),
        quiz_q("q6", "What civic pressure does this lesson highlight?", ["Glorification of convicted war criminals and Srebrenica genocide denial among elites", "All mail is free", "Postcards are illegal", "Sarajevo has no post office"], 0, "Nationalist political elites still glorify convicted war criminals and deny the Srebrenica genocide.", "culture"),
        quiz_q("q7", "Which line uses i correctly?", ["Volim grad i učim bosanski.", "Zato pišem ali marka.", "Neću skočiti most.", "Moraš platiti kiriju."], 0, "Volim grad i učim bosanski links two facts with i.", "grammar"),
        quiz_q("q8", "What does marka mean at the post office?", ["Stamp", "Bridge", "Office", "River"], 0, "Marka means stamp.", "vocabulary"),
        quiz_q("q9", "Why does Amira warn Ana?", ["The message must be short", "The bridge is closed", "Rent is due", "The bus is late"], 0, "Amira says the poruka must be short for the card.", "dialogue"),
        quiz_q("q10", "Who sells the stamp in the dialogue?", ["Seller at the post office", "Landlord", "Passerby", "Professor"], 0, "A seller helps with stamps at the post office.", "dialogue"),
    ],
    civic_ctx=civic(
        "Genocide denial still rewards nationalist elites",
        "Systematic glorification of convicted war criminals and denial of the Srebrenica genocide remain widespread among nationalist political elites in Bosnia and Herzegovina. Public murals, commemorative events, and campaign rhetoric still honor figures courts convicted for mass violence while minimizing or rejecting judicial findings about Srebrenica. That message reaches textbooks, media, and election rallies long after tribunal judgments. Families who lost relatives therefore read postcards home in a public culture that still debates their grief as politics.",
        "civic-genocide-denial",
        "Wikipedia article on Bosnian genocide denial",
        "https://en.wikipedia.org/wiki/Bosnian_genocide_denial",
    ),
    listen=authentic_listen(
        "Čuj Bosnu with greeting lines for postcards",
        "speaker",
        "A short greeting lesson gives opening lines you can place on a postcard.",
        "Learn Bosnian Greetings",
        "Learn Bosnian with Elma",
        "Greeting phrases",
        "https://www.youtube.com/watch?v=QkvCVZqRYFY",
        "What kind of language is the speaker mainly teaching?",
        ["Greetings and opening phrases", "Bus tickets", "Furniture names", "Football rules"],
        0,
        "Listen for a greeting you could write at the top of a card.",
        ["zdravo", "dobar"],
        "Catch one greeting word rather than every phrase.",
        [("Dobar dan.", "Good day."), ("Pišem pismo danas.", "I write a letter today.")],
        "After the clip, write one postcard opening aloud.",
    ),
    speak_targets=[0, 6],
    section=4,
    say_again_block=say_again([
        ("Pišem pismo.", "I write a letter."),
        ("Hvala, molim.", "Thank you, please."),
        ("Volim ovu kafu.", "I love this coffee."),
        ("Sarajevo je lijep.", "Sarajevo is beautiful."),
    ]),
    image_briefs=[
        "Small desk with postcard and pen for postcard-desk.",
        "Stamp on an envelope at the post office for stamp-envelope.",
        "Ferhadija street mood for ferhadija-letter.",
        "Documentary still on genocide denial rhetoric for civic-genocide-denial.",
    ],
)

LESSON_30 = chapter(
    day=30,
    title="Završna proslava",
    title_en="Graduation party",
    theme="Party vocab and Book 1 frame review",
    story="Friends toast Book 1 completion until Mrvica steals the cake from the party table.",
    goals={
        "vocabulary": [
            "Reuse party words torta, slavlje, čaša, and pjeva.",
            "Drill core present frames from the whole book.",
            "Celebrate with čestitam and hvala in polite party talk.",
        ],
        "grammar": [
            "Remember volim, želim, imam, and idemo as book-wide frames.",
            "Switch among question chunks you met in travel, food, and home lessons.",
            "Keep every review line in the present tense.",
        ],
        "culture": [
            "Picture a home party that marks Book 1 graduation.",
            "Let Mrvica's cake heist add comic glue without new grammar systems.",
            "Treat the scene as a speaking celebration rather than a test hall.",
        ],
    },
    vocabulary=[
        vocab("torta", "cake", "TOR-ta", "noun", "Torta je slatka."),
        vocab("slavlje", "celebration", "SLAV-lyeh", "noun", "Slavlje je veselo."),
        vocab("čaša", "glass", "CHAH-shah", "noun", "Čaša je puna."),
        vocab("pjevati", "to sing", "PYEH-vah-tee", "verb", "Pjevamo zajedno."),
        vocab("zabava", "party or fun", "zah-BAH-vah", "noun", "Zabava je kod Amire."),
        vocab("čestitam", "congratulations", "ches-tee-TAHM", "phrase", "Čestitam!"),
        vocab("prijatelj", "friend", "pree-yah-TEL", "noun", "Prijatelj je ovdje."),
        vocab("sretan", "happy or merry", "SREH-tahn", "adjective", "Sretan sam danas."),
        vocab("zajedno", "together", "zah-YED-noh", "adverb", "Pijemo zajedno."),
        vocab("volim", "I like or I love", "VOH-leem", "verb form", "Volim ovu tortu."),
        vocab("želim", "I want", "ZHEH-leem", "verb form", "Želim još torte."),
        vocab("imam", "I have", "EE-mam", "verb form", "Imam čašu."),
        vocab("idemo", "we are going", "EE-deh-moh", "phrase", "Idemo na zabavu."),
    ],
    grammar_panels=[
        grammar(
            "Remember volim and želim",
            1,
            "Volim and želim are book-wide want frames. Add torta, prijatelje, or bosanski after the verb. Keep the pair in the present for party toasts.",
            [
                ("Volim ovu zabavu.", "I love this party."),
                ("Želim još sok.", "I want more juice."),
                ("Volim prijatelje ovdje.", "I love the friends here."),
            ],
        ),
        grammar(
            "Remember imam and idemo",
            4,
            "Imam claims what is in your hand at the table. Idemo moves the group toward cake or music. Both frames built the book and still work tonight.",
            [
                ("Imam čašu.", "I have a glass."),
                ("Imam dobru ideju.", "I have a good idea."),
                ("Idemo na slavlje.", "We are going to the celebration."),
            ],
        ),
        grammar(
            "Remember question switches",
            8,
            "Rotate Koliko košta?, Gdje je?, Kakvo je vrijeme?, and Gdje radiš? as quick review switches. Answer with one present line each. No new charts tonight.",
            [
                ("Koliko košta torta?", "How much does the cake cost?"),
                ("Gdje je torta?", "Where is the cake?"),
                ("Kakvo je vrijeme?", "How is the weather?"),
            ],
        ),
    ],
    culture_title="A home graduation party in Sarajevo",
    culture_body=(
        "Amira clears the table for a small slavlje that marks the end of Book 1 rather than a formal school diploma. "
        "Friends bring šampanjac in čaše while someone starts a song on the phone speaker. "
        "Ana and Emir toast with čestitam and laugh about every lesson from café burek to cold Neretva water. "
        "Mrvica watches the torta with professional interest. "
        "The room mixes Bosnian frames with kitchen warmth. "
        "A graduation party here is present tense joy plus one mischievous cat rather than a grammar exam."
    ),
    culture_image="party-table",
    blocks=[
        {
            "id": "a",
            "title": "Lesson A. Party words and remember panels",
            "body": (
                "Open with torta, slavlje, and čaša so the table feels festive before the first toast. "
                "Review volim and želim with party nouns you already know from food and friend lessons. "
                "Say Čestitam! to Ana and Emir for finishing Book 1 together at Amira's table. "
                "Add pjevati and zajedno when the group sings one chorus from a phone speaker. "
                "Keep remember panels short. One frame, one example, one smile, then the next frame. "
                "Mrvica circles the torta while Amira warns Ne diraj! with a laugh in her voice. "
                "Say each toast line twice, then raise your čaša toward the open window together."
            ),
            "tips": [
                "Reuse molim when you offer cake.",
                "Keep volim and želim in present lines only.",
                "Point at torta when you drill imam.",
            ],
        },
        {
            "id": "b",
            "title": "Lesson B. Book-wide frame drill",
            "body": (
                "Move from party nouns to a fast frame drill around Amira's living room. "
                "Switch among Koliko košta?, Gdje je?, and Kakvo je vrijeme? as joke questions between friends. "
                "Answer with imam, idemo, or radim chunks from earlier lessons without opening any new charts. "
                "Emir says Idemo na balkon while Ana asks Gdje je torta and everyone smiles. "
                "Mrvica steals the cake and Amira shouts Mrvica, ne! across the table. "
                "Everyone laughs and keeps speaking Bosnian anyway because that is the real graduation test tonight. "
                "Practice a victory chain aloud. Toast, question switch, answer, cat shout, hvala, and vidimo se again."
            ),
            "tips": [
                "Treat review as spoken frames rather than silent reading.",
                "Use prijatelj when you thank the group.",
                "End with hvala and vidimo se u Book 2 preview talk.",
            ],
        },
    ],
    conversation={
        "title": "Torta nestaje",
        "setting": "Amira hosts a Book 1 graduation party until Mrvica grabs the cake from the table.",
        "lines": [
            {"speaker": "Amira", "bosnian": "Dobrodošli na slavlje. Torta je na stolu.", "english": "Welcome to the celebration. The cake is on the table."},
            {"speaker": "Ana", "bosnian": "Čestitam svima. Volim ovu zabavu.", "english": "Congratulations to everyone. I love this party."},
            {"speaker": "Emir", "bosnian": "Želim još sok. Imam čašu.", "english": "I want more juice. I have a glass."},
            {"speaker": "Mrvica", "bosnian": "Mrvica gleda tortu.", "english": "Mrvica watches the cake."},
            {"speaker": "Ana", "bosnian": "Gdje je torta? Ne vidim je.", "english": "Where is the cake? I do not see it."},
            {"speaker": "Emir", "bosnian": "Mrvica je brza! Torta je nestala.", "english": "Mrvica is fast! The cake is gone."},
            {"speaker": "Amira", "bosnian": "Mrvica, ne! Ali svi se smiju.", "english": "Mrvica, no! But everyone laughs."},
            {"speaker": "Ana", "bosnian": "Hvala za sve. Idemo dalje zajedno.", "english": "Thank you for everything. We go on together."},
        ],
    },
    puzzles=[
        {
            "id": "p1",
            "type": "match",
            "title": "Match party words",
            "prompt": "Match each Bosnian party word with its English meaning.",
            "items": [
                {"left": "torta", "right": "cake"},
                {"left": "slavlje", "right": "celebration"},
                {"left": "čaša", "right": "glass"},
                {"left": "čestitam", "right": "congratulations"},
                {"left": "zajedno", "right": "together"},
            ],
        },
        {
            "id": "p2",
            "type": "truefalse",
            "title": "True or false review",
            "prompt": "Decide whether each sentence matches the lesson.",
            "items": [
                {"statement": "Volim ovu zabavu means I love this party.", "answer": True},
                {"statement": "Mrvica steals the cake.", "answer": True},
                {"statement": "Idemo means we are going.", "answer": True},
                {"statement": "Book 1 adds past tense storytelling.", "answer": False},
            ],
        },
    ],
    practice=[
        {"id": "pr1", "prompt": "Write the Bosnian for Congratulations!", "hint": "One word.", "answer": "Čestitam!"},
        {"id": "pr2", "prompt": "Write the Bosnian for I love this party.", "hint": "Use Volim ovu zabavu.", "answer": "Volim ovu zabavu."},
        {"id": "pr3", "prompt": "Write the Bosnian for Where is the cake?", "hint": "Use Gdje je torta?", "answer": "Gdje je torta?"},
        {"id": "pr4", "prompt": "Write the Bosnian for I have a glass.", "hint": "Use Imam čašu.", "answer": "Imam čašu."},
        {"id": "pr5", "prompt": "Write the Bosnian for We go on together.", "hint": "Use Idemo dalje zajedno.", "answer": "Idemo dalje zajedno."},
        {"id": "pr6", "prompt": "Write the Bosnian word for celebration.", "hint": "It begins with slav.", "answer": "slavlje"},
        {"id": "pr7", "prompt": "Write the Bosnian for I want more juice.", "hint": "Use Želim još sok.", "answer": "Želim još sok."},
        {"id": "pr8", "prompt": "Write the Bosnian for The cake is sweet.", "hint": "Use torta and slatka.", "answer": "Torta je slatka."},
    ],
    facts=[
        {"title": "Book 1 ends in the present", "body": "Graduation night reviews frames without opening past tense storytelling. That matches the Book 1 pedagogy lock learners followed from Lesson 1."},
        {"title": "Mrvica keeps comic glue", "body": "The cake heist gives Mrvica a party job without new grammar. Cats and torta are memorable review anchors."},
        {"title": "Čestitam fits any toast", "body": "One cheerful čestitam line congratulates friends on language miles. Pair it with hvala for polite celebration."},
        {"title": "Frames travel better than tables", "body": "Volim, želim, imam, and idemo carried learners through cafés, buses, flats, and Mostar. Tonight they share one table."},
    ],
    resources=[
        {"label": "Dino Merlin sings Sredinom", "url": "https://www.youtube.com/watch?v=9NADgl_ukEE", "note": "A familiar song closes Book 1 on a celebratory note."},
        {"label": "Book 1 complete", "url": "/learn", "note": "Return to the course home and preview what comes next."},
        {"label": "How to speak Bosnian channel", "url": "https://www.youtube.com/@HowtospeakBosnian", "note": "Keep practicing with the channel after Book 1."},
    ],
    quiz=[
        quiz_q("q1", "What does torta mean?", ["Cake", "Glass", "Letter", "Bridge"], 0, "Torta means cake.", "vocabulary"),
        quiz_q("q2", "Who steals the cake?", ["Mrvica", "Landlord", "Professor", "Clerk"], 0, "Mrvica steals the cake.", "dialogue"),
        quiz_q("q3", "Which line means I love this party?", ["Volim ovu zabavu.", "Moraš platiti kiriju.", "Neću skočiti!", "Pišem pismo."], 0, "Volim ovu zabavu means I love this party.", "grammar"),
        quiz_q("q4", "What does čestitam mean?", ["Congratulations", "Goodbye", "Rent", "Jump"], 0, "Čestitam means congratulations.", "vocabulary"),
        quiz_q("q5", "Which question asks where the cake is?", ["Gdje je torta?", "Koliko je kirija?", "Gdje radiš?", "Kakvo je vrijeme?"], 0, "Gdje je torta? asks where the cake is.", "grammar"),
        quiz_q("q6", "What civic topic appears in this finale?", ["Night Wolves motorcycle club parades in Republika Srpska", "Free cake for all citizens", "Mostar bans diving", "Postcards are taxed"], 0, "The Kremlin-linked Night Wolves ride in Republika Srpska including entity day events.", "culture"),
        quiz_q("q7", "What does idemo dalje zajedno mean?", ["We go on together", "I rent the flat", "The river is cold", "I send a postcard"], 0, "Idemo dalje zajedno means we go on together.", "grammar"),
        quiz_q("q8", "Which frame means I have?", ["imam", "idem", "skočim", "pišem"], 0, "Imam means I have.", "grammar"),
        quiz_q("q9", "What tense does Book 1 graduation review use?", ["Present tense only", "Past tense only", "Future tense only", "No verbs"], 0, "Book 1 stays in the present tense.", "culture"),
        quiz_q("q10", "Where is the party hosted?", ["At Amira's", "On Stari Most", "In the post office", "On a bus"], 0, "Amira hosts the graduation party.", "dialogue"),
    ],
    civic_ctx=civic(
        "Night Wolves parades signal Kremlin-linked symbolism in Republika Srpska",
        "The Russian Night Wolves motorcycle club maintains close Kremlin ties and faces international sanctions yet still rides through Republika Srpska and Banja Luka, including entity day events with political backing. Their parades mix Orthodox imagery, nationalist flags, and pro-Russian messaging on streets where local politicians welcome the spectacle. For learners finishing Book 1, that guest presence shows how external authoritarian soft power lands inside one entity's public calendar long after the Dayton framework promised a single democratic state.",
        "civic-night-wolves",
        "RFE/RL report on Night Wolves in Republika Srpska",
        "https://www.rferl.org/a/russia-motorcycle-night-wolves-republika-srpska/32215945.html",
    ),
    listen=authentic_listen(
        "Čuj Bosnu with a celebration song",
        "song",
        "A familiar Bosnian song gives a musical ear stretch for graduation night.",
        "Dino Merlin - Sredinom",
        "Dino Merlin",
        "Celebration listening",
        "https://www.youtube.com/watch?v=9NADgl_ukEE",
        "What kind of clip is this?",
        ["A Bosnian song for listening practice", "A bus ticket tutorial", "A rent contract reading", "A grammar table lecture"],
        0,
        "Listen for one word or mood you recognize from earlier lessons.",
        ["sredinom", "bosno"],
        "Catch an anchor word in music rather than every line.",
        [("Čestitam!", "Congratulations!"), ("Volim prijatelje.", "I love friends.")],
        "After the clip, say one party toast line aloud.",
    ),
    speak_targets=[1, 4],
    section=4,
    say_again_block=say_again([
        ("Volim burek.", "I love burek."),
        ("Treba mi karta.", "I need a ticket."),
        ("Idemo u Mostar.", "We are going to Mostar."),
        ("Hvala za sve.", "Thank you for everything."),
    ]),
    image_briefs=[
        "Party table with čaše and torta for party-table.",
        "Mrvica near a missing cake for cake-heist.",
        "Friends raising glasses for friends-toast.",
        "Night Wolves motorcycle parade still for civic-night-wolves.",
    ],
    can_do_checks=[
        {"id": "cd1", "kind": "speak", "prompt": "I can say three Book 1 frames aloud with volim, želim, or imam."},
        {"id": "cd2", "kind": "speak", "prompt": "I can ask one review question with Koliko košta?, Gdje je?, or Kakvo je vrijeme?"},
        {"id": "cd3", "kind": "listen", "prompt": "I can catch one familiar word in the celebration listening clip."},
        {"id": "cd4", "kind": "write", "prompt": "I can write a two-line party toast using lesson vocabulary."},
        {"id": "cd5", "kind": "speak", "prompt": "I can tell the Mrvica cake story in two present tense sentences."},
    ],
)

LESSONS: dict[int, dict] = {
    26: LESSON_26,
    27: LESSON_27,
    28: LESSON_28,
    29: LESSON_29,
    30: LESSON_30,
}

VIDEOS: dict[int, str] = {
    26: """
# Lesson 26 video script for Stanovanje
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN. Lesson 26. Housing
- BS. Stanovanje
- Background. A bright kitchen in a Zenica flat.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 26 is Stanovanje. Ana and Emir visit a Zenica flat and almost sign a monthly lease.
**On screen:** Stanovanje | Lesson 26

### 0:40 Goals
**Narration:** You learn rent words, može permission chunks, and moraš obligation lines for a polite housing visit.
**On screen:** kirija | Može? | Moraš platiti kiriju

### 1:30 Culture hook
**Narration:** Flat hunting in Zenica mixes tram lines, student demand, and handwritten rent notes on apartment doors.
**On screen:** Zenica | kuhinja | kirija | image credits

### 3:00 Lesson A. Permission and rent questions
**Narration:** Ask Može? Mogu pogledati stan? Name kuhinja and kupatilo. Ask Koliko je kirija?
**On screen:** Može? | Koliko je kirija? | mjesečno

### 5:00 Lesson B. Almost signing the lease
**Narration:** Hear moraš platiti kiriju, describe namještaj, and practice ugovor and ključ before you decide.
**On screen:** Moraš platiti kiriju. | namještaj | ugovor

### 6:30 Mini dialogue
**Narration:** Ana, Emir, and Amira tour the flat with the landlord and thank him before evening.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and ask about rent aloud. Continue with Lesson 27, Posao i škola.
**On screen:** Ask about rent | Next lesson is Posao i škola

## End screen
- Link to website `/learn/lesson/26`
- Playlist. Learn Bosnian Book 1
- Image credits appear in the description.
""",
    27: """
# Lesson 27 video script for Posao i škola
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN. Lesson 27. Work and school
- BS. Posao i škola
- Background. A guide badge and campus desk in Banja Luka.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 27 is Posao i škola. Emir leads a guide morning while Ana studies in the library.
**On screen:** Posao i škola | Lesson 27

### 0:40 Goals
**Narration:** You learn radim and učim routines plus Gdje radiš? for polite work talk.
**On screen:** radim | učim | Gdje radiš?

### 1:30 Culture hook
**Narration:** Banja Luka mixes tram commutes, campus hallways, and office breaks beside the Vrbas.
**On screen:** Banja Luka | biblioteka | kolega | image credits

### 3:00 Lesson A. Work and study verbs
**Narration:** Say Radim kao vodič and Učim bosanski. Add kolega and student on the path.
**On screen:** Radim | Učim | kolega

### 5:00 Lesson B. Schedules on a busy day
**Narration:** Use raspored, Imam pauzu u podne, and hvala when the shift ends.
**On screen:** raspored | pauza | vidimo se

### 6:30 Mini dialogue
**Narration:** Emir, Ana, and Amira compare work and study plans before coffee.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and describe your own routine aloud. Continue with Lesson 28, Mostar napokon!
**On screen:** Describe your routine | Next lesson is Mostar napokon!

## End screen
- Link to website `/learn/lesson/27`
- Playlist. Learn Bosnian Book 1
- Image credits appear in the description.
""",
    28: """
# Lesson 28 video script for Mostar napokon!
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN. Lesson 28. Mostar at last!
- BS. Mostar napokon!
- Background. Stari Most over the green Neretva.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 28 is Mostar napokon! The friends reach Stari Most and face a cold river dare.
**On screen:** Mostar napokon! | Lesson 28

### 0:40 Goals
**Narration:** You learn idemo travel chunks, želim wanting lines, and Neću! refusals by the Neretva.
**On screen:** Idemo | Želim | Neću!

### 1:30 Culture hook
**Narration:** Stari Most and summer diving tradition frame the old town. Spring water stays cold for tourists.
**On screen:** Stari most | Neretva | skok | image credits

### 3:00 Lesson A. Arrival and landmark names
**Narration:** Say Idemo u Mostar. Describe visok most and zelena rijeka in present lines.
**On screen:** Idemo u Mostar. | Stari most | rijeka

### 5:00 Lesson B. The jump dare
**Narration:** Hear Želim skočiti, answer Neću! Voda je hladna, and call skok opasan.
**On screen:** Želim skočiti | Neću! | opasan

### 6:30 Mini dialogue
**Narration:** Ana refuses the jump while a passerby explains summer diving.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and name one landmark aloud. Continue with Lesson 29, Pisma iz BiH.
**On screen:** Name a landmark | Next lesson is Pisma iz BiH

## End screen
- Link to website `/learn/lesson/28`
- Playlist. Learn Bosnian Book 1
- Image credits appear in the description.
""",
    29: """
# Lesson 29 video script for Pisma iz BiH
**Length target:** 8 to 10 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN. Lesson 29. Letters from Bosnia and Herzegovina
- BS. Pisma iz BiH
- Background. A postcard desk near Ferhadija in Sarajevo.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 29 is Pisma iz BiH. Ana writes a postcard home with i, ali, and zato.
**On screen:** Pisma iz BiH | Lesson 29

### 0:40 Goals
**Narration:** You learn mail nouns plus linking words for short present tense messages.
**On screen:** razglednica | ali | zato

### 1:30 Culture hook
**Narration:** Diaspora families still smile at handwritten cards from Sarajevo with tram bells in the background.
**On screen:** Ferhadija | pošta | porodica | image credits

### 3:00 Lesson A. Postcard nouns and verbs
**Narration:** Say Pišem pismo and Šaljem razglednicu. Buy marka and koverat at pošta.
**On screen:** Pišem | Šaljem | marka

### 5:00 Lesson B. I, ali, and zato on the card
**Narration:** Link ideas with i, contrast with ali, and close with zato pišem on a small card.
**On screen:** i | ali | zato

### 6:30 Mini dialogue
**Narration:** Ana, Emir, and Amira finish the card and walk to the post office.
**On screen:** Dialogue lines appear in Bosnian and English.

### 8:00 Practice prompt
**Narration:** Pause and write one postcard line aloud. Continue with Lesson 30, Završna proslava.
**On screen:** Write one line | Next lesson is Završna proslava

## End screen
- Link to website `/learn/lesson/29`
- Playlist. Learn Bosnian Book 1
- Image credits appear in the description.
""",
    30: """
# Lesson 30 video script for Završna proslava
**Length target:** 6 to 8 minutes
**Style:** Scenic Bosnian stills with yellow and gold on-screen text.
**Status:** Export when the chapter is `published`.

## Thumbnail text
- EN. Lesson 30. Graduation party
- BS. Završna proslava
- Background. Friends toast at Amira's table before Mrvica grabs the cake.

## Narration and on-screen cues

### 0:00 Cold open
**Narration:** Lesson 30 is Završna proslava. Book 1 ends with a party, a toast, and one cake heist.
**On screen:** Završna proslava | Lesson 30

### 0:40 Goals
**Narration:** You review volim, želim, imam, and idemo plus party words torta and čestitam.
**On screen:** volim | želim | čestitam

### 1:20 Culture hook
**Narration:** Amira hosts a home slavlje where friends celebrate present tense miles from café to Mostar.
**On screen:** slavlje | torta | prijatelji | image credits

### 2:40 Lesson A. Party words and remember panels
**Narration:** Toast with Čestitam! Review volim and želim with torta and čaša.
**On screen:** Čestitam! | Volim ovu zabavu.

### 4:20 Lesson B. Book-wide frame drill
**Narration:** Switch review questions fast. Mrvica steals the torta and everyone laughs.
**On screen:** Gdje je torta? | Mrvica! | hvala

### 5:30 Mini dialogue
**Narration:** The cake disappears. Ana thanks everyone and says idemo dalje zajedno.
**On screen:** Dialogue lines appear in Bosnian and English.

### 6:40 Practice prompt
**Narration:** Pause and say three Book 1 frames aloud. Book 1 is complete. Visit `/learn` for what comes next.
**On screen:** Three frames | Book 1 complete at /learn

## End screen
- Link to website `/learn`
- Playlist. Learn Bosnian Book 1
- Image credits appear in the description.
""",
}

assert set(LESSONS) == set(VIDEOS) == {26, 27, 28, 29, 30}
