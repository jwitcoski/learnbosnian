export type ChapterStatus = "outlined" | "draft" | "in_review" | "published";

export type VocabEntry = {
  bosnian: string;
  english: string;
  pronunciation?: string;
  partOfSpeech?: string;
  example?: string;
};

export type GrammarBite = {
  title: string;
  explanation: string;
  examples?: { bosnian: string; english: string }[];
};

export type ConversationLine = {
  speaker: string;
  bosnian: string;
  english: string;
};

export type Puzzle = {
  id: string;
  type: "match" | "scramble" | "fill" | "truefalse" | "picture";
  title: string;
  prompt: string;
  items?: any[];
  answer?: any;
};

export type PracticeItem = {
  id: string;
  prompt: string;
  hint?: string;
  answer: string;
};

export type QuizSkill =
  | "vocabulary"
  | "grammar"
  | "dialogue"
  | "culture"
  | "listening";

export type QuizQuestion = {
  id: string;
  question: string;
  options: string[];
  correctIndex: number;
  explanation?: string;
  skill?: QuizSkill;
};

export type AuthenticListen = {
  title: string;
  kind: "song" | "speaker";
  hook: string;
  source: {
    title: string;
    artistOrSpeaker: string;
    year?: string;
    regionOrScene?: string;
    license: string;
    credit: string;
    pageUrl: string;
    embedUrl?: string;
    clipId?: string;
  };
  durationHint?: string;
  listenTask: {
    prompt: string;
    gistQuestion: {
      prompt: string;
      options: string[];
      correctIndex: number;
    };
    targetWords?: string[];
    noticePrompt?: string;
  };
  reveal: {
    keyLines: { bosnian: string; english: string }[];
    teacherNote: string;
  };
};

export type CanDoCheck = {
  id: string;
  prompt: string;
  kind?: "speak" | "listen" | "write";
};

export type ChapterImage = {
  id: string;
  alt?: string;
  localPath?: string;
  sourceUrl: string;
  pageUrl?: string;
  author?: string;
  license: string;
  credit: string;
};

export type DictionaryEntry = {
  bosnian: string;
  english: string;
  partOfSpeech?: string;
  day?: number;
};

export type Chapter = {
  day: number;
  book: number;
  /** Curriculum section grouping (formerly called week) */
  section: number;
  title: string;
  titleEn: string;
  theme: string;
  status: ChapterStatus;
  reviewedAt?: string | null;
  reviewerNotes?: string;
  estimatedMinutes?: number;
  storyBeat?: string;
  learningGoals: {
    vocabulary: string[];
    grammar: string[];
    culture: string[];
  };
  vocabulary: VocabEntry[];
  grammar: GrammarBite[];
  culture?: {
    title: string;
    body: string;
    imageId?: string | null;
  };
  /** Fact-based civic note on structural pressures facing BiH, with its own image */
  civicContext?: {
    title: string;
    /** One paragraph of fact-based context */
    body: string;
    imageId?: string | null;
    /** Wikipedia or news article for further reading */
    learnMore: {
      label: string;
      url: string;
    };
  };
  lessonBlocks: {
    id: string;
    title: string;
    body: string;
    tips?: string[];
  }[];
  conversation?: {
    title: string;
    setting: string;
    lines: ConversationLine[];
  };
  /** Line indexes (0-based) offered for AI speak-check; default first learner lines */
  speakTargets?: number[];
  puzzles: Puzzle[];
  practice: PracticeItem[];
  funFacts: { title: string; body: string }[];
  /** Authentic speaker/singer listening beat (Čuj Bosnu) */
  authenticListen?: AuthenticListen;
  /** Section or lesson can-do self-checks */
  canDoChecks?: CanDoCheck[];
  resources: { label: string; url: string; note?: string }[];
  sectionQuiz: {
    title: string;
    passPercent?: number;
    questions: QuizQuestion[];
  };
  dictionaryEntries: DictionaryEntry[];
  images: ChapterImage[];
  imagesNeeded?: boolean;
  imageBriefs?: string[];
};

export type DayOutline = {
  day: number;
  section: number;
  title: string;
  titleEn: string;
  theme: string;
  languageFocus: string;
  storyBeat: string;
};

export type BookOutline = {
  book: number;
  title: string;
  titleBs?: string;
  level?: string;
  days?: DayOutline[];
  sections?: { section: number; title: string; focus: string }[];
  cast?: string[];
  summary?: string;
  themes?: string[];
  status?: string;
  note?: string;
};
