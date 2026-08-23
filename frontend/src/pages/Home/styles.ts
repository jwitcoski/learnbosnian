import styled from "styled-components";

export const HomeRoot = styled.div`
  width: 100%;
`;

export const ShelfFrame = styled.section`
  position: relative;
  width: 100%;
  height: min(100dvh, 920px);
  min-height: 640px;
  background: #171a24;
  overflow: hidden;

  iframe {
    display: block;
    width: 100%;
    height: 100%;
    border: 0;
    background: #171a24;
  }

  @media (max-width: 700px) {
    height: min(100dvh, 780px);
    min-height: 560px;
  }
`;

export const ShelfCredit = styled.p`
  max-width: 720px;
  margin: 0 auto;
  padding: 1rem 1.5rem 0.25rem;
  font-size: 0.85rem;
  line-height: 1.45;
  color: var(--color-muted);
  text-align: center;

  a {
    color: var(--color-crimson);
  }
`;

export const KilimBand = styled.div`
  height: 16px;
  margin: 1.5rem 0 0;
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

export const ContactWrap = styled.div`
  max-width: 720px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
`;
