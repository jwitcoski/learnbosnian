import { lazy } from "react";
import { useHistory } from "react-router-dom";
import {
  HomeRoot,
  Hero,
  Cta,
  KilimBand,
  Section,
  Pillars,
  Illustrate,
  SolidCta,
  YoutubeStrip,
  ContactWrap,
  StyledPhoto,
} from "./styles";

const Contact = lazy(() => import("../../components/ContactForm"));
const ScrollToTop = lazy(() => import("../../common/ScrollToTop"));

const PHOTOS = {
  mostar: {
    src: "/images/home/mostar-bridge.jpg",
    alt: "Pencil sketch of Stari Most, the Old Bridge in Mostar",
    credit:
      "Pencil sketch from photo — Stari Most, Mostar — Hatice Baran / Pexels",
  },
  coffee: {
    src: "/images/home/bosnian-coffee.jpg",
    alt: "Pencil sketch of a traditional Bosnian coffee set",
    credit:
      "Pencil sketch from photo — Bosnian coffee, Baščaršija — İhsan Işık / Wikimedia Commons (CC BY 3.0)",
  },
  costume: {
    src: "/images/home/traditional-costume.jpg",
    alt: "Pencil sketch of women in traditional Bosnian folk dress",
    credit:
      "Pencil sketch from photo — Traditional Bosnian costume — Historym1468 / Wikimedia Commons (CC BY 4.0)",
  },
};

const Home = () => {
  const history = useHistory();

  return (
    <HomeRoot>
      <ScrollToTop />

      <Hero>
        <div className="hero-copy">
          <h1 className="brand">Learn Bosnian</h1>
          <p className="lede">
            Real Bosnian in Latin script, culture from Sarajevo to Mostar, and a
            silly story with Ana, Emir, Amira, and Mrvica the cat.
          </p>
          <div className="cta-row">
            <Cta type="button" onClick={() => history.push("/learn/day/0")}>
              Start Day 0
            </Cta>
            <Cta $ghost type="button" onClick={() => history.push("/learn")}>
              See curriculum
            </Cta>
          </div>
        </div>
        <StyledPhoto>
          <img src={PHOTOS.mostar.src} alt={PHOTOS.mostar.alt} />
          <span className="credit">{PHOTOS.mostar.credit}</span>
        </StyledPhoto>
      </Hero>

      <KilimBand aria-hidden />

      <Illustrate $flip>
        <StyledPhoto>
          <img src={PHOTOS.coffee.src} alt={PHOTOS.coffee.alt} />
          <span className="credit">{PHOTOS.coffee.credit}</span>
        </StyledPhoto>
        <div className="copy">
          <h2>One clear path</h2>
          <p>
            Every chapter is drafted and reviewed before it goes live. Sit with a
            džezva of kahva and follow the same lesson shape each day — goals,
            culture, practice, and a quiz.
          </p>
          <SolidCta type="button" onClick={() => history.push("/learn")}>
            Open the curriculum
          </SolidCta>
        </div>
      </Illustrate>

      <KilimBand aria-hidden />

      <Section>
        <h2>Same lesson shape every day</h2>
        <p className="support">
          Goals, culture, vocab, grammar, a puzzle, conversation, practice, fun
          facts, another game, resources, then a section quiz.
        </p>
        <Pillars>
          <article>
            <div className="label">Speak</div>
            <p>Dialogues with recurring characters and a gentle storyline.</p>
          </article>
          <article>
            <div className="label">Play</div>
            <p>
              Matching, unscramble, and quizzes for brains that tire of dry
              drills.
            </p>
          </article>
          <article>
            <div className="label">Remember</div>
            <p>
              A growing mini-dictionary of every word you learn, ready when you
              need it.
            </p>
          </article>
        </Pillars>
      </Section>

      <Illustrate>
        <div className="copy">
          <h2>Follow the story through Bosnia</h2>
          <p>
            Walk Baščaršija with Ana, drink kahva at Amira’s, get lost with Emir,
            and let Mrvica steal the scene. Book 1 takes you from first greetings
            to Mostar — and the culture of the whole country.
          </p>
          <SolidCta type="button" onClick={() => history.push("/books")}>
            Browse the book series
          </SolidCta>
        </div>
        <StyledPhoto>
          <img src={PHOTOS.costume.src} alt={PHOTOS.costume.alt} />
          <span className="credit">{PHOTOS.costume.credit}</span>
        </StyledPhoto>
      </Illustrate>

      <YoutubeStrip>
        <img src="/img/svg/youtube.svg" alt="" width={56} height={56} />
        <div>
          <h2>Watch along on YouTube</h2>
          <p>
            Join learners on How to speak Bosnian. Each Book 1 chapter has a
            companion video with scenic stills, clear text, and optional
            narration.
          </p>
          <SolidCta
            type="button"
            onClick={() =>
              window.open("https://www.youtube.com/@HowtospeakBosnian", "_blank")
            }
          >
            Open YouTube channel
          </SolidCta>
        </div>
      </YoutubeStrip>

      <ContactWrap>
        <Contact
          title="Say zdravo"
          content="Questions about the books, school use, or a chapter draft? Send a note."
          id="contact"
        />
      </ContactWrap>
    </HomeRoot>
  );
};

export default Home;
