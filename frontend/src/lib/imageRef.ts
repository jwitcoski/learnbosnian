import type { Chapter, ChapterImage } from "../types/chapter";

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

export function imageRefCode(
  book: number,
  day: number,
  index: number
): string {
  return `${book}.${day}${String.fromCharCode(97 + index)}`;
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

export function photoCaption(chapter: Chapter, image: ChapterImage): string {
  const ref = imageRefFor(chapter, image.id);
  return ref ? `${ref} ${image.credit}` : image.credit;
}
