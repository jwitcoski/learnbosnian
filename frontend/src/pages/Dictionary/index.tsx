import { useMemo, useState, type CSSProperties } from "react";
import { Link } from "react-router-dom";
import { buildDictionary } from "../../data/loadChapters";
import type { DictionaryEntry } from "../../types/chapter";
import { DictRow, LessonPage, SectionDivider } from "../../components/lesson/styles";
import { useClipAudio } from "../../hooks/useClipAudio";
import { vocabClipId } from "../../lib/audioClips";

type SortMode = "bosnian" | "english" | "lesson";

const SORTS: { id: SortMode; label: string }[] = [
  { id: "bosnian", label: "Bosnian" },
  { id: "english", label: "English" },
  { id: "lesson", label: "Lesson" },
];

const BOOKS: { id: number; label: string; ready: boolean }[] = [
  { id: 1, label: "Book 1", ready: true },
  { id: 2, label: "Book 2 · soon", ready: false },
  { id: 3, label: "Book 3 · soon", ready: false },
];

function compareBosnian(a: DictionaryEntry, b: DictionaryEntry) {
  return a.bosnian.localeCompare(b.bosnian, "bs", { sensitivity: "base" });
}

function sortEntries(entries: DictionaryEntry[], sort: SortMode) {
  const list = [...entries];
  if (sort === "english") {
    list.sort(
      (a, b) =>
        a.english.localeCompare(b.english, "en", { sensitivity: "base" }) ||
        compareBosnian(a, b)
    );
  } else if (sort === "lesson") {
    list.sort((a, b) => (a.day ?? 0) - (b.day ?? 0) || compareBosnian(a, b));
  } else {
    list.sort(compareBosnian);
  }
  return list;
}

const chipStyle = (active: boolean, disabled?: boolean): CSSProperties => ({
  background: active ? "var(--color-crimson)" : "transparent",
  color: active ? "#fff" : "var(--color-brown)",
  border: "2px solid var(--color-crimson)",
  padding: "0.35rem 0.75rem",
  fontWeight: 700,
  cursor: disabled ? "default" : "pointer",
  font: "inherit",
  fontSize: "0.9rem",
  opacity: disabled ? 0.55 : 1,
});

const Dictionary = () => {
  const entries = useMemo(() => buildDictionary(true), []);
  const [q, setQ] = useState("");
  const [sort, setSort] = useState<SortMode>("bosnian");
  const [book, setBook] = useState(1);
  const { playClip, playingId, missing } = useClipAudio();

  const visible = useMemo(() => {
    const needle = q.trim().toLowerCase();
    const byBook = entries.filter((e) => (e.book ?? 1) === book);
    const filtered = needle
      ? byBook.filter((e) =>
          `${e.bosnian} ${e.english}`.toLowerCase().includes(needle)
        )
      : byBook;
    return sortEntries(filtered, sort);
  }, [entries, q, sort, book]);

  return (
    <LessonPage>
      <h1>Dictionary</h1>
      <p>
        Words from lessons you can open now. Tap a word to hear it. Pick a book
        to see its list. Latin script only.
      </p>
      <p>
        <Link to={`/learn/book/${book}`}>← Book {book} curriculum</Link>
      </p>
      <SectionDivider />
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search Bosnian or English…"
        style={{ marginBottom: "1rem" }}
      />
      <div
        role="group"
        aria-label="Dictionary book"
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "0.45rem",
          marginBottom: "0.85rem",
        }}
      >
        <span style={{ color: "var(--color-muted)", marginRight: "0.25rem" }}>
          Book
        </span>
        {BOOKS.map((opt) => {
          const active = book === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              aria-pressed={active}
              disabled={!opt.ready}
              onClick={() => {
                if (opt.ready) setBook(opt.id);
              }}
              style={chipStyle(active, !opt.ready)}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
      <div
        role="group"
        aria-label="Sort dictionary"
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "0.45rem",
          marginBottom: "0.85rem",
        }}
      >
        <span style={{ color: "var(--color-muted)", marginRight: "0.25rem" }}>
          Sort by
        </span>
        {SORTS.map((opt) => {
          const active = sort === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              aria-pressed={active}
              onClick={() => setSort(opt.id)}
              style={chipStyle(active)}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
      <p style={{ color: "var(--color-muted)" }}>{visible.length} entries</p>
      <div>
        {visible.map((e) => {
          const day = e.day ?? 0;
          const entryBook = e.book ?? 1;
          const clipId = vocabClipId(entryBook, day, e.bosnian);
          const isPlaying = playingId === clipId;
          const isMissing = Boolean(missing[clipId]);
          return (
            <DictRow
              key={`${entryBook}-${e.bosnian}-${day}`}
              type="button"
              onClick={() => {
                if (!isMissing) playClip(clipId);
              }}
              data-playing={isPlaying ? "true" : "false"}
              data-missing={isMissing ? "true" : "false"}
              aria-label={`Play pronunciation for ${e.bosnian}`}
            >
              <strong>{e.bosnian}</strong>
              <span>{e.english}</span>
              <span style={{ color: "var(--color-muted)", fontSize: "0.85rem" }}>
                Lesson {day}
              </span>
              <span className="listen">
                {isPlaying ? "Playing…" : isMissing ? "Audio soon" : "Tap to hear"}
              </span>
            </DictRow>
          );
        })}
      </div>
    </LessonPage>
  );
};

export default Dictionary;
