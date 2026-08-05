const STORAGE_KEY = "learnbosnian-progress-v1";

export type ProgressState = {
  completedDays: number[];
  quizScores: Record<string, number>;
  lastDay?: number;
};

function read(): ProgressState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completedDays: [], quizScores: {} };
    return JSON.parse(raw) as ProgressState;
  } catch {
    return { completedDays: [], quizScores: {} };
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
