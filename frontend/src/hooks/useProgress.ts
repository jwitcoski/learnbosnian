const STORAGE_KEY = "learnbosnian-progress-v1";

export type ProgressState = {
  completedDays: number[];
  quizScores: Record<string, number>;
  /** Scores for section-1..section-4 and final */
  assessmentScores?: Record<string, number>;
  lastDay?: number;
};

function read(): ProgressState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completedDays: [], quizScores: {}, assessmentScores: {} };
    const parsed = JSON.parse(raw) as ProgressState;
    if (!parsed.assessmentScores) parsed.assessmentScores = {};
    return parsed;
  } catch {
    return { completedDays: [], quizScores: {}, assessmentScores: {} };
  }
}

function write(state: ProgressState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export function getProgress(): ProgressState {
  return read();
}

export function markDayComplete(day: number) {
  const state = read();
  if (!state.completedDays.includes(day)) {
    state.completedDays.push(day);
    state.completedDays.sort((a, b) => a - b);
  }
  state.lastDay = day;
  write(state);
  return state;
}

export function saveQuizScore(day: number, percent: number) {
  const state = read();
  state.quizScores[String(day)] = percent;
  if (percent >= 70) {
    if (!state.completedDays.includes(day)) {
      state.completedDays.push(day);
      state.completedDays.sort((a, b) => a - b);
    }
  }
  state.lastDay = day;
  write(state);
  return state;
}

export function isDayComplete(day: number): boolean {
  return read().completedDays.includes(day);
}

export function saveAssessmentScore(
  assessmentId: string,
  percent: number,
  passPercent = 70
) {
  const state = read();
  if (!state.assessmentScores) state.assessmentScores = {};
  state.assessmentScores[assessmentId] = percent;
  write(state);
  return { state, passed: percent >= passPercent };
}

export function getAssessmentScore(assessmentId: string): number | undefined {
  return read().assessmentScores?.[assessmentId];
}

export function isAssessmentPassed(
  assessmentId: string,
  passPercent = 70
): boolean {
  const score = getAssessmentScore(assessmentId);
  return typeof score === "number" && score >= passPercent;
}
