import { Link } from "react-router-dom";
import data from "../../data/attributions.json";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";
import {
  AttrIntro,
  AttrMeta,
  AttrList,
  AttrCard,
  AttrThumb,
  AttrBody,
  AttrTitle,
  AttrWhere,
  AttrDl,
  AttrLink,
  AttrNotes,
  CiteBox,
} from "./styles";

type AttrEntry = {
  id: string;
  ref?: string;
  title: string;
  whereUsed?: string[];
  author?: string;
  source?: string;
  license?: string;
  pageUrl?: string;
  sourceUrl?: string;
  localPath?: string;
  credit?: string;
  notes?: string;
  book?: number | string;
  day?: number;
};

const Attributions = () => {
  const entries = (data.entries || []) as AttrEntry[];

  return (
    <LessonPage>
      <h1>{data.title}</h1>
      <AttrIntro>{data.intro}</AttrIntro>
      <AttrMeta>
        {data.total} image{data.total === 1 ? "" : "s"} · last synced{" "}
        {data.generatedAt}
      </AttrMeta>

      <CiteBox>
        <h2>How to cite for the book</h2>
        <p>{data.citationNote}</p>
        <p>
          This page is the master list. Lesson photos are numbered{" "}
          <strong>book.lesson + letter</strong>: 1.1a is Book 1, Lesson 1,
          first photo. Grammar photos use <strong>G.chapter + letter</strong>:
          G.1a is Grammar, Chapter 1, first photo. Captions on each page use
          the same codes.
        </p>
      </CiteBox>

      <SectionDivider />

      <AttrList>
        {entries.map((e) => {
          const href = e.pageUrl || e.sourceUrl;
          return (
            <AttrCard key={e.id} id={e.ref || e.id}>
              {e.localPath ? (
                <AttrThumb>
                  <img src={e.localPath} alt="" />
                </AttrThumb>
              ) : (
                <AttrThumb aria-hidden />
              )}
              <AttrBody>
              {e.ref ? <span id={e.id} hidden /> : null}
              <AttrTitle>
                {e.ref ? <span className="ref">{e.ref}</span> : null}
                {e.title}
              </AttrTitle>
              {e.whereUsed?.length ? (
                <AttrWhere>
                  {e.whereUsed.map((w) => (
                    <li key={w}>{w}</li>
                  ))}
                </AttrWhere>
              ) : null}
              <AttrDl>
                {e.author ? (
                  <>
                    <dt>Author</dt>
                    <dd>{e.author}</dd>
                  </>
                ) : null}
                {e.source ? (
                  <>
                    <dt>Source</dt>
                    <dd>{e.source}</dd>
                  </>
                ) : null}
                {e.license ? (
                  <>
                    <dt>License</dt>
                    <dd>{e.license}</dd>
                  </>
                ) : null}
                {e.credit ? (
                  <>
                    <dt>Credit line</dt>
                    <dd>{e.credit}</dd>
                  </>
                ) : null}
                {e.localPath ? (
                  <>
                    <dt>Local file</dt>
                    <dd>
                      <code>{e.localPath}</code>
                    </dd>
                  </>
                ) : null}
              </AttrDl>
              {href ? (
                <AttrLink href={href} target="_blank" rel="noopener noreferrer">
                  Open source page →
                </AttrLink>
              ) : null}
              {e.notes ? <AttrNotes>{e.notes}</AttrNotes> : null}
              </AttrBody>
            </AttrCard>
          );
        })}
      </AttrList>

      <SectionDivider />

      <p>
        <Link to="/">← Home</Link>
        {" · "}
        <Link to="/learn/book/1">Curriculum</Link>
      </p>
    </LessonPage>
  );
};

export default Attributions;
