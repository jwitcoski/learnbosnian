import { Link, Redirect, useParams } from "react-router-dom";
import {
  canViewAssessments,
  getSectionTest,
} from "../../data/loadAssessments";
import AssessmentQuiz from "../../components/lesson/AssessmentQuiz";
import { LessonPage, Banner } from "../../components/lesson/styles";

const SectionTestPage = () => {
  const { n } = useParams<{ n: string }>();
  const section = Number.parseInt(n, 10);
  const assessment = getSectionTest(section);

  if (!assessment || Number.isNaN(section)) {
    return <Redirect to="/learn/book/1" />;
  }

  if (!canViewAssessments()) {
    return (
      <LessonPage>
        <Banner>Section tests are not public yet.</Banner>
        <p>
          <Link to="/learn/book/1">← Curriculum</Link>
        </p>
      </LessonPage>
    );
  }

  return (
    <LessonPage>
      <p>
        <Link to="/learn/book/1">← Curriculum</Link>
      </p>
      <h1>{assessment.titleEn || assessment.title}</h1>
      <AssessmentQuiz assessment={assessment} />
    </LessonPage>
  );
};

export default SectionTestPage;
