/** Photos in the order they appear on a lesson page: hero, then the rest, civic last. */
function orderedChapterImages(chapter) {
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
  return [hero, ...rest, civic].filter(Boolean);
}

function imageRefCode(book, day, index) {
  return `${book}.${day}${String.fromCharCode(97 + index)}`;
}

function imageRefFor(chapter, imageId) {
  const index = orderedChapterImages(chapter).findIndex(
    (i) => i.id === imageId
  );
  if (index < 0) return "";
  return imageRefCode(chapter.book || 1, chapter.day, index);
}

module.exports = {
  orderedChapterImages,
  imageRefCode,
  imageRefFor,
};
