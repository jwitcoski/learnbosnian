import { lazy, useEffect } from "react";
import { useHistory } from "react-router-dom";
import {
  HomeRoot,
  ShelfFrame,
  ShelfCredit,
  ContactWrap,
  KilimBand,
} from "./styles";

const Contact = lazy(() => import("../../components/ContactForm"));
const ScrollToTop = lazy(() => import("../../common/ScrollToTop"));

type ShelfMessage = {
  source?: string;
  type?: string;
  href?: string;
  external?: boolean;
};

const Home = () => {
  const history = useHistory();

  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      const data = event.data as ShelfMessage;
      if (!data || data.source !== "speak-bosnian-shelf" || data.type !== "navigate") {
        return;
      }
      const href = data.href;
      if (!href) return;

      if (data.external) {
        window.open(href, "_blank", "noopener,noreferrer");
        return;
      }

      if (href.startsWith("#")) {
        const el = document.querySelector(href);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }

      history.push(href);
    };

    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, [history]);

  return (
    <HomeRoot>
      <ScrollToTop />

      <ShelfFrame>
        <iframe
          title="How to Speak Bosnian series shelf"
          src="/shelf/complete-shelf.html"
          loading="eager"
          allow="autoplay"
        />
      </ShelfFrame>

      <ShelfCredit>
        Interactive shelf adapted from{" "}
        <a
          href="https://github.com/MengTo/threeui"
          target="_blank"
          rel="noreferrer"
        >
          ThreeUI Complete Shelf
        </a>{" "}
        (MIT). Open a volume, then use Enter to go to that book or page.
      </ShelfCredit>

      <KilimBand aria-hidden />

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
