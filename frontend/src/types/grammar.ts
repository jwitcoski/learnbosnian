import type { ChapterImage, ChapterStatus, QuizQuestion, VocabEntry } from "./chapter";

export type GrammarSlot = {
  heading: string;
  body: string;
  speaker?: string;
  bosnian?: string;
  english?: string;
  table?: {
    headers: string[];
    rows: string[][];
  };
};

export type GrammarLookItem = {
  speaker: string;
  bosnian: string;
  english: string;
};

export type GrammarTryItem = {
  id: string;
  prompt: string;
  options: string[];
  correctIndex: number;
  explanation?: string;
};

export type GrammarImage = ChapterImage & {
  grammarCaption?: string;
};

export type GrammarChapter = {
  chapter: number;
  kind: "grammar";
  title: string;
  titleEn: string;
  theme: string;
  status: ChapterStatus;
  reviewedAt?: string | null;
  reviewerNotes?: string;
  estimatedMinutes?: number;
  whyHere: GrammarSlot;
  englishLies: GrammarSlot;
  knownLine: GrammarSlot;
  pattern: GrammarSlot;
  howYouGuess?: GrammarSlot;
  trick?: GrammarSlot;
  nerd: GrammarSlot;
  vocabulary?: VocabEntry[];
  /** 0-based indexes into look.items for Speak Check. Default: first few spoken lines. */
  speakTargets?: number[];
  look?: {
    heading: string;
    items: GrammarLookItem[];
  };
  try?: {
    heading: string;
    items: GrammarTryItem[];
  };
  quiz: {
    title: string;
    passPercent?: number;
    questions: QuizQuestion[];
  };
  next: {
    body: string;
    chapter?: number | null;
  };
  imageSlots: {
    hero: string;
    afterPattern?: string;
    afterNerd?: string;
  };
  images: GrammarImage[];
  imagesNeeded?: boolean;
  imageBriefs?: string[];
};

export type GrammarOutlineChapter = {
  chapter: number;
  title: string;
  titleEn: string;
  theme: string;
  status: ChapterStatus;
};

export type GrammarOutline = {
  kind: "grammar";
  title: string;
  titleBs?: string;
  level?: string;
  status?: string;
  summary?: string;
  pedagogy?: string;
  parts: {
    part: number;
    title: string;
    focus: string;
    chapters: number[];
  }[];
  chapters: GrammarOutlineChapter[];
};
