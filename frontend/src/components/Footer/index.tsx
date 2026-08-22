import { Row, Col } from "antd";
import { Link } from "react-router-dom";
import { SvgIcon } from "../../common/SvgIcon";
import Container from "../../common/Container";
import {
  FooterSection,
  Title,
  NavLink,
  Extra,
  LogoContainer,
  Para,
  Large,
  Chat,
  FooterContainer,
  Language,
} from "./styles";

interface SocialLinkProps {
  href: string;
  src: string;
}

const Footer = () => {
  const SocialLink = ({ href, src }: SocialLinkProps) => {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        key={src}
        aria-label={src}
      >
        <SvgIcon src={src} width="25px" height="25px" />
      </a>
    );
  };

  return (
    <>
      <FooterSection>
        <Container>
          <Row justify="space-between">
            <Col lg={10} md={10} sm={12} xs={24}>
              <Language>How to Speak Bosnian</Language>
              <Para>
                Book 1, Grammar, and later books live on the Learn page. Latin
                script. A cat named Mrvica.
              </Para>
              <a href="mailto:info@howtospeakbosnian.com">
                <Chat>Contact</Chat>
              </a>
            </Col>
            <Col lg={8} md={8} sm={12} xs={12}>
              <Title>Study</Title>
              <Large to="/learn">Curriculum</Large>
              <Large to="/dictionary">Dictionary</Large>
              <Large to="/learn">Book series</Large>
              <Large to="/learn/book/1">Book 1</Large>
              <Large to="/learn/grammar">Grammar</Large>
              <Large to="/attributions">Photo attributions</Large>
            </Col>
            <Col lg={6} md={6} sm={12} xs={12}>
              <Title>Watch</Title>
              <a
                href="https://www.youtube.com/@HowtospeakBosnian"
                target="_blank"
                rel="noreferrer"
              >
                <Para>YouTube channel</Para>
              </a>
              <Link to="/learn">
                <Para>Books 2 &amp; 3 (not started)</Para>
              </Link>
              <Link to="/attributions">
                <Para>Photo credits</Para>
              </Link>
            </Col>
          </Row>
        </Container>
      </FooterSection>
      <Extra>
        <Container border={true}>
          <Row
            justify="space-between"
            align="middle"
            style={{ paddingTop: "3rem" }}
          >
            <NavLink to="/">
              <LogoContainer>
                <div
                  style={{
                    fontSize: "18px",
                    fontWeight: "bold",
                    color: "#f5ebe0",
                    fontFamily: "var(--font-display)",
                  }}
                >
                  How to Speak Bosnian
                </div>
              </LogoContainer>
            </NavLink>
            <FooterContainer>
              <SocialLink
                href="https://www.youtube.com/@HowtospeakBosnian"
                src="youtube.svg"
              />
            </FooterContainer>
          </Row>
        </Container>
      </Extra>
    </>
  );
};

export default Footer;
