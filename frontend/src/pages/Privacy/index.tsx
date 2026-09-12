import { Link } from "react-router-dom";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";

const Privacy = () => {
  return (
    <LessonPage>
      <h1>Privacy policy</h1>
      <p>Last updated: 12 September 2026</p>
      <p>
        This policy explains how How to Speak Bosnian
        (howtospeakbosnian.com) handles information when you use the website.
        You can study without creating an account.
      </p>

      <SectionDivider />

      <h2>Who we are</h2>
      <p>
        How to Speak Bosnian is an independent language-learning site. Contact:{" "}
        <a href="mailto:info@howtospeakbosnian.com">
          info@howtospeakbosnian.com
        </a>
        .
      </p>

      <h2>What we store on your device</h2>
      <p>
        Lesson progress, quiz scores, and similar study state stay in your
        browser (for example localStorage). That data does not go to our
        servers as a user profile. Clearing site data in your browser removes
        it.
      </p>
      <p>
        If you use Record yourself / speak check, a short audio clip is sent
        so we can score pronunciation. We do not use those clips to build a
        marketing profile.
      </p>

      <h2>Analytics</h2>
      <p>
        We use Google Analytics 4 (measurement ID G-WET6BEL10L) to see which
        pages are used. Google may set cookies or similar identifiers and
        receive your IP address, browser type, and page path. See{" "}
        <a
          href="https://policies.google.com/privacy"
          target="_blank"
          rel="noreferrer"
        >
          Google’s privacy policy
        </a>
        .
      </p>

      <h2>Advertising</h2>
      <p>
        We use Google AdSense (publisher ID ca-pub-4372859798489282). Google
        may show ads and use cookies or advertising IDs to measure ads and,
        where allowed, personalize them. You can learn more and opt out through{" "}
        <a
          href="https://www.google.com/settings/ads"
          target="_blank"
          rel="noreferrer"
        >
          Google Ads settings
        </a>{" "}
        and{" "}
        <a
          href="https://policies.google.com/technologies/ads"
          target="_blank"
          rel="noreferrer"
        >
          how Google uses data in ads
        </a>
        .
      </p>

      <h2>Contact form and email</h2>
      <p>
        If you write to us, we keep the message so we can reply. We do not sell
        your email address.
      </p>

      <h2>Children</h2>
      <p>
        The course is written for general learners. We do not knowingly collect
        personal information from children under 13.
      </p>

      <h2>Changes</h2>
      <p>
        If this policy changes, we will update this page and the date at the
        top.
      </p>
      <p>
        <Link to="/about">About the site</Link>
        {" · "}
        <Link to="/">Home</Link>
      </p>
    </LessonPage>
  );
};

export default Privacy;
