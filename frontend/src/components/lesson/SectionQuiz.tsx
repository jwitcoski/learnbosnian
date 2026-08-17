import { useState } from "react";
import { Link } from "react-router-dom";
import type { Chapter, QuizSkill } from "../../types/chapter";
import { saveQuizScore } from "../../hooks/useProgress";
import { addMissedWords } from "../../hooks/useReviewDeck";
import { PrimaryButton } from "./styles";

type Props = {
  chapter: Chapter;
  embedded?: boolean;
};

const SKILL_LINKS: {
  skill: QuizSkill;
  label: string;
  hash: string;
  available: (ch: Chapter) => boolean;
}[] = [
  {
    skill: "vocabulary",
    label: "Review Words",
    hash: "vocab",
    available: (ch) => (ch.vocabulary?.length || 0) > 0,
  },
  {
    skill: "grammar",
    label: "Review Grammar",
    hash: "grammar",
    available: (ch) => (ch.grammar?.length || 0) > 0,
  },
  {
    skill: "dialogue",
    label: "Review Dialogue",
    hash: "conversation",
    available: (ch) => (ch.conversation?.lines?.length || 0) > 0,
  },
  {
    skill: "listening",
    label: "Hear Bosnia",
    hash: "authentic-listen",
    available: (ch) => Boolean(ch.authenticListen),
  },
];

function fallbackSkills(ch: Chapter): QuizSkill[] {
  const out: QuizSkill[] = [];
  if (ch.vocabulary?.length) out.push("vocabulary");
  if (ch.grammar?.length) out.push("grammar");
  if (ch.conversation?.lines?.length) out.push("dialogue");
  if (ch.practice?.length) out.push("vocabulary");
  return out;
}

function questionText(q: Chapter["sectionQuiz"]["questions"][number]): string {
  return q.question || (q as { prompt?: string }).prompt || "";
}

export default function SectionQuiz({ chapter, embedded }: Props) {
  const questions = chapter.sectionQuiz?.questions || [];
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<{
    percent: number;
    passed: boolean;
    correctCount: number;
    missedSkills: Record<string, number>;
  } | null>(null);

  if (!questions.length) {
    return <p>This quiz will appear when the lesson is fully drafted.</p>;
  }

  const submit = () => {
    let correct = 0;
    const missedSkills: Record<string, number> = {};
    const missedVocab: { bosnian: string; english: string; day: number }[] = [];

    questions.forEach((q) => {
      const ok = answers[q.id] === q.correctIndex;
      if (ok) {
        correct += 1;
        return;
      }
      const skill = q.skill || "vocabulary";
      missedSkills[skill] = (missedSkills[skill] || 0) + 1;
      // Heuristic: pull a matching vocab card from the question text
      const text = questionText(q).toLowerCase();
      const hit = chapter.vocabulary?.find((v) =>
        text.includes(v.bosnian.toLowerCase())
      );
      if (hit) {
        missedVocab.push({
          bosnian: hit.bosnian,
          english: hit.english,
          day: chapter.day,
        });
      }
    });

    if (missedVocab.length) addMissedWords(missedVocab);

    const percent = Math.round((correct / questions.length) * 100);
    const passPercent = chapter.sectionQuiz.passPercent ?? 70;
    const passed = percent >= passPercent;
    saveQuizScore(chapter.day, percent);
    setResult({ percent, passed, correctCount: correct, missedSkills });
  };

  const pick = (questionId: string, optionIndex: number) => {
    setAnswers({ ...answers, [questionId]: optionIndex });
    if (result) setResult(null);
  };

  const remediationSkills = (() => {
    if (!result || result.passed) return [];
    const keys = Object.keys(result.missedSkills) as QuizSkill[];
    if (keys.length === 0) return fallbackSkills(chapter);
    return keys;
  })();

  const hrefFor = (hash: string) => {
    if (embedded) return `#${hash}`;
    return `/learn/lesson/${chapter.day}#${hash}`;
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
                {qi + 1}. {questionText(q)}
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
        {result ? "Submit again" : "Submit quiz"}
      </PrimaryButton>
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>
            Score:{" "}
            <strong>
              {result.correctCount}/{questions.length} ({result.percent}%)
            </strong>
            {result.passed ? ". Lesson complete." : null}
          </p>
          {!result.passed && (
            <div>
              <p>Review the linked parts, then submit again.</p>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "0.65rem",
                  marginTop: "0.5rem",
                }}
              >
                {SKILL_LINKS.filter(
                  (s) =>
                    remediationSkills.includes(s.skill) &&
                    s.available(chapter)
                ).map((s) => (
                  <Link
                    key={s.hash}
                    to={hrefFor(s.hash)}
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
                    {s.label}
                    {result.missedSkills[s.skill]
                      ? ` (${result.missedSkills[s.skill]} misses)`
                      : ""}
                  </Link>
                ))}
                {chapter.practice?.length > 0 &&
                  (remediationSkills.includes("vocabulary") ||
                    remediationSkills.includes("grammar") ||
                    remediationSkills.includes("dialogue")) && (
                    <Link
                      to={hrefFor("practice")}
                      style={{
                        display: "inline-block",
                        padding: "0.45rem 0.85rem",
                        background: "var(--color-brown, #5d4037)",
                        color: "#fff",
                        fontWeight: 700,
                        textDecoration: "none",
                        borderRadius: 4,
                      }}
                    >
                      Review Practice
                    </Link>
                  )}
              </div>
            </div>
          )}
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
