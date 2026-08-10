#!/usr/bin/env node
/**
 * Attach rights-checkable YouTube embeds to Lessons 0–7 Čuj Bosnu blocks.
 * Run: node scripts/set-cuj-youtube.cjs && node scripts/sync-content.cjs
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "content", "book1");

/** Verified via YouTube oembed. Avoids the course "How to speak Bosnian" channel. */
const EMBEDS = {
  0: {
    kind: "speaker",
    title: "Čuj Bosnu: one language, three names",
    hook: "Lesson 0 is about what Bosnian is. Hear a real explainer that compares Bosnian, Croatian, and Serbian so your ear meets the neighborhood of the language.",
    source: {
      title: "Bosnian VS Croatian VS Serbian VS Montenegro!",
      artistOrSpeaker: "Croatian with Mirsad",
      regionOrScene: "Language orientation",
      year: "2021",
      license: "YouTube Terms of Service (embed)",
      credit: "Croatian with Mirsad on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=YCXy9xAFTBg",
      embedUrl: "https://www.youtube.com/watch?v=YCXy9xAFTBg",
    },
    durationHint: "watch 60–90 seconds, then gist",
    listenTask: {
      prompt: "Play the video. Listen for the idea that these standards are close, then pause.",
      gistQuestion: {
        prompt: "What is the clip mainly comparing?",
        options: [
          "Coffee recipes only",
          "Bosnian, Croatian, and Serbian (and neighbors)",
          "Only mountain names",
          "Only football clubs",
        ],
        correctIndex: 1,
      },
      targetWords: ["bosanski", "jezik"],
      noticePrompt: "You do not need every word. Catch that the languages sit close together.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Bosanski jezik.", english: "The Bosnian language." },
        { bosnian: "Razumijemo se.", english: "We understand each other." },
      ],
      teacherNote:
        "This course stays Bosnian-focused after Lesson 0. Use the clip to calm the identity question, then move on.",
    },
  },
  1: {
    kind: "song",
    title: "Čuj Bosnu: Bembaša sings Sarajevo",
    hook: "Leave the studio voice for a classic Sarajevo sevdah. Himzo Polovina sings Kad ja pođoh na Bembašu.",
    source: {
      title: "Kad ja pođoh na Bentbašu",
      artistOrSpeaker: "Himzo Polovina",
      regionOrScene: "Sarajevo / Bembaša",
      license: "YouTube Terms of Service (embed)",
      credit: "Himzo Polovina — Topic / archival performance on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=ZXtzoqMn3Lg",
      embedUrl: "https://www.youtube.com/watch?v=ZXtzoqMn3Lg",
    },
    durationHint: "45–90 seconds of the song",
    listenTask: {
      prompt: "Play the song. Feel the pace before hunting for words.",
      gistQuestion: {
        prompt: "What kind of clip is this?",
        options: [
          "A sports radio shout",
          "A warm traditional song (sevdah)",
          "A weather robot",
          "A silent map",
        ],
        correctIndex: 1,
      },
      targetWords: ["Sarajevo", "zdravo"],
      noticePrompt: "Sevdah stretches vowels. Your classroom zdravo will be shorter.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Kad ja pođoh na Bembašu…", english: "When I went to Bembaša…" },
        { bosnian: "Sarajevo.", english: "Sarajevo." },
      ],
      teacherNote:
        "Bembaša is a Sarajevo place in song. Today’s win is the mood plus any greeting word you catch later in the lesson.",
    },
  },
  2: {
    kind: "speaker",
    title: "Čuj Bosnu: Ja sam… in a real teacher voice",
    hook: "Hear someone walk through Ja sam and self-introduction patterns outside our Ana/Emir studio takes.",
    source: {
      title: "Bosnian Grammar: How to Say 'I am' (Ja sam) - Introducing Yourself",
      artistOrSpeaker: "Lingo Hero",
      regionOrScene: "Introductions",
      license: "YouTube Terms of Service (embed)",
      credit: "Lingo Hero on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=CUUGzc3C1G8",
      embedUrl: "https://www.youtube.com/watch?v=CUUGzc3C1G8",
    },
    durationHint: "45–60 seconds",
    listenTask: {
      prompt: "Listen for the chunk Ja sam…",
      gistQuestion: {
        prompt: "What is the speaker teaching?",
        options: [
          "How to order pizza only",
          "How to say I am… / introduce yourself",
          "How to dive from Stari Most",
          "How to bake hljeb only",
        ],
        correctIndex: 1,
      },
      targetWords: ["ja", "sam"],
      noticePrompt: "Grab Ja sam + NAME as one piece.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Ja sam Ana.", english: "I am Ana." },
        { bosnian: "Drago mi je.", english: "Nice to meet you." },
      ],
      teacherNote:
        "Even if the clip uses another name, the frame Ja sam + NAME is today’s win.",
    },
  },
  3: {
    kind: "speaker",
    title: "Čuj Bosnu: kahva with a Sarajevo guide",
    hook: "Café talk is Bosnia’s classroom. A local guide walks you through traditional Bosnian coffee.",
    source: {
      title: "Bosnian Coffee - Explore Sarajevo with Local Guides",
      artistOrSpeaker: "Meet Bosnia Tours (Edin)",
      regionOrScene: "Sarajevo café / kahva",
      license: "YouTube Terms of Service (embed)",
      credit: "Meet Bosnia Tours on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=wFGbkVzNCFU",
      embedUrl: "https://www.youtube.com/watch?v=wFGbkVzNCFU",
    },
    durationHint: "60–90 seconds",
    listenTask: {
      prompt: "Listen for kahva / coffee ritual words, even in English-framed talk.",
      gistQuestion: {
        prompt: "Where does this speech feel at home?",
        options: [
          "A quiet exam hall only",
          "A café / coffee ritual",
          "A hospital ER",
          "A math lecture only",
        ],
        correctIndex: 1,
      },
      targetWords: ["kahva", "molim"],
      noticePrompt: "Orders stay short. molim softens the ask.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Kahvu, molim.", english: "A coffee, please." },
        { bosnian: "Hvala.", english: "Thank you." },
      ],
      teacherNote:
        "Café noise and bilingual guides are real life. Gist listening beats perfect transcription.",
    },
  },
  4: {
    kind: "song",
    title: "Čuj Bosnu: a song for majka",
    hook: "Family words live in songs too. Listen to Tebi majko misli lete and catch the warm majka sound.",
    source: {
      title: "Tebi majko misli lete - Sementa Rajhard",
      artistOrSpeaker: "Sementa Rajhard",
      regionOrScene: "Family / majka",
      license: "YouTube Terms of Service (embed)",
      credit: "Sementa Rajhard performance on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=QkvCVZqRYFY",
      embedUrl: "https://www.youtube.com/watch?v=QkvCVZqRYFY",
    },
    durationHint: "45–90 seconds",
    listenTask: {
      prompt: "Listen for majka or the warm mother-directed tone.",
      gistQuestion: {
        prompt: "What fits the clip’s mood?",
        options: [
          "Cold technical manual",
          "Warm song aimed at mother / family feeling",
          "Airport gate change only",
          "Silent meditation app",
        ],
        correctIndex: 1,
      },
      targetWords: ["majka", "porodica"],
      noticePrompt: "Gender endings like -a often mark feminine nouns you met today.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Majko…", english: "Mother…" },
        { bosnian: "To je moja porodica.", english: "That is my family." },
      ],
      teacherNote:
        "If you missed the full lyric, you still practiced listening for family vocabulary.",
    },
  },
  5: {
    kind: "speaker",
    title: "Čuj Bosnu: Mostar on camera",
    hook: "Travel talk names places. Walk Mostar and Stari Most with a 4K tour and listen for place atmosphere.",
    source: {
      title: "Mostar Bosnia 4K Walking Tour | Old Bridge Mostar",
      artistOrSpeaker: "Urban Walking Tour",
      regionOrScene: "Mostar / Stari Most",
      license: "YouTube Terms of Service (embed)",
      credit: "Urban Walking Tour on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=vxdZQeN6c7A",
      embedUrl: "https://www.youtube.com/watch?v=vxdZQeN6c7A",
    },
    durationHint: "60–90 seconds of the walk",
    listenTask: {
      prompt: "Watch the bridge and streets. Listen for any tour voice naming Mostar.",
      gistQuestion: {
        prompt: "What place is this clip oriented around?",
        options: [
          "A Mostar / Old Bridge travel scene",
          "A bakery only",
          "A coding tutorial",
          "A silent chess match",
        ],
        correctIndex: 0,
      },
      targetWords: ["Mostar", "gdje"],
      noticePrompt: "Place names stay clear even when speech is fast or sparse.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Gdje je Mostar?", english: "Where is Mostar?" },
        { bosnian: "Mostar je tamo.", english: "Mostar is over there." },
      ],
      teacherNote: "Map language is short. Gdje + place is enough for today.",
    },
  },
  6: {
    kind: "speaker",
    title: "Čuj Bosnu: sati in real teaching speech",
    hook: "Schedules need clock phrases. Hear sati i minuti explained in Bosnian lesson speech.",
    source: {
      title: "Learn Bosnian: Telling Time (Sati i Minuti)",
      artistOrSpeaker: "Lingo Hero",
      regionOrScene: "Daily time / clocks",
      license: "YouTube Terms of Service (embed)",
      credit: "Lingo Hero on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=0xiYbtHQaDc",
      embedUrl: "https://www.youtube.com/watch?v=0xiYbtHQaDc",
    },
    durationHint: "45–60 seconds",
    listenTask: {
      prompt: "Listen for sati or a number + time feel.",
      gistQuestion: {
        prompt: "What kind of information is this clip carrying?",
        options: [
          "Mostly telling time / clock language",
          "Only mountain climbing ads",
          "Only classical physics",
          "Only animal sounds",
        ],
        correctIndex: 0,
      },
      targetWords: ["sati", "jutro"],
      noticePrompt: "Time phrases are chunks: Koliko je sati?",
    },
    reveal: {
      keyLines: [
        { bosnian: "Koliko je sati?", english: "What time is it?" },
        { bosnian: "Dobro jutro.", english: "Good morning." },
      ],
      teacherNote:
        "If numbers blur, keep the question frame. You can answer with a known hour.",
    },
  },
  7: {
    kind: "song",
    title: "Čuj Bosnu: Bosno moja for week one",
    hook: "Close the week with a classic love-of-Bosnia sevdah. Beba Selimović sings Bosno moja, divna, mila.",
    source: {
      title: "Beba Selimović - Bosno moja, divna, mila",
      artistOrSpeaker: "Beba Selimović",
      regionOrScene: "Week 1 review / BiH",
      license: "YouTube Terms of Service (embed)",
      credit: "Beba Selimović performance on YouTube",
      pageUrl: "https://www.youtube.com/watch?v=OXul62dILOo",
      embedUrl: "https://www.youtube.com/watch?v=OXul62dILOo",
    },
    durationHint: "60–90 seconds",
    listenTask: {
      prompt: "Listen for Bosna / warm chorus energy, plus any Week 1 word that sneaks in later.",
      gistQuestion: {
        prompt: "What is this review clip?",
        options: [
          "A traditional song about Bosnia",
          "A silent spreadsheet",
          "Only English ads",
          "Only typing sounds",
        ],
        correctIndex: 0,
      },
      targetWords: ["Bosna", "hvala", "zdravo"],
      noticePrompt: "Review listening is retrieval. Familiar beats count as wins.",
    },
    reveal: {
      keyLines: [
        { bosnian: "Bosno moja, divna, mila…", english: "My Bosnia, wonderful, dear…" },
        { bosnian: "Hvala.", english: "Thank you." },
      ],
      teacherNote:
        "Week 1 closed with a real ear stretch. Keep one song in your pocket for the bus.",
    },
  },
};

for (let day = 0; day <= 7; day += 1) {
  const file = path.join(
    ROOT,
    `day-${String(day).padStart(2, "0")}`,
    "chapter.json"
  );
  const ch = JSON.parse(fs.readFileSync(file, "utf8"));
  const block = EMBEDS[day];
  ch.authenticListen = {
    ...(ch.authenticListen || {}),
    ...block,
    source: { ...(ch.authenticListen?.source || {}), ...block.source },
    listenTask: block.listenTask,
    reveal: block.reveal,
  };
  fs.writeFileSync(file, `${JSON.stringify(ch, null, 2)}\n`);
  console.log("updated", day, block.source.embedUrl);
}
console.log("done");
