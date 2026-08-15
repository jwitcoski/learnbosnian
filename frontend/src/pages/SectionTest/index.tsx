import { Link, Redirect, useParams } from "react-router-dom";
import { getSectionTest } from "../../data/loadAssessments";
import AssessmentQuiz from "../../components/lesson/AssessmentQuiz";
import { LessonPage } from "../../components/lesson/styles";

const SectionTestPage = () => {
  const { n } = useParams<{ n: string }>();
  const section = Number.parseInt(n, 10);
  const assessment = getSectionTest(section);

  if (!assessment || Number.isNaN(section)) {
    return <Redirect to="/learn" />;
  }

  return (
    <LessonPage>
      <p>
        <Link to="/learn">← Curriculum</Link>
      </p>
      <h1>{assessment.titleEn || assessment.title}</h1>
      <AssessmentQuiz assessment={assessment} />
    </LessonPage>
  );
};

export default SectionTestPage;
