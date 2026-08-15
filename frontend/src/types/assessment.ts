import type { QuizQuestion } from "./chapter";

export type AssessmentKind = "section" | "final";

export type AssessmentQuestion = QuizQuestion & {
  /** Lesson to reopen after a miss */
  remediationDay?: number;
};

export type Assessment = {
  id: string;
  book: number;
  kind: AssessmentKind;
  section?: number;
  coversDays: number[];
  title: string;
  titleEn: string;
  intro: string;
  passPercent: number;
  questions: AssessmentQuestion[];
};

export type AssessmentIndex = {
  book: number;
  sectionTests: string[];
  finalTest: string;
};
