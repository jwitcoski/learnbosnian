import { Link } from "react-router-dom";
import type { Chapter } from "../../types/chapter";
import { getChapter, canViewChapter } from "../../data/loadChapters";
import PuzzleGame from "./PuzzleGame";
import PracticeList from "./PracticeList";
import SectionQuiz from "./SectionQuiz";
import {
  Banner,
  Credit,
  Dialogue,
  GoalList,
  HeroBand,
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

export default function LessonShell({ chapter }: Props) {
  const hero =
    chapter.images?.find((i) => i.id === chapter.culture?.imageId) ||
    chapter.images?.[0];

  const prev = getChapter(chapter.day - 1);
  const next = getChapter(chapter.day + 1);
  const prevOpen = prev ? canViewChapter(prev) : false;
  const nextOpen = next ? canViewChapter(next) : false;

  return (
    <LessonPage>
      {chapter.status === "draft" && (
        <Banner>
          Preview — this chapter is a <strong>draft</strong> awaiting human review
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
              ? "Day 0 · Orientation"
              : `Day ${chapter.day} · Week ${chapter.week}`}{" "}
            · ~{chapter.estimatedMinutes || 60} min
          </div>
          <h1>{chapter.title}</h1>
          <p className="meta">
            {chapter.titleEn} — {chapter.theme}
          </p>
        </div>
      </HeroBand>
      {hero && (
        <Credit>
          <Link to={`/attributions#book1-day-${String(chapter.day).padStart(2, "0")}-${hero.id}`}>
            {hero.credit}
          </Link>
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
          {chapter.images?.[1] && (
            <figure style={{ margin: "1rem 0" }}>
              <div
                style={{
                  width: "100%",
                  aspectRatio: "16 / 9",
                  overflow: "hidden",
                  background: "#efe6d8",
                }}
              >
                <img
                  src={chapter.images[1].localPath}
                  alt={chapter.images[1].alt}
                  style={{
                    width: "100%",
                    height: "100%",
                    display: "block",
                    objectFit: "cover",
                    objectPosition: "center",
                  }}
                />
              </div>
              <Credit as="figcaption">
                <Link
                  to={`/attributions#book1-day-${String(chapter.day).padStart(2, "0")}-${chapter.images[1].id}`}
                >
                  {chapter.images[1].credit}
                </Link>
              </Credit>
            </figure>
          )}
        </Panel>
      )}

      <SectionDivider />

      <Panel id="vocab">
        <h2>Words for today</h2>
        <VocabGrid>
          {chapter.vocabulary.map((v) => (
            <VocabCard key={v.bosnian}>
              <div className="bs">{v.bosnian}</div>
              <div className="en">{v.english}</div>
              {v.pronunciation && <div className="pron">{v.pronunciation}</div>}
            </VocabCard>
          ))}
        </VocabGrid>
      </Panel>

      {chapter.grammar.map((g) => (
        <Panel key={g.title}>
          <h2>{g.title}</h2>
          <p>{g.explanation}</p>
          {g.examples && (
            <GoalList>
              {g.examples.map((ex) => (
                <li key={ex.bosnian}>
                  <strong>{ex.bosnian}</strong> — {ex.english}
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
          <Dialogue>
            {chapter.conversation.lines.map((line, i) => (
              <Line key={`${line.speaker}-${i}`} $speaker={line.speaker}>
                <div className="speaker">{line.speaker}</div>
                <div className="bs">{line.bosnian}</div>
                <div className="en">{line.english}</div>
              </Line>
            ))}
          </Dialogue>
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

      {chapter.puzzles[1] && (
        <Panel id="game">
          <SectionDivider />
          <h2>More practice — game</h2>
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
                {r.note ? ` — ${r.note}` : ""}
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
          <Link to={`/quiz/day/${chapter.day}`}>Day {chapter.day} quiz</Link>
        </p>
        <SectionQuiz chapter={chapter} embedded />
      </Panel>

      <Panel id="continue">
        <SectionDivider />
        <h2>Continue</h2>
        <DayNav>
          {prev ? (
            prevOpen ? (
              <DayNavLink to={`/learn/day/${prev.day}`}>
                ← Day {prev.day}: {prev.title}
              </DayNavLink>
            ) : (
              <span className="soon">← Day {prev.day} · soon</span>
            )
          ) : (
            <Link to="/learn">← All lessons</Link>
          )}
          {next ? (
            nextOpen ? (
              <DayNavLink $primary to={`/learn/day/${next.day}`}>
                Day {next.day}: {next.title} →
              </DayNavLink>
            ) : (
              <span className="soon">
                Day {next.day}: {next.title} · soon
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
