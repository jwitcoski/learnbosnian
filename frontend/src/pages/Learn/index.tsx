import { Link } from "react-router-dom";
import { book1Outline } from "../../data/loadChapters";
import { grammarOutline } from "../../data/loadGrammar";
import book2Outline from "../../data/book2/outline.json";
import book3Outline from "../../data/book3/outline.json";
import {
  DayTile,
  LessonPage,
  LockedGrid,
  SectionDivider,
} from "../../components/lesson/styles";

const Learn = () => {
  return (
    <LessonPage>
      <h1>Learn</h1>
      <p>
        Pick a book. Book 1 is the walk through town. Grammar is the notebook
        beside it. Website lessons, print, and YouTube companions for Book 1 as
        lessons are published.
      </p>
      <p>
        <Link to="/dictionary">Dictionary</Link>
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

      <LockedGrid>
        <DayTile as={Link} to="/learn/book/1" $open $done={false}>
          <div className="daynum">Book 1</div>
          <div className="title">{book1Outline.title}</div>
          <div className="theme">
            Level {book1Outline.level}. Lesson 0 plus thirty present-tense
            lessons. Cast: {book1Outline.cast?.join(", ")}.
          </div>
        </DayTile>
        <DayTile as={Link} to="/learn/grammar" $open $done={false}>
          <div className="daynum">Grammar</div>
          <div className="title">{grammarOutline.title}</div>
          <div className="theme">
            {grammarOutline.level}. Chapters 0 and 1 are up for a look. Cases,
            then verbs, then how a sentence actually runs.
          </div>
        </DayTile>
        <DayTile as="div" $open={false} $done={false}>
          <div className="daynum">Book 2 · soon</div>
          <div className="title">{book2Outline.title}</div>
          <div className="theme">Not started</div>
        </DayTile>
        <DayTile as="div" $open={false} $done={false}>
          <div className="daynum">Book 3 · soon</div>
          <div className="title">{book3Outline.title}</div>
          <div className="theme">Not started</div>
        </DayTile>
      </LockedGrid>
    </LessonPage>
  );
};

export default Learn;
