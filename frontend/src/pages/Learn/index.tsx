import { Link } from "react-router-dom";
import { listChapters, book1Outline, canViewChapter } from "../../data/loadChapters";
import { getFinalTest, getSectionTest } from "../../data/loadAssessments";
import {
  getProgress,
  isAssessmentPassed,
} from "../../hooks/useProgress";
import {
  DayTile,
  LessonPage,
  LockedGrid,
  SectionDivider,
} from "../../components/lesson/styles";

const Learn = () => {
  const chapters = listChapters();
  const progress = getProgress();
  const finalTest = getFinalTest();

  return (
    <LessonPage>
      <h1>Book 1 curriculum</h1>
      <p>
        Start with Lesson 0 (Why Bosnian?). Then follow Ana, Emir, Amira, and
        Mrvica across Bosnia and Herzegovina. New lessons go live after review.
      </p>
      <p>
        Book 1 has Lesson 0 plus Lessons 1 to 30 in four sections. Each section
        ends with a <strong>section test</strong>. After Lesson 30, take the{" "}
        <strong>Book 1 final test</strong>.
      </p>
      <p>
        <Link to="/dictionary">Dictionary</Link>
        {" · "}
        <Link to="/books">Book series</Link>
        {" · "}
        <Link to="/test/final">Final test</Link>
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

      {book1Outline.sections?.map((sec) => {
        const sectionTest =
          sec.section >= 1 && sec.section <= 4
            ? getSectionTest(sec.section)
            : undefined;
        const testPassed = sectionTest
          ? isAssessmentPassed(sectionTest.id, sectionTest.passPercent)
          : false;
        const testScore = sectionTest
          ? progress.assessmentScores?.[sectionTest.id]
          : undefined;

        return (
          <section key={sec.section} style={{ marginBottom: "2rem" }}>
            <h2>
              {sec.section === 0
                ? `Orientation: ${sec.title}`
                : `Section ${sec.section}: ${sec.title}`}
            </h2>
            <p style={{ color: "var(--color-muted)" }}>{sec.focus}</p>
            <LockedGrid>
              {chapters
                .filter((c) => c.section === sec.section)
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
                        {open ? c.theme : `Lesson ${c.day} · coming soon`}
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
              {sectionTest && (
                <DayTile
                  as={Link}
                  to={`/test/section/${sec.section}`}
                  $open
                  $done={testPassed}
                >
                  <div className="daynum">
                    Section {sec.section} test
                    {testPassed
                      ? " · passed"
                      : typeof testScore === "number"
                        ? ` · ${testScore}%`
                        : ""}
                  </div>
                  <div className="title">{sectionTest.title}</div>
                  <div className="theme">
                    Lessons {sectionTest.coversDays[0]}–
                    {sectionTest.coversDays[sectionTest.coversDays.length - 1]} ·{" "}
                    {sectionTest.passPercent}% to pass
                  </div>
                </DayTile>
              )}
            </LockedGrid>
          </section>
        );
      })}

      {finalTest && (
        <section style={{ marginBottom: "2rem" }}>
          <h2>Book 1 final test</h2>
          <p style={{ color: "var(--color-muted)" }}>{finalTest.intro}</p>
          <LockedGrid>
            <DayTile
              as={Link}
              to="/test/final"
              $open
              $done={isAssessmentPassed(finalTest.id, finalTest.passPercent)}
            >
              <div className="daynum">
                Final test
                {isAssessmentPassed(finalTest.id, finalTest.passPercent)
                  ? " · passed"
                  : typeof progress.assessmentScores?.[finalTest.id] ===
                      "number"
                    ? ` · ${progress.assessmentScores[finalTest.id]}%`
                    : ""}
              </div>
              <div className="title">{finalTest.title}</div>
              <div className="theme">
                Lessons 1–30 · {finalTest.questions.length} questions ·{" "}
                {finalTest.passPercent}% to pass
              </div>
            </DayTile>
          </LockedGrid>
        </section>
      )}
    </LessonPage>
  );
};

export default Learn;
