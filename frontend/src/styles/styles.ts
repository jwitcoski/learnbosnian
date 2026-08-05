import { createGlobalStyle } from "styled-components";
import { colors, fonts } from "./theme";

export const Styles = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap');

  :root {
    --color-crimson: ${colors.crimson};
    --color-brown: ${colors.brown};
    --color-sage: ${colors.sage};
    --color-navy: ${colors.navy};
    --color-beige: ${colors.beige};
    --color-lavender: ${colors.lavender};
    --color-cream: ${colors.cream};
    --color-gold: ${colors.gold};
    --color-text: ${colors.text};
    --color-muted: ${colors.muted};
    --font-display: ${fonts.display};
    --font-body: ${fonts.body};
  }

  *, *::before, *::after { box-sizing: border-box; }

  body, html, a {
    font-family: var(--font-body);
  }

  body {
    margin: 0;
    padding: 0;
    border: 0;
    outline: 0;
    background:
      radial-gradient(ellipse at top, rgba(132, 146, 116, 0.18), transparent 55%),
      linear-gradient(180deg, ${colors.cream} 0%, ${colors.beige} 45%, ${colors.lavender} 100%);
    color: var(--color-text);
    overflow-x: hidden;
    min-height: 100vh;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display);
    color: var(--color-brown);
    line-height: 1.2;
    margin: 0 0 0.6rem;
  }

  h1 { font-size: clamp(2rem, 4vw, 3.25rem); font-weight: 700; }
  h2 { font-size: clamp(1.5rem, 3vw, 2.25rem); font-weight: 700; }
  h3 { font-size: clamp(1.2rem, 2vw, 1.5rem); font-weight: 600; }

  p {
    color: var(--color-text);
    font-size: 1.125rem;
    line-height: 1.55;
  }

  a {
    text-decoration: none;
    color: var(--color-crimson);
    transition: color 0.2s ease;
    :hover { color: var(--color-brown); }
  }

  button {
    font-family: var(--font-body);
  }

  input, textarea {
    border-radius: 4px;
    border: 0;
    background: rgb(241, 242, 243);
    transition: all 0.3s ease-in-out;
    outline: none;
    width: 100%;
    padding: 1rem 1.25rem;
    :focus-within {
      background: none;
      box-shadow: ${colors.crimson} 0px 0px 0px 1px;
    }
  }

  *:focus { outline: none; }

  .ant-drawer-body {
    display: flex;
    flex-direction: column;
    text-align: left;
    padding-top: 1.5rem;
  }

  .ant-drawer-content-wrapper {
    width: 300px !important;
  }
`;
