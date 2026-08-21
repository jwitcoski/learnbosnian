import { Link } from "react-router-dom";
import {
  grammarOutline,
  getGrammarChapter,
  canViewGrammarChapter,
} from "../../data/loadGrammar";
import {
  DayTile,
  LessonPage,
  LockedGrid,
  SectionDivider,
} from "../../components/lesson/styles";

const Grammar = () => {
  return (
    <LessonPage>
      <p>
        <Link to="/learn">← All books</Link>
      </p>
      <h1>{grammarOutline.title}</h1>
      <p>{grammarOutline.summary}</p>
      <p style={{ color: "var(--color-muted)" }}>{grammarOutline.pedagogy}</p>

      <SectionDivider />

      {grammarOutline.parts.map((part) => (
        <section key={part.part} style={{ marginBottom: "2rem" }}>
          <h2>
            Part {part.part}. {part.title}
          </h2>
          <p style={{ color: "var(--color-muted)" }}>{part.focus}</p>
          <LockedGrid>
            {part.chapters.map((n) => {
              const listed = grammarOutline.chapters.find(
                (c) => c.chapter === n
              );
              const drafted = getGrammarChapter(n);
              const open = listed ? canViewGrammarChapter(listed) : false;
              const title = drafted?.title || listed?.title || `Chapter ${n}`;
              const theme = drafted?.theme || listed?.theme || "";
              const inner = (
                <>
                  <div className="daynum">
                    Chapter {n}
                    {open ? "" : " · soon"}
                  </div>
                  <div className="title">{title}</div>
                  <div className="theme">{open ? theme : "Not drafted yet"}</div>
                </>
              );
              if (open && drafted) {
                return (
                  <DayTile
                    key={n}
                    as={Link}
                    to={`/learn/grammar/${n}`}
                    $open
                    $done={false}
                  >
                    {inner}
                  </DayTile>
                );
              }
              return (
                <DayTile key={n} as="div" $open={false} $done={false}>
                  {inner}
                </DayTile>
              );
            })}
          </LockedGrid>
        </section>
      ))}
    </LessonPage>
  );
};

export default Grammar;
