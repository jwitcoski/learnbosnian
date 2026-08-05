import styled from "styled-components";
import { Link } from "react-router-dom";
import { MenuOutlined } from "@ant-design/icons";

export const HeaderSection = styled("header")`
  padding: 0.85rem 0.5rem;
  background: rgba(255, 248, 240, 0.92);
  border-bottom: 3px solid var(--color-crimson);
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(6px);

  .ant-row-space-between {
    align-items: center;
    text-align: center;
  }
`;

export const LogoContainer = styled(Link)`
  display: flex;
`;

export const NavLink = styled("div")`
  display: inline-block;
  text-align: center;
`;

export const CustomNavLink = styled("div")`
  width: 203px;
  display: inline-block;

  @media only screen and (max-width: 411px) {
    width: 150px;
  }

  @media only screen and (max-width: 320px) {
    width: 118px;
  }
`;

export const Burger = styled("div")`
  @media only screen and (max-width: 890px) {
    display: block;
  }

  display: none;

  svg {
    fill: var(--color-brown);
  }
`;

export const NotHidden = styled("div")`
  @media only screen and (max-width: 890px) {
    display: none;
  }
`;

export const Menu = styled("h5")`
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  color: var(--color-brown);
`;

export const CustomNavLinkSmall = styled(NavLink)`
  font-size: 1.05rem;
  color: var(--color-brown);
  transition: color 0.2s ease-in;
  margin: 0.5rem 1.25rem;

  @media only screen and (max-width: 768px) {
    margin: 1.25rem 2rem;
  }

  a {
    color: inherit;
  }
`;

export const Label = styled("span")`
  font-weight: 500;
  color: var(--color-muted);
  text-align: right;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
`;

export const Outline = styled(MenuOutlined)`
  font-size: 22px;
  color: var(--color-brown);
`;

export const Span = styled("span")`
  cursor: pointer;
  transition: color 0.2s ease;
  font-weight: 600;

  &:hover,
  &:active,
  &:focus {
    color: var(--color-crimson);
  }
`;
