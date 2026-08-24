import outline from "./grammar/outline.json";
import chapters from "./grammar/chapters";
import type { GrammarChapter, GrammarOutline } from "../types/grammar";

const byChapter: Record<number, GrammarChapter> = {};
chapters.forEach((chapter) => {
  byChapter[chapter.chapter] = chapter;
});

export const grammarOutline = outline as GrammarOutline;

export function listGrammarChapters(): GrammarChapter[] {
  return Object.values(byChapter).sort((a, b) => a.chapter - b.chapter);
}

export function getGrammarChapter(n: number): GrammarChapter | null {
  return byChapter[n] || null;
}

export function canViewGrammarChapter(
  chapter: GrammarChapter | GrammarOutline["chapters"][number]
): boolean {
  return chapter.status === "published" || chapter.status === "draft";
}
