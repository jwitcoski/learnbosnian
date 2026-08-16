#!/usr/bin/env node
/**
 * Generate vocab-supplement video scripts from chapter.json.
 * Supplement series: intro → short grammar → vocab (slow ×2 + definition ×2) → ending.
 *
 * Usage:
 *   node scripts/generate-vocab-video-scripts.cjs
 *   node scripts/generate-vocab-video-scripts.cjs --day 1
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const bookDir = path.join(root, "content", "book1");

const dayArg = process.argv.indexOf("--day");
const onlyDay = dayArg >= 0 ? Number(process.argv[dayArg + 1]) : null;

function firstSentence(text) {
  const cleaned = String(text || "")
    .replace(/\u2014|\u2013/g, ".")
    .replace(/\s+/g, " ")
    .trim();
  const m = cleaned.match(/^(.+?[.!?])(\s|$)/);
  let s = m ? m[1].trim() : cleaned.slice(0, 160).trim();
  if (s.length > 180) s = s.slice(0, 177).trim() + ".";
  return s;
}

function tipLine(panel) {
  return firstSentence(panel.explanation);
}

function estimateMinutes(vocabCount, grammarCount) {
  const intro = 0.4;
  const grammar = Math.max(0.5, grammarCount * 0.35);
  const vocab = vocabCount * (20 / 60);
  const ending = 0.35;
  const total = intro + grammar + vocab + ending;
  const low = Math.max(5, Math.round(total - 0.5));
  const high = Math.min(10, Math.max(low + 1, Math.round(total + 0.8)));
  return { low, high, total: Math.round(total * 10) / 10 };
}

function speakTitle(text) {
  return String(text || "")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/[.!?,;:]+$/g, "");
}

function nextLessonLine(day) {
  if (day >= 30) {
    return "That’s all for Lesson 30 and Book 1 vocab. Keep practicing on learnbosnian.club.";
  }
  if (day === 0) {
    return "That’s all for Lesson 0. Practice these words on learnbosnian.club, then continue with Lesson 1 on the site.";
  }
  return `That’s all for Lesson ${day}. Practice these words on learnbosnian.club, then continue with Lesson ${day + 1} on the site.`;
}

function buildScript(chapter) {
  const day = chapter.day;
  const title = chapter.title;
  const titleEn = chapter.titleEn || title;
  const vocab = chapter.vocabulary || [];
  const grammar = chapter.grammar || [];
  const timing = estimateMinutes(vocab.length, grammar.length);

  const lines = [];
  lines.push(`# Lesson ${day} vocab supplement. ${title}`);
  lines.push("");
  lines.push(`**Series:** How to Speak Bosnian (vocab supplement, not a full lesson reload)`);
  lines.push(`**Length target:** ${timing.low} to ${timing.high} minutes (est. ~${timing.total} min at drill pace)`);
  lines.push(`**Style:** Gold or yellow text over rights-safe Bosnia drone or street B-roll`);
  lines.push(`**Words:** ${vocab.length} · **Grammar panels:** ${grammar.length}`);
  lines.push("");
  lines.push("## Thumbnail text");
  lines.push(`- EN. Lesson ${day}. ${titleEn}`);
  lines.push(`- BS. ${title}`);
  lines.push("- Badge. Vocab + grammar");
  lines.push("");
  lines.push("## Slide deck and narration");
  lines.push("");
  lines.push("### Slide 1. Title");
  lines.push("**On screen:**");
  lines.push("- How to Speak Bosnian");
  lines.push(`- Lesson ${day}`);
  lines.push(`- ${title}`);
  lines.push(`- ${titleEn}`);
  lines.push("**Narration:**");
  lines.push(
    `Hi and welcome to How to Speak Bosnian. Today we will be going over the vocab and grammar of Lesson ${day}, ${speakTitle(titleEn)}. ${speakTitle(title)}.`
  );
  lines.push("");
  lines.push("### Slide 2. Agenda");
  lines.push("**On screen:**");
  lines.push("- Today");
  lines.push("- Short grammar");
  lines.push("- Vocabulary drill");
  lines.push("**Narration:**");
  lines.push(
    "This video is a quick supplement. We will preview the grammar, then I will say each word slowly twice and the English meaning twice."
  );
  lines.push("");

  grammar.forEach((panel, i) => {
    const tip = tipLine(panel);
    lines.push(`### Slide ${3 + i}. Grammar. ${panel.title}`);
    lines.push("**On screen:**");
    lines.push(`- ${panel.title}`);
    lines.push(`- ${tip}`);
    lines.push("**Narration:**");
    if (i === 0) {
      lines.push(`First, grammar. ${panel.title}. ${firstSentence(panel.explanation)}`);
    } else {
      lines.push(`${panel.title}. ${firstSentence(panel.explanation)}`);
    }
    lines.push("");
  });

  const vocabDividerNum = 3 + grammar.length;
  lines.push(`### Slide ${vocabDividerNum}. Vocabulary`);
  lines.push("**On screen:**");
  lines.push("- Vocabulary");
  lines.push(`- ${vocab.length} words`);
  lines.push("**Narration:**");
  lines.push("Now the vocabulary. Repeat after me in your head, or out loud.");
  lines.push("");

  vocab.forEach((v, i) => {
    const slideNum = vocabDividerNum + 1 + i;
    const en = v.english;
    const pron = v.pronunciation ? ` (${v.pronunciation})` : "";
    lines.push(`### Slide ${slideNum}. ${v.bosnian}`);
    lines.push("**On screen:**");
    lines.push(`- ${v.bosnian}`);
    lines.push(`- ${en}`);
    if (v.pronunciation) lines.push(`- ${v.pronunciation}`);
    lines.push("**Narration:**");
    lines.push(`${v.bosnian}. ${v.bosnian}. ${en}. ${en}.`);
    lines.push("");
  });

  const closeNum = vocabDividerNum + 1 + vocab.length;
  lines.push(`### Slide ${closeNum}. Closing`);
  lines.push("**On screen:**");
  lines.push("- Hvala");
  lines.push("- learnbosnian.club");
  if (day < 30) {
    lines.push(`- Next. Lesson ${day === 0 ? 1 : day + 1}`);
  } else {
    lines.push("- Book 1 complete");
  }
  lines.push("**Narration:**");
  lines.push(`${nextLessonLine(day)} Hvala, and doviđenja!`);
  lines.push("");
  lines.push("## CapCut notes");
  lines.push("- Keep B-roll under the text. Prefer rights-safe BiH drone or street clips (Pexels, Pixabay, Commons).");
  lines.push("- Leave ~1 second of silence between word cards.");
  lines.push("- No Cyrillic on screen.");
  lines.push("- Full lesson (dialogue, puzzles, culture) stays on the website.");
  lines.push("");
  lines.push("## Word checklist");
  vocab.forEach((v) => {
    const pron = v.pronunciation ? ` · ${v.pronunciation}` : "";
    lines.push(`- [ ] ${v.bosnian} · ${v.english}${pron}`);
  });
  lines.push("");

  return lines.join("\n");
}

function listDays() {
  return fs
    .readdirSync(bookDir)
    .filter((d) => d.startsWith("day-"))
    .sort()
    .map((d) => Number(d.replace("day-", "")));
}

const days = onlyDay != null && !Number.isNaN(onlyDay) ? [onlyDay] : listDays();
let written = 0;

for (const day of days) {
  const dayDir = path.join(bookDir, `day-${String(day).padStart(2, "0")}`);
  const chapterPath = path.join(dayDir, "chapter.json");
  if (!fs.existsSync(chapterPath)) {
    console.warn("Skip missing", chapterPath);
    continue;
  }
  const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
  const out = path.join(dayDir, "vocab-video-script.md");
  fs.writeFileSync(out, buildScript(chapter));
  written += 1;
  console.log("Wrote", path.relative(root, out));
}

console.log(`Done. ${written} vocab supplement script(s).`);
