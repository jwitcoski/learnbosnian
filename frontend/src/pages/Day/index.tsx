import { Redirect, useParams } from "react-router-dom";
import { getChapter, canViewChapter } from "../../data/loadChapters";
import LessonShell from "../../components/lesson/LessonShell";
import { LessonPage, Banner } from "../../components/lesson/styles";
import { Link } from "react-router-dom";

const DayPage = () => {
  const { n } = useParams<{ n: string }>();
  const day = Number.parseInt(n, 10);
  const chapter = getChapter(day);

  if (!chapter || Number.isNaN(day)) {
    return <Redirect to="/learn" />;
  }

  if (!canViewChapter(chapter)) {
    return (
      <LessonPage>
        <Banner>
          Day {chapter.day} — <strong>{chapter.title}</strong> is scheduled for Night{" "}
          {chapter.day}. Status: {chapter.status}.
        </Banner>
        <p>{chapter.theme}</p>
        <p>{chapter.storyBeat}</p>
        <Link to="/learn">← Back to curriculum</Link>
      </LessonPage>
    );
  }

  return <LessonShell key={chapter.day} chapter={chapter} />;
};

export default DayPage;
