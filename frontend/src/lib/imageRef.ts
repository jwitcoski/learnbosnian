import type { Chapter, ChapterImage } from "../types/chapter";
import type { GrammarChapter, GrammarImage } from "../types/grammar";

/** Photos in the order they appear on a lesson page: hero, then the rest, civic last. */
export function orderedChapterImages(chapter: Chapter): ChapterImage[] {
  const images = chapter.images || [];
  if (!images.length) return [];
  const civicId = chapter.civicContext?.imageId || null;
  const hero =
    images.find((i) => i.id === chapter.culture?.imageId) || images[0];
  const rest = images.filter(
    (i) => i.id !== hero?.id && i.id !== civicId
  );
  const civic = civicId
    ? images.find((i) => i.id === civicId)
    : undefined;
  return [hero, ...rest, civic].filter(
    (img): img is ChapterImage => Boolean(img)
  );
}

export function orderedGrammarImages(chapter: GrammarChapter): GrammarImage[] {
  const images = chapter.images || [];
  if (!images.length) return [];
  const ids = [
    chapter.imageSlots?.hero,
    chapter.imageSlots?.afterPattern,
    chapter.imageSlots?.afterNerd,
  ].filter((id): id is string => Boolean(id));
  const found = ids
    .map((id) => images.find((i) => i.id === id))
    .filter((img): img is GrammarImage => Boolean(img));
  const rest = images.filter((i) => !ids.includes(i.id));
  return [...found, ...rest];
}

export function imageRefCode(
  book: number | string,
  day: number,
  index: number
): string {
  const bookPart = book === "grammar" || book === "G" ? "G" : String(book);
  return `${bookPart}.${day}${String.fromCharCode(97 + index)}`;
}

export function imageRefFor(
  chapter: Chapter,
  imageId: string
): string {
  const index = orderedChapterImages(chapter).findIndex(
    (i) => i.id === imageId
  );
  if (index < 0) return "";
  return imageRefCode(chapter.book || 1, chapter.day, index);
}

export function grammarImageRefFor(
  chapter: GrammarChapter,
  imageId: string
): string {
  const index = orderedGrammarImages(chapter).findIndex(
    (i) => i.id === imageId
  );
  if (index < 0) return "";
  return imageRefCode("G", chapter.chapter, index);
}

export function photoCaption(chapter: Chapter, image: ChapterImage): string {
  const ref = imageRefFor(chapter, image.id);
  return ref ? `${ref} ${image.credit}` : image.credit;
}
