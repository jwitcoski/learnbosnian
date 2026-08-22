import { useMemo, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import type {
  GrammarChapter,
  GrammarImage,
  GrammarSlot,
  GrammarTryItem,
} from "../../types/grammar";
import { getGrammarChapter, canViewGrammarChapter } from "../../data/loadGrammar";
import { grammarImageRefFor } from "../../lib/imageRef";
import { useClipAudio } from "../../hooks/useClipAudio";
import {
  collectGrammarSpokenLines,
  grammarDialogueClipId,
  grammarVocabClipId,
} from "../../lib/audioClips";
import {
  getSpeakAttempts,
  incrementSpeakAttempts,
  SPEAK_ATTEMPTS_PER_LESSON,
} from "../../hooks/useReviewDeck";
import SpeakPractice from "../lesson/SpeakPractice";
import {
  ChoiceButton,
  ChoiceRow,
  Credit,
  DayNav,
  DayNavLink,
  Dialogue,
  GrammarCaption,
  GrammarTable,
  HeroBand,
  LessonFigure,
  LessonPage,
  Line,
  NerdBox,
  Panel,
  PrimaryButton,
  SectionDivider,
  VocabCard,
  VocabGrid,
} from "../lesson/styles";

function pickGrammarSpeakTargets(chapter: GrammarChapter): number[] {
  const lines = chapter.look?.items || [];
  const listed = (chapter.speakTargets || []).filter(
    (i) => Number.isInteger(i) && i >= 0 && i < lines.length
  );
  if (listed.length) return listed.slice(0, 3);
  const idxs: number[] = [];
  for (let i = 0; i < lines.length && idxs.length < 3; i += 1) {
    const sp = (lines[i].speaker || "").toLowerCase();
    if (sp === "narrator" || sp === "mrvica") continue;
    idxs.push(i);
  }
  return idxs;
}

function findImage(chapter: GrammarChapter, id?: string): GrammarImage | null {
  if (!id) return null;
  return chapter.images.find((img) => img.id === id) || null;
}

function grammarAttrHash(ref: string, chapterNum: number, id: string) {
  return `/attributions#${
    ref || `grammar-ch-${String(chapterNum).padStart(2, "0")}-${id}`
  }`;
}

function SlotBody({ text }: { text: string }) {
  return (
    <>
      {text.split(/\n\n+/).map((para, i) => (
        <p key={i}>{para}</p>
      ))}
    </>
  );
}

function GrammarImageFigure({
  chapter,
  image,
}: {
  chapter: GrammarChapter;
  image: GrammarImage;
}) {
  if (!image?.localPath) return null;
  const ref = grammarImageRefFor(chapter, image.id);
  return (
    <LessonFigure>
      <div className="frame">
        <img src={image.localPath} alt={image.alt || image.id} />
      </div>
      {image.grammarCaption ? (
        <GrammarCaption>{image.grammarCaption}</GrammarCaption>
      ) : null}
      <Credit as="figcaption">
        <Link to={grammarAttrHash(ref, chapter.chapter, image.id)}>
          {ref ? <span className="ref">{ref}</span> : null}
          {image.credit}
        </Link>
      </Credit>
    </LessonFigure>
  );
}

function TalkSlot({
  slot,
  children,
}: {
  slot: GrammarSlot;
  children?: ReactNode;
}) {
  return (
    <Panel>
      <h2>{slot.heading}</h2>
      <SlotBody text={slot.body} />
      {slot.table ? (
        <GrammarTable>
          <thead>
            <tr>
              {slot.table.headers.map((h) => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {slot.table.rows.map((row) => (
              <tr key={row.join("|")}>
                {row.map((cell, i) => (
                  <td key={`${cell}-${i}`}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </GrammarTable>
      ) : null}
      {children}
    </Panel>
  );
}

function TryList({ items }: { items: GrammarTryItem[] }) {
  const [picked, setPicked] = useState<Record<string, number>>({});
  const [revealed, setRevealed] = useState(false);

  return (
    <div>
      {items.map((item) => {
        const choice = picked[item.id];
        return (
          <div key={item.id} style={{ marginBottom: "1.25rem" }}>
            <p style={{ marginBottom: "0.25rem", fontWeight: 600 }}>
              {item.prompt}
            </p>
            <ChoiceRow>
              {item.options.map((opt, i) => {
                let state: "idle" | "correct" | "wrong" | "missed" = "idle";
                if (revealed) {
                  if (i === item.correctIndex) state = "correct";
                  else if (choice === i) state = "wrong";
                }
                return (
                  <ChoiceButton
                    key={opt}
                    type="button"
                    $state={state}
                    onClick={() => {
                      setPicked({ ...picked, [item.id]: i });
                      if (revealed) setRevealed(false);
                    }}
                  >
                    {opt}
                  </ChoiceButton>
                );
              })}
            </ChoiceRow>
            {revealed && (
              <p
                style={{
                  margin: "0.15rem 0 0",
                  color:
                    choice === item.correctIndex
                      ? "var(--color-sage)"
                      : "var(--color-crimson)",
                  fontWeight: 600,
                }}
              >
                {choice === item.correctIndex
                  ? item.explanation || "Yes."
                  : `No. ${item.explanation || ""}`.trim()}
              </p>
            )}
          </div>
        );
      })}
      <PrimaryButton type="button" onClick={() => setRevealed(true)}>
        Check
      </PrimaryButton>
    </div>
  );
}

function QuickCheck({ chapter }: { chapter: GrammarChapter }) {
  const questions = chapter.quiz.questions || [];
  const pass = chapter.quiz.passPercent || 70;
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<{
    percent: number;
    passed: boolean;
    correct: number;
  } | null>(null);

  if (!questions.length) return null;

  return (
    <Panel id="check">
      <h2>{chapter.quiz.title}</h2>
      {questions.map((q, qi) => (
        <div key={q.id} style={{ marginBottom: "1.35rem" }}>
          <p style={{ fontWeight: 600, marginBottom: "0.4rem" }}>
            {qi + 1}. {q.question}
          </p>
          <ChoiceRow>
            {q.options.map((opt, i) => {
              let state: "idle" | "correct" | "wrong" | "missed" = "idle";
              if (result) {
                if (i === q.correctIndex) state = "correct";
                else if (answers[q.id] === i) state = "wrong";
              }
              return (
                <ChoiceButton
                  key={opt}
                  type="button"
                  $state={state}
                  onClick={() => {
                    setAnswers({ ...answers, [q.id]: i });
                    if (result) setResult(null);
                  }}
                >
                  {opt}
                </ChoiceButton>
              );
            })}
          </ChoiceRow>
          {result && q.explanation ? (
            <p
              style={{
                margin: "0.35rem 0 0",
                color: "var(--color-muted)",
                fontSize: "0.95rem",
              }}
            >
              {q.explanation}
            </p>
          ) : null}
        </div>
      ))}
      <PrimaryButton
        type="button"
        onClick={() => {
          const correct = questions.filter(
            (q) => answers[q.id] === q.correctIndex
          ).length;
          const percent = Math.round((correct / questions.length) * 100);
          setResult({
            percent,
            passed: percent >= pass,
            correct,
          });
        }}
      >
        Check
      </PrimaryButton>
      {result ? (
        <p style={{ marginTop: "0.85rem", fontWeight: 700 }}>
          {result.correct} of {questions.length}. {result.percent}%.{" "}
          {result.passed ? "Good." : "Look back at the piles and try again."}
        </p>
      ) : null}
    </Panel>
  );
}

type Props = { chapter: GrammarChapter };

export default function GrammarShell({ chapter }: Props) {
  const hero = findImage(chapter, chapter.imageSlots.hero);
  const afterPattern = findImage(chapter, chapter.imageSlots.afterPattern);
  const afterNerd = findImage(chapter, chapter.imageSlots.afterNerd);
  const prev = getGrammarChapter(chapter.chapter - 1);
  const nextDraft = getGrammarChapter(chapter.chapter + 1);
  const prevOpen = prev ? canViewGrammarChapter(prev) : false;
  const nextOpen = nextDraft ? canViewGrammarChapter(nextDraft) : false;
  const heroRef = hero ? grammarImageRefFor(chapter, hero.id) : "";
  const spokenLines = useMemo(
    () => collectGrammarSpokenLines(chapter),
    [chapter]
  );
  const vocab = chapter.vocabulary || [];
  const speakTargets = useMemo(
    () => pickGrammarSpeakTargets(chapter),
    [chapter]
  );
  const attemptKey = `grammar-${chapter.chapter}`;
  const [attemptsUsed, setAttemptsUsed] = useState(() =>
    getSpeakAttempts(attemptKey)
  );
  const attemptsLeft = Math.max(0, SPEAK_ATTEMPTS_PER_LESSON - attemptsUsed);
  const {
    playClip,
    playingId,
    missing,
    rate,
    loop,
    setPlaybackRate,
    setLooping,
  } = useClipAudio();

  const playSpoken = (bosnian: string) => {
    const index = spokenLines.findIndex(
      (line) => line.bosnian.trim().toLowerCase() === bosnian.trim().toLowerCase()
    );
    if (index < 0) return;
    playClip(grammarDialogueClipId(chapter.chapter, index), { loop, rate });
  };

  return (
    <LessonPage>
      <p>
        <Link to="/learn/grammar">← Grammar</Link>
      </p>
      <HeroBand>
        {hero?.localPath && (
          <div className="hero-media">
            <img src={hero.localPath} alt={hero.alt || chapter.title} />
          </div>
        )}
        <div className="hero-copy">
          <div className="meta">
            Chapter {chapter.chapter} · ~{chapter.estimatedMinutes || 40} min
          </div>
          <h1>{chapter.title}</h1>
          <p className="meta">
            {chapter.titleEn}. {chapter.theme}
          </p>
        </div>
      </HeroBand>
      {hero && (
        <>
          {hero.grammarCaption ? (
            <GrammarCaption>{hero.grammarCaption}</GrammarCaption>
          ) : null}
          <Credit>
            <Link to={grammarAttrHash(heroRef, chapter.chapter, hero.id)}>
              {heroRef ? <span className="ref">{heroRef}</span> : null}
              {hero.credit}
            </Link>
          </Credit>
        </>
      )}

      <TalkSlot slot={chapter.whyHere} />
      <SectionDivider />
      <TalkSlot slot={chapter.englishLies} />
      <SectionDivider />
      <TalkSlot slot={chapter.knownLine}>
        {chapter.knownLine.bosnian ? (
          <SpokenLine
            speaker={chapter.knownLine.speaker || "Ana"}
            bosnian={chapter.knownLine.bosnian}
            english={chapter.knownLine.english || ""}
            clipId={grammarDialogueClipId(
              chapter.chapter,
              Math.max(
                0,
                spokenLines.findIndex(
                  (line) =>
                    line.bosnian.trim().toLowerCase() ===
                    chapter.knownLine.bosnian?.trim().toLowerCase()
                )
              )
            )}
            playingId={playingId}
            missing={missing}
            onPlay={() => playSpoken(chapter.knownLine.bosnian || "")}
          />
        ) : null}
      </TalkSlot>
      <SectionDivider />
      <TalkSlot slot={chapter.pattern}>
        {afterPattern ? (
          <GrammarImageFigure chapter={chapter} image={afterPattern} />
        ) : null}
      </TalkSlot>
      {chapter.howYouGuess ? (
        <>
          <SectionDivider />
          <TalkSlot slot={chapter.howYouGuess} />
        </>
      ) : null}
      {chapter.trick ? (
        <>
          <SectionDivider />
          <TalkSlot slot={chapter.trick} />
        </>
      ) : null}
      <SectionDivider />
      <NerdBox>
        <h2>{chapter.nerd.heading}</h2>
        <SlotBody text={chapter.nerd.body} />
      </NerdBox>
      {afterNerd ? (
        <GrammarImageFigure chapter={chapter} image={afterNerd} />
      ) : null}

      {vocab.length ? (
        <>
          <SectionDivider />
          <Panel id="words">
            <h2>Sample words</h2>
            <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
              Tap a word to hear it.
            </p>
            <VocabGrid>
              {vocab.map((v) => {
                const clipId = grammarVocabClipId(chapter.chapter, v.bosnian);
                const isPlaying = playingId === clipId;
                const isMissing = Boolean(missing[clipId]);
                return (
                  <VocabCard
                    key={v.bosnian}
                    type="button"
                    onClick={() => {
                      if (!isMissing) playClip(clipId, { loop, rate });
                    }}
                    data-playing={isPlaying ? "true" : "false"}
                    data-missing={isMissing ? "true" : "false"}
                    aria-label={`Play pronunciation for ${v.bosnian}`}
                  >
                    <div className="bs">{v.bosnian}</div>
                    <div className="en">{v.english}</div>
                    {v.pronunciation ? (
                      <div className="pron">{v.pronunciation}</div>
                    ) : null}
                    <div className="listen">
                      {isPlaying
                        ? "Playing…"
                        : isMissing
                        ? "Audio soon"
                        : "Tap to hear"}
                    </div>
                  </VocabCard>
                );
              })}
            </VocabGrid>
          </Panel>
        </>
      ) : null}

      {chapter.look?.items?.length ? (
        <>
          <SectionDivider />
          <Panel>
            <h2>{chapter.look.heading}</h2>
            <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
              Each line has a speaker. Tap the line to hear it. On some lines
              you can record yourself for a short Speak Check.
            </p>
            <div
              style={{
                display: "flex",
                gap: "0.5rem",
                flexWrap: "wrap",
                marginBottom: "0.75rem",
              }}
            >
              <PrimaryButton type="button" onClick={() => setLooping(!loop)}>
                Loop: {loop ? "on" : "off"}
              </PrimaryButton>
              <PrimaryButton
                type="button"
                onClick={() => setPlaybackRate(rate === 1 ? 0.75 : 1)}
              >
                Speed: {rate === 1 ? "1×" : "0.75×"}
              </PrimaryButton>
            </div>
            <Dialogue>
              {chapter.look.items.map((item, i) => {
                const index = spokenLines.findIndex(
                  (line) =>
                    line.bosnian.trim().toLowerCase() ===
                    item.bosnian.trim().toLowerCase()
                );
                const clipId = grammarDialogueClipId(
                  chapter.chapter,
                  index < 0 ? i : index
                );
                return (
                  <SpokenLine
                    key={`${item.speaker}-${item.bosnian}-${i}`}
                    speaker={item.speaker}
                    bosnian={item.bosnian}
                    english={item.english}
                    clipId={clipId}
                    playingId={playingId}
                    missing={missing}
                    onPlay={() => playSpoken(item.bosnian)}
                  >
                    {speakTargets.includes(i) ? (
                      <SpeakPractice
                        day={chapter.chapter}
                        lineIndex={i}
                        bosnian={item.bosnian}
                        english={item.english}
                        vocabulary={vocab.map((word) => word.bosnian)}
                        attemptsLeft={attemptsLeft}
                        onAiAttempt={() =>
                          setAttemptsUsed(incrementSpeakAttempts(attemptKey))
                        }
                      />
                    ) : null}
                  </SpokenLine>
                );
              })}
            </Dialogue>
          </Panel>
        </>
      ) : null}

      {chapter.try?.items?.length ? (
        <>
          <SectionDivider />
          <Panel>
            <h2>{chapter.try.heading}</h2>
            <TryList items={chapter.try.items} />
          </Panel>
        </>
      ) : null}

      <SectionDivider />
      <QuickCheck chapter={chapter} />

      <SectionDivider />
      <Panel>
        <h2>Next</h2>
        <p>{chapter.next.body}</p>
      </Panel>

      <DayNav>
        {prevOpen && prev ? (
          <DayNavLink to={`/learn/grammar/${prev.chapter}`}>
            ← Chapter {prev.chapter}
          </DayNavLink>
        ) : (
          <Link to="/learn/grammar">← All chapters</Link>
        )}
        {nextOpen && nextDraft ? (
          <DayNavLink $primary to={`/learn/grammar/${nextDraft.chapter}`}>
            Chapter {nextDraft.chapter} →
          </DayNavLink>
        ) : (
          <span className="soon">Next chapter is not up yet</span>
        )}
      </DayNav>
    </LessonPage>
  );
}

function SpokenLine({
  speaker,
  bosnian,
  english,
  clipId,
  playingId,
  missing,
  onPlay,
  children,
}: {
  speaker: string;
  bosnian: string;
  english: string;
  clipId: string;
  playingId: string | null;
  missing: Record<string, true>;
  onPlay: () => void;
  children?: ReactNode;
}) {
  const isPlaying = playingId === clipId;
  const isMissing = Boolean(missing[clipId]);
  return (
    <Line
      $speaker={speaker}
      data-playing={isPlaying ? "true" : "false"}
      data-missing={isMissing ? "true" : "false"}
      style={{ marginTop: "0.75rem" }}
    >
      <button
        type="button"
        className="play"
        onClick={onPlay}
        aria-label={`Play line by ${speaker}`}
      >
        <div className="speaker">{speaker}</div>
        <div className="bs">{bosnian}</div>
        <div className="en">{english}</div>
        <div className="listen">
          {isPlaying ? "Playing…" : isMissing ? "Audio soon" : "Tap to hear"}
        </div>
      </button>
      {children}
    </Line>
  );
}
