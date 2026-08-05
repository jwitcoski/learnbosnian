#!/usr/bin/env node
/**
 * Sync portable content/ into frontend/src/data for the CRA app.
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const src = path.join(root, "content");
const dest = path.join(root, "frontend", "src", "data");

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
