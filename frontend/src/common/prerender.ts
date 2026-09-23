/**
 * Static HTML written into #root by scripts/prerender.cjs. It is shown as the
 * Suspense fallback on first load only, so there is no blank flash while the
 * route chunk downloads. Later navigations fall back to nothing.
 */
let prerenderedHtml: string | null = null;

export function capturePrerenderedHtml(root: HTMLElement) {
  if (root.dataset.prerenderedPath === window.location.pathname) {
    prerenderedHtml = root.innerHTML;
  }
  delete root.dataset.prerenderedPath;
}

export function takePrerenderedHtml(): string | null {
  const html = prerenderedHtml;
  prerenderedHtml = null;
  return html;
}
