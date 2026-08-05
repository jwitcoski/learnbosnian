import { useState } from "react";
import type { PracticeItem } from "../../types/chapter";
import { PrimaryButton } from "./styles";

type Props = { items: PracticeItem[] };

export default function PracticeList({ items }: Props) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [revealed, setRevealed] = useState(false);

  if (!items.length) return null;

  return (
    <div>
      {items.map((item) => {
        const ok =
          revealed &&
          (answers[item.id] || "").trim().toLowerCase() ===
            item.answer.trim().toLowerCase();
        return (
          <div key={item.id} style={{ marginBottom: "1rem" }}>
            <p style={{ marginBottom: "0.35rem" }}>{item.prompt}</p>
            {item.hint && (
              <p style={{ fontSize: "0.9rem", color: "var(--color-muted)" }}>
                Hint: {item.hint}
              </p>
            )}
            <input
              value={answers[item.id] || ""}
              onChange={(e) =>
                setAnswers({ ...answers, [item.id]: e.target.value })
              }
              placeholder="Your answer"
            />
            {revealed && (
              <p style={{ color: ok ? "var(--color-sage)" : "var(--color-crimson)" }}>
                {ok ? "Correct!" : `Answer: ${item.answer}`}
              </p>
            )}
          </div>
        );
      })}
      <PrimaryButton type="button" onClick={() => setRevealed(true)}>
        Check practice
      </PrimaryButton>
    </div>
  );
}
