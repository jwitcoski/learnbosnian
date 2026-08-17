import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { buildDictionary } from "../../data/loadChapters";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";

const Dictionary = () => {
  const entries = useMemo(() => buildDictionary(true), []);
  const [q, setQ] = useState("");

  const filtered = entries.filter((e) => {
    const hay = `${e.bosnian} ${e.english}`.toLowerCase();
    return hay.includes(q.trim().toLowerCase());
  });

  return (
    <LessonPage>
      <h1>Dictionary</h1>
      <p>
        Words from lessons you can open now. The list grows as Book 1 lessons are
        reviewed and published. Latin script only.
      </p>
      <p>
        <Link to="/learn">← Curriculum</Link>
      </p>
      <SectionDivider />
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search Bosnian or English…"
        style={{ marginBottom: "1rem" }}
      />
      <p style={{ color: "var(--color-muted)" }}>{filtered.length} entries</p>
      <div>
        {filtered.map((e) => (
          <div
            key={`${e.bosnian}-${e.day}`}
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr auto",
              gap: "0.5rem",
              padding: "0.55rem 0",
              borderBottom: "1px solid rgba(93,64,55,0.15)",
            }}
          >
            <strong>{e.bosnian}</strong>
            <span>{e.english}</span>
            <span style={{ color: "var(--color-muted)", fontSize: "0.85rem" }}>
              Lesson {e.day}
            </span>
          </div>
        ))}
      </div>
    </LessonPage>
  );
};

export default Dictionary;
