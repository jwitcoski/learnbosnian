import { lazy } from "react";
import { useHistory } from "react-router-dom";
import {
  HomeRoot,
  Hero,
  Cta,
  KilimBand,
  Section,
  Pillars,
  Split,
  SolidCta,
  YoutubeStrip,
  ContactWrap,
} from "./styles";

const Contact = lazy(() => import("../../components/ContactForm"));
const ScrollToTop = lazy(() => import("../../common/ScrollToTop"));

const BASCARSIJA = {
  src: "/images/book1/day-01-bascarsija.jpg",
  credit:
    "Baščaršija, Sarajevo — Kathleen Franklin / Wikimedia Commons (CC BY 2.0)",
};

const SEBILJ = {
  src: "/images/book1/day-01-sebilj.jpg",
  credit:
    "Sebilj fountain, Sarajevo — BloodSaric / Wikimedia Commons (CC BY-SA 2.5)",
};

const Home = () => {
  const history = useHistory();

  return (
    <HomeRoot>
      <ScrollToTop />

      <Hero>
        <div className="hero-media" aria-hidden>
          <img src={BASCARSIJA.src} alt="" />
        </div>
        <div className="hero-shade" aria-hidden />
        <div className="hero-inner">
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
          <p className="credit">{BASCARSIJA.credit}</p>
        </div>
      </Hero>

      <KilimBand aria-hidden />

      <Section>
        <h2>One clear path</h2>
        <p className="support">
          Every chapter is drafted and reviewed before it goes live. Companion
          videos live on the How to speak Bosnian channel.
        </p>
        <SolidCta type="button" onClick={() => history.push("/learn")}>
          Open the curriculum
        </SolidCta>
      </Section>

      <KilimBand aria-hidden />

      <Section>
        <h2>Same lesson shape every day</h2>
        <p className="support">
          Goals, culture, vocab, grammar, a puzzle, conversation, practice, fun
          facts, another game, resources, then a section quiz. The same layout
          each day so you always know what comes next.
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

      <Split>
        <div className="photo">
          <img src={SEBILJ.src} alt="Sebilj fountain in Baščaršija, Sarajevo" />
          <div className="credit">{SEBILJ.credit}</div>
        </div>
        <div className="copy">
          <h2>Follow the story through Bosnia</h2>
          <p>
            Walk Baščaršija with Ana, drink kahva at Amira’s, get lost with Emir,
            and let Mrvica steal the scene. Book 1 takes you from first greetings
            to Mostar.
          </p>
          <SolidCta type="button" onClick={() => history.push("/books")}>
            Browse the book series
          </SolidCta>
        </div>
      </Split>

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
