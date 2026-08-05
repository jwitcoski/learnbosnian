import styled, { keyframes } from "styled-components";

const fadeUp = keyframes`
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
`;

const drift = keyframes`
  0% { transform: scale(1.05) translate(0, 0); }
  50% { transform: scale(1.1) translate(-1.5%, -1%); }
  100% { transform: scale(1.05) translate(0, 0); }
`;

export const HomeRoot = styled.div`
  width: 100%;
`;

export const Hero = styled.section`
  position: relative;
  min-height: min(92vh, 760px);
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  background: linear-gradient(135deg, var(--color-brown), var(--color-crimson));

  .hero-media {
    position: absolute;
    inset: 0;
    z-index: 0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      animation: ${drift} 22s ease-in-out infinite;
    }
  }

  .hero-shade {
    position: absolute;
    inset: 0;
    z-index: 1;
    background:
      linear-gradient(180deg, rgba(44, 24, 16, 0.25) 0%, rgba(44, 24, 16, 0.78) 70%),
      linear-gradient(90deg, rgba(93, 64, 55, 0.45), transparent 55%);
  }

  .hero-inner {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 3.5rem 1.5rem 3rem;
    color: #fff;
    animation: ${fadeUp} 0.9s ease both;
  }

  .brand {
    font-family: var(--font-display);
    font-size: clamp(2.6rem, 7vw, 4.5rem);
    font-weight: 700;
    line-height: 1.05;
    margin: 0 0 0.75rem;
    color: #fff;
    letter-spacing: -0.02em;
  }

  .lede {
    max-width: 34rem;
    font-size: clamp(1.05rem, 2.2vw, 1.25rem);
    line-height: 1.5;
    margin: 0 0 1.5rem;
    color: rgba(255, 248, 240, 0.95);
  }

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .credit {
    margin-top: 1.25rem;
    font-size: 0.75rem;
    opacity: 0.8;
  }
`;

export const Cta = styled.button<{ $ghost?: boolean }>`
  appearance: none;
  border: 2px solid ${(p) => (p.$ghost ? "rgba(255,248,240,0.85)" : "var(--color-crimson)")};
  background: ${(p) => (p.$ghost ? "transparent" : "var(--color-crimson)")};
  color: #fff;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 1rem;
  padding: 0.85rem 1.35rem;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease, border-color 0.2s ease;

  &:hover {
    background: ${(p) => (p.$ghost ? "rgba(255,248,240,0.12)" : "var(--color-brown)")};
    border-color: ${(p) => (p.$ghost ? "#fff" : "var(--color-brown)")};
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

export const Split = styled.section`
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 0;
  max-width: 1100px;
  margin: 0 auto 2rem;
  align-items: stretch;

  @media (max-width: 860px) {
    grid-template-columns: 1fr;
  }

  .photo {
    position: relative;
    min-height: 320px;
    overflow: hidden;
    background: var(--color-brown);

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .credit {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      padding: 0.5rem 0.75rem;
      font-size: 0.7rem;
      color: rgba(255, 248, 240, 0.9);
      background: linear-gradient(transparent, rgba(44, 24, 16, 0.85));
    }
  }

  .copy {
    background: rgba(255, 255, 255, 0.55);
    border-left: 6px solid var(--color-sage);
    padding: 2.25rem 1.75rem;
    display: flex;
    flex-direction: column;
    justify-content: center;

    @media (max-width: 860px) {
      border-left: none;
      border-top: 6px solid var(--color-sage);
    }

    h2 {
      margin-top: 0;
    }

    p {
      color: var(--color-text);
      margin: 0 0 1.25rem;
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
