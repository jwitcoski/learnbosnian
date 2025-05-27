import { Row, Col } from "antd";
import { withTranslation, TFunction } from "react-i18next";
import { SvgIcon } from "../../common/SvgIcon";
import Container from "../../common/Container";

import i18n from "i18next";
import {
  FooterSection,
  Title,
  NavLink,
  Extra,
  LogoContainer,
  Para,
  Large,
  Chat,
  Empty,
  FooterContainer,
  Language,
  Label,
  LanguageSwitch,
  LanguageSwitchContainer,
} from "./styles";

interface SocialLinkProps {
  href: string;
  src: string;
}

const Footer = ({ t }: { t: TFunction }) => {
  const handleChange = (language: string) => {
    i18n.changeLanguage(language);
  };

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
            <Col lg={10} md={10} sm={12} xs={12}>
              <Language>{t("Contact")}</Language>
              <Large to="/">{t("Need help learning?")}</Large>
              <Para>
                {t(`Have questions about Bosnian language or our lessons? We're here to help!`)}
              </Para>
              <a href="mailto:info@learnbosnian.com">
                <Chat>{t(`Contact Us`)}</Chat>
              </a>
            </Col>
            <Col lg={8} md={8} sm={12} xs={12}>
              <Title>{t("Learning Resources")}</Title>
              <Large to="/">{t("Grammar Guide")}</Large>
              <Large to="/">{t("Vocabulary Lists")}</Large>
              <Large to="/">{t("Pronunciation Guide")}</Large>
              <Large to="/">{t("Cultural Notes")}</Large>
            </Col>
            <Col lg={6} md={6} sm={12} xs={12}>
              <Title>{t("Support")}</Title>
              <Large to="/">{t("Help Center")}</Large>
              <Large to="/">{t("Community Forum")}</Large>
              <Large to="/">{t("Study Tips")}</Large>
            </Col>
          </Row>
          <Row justify="space-between">
            <Col lg={10} md={10} sm={12} xs={12}>
              <Empty />
              <Language>{t("About Bosnia")}</Language>
              <Para>{t("Learn about the beautiful country")}</Para>
              <Para>{t("where Bosnian is spoken")}</Para>
              <Para>{t("Sarajevo • Mostar • Banja Luka")}</Para>
            </Col>
            <Col lg={8} md={8} sm={12} xs={12}>
              <Title>{t("Learn More")}</Title>
              <Large to="/">{t("About Us")}</Large>
              <Large to="/">{t("Teaching Method")}</Large>
              <Large to="/">{t("Success Stories")}</Large>
              <Large to="/">{t("Blog")}</Large>
            </Col>
            <Col lg={6} md={6} sm={12} xs={12}>
              <Label htmlFor="select-lang">{t("Language")}</Label>
              <LanguageSwitchContainer>
                <LanguageSwitch onClick={() => handleChange("en")}>
                  <SvgIcon
                    src="united-states.svg"
                    aria-label="English"
                    width="30px"
                    height="30px"
                  />
                </LanguageSwitch>
                <LanguageSwitch onClick={() => handleChange("bs")}>
                  <SvgIcon
                    src="bosnia.svg"
                    aria-label="Bosanski"
                    width="30px"
                    height="30px"
                  />
                </LanguageSwitch>
              </LanguageSwitchContainer>
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
                <div style={{ 
                  fontSize: '20px', 
                  fontWeight: 'bold', 
                  color: '#18216d',
                  textAlign: 'center'
                }}>
                  <div>Learn</div>
                  <div>Bosnian</div>
                </div>
              </LogoContainer>
            </NavLink>
            <FooterContainer>
              <SocialLink
                href="https://github.com/learnbosnian"
                src="github.svg"
              />
              <SocialLink
                href="https://twitter.com/learnbosnian"
                src="twitter.svg"
              />
              <SocialLink
                href="https://www.facebook.com/learnbosnian"
                src="facebook.svg"
              />
              <SocialLink
                href="https://www.youtube.com/learnbosnian"
                src="youtube.svg"
              />
            </FooterContainer>
          </Row>
        </Container>
      </Extra>
    </>
  );
};

export default withTranslation()(Footer);
