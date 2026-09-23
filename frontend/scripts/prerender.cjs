/**
 * Render every sitemap URL in headless Chrome and write static HTML into build/
 * so crawlers (Google Search, AdSense review) see real page text without JS.
 *
 *   /                  -> build/home/index.html   (index.html stays the SPA shell)
 *   /learn/lesson/3    -> build/learn/lesson/3/index.html
 *
 * CloudFront maps extensionless URLs to those files (see main.tf). Anything not
 * prerendered still falls back to the untouched build/index.html shell.
 *
 * Run after `react-scripts build`: `npm run prerender`.
 */
const fs = require("fs");
const http = require("http");
const path = require("path");
const puppeteer = require("puppeteer");

const BUILD_DIR = path.resolve(__dirname, "../build");
const SITE_ORIGIN = "https://howtospeakbosnian.com";
const CONCURRENCY = 4;
const BLOCKED_HOSTS = [
  "googlesyndication.com",
  "googletagmanager.com",
  "google-analytics.com",
  "doubleclick.net",
  "googleadservices.com",
  "adservice.google.com",
];

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".map": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".txt": "text/plain",
  ".xml": "application/xml",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".mp3": "audio/mpeg",
  ".pdf": "application/pdf",
};

const shellHtml = fs.readFileSync(path.join(BUILD_DIR, "index.html"), "utf8");

function sitemapPaths() {
  const xml = fs.readFileSync(path.join(BUILD_DIR, "sitemap.xml"), "utf8");
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(
    (m) => new URL(m[1].trim()).pathname
  );
}

function outputFile(routePath) {
  const dir = routePath === "/" ? "home" : routePath.replace(/^\/+|\/+$/g, "");
  return path.join(BUILD_DIR, dir, "index.html");
}

function startServer() {
  const server = http.createServer((req, res) => {
    const pathname = decodeURIComponent(new URL(req.url, "http://x").pathname);
    const ext = path.extname(pathname);
    if (!ext) {
      res.writeHead(200, { "Content-Type": MIME[".html"] });
      res.end(shellHtml);
      return;
    }
    const file = path.join(BUILD_DIR, pathname);
    if (!file.startsWith(BUILD_DIR) || !fs.existsSync(file)) {
      res.writeHead(404);
      res.end();
      return;
    }
    res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

function escapeAttr(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function truncate(text, max = 160) {
  if (text.length <= max) return text;
  return `${text.slice(0, max - 3).replace(/\s+\S*$/, "")}…`;
}

function setMeta(html, attr, key, value) {
  const pattern = new RegExp(`<meta ${attr}="${key}" content="[^"]*"\\s*/?>`);
  const tag = `<meta ${attr}="${key}" content="${escapeAttr(value)}"/>`;
  return pattern.test(html) ? html.replace(pattern, tag) : html;
}

function buildPage(routePath, snapshot) {
  const url = `${SITE_ORIGIN}${routePath}`;
  let html = shellHtml;
  html = html.replace(
    /<title>[^<]*<\/title>/,
    `<title>${escapeAttr(snapshot.title)}</title>`
  );
  if (snapshot.description) {
    html = setMeta(html, "name", "description", snapshot.description);
    html = setMeta(html, "property", "og:description", snapshot.description);
    html = setMeta(html, "property", "twitter:description", snapshot.description);
  }
  html = setMeta(html, "property", "og:title", snapshot.title);
  html = setMeta(html, "property", "twitter:title", snapshot.title);
  html = setMeta(html, "property", "og:url", url);

  const headExtras = [
    `<link rel="canonical" href="${escapeAttr(url)}"/>`,
    ...snapshot.stylesheets.map(
      (href) => `<link href="${escapeAttr(href)}" rel="stylesheet">`
    ),
    `<style data-prerendered>${snapshot.css.replace(/<\/style/gi, "<\\/style")}</style>`,
  ].join("");
  html = html.replace("</head>", `${headExtras}</head>`);
  html = html.replace(/<noscript>[\s\S]*?<\/noscript>/, "");

  html = html.replace(
    '<div id="root"></div>',
    `<div id="root" data-prerendered-path="${escapeAttr(routePath)}">${snapshot.body}</div>`
  );
  return html;
}

async function snapshotRoute(browser, origin, routePath) {
  const page = await browser.newPage();
  try {
    await page.setRequestInterception(true);
    page.on("request", (request) => {
      const host = new URL(request.url()).hostname;
      if (BLOCKED_HOSTS.some((h) => host === h || host.endsWith(`.${h}`))) {
        request.abort();
      } else {
        request.continue();
      }
    });
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(`${origin}${routePath}`, {
      waitUntil: "networkidle0",
      timeout: 60000,
    });
    await page.waitForSelector("#root h1", { timeout: 30000 });
    await new Promise((resolve) => setTimeout(resolve, 300));

    const finalPath = new URL(page.url()).pathname;
    if (finalPath !== routePath) {
      throw new Error(`redirected to ${finalPath}`);
    }

    return await page.evaluate((shellLinks) => {
      const root = document.getElementById("root");
      const css = Array.from(document.querySelectorAll("style"))
        .map((style) => {
          try {
            return Array.from(style.sheet.cssRules)
              .map((rule) => rule.cssText)
              .join("\n");
          } catch (e) {
            return style.textContent || "";
          }
        })
        .join("\n");
      const stylesheets = Array.from(
        document.querySelectorAll('link[rel="stylesheet"]')
      )
        .map((link) => link.getAttribute("href"))
        .filter((href) => href && !shellLinks.includes(href));

      const clean = (el) => el.textContent.replace(/\s+/g, " ").trim();
      const h1 = root.querySelector("h1");
      const next = h1.nextElementSibling;
      const subtitle =
        next && next.tagName === "P" && clean(next).length < 100 ? next : null;
      const paragraphs = Array.from(root.querySelectorAll("p"))
        .filter(
          (p) =>
            p !== subtitle &&
            !p.closest("footer, header, #video, figure") &&
            !(p.children.length === 1 && p.firstElementChild.tagName === "A")
        )
        .map(clean)
        .filter(Boolean);

      return {
        title: document.title,
        subtitle: subtitle ? clean(subtitle) : "",
        descriptionCandidates: paragraphs
          .filter((text) => text.length >= 50)
          .slice(0, 8),
        summary: [clean(h1), ...paragraphs].join(". ").replace(/\.\./g, "."),
        css,
        stylesheets,
        body: root.innerHTML,
        textLength: root.innerText.length,
      };
    }, [...shellHtml.matchAll(/<link href="([^"]+)" rel="stylesheet">/g)].map((m) => m[1]));
  } finally {
    await page.close();
  }
}

async function main() {
  const routes = [...new Set(sitemapPaths())];
  const server = await startServer();
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const failures = [];
  const snapshots = new Map();
  const queue = [...routes];

  async function worker() {
    while (queue.length) {
      const routePath = queue.shift();
      try {
        snapshots.set(routePath, await snapshotRoute(browser, origin, routePath));
      } catch (error) {
        failures.push(`${routePath}: ${error.message}`);
        console.error(`  FAILED ${routePath}: ${error.message}`);
      }
    }
  }

  try {
    console.log(`Prerendering ${routes.length} pages from sitemap.xml`);
    await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  } finally {
    await browser.close();
    server.close();
  }

  // Boilerplate intros repeat across lessons; describe each page with its
  // first paragraph that no other page shares.
  const paragraphUse = new Map();
  for (const snapshot of snapshots.values()) {
    for (const text of new Set(snapshot.descriptionCandidates)) {
      paragraphUse.set(text, (paragraphUse.get(text) || 0) + 1);
    }
  }

  for (const routePath of routes) {
    const snapshot = snapshots.get(routePath);
    if (!snapshot) continue;
    const candidates = snapshot.descriptionCandidates;
    const body =
      candidates.find((text) => paragraphUse.get(text) === 1) || snapshot.summary;
    const lead = snapshot.subtitle.replace(/([^.!?])$/, "$1.");
    snapshot.description = truncate(lead ? `${lead} ${body}` : body);
    const file = outputFile(routePath);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, buildPage(routePath, snapshot));
    const thin = snapshot.textLength < 300 ? "  (thin: under 300 chars)" : "";
    console.log(`  ${routePath} -> ${path.relative(BUILD_DIR, file)}${thin}`);
  }

  console.log(`Prerendered ${snapshots.size}/${routes.length} pages.`);
  if (failures.length) {
    console.error(`Prerender failed for:\n  ${failures.join("\n  ")}`);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
