import { Link } from "react-router-dom";
import { listChapters, book1Outline, canViewChapter } from "../../data/loadChapters";
import { getProgress } from "../../hooks/useProgress";
import {
  DayTile,
  LessonPage,
  LockedGrid,
  SectionDivider,
} from "../../components/lesson/styles";

const Learn = () => {
  const chapters = listChapters();
  const progress = getProgress();

  return (
    <LessonPage>
      <h1>Book 1 curriculum</h1>
      <p>
        Start with Lesson 0 (why Bosnian?), then follow Ana, Emir, Amira, and
        Mrvica through Bosnia and Herzegovina. New chapters publish after human
        review.
      </p>
      <p>
        <Link to="/dictionary">Mini-dictionary</Link>
        {" · "}
        <Link to="/books">Book series</Link>
        {" · "}
        <a
          href="https://www.youtube.com/@HowtospeakBosnian"
          target="_blank"
          rel="noreferrer"
        >
          YouTube
        </a>
      </p>

      <SectionDivider />

      {book1Outline.weeks?.map((week) => (
        <section key={week.week} style={{ marginBottom: "2rem" }}>
          <h2>
            {week.week === 0
              ? `Orientation: ${week.title}`
              : `Week ${week.week}: ${week.title}`}
          </h2>
          <p style={{ color: "var(--color-muted)" }}>{week.focus}</p>
          <LockedGrid>
            {chapters
              .filter((c) => c.week === week.week)
              .map((c) => {
                const open = canViewChapter(c);
                const done = progress.completedDays.includes(c.day);
                const inner = (
                  <>
                    <div className="daynum">
                      Lesson {c.day}
                      {done ? " · done" : open ? "" : " · soon"}
                    </div>
                    <div className="title">{c.title}</div>
                    <div className="theme">
                      {open ? c.theme : `Coming soon · Lesson ${c.day}`}
                    </div>
                  </>
                );
                if (open) {
                  return (
                    <DayTile
                      key={c.day}
                      as={Link}
                      to={`/learn/lesson/${c.day}`}
                      $open
                      $done={done}
                    >
                      {inner}
                    </DayTile>
                  );
                }
                return (
                  <DayTile key={c.day} as="div" $open={false} $done={false}>
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

export default Learn;
