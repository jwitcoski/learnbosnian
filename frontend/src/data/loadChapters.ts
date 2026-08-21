import outline from "../data/book1/outline.json";
import chapters from "../data/book1/chapters";
import type { BookOutline, Chapter, DictionaryEntry } from "../types/chapter";

const chaptersByDay: Record<number, Chapter> = {};
chapters.forEach((chapter) => {
  chaptersByDay[chapter.day] = chapter;
});

export const book1Outline = outline as BookOutline;

export function listChapters(): Chapter[] {
  return Object.values(chaptersByDay).sort((a, b) => a.day - b.day);
}

export function getChapter(day: number): Chapter | null {
  return chaptersByDay[day] || null;
}

export function isChapterOpen(chapter: Chapter): boolean {
  return chapter.status === "published";
}

/** Draft chapters are previewable so Night 1 exemplar can be reviewed on the site. */
export function canViewChapter(chapter: Chapter): boolean {
  return chapter.status === "published" || chapter.status === "draft";
}

export function listOpenChapters(): Chapter[] {
  return listChapters().filter(canViewChapter);
}

export function buildDictionary(onlyOpen = true): DictionaryEntry[] {
  const entries: DictionaryEntry[] = [];
  const seen = new Set<string>();
  listChapters().forEach((ch) => {
    if (onlyOpen && !canViewChapter(ch)) return;
    ch.dictionaryEntries.forEach((e) => {
      const key = `${ch.book}:${e.bosnian.toLowerCase()}`;
      if (seen.has(key)) return;
      seen.add(key);
      entries.push({ ...e, day: e.day || ch.day, book: ch.book });
    });
  });
  return entries.sort((a, b) =>
    a.bosnian.localeCompare(b.bosnian, "bs", { sensitivity: "base" })
  );
}
