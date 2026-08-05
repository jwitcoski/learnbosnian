import styled from "styled-components";

export const AttrIntro = styled.p`
  font-size: 1.1rem;
  line-height: 1.55;
  color: var(--color-text);
  max-width: 40rem;
`;

export const AttrMeta = styled.p`
  margin: 0 0 1.5rem;
  font-size: 0.95rem;
  color: var(--color-muted);
`;

export const CiteBox = styled.aside`
  border-top: 4px solid var(--color-crimson);
  padding-top: 0.85rem;
  margin-bottom: 1.5rem;

  h2 {
    margin: 0 0 0.5rem;
    font-family: var(--font-display);
    font-size: 1.35rem;
    color: var(--color-brown);
  }

  p {
    margin: 0 0 0.65rem;
    color: var(--color-text);
    line-height: 1.5;
  }

  code {
    font-size: 0.9em;
  }
`;

export const AttrList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
`;

export const AttrCard = styled.article`
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(93, 64, 55, 0.15);
`;

export const AttrTitle = styled.h2`
  margin: 0 0 0.4rem;
  font-family: var(--font-display);
  font-size: 1.35rem;
  color: var(--color-brown);
`;

export const AttrWhere = styled.ul`
  margin: 0 0 0.75rem;
  padding-left: 1.1rem;
  color: var(--color-muted);
  font-size: 0.95rem;

  li {
    margin-bottom: 0.2rem;
  }
`;

export const AttrDl = styled.dl`
  display: grid;
  grid-template-columns: 7.5rem 1fr;
  gap: 0.35rem 0.75rem;
  margin: 0 0 0.75rem;
  font-size: 0.98rem;

  dt {
    margin: 0;
    color: var(--color-muted);
    font-weight: 600;
  }

  dd {
    margin: 0;
    color: var(--color-text);
  }

  code {
    font-size: 0.88em;
    word-break: break-all;
  }

  @media (max-width: 560px) {
    grid-template-columns: 1fr;
    gap: 0.15rem;

    dt {
      margin-top: 0.45rem;
    }
  }
`;

export const AttrLink = styled.a`
  display: inline-block;
  font-weight: 700;
  color: var(--color-crimson);
  text-decoration: none;

  &:hover {
    text-decoration: underline;
    color: var(--color-brown);
  }
`;

export const AttrNotes = styled.p`
  margin: 0.65rem 0 0;
  font-size: 0.92rem;
  color: var(--color-muted);
  line-height: 1.45;
`;
