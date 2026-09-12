import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}

const MEASUREMENT_ID = "G-WET6BEL10L";

/** Send GA4 page views on client-side route changes (first load is handled by gtag in index.html). */
const GoogleAnalytics = () => {
  const { pathname, search } = useLocation();
  const isFirstLoad = useRef(true);

  useEffect(() => {
    if (isFirstLoad.current) {
      isFirstLoad.current = false;
      return;
    }
    window.gtag?.("config", MEASUREMENT_ID, {
      page_path: `${pathname}${search}`,
    });
  }, [pathname, search]);

  return null;
};

export default GoogleAnalytics;
