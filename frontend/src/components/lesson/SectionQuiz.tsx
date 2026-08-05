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
  const [result, setResult] = useState<{
    percent: number;
    passed: boolean;
    correctCount: number;
  } | null>(null);

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
    setResult({ percent, passed, correctCount: correct });
  };

  const pick = (questionId: string, optionIndex: number) => {
    setAnswers({ ...answers, [questionId]: optionIndex });
    if (result) setResult(null);
  };

  return (
    <div>
      <h3>{chapter.sectionQuiz.title}</h3>
      {questions.map((q, qi) => {
        const selected = answers[q.id];
        const hasAnswer = selected !== undefined;
        const isCorrect = hasAnswer && selected === q.correctIndex;
        const showFeedback = Boolean(result);

        return (
          <div
            key={q.id}
            style={{
              marginBottom: "1.25rem",
              padding: showFeedback ? "0.85rem 1rem" : undefined,
              borderLeft: showFeedback
                ? `4px solid ${
                    isCorrect ? "var(--color-sage)" : "var(--color-crimson)"
                  }`
                : undefined,
              background: showFeedback
                ? isCorrect
                  ? "rgba(132, 146, 116, 0.12)"
                  : "rgba(198, 40, 40, 0.08)"
                : undefined,
            }}
          >
            <p>
              <strong>
                {qi + 1}. {q.question}
              </strong>
            </p>
            {q.options.map((opt, oi) => {
              const chosen = selected === oi;
              const isRightOption = oi === q.correctIndex;
              let optionColor: string | undefined;
              let weight: number | undefined;
              if (showFeedback) {
                if (isRightOption) {
                  optionColor = "var(--color-sage)";
                  weight = 700;
                } else if (chosen && !isCorrect) {
                  optionColor = "var(--color-crimson)";
                  weight = 600;
                }
              }
              return (
                <label
                  key={opt}
                  style={{
                    display: "block",
                    marginBottom: "0.35rem",
                    cursor: "pointer",
                    color: optionColor,
                    fontWeight: weight,
                  }}
                >
                  <input
                    type="radio"
                    name={q.id}
                    checked={chosen}
                    onChange={() => pick(q.id, oi)}
                    style={{ width: "auto", marginRight: "0.5rem" }}
                  />
                  {opt}
                  {showFeedback && isRightOption ? " ✓" : ""}
                  {showFeedback && chosen && !isCorrect ? " ✗" : ""}
                </label>
              );
            })}
            {showFeedback && (
              <p
                style={{
                  fontSize: "0.95rem",
                  marginTop: "0.5rem",
                  marginBottom: 0,
                  color: isCorrect ? "var(--color-sage)" : "var(--color-crimson)",
                  fontWeight: 700,
                }}
              >
                {isCorrect ? "Correct" : "Incorrect"}
                {!hasAnswer ? " — no answer selected" : ""}
                {!isCorrect ? ` — right answer: ${q.options[q.correctIndex]}` : ""}
              </p>
            )}
            {showFeedback && q.explanation && (
              <p
                style={{
                  fontSize: "0.95rem",
                  color: "var(--color-muted)",
                  marginTop: "0.35rem",
                  marginBottom: 0,
                }}
              >
                {q.explanation}
              </p>
            )}
          </div>
        );
      })}
      <PrimaryButton type="button" onClick={submit}>
        {result ? "Submit again" : "Submit quiz"}
      </PrimaryButton>
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>
            Score:{" "}
            <strong>
              {result.correctCount}/{questions.length} ({result.percent}%)
            </strong>{" "}
            —{" "}
            {result.passed
              ? "Lesson complete!"
              : "Try again after a quick review."}
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
