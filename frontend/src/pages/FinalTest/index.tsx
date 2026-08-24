import { Link, Redirect } from "react-router-dom";
import {
  canViewAssessments,
  getFinalTest,
} from "../../data/loadAssessments";
import AssessmentQuiz from "../../components/lesson/AssessmentQuiz";
import { LessonPage, Banner } from "../../components/lesson/styles";

const FinalTestPage = () => {
  const assessment = getFinalTest();

  if (!assessment) {
    return <Redirect to="/learn/book/1" />;
  }

  if (!canViewAssessments()) {
    return (
      <LessonPage>
        <Banner>The final test is not public yet.</Banner>
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

export default FinalTestPage;
