import type { QuizQuestion } from "./chapter";

export type AssessmentKind = "section" | "final";

export type AssessmentPart = {
  id: string;
  title: string;
  intro?: string;
};

export type AssessmentQuestion = QuizQuestion & {
  /** Lesson to reopen after a miss */
  remediationDay?: number;
  /** Groups the question under a named part (match, gap, talk). */
  part?: string;
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
  parts?: AssessmentPart[];
  questions: AssessmentQuestion[];
};

export type AssessmentIndex = {
  book: number;
  sectionTests: string[];
  finalTest: string;
};
