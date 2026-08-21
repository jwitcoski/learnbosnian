#!/usr/bin/env node
/**
 * Sync portable content/ into frontend/src/data for the CRA app.
 */
const fs = require("fs");
const path = require("path");
const { orderedChapterImages, imageRefCode } = require("./lib/image-ref.cjs");
const { buildClipsCatalog } = require("./lib/audio-clips.cjs");

const root = path.join(__dirname, "..");
const src = path.join(root, "content");
const dest = path.join(root, "frontend", "src", "data");

// Keep audio clip catalog in sync with chapter content
require("./build-audio-clips.cjs");

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const s = path.join(from, entry.name);
    const d = path.join(to, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

for (const book of ["book1", "book2", "book3"]) {
  const from = path.join(src, book);
  const to = path.join(dest, book);
  if (!fs.existsSync(from)) continue;
  fs.rmSync(to, { recursive: true, force: true });
  copyDir(from, to);
  console.log(`Synced ${book} → frontend/src/data/${book}`);
}

const book1 = path.join(dest, "book1");
if (fs.existsSync(book1)) {
  const days = fs
    .readdirSync(book1)
    .filter((d) => d.startsWith("day-"))
    .sort();
  const imports = days
    .map((d) => {
      const n = d.replace("day-", "");
      return `import day${n} from "./${d}/chapter.json";`;
    })
    .join("\n");
  const arr = days.map((d) => `day${d.replace("day-", "")}`).join(", ");
  const index = `${imports}
import type { Chapter } from "../../types/chapter";

const chapters: Chapter[] = [${arr}] as Chapter[];

export default chapters;
`;
  fs.writeFileSync(path.join(book1, "chapters.ts"), index);
  console.log("Regenerated book1/chapters.ts");
}

/** Build running photo attribution register for the site + book cites */
function harvestChapterImages() {
  const entries = [];
  for (const book of ["book1", "book2", "book3"]) {
    const bookDir = path.join(src, book);
    if (!fs.existsSync(bookDir)) continue;
    for (const day of fs.readdirSync(bookDir).sort()) {
      const chapterPath = path.join(bookDir, day, "chapter.json");
      if (!fs.existsSync(chapterPath)) continue;
      const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
      const ordered = orderedChapterImages(chapter);
      ordered.forEach((img, index) => {
        const source =
          img.pageUrl?.includes("wikimedia")
            ? "Wikimedia Commons"
            : img.pageUrl?.includes("pexels")
            ? "Pexels"
            : img.pageUrl?.includes("unsplash")
            ? "Unsplash"
            : "Other";
        const creditParts = [img.author, source !== "Other" ? source : ""]
          .filter(Boolean)
          .join(" / ");
        const credit = img.license
          ? `${creditParts} (${img.license})`.trim()
          : creditParts;
        const ref = imageRefCode(chapter.book || 1, chapter.day, index);
        entries.push({
          id: `${book}-day-${String(chapter.day).padStart(2, "0")}-${img.id}`,
          ref,
          title: img.credit || img.alt || img.id,
          whereUsed: [
            `Book ${chapter.book} · Lesson ${chapter.day} — ${
              chapter.titleEn || chapter.title
            }`,
          ],
          author: img.author || "",
          source,
          license: img.license || "",
          pageUrl: img.pageUrl || img.sourceUrl || "",
          sourceUrl: img.sourceUrl || img.pageUrl || "",
          localPath: img.localPath || "",
          credit,
          notes: "",
          book: chapter.book,
          day: chapter.day,
        });
      });
    }
  }
  return entries;
}

const manualPath = path.join(src, "attributions.json");
const manual = fs.existsSync(manualPath)
  ? JSON.parse(fs.readFileSync(manualPath, "utf8"))
  : { title: "Photo attributions", intro: "", citationNote: "", entries: [] };

const chapterEntries = harvestChapterImages();
const byId = new Map();
for (const e of manual.entries || []) byId.set(e.id, { ...e });
for (const e of chapterEntries) {
  if (byId.has(e.id)) {
    const prev = byId.get(e.id);
    byId.set(e.id, {
      ...e,
      ...prev,
      whereUsed: Array.from(
        new Set([...(prev.whereUsed || []), ...(e.whereUsed || [])])
      ),
    });
  } else {
    byId.set(e.id, e);
  }
}

const merged = {
  title: manual.title || "Photo attributions",
  intro: manual.intro || "",
  citationNote: manual.citationNote || "",
  generatedAt: new Date().toISOString().slice(0, 10),
  total: byId.size,
  entries: Array.from(byId.values()).sort((a, b) => {
    const dayA = a.day ?? 999;
    const dayB = b.day ?? 999;
    if (dayA !== dayB) return dayA - dayB;
    const refA = a.ref || "";
    const refB = b.ref || "";
    if (refA && refB && refA !== refB) return refA.localeCompare(refB, undefined, { numeric: true });
    return String(a.id).localeCompare(String(b.id));
  }),
};

fs.writeFileSync(
  path.join(dest, "attributions.json"),
  JSON.stringify(merged, null, 2) + "\n"
);
console.log(
  `Wrote attributions.json (${merged.total} entries) → frontend/src/data/`
);

/** Sync audio clip catalog + voice profiles into frontend + recorder + backend */
const audioSrc = path.join(src, "audio");
const audioTargets = [
  path.join(dest, "audio"),
  path.join(root, "recorder", "src", "data"),
  path.join(root, "backend", "data"),
];
const catalog = buildClipsCatalog(root);
for (const target of audioTargets) {
  fs.mkdirSync(target, { recursive: true });
  fs.writeFileSync(
    path.join(target, "clips.json"),
    JSON.stringify(catalog, null, 2) + "\n"
  );
  for (const name of ["voice-profiles.json", "speaker-genders.json"]) {
    const from = path.join(audioSrc, name);
    if (fs.existsSync(from)) {
      fs.copyFileSync(from, path.join(target, name));
    }
  }
}
console.log(
  `Synced audio catalog (${catalog.total} clips) → frontend, recorder, backend`
);
