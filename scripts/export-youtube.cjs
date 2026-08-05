#!/usr/bin/env node
/**
 * Export YouTube pack for a chapter (run after human approve / publish).
 * Usage: node scripts/export-youtube.cjs --day 1
 */
const fs = require("fs");
const path = require("path");

const dayArg = process.argv.indexOf("--day");
const day = dayArg >= 0 ? Number(process.argv[dayArg + 1]) : NaN;
if (!day || Number.isNaN(day)) {
  console.error("Usage: node scripts/export-youtube.cjs --day N");
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
if (chapter.status !== "published" && chapter.status !== "draft") {
  console.warn(
    `Warning: status is "${chapter.status}". Prefer exporting after publish.`
  );
}

const outDir = path.join(
  root,
  "exports",
  "youtube",
  `day-${String(day).padStart(2, "0")}`
);
fs.mkdirSync(outDir, { recursive: true });

const scriptPath = path.join(dayDir, "video-script.md");
const script = fs.existsSync(scriptPath)
  ? fs.readFileSync(scriptPath, "utf8")
  : `# Lesson ${day} — ${chapter.title}\n\n_No video-script.md yet._\n`;

fs.writeFileSync(path.join(outDir, "narration.md"), script);

const cues = [
  `# On-screen cue list — Lesson ${day}`,
  "",
  `Title: ${chapter.title} / ${chapter.titleEn}`,
  `Theme: ${chapter.theme}`,
  "",
  "## Vocabulary cards",
  ...(chapter.vocabulary || []).map(
    (v) => `- ${v.bosnian} — ${v.english}${v.pronunciation ? ` (${v.pronunciation})` : ""}`
  ),
  "",
  "## Grammar titles",
  ...(chapter.grammar || []).map((g) => `- ${g.title}`),
  "",
  "## Dialogue lines",
  ...((chapter.conversation && chapter.conversation.lines) || []).map(
    (l) => `- ${l.speaker}: ${l.bosnian}`
  ),
  "",
  "## Thumbnail text",
  `- EN: Lesson ${day} — ${chapter.titleEn}`,
  `- BS: ${chapter.title}`,
  "",
  "## Description blurb",
  `Learn Bosnian in 30 Days — Lesson ${day}: ${chapter.title}.`,
  `Lesson on the site: /learn/lesson/${day}`,
  `Channel: https://www.youtube.com/@HowtospeakBosnian`,
  "",
  "## Image credits",
  ...(chapter.images || []).map((i) => `- ${i.credit} (${i.pageUrl || i.sourceUrl})`),
].join("\n");

fs.writeFileSync(path.join(outDir, "cues.md"), cues + "\n");
fs.writeFileSync(
  path.join(outDir, "assets.json"),
  JSON.stringify(
    {
      day,
      title: chapter.title,
      images: chapter.images || [],
      localImageDir: "frontend/public/images/book1",
    },
    null,
    2
  ) + "\n"
);

fs.writeFileSync(
  path.join(outDir, "CAPCUT.txt"),
  `CapCut / DaVinci quick steps
1. New 1920x1080 project; 8–10 min timeline.
2. Drop scenic stills from assets.json (Ken Burns zoom).
3. Yellow/gold title text matching channel style.
4. Paste narration.md into TTS (Piper or CapCut voice) or record.
5. Overlay cue cards from cues.md.
6. End screen → website /learn/lesson/${day} + playlist.
7. Export 1080p; upload SRT from narration.
`
);

console.log(`YouTube pack written to ${outDir}`);
