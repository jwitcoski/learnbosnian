import outline from "./grammar/outline.json";
import chapters from "./grammar/chapters";
import type { GrammarChapter, GrammarOutline } from "../types/grammar";
import { isReviewUnlocked } from "../hooks/useReviewUnlock";

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
  if (chapter.status === "published") return true;
  if (chapter.status === "draft" && isReviewUnlocked()) return true;
  return false;
}
