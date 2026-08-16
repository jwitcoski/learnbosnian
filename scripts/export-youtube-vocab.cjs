#!/usr/bin/env node
/**
 * Export CapCut pack for a vocab-supplement video.
 * Usage: node scripts/export-youtube-vocab.cjs --day N
 */
const fs = require("fs");
const path = require("path");

const dayArg = process.argv.indexOf("--day");
const day = dayArg >= 0 ? Number(process.argv[dayArg + 1]) : NaN;
if (dayArg < 0 || Number.isNaN(day)) {
  console.error("Usage: node scripts/export-youtube-vocab.cjs --day N");
  process.exit(1);
}

const root = path.join(__dirname, "..");
const dayDir = path.join(
  root,
  "content",
  "book1",
  `day-${String(day).padStart(2, "0")}`
);
const chapterPath = path.join(dayDir, "chapter.json");
if (!fs.existsSync(chapterPath)) {
  console.error("Missing chapter", chapterPath);
  process.exit(1);
}

const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
const outDir = path.join(
  root,
  "exports",
  "youtube-vocab",
  `day-${String(day).padStart(2, "0")}`
);
fs.mkdirSync(outDir, { recursive: true });

const scriptPath = path.join(dayDir, "vocab-video-script.md");
if (!fs.existsSync(scriptPath)) {
  require("child_process").execSync(
    `node "${path.join(__dirname, "generate-vocab-video-scripts.cjs")}" --day ${day}`,
    { stdio: "inherit" }
  );
}
const script = fs.readFileSync(scriptPath, "utf8");
fs.writeFileSync(path.join(outDir, "narration.md"), script);

const cues = [
  `# Vocab supplement cue list. Lesson ${day}`,
  "",
  `Title: ${chapter.title} / ${chapter.titleEn}`,
  `Theme: ${chapter.theme || ""}`,
  "Series: How to Speak Bosnian (supplement)",
  "",
  "## Slide order",
  "1. Title + fixed intro",
  "2. Agenda",
  ...(chapter.grammar || []).map(
    (g, i) => `${3 + i}. Grammar. ${g.title}`
  ),
  `${3 + (chapter.grammar || []).length}. Vocabulary divider`,
  ...((chapter.vocabulary || []).map(
    (v, i) =>
      `${3 + (chapter.grammar || []).length + 1 + i}. ${v.bosnian} · ${v.english}`
  )),
  "Closing. Hvala + learnbosnian.club",
  "",
  "## Narration pattern per word",
  "- Bosnian (slow)",
  "- Bosnian (slow) again",
  "- English definition",
  "- English definition again",
  "",
  "## Thumbnail text",
  `- EN: Lesson ${day}. ${chapter.titleEn}`,
  `- BS: ${chapter.title}`,
  "- Badge: Vocab + grammar",
  "",
  "## Description blurb",
  `How to Speak Bosnian. Lesson ${day} vocab and grammar supplement. ${chapter.title}.`,
  `Full lesson on the site: /learn/lesson/${day}`,
  "This is a drill video, not a full lesson reload.",
  "Channel: https://www.youtube.com/@HowtospeakBosnian",
  "",
  "## B-roll",
  "- Rights-safe Bosnia drone or street footage only (Pexels, Pixabay, Commons).",
  "- Credit clips in the YouTube description.",
  "",
].join("\n");

fs.writeFileSync(path.join(outDir, "cues.md"), cues);

fs.writeFileSync(
  path.join(outDir, "assets.json"),
  JSON.stringify(
    {
      day,
      series: "vocab-supplement",
      title: chapter.title,
      titleEn: chapter.titleEn,
      vocabulary: (chapter.vocabulary || []).map((v) => ({
        bosnian: v.bosnian,
        english: v.english,
        pronunciation: v.pronunciation || null,
      })),
      grammarTitles: (chapter.grammar || []).map((g) => g.title),
    },
    null,
    2
  ) + "\n"
);

fs.writeFileSync(
  path.join(outDir, "CAPCUT.txt"),
  `CapCut / DaVinci. Vocab supplement
1. New 1920x1080 project. Target 5 to 10 minutes.
2. Lay rights-safe BiH drone or street B-roll under the whole timeline.
3. Gold or yellow title text (channel style). One composition per slide from cues.md.
4. Paste narration from narration.md (record or TTS). Slow on Bosnian words.
5. For each vocab card: Bosnian twice (slow), English twice, ~1s gap.
6. End screen → learnbosnian.club/learn/lesson/${day} + Vocab playlist.
7. Export 1080p. Put B-roll credits in the description.
`
);

console.log("Wrote", path.relative(root, outDir));
