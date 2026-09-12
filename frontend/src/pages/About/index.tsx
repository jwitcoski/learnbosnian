import { Link } from "react-router-dom";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";

const About = () => {
  return (
    <LessonPage>
      <h1>About</h1>
      <p>
        How to Speak Bosnian is an independent site for learning Bosnian in
        Latin script. It is for people who are visiting Bosnia and Herzegovina,
        moving there, marrying in, or reclaiming a family language. The named
        language on these pages is Bosnian, not a vague mix of the region.
      </p>

      <SectionDivider />

      <h2>What you can study here</h2>
      <p>
        Book 1 is a full A1 course: Lesson 0 plus thirty present-tense survival
        lessons. You walk through cafés, streets, buses, and homes with Ana,
        Emir, Amira, and a cat named Mrvica. Each section ends with a test, and
        Book 1 ends with a final test. A dictionary collects the words as you
        go.
      </p>
      <p>
        Grammar sits beside Book 1 as a notebook for endings, gender, cases,
        and how a sentence actually runs. Companion videos live on{" "}
        <a
          href="https://www.youtube.com/@HowtospeakBosnian"
          target="_blank"
          rel="noreferrer"
        >
          YouTube
        </a>
        .
      </p>

      <h2>How the course is built</h2>
      <p>
        Lessons are story-led and stay in the present tense in Book 1. Deeper
        past-tense work waits for later books. Print and video versions share
        the same lesson files as the website.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about the books, classroom use, or how to start:{" "}
        <a href="mailto:info@howtospeakbosnian.com">
          info@howtospeakbosnian.com
        </a>
        .
      </p>
      <p>
        <Link to="/learn/book/1">Open Book 1</Link>
        {" · "}
        <Link to="/privacy">Privacy policy</Link>
        {" · "}
        <Link to="/attributions">Photo credits</Link>
      </p>
    </LessonPage>
  );
};

export default About;
