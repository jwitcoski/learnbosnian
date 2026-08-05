import { useMemo, useState } from "react";
import type { Puzzle } from "../../types/chapter";
import { GhostButton, PrimaryButton } from "./styles";

type Props = { puzzle: Puzzle };

export default function PuzzleGame({ puzzle }: Props) {
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

  if (puzzle.type === "match") {
    const check = () => {
      let correct = 0;
      matchItems.forEach((item) => {
        if (guesses[item.left] === item.right) correct += 1;
      });
      setScore(`${correct} / ${matchItems.length} correct`);
    };

    return (
      <div>
        <h3>{puzzle.title}</h3>
        <p>{puzzle.prompt}</p>
        {matchItems.map((item) => (
          <div key={item.left} style={{ marginBottom: "0.65rem" }}>
            <strong>{item.left}</strong>{" "}
            <select
              value={guesses[item.left] || ""}
              onChange={(e) =>
                setGuesses({ ...guesses, [item.left]: e.target.value })
              }
              style={{ marginLeft: "0.5rem", padding: "0.35rem" }}
            >
              <option value="">— choose —</option>
              {rights.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>
        ))}
        <PrimaryButton type="button" onClick={check}>
          Check matches
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
    };
    return (
      <div>
        <h3>{puzzle.title}</h3>
        <p>{puzzle.prompt}</p>
        {items.map((item, idx) => (
          <div key={item.scrambled} style={{ marginBottom: "0.65rem" }}>
            <code>{item.scrambled}</code>{" "}
            <input
              value={guesses[String(idx)] || ""}
              onChange={(e) =>
                setGuesses({ ...guesses, [String(idx)]: e.target.value })
              }
              style={{ width: "160px", display: "inline-block", padding: "0.4rem" }}
              placeholder="unscramble"
            />
          </div>
        ))}
        <PrimaryButton type="button" onClick={check}>
          Check answers
        </PrimaryButton>
        {score && <p style={{ marginTop: "0.75rem" }}>{score}</p>}
        <GhostButton
          type="button"
          style={{ marginLeft: "0.5rem" }}
          onClick={() => setGuesses({})}
        >
          Reset
        </GhostButton>
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
