import { lazy } from "react";
import { Link, useHistory } from "react-router-dom";
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
    src: "/images/home/mostar-bridge.png",
    alt: "Flat polygon painting of Stari Most, the Old Bridge in Mostar",
    credit:
      "Stari Most, Mostar",
  },
  coffee: {
    src: "/images/home/bosnian-coffee.png",
    alt: "Flat polygon painting of a traditional Bosnian coffee set",
    credit:
      "Bosnian coffee, Baščaršija",
  },
  costume: {
    src: "/images/home/traditional-costume.png",
    alt: "Flat polygon painting of women in traditional Bosnian folk dress",
    credit:
      "Traditional Bosnian costume",
  },
};

const Home = () => {
  const history = useHistory();

  return (
    <HomeRoot>
      <ScrollToTop />

      <Hero>
        <div className="hero-copy">
          <h1 className="brand">How to Speak Bosnian</h1>
          <p className="lede">
            Beginner Bosnian for short stays and early life here. Order food,
            ask directions, meet people. Present tense only. Latin script only.
            Ana, Emir, Amira, and Mrvica walk you through it.
          </p>
          <div className="cta-row">
            <Cta type="button" onClick={() => history.push("/learn/book/1")}>
              Start Book 1
            </Cta>
            <Cta $ghost type="button" onClick={() => history.push("/learn")}>
              See curriculum
            </Cta>
          </div>
        </div>
        <StyledPhoto>
          <img src={PHOTOS.mostar.src} alt={PHOTOS.mostar.alt} />
          <Link className="credit" to="/attributions#home-mostar">
            {PHOTOS.mostar.credit}
          </Link>
        </StyledPhoto>
      </Hero>

      <KilimBand aria-hidden />

      <Illustrate $flip>
        <StyledPhoto>
          <img src={PHOTOS.coffee.src} alt={PHOTOS.coffee.alt} />
          <Link className="credit" to="/attributions#home-coffee">
            {PHOTOS.coffee.credit}
          </Link>
        </StyledPhoto>
        <div className="copy">
          <h2>One path, reviewed as it goes live</h2>
          <p>
            Each lesson is drafted and reviewed before it goes live. Same shape
            every time: goals, culture, practice, and a quiz. Make a džezva of
            kahva and settle in.
          </p>
          <SolidCta type="button" onClick={() => history.push("/learn")}>
            Open curriculum
          </SolidCta>
        </div>
      </Illustrate>

      <KilimBand aria-hidden />

      <Section>
        <h2>What you do in each lesson</h2>
        <p className="support">
          Goals, culture, words, grammar, a Say again warm-up, a puzzle,
          conversation, practice, fun facts, a game, resources, then the lesson
          quiz.
        </p>
        <Pillars>
          <article>
            <div className="label">Speak</div>
            <p>
              Dialogues with the same characters. Then record yourself for Speak
              Check, which listens and coaches your pronunciation.
            </p>
          </article>
          <article>
            <div className="label">Play</div>
            <p>
              Matching, unscramble, and quizzes when you want a break from
              drills.
            </p>
          </article>
          <article>
            <div className="label">Remember</div>
            <p>
              A Dictionary that grows with each published lesson.
            </p>
          </article>
        </Pillars>
      </Section>

      <Illustrate>
        <div className="copy">
          <h2>Follow the story across Bosnia and Herzegovina</h2>
          <p>
            Walk Baščaršija with Ana. Drink kahva at Amira’s. Get a little lost
            with Emir. Let Mrvica steal the scene. Book 1 is survival Bosnian for
            travelers and new arrivals, all in the present tense.
          </p>
          <SolidCta type="button" onClick={() => history.push("/learn")}>
            See the books
          </SolidCta>
        </div>
        <StyledPhoto>
          <img src={PHOTOS.costume.src} alt={PHOTOS.costume.alt} />
          <Link className="credit" to="/attributions#home-costume">
            {PHOTOS.costume.credit}
          </Link>
        </StyledPhoto>
      </Illustrate>

      <YoutubeStrip>
        <img src="/img/svg/youtube.svg" alt="" width={56} height={56} />
        <div>
          <h2>Watch on YouTube</h2>
          <p>
            Companion videos go up on YouTube as each Book 1 lesson is written
            and published, with stills, on-screen text, and optional narration.
          </p>
          <SolidCta
            type="button"
            onClick={() =>
              window.open("https://www.youtube.com/@HowtospeakBosnian", "_blank")
            }
          >
            Open the channel
          </SolidCta>
        </div>
      </YoutubeStrip>

      <ContactWrap>
        <Contact
          title="Say zdravo"
          content="Questions about the books, classroom use, or a lesson draft? Send a note."
          id="contact"
        />
      </ContactWrap>
    </HomeRoot>
  );
};

export default Home;
