import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const SITE_NAME = "How to Speak Bosnian";

function titleFromHeading() {
  const heading = document.querySelector("#root h1")?.textContent?.trim();
  if (!heading || heading === SITE_NAME) return SITE_NAME;
  return `${heading} · ${SITE_NAME}`;
}

/**
 * Title each page after its h1. Route pages load lazily, so watch #root until
 * the heading appears; scripts/prerender.cjs bakes the result into static HTML.
 */
const DocumentTitle = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    const root = document.getElementById("root");
    const update = () => {
      const next = titleFromHeading();
      if (document.title !== next) document.title = next;
    };
    update();
    if (!root) return;
    const observer = new MutationObserver(update);
    observer.observe(root, { childList: true, subtree: true, characterData: true });
    return () => observer.disconnect();
  }, [pathname]);

  return null;
};

export default DocumentTitle;
