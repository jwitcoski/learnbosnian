const REVIEW_STORAGE_KEY = "lb-review-unlock";

/** Shared with reviewers only — not linked from the public site. */
export function getReviewPassword(): string {
  return process.env.REACT_APP_REVIEW_PASSWORD || "SedmicaReview";
}

export function isReviewUnlocked(): boolean {
  try {
    return sessionStorage.getItem(REVIEW_STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

export function unlockReview(password: string): boolean {
  if (password.trim() === getReviewPassword()) {
    try {
      sessionStorage.setItem(REVIEW_STORAGE_KEY, "1");
    } catch {
      /* ignore */
    }
    return true;
  }
  return false;
}

export function lockReview(): void {
  try {
    sessionStorage.removeItem(REVIEW_STORAGE_KEY);
  } catch {
    /* ignore */
  }
}
