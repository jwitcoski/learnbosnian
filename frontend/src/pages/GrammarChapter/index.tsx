import { Redirect, useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import {
  getGrammarChapter,
  canViewGrammarChapter,
} from "../../data/loadGrammar";
import GrammarShell from "../../components/grammar/GrammarShell";
import { LessonPage, Banner } from "../../components/lesson/styles";

const GrammarChapterPage = () => {
  const { n } = useParams<{ n: string }>();
  const chapterNum = Number.parseInt(n, 10);
  const chapter = getGrammarChapter(chapterNum);

  if (!chapter || Number.isNaN(chapterNum)) {
    return <Redirect to="/learn/grammar" />;
  }

  if (!canViewGrammarChapter(chapter)) {
    return (
      <LessonPage>
        <Banner>
          Chapter {chapter.chapter} (<strong>{chapter.title}</strong>) is not
          live yet.
        </Banner>
        <p>{chapter.theme}</p>
        <Link to="/learn/grammar">← Back to Grammar</Link>
      </LessonPage>
    );
  }

  return <GrammarShell key={chapter.chapter} chapter={chapter} />;
};

export default GrammarChapterPage;
