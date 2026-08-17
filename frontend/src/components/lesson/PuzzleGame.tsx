import { useMemo, useState } from "react";
import type { Puzzle } from "../../types/chapter";
import { GhostButton, PrimaryButton } from "./styles";
import BosnianTextInput from "./BosnianTextInput";

type Props = { puzzle: Puzzle };

function ItemFeedback({
  ok,
  correctLabel,
}: {
  ok: boolean;
  correctLabel?: string;
}) {
  return (
    <p
      style={{
        margin: "0.35rem 0 0",
        fontSize: "0.95rem",
        fontWeight: 700,
        color: ok ? "var(--color-sage)" : "var(--color-crimson)",
      }}
    >
      {ok ? "Correct" : correctLabel ? `Incorrect. ${correctLabel}` : "Incorrect"}
    </p>
  );
}

export default function PuzzleGame({ puzzle }: Props) {
  const [checked, setChecked] = useState(false);
  const [score, setScore] = useState<string | null>(null);
  const [guesses, setGuesses] = useState<Record<string, string>>({});

  const matchItems = useMemo(() => {
    if (puzzle.type !== "match") return [];
    return (puzzle.items || []) as { left: string; right: string }[];
  }, [puzzle]);

  const rights = useMemo(() => {
    const r = matchItems.map((i) => i.right);
    return [...r].sort(() => Math.random() - 0.5);
  }, [matchItems]);

  const setGuess = (key: string, value: string) => {
    setGuesses({ ...guesses, [key]: value });
    if (checked) {
      setChecked(false);
      setScore(null);
    }
  };

  if (puzzle.type === "match") {
    const check = () => {
      let correct = 0;
      matchItems.forEach((item) => {
        if (guesses[item.left] === item.right) correct += 1;
      });
      setScore(`${correct} / ${matchItems.length} correct`);
      setChecked(true);
    };

    return (
      <div>
        <h3>{puzzle.title}</h3>
        <p>{puzzle.prompt}</p>
        {matchItems.map((item) => {
          const guess = guesses[item.left] || "";
          const ok = guess === item.right;
          return (
            <div key={item.left} style={{ marginBottom: "0.85rem" }}>
              <strong>{item.left}</strong>{" "}
              <select
                value={guess}
                onChange={(e) => setGuess(item.left, e.target.value)}
                style={{
                  marginLeft: "0.5rem",
                  padding: "0.35rem",
                  borderColor: checked
                    ? ok
                      ? "var(--color-sage)"
                      : "var(--color-crimson)"
                    : undefined,
                }}
              >
                <option value="">Choose…</option>
                {rights.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
              {checked && (
                <ItemFeedback
                  ok={ok}
                  correctLabel={`answer: ${item.right}`}
                />
              )}
            </div>
          );
        })}
        <PrimaryButton type="button" onClick={check}>
          {checked ? "Check again" : "Check matches"}
        </PrimaryButton>
        {score && <p style={{ marginTop: "0.75rem" }}>{score}</p>}
      </div>
    );
  }

  if (puzzle.type === "scramble") {
    const items = (puzzle.items || []) as {
      scrambled: string;
      answer: string;
    }[];
    const check = () => {
      let correct = 0;
      items.forEach((item, idx) => {
        const g = (guesses[String(idx)] || "").trim().toLowerCase();
        if (g === item.answer.toLowerCase()) correct += 1;
      });
      setScore(`${correct} / ${items.length} correct`);
      setChecked(true);
    };
    return (
      <div>
        <h3>{puzzle.title}</h3>
        <p>{puzzle.prompt}</p>
        <p style={{ fontSize: "0.95rem", color: "var(--color-muted)" }}>
          Need č ć š ž đ? Use the accent buttons under each box.
        </p>
        {items.map((item, idx) => {
          const key = String(idx);
          const guess = (guesses[key] || "").trim().toLowerCase();
          const ok = guess === item.answer.toLowerCase();
          return (
            <div key={item.scrambled} style={{ marginBottom: "0.85rem" }}>
              <code>{item.scrambled}</code>
              <BosnianTextInput
                value={guesses[key] || ""}
                onChange={(next) => setGuess(key, next)}
                placeholder="unscramble"
                style={{
                  maxWidth: "220px",
                  borderColor: checked
                    ? ok
                      ? "var(--color-sage)"
                      : "var(--color-crimson)"
                    : undefined,
                }}
              />
              {checked && (
                <ItemFeedback
                  ok={ok}
                  correctLabel={`answer: ${item.answer}`}
                />
              )}
            </div>
          );
        })}
        <PrimaryButton type="button" onClick={check}>
          {checked ? "Check again" : "Check answers"}
        </PrimaryButton>
        {score && <p style={{ marginTop: "0.75rem" }}>{score}</p>}
        <GhostButton
          type="button"
          style={{ marginLeft: "0.5rem" }}
          onClick={() => {
            setGuesses({});
            setChecked(false);
            setScore(null);
          }}
        >
          Reset
        </GhostButton>
      </div>
    );
  }

  if (puzzle.type === "truefalse") {
    const items = (puzzle.items || []) as {
      statement: string;
      answer: boolean;
    }[];
    const check = () => {
      let correct = 0;
      items.forEach((item, idx) => {
        const g = guesses[String(idx)];
        if (g === String(item.answer)) correct += 1;
      });
      setScore(`${correct} / ${items.length} correct`);
      setChecked(true);
    };
    return (
      <div>
        <h3>{puzzle.title}</h3>
        <p>{puzzle.prompt}</p>
        {items.map((item, idx) => {
          const key = String(idx);
          const guess = guesses[key] || "";
          const ok = guess === String(item.answer);
          return (
            <div key={item.statement} style={{ marginBottom: "0.85rem" }}>
              <p style={{ marginBottom: "0.35rem" }}>{item.statement}</p>
              <select
                value={guess}
                onChange={(e) => setGuess(key, e.target.value)}
                style={{
                  padding: "0.35rem",
                  borderColor: checked
                    ? ok
                      ? "var(--color-sage)"
                      : "var(--color-crimson)"
                    : undefined,
                }}
              >
                <option value="">Choose…</option>
                <option value="true">True</option>
                <option value="false">False</option>
              </select>
              {checked && (
                <ItemFeedback
                  ok={ok}
                  correctLabel={`answer: ${item.answer ? "True" : "False"}`}
                />
              )}
            </div>
          );
        })}
        <PrimaryButton type="button" onClick={check}>
          {checked ? "Check again" : "Check answers"}
        </PrimaryButton>
        {score && <p style={{ marginTop: "0.75rem" }}>{score}</p>}
      </div>
    );
  }

  return (
    <div>
      <h3>{puzzle.title}</h3>
      <p>{puzzle.prompt}</p>
    </div>
  );
}
