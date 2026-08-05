import styled, { keyframes } from "styled-components";

const fadeUp = keyframes`
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
`;

export const HomeRoot = styled.div`
  width: 100%;
`;

/** Cream panel for flat polygon illustrations (transparent PNGs) */
export const StyledPhoto = styled.figure`
  margin: 0;
  position: relative;
  background: transparent;
  padding: 0.5rem 0.5rem 1.5rem;

  img {
    position: relative;
    z-index: 0;
    display: block;
    width: 100%;
    height: auto;
    max-height: 440px;
    object-fit: contain;
    margin: 0 auto;
  }

  .credit {
    display: block;
    margin-top: 0.55rem;
    font-size: 0.72rem;
    color: var(--color-muted);
    line-height: 1.35;
  }
`;

export const Hero = styled.section`
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 2rem;
  align-items: center;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 2rem;
  min-height: min(88vh, 720px);
  animation: ${fadeUp} 0.85s ease both;

  @media (max-width: 860px) {
    grid-template-columns: 1fr;
    min-height: auto;
    padding-top: 1.75rem;

    ${StyledPhoto} {
      order: -1;
    }
  }

  .hero-copy {
    color: var(--color-text);
  }

  .brand {
    font-family: var(--font-display);
    font-size: clamp(2.6rem, 7vw, 4.5rem);
    font-weight: 700;
    line-height: 1.05;
    margin: 0 0 0.75rem;
    color: var(--color-brown);
    letter-spacing: -0.02em;
  }

  .lede {
    max-width: 34rem;
    font-size: clamp(1.05rem, 2.2vw, 1.25rem);
    line-height: 1.5;
    margin: 0 0 1.5rem;
    color: var(--color-muted);
  }

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }
`;

export const Cta = styled.button<{ $ghost?: boolean }>`
  appearance: none;
  border: 2px solid ${(p) => (p.$ghost ? "var(--color-brown)" : "var(--color-crimson)")};
  background: ${(p) => (p.$ghost ? "transparent" : "var(--color-crimson)")};
  color: ${(p) => (p.$ghost ? "var(--color-brown)" : "#fff")};
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 1rem;
  padding: 0.85rem 1.35rem;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease, color 0.2s ease;

  &:hover {
    background: var(--color-brown);
    border-color: var(--color-brown);
    color: #fff;
    transform: translateY(-1px);
  }
`;

export const KilimBand = styled.div`
  height: 16px;
  background: repeating-linear-gradient(
    90deg,
    var(--color-crimson) 0 12px,
    var(--color-beige) 12px 18px,
    var(--color-navy) 18px 30px,
    var(--color-sage) 30px 42px,
    var(--color-brown) 42px 54px,
    var(--color-gold) 54px 66px
  );
`;

export const Section = styled.section`
  max-width: 980px;
  margin: 0 auto;
  padding: 3.5rem 1.5rem;

  h2 {
    font-family: var(--font-display);
    color: var(--color-brown);
    font-size: clamp(1.75rem, 3.5vw, 2.4rem);
    margin-bottom: 0.75rem;
  }

  p.support {
    color: var(--color-muted);
    max-width: 40rem;
    margin: 0 0 1.5rem;
    font-size: 1.125rem;
  }
`;

export const Pillars = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  article {
    border-top: 4px solid var(--color-crimson);
    padding-top: 0.85rem;
  }

  .label {
    font-family: var(--font-display);
    font-weight: 700;
    color: var(--color-crimson);
    font-size: 1.15rem;
    margin-bottom: 0.35rem;
  }

  p {
    margin: 0;
    color: var(--color-text);
    font-size: 1.05rem;
  }
`;

export const Illustrate = styled.section<{ $flip?: boolean }>`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
  align-items: center;

  @media (max-width: 860px) {
    grid-template-columns: 1fr;
    padding: 2.25rem 1.5rem;
  }

  .copy {
    order: ${(p) => (p.$flip ? 2 : 1)};

    @media (max-width: 860px) {
      order: 2;
    }

    h2 {
      margin-top: 0;
      font-family: var(--font-display);
      color: var(--color-brown);
    }

    p {
      color: var(--color-text);
      margin: 0 0 1.25rem;
      font-size: 1.125rem;
      line-height: 1.55;
    }
  }

  ${StyledPhoto} {
    order: ${(p) => (p.$flip ? 1 : 2)};

    @media (max-width: 860px) {
      order: 1;
    }
  }
`;

export const SolidCta = styled.button`
  appearance: none;
  align-self: flex-start;
  border: 2px solid var(--color-crimson);
  background: var(--color-crimson);
  color: #fff;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 1rem;
  padding: 0.75rem 1.2rem;
  cursor: pointer;

  &:hover {
    background: var(--color-brown);
    border-color: var(--color-brown);
  }
`;

export const YoutubeStrip = styled.section`
  max-width: 980px;
  margin: 0 auto 3rem;
  padding: 1.75rem 1.5rem;
  display: flex;
  gap: 1.25rem;
  align-items: center;
  border-top: 1px solid rgba(93, 64, 55, 0.2);
  border-bottom: 1px solid rgba(93, 64, 55, 0.2);

  @media (max-width: 640px) {
    flex-direction: column;
    text-align: center;
  }

  img {
    width: 56px;
    height: 56px;
    flex-shrink: 0;
  }

  h2 {
    font-size: 1.5rem;
    margin: 0 0 0.35rem;
  }

  p {
    margin: 0 0 0.75rem;
    color: var(--color-muted);
    font-size: 1.05rem;
  }
`;

export const ContactWrap = styled.div`
  max-width: 720px;
  margin: 0 auto;
  padding: 0 1.5rem 4rem;
`;
