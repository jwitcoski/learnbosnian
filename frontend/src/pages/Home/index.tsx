import { lazy } from "react";
import { Link, useHistory } from "react-router-dom";
import { book1Outline } from "../../data/loadChapters";
import { grammarOutline } from "../../data/loadGrammar";
import book2Outline from "../../data/book2/outline.json";
import book3Outline from "../../data/book3/outline.json";
import {
  HomeRoot,
  Hero,
  Cta,
  KilimBand,
  Section,
  BookGrid,
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
            Bosnian is the language of Bosnia and Herzegovina. People speak it
            at home, in schools and cafés, and in families living far from the
            country. You learn it because you are visiting, moving, marrying
            in, reclaiming a family language, or you already care about this
            place and want the real name for what you hear. This site teaches
            that named language, not a vague mix of the region.
          </p>
          <div className="cta-row">
            <Cta type="button" onClick={() => history.push("/learn/book/1")}>
              Start Book 1
            </Cta>
            <Cta $ghost type="button" onClick={() => history.push("/learn")}>
              See the books
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
          <h2>What this site is for</h2>
          <p>
            Bosnian hangs meaning on the ends of words, where English hangs it
            on little words and word order. The site exists so you can speak
            anyway. Book 1 gives you ready phrases in the present tense. The
            Grammar book is the notebook beside that walk. Books 2 and 3 wait
            until you want past-tense stories and longer talk. Every page uses
            Latin script.
          </p>
          <SolidCta type="button" onClick={() => history.push("/learn")}>
            See the books
          </SolidCta>
        </div>
      </Illustrate>

      <KilimBand aria-hidden />

      <Section>
        <h2>The books</h2>
        <p className="support">
          The Learn page holds the books. Book 1 is the walk through town in
          the present tense. Grammar is the notebook for endings. Books 2 and 3
          pick up past stories and longer talk. The dictionary and YouTube sit
          in the header when you want a word or a video.
        </p>
        <BookGrid>
          <Link to="/learn/book/1">
            <div className="kicker">Open now</div>
            <h3>Book 1</h3>
            <p>
              {book1Outline.title}. Phrases for the café, the street, and
              meeting people, in the present tense, with Ana, Emir, Amira, and
              Mrvica.
            </p>
          </Link>
          <Link to="/learn/grammar">
            <div className="kicker">Open now</div>
            <h3>Grammar</h3>
            <p>
              {grammarOutline.title}. English keeps coffee still in every job.
              Bosnian changes kahva to kahvu when you want the drink, because
              the work sits on the end of the word. This notebook covers
              gender, cases, verbs, and how a sentence actually runs, with the
              same small words you meet in Book 1.
            </p>
          </Link>
          <div className="soon">
            <div className="kicker">Not started</div>
            <h3>Book 2</h3>
            <p>
              {book2Outline.title}. Past-tense stories and more of the country,
              after Book 1 stays in the present.
            </p>
          </div>
          <div className="soon">
            <div className="kicker">Not started</div>
            <h3>Book 3</h3>
            <p>
              {book3Outline.title}. Longer conversation and writing, once the
              earlier books have done their job.
            </p>
          </div>
        </BookGrid>
      </Section>

      <KilimBand aria-hidden />

      <Illustrate>
        <div className="copy">
          <h2>Book 1 is the walk through town</h2>
          <p>
            If you want a story while you learn, that is Book 1. Ana drinks
            kahva at Amira’s. Emir gets a little lost with her. Mrvica steals
            the scene. It is survival Bosnian for a visit or early life here,
            and it is only one book on the shelf.
          </p>
          <SolidCta type="button" onClick={() => history.push("/learn/book/1")}>
            Open Book 1
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
            Companion videos sit on YouTube with stills, on-screen text, and
            optional narration, so you can hear a Book 1 lesson when you are
            away from the page.
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
          content="Questions about the books, classroom use, or how to start? Send a note."
          id="contact"
        />
      </ContactWrap>
    </HomeRoot>
  );
};

export default Home;
