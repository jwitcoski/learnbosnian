#!/usr/bin/env node
/**
 * Patch Lessons 0–7 with authenticListen, quiz skill tags, speakTargets, canDoChecks.
 * Run: node scripts/patch-pedagogy-content.cjs
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "content", "book1");

const AUTH = {
  0: {
    title: "Čuj Bosnu: a first real voice",
    kind: "speaker",
    hook: "Before Ana lands, hear Bosnian outside a classroom: a short public talk about language and home.",
    source: {
      title: "Bosnian language (overview talk excerpt)",
      artistOrSpeaker: "Public cultural speaker",
      regionOrScene: "Orientation / BiH",
      license: "YouTube Terms of Service (embed)",
      credit: "Educational overview linked via Wikipedia context on Bosnian language",
      pageUrl: "https://en.wikipedia.org/wiki/Bosnian_language",
    },
    durationHint: "60–90 seconds",
    listenTask: {
      prompt: "Listen once without reading. Do not hunt for every word.",
      gistQuestion: {
        prompt: "What is this clip mainly about?",
        options: [
          "Cooking recipes",
          "Language and identity",
          "Football scores",
          "Weather only"
        ],
        correctIndex: 1
      },
      targetWords: ["bosanski", "jezik"],
      noticePrompt: "Notice how clear vowels feel even when you miss some words."
    },
    reveal: {
      keyLines: [
        { bosnian: "Bosanski jezik.", english: "The Bosnian language." },
        { bosnian: "Dobrodošli.", english: "Welcome." }
      ],
      teacherNote: "You do not need full comprehension yet. Train the ear for rhythm and a few anchors."
    }
  },
  1: {
    title: "Čuj Bosnu: greetings in song",
    kind: "song",
    hook: "Sarajevo mornings start with sound. Hear a sevdah-tinged greeting mood, then catch one clear word.",
    source: {
      title: "Sevdalinka (traditional love song tradition)",
      artistOrSpeaker: "Traditional sevdah repertoire",
      regionOrScene: "Sarajevo / sevdah",
      license: "YouTube Terms of Service (embed)",
      credit: "Traditional sevdah repertoire; context via Wikipedia Sevdalinka",
      pageUrl: "https://en.wikipedia.org/wiki/Sevdalinka",
    },
    durationHint: "45–90 seconds",
    listenTask: {
      prompt: "Play a short stretch. Listen for mood first, words second.",
      gistQuestion: {
        prompt: "What feeling fits this clip best?",
        options: ["Angry sports chant", "Warm / nostalgic song", "Robot GPS voice", "Kids counting only"],
        correctIndex: 1
      },
      targetWords: ["zdravo", "Sarajevo"],
      noticePrompt: "Sevdah often feels intimate and unhurried. That pacing helps beginners."
    },
    reveal: {
      keyLines: [
        { bosnian: "Zdravo.", english: "Hello." },
        { bosnian: "Sarajevo.", english: "Sarajevo." }
      ],
      teacherNote: "Song vowels stretch. Your classroom zdravo will be shorter and clearer."
    }
  },
  2: {
    title: "Čuj Bosnu: saying who you are",
    kind: "speaker",
    hook: "People introduce themselves every day. Hear a natural self-introduction cadence.",
    source: {
      title: "Short self-introduction (public interview bite)",
      artistOrSpeaker: "Interview speaker",
      regionOrScene: "Everyday speech",
      license: "YouTube Terms of Service (embed)",
      credit: "Public interview-style speech; pedagogical excerpt via embed",
      pageUrl: "https://en.wikipedia.org/wiki/Bosnia_and_Herzegovina",
    },
    durationHint: "45–60 seconds",
    listenTask: {
      prompt: "Listen for a name pattern: Ja sam…",
      gistQuestion: {
        prompt: "What is the speaker doing?",
        options: ["Ordering pizza only", "Introducing themselves", "Reading a train timetable", "Singing opera"],
        correctIndex: 1
      },
      targetWords: ["ja", "sam"],
      noticePrompt: "Ja sam… is a chunk. Grab it as one piece."
    },
    reveal: {
      keyLines: [
        { bosnian: "Ja sam Ana.", english: "I am Ana." },
        { bosnian: "Drago mi je.", english: "Nice to meet you." }
      ],
      teacherNote: "Even if the clip uses another name, the frame Ja sam + NAME is today’s win."
    }
  },
  3: {
    title: "Čuj Bosnu: kahva talk",
    kind: "speaker",
    hook: "Café talk is Bosnia’s classroom. Hear coffee-house speech and listen for kahva.",
    source: {
      title: "Café / coffee culture talk",
      artistOrSpeaker: "Café culture speaker",
      regionOrScene: "Baščaršija café",
      license: "YouTube Terms of Service (embed)",
      credit: "Coffee culture media; context via Bosnian coffee traditions",
      pageUrl: "https://en.wikipedia.org/wiki/Bosnian_coffee",
    },
    durationHint: "45–90 seconds",
    listenTask: {
      prompt: "Listen for kahva or numbers near an order.",
      gistQuestion: {
        prompt: "Where does this speech feel at home?",
        options: ["A quiet library only", "A café / social pause", "A hospital ER", "A math exam"],
        correctIndex: 1
      },
      targetWords: ["kahva", "molim"],
      noticePrompt: "Orders are short. molim softens the ask."
    },
    reveal: {
      keyLines: [
        { bosnian: "Kahvu, molim.", english: "A coffee, please." },
        { bosnian: "Hvala.", english: "Thank you." }
      ],
      teacherNote: "Café noise is real life. Gist listening matters more than perfect transcription."
    }
  },
  4: {
    title: "Čuj Bosnu: family words in song",
    kind: "song",
    hook: "Family words show up in songs and toasts. Listen for majka, otac, or a warm chorus.",
    source: {
      title: "Folk / family-themed song excerpt",
      artistOrSpeaker: "Folk repertoire",
      regionOrScene: "Family gatherings",
      license: "YouTube Terms of Service (embed)",
      credit: "Folk repertoire embed; cultural context",
      pageUrl: "https://en.wikipedia.org/wiki/Music_of_Bosnia_and_Herzegovina",
    },
    durationHint: "45–90 seconds",
    listenTask: {
      prompt: "Do not translate everything. Catch one family word if it appears, or the warm tone.",
      gistQuestion: {
        prompt: "What fits the clip’s mood?",
        options: ["Cold technical manual", "Warm song / gathering feel", "Airport gate change only", "Silent meditation"],
        correctIndex: 1
      },
      targetWords: ["majka", "otac", "porodica"],
      noticePrompt: "Gender endings (-a) often mark feminine nouns you met today."
    },
    reveal: {
      keyLines: [
        { bosnian: "To je moja porodica.", english: "That is my family." },
        { bosnian: "Moja majka.", english: "My mother." }
      ],
      teacherNote: "If you missed the exact lyric, you still practiced listening for family vocabulary."
    }
  },
  5: {
    title: "Čuj Bosnu: Mostar on the map",
    kind: "speaker",
    hook: "Travel talk names places. Listen for Mostar, map words, or south/north cues.",
    source: {
      title: "Travel / Mostar place talk",
      artistOrSpeaker: "Travel speaker",
      regionOrScene: "Mostar / Herzegovina",
      license: "YouTube Terms of Service (embed)",
      credit: "Travel media embed; place context via Mostar article",
      pageUrl: "https://en.wikipedia.org/wiki/Mostar",
    },
    durationHint: "45–90 seconds",
    listenTask: {
      prompt: "Listen for a place name you know: Mostar.",
      gistQuestion: {
        prompt: "What is the clip oriented around?",
        options: ["A place / travel description", "Baking bread only", "Computer code", "Silent chess"],
        correctIndex: 0
      },
      targetWords: ["Mostar", "gdje"],
      noticePrompt: "Place names stay clear even in fast speech."
    },
    reveal: {
      keyLines: [
        { bosnian: "Gdje je Mostar?", english: "Where is Mostar?" },
        { bosnian: "Mostar je tamo.", english: "Mostar is over there." }
      ],
      teacherNote: "Map language is short. Gdje + place is enough for today."
    }
  },
  6: {
    title: "Čuj Bosnu: time in real speech",
    kind: "speaker",
    hook: "Schedules and small talk use clock phrases. Listen for sati or a time-of-day greeting.",
    source: {
      title: "Everyday time / schedule talk",
      artistOrSpeaker: "Everyday speaker",
      regionOrScene: "Daily routines",
      license: "YouTube Terms of Service (embed)",
      credit: "Everyday speech embed for time listening practice",
      pageUrl: "https://en.wikipedia.org/wiki/Time",
    },
    durationHint: "45–60 seconds",
    listenTask: {
      prompt: "Listen for a number + time feel, even if you miss the exact minute.",
      gistQuestion: {
        prompt: "What kind of information is this clip carrying?",
        options: ["Mostly timing / daily life talk", "Only mountain climbing gear ads", "Only classical physics", "Only animal sounds"],
        correctIndex: 0
      },
      targetWords: ["sati", "jutro"],
      noticePrompt: "Time phrases are chunks: Koliko je sati?"
    },
    reveal: {
      keyLines: [
        { bosnian: "Koliko je sati?", english: "What time is it?" },
        { bosnian: "Dobro jutro.", english: "Good morning." }
      ],
      teacherNote: "If numbers blur, keep the question frame. You can answer with a gesture and a known hour."
    }
  },
  7: {
    title: "Čuj Bosnu: week-one ear stretch",
    kind: "song",
    hook: "Review week: one more song so your ear leaves the studio voices behind.",
    source: {
      title: "Bosnian / regional song medley mood",
      artistOrSpeaker: "Regional song repertoire",
      regionOrScene: "Week 1 review",
      license: "YouTube Terms of Service (embed)",
      credit: "Song embed for review listening; music of BiH context",
      pageUrl: "https://en.wikipedia.org/wiki/Music_of_Bosnia_and_Herzegovina",
    },
    durationHint: "60–90 seconds",
    listenTask: {
      prompt: "Listen for any Week 1 word: greeting, hvala, or a place name.",
      gistQuestion: {
        prompt: "Did you catch at least one familiar Week 1 sound or word?",
        options: ["Yes, something felt familiar", "No, total silence", "Only English ads", "Only typing sounds"],
        correctIndex: 0
      },
      targetWords: ["zdravo", "hvala", "Sarajevo"],
      noticePrompt: "Review listening is retrieval. Familiar beats count as wins."
    },
    reveal: {
      keyLines: [
        { bosnian: "Zdravo.", english: "Hello." },
        { bosnian: "Hvala.", english: "Thank you." },
        { bosnian: "Doviđenja.", english: "Goodbye." }
      ],
      teacherNote: "Week 1 closed with a real ear stretch. Keep one song in your pocket for the bus."
    }
  }
};

function guessSkill(q) {
  const t = `${q.question} ${(q.options || []).join(" ")}`.toLowerCase();
  if (/baščaršija|mostar|sarajevo|culture|bosnia|kahva culture|bazaar|bridge|sebilj|jajce|blagaj/.test(t)) {
    return "culture";
  }
  if (/dialogue|who says|emir|ana|amira|conversation|line/.test(t)) return "dialogue";
  if (/conjugate|biti|gender|moj|moja|ending|alphabet|č vs|grammar|present|verb|case|gdje\/|u\/na/.test(t)) {
    return "grammar";
  }
  if (/hear|listen|sound|pronounc/.test(t)) return "listening";
  return "vocabulary";
}

function defaultCanDo(day) {
  if (day !== 7) return undefined;
  return [
    { id: "cd1", kind: "speak", prompt: "Greet someone with zdravo or dobar dan aloud." },
    { id: "cd2", kind: "speak", prompt: "Say Ja sam… and your name." },
    { id: "cd3", kind: "listen", prompt: "Understand kahvu, molim in a slow line without reading English first." },
    { id: "cd4", kind: "speak", prompt: "Ask Gdje je… about a place on a map." },
    { id: "cd5", kind: "write", prompt: "Type three Week 1 words with correct čćšžđ." }
  ];
}

function patchDay(day) {
  const file = path.join(ROOT, `day-${String(day).padStart(2, "0")}`, "chapter.json");
  const ch = JSON.parse(fs.readFileSync(file, "utf8"));
  ch.authenticListen = AUTH[day];
  if (ch.sectionQuiz?.questions) {
    ch.sectionQuiz.questions = ch.sectionQuiz.questions.map((q) => ({
      ...q,
      skill: q.skill || guessSkill(q),
    }));
  }
  if (ch.conversation?.lines?.length) {
    const targets = [];
    ch.conversation.lines.forEach((line, i) => {
      const sp = (line.speaker || "").toLowerCase();
      if (sp === "narrator" || sp === "mrvica") return;
      if (targets.length < 3) targets.push(i);
    });
    ch.speakTargets = targets;
  }
  const canDo = defaultCanDo(day);
  if (canDo) ch.canDoChecks = canDo;
  fs.writeFileSync(file, `${JSON.stringify(ch, null, 2)}\n`);
  console.log("patched", file);
}

for (let d = 0; d <= 7; d += 1) patchDay(d);
console.log("done");
