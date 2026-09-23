import { Link } from "react-router-dom";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";
import { CONTACT_EMAIL } from "../../common/utils/useForm";

const Contact = () => {
  return (
    <LessonPage>
      <h1>Contact</h1>
      <p>
        How to Speak Bosnian is an independent site. Questions, corrections,
        and classroom requests all go to one inbox. Write in English or
        Bosnian.
      </p>
      <p>
        Email:{" "}
        <a href={`mailto:${CONTACT_EMAIL}`}>
          <strong>{CONTACT_EMAIL}</strong>
        </a>
      </p>

      <SectionDivider />

      <h2>Good reasons to write</h2>
      <ul>
        <li>
          You found a mistake in a lesson, a translation, or a recording. Name
          the lesson number and the phrase so it can be fixed quickly.
        </li>
        <li>
          You teach Bosnian and want to use Book 1 or the Grammar notebook
          with a class.
        </li>
        <li>
          You are not sure where to start. Say how you will use Bosnian: a
          visit, a move, family, or work.
        </li>
        <li>
          You own a photo on the site and want the credit changed or the image
          removed. The <Link to="/attributions">photo credits</Link> page lists
          every source.
        </li>
        <li>
          You have a question about privacy or the data this site stores. See
          the <Link to="/privacy">privacy policy</Link> first; it may already
          answer it.
        </li>
      </ul>

      <h2>Video</h2>
      <p>
        Comments on the{" "}
        <a
          href="https://www.youtube.com/@HowtospeakBosnian"
          target="_blank"
          rel="noreferrer"
        >
          YouTube channel
        </a>{" "}
        are read too, but email is the surest way to get a reply.
      </p>
      <p>
        <Link to="/about">About the site</Link>
        {" · "}
        <Link to="/learn/book/1">Open Book 1</Link>
      </p>
    </LessonPage>
  );
};

export default Contact;
