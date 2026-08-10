#!/usr/bin/env node
/**
 * Normalize Book 1 lesson copy:
 * - Replace em/en dashes used as punctuation
 * - Strip website-only "accent button" instructions from chapter JSON
 * - Rename review lesson titles that still say Sedmica/Week
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const bookDir = path.join(root, "content", "book1");

function fixDashes(s) {
  if (typeof s !== "string") return s;
  let t = s;
  t = t.replace(/How to speak Bosnian — YouTube/g, "How to speak Bosnian (YouTube)");
  t = t.replace(/Based on photo: ([^—\n]+) — /g, "Based on photo: $1. ");
  t = t.replace(/Based on map: ([^—\n]+) — /g, "Based on map: $1. ");
  t = t.replace(/Lesson ([AB]) — /g, "Lesson $1: ");
  t = t.replace(/Lesson (\d+) — /g, "Lesson $1: ");
  // Paired appositives: "foo — bar — baz" → "foo (bar) baz"
  t = t.replace(/(\w[\w'’]*)\s*—\s*([^—\n]{1,40}?)\s*—\s*/g, "$1 ($2) ");
  // Gloss pairs in examples / dialogue: "BS — EN" inside short fragments → "BS: EN"
  t = t.replace(/(\b[\wčćšžđČĆŠŽĐ'’]+)\s*—\s*(?=[A-Z])/g, "$1: ");
  // Remaining em/en dashes between clauses → period + space (full sentences)
  t = t.replace(/\s*—\s*/g, ". ");
  t = t.replace(/\s*–\s*/g, ". ");
  t = t.replace(/\.\s*\./g, ".");
  t = t.replace(/\?\s*\./g, "?");
  t = t.replace(/!\s*\./g, "!");
  t = t.replace(/:\s*\./g, ".");
  t = t.replace(/\s{2,}/g, " ");
  return t;
}

function stripAccentUi(s) {
  if (typeof s !== "string") return s;
  let t = s;
  t = t.replace(/On this site,[^.]*\.\s*/gi, "");
  t = t.replace(/When you type answers here,[^.]*\.\s*/gi, "");
  t = t.replace(/Tap those accents when you practice typing\./gi, "Write the special letters carefully when you practice.");
  t = t.replace(/use the accent buttons under the box for č ć š ž đ/gi, "write č ć š ž đ correctly");
  t = t.replace(/[Uu]se the accent buttons?/g, "include the special letter");
  t = t.replace(/tap č ć š ž đ \(and capitals\) to insert the letter at your cursor\.?\s*/gi, "");
  t = t.replace(/tap đ under the answer box/gi, "type đ");
  t = t.replace(/type c then tap č on the accent bar \(or long-press c on phone\)/gi, "needs č");
  t = t.replace(/needs š and č; use the accent buttons/gi, "needs š and č");
  t = t.replace(/Needs the accent button when typing\./gi, "Needs the letter đ.");
  t = t.replace(/The letter đ needs the accent button when typing\./gi, "The letter đ must be written correctly.");
  return t;
}

function walk(value, key) {
  if (typeof value === "string") {
    // Keep image credits readable but dash-free
    let out = fixDashes(value);
    if (
      key === "explanation" ||
      key === "body" ||
      key === "hint" ||
      key === "prompt" ||
      key === "tips" ||
      key === "title" ||
      key === "note" ||
      key === "label" ||
      key === "english" ||
      key === "bosnian" ||
      key === "setting" ||
      key === "storyBeat" ||
      key === "theme" ||
      key === "reviewerNotes" ||
      key === "question" ||
      key === "statement"
    ) {
      out = stripAccentUi(out);
    }
    return out;
  }
  if (Array.isArray(value)) return value.map((v) => walk(v, key));
  if (value && typeof value === "object") {
    const next = {};
    for (const [k, v] of Object.entries(value)) next[k] = walk(v, k);
    return next;
  }
  return value;
}

const reviewTitles = {
  7: { title: "Ponavljanje", titleEn: "Review" },
  14: { title: "Ponavljanje", titleEn: "Review" },
  21: { title: "Ponavljanje", titleEn: "Review" },
};

for (const day of fs.readdirSync(bookDir).filter((d) => d.startsWith("day-"))) {
  const fp = path.join(bookDir, day, "chapter.json");
  if (!fs.existsSync(fp)) continue;
  let ch = JSON.parse(fs.readFileSync(fp, "utf8"));
  ch = walk(ch);
  const n = ch.day;
  if (reviewTitles[n]) {
    ch.title = reviewTitles[n].title;
    ch.titleEn = reviewTitles[n].titleEn;
  }
  // Remove Week N / Sedmica N from theme/notes soft pass
  const scrubWeek = (s) =>
    typeof s === "string"
      ? s
          .replace(/Week\s*\d+\s*/gi, "")
          .replace(/Sedmica\s*\d+\s*/gi, "")
          .replace(/\s{2,}/g, " ")
          .trim()
      : s;
  ch.theme = scrubWeek(ch.theme);
  ch.reviewerNotes = scrubWeek(ch.reviewerNotes);
  fs.writeFileSync(fp, JSON.stringify(ch, null, 2) + "\n");
  console.log("fixed", day);
}

// outline review titles
const outlinePath = path.join(bookDir, "outline.json");
const outline = JSON.parse(fs.readFileSync(outlinePath, "utf8"));
for (const d of outline.days || []) {
  if (reviewTitles[d.day]) {
    d.title = reviewTitles[d.day].title;
    d.titleEn = reviewTitles[d.day].titleEn;
  }
  if (typeof d.title === "string") d.title = fixDashes(d.title);
  if (typeof d.titleEn === "string") d.titleEn = fixDashes(d.titleEn);
}
fs.writeFileSync(outlinePath, JSON.stringify(outline, null, 2) + "\n");
console.log("outline updated");

// video scripts for drafted days
for (const day of fs.readdirSync(bookDir).filter((d) => d.startsWith("day-"))) {
  const fp = path.join(bookDir, day, "video-script.md");
  if (!fs.existsSync(fp)) continue;
  let md = fs.readFileSync(fp, "utf8");
  md = fixDashes(md);
  md = md.replace(/Week\s*One/gi, "this set of lessons");
  md = md.replace(/Week\s*\d+/gi, "this review");
  md = md.replace(/Sedmica\s*\d+/gi, "Ponavljanje");
  md = md.replace(/Next week/gi, "Next");
  fs.writeFileSync(fp, md);
}
console.log("video scripts updated");
