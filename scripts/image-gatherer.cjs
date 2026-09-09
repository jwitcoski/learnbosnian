#!/usr/bin/env node
/**
 * Find openly licensed Wikimedia Commons images for a lesson and apply a
 * human-selected candidate to the chapter's image manifest.
 */
const fs = require("fs");
const path = require("path");
const https = require("https");
const { spawnSync } = require("child_process");

const root = path.join(__dirname, "..");
const args = process.argv.slice(2);
const valueAfter = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : undefined;
};
const has = (flag) => args.includes(flag);
const day = Number(valueAfter("--day"));
const slot = valueAfter("--slot") || "hero";
const query = valueAfter("--query");
const candidateIndex = Number(valueAfter("--candidate"));
const manifestArg = valueAfter("--manifest");
const allowedSlots = new Set(["hero", "conversation", "civic"]);
const userAgent = "LearnBosnianImageBot/1.0 (educational; learnbosnian-project)";

if (!Number.isInteger(day) || day < 1 || day > 30 || !allowedSlots.has(slot)) {
  console.error("Usage: node scripts/image-gatherer.cjs --day 22 --slot hero --query \"Travnik mosque\" --discover");
  console.error("Apply:  node scripts/image-gatherer.cjs --day 22 --slot hero --manifest <file> --candidate 0 --apply");
  process.exit(1);
}

function requestJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": userAgent } }, (response) => {
      let body = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => { body += chunk; });
      response.on("end", () => {
        if (response.statusCode < 200 || response.statusCode >= 300) {
          reject(new Error(`HTTP ${response.statusCode} from Commons`));
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
        fs.unlinkSync(destination);
        download(response.headers.location, destination).then(resolve, reject);
        return;
      }
      if (response.statusCode !== 200) {
        file.close();
        fs.unlinkSync(destination);
        reject(new Error(`HTTP ${response.statusCode} downloading image`));
        return;
      }
      response.pipe(file);
      file.on("finish", () => file.close(resolve));
    }).on("error", (error) => {
      file.close();
      if (fs.existsSync(destination)) fs.unlinkSync(destination);
      reject(error);
    });
  });
}

function slug(value) {
  return value.normalize("NFKD").replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "").toLowerCase().slice(0, 48);
}

function isOpenLicense(metadata) {
  const license = `${metadata.LicenseShortName?.value || ""} ${metadata.UsageTerms?.value || ""}`.toLowerCase();
  return /cc0|public domain|cc by(?:-sa)?(?:\s|$)/.test(license);
}

function clean(value) {
  return String(value || "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
}

async function discover() {
  if (!query) throw new Error("--query is required with --discover.");
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
  const candidates = pages.map((page) => {
    const info = page.imageinfo?.[0] || {};
    const metadata = info.extmetadata || {};
    return {
      title: page.title,
      pageUrl: `https://commons.wikimedia.org/wiki/${encodeURIComponent(page.title.replace(/ /g, "_"))}`,
      sourceUrl: info.url,
      downloadUrl: info.thumburl || info.url,
      mime: info.mime,
      width: info.width,
      height: info.height,
      author: clean(metadata.Artist?.value),
      license: clean(metadata.LicenseShortName?.value),
      licenseUrl: clean(metadata.LicenseUrl?.value),
      description: clean(metadata.ImageDescription?.value),
      openLicense: isOpenLicense(metadata),
      review: "Confirm the subject, composition, license, and attribution before applying."
    };
  }).filter((candidate) => candidate.sourceUrl && candidate.openLicense && /^image\//.test(candidate.mime || ""));

  const outputDir = path.join(root, ".grok", "image-runs", `day-${String(day).padStart(2, "0")}-${Date.now()}`);
  fs.mkdirSync(outputDir, { recursive: true });
  const output = { day, slot, query, source: "Wikimedia Commons API", createdAt: new Date().toISOString(), candidates };
  const outputPath = path.join(outputDir, "candidates.json");
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2) + "\n");
  console.log(`Found ${candidates.length} open-license candidates.`);
  console.log(`Review: ${path.relative(root, outputPath)}`);
  candidates.forEach((candidate, index) => console.log(`[${index}] ${candidate.title} | ${candidate.license} | ${candidate.author}`));
}

function chapterPath() {
  return path.join(root, "content", "book1", `day-${String(day).padStart(2, "0")}`, "chapter.json");
}

async function applyCandidate() {
  if (!manifestArg || !Number.isInteger(candidateIndex) || candidateIndex < 0) {
    throw new Error("--manifest and a non-negative --candidate are required with --apply.");
  }
  const manifestPath = path.resolve(manifestArg);
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const candidate = manifest.candidates?.[candidateIndex];
  if (!candidate || !candidate.openLicense) throw new Error("Candidate is missing or does not have an approved open license.");
  if (manifest.day !== day || manifest.slot !== slot) throw new Error("Manifest day/slot does not match the apply command.");

  const chapterFile = chapterPath();
  const chapter = JSON.parse(fs.readFileSync(chapterFile, "utf8"));
  const id = `${slot}-${slug(candidate.title.replace(/^File:/, ""))}`;
  const dayDir = path.dirname(chapterFile);
  const sourceDir = path.join(root, ".grok", "image-runs", "sources");
  const publicDir = path.join(root, "frontend", "public", "images", "book1");
  fs.mkdirSync(sourceDir, { recursive: true });
  fs.mkdirSync(publicDir, { recursive: true });
  const sourcePath = path.join(sourceDir, `${id}.source`);
  const outputPath = path.join(publicDir, `day-${String(day).padStart(2, "0")}-${id}.png`);
  await download(candidate.downloadUrl || candidate.sourceUrl, sourcePath);

  const polygonizer = path.join(__dirname, "polygonize-photo.py");
  const result = spawnSync("python", [polygonizer, sourcePath, outputPath], { encoding: "utf8", stdio: "inherit" });
  if (result.status !== 0) throw new Error("Polygonization failed. The chapter was not changed.");

  const entry = {
    id,
    alt: `Polygon painting based on the credited Commons photo. ${candidate.description || candidate.title.replace(/^File:/, "")}.`,
    localPath: `/images/book1/day-${String(day).padStart(2, "0")}-${id}.png`,
    sourceUrl: candidate.sourceUrl,
    pageUrl: candidate.pageUrl,
    author: candidate.author || "Unknown Commons contributor",
    license: candidate.license,
    credit: candidate.title.replace(/^File:/, "")
  };
  chapter.images = [...(chapter.images || []).filter((image) => image.id !== id), entry];
  if (slot === "hero") {
    chapter.culture = chapter.culture || {};
    chapter.culture.imageId = id;
  } else if (slot === "conversation") {
    chapter.conversation = chapter.conversation || {};
    chapter.conversation.imageId = id;
  } else {
    chapter.civicContext = chapter.civicContext || {};
    chapter.civicContext.imageId = id;
  }
  chapter.imagesNeeded = false;
  chapter.status = chapter.status === "published" ? "in_review" : chapter.status;
  fs.writeFileSync(chapterFile, JSON.stringify(chapter, null, 2) + "\n");
  console.log(`Applied ${candidate.title} to ${path.relative(root, chapterFile)} as ${id}.`);
  console.log("Run npm run sync-content, then have a human compare the polygon to the source and verify the attribution.");
}

(async () => {
  if (has("--discover")) await discover();
  else if (has("--apply")) await applyCandidate();
  else throw new Error("Choose --discover or --apply.");
})().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
