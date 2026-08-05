import styled from "styled-components";

export const StyledButton = styled("button")<{ color?: string }>`
  background: ${(p) => (p.color ? "transparent" : "#C62828")};
  color: ${(p) => (p.color ? "#5D4037" : "#fff")};
  font-size: 1rem;
  font-weight: 700;
  width: 100%;
  border: 2px solid ${(p) => (p.color ? "#5D4037" : "#C62828")};
  border-radius: 0;
  padding: 13px 0;
  cursor: pointer;
  margin-top: 0.625rem;
  max-width: 180px;
  transition: all 0.3s ease-in-out;

  &:hover,
  &:active,
  &:focus {
    color: #fff;
    border: 2px solid #5D4037;
    background-color: #5D4037;
  }
`;
