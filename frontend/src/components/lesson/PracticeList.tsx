import { useState } from "react";
import type { PracticeItem } from "../../types/chapter";
import { PrimaryButton } from "./styles";
import BosnianTextInput from "./BosnianTextInput";

type Props = { items: PracticeItem[] };

export default function PracticeList({ items }: Props) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [revealed, setRevealed] = useState(false);

  if (!items.length) return null;

  return (
    <div>
      <p style={{ fontSize: "0.95rem", color: "var(--color-muted)" }}>
        Your keyboard may not have č ć š ž đ. Tap the accent buttons under each box
        to insert them.
      </p>
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
            <BosnianTextInput
              value={answers[item.id] || ""}
              onChange={(next) => {
                setAnswers({ ...answers, [item.id]: next });
                if (revealed) setRevealed(false);
              }}
              placeholder="Your answer"
              style={
                revealed
                  ? {
                      border: `2px solid ${
                        ok ? "var(--color-sage)" : "var(--color-crimson)"
                      }`,
                    }
                  : undefined
              }
            />
            {revealed && (
              <p style={{ color: ok ? "var(--color-sage)" : "var(--color-crimson)", fontWeight: 700 }}>
                {ok ? "Correct" : `Incorrect — answer: ${item.answer}`}
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
