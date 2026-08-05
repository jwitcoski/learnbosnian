import styled, { keyframes } from "styled-components";
import { Link } from "react-router-dom";

const shimmer = keyframes`
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
`;

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
  position: relative;
  border-radius: 0;
  overflow: hidden;
  margin-bottom: 1.5rem;
  min-height: 280px;
  display: flex;
  align-items: flex-end;
  background: linear-gradient(135deg, var(--color-brown), var(--color-crimson));
  animation: ${shimmer} 12s linear infinite;
  background-size: 200% 200%;

  img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.55;
  }

  .hero-copy {
    position: relative;
    z-index: 1;
    padding: 1.75rem;
    color: white;
    text-shadow: 0 1px 8px rgba(0, 0, 0, 0.45);
    width: 100%;
    background: linear-gradient(transparent, rgba(44, 24, 16, 0.75));
  }

  h1 {
    color: white;
    margin-bottom: 0.25rem;
  }

  .meta {
    font-size: 1rem;
    opacity: 0.95;
  }
`;

export const Credit = styled.p`
  font-size: 0.8rem !important;
  color: var(--color-muted) !important;
  margin: 0.35rem 0 0;
`;

export const Panel = styled.section`
  padding: 1.25rem 0;
`;

export const VocabGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.75rem;
`;

export const VocabCard = styled.div`
  padding: 0.85rem 1rem;
  background: rgba(255, 255, 255, 0.55);
  border-left: 4px solid var(--color-crimson);
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-2px);
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
`;

export const Dialogue = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

export const Line = styled.div<{ $speaker: string }>`
  padding: 0.75rem 1rem;
  background: ${(p) =>
    p.$speaker === "Ana"
      ? "rgba(198, 40, 40, 0.08)"
      : p.$speaker === "Emir"
      ? "rgba(26, 35, 126, 0.08)"
      : p.$speaker === "Amira"
      ? "rgba(132, 146, 116, 0.18)"
      : "rgba(93, 64, 55, 0.08)"};
  border-left: 3px solid var(--color-brown);

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
