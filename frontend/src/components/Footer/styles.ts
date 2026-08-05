import styled from "styled-components";
import { Link } from "react-router-dom";

export const FooterSection = styled("footer")`
  background: #2c1810;
  padding: 2.5rem 0;
  color: #f5ebe0;
`;

export const Title = styled("h4")`
  font-size: 22px;
  text-transform: capitalize;
  color: #f5ebe0;
  font-family: var(--font-display);

  @media screen and (max-width: 414px) {
    padding: 1.5rem 0;
  }
`;

export const NavLink = styled(Link)`
  display: block;
  font-size: 1rem;
  margin-bottom: 0.625rem;
  transition: all 0.2s ease-in-out;
  color: #d4c4b0;

  &:hover,
  &:active,
  &:focus {
    color: var(--color-gold);
  }
`;

export const Extra = styled("section")`
  background: #1a120e;
  position: relative;
  width: 100%;
  margin-right: auto;
  margin-left: auto;
  padding-bottom: 2rem;
  border-top: 3px solid var(--color-crimson);
`;

export const LogoContainer = styled("div")`
  display: flex;
  position: relative;
`;

export const Para = styled("div")`
  color: #d4c4b0;
  font-size: 14px;
  width: 70%;
`;

export const Large = styled(Link)`
  font-size: 16px;
  color: #f5ebe0;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-transform: capitalize;
  line-height: 24px;
  display: block;
  margin-bottom: 0.625rem;
  max-width: max-content;

  &:hover {
    color: var(--color-gold);
    text-decoration: underline;
    text-underline-offset: 3px;
  }
`;

export const Chat = styled("p")`
  color: #f5ebe0;
  max-width: fit-content;
  border-bottom: 1px solid #d4c4b0;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease-in-out;

  &:hover {
    border-bottom: 1px solid var(--color-gold);
    color: var(--color-gold);
  }
`;

export const Empty = styled("div")`
  position: relative;
  height: 53px;
`;

export const FooterContainer = styled("div")`
  max-width: 510px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  text-align: center;
  align-items: center;
  transition: all 0.1s ease-in-out;

  a {
    &:hover,
    &:active,
    &:focus {
      transform: scale(1.1);
    }
  }

  @media screen and (max-width: 769px) {
    width: auto;

    a:not(:last-child) {
      display: none;
    }
  }

  div {
    cursor: pointer;
    margin-right: 15px;
    width: 25px;
    height: 25px;

    &:hover {
      fill: var(--color-gold);
    }
  }
`;

export const Language = styled("h4")`
  font-size: 22px;
  text-transform: capitalize;
  color: #f5ebe0;
  font-family: var(--font-display);

  @media screen and (max-width: 414px) {
    padding: 1.5rem 0;
  }
`;

export const Label = styled("label")`
  font-size: 22px;
  text-transform: capitalize;
  color: #f5ebe0;
  display: block;
  margin-bottom: 2rem;
  font-family: var(--font-display);

  @media screen and (max-width: 414px) {
    padding: 1.5rem 0;
    margin-bottom: 1rem;
  }
`;

export const LanguageSwitch = styled("div")`
  cursor: pointer;
  transition: all 0.1s ease-in-out;

  &:hover,
  &:active,
  &:focus {
    transform: scale(1.1);
  }
`;

export const LanguageSwitchContainer = styled("div")`
  display: flex;
  justify-content: space-between;
  width: 85px;
`;
