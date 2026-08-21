import { useEffect } from "react";
import { useLocation } from "react-router-dom";

function scrollToHash(hash: string) {
  const id = decodeURIComponent(hash.replace(/^#/, ""));
  if (!id) return false;
  const el = document.getElementById(id);
  if (!el) return false;
  el.scrollIntoView({ block: "start" });
  return true;
}

/** Reset window scroll on route change. If the URL has a hash, jump to that id. */
const ScrollToTopOnNavigate = () => {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (!hash) {
      window.scrollTo(0, 0);
      return;
    }
    if (scrollToHash(hash)) return;
    const times = [0, 80, 250, 500].map((ms) =>
      window.setTimeout(() => scrollToHash(hash), ms)
    );
    return () => times.forEach((id) => window.clearTimeout(id));
  }, [pathname, hash]);

  return null;
};

export default ScrollToTopOnNavigate;
