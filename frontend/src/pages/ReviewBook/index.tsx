import { Link } from "react-router-dom";
import { LessonPage, PrimaryButton } from "../../components/lesson/styles";

const PDF_SRC = "/reviewbook/book1-interior.pdf";

/**
 * Draft print PDF viewer — obscure URL for reviewers, not linked from main nav.
 */
const ReviewBook = () => {
  return (
    <LessonPage>
      <p>
        <Link to="/learn">← Learn</Link>
      </p>
      <h1>Book 1 — draft print preview</h1>
      <p style={{ color: "var(--color-muted)" }}>
        Full paperback interior (7×10 in) for review. Not the public curriculum —
        lesson pages on the site still follow normal publish rules.
      </p>
      <p style={{ marginBottom: "1rem" }}>
        <PrimaryButton as="a" href={PDF_SRC} target="_blank" rel="noreferrer">
          Open PDF in a new tab
        </PrimaryButton>
        {" · "}
        <a href={PDF_SRC} download="book1-interior-draft.pdf">
          Download
        </a>
      </p>
      <div
        style={{
          border: "1px solid var(--color-border, #c9b8a0)",
          borderRadius: 4,
          overflow: "hidden",
          background: "#2a2a2a",
          minHeight: "75vh",
        }}
      >
        <iframe
          title="Book 1 draft interior PDF"
          src={`${PDF_SRC}#view=FitH`}
          style={{
            width: "100%",
            height: "80vh",
            border: "none",
            display: "block",
          }}
        />
      </div>
    </LessonPage>
  );
};

export default ReviewBook;
