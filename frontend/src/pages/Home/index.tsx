import { lazy } from "react";
import { useHistory } from "react-router-dom";
import { Button } from "../../common/Button";
import IntroContent from "../../content/IntroContent.json";
import MiddleBlockContent from "../../content/MiddleBlockContent.json";
import AboutContent from "../../content/AboutContent.json";
import MissionContent from "../../content/MissionContent.json";
import ProductContent from "../../content/ProductContent.json";
import ContactContent from "../../content/ContactContent.json";

const Contact = lazy(() => import("../../components/ContactForm"));
const MiddleBlock = lazy(() => import("../../components/MiddleBlock"));
const Container = lazy(() => import("../../common/Container"));
const ScrollToTop = lazy(() => import("../../common/ScrollToTop"));
const ContentBlock = lazy(() => import("../../components/ContentBlock"));

const Home = () => {
  const history = useHistory();

  return (
    <Container>
      <ScrollToTop />
      <ContentBlock
        direction="right"
        title={IntroContent.title}
        content={IntroContent.text}
        button={IntroContent.button}
        icon="developer.svg"
        id="intro"
        onPrimaryClick={() => history.push("/learn/day/0")}
        onSecondaryClick={() => history.push("/learn")}
      />
      <MiddleBlock
        title={MiddleBlockContent.title}
        content={MiddleBlockContent.text}
        button={MiddleBlockContent.button}
        onButtonClick={() => history.push("/learn")}
      />
      <ContentBlock
        direction="left"
        title={AboutContent.title}
        content={AboutContent.text}
        section={AboutContent.section}
        icon="graphs.svg"
        id="about"
      />
      <ContentBlock
        direction="right"
        title={MissionContent.title}
        content={MissionContent.text}
        icon="product-launch.svg"
        id="mission"
        button={[
          { title: "Browse books", color: "#fff" },
          { title: "YouTube channel" },
        ]}
        onPrimaryClick={() => history.push("/books")}
        onSecondaryClick={() =>
          window.open("https://www.youtube.com/@HowtospeakBosnian", "_blank")
        }
      />
      <ContentBlock
        direction="left"
        title={ProductContent.title}
        content={ProductContent.text}
        icon="youtube.svg"
        iconSize="88px"
        id="product"
        button={[{ title: "Open YouTube channel" }]}
        onPrimaryClick={() =>
          window.open("https://www.youtube.com/@HowtospeakBosnian", "_blank")
        }
      />
      <div style={{ textAlign: "center", margin: "2rem 0" }}>
        <Button onClick={() => history.push("/dictionary")}>
          Open mini-dictionary
        </Button>
      </div>
      <Contact
        title={ContactContent.title}
        content={ContactContent.text}
        id="contact"
      />
    </Container>
  );
};

export default Home;
