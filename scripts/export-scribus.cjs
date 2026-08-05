#!/usr/bin/env node
/**
 * Export published (or draft preview) chapters for Scribus / print layout.
 * Usage: node scripts/export-scribus.cjs [--all-drafts]
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const bookDir = path.join(root, "content", "book1");
const outDir = path.join(root, "exports", "scribus", "book1");
const includeDrafts = process.argv.includes("--all-drafts");

fs.mkdirSync(outDir, { recursive: true });

function loadChapters() {
  const days = fs
    .readdirSync(bookDir)
    .filter((d) => d.startsWith("day-"))
    .sort();
  return days.map((d) =>
    JSON.parse(fs.readFileSync(path.join(bookDir, d, "chapter.json"), "utf8"))
  );
}

const chapters = loadChapters().filter((c) =>
  includeDrafts
    ? c.status === "published" || c.status === "draft"
    : c.status === "published" || c.status === "draft"
);

let markdown = `# Learn Bosnian in 30 Days — Book 1\n\nExport generated ${new Date().toISOString()}\n\n`;
const dict = [];
const imageManifest = [];

for (const ch of chapters) {
  if (ch.status === "outlined") continue;
  markdown += `\n---\n\n# Day ${ch.day}: ${ch.title}\n\n`;
  markdown += `**English title:** ${ch.titleEn}\n\n`;
  markdown += `**Theme:** ${ch.theme}\n\n`;
  markdown += `**Status:** ${ch.status}\n\n`;
  markdown += `## Goals\n\n`;
  markdown += `### Vocabulary\n${(ch.learningGoals.vocabulary || [])
    .map((x) => `- ${x}`)
    .join("\n")}\n\n`;
  markdown += `### Grammar\n${(ch.learningGoals.grammar || [])
    .map((x) => `- ${x}`)
    .join("\n")}\n\n`;
  markdown += `### Culture\n${(ch.learningGoals.culture || [])
    .map((x) => `- ${x}`)
    .join("\n")}\n\n`;

  if (ch.culture) {
    markdown += `## Culture — ${ch.culture.title}\n\n${ch.culture.body}\n\n`;
  }

  if (ch.vocabulary?.length) {
    markdown += `## Vocabulary\n\n| Bosnian | English | Pronunciation |\n|---------|---------|---------------|\n`;
    for (const v of ch.vocabulary) {
      markdown += `| ${v.bosnian} | ${v.english} | ${v.pronunciation || ""} |\n`;
    }
    markdown += `\n`;
  }

  for (const g of ch.grammar || []) {
    markdown += `## Grammar — ${g.title}\n\n${g.explanation}\n\n`;
    for (const ex of g.examples || []) {
      markdown += `- **${ex.bosnian}** — ${ex.english}\n`;
    }
    markdown += `\n`;
  }

  for (const b of ch.lessonBlocks || []) {
    markdown += `## ${b.title}\n\n${b.body}\n\n`;
  }

  if (ch.conversation?.lines?.length) {
    markdown += `## Conversation — ${ch.conversation.title}\n\n_${ch.conversation.setting}_\n\n`;
    for (const line of ch.conversation.lines) {
      markdown += `**${line.speaker}:** ${line.bosnian}  \n*${line.english}*\n\n`;
    }
  }

  for (const f of ch.funFacts || []) {
    markdown += `### Fun fact — ${f.title}\n\n${f.body}\n\n`;
  }

  for (const e of ch.dictionaryEntries || []) {
    dict.push({ ...e, day: e.day || ch.day });
  }
  for (const img of ch.images || []) {
    imageManifest.push({ day: ch.day, ...img });
  }

  const dayFile = path.join(outDir, `day-${String(ch.day).padStart(2, "0")}.md`);
  fs.writeFileSync(
    dayFile,
    markdown.split(`# Day ${ch.day}:`)[1]
      ? `# Day ${ch.day}:` + markdown.split(`# Day ${ch.day}:`)[1]
      : markdown
  );
}

dict.sort((a, b) => a.bosnian.localeCompare(b.bosnian, "bs"));
const vocabCsv = ["bosnian,english,partOfSpeech,day"]
  .concat(
    dict.map(
      (e) =>
        `"${e.bosnian.replace(/"/g, '""')}","${e.english.replace(/"/g, '""')}","${
          e.partOfSpeech || ""
        }",${e.day}`
    )
  )
  .join("\n");

fs.writeFileSync(path.join(outDir, "book1-full.md"), markdown);
fs.writeFileSync(path.join(outDir, "dictionary.csv"), vocabCsv + "\n");
fs.writeFileSync(
  path.join(outDir, "images-manifest.json"),
  JSON.stringify(imageManifest, null, 2) + "\n"
);
fs.writeFileSync(
  path.join(outDir, "README.txt"),
  `Scribus import pack for Book 1
1. Open or create a .sla with kilim-inspired master pages (crimson/brown/sage).
2. Place book1-full.md section by section (or per day-XX.md).
3. Insert images from frontend/public/images/book1 using images-manifest.json credits in the appendix.
4. Append dictionary.csv as the mini-dictionary A–Ž.
`
);

console.log(`Wrote Scribus pack to ${outDir} (${chapters.length} chapters)`);
