import styled from "styled-components";
import { Link } from "react-router-dom";

export const SectionDivider = styled.div`
  height: 18px;
  margin: 2rem 0;
  background: repeating-linear-gradient(
    90deg,
    var(--color-crimson) 0 12px,
    var(--color-beige) 12px 18px,
    var(--color-navy) 18px 30px,
    var(--color-sage) 30px 42px,
    var(--color-brown) 42px 54px,
    var(--color-gold) 54px 66px
  );
  clip-path: polygon(
    0 50%, 2% 0, 4% 50%, 6% 100%, 8% 50%, 10% 0, 12% 50%, 14% 100%,
    16% 50%, 18% 0, 20% 50%, 22% 100%, 24% 50%, 26% 0, 28% 50%, 30% 100%,
    32% 50%, 34% 0, 36% 50%, 38% 100%, 40% 50%, 42% 0, 44% 50%, 46% 100%,
    48% 50%, 50% 0, 52% 50%, 54% 100%, 56% 50%, 58% 0, 60% 50%, 62% 100%,
    64% 50%, 66% 0, 68% 50%, 70% 100%, 72% 50%, 74% 0, 76% 50%, 78% 100%,
    80% 50%, 82% 0, 84% 50%, 86% 100%, 88% 50%, 90% 0, 92% 50%, 94% 100%,
    96% 50%, 98% 0, 100% 50%, 100% 100%, 0 100%
  );
  opacity: 0.9;
`;

export const LessonPage = styled.main`
  max-width: 820px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 4rem;
`;

export const HeroBand = styled.header`
  margin-bottom: 0.35rem;
  border: 1px solid rgba(93, 64, 55, 0.12);
  background: #f7f1e8;
  overflow: hidden;

  .hero-media {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #efe6d8;
    overflow: hidden;

    img {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
    }
  }

  .hero-copy {
    padding: 1.15rem 1.25rem 1.25rem;
    background: var(--color-brown);
    color: #fff;

    h1 {
      color: #fff;
      margin: 0 0 0.35rem;
    }

    .meta {
      margin: 0;
      font-size: 1rem;
      opacity: 0.92;
      color: #f5ebe0;
    }

    .meta + .meta {
      margin-top: 0.25rem;
    }
  }
`;

export const Credit = styled.p`
  font-size: 0.8rem !important;
  color: var(--color-muted) !important;
  margin: 0.35rem 0 0;

  a {
    color: inherit;
    text-decoration: none;

    &:hover {
      color: var(--color-crimson);
      text-decoration: underline;
    }
  }

  .ref {
    font-weight: 700;
    color: var(--color-crimson);
    margin-right: 0.4rem;
  }
`;

export const LessonFigure = styled.figure`
  margin: 1.25rem 0 1.5rem;
  padding: 0;

  .frame {
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: #efe6d8;
    border: 1px solid rgba(93, 64, 55, 0.12);
  }

  img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }
`;

export const Panel = styled.section`
  padding: 1.25rem 0;
`;

export const VocabGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.75rem;
`;

export const VocabCard = styled.button`
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.85rem 1rem;
  background: rgba(255, 255, 255, 0.55);
  border: none;
  border-left: 4px solid var(--color-crimson);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  font: inherit;
  color: inherit;

  &:hover {
    transform: translateY(-2px);
  }

  &:focus-visible {
    outline: 2px solid var(--color-crimson);
    outline-offset: 2px;
  }

  &[data-playing="true"] {
    box-shadow: inset 0 0 0 1px var(--color-crimson);
  }

  &[data-missing="true"] {
    cursor: default;
    opacity: 0.85;
  }

  .bs {
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--color-brown);
  }
  .en {
    color: var(--color-muted);
  }
  .pron {
    font-size: 0.85rem;
    color: var(--color-sage);
  }
  .listen {
    margin-top: 0.35rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-crimson);
  }
`;

export const DictRow = styled.button`
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 0.5rem;
  align-items: baseline;
  width: 100%;
  text-align: left;
  padding: 0.55rem 0.35rem;
  margin: 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(93, 64, 55, 0.15);
  cursor: pointer;
  font: inherit;
  color: inherit;

  &:hover:not([data-missing="true"]) {
    background: rgba(196, 30, 58, 0.06);
  }

  &:focus-visible {
    outline: 2px solid var(--color-crimson);
    outline-offset: 2px;
  }

  &[data-playing="true"] {
    background: rgba(196, 30, 58, 0.1);
  }

  &[data-missing="true"] {
    cursor: default;
    opacity: 0.85;
  }

  .listen {
    grid-column: 1 / -1;
    margin-top: -0.15rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-crimson);
  }
`;

export const Dialogue = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

export const Line = styled.div<{ $speaker: string }>`
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.75rem 1rem;
  background: ${(p) =>
    p.$speaker === "Ana"
      ? "rgba(198, 40, 40, 0.08)"
      : p.$speaker === "Emir"
      ? "rgba(26, 35, 126, 0.08)"
      : p.$speaker === "Amira"
      ? "rgba(132, 146, 116, 0.18)"
      : "rgba(93, 64, 55, 0.08)"};
  border: none;
  border-left: 3px solid var(--color-brown);
  color: inherit;
  transition: box-shadow 0.2s ease;

  &[data-playing="true"] {
    box-shadow: inset 0 0 0 1px var(--color-crimson);
  }

  button.play {
    display: block;
    width: 100%;
    margin: 0;
    padding: 0;
    border: none;
    background: transparent;
    text-align: left;
    font: inherit;
    color: inherit;
    cursor: pointer;

    &:focus-visible {
      outline: 2px solid var(--color-crimson);
      outline-offset: 2px;
    }
  }

  .speaker {
    font-weight: 700;
    color: var(--color-crimson);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .bs {
    font-size: 1.15rem;
    font-weight: 600;
  }
  .en {
    color: var(--color-muted);
    font-size: 0.95rem;
  }
  .listen {
    margin-top: 0.3rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-crimson);
  }
`;

export const GoalList = styled.ul`
  padding-left: 1.2rem;
  li {
    margin-bottom: 0.35rem;
    font-size: 1.05rem;
  }
`;

export const ButtonRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
`;

export const PrimaryButton = styled.button`
  background: var(--color-crimson);
  color: white;
  border: none;
  padding: 0.75rem 1.25rem;
  font-weight: 700;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.15s ease, background 0.15s ease;

  &:hover {
    background: var(--color-brown);
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.55;
    cursor: not-allowed;
    transform: none;
  }
`;

export const GhostButton = styled.button`
  background: transparent;
  color: var(--color-brown);
  border: 2px solid var(--color-brown);
  padding: 0.65rem 1.15rem;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;

  &:hover {
    background: rgba(93, 64, 55, 0.08);
  }
`;

export const Banner = styled.div`
  background: rgba(212, 160, 23, 0.2);
  border-left: 4px solid var(--color-gold);
  padding: 0.85rem 1rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
`;

export const DayNav = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.85rem;
  margin-top: 0.5rem;

  .soon {
    color: var(--color-muted);
    font-size: 0.95rem;
  }
`;

export const DayNavLink = styled(Link)<{ $primary?: boolean }>`
  display: inline-block;
  padding: 0.75rem 1.15rem;
  font-weight: 700;
  text-decoration: none;
  border: 2px solid
    ${(p) => (p.$primary ? "var(--color-crimson)" : "var(--color-brown)")};
  background: ${(p) => (p.$primary ? "var(--color-crimson)" : "transparent")};
  color: ${(p) => (p.$primary ? "#fff" : "var(--color-brown)")};

  &:hover {
    background: var(--color-brown);
    border-color: var(--color-brown);
    color: #fff;
  }
`;

export const LockedGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.85rem;
`;

export const DayTile = styled.div<{ $open?: boolean; $done?: boolean }>`
  display: block;
  padding: 1rem;
  min-height: 120px;
  background: ${(p) =>
    p.$open ? "rgba(255,255,255,0.7)" : "rgba(92, 83, 70, 0.12)"};
  border-top: 4px solid
    ${(p) =>
      p.$done
        ? "var(--color-sage)"
        : p.$open
        ? "var(--color-crimson)"
        : "var(--color-muted)"};
  color: var(--color-text);
  opacity: ${(p) => (p.$open ? 1 : 0.72)};
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-decoration: none;

  &:hover {
    transform: ${(p) => (p.$open ? "translateY(-3px)" : "none")};
    box-shadow: ${(p) =>
      p.$open ? "0 8px 20px rgba(93,64,55,0.12)" : "none"};
    color: var(--color-text);
  }

  .daynum {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--color-crimson);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .title {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1.05rem;
    margin: 0.35rem 0;
  }
  .theme {
    font-size: 0.85rem;
    color: var(--color-muted);
  }
`;

export const NerdBox = styled.aside`
  margin: 0.5rem 0 1.25rem;
  padding: 1rem 1.15rem 1.1rem;
  background: rgba(212, 160, 23, 0.12);
  border-left: 4px solid var(--color-gold);

  h2 {
    margin-top: 0;
    font-size: 1.15rem;
  }

  p:last-child {
    margin-bottom: 0;
  }
`;

export const GrammarTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0 0.25rem;
  font-size: 0.98rem;

  th,
  td {
    text-align: left;
    padding: 0.55rem 0.7rem;
    border-bottom: 1px solid rgba(93, 64, 55, 0.15);
    vertical-align: top;
  }

  th {
    font-size: 0.8rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-muted);
    font-weight: 700;
  }

  td:first-child {
    font-weight: 700;
    color: var(--color-brown);
    white-space: nowrap;
  }
`;

export const ChoiceRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.35rem 0 0.5rem;
`;

export const ChoiceButton = styled.button<{
  $state?: "idle" | "correct" | "wrong" | "missed";
}>`
  background: ${(p) =>
    p.$state === "correct"
      ? "var(--color-sage)"
      : p.$state === "wrong"
      ? "var(--color-crimson)"
      : "transparent"};
  color: ${(p) =>
    p.$state === "correct" || p.$state === "wrong"
      ? "#fff"
      : "var(--color-brown)"};
  border: 2px solid
    ${(p) =>
      p.$state === "missed"
        ? "var(--color-sage)"
        : p.$state === "correct" || p.$state === "wrong"
        ? "transparent"
        : "var(--color-brown)"};
  padding: 0.45rem 0.85rem;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.95rem;
  font: inherit;

  &:hover {
    background: ${(p) =>
      p.$state === "idle" || !p.$state
        ? "rgba(93, 64, 55, 0.08)"
        : p.$state === "correct"
        ? "var(--color-sage)"
        : p.$state === "wrong"
        ? "var(--color-crimson)"
        : "transparent"};
  }
`;

export const GrammarCaption = styled.p`
  font-size: 1rem !important;
  font-weight: 600;
  color: var(--color-brown) !important;
  margin: 0.65rem 0 0.15rem;
`;

