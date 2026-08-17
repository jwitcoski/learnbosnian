import { Link } from "react-router-dom";
import book2 from "../../data/book2/outline.json";
import book3 from "../../data/book3/outline.json";
import { book1Outline } from "../../data/loadChapters";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";

const Books = () => {
  return (
    <LessonPage>
      <h1>The book series</h1>
      <p>
        Book 1 is live and growing. Books 2 and 3 are future plans: from first
        greetings toward fuller conversation, with website lessons, print
        (Scribus), and YouTube companions.
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
        <h2>{book2.title}</h2>
        <p>{book2.summary}</p>
        <ul>
          {book2.themes.map((t: string) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
        <p style={{ color: "var(--color-muted)" }}>{book2.note}</p>
      </section>

      <section>
        <h2>{book3.title}</h2>
        <p>{book3.summary}</p>
        <ul>
          {book3.themes.map((t: string) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
        <p style={{ color: "var(--color-muted)" }}>{book3.note}</p>
      </section>
    </LessonPage>
  );
};

export default Books;
