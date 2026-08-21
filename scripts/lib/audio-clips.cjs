/**
 * Shared helpers to build stable audio clip IDs from chapter JSON.
 */
const fs = require("fs");
const path = require("path");

function slugify(text) {
  return String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "dj")
    .replace(/č/gi, "c")
    .replace(/ć/gi, "c")
    .replace(/š/gi, "s")
    .replace(/ž/gi, "z")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64) || "clip";
}

function dayPad(day) {
  return String(day).padStart(2, "0");
}

function vocabClipId(book, day, bosnian) {
  return `b${book}-d${dayPad(day)}-vocab-${slugify(bosnian)}`;
}

function dialogueClipId(book, day, lineIndex) {
  return `b${book}-d${dayPad(day)}-dialogue-${String(lineIndex).padStart(2, "0")}`;
}

function grammarVocabClipId(chapter, bosnian) {
  return `g-c${dayPad(chapter)}-vocab-${slugify(bosnian)}`;
}

function grammarDialogueClipId(chapter, lineIndex) {
  return `g-c${dayPad(chapter)}-dialogue-${String(lineIndex).padStart(2, "0")}`;
}

function collectGrammarSpokenLines(chapter) {
  const lines = [];
  const seen = new Set();
  const add = (line) => {
    if (!line || !line.bosnian) return;
    const key = String(line.bosnian).trim().toLowerCase();
    if (!key || seen.has(key)) return;
    seen.add(key);
    lines.push({
      speaker: line.speaker || "Ana",
      bosnian: line.bosnian,
      english: line.english || "",
    });
  };
  add(chapter.knownLine);
  (chapter.look && chapter.look.items ? chapter.look.items : []).forEach(add);
  return lines;
}

function s3KeyForClip(clipId) {
  return `clips/${clipId}`;
}

function loadJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

/** Normalize speaker → { voiceId, gender } (supports legacy string gender map). */
function resolveSpeakerAssignment(genders, speaker) {
  const raw =
    (speaker && genders.speakers && genders.speakers[speaker]) ||
    genders.default ||
    { voiceId: "female-1", gender: "female" };

  if (typeof raw === "string") {
    return {
      voiceId:
        raw === "male" ? "male-1" : raw === "female" ? "female-1" : "female-1",
      gender: raw === "male" ? "male" : raw === "female" ? "female" : "any",
    };
  }

  return {
    voiceId: raw.voiceId || "female-1",
    gender: raw.gender || "female",
  };
}

function buildClipsCatalog(rootDir) {
  const contentDir = path.join(rootDir, "content");
  const voices = loadJson(path.join(contentDir, "audio", "voice-profiles.json"), {
    voices: [],
  });
  const genders = loadJson(
    path.join(contentDir, "audio", "speaker-genders.json"),
    {
      vocabVoiceId: "female-1",
      speakers: {},
      default: { voiceId: "female-1", gender: "female" },
    }
  );

  const vocabVoiceId = genders.vocabVoiceId || "female-1";
  const vocabVoice = (voices.voices || []).find((v) => v.id === vocabVoiceId);
  const vocabGender = vocabVoice?.gender || "female";

  const clips = [];

  for (const bookName of ["book1", "book2", "book3"]) {
    const bookDir = path.join(contentDir, bookName);
    if (!fs.existsSync(bookDir)) continue;

    for (const entry of fs.readdirSync(bookDir).sort()) {
      if (!entry.startsWith("day-")) continue;
      const chapterPath = path.join(bookDir, entry, "chapter.json");
      if (!fs.existsSync(chapterPath)) continue;
      const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
      const book = chapter.book || Number(bookName.replace("book", "")) || 1;
      const day = chapter.day;

      (chapter.vocabulary || []).forEach((v, index) => {
        const id = vocabClipId(book, day, v.bosnian);
        clips.push({
          id,
          book,
          day,
          type: "vocab",
          index,
          bosnian: v.bosnian,
          english: v.english,
          pronunciation: v.pronunciation || "",
          preferredGender: vocabGender,
          assignedVoiceId: vocabVoiceId,
          speaker: null,
          s3Key: s3KeyForClip(id),
        });
      });

      const lines = chapter.conversation?.lines || [];
      lines.forEach((line, index) => {
        const id = dialogueClipId(book, day, index);
        const assignment = resolveSpeakerAssignment(genders, line.speaker);
        clips.push({
          id,
          book,
          day,
          type: "dialogue",
          index,
          bosnian: line.bosnian,
          english: line.english,
          pronunciation: "",
          preferredGender: assignment.gender,
          assignedVoiceId: assignment.voiceId,
          speaker: line.speaker,
          conversationTitle: chapter.conversation?.title || "",
          s3Key: s3KeyForClip(id),
        });
      });
    }
  }

  const grammarDir = path.join(contentDir, "grammar");
  if (fs.existsSync(grammarDir)) {
    for (const entry of fs.readdirSync(grammarDir).sort()) {
      if (!entry.startsWith("chapter-")) continue;
      const chapterPath = path.join(grammarDir, entry, "chapter.json");
      if (!fs.existsSync(chapterPath)) continue;
      const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
      const chNum = chapter.chapter;
      const recorderDay = 80 + chNum;

      (chapter.vocabulary || []).forEach((v, index) => {
        const id = grammarVocabClipId(chNum, v.bosnian);
        clips.push({
          id,
          book: 0,
          day: recorderDay,
          type: "vocab",
          index,
          bosnian: v.bosnian,
          english: v.english,
          pronunciation: v.pronunciation || "",
          preferredGender: vocabGender,
          assignedVoiceId: vocabVoiceId,
          speaker: null,
          track: "grammar",
          grammarChapter: chNum,
          s3Key: s3KeyForClip(id),
        });
      });

      const lines = collectGrammarSpokenLines(chapter);
      lines.forEach((line, index) => {
        const id = grammarDialogueClipId(chNum, index);
        const assignment = resolveSpeakerAssignment(genders, line.speaker);
        clips.push({
          id,
          book: 0,
          day: recorderDay,
          type: "dialogue",
          index,
          bosnian: line.bosnian,
          english: line.english,
          pronunciation: "",
          preferredGender: assignment.gender,
          assignedVoiceId: assignment.voiceId,
          speaker: line.speaker,
          conversationTitle: `Grammar chapter ${chNum}`,
          track: "grammar",
          grammarChapter: chNum,
          s3Key: s3KeyForClip(id),
        });
      });
    }
  }

  const speakerVoices = {};
  for (const [name, raw] of Object.entries(genders.speakers || {})) {
    speakerVoices[name] = resolveSpeakerAssignment(genders, name);
  }

  return {
    generatedAt: new Date().toISOString(),
    voiceProfiles: voices.voices || [],
    speakerGenders: Object.fromEntries(
      Object.entries(speakerVoices).map(([k, v]) => [k, v.gender])
    ),
    speakerVoices,
    vocabVoiceId,
    total: clips.length,
    clips,
  };
}

module.exports = {
  slugify,
  dayPad,
  vocabClipId,
  dialogueClipId,
  grammarVocabClipId,
  grammarDialogueClipId,
  collectGrammarSpokenLines,
  s3KeyForClip,
  buildClipsCatalog,
  resolveSpeakerAssignment,
};
