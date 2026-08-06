/** Stable audio clip IDs — keep in sync with scripts/lib/audio-clips.cjs */

export function slugify(text: string): string {
  return (
    String(text || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/gi, "dj")
      .replace(/č/gi, "c")
      .replace(/ć/gi, "c")
      .replace(/š/gi, "s")
      .replace(/ž/gi, "z")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 64) || "clip"
  );
}

function dayPad(day: number) {
  return String(day).padStart(2, "0");
}

export function vocabClipId(book: number, day: number, bosnian: string) {
  return `b${book}-d${dayPad(day)}-vocab-${slugify(bosnian)}`;
}

export function dialogueClipId(book: number, day: number, lineIndex: number) {
  return `b${book}-d${dayPad(day)}-dialogue-${String(lineIndex).padStart(2, "0")}`;
}

export function audioPublicBase() {
  return (
    process.env.REACT_APP_AUDIO_BASE_URL ||
    "https://audio.learnbosnian.local"
  ).replace(/\/$/, "");
}

export function clipAudioUrl(clipId: string) {
  return `${audioPublicBase()}/clips/${clipId}`;
}
