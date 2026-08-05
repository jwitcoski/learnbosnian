import { useState } from "react";
import { Link } from "react-router-dom";
import type { Chapter } from "../../types/chapter";
import { saveQuizScore } from "../../hooks/useProgress";
import { PrimaryButton } from "./styles";

type Props = {
  chapter: Chapter;
  embedded?: boolean;
};

export default function SectionQuiz({ chapter, embedded }: Props) {
  const questions = chapter.sectionQuiz?.questions || [];
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<{ percent: number; passed: boolean } | null>(
    null
  );

  if (!questions.length) {
    return <p>Quiz arrives when this chapter is fully drafted.</p>;
  }

  const submit = () => {
    let correct = 0;
    questions.forEach((q) => {
      if (answers[q.id] === q.correctIndex) correct += 1;
    });
    const percent = Math.round((correct / questions.length) * 100);
    const passPercent = chapter.sectionQuiz.passPercent ?? 70;
    const passed = percent >= passPercent;
    saveQuizScore(chapter.day, percent);
    setResult({ percent, passed });
  };

  return (
    <div>
      <h3>{chapter.sectionQuiz.title}</h3>
      {questions.map((q, qi) => (
        <div key={q.id} style={{ marginBottom: "1.25rem" }}>
          <p>
            <strong>
              {qi + 1}. {q.question}
            </strong>
          </p>
          {q.options.map((opt, oi) => (
            <label
              key={opt}
              style={{ display: "block", marginBottom: "0.35rem", cursor: "pointer" }}
            >
              <input
                type="radio"
                name={q.id}
                checked={answers[q.id] === oi}
                onChange={() => setAnswers({ ...answers, [q.id]: oi })}
                style={{ width: "auto", marginRight: "0.5rem" }}
              />
              {opt}
            </label>
          ))}
          {result && (
            <p style={{ fontSize: "0.95rem", color: "var(--color-muted)" }}>
              {q.explanation}
            </p>
          )}
        </div>
      ))}
      <PrimaryButton type="button" onClick={submit}>
        Submit quiz
      </PrimaryButton>
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>
            Score: <strong>{result.percent}%</strong> —{" "}
            {result.passed ? "Day complete!" : "Try again after a quick review."}
          </p>
          {result.passed && !embedded && (
            <p>
              <Link to="/learn">Back to curriculum</Link>
            </p>
          )}
        </div>
      )}
    </div>
  );
}
