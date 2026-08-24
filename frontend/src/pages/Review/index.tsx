import { FormEvent, useEffect, useState } from "react";
import { Link, useHistory, useLocation } from "react-router-dom";
import {
  isReviewUnlocked,
  lockReview,
  unlockReview,
} from "../../hooks/useReviewUnlock";
import { LessonPage, PrimaryButton } from "../../components/lesson/styles";

/**
 * Private unlock for draft lessons. Not linked from public navigation.
 * Share https://howtospeakbosnian.com/review with the password.
 */
const ReviewGate = () => {
  const history = useHistory();
  const location = useLocation();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [unlocked, setUnlocked] = useState(isReviewUnlocked());

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const key = params.get("key");
    if (key && unlockReview(key)) {
      setUnlocked(true);
      history.replace("/learn/book/1");
    }
  }, [location.search, history]);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (unlockReview(password)) {
      setError("");
      setUnlocked(true);
      history.push("/learn/book/1");
      return;
    }
    setError("Wrong password.");
  };

  if (unlocked) {
    return (
      <LessonPage>
        <h1>Review mode on</h1>
        <p>
          Draft lessons (and section / final tests) are unlocked in this browser
          tab. Public visitors without the password still only see published
          chapters.
        </p>
        <p>
          <Link to="/learn/book/1">Open Book 1 curriculum →</Link>
        </p>
        <p>
          <button
            type="button"
            onClick={() => {
              lockReview();
              setUnlocked(false);
            }}
            style={{
              background: "none",
              border: "none",
              color: "var(--color-crimson)",
              textDecoration: "underline",
              cursor: "pointer",
              padding: 0,
              font: "inherit",
            }}
          >
            Lock review mode
          </button>
        </p>
      </LessonPage>
    );
  }

  return (
    <LessonPage>
      <h1>Private review</h1>
      <p>
        Enter the shared review password to preview unpublished draft lessons.
        This page is not linked from the public site.
      </p>
      <form onSubmit={onSubmit} style={{ maxWidth: "22rem" }}>
        <label htmlFor="review-password" style={{ display: "block" }}>
          Password
        </label>
        <input
          id="review-password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", margin: "0.35rem 0 0.75rem" }}
        />
        {error && (
          <p style={{ color: "var(--color-crimson)", marginTop: 0 }}>{error}</p>
        )}
        <PrimaryButton type="submit">Unlock drafts</PrimaryButton>
      </form>
    </LessonPage>
  );
};

export default ReviewGate;
