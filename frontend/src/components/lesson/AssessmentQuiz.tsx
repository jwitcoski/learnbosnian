import { useState } from "react";
import { Link } from "react-router-dom";
import type { Assessment } from "../../types/assessment";
import type { QuizSkill } from "../../types/chapter";
import { saveAssessmentScore } from "../../hooks/useProgress";
import { PrimaryButton } from "./styles";

type Props = {
  assessment: Assessment;
};

export default function AssessmentQuiz({ assessment }: Props) {
  const questions = assessment.questions || [];
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<{
    percent: number;
    passed: boolean;
    correctCount: number;
    missedDays: number[];
    missedSkills: Record<string, number>;
  } | null>(null);

  if (!questions.length) {
    return <p>This test is not ready yet.</p>;
  }

  const submit = () => {
    let correct = 0;
    const missedDays = new Set<number>();
    const missedSkills: Record<string, number> = {};

    questions.forEach((q) => {
      const ok = answers[q.id] === q.correctIndex;
      if (ok) {
        correct += 1;
        return;
      }
      const skill = (q.skill || "vocabulary") as QuizSkill;
      missedSkills[skill] = (missedSkills[skill] || 0) + 1;
      if (q.remediationDay) missedDays.add(q.remediationDay);
    });

    const percent = Math.round((correct / questions.length) * 100);
    const passPercent = assessment.passPercent ?? 70;
    const passed = percent >= passPercent;
    saveAssessmentScore(assessment.id, percent, passPercent);
    setResult({
      percent,
      passed,
      correctCount: correct,
      missedDays: [...missedDays].sort((a, b) => a - b),
      missedSkills,
    });
  };

  const pick = (questionId: string, optionIndex: number) => {
    setAnswers({ ...answers, [questionId]: optionIndex });
    if (result) setResult(null);
  };

  return (
    <div>
      <h3>{assessment.title}</h3>
      <p style={{ color: "var(--color-muted)" }}>{assessment.intro}</p>
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
                  key={`${q.id}-${oi}`}
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
                  color: isCorrect
                    ? "var(--color-sage)"
                    : "var(--color-crimson)",
                  fontWeight: 700,
                }}
              >
                {isCorrect ? "Correct" : "Incorrect"}
                {!hasAnswer ? ". No answer selected" : ""}
                {!isCorrect
                  ? `. Right answer: ${q.options[q.correctIndex]}`
                  : ""}
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
        {result ? "Submit again" : "Submit test"}
      </PrimaryButton>
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>
            Score:{" "}
            <strong>
              {result.correctCount}/{questions.length} ({result.percent}%)
            </strong>
            {result.passed
              ? `. ${
                  assessment.kind === "final"
                    ? "Book 1 final passed!"
                    : "Section test passed!"
                }`
              : `. Need ${assessment.passPercent}% to pass.`}
          </p>
          {!result.passed && result.missedDays.length > 0 && (
            <div>
              <p>Review these lessons, then submit again.</p>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "0.65rem",
                  marginTop: "0.5rem",
                }}
              >
                {result.missedDays.map((day) => (
                  <Link
                    key={day}
                    to={`/learn/lesson/${day}`}
                    style={{
                      display: "inline-block",
                      padding: "0.45rem 0.85rem",
                      background: "var(--color-crimson)",
                      color: "#fff",
                      fontWeight: 700,
                      textDecoration: "none",
                      borderRadius: 4,
                    }}
                  >
                    Lesson {day}
                  </Link>
                ))}
              </div>
            </div>
          )}
          {result.passed && (
            <p>
              <Link to="/learn">Back to curriculum</Link>
              {assessment.kind === "section" && assessment.section && assessment.section < 4 ? (
                <>
                  {" · "}
                  <Link to={`/test/section/${assessment.section + 1}`}>
                    Next section test
                  </Link>
                </>
              ) : null}
              {assessment.kind === "section" && assessment.section === 4 ? (
                <>
                  {" · "}
                  <Link to="/test/final">Book 1 final test</Link>
                </>
              ) : null}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
