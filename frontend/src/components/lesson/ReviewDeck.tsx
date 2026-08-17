import { useMemo, useState } from "react";
import type { VocabEntry } from "../../types/chapter";
import { PrimaryButton } from "./styles";
import {
  getReviewQueue,
  recordReviewResult,
  ReviewCard,
} from "../../hooks/useReviewDeck";

type Props = {
  day: number;
  lessonVocab: VocabEntry[];
};

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export default function ReviewDeck({ day, lessonVocab }: Props) {
  const seedCards = useMemo(() => {
    const lesson: ReviewCard[] = lessonVocab.slice(0, 5).map((v) => ({
      id: `d${day}-${v.bosnian}`,
      bosnian: v.bosnian,
      english: v.english,
      day,
    }));
    const prior = getReviewQueue(day).filter((c) => c.day !== day).slice(0, 5);
    return shuffle([...lesson, ...prior]).slice(0, 10);
  }, [day, lessonVocab]);

  const [cards] = useState(seedCards);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [done, setDone] = useState(false);

  if (!cards.length) return null;

  const card = cards[idx];

  const grade = (ok: boolean) => {
    recordReviewResult(card, ok);
    setFlipped(false);
    if (idx + 1 >= cards.length) {
      setDone(true);
    } else {
      setIdx(idx + 1);
    }
  };

  return (
    <div>
      <h2>Quick review</h2>
      <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
        A few words from this lesson, plus ones you missed before. Flip the
        card, then mark how it went.
      </p>
      {done ? (
        <p style={{ fontWeight: 700, color: "var(--color-sage)" }}>
          Round done. Come back next lesson for more.
        </p>
      ) : (
        <>
          <p style={{ fontSize: "0.9rem", color: "var(--color-muted)" }}>
            Card {idx + 1} / {cards.length}
          </p>
          <button
            type="button"
            onClick={() => setFlipped((v) => !v)}
            style={{
              display: "block",
              width: "100%",
              maxWidth: 420,
              minHeight: 140,
              padding: "1.25rem",
              textAlign: "left",
              border: "2px solid var(--color-crimson, #c62828)",
              borderRadius: 8,
              background: "var(--color-cream, #fff)",
              cursor: "pointer",
              marginBottom: "0.75rem",
            }}
          >
            <div style={{ fontSize: "1.4rem", fontWeight: 700 }}>
              {flipped ? card.english : card.bosnian}
            </div>
            <div style={{ color: "var(--color-muted)", marginTop: "0.5rem" }}>
              {flipped ? "English" : "Bosnian · tap to flip"}
            </div>
          </button>
          {flipped && (
            <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
              <PrimaryButton type="button" onClick={() => grade(false)}>
                Again
              </PrimaryButton>
              <PrimaryButton type="button" onClick={() => grade(true)}>
                Got it
              </PrimaryButton>
            </div>
          )}
        </>
      )}
    </div>
  );
}
