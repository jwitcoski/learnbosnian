import { Link, Redirect } from "react-router-dom";
import { getFinalTest } from "../../data/loadAssessments";
import AssessmentQuiz from "../../components/lesson/AssessmentQuiz";
import { LessonPage } from "../../components/lesson/styles";

const FinalTestPage = () => {
  const assessment = getFinalTest();

  if (!assessment) {
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

export default FinalTestPage;
