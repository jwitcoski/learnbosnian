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

function s3KeyForClip(clipId) {
  return `clips/${clipId}`;
}

function loadJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function buildClipsCatalog(rootDir) {
  const contentDir = path.join(rootDir, "content");
  const voices = loadJson(path.join(contentDir, "audio", "voice-profiles.json"), {
    voices: [],
  });
  const genders = loadJson(
    path.join(contentDir, "audio", "speaker-genders.json"),
    { speakers: {}, default: "any" }
  );

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
          // Female 1 is the main vocab voice-over
          preferredGender: "female",
          speaker: null,
          s3Key: s3KeyForClip(id),
        });
      });

      const lines = chapter.conversation?.lines || [];
      lines.forEach((line, index) => {
        const id = dialogueClipId(book, day, index);
        const preferredGender =
          genders.speakers[line.speaker] || genders.default || "any";
        clips.push({
          id,
          book,
          day,
          type: "dialogue",
          index,
          bosnian: line.bosnian,
          english: line.english,
          pronunciation: "",
          preferredGender,
          speaker: line.speaker,
          conversationTitle: chapter.conversation?.title || "",
          s3Key: s3KeyForClip(id),
        });
      });
    }
  }

  return {
    generatedAt: new Date().toISOString(),
    voiceProfiles: voices.voices || [],
    speakerGenders: genders.speakers || {},
    total: clips.length,
    clips,
  };
}

module.exports = {
  slugify,
  dayPad,
  vocabClipId,
  dialogueClipId,
  s3KeyForClip,
  buildClipsCatalog,
};
