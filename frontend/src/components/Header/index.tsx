import { useState } from "react";
import { Row, Col, Drawer } from "antd";
import { Link } from "react-router-dom";
import Container from "../../common/Container";
import { Button } from "../../common/Button";
import {
  HeaderSection,
  LogoContainer,
  Burger,
  NotHidden,
  Menu,
  CustomNavLinkSmall,
  Label,
  Outline,
  Span,
} from "./styles";

const Header = () => {
  const [visible, setVisibility] = useState(false);

  const toggleButton = () => {
    setVisibility(!visible);
  };

  const MenuItem = () => {
    return (
      <>
        <CustomNavLinkSmall>
          <Link to="/learn">
            <Span>Learn</Span>
          </Link>
        </CustomNavLinkSmall>
        <CustomNavLinkSmall>
          <Link to="/dictionary">
            <Span>Dictionary</Span>
          </Link>
        </CustomNavLinkSmall>
        <CustomNavLinkSmall>
          <Link to="/books">
            <Span>Books</Span>
          </Link>
        </CustomNavLinkSmall>
        <CustomNavLinkSmall>
          <a
            href="https://www.youtube.com/@HowtospeakBosnian"
            target="_blank"
            rel="noreferrer"
          >
            <Span>YouTube</Span>
          </a>
        </CustomNavLinkSmall>
        <CustomNavLinkSmall style={{ width: "180px" }}>
          <Link to="/learn/day/0">
            <Span>
              <Button>Start Day 0</Button>
            </Span>
          </Link>
        </CustomNavLinkSmall>
      </>
    );
  };

  return (
    <HeaderSection>
      <Container>
        <Row justify="space-between">
          <LogoContainer to="/" aria-label="homepage">
            <div
              style={{
                fontSize: "18px",
                fontWeight: "bold",
                color: "#5D4037",
                fontFamily: "var(--font-display)",
                lineHeight: 1.15,
              }}
            >
              <div>Learn Bosnian</div>
            </div>
          </LogoContainer>
          <NotHidden>
            <MenuItem />
          </NotHidden>
          <Burger onClick={toggleButton}>
            <Outline />
          </Burger>
        </Row>
        <Drawer closable={false} open={visible} onClose={toggleButton}>
          <Col style={{ marginBottom: "2.5rem" }}>
            <Label onClick={toggleButton}>
              <Col span={12}>
                <Menu>Menu</Menu>
              </Col>
              <Col span={12}>
                <Outline />
              </Col>
            </Label>
          </Col>
          <div onClick={() => setVisibility(false)}>
            <MenuItem />
          </div>
        </Drawer>
      </Container>
    </HeaderSection>
  );
};

export default Header;
