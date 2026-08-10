const STORAGE_KEY = "learnbosnian-review-v1";

export type ReviewCard = {
  id: string;
  bosnian: string;
  english: string;
  day: number;
};

type Store = {
  /** cardId -> due timestamp ms; lower = sooner */
  due: Record<string, number>;
  cards: Record<string, ReviewCard>;
  misses: string[];
};

function read(): Store {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { due: {}, cards: {}, misses: [] };
    return JSON.parse(raw) as Store;
  } catch {
    return { due: {}, cards: {}, misses: [] };
  }
}

function write(store: Store) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

export function addMissedWords(
  items: { bosnian: string; english: string; day: number }[]
) {
  const store = read();
  const now = Date.now();
  for (const item of items) {
    const id = `d${item.day}-${item.bosnian}`;
    store.cards[id] = { id, ...item };
    store.due[id] = now;
    if (!store.misses.includes(id)) store.misses.push(id);
  }
  write(store);
}

export function getReviewQueue(currentDay: number): ReviewCard[] {
  const store = read();
  const now = Date.now();
  const dueIds = Object.keys(store.due)
    .filter((id) => store.due[id] <= now)
    .sort((a, b) => store.due[a] - store.due[b]);
  const missIds = store.misses.filter((id) => !dueIds.includes(id));
  const ordered = [...dueIds, ...missIds];
  return ordered
    .map((id) => store.cards[id])
    .filter(Boolean)
    .filter((c) => c.day <= currentDay);
}

export function recordReviewResult(card: ReviewCard, ok: boolean) {
  const store = read();
  store.cards[card.id] = card;
  const now = Date.now();
  if (ok) {
    store.due[card.id] = now + 1000 * 60 * 60 * 24 * 2;
    store.misses = store.misses.filter((id) => id !== card.id);
  } else {
    store.due[card.id] = now + 1000 * 60 * 10;
    if (!store.misses.includes(card.id)) store.misses.push(card.id);
  }
  write(store);
}

const SPEAK_KEY = "learnbosnian-speak-attempts-v1";

export function getSpeakAttempts(day: number): number {
  try {
    const raw = localStorage.getItem(SPEAK_KEY);
    if (!raw) return 0;
    const map = JSON.parse(raw) as Record<string, number>;
    return map[String(day)] || 0;
  } catch {
    return 0;
  }
}

export function incrementSpeakAttempts(day: number): number {
  let map: Record<string, number> = {};
  try {
    const raw = localStorage.getItem(SPEAK_KEY);
    if (raw) map = JSON.parse(raw);
  } catch {
    map = {};
  }
  const next = (map[String(day)] || 0) + 1;
  map[String(day)] = next;
  localStorage.setItem(SPEAK_KEY, JSON.stringify(map));
  return next;
}

export const SPEAK_ATTEMPTS_PER_LESSON = 3;
