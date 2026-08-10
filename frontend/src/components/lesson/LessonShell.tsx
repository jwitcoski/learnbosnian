import { Link } from "react-router-dom";
import type { Chapter, ChapterImage } from "../../types/chapter";
import { getChapter, canViewChapter } from "../../data/loadChapters";
import { useClipAudio } from "../../hooks/useClipAudio";
import {
  dialogueClipId,
  vocabClipId,
} from "../../lib/audioClips";
import PuzzleGame from "./PuzzleGame";
import PracticeList from "./PracticeList";
import SectionQuiz from "./SectionQuiz";
import {
  Banner,
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
  const { playClip, playingId, missing } = useClipAudio();
  const book = chapter.book || 1;

  return (
    <LessonPage>
      {chapter.status === "draft" && (
        <Banner>
          Preview: this chapter is a <strong>draft</strong> awaiting human review
          before official publish.
        </Banner>
      )}

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
        <h2>Today’s goals</h2>
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
        <h2>Words for today</h2>
        <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
          Tap a word to hear it when a recording is available.
        </p>
        <VocabGrid>
          {chapter.vocabulary.map((v) => {
            const clipId = vocabClipId(book, chapter.day, v.bosnian);
            const isPlaying = playingId === clipId;
            const isMissing = Boolean(missing[clipId]);
            return (
              <VocabCard
                key={v.bosnian}
                type="button"
                onClick={() => playClip(clipId)}
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
                  {isPlaying ? "Playing…" : isMissing ? "Audio soon" : "Tap to hear"}
                </div>
              </VocabCard>
            );
          })}
        </VocabGrid>
        {midImage && <ChapterImageFigure day={chapter.day} image={midImage} />}
      </Panel>

      {chapter.grammar.map((g) => (
        <Panel key={g.title}>
          <h2>{g.title}</h2>
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
        </Panel>
      ))}

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
            Tap a line to hear the voice-over when available.
          </p>
          <Dialogue>
            {chapter.conversation.lines.map((line, i) => {
              const clipId = dialogueClipId(book, chapter.day, i);
              const isPlaying = playingId === clipId;
              const isMissing = Boolean(missing[clipId]);
              return (
                <Line
                  key={`${line.speaker}-${i}`}
                  type="button"
                  $speaker={line.speaker}
                  onClick={() => playClip(clipId)}
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

      {chapter.civicContext && (
        <Panel id="civic-context">
          <SectionDivider />
          <h2>Bosnia today</h2>
          <h3>{chapter.civicContext.title}</h3>
          <p>{chapter.civicContext.body}</p>
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
        <h2>Section quiz</h2>
        <p>
          Or open the dedicated quiz page:{" "}
          <Link to={`/quiz/lesson/${chapter.day}`}>
            Lesson {chapter.day} quiz
          </Link>
        </p>
        <SectionQuiz chapter={chapter} embedded />
      </Panel>

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
