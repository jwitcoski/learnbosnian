import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Chapter, ChapterImage } from "../../types/chapter";
import { getChapter, canViewChapter } from "../../data/loadChapters";
import { useClipAudio } from "../../hooks/useClipAudio";
import {
  dialogueClipId,
  vocabClipId,
} from "../../lib/audioClips";
import {
  getSpeakAttempts,
  incrementSpeakAttempts,
  SPEAK_ATTEMPTS_PER_LESSON,
} from "../../hooks/useReviewDeck";
import PuzzleGame from "./PuzzleGame";
import PracticeList from "./PracticeList";
import SectionQuiz from "./SectionQuiz";
import AuthenticListenPanel from "./AuthenticListenPanel";
import SpeakPractice from "./SpeakPractice";
import ReviewDeck from "./ReviewDeck";
import CanDoChecklist from "./CanDoChecklist";
import { PrimaryButton } from "./styles";
import {
  Credit,
  Dialogue,
  GoalList,
  HeroBand,
  LessonFigure,
  LessonPage,
  Line,
  Panel,
  SectionDivider,
  VocabCard,
  VocabGrid,
  DayNav,
  DayNavLink,
} from "./styles";

type Props = { chapter: Chapter };

function attrHash(day: number, id: string) {
  return `/attributions#book1-day-${String(day).padStart(2, "0")}-${id}`;
}

function ChapterImageFigure({
  day,
  image,
}: {
  day: number;
  image: ChapterImage;
}) {
  if (!image?.localPath) return null;
  return (
    <LessonFigure>
      <div className="frame">
        <img src={image.localPath} alt={image.alt || image.id} />
      </div>
      <Credit as="figcaption">
        <Link to={attrHash(day, image.id)}>{image.credit}</Link>
      </Credit>
    </LessonFigure>
  );
}

function pickSpeakTargets(chapter: Chapter): number[] {
  if (chapter.speakTargets?.length) return chapter.speakTargets.slice(0, 3);
  const lines = chapter.conversation?.lines || [];
  const idxs: number[] = [];
  for (let i = 0; i < lines.length && idxs.length < 3; i += 1) {
    const sp = (lines[i].speaker || "").toLowerCase();
    if (sp === "narrator" || sp === "mrvica") continue;
    idxs.push(i);
  }
  return idxs;
}

export default function LessonShell({ chapter }: Props) {
  const images = chapter.images || [];
  const civicImageId = chapter.civicContext?.imageId || null;
  const hero =
    images.find((i) => i.id === chapter.culture?.imageId) || images[0];
  const rest = images.filter(
    (i) => i.id !== hero?.id && i.id !== civicImageId
  );
  const cultureImage = rest[0];
  const midImage = rest[1];
  const moreImages = rest.slice(2);

  const prev = getChapter(chapter.day - 1);
  const next = getChapter(chapter.day + 1);
  const prevOpen = prev ? canViewChapter(prev) : false;
  const nextOpen = next ? canViewChapter(next) : false;
  const {
    playClip,
    playingId,
    missing,
    rate,
    loop,
    setPlaybackRate,
    setLooping,
  } = useClipAudio();
  const book = chapter.book || 1;

  const [attemptsUsed, setAttemptsUsed] = useState(() =>
    getSpeakAttempts(chapter.day)
  );
  const speakTargets = useMemo(() => pickSpeakTargets(chapter), [chapter]);
  const attemptsLeft = Math.max(0, SPEAK_ATTEMPTS_PER_LESSON - attemptsUsed);

  const videoResource = chapter.resources?.find(
    (r) =>
      /youtube|video|watch/i.test(r.label) ||
      /youtu\.be|youtube\.com/.test(r.url)
  );

  return (
    <LessonPage>
      <HeroBand>
        {hero?.localPath && (
          <div className="hero-media">
            <img src={hero.localPath} alt={hero.alt || chapter.title} />
          </div>
        )}
        <div className="hero-copy">
          <div className="meta">
            {chapter.day === 0
              ? "Lesson 0 · Orientation"
              : `Lesson ${chapter.day}`}{" "}
            · ~{chapter.estimatedMinutes || 60} min
          </div>
          <h1>{chapter.title}</h1>
          <p className="meta">
            {chapter.titleEn}. {chapter.theme}
          </p>
        </div>
      </HeroBand>
      {hero && (
        <Credit>
          <Link to={attrHash(chapter.day, hero.id)}>{hero.credit}</Link>
        </Credit>
      )}

      <Panel id="goals">
        <h2>Lesson goals</h2>
        <h3>Vocabulary</h3>
        <GoalList>
          {chapter.learningGoals.vocabulary.map((g) => (
            <li key={g}>{g}</li>
          ))}
        </GoalList>
        <h3>Grammar</h3>
        <GoalList>
          {chapter.learningGoals.grammar.map((g) => (
            <li key={g}>{g}</li>
          ))}
        </GoalList>
        <h3>Culture</h3>
        <GoalList>
          {chapter.learningGoals.culture.map((g) => (
            <li key={g}>{g}</li>
          ))}
        </GoalList>
      </Panel>

      {videoResource && (
        <Panel id="video">
          <SectionDivider />
          <h2>Watch the companion video</h2>
          <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
            Start here when you can. Then return for words, dialogue, and
            practice on this page.
          </p>
          <p>
            <a href={videoResource.url} target="_blank" rel="noreferrer">
              {videoResource.label}
            </a>
            {videoResource.note ? `. ${videoResource.note}` : ""}
          </p>
        </Panel>
      )}

      <SectionDivider />

      {chapter.culture && (
        <Panel id="culture">
          <h2>{chapter.culture.title}</h2>
          <p>{chapter.culture.body}</p>
          {cultureImage && (
            <ChapterImageFigure day={chapter.day} image={cultureImage} />
          )}
        </Panel>
      )}

      <SectionDivider />

      <Panel id="vocab">
        <h2>Lesson vocabulary</h2>
        <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
          Tap any word to hear it. Loop and slow speed help with shadowing.
        </p>
        <div
          style={{
            display: "flex",
            gap: "0.5rem",
            flexWrap: "wrap",
            marginBottom: "0.75rem",
          }}
        >
          <PrimaryButton
            type="button"
            onClick={() => setLooping(!loop)}
          >
            Loop: {loop ? "on" : "off"}
          </PrimaryButton>
          <PrimaryButton
            type="button"
            onClick={() => setPlaybackRate(rate === 1 ? 0.75 : 1)}
          >
            Speed: {rate === 1 ? "1×" : "0.75×"}
          </PrimaryButton>
        </div>
        <VocabGrid>
          {chapter.vocabulary.map((v) => {
            const clipId = vocabClipId(book, chapter.day, v.bosnian);
            const isPlaying = playingId === clipId;
            const isMissing = Boolean(missing[clipId]);
            return (
              <VocabCard
                key={v.bosnian}
                type="button"
                onClick={() => {
                  if (!isMissing) {
                    playClip(clipId, { loop, rate });
                  }
                }}
                data-playing={isPlaying ? "true" : "false"}
                data-missing={isMissing ? "true" : "false"}
                aria-label={`Play pronunciation for ${v.bosnian}`}
              >
                <div className="bs">{v.bosnian}</div>
                <div className="en">{v.english}</div>
                {v.pronunciation && (
                  <div className="pron">{v.pronunciation}</div>
                )}
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
        {midImage && <ChapterImageFigure day={chapter.day} image={midImage} />}
      </Panel>

      <Panel id="grammar">
        <SectionDivider />
        <h2>Grammar</h2>
        {chapter.grammar.map((g) => (
          <div key={g.title} style={{ marginBottom: "1.25rem" }}>
            <h3>{g.title}</h3>
            <p>{g.explanation}</p>
            {g.examples && (
              <GoalList>
                {g.examples.map((ex) => (
                  <li key={ex.bosnian}>
                    <strong>{ex.bosnian}</strong>: {ex.english}
                  </li>
                ))}
              </GoalList>
            )}
          </div>
        ))}
      </Panel>

      {chapter.sayAgain?.lines?.length ? (
        <Panel id="say-again">
          <SectionDivider />
          <h2>{chapter.sayAgain.title || "Say again"}</h2>
          {chapter.sayAgain.intro ? (
            <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
              {chapter.sayAgain.intro}
            </p>
          ) : null}
          <GoalList>
            {chapter.sayAgain.lines.map((line) => (
              <li key={line.bosnian}>
                <strong>{line.bosnian}</strong>: {line.english}
              </li>
            ))}
          </GoalList>
        </Panel>
      ) : null}

      {chapter.lessonBlocks.map((block, idx) => (
        <Panel key={block.id} id={`lesson-${block.id}`}>
          <SectionDivider />
          <h2>{block.title}</h2>
          <p>{block.body}</p>
          {block.tips && (
            <GoalList>
              {block.tips.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </GoalList>
          )}
          {idx === 0 && chapter.puzzles[0] && (
            <>
              <SectionDivider />
              <PuzzleGame puzzle={chapter.puzzles[0]} />
            </>
          )}
        </Panel>
      ))}

      {chapter.conversation && chapter.conversation.lines?.length > 0 && (
        <Panel id="conversation">
          <SectionDivider />
          <h2>{chapter.conversation.title}</h2>
          <p style={{ color: "var(--color-muted)" }}>
            {chapter.conversation.setting}
          </p>
          <p style={{ color: "var(--color-muted)" }}>
            Play the full scene once (cover the English with your hand if you
            can), then tap individual lines. Use Speak on the highlighted lines.
          </p>
          <div
            style={{
              display: "flex",
              gap: "0.5rem",
              flexWrap: "wrap",
              marginBottom: "0.75rem",
            }}
          >
            <PrimaryButton
              type="button"
              onClick={() => {
                const first = dialogueClipId(book, chapter.day, 0);
                playClip(first, { loop: false, rate });
              }}
            >
              Play first line
            </PrimaryButton>
            <PrimaryButton
              type="button"
              onClick={() => setLooping(!loop)}
            >
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
            {chapter.conversation.lines.map((line, i) => {
              const clipId = dialogueClipId(book, chapter.day, i);
              const isPlaying = playingId === clipId;
              const isMissing = Boolean(missing[clipId]);
              const isSpeak = speakTargets.includes(i);
              return (
                <div key={`${line.speaker}-${i}`}>
                  <Line
                    type="button"
                    $speaker={line.speaker}
                    onClick={() => playClip(clipId, { loop, rate })}
                    data-playing={isPlaying ? "true" : "false"}
                    data-missing={isMissing ? "true" : "false"}
                    aria-label={`Play dialogue line by ${line.speaker}`}
                  >
                    <div className="speaker">{line.speaker}</div>
                    <div className="bs">{line.bosnian}</div>
                    <div className="en">{line.english}</div>
                    <div className="listen">
                      {isPlaying
                        ? "Playing…"
                        : isMissing
                        ? "Audio soon"
                        : "Tap to hear"}
                    </div>
                  </Line>
                  {isSpeak && (
                    <SpeakPractice
                      day={chapter.day}
                      lineIndex={i}
                      bosnian={line.bosnian}
                      english={line.english}
                      vocabulary={chapter.vocabulary.map((v) => v.bosnian)}
                      teacherPlay={() => playClip(clipId, { loop: false, rate })}
                      teacherPlaying={isPlaying}
                      attemptsLeft={attemptsLeft}
                      onAiAttempt={() =>
                        setAttemptsUsed(incrementSpeakAttempts(chapter.day))
                      }
                    />
                  )}
                </div>
              );
            })}
          </Dialogue>
        </Panel>
      )}

      {moreImages.length > 0 && (
        <Panel id="more-photos">
          <SectionDivider />
          <h2>More scenes</h2>
          {moreImages.map((img) => (
            <ChapterImageFigure key={img.id} day={chapter.day} image={img} />
          ))}
        </Panel>
      )}

      {chapter.practice?.length > 0 && (
        <Panel id="practice">
          <SectionDivider />
          <h2>Practice</h2>
          <PracticeList items={chapter.practice} />
        </Panel>
      )}

      {chapter.funFacts?.length > 0 && (
        <Panel id="fun-facts">
          <SectionDivider />
          <h2>Fun facts</h2>
          {chapter.funFacts.map((f) => (
            <div key={f.title} style={{ marginBottom: "1rem" }}>
              <h3>{f.title}</h3>
              <p>{f.body}</p>
            </div>
          ))}
        </Panel>
      )}

      {chapter.authenticListen && (
        <Panel id="authentic-listen">
          <SectionDivider />
          <h2>{chapter.authenticListen.title}</h2>
          <AuthenticListenPanel block={chapter.authenticListen} />
        </Panel>
      )}

      {chapter.civicContext && (
        <Panel id="civic-context">
          <SectionDivider />
          <h2>Bosnia today</h2>
          <h3>{chapter.civicContext.title}</h3>
          <p>{chapter.civicContext.body}</p>
          {chapter.civicContext.learnMore?.url && (
            <p style={{ marginTop: "0.75rem" }}>
              <a
                href={chapter.civicContext.learnMore.url}
                target="_blank"
                rel="noreferrer"
              >
                {chapter.civicContext.learnMore.label || "Read more"}
              </a>
            </p>
          )}
          {(() => {
            const civicImg = images.find(
              (i) => i.id === chapter.civicContext?.imageId
            );
            return civicImg ? (
              <ChapterImageFigure day={chapter.day} image={civicImg} />
            ) : null;
          })()}
        </Panel>
      )}

      {chapter.puzzles[1] && (
        <Panel id="game">
          <SectionDivider />
          <h2>More practice: game</h2>
          <PuzzleGame puzzle={chapter.puzzles[1]} />
        </Panel>
      )}

      <Panel id="review-deck">
        <SectionDivider />
        <ReviewDeck day={chapter.day} lessonVocab={chapter.vocabulary || []} />
      </Panel>

      {chapter.canDoChecks && chapter.canDoChecks.length > 0 && (
        <Panel id="can-do">
          <SectionDivider />
          <CanDoChecklist items={chapter.canDoChecks} />
        </Panel>
      )}

      {chapter.resources?.length > 0 && (
        <Panel id="resources">
          <SectionDivider />
          <h2>Additional resources</h2>
          <GoalList>
            {chapter.resources.map((r) => (
              <li key={r.url}>
                <a href={r.url} target="_blank" rel="noreferrer">
                  {r.label}
                </a>
                {r.note ? `. ${r.note}` : ""}
              </li>
            ))}
          </GoalList>
        </Panel>
      )}

      <Panel id="quiz">
        <SectionDivider />
        <h2>Lesson quiz</h2>
        <p>
          Or open the dedicated quiz page:{" "}
          <Link to={`/quiz/lesson/${chapter.day}`}>
            Lesson {chapter.day} quiz
          </Link>
        </p>
        <SectionQuiz chapter={chapter} embedded />
      </Panel>

      {(chapter.day === 7 ||
        chapter.day === 14 ||
        chapter.day === 21 ||
        chapter.day === 30) && (
        <Panel id="section-test">
          <SectionDivider />
          <h2>{chapter.day === 30 ? "Tests" : "Section test"}</h2>
          {chapter.day === 30 ? (
            <>
              <p>
                Finish Section 4 with its section test, then take the Book 1
                final covering Lessons 1 to 30.
              </p>
              <p>
                <Link to="/test/section/4">Open Section 4 test</Link>
                {" · "}
                <Link to="/test/final">Open Book 1 final test</Link>
              </p>
            </>
          ) : (
            <>
              <p>
                After this review, take the Section {chapter.section} test
                covering the lessons in this section.
              </p>
              <p>
                <Link to={`/test/section/${chapter.section}`}>
                  Open Section {chapter.section} test
                </Link>
              </p>
            </>
          )}
        </Panel>
      )}

      <Panel id="continue">
        <SectionDivider />
        <h2>Continue</h2>
        <DayNav>
          {prev ? (
            prevOpen ? (
              <DayNavLink to={`/learn/lesson/${prev.day}`}>
                ← Lesson {prev.day}: {prev.title}
              </DayNavLink>
            ) : (
              <span className="soon">← Lesson {prev.day} · soon</span>
            )
          ) : (
            <Link to="/learn">← All lessons</Link>
          )}
          {next ? (
            nextOpen ? (
              <DayNavLink $primary to={`/learn/lesson/${next.day}`}>
                Lesson {next.day}: {next.title} →
              </DayNavLink>
            ) : (
              <span className="soon">
                Lesson {next.day}: {next.title} · soon
              </span>
            )
          ) : (
            <Link to="/learn">Curriculum →</Link>
          )}
        </DayNav>
      </Panel>
    </LessonPage>
  );
}
