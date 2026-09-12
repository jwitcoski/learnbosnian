import { Link } from "react-router-dom";
import { book1Outline } from "../../data/loadChapters";
import { grammarOutline } from "../../data/loadGrammar";
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
        Book 1 is the walk through town in the present tense. Grammar is the
        notebook beside it. Dictionary and YouTube sit in the header when you
        want a word or a video.
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
            {grammarOutline.level}. Cases, then verbs, then how a sentence
            actually runs.
          </div>
        </DayTile>
      </LockedGrid>
    </LessonPage>
  );
};

export default Learn;
