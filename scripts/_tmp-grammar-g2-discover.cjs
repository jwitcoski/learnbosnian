const fs = require("fs");
const path = require("path");
const https = require("https");

const root = path.join(__dirname, "..");
const userAgent = "LearnBosnianImageBot/1.0 (educational; learnbosnian-project)";
const outDir = path.join(root, ".grok", "image-runs");
const thumbsDir = path.join(outDir, "thumbs");

function requestJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": userAgent } }, (response) => {
      let body = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => { body += chunk; });
      response.on("end", () => {
        if (response.statusCode < 200 || response.statusCode >= 300) {
          reject(new Error(`HTTP ${response.statusCode} from Commons for ${url}`));
          return;
        }
        try { resolve(JSON.parse(body)); } catch (error) { reject(error); }
      });
    }).on("error", reject);
  });
}

function download(url, destination) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destination);
    https.get(url, { headers: { "User-Agent": userAgent } }, (response) => {
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        file.close();
        try { fs.unlinkSync(destination); } catch (_) {}
        download(response.headers.location, destination).then(resolve, reject);
        return;
      }
      if (response.statusCode === 429) {
        file.close();
        try { fs.unlinkSync(destination); } catch (_) {}
        reject(new Error("HTTP 429"));
        return;
      }
      if (response.statusCode !== 200) {
        file.close();
        try { fs.unlinkSync(destination); } catch (_) {}
        reject(new Error(`HTTP ${response.statusCode} downloading ${url}`));
        return;
      }
      response.pipe(file);
      file.on("finish", () => file.close(() => resolve()));
    }).on("error", (error) => {
      file.close();
      if (fs.existsSync(destination)) fs.unlinkSync(destination);
      reject(error);
    });
  });
}

function isOpenLicense(metadata) {
  const license = `${metadata.LicenseShortName?.value || ""} ${metadata.UsageTerms?.value || ""}`.toLowerCase();
  return /cc0|public domain|cc by(?:-sa)?(?:\s|$)/.test(license);
}

function clean(value) {
  return String(value || "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function searchQuery(query) {
  const params = new URLSearchParams({
    action: "query",
    generator: "search",
    gsrsearch: query,
    gsrnamespace: "6",
    gsrlimit: "20",
    prop: "imageinfo",
    iiprop: "url|size|mime|extmetadata",
    iiurlwidth: "1600",
    format: "json",
    origin: "*"
  });
  const data = await requestJson(`https://commons.wikimedia.org/w/api.php?${params}`);
  const pages = Object.values(data.query?.pages || {});
  return pages.map((page) => {
    const info = page.imageinfo?.[0] || {};
    const metadata = info.extmetadata || {};
    const thumb320 = info.thumburl
      ? info.thumburl.replace(/\/\d+px-/, "/320px-")
      : null;
    return {
      title: page.title,
      pageUrl: `https://commons.wikimedia.org/wiki/${encodeURIComponent(page.title.replace(/ /g, "_"))}`,
      sourceUrl: info.url,
      downloadUrl: info.thumburl || info.url,
      thumbUrl: thumb320 || info.thumburl || info.url,
      mime: info.mime,
      width: info.width,
      height: info.height,
      author: clean(metadata.Artist?.value),
      license: clean(metadata.LicenseShortName?.value),
      licenseUrl: clean(metadata.LicenseUrl?.value),
      description: clean(metadata.ImageDescription?.value),
      openLicense: isOpenLicense(metadata),
      matchedQuery: query,
      review: "Confirm the subject, composition, license, and attribution before applying."
    };
  }).filter((c) => c.sourceUrl && c.openLicense && /^image\//.test(c.mime || ""));
}

function looksBadCoffee(c) {
  const blob = `${c.title} ${c.description}`.toLowerCase();
  if (/beer|pivo|can|whiteboard|clipart|gender|silhouette|icon|svg|logo/.test(blob)) return true;
  return false;
}

function looksBadHouse(c) {
  const blob = `${c.title} ${c.description}`.toLowerCase();
  if (/beer|pivo|whiteboard|clipart|gender|silhouette|icon|svg|logo/.test(blob)) return true;
  // civic-building-only without house cues — soft filter notes only; keep if Počitelj/houses
  return false;
}

async function discoverSlot(slotConfig) {
  const byTitle = new Map();
  const queryResults = {};
  for (const query of slotConfig.queries) {
    console.log(`Searching [${slotConfig.id}]: ${query}`);
    try {
      const results = await searchQuery(query);
      queryResults[query] = results.length;
      for (const c of results) {
        if (!byTitle.has(c.title)) byTitle.set(c.title, c);
        else {
          const existing = byTitle.get(c.title);
          existing.matchedQuery = `${existing.matchedQuery}; ${query}`;
        }
      }
    } catch (err) {
      queryResults[query] = `ERROR: ${err.message}`;
      console.error(`Query failed: ${query} -> ${err.message}`);
    }
    await sleep(800);
  }

  let candidates = [...byTitle.values()];
  if (slotConfig.id === "G.2a") candidates = candidates.filter((c) => !looksBadCoffee(c));
  if (slotConfig.id === "G.2b") candidates = candidates.filter((c) => !looksBadHouse(c));

  // Prefer subject keywords in ranking notes (metadata only; human picks)
  const subjectRe = slotConfig.subjectRe;
  candidates.sort((a, b) => {
    const as = subjectRe.test(`${a.title} ${a.description}`.toLowerCase()) ? 0 : 1;
    const bs = subjectRe.test(`${b.title} ${b.description}`.toLowerCase()) ? 0 : 1;
    if (as !== bs) return as - bs;
    return (b.width || 0) - (a.width || 0);
  });

  return {
    slot: slotConfig.slot,
    grammarRef: slotConfig.id,
    object: slotConfig.object,
    queries: slotConfig.queries,
    queryResults,
    source: "Wikimedia Commons API",
    createdAt: new Date().toISOString(),
    note: "Discover-only. Do not apply/download/polygonize until human selects. Metadata from Commons extmetadata; openLicense filtered to CC0/PD/CC BY/CC BY-SA.",
    candidates
  };
}

async function downloadThumbs(manifest, prefix, max = 8) {
  fs.mkdirSync(thumbsDir, { recursive: true });
  const notes = [];
  let hit429 = false;
  const top = manifest.candidates.slice(0, max);
  for (let i = 0; i < top.length; i++) {
    const c = top[i];
    const safe = c.title.replace(/^File:/, "").replace(/[^\w.\-()+]/g, "_").slice(0, 80);
    const ext = (c.mime || "").includes("png") ? "png" : (c.mime || "").includes("gif") ? "gif" : "jpg";
    const dest = path.join(thumbsDir, `${prefix}-${String(i).padStart(2, "0")}-${safe}.${ext}`);
    try {
      await download(c.thumbUrl || c.downloadUrl, dest);
      c.localThumb = path.relative(root, dest).replace(/\\/g, "/");
      notes.push(`OK ${c.localThumb}`);
      await sleep(400);
    } catch (err) {
      if (/429/.test(err.message)) {
        hit429 = true;
        notes.push(`429 skipped remaining thumbs after ${c.title}`);
        break;
      }
      notes.push(`FAIL ${c.title}: ${err.message}`);
    }
  }
  return { notes, hit429 };
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(thumbsDir, { recursive: true });

  const slots = [
    {
      id: "G.2a",
      slot: "hero",
      object: "kahva",
      outFile: "grammar-g2a-kahva-candidates.json",
      thumbPrefix: "g2a-kahva",
      queries: [
        "Bosnian coffee džezva",
        "Bosnian coffee set",
        "džezva fildžan",
        "Bosnian Coffee Džezva",
        "Turkish coffee Bosnia dzezva"
      ],
      subjectRe: /coffee|d[zž]ezva|fild[zž]an|kahv|cezve|ibrik|bakir/
    },
    {
      id: "G.2b",
      slot: "afterPattern",
      object: "kuća",
      outFile: "grammar-g2b-kuca-candidates.json",
      thumbPrefix: "g2b-kuca",
      queries: [
        "Počitelj houses",
        "Počitelj panorama",
        "Herzegovina stone houses",
        "Počitelj",
        "Počitelj Bosnia stone"
      ],
      subjectRe: /po[cč]itelj|stone house|ku[cć]a|herzegovina|kamen/
    }
  ];

  const summary = {};
  for (const slot of slots) {
    const manifest = await discoverSlot(slot);
    const thumbInfo = await downloadThumbs(manifest, slot.thumbPrefix, 8);
    manifest.thumbNotes = thumbInfo.notes;
    manifest.thumbsHit429 = thumbInfo.hit429;
    const outPath = path.join(outDir, slot.outFile);
    // Strip helper thumbUrl from final candidate objects? Keep thumbUrl as extra review aid; required fields present.
    const cleaned = {
      ...manifest,
      candidates: manifest.candidates.map(({ thumbUrl, matchedQuery, localThumb, review, ...req }) => ({
        ...req,
        matchedQuery,
        thumbUrl,
        localThumb,
        review,
        openLicense: true
      }))
    };
    // Ensure openLicense true only (already filtered)
    cleaned.candidates = cleaned.candidates.filter((c) => c.openLicense === true);
    fs.writeFileSync(outPath, JSON.stringify(cleaned, null, 2) + "\n");
    summary[slot.id] = {
      path: path.relative(root, outPath).replace(/\\/g, "/"),
      count: cleaned.candidates.length,
      queryResults: cleaned.queryResults,
      thumbsHit429: cleaned.thumbsHit429,
      top: cleaned.candidates.slice(0, 5).map((c, i) => ({
        i,
        title: c.title,
        license: c.license,
        author: c.author,
        w: c.width,
        h: c.height,
        desc: (c.description || "").slice(0, 140),
        pageUrl: c.pageUrl,
        localThumb: c.localThumb || null
      }))
    };
    console.log(`Wrote ${outPath} with ${cleaned.candidates.length} candidates`);
  }
  fs.writeFileSync(path.join(outDir, "_grammar-g2-discover-summary.json"), JSON.stringify(summary, null, 2) + "\n");
  console.log(JSON.stringify(summary, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
