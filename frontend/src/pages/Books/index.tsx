import { Link } from "react-router-dom";
import { book1Outline } from "../../data/loadChapters";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";

const Books = () => {
  return (
    <LessonPage>
      <h1>The book series</h1>
      <p>
        Book 1 is live and growing. Website lessons, print (Scribus), and YouTube
        companions for each lesson as it is published.
      </p>

      <SectionDivider />

      <section style={{ marginBottom: "2rem" }}>
        <h2>Book 1: {book1Outline.title}</h2>
        <p>
          Level {book1Outline.level}. Thirty present-tense lessons (about an hour
          each) for travelers and new arrivals. Cast:{" "}
          {book1Outline.cast?.join(", ")}.
        </p>
        <p>
          <Link to="/learn">Start Book 1</Link>
        </p>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>Book 2</h2>
        <p style={{ color: "var(--color-muted)" }}>Not started</p>
      </section>

      <section>
        <h2>Book 3</h2>
        <p style={{ color: "var(--color-muted)" }}>Not started</p>
      </section>
    </LessonPage>
  );
};

export default Books;
