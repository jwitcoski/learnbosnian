import { Link } from "react-router-dom";
import data from "../../data/attributions.json";
import { LessonPage, SectionDivider } from "../../components/lesson/styles";
import {
  AttrIntro,
  AttrMeta,
  AttrList,
  AttrCard,
  AttrTitle,
  AttrWhere,
  AttrDl,
  AttrLink,
  AttrNotes,
  CiteBox,
} from "./styles";

type AttrEntry = {
  id: string;
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
  book?: number;
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
          This page is the master list. For Scribus or YouTube packs, take
          credits from here or from each lesson’s image list.
        </p>
      </CiteBox>

      <SectionDivider />

      <AttrList>
        {entries.map((e) => {
          const href = e.pageUrl || e.sourceUrl;
          return (
            <AttrCard key={e.id} id={e.id}>
              <AttrTitle>{e.title}</AttrTitle>
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
            </AttrCard>
          );
        })}
      </AttrList>

      <SectionDivider />

      <p>
        <Link to="/">← Home</Link>
        {" · "}
        <Link to="/learn">Curriculum</Link>
      </p>
    </LessonPage>
  );
};

export default Attributions;
