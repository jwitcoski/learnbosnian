import { Row, Col } from "antd";
import { Fade } from "react-awesome-reveal";
import { withTranslation } from "react-i18next";

import { ContentBlockProps } from "./types";
import { Button } from "../../common/Button";
import { SvgIcon } from "../../common/SvgIcon";
import {
  ContentSection,
  Content,
  ContentWrapper,
  ServiceWrapper,
  MinTitle,
  MinPara,
  StyledRow,
  ButtonWrapper,
} from "./styles";

const ContentBlock = ({
  icon,
  title,
  content,
  section,
  button,
  t,
  id,
  direction,
  onPrimaryClick,
  onSecondaryClick,
  iconSize,
}: ContentBlockProps) => {
  const scrollTo = (target: string) => {
    const element = document.getElementById(target) as HTMLDivElement;
    element?.scrollIntoView({
      behavior: "smooth",
    });
  };

  const iconWidth = iconSize || "100%";
  const iconHeight = iconSize || "100%";

  return (
    <ContentSection>
      <Fade direction={direction} triggerOnce>
        <StyledRow
          justify="space-between"
          align="middle"
          id={id}
          direction={direction}
        >
          {icon && (
            <Col lg={11} md={11} sm={12} xs={24}>
              <div
                style={
                  iconSize
                    ? {
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        minHeight: "160px",
                      }
                    : undefined
                }
              >
                <SvgIcon src={icon} width={iconWidth} height={iconHeight} />
              </div>
            </Col>
          )}
          <Col lg={icon ? 11 : 24} md={icon ? 11 : 24} sm={icon ? 11 : 24} xs={24}>
            <ContentWrapper style={icon ? undefined : { maxWidth: "720px", margin: "0 auto" }}>
              <h6>{t(title)}</h6>
              <Content>{t(content)}</Content>
              {button && button.length > 0 && (
                <ButtonWrapper>
                  {button.map(
                    (
                      item: {
                        color?: string;
                        title: string;
                      },
                      idx: number
                    ) => {
                      const handler =
                        idx === 0
                          ? onPrimaryClick || (() => scrollTo("about"))
                          : onSecondaryClick || (() => scrollTo("about"));
                      return (
                        <Button
                          key={idx}
                          color={item.color}
                          onClick={handler}
                        >
                          {t(item.title)}
                        </Button>
                      );
                    }
                  )}
                </ButtonWrapper>
              )}
              {section && section.length > 0 && (
                <ServiceWrapper>
                  <Row justify="space-between">
                    {section.map(
                      (
                        item: {
                          title: string;
                          content: string;
                          icon: string;
                        },
                        sid: number
                      ) => {
                        return (
                          <Col key={sid} span={11}>
                            <SvgIcon
                              src={item.icon}
                              width="60px"
                              height="60px"
                            />
                            <MinTitle>{t(item.title)}</MinTitle>
                            <MinPara>{t(item.content)}</MinPara>
                          </Col>
                        );
                      }
                    )}
                  </Row>
                </ServiceWrapper>
              )}
            </ContentWrapper>
          </Col>
        </StyledRow>
      </Fade>
    </ContentSection>
  );
};

export default withTranslation()(ContentBlock);
