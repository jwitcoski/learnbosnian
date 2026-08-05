import { useEffect } from "react";
import { useLocation } from "react-router-dom";

/** Reset window scroll on every route change (including day → day). */
const ScrollToTopOnNavigate = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

export default ScrollToTopOnNavigate;
