import { Link, Redirect, useParams } from "react-router-dom";
import { getChapter, canViewChapter } from "../../data/loadChapters";
import SectionQuiz from "../../components/lesson/SectionQuiz";
import { LessonPage, Banner } from "../../components/lesson/styles";

const QuizPage = () => {
  const { n } = useParams<{ n: string }>();
  const day = Number.parseInt(n, 10);
  const chapter = getChapter(day);

  if (!chapter || Number.isNaN(day)) {
    return <Redirect to="/learn" />;
  }

  if (!canViewChapter(chapter)) {
    return (
      <LessonPage>
        <Banner>This quiz opens when Lesson {day} is live.</Banner>
        <Link to="/learn">← Curriculum</Link>
      </LessonPage>
    );
  }

  return (
    <LessonPage>
      <p>
        <Link to={`/learn/lesson/${day}`}>← Lesson {day}</Link>
      </p>
      <h1>
        Lesson {day} quiz: {chapter.title}
      </h1>
      <SectionQuiz chapter={chapter} />
    </LessonPage>
  );
};

export default QuizPage;
