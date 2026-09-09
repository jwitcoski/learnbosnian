#!/usr/bin/env node
/**
 * Run the LearnBosnian editorial bot team against one Book 1 lesson.
 * Safe by default: responses are written to .grok/runs and never published.
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const config = JSON.parse(fs.readFileSync(path.join(__dirname, "grok-bots.config.json"), "utf8"));
const args = new Set(process.argv.slice(2));
const valueAfter = (flag) => {
  const index = process.argv.indexOf(flag);
  return index >= 0 ? process.argv[index + 1] : undefined;
};

const day = Number(valueAfter("--day"));
const requestedBot = valueAfter("--bot");
const manifestArg = valueAfter("--manifest");
const dryRun = args.has("--dry-run");
const exportPrompts = args.has("--export-prompts");
const chain = args.has("--chain");
const applyDraft = args.has("--apply-draft");

if (!Number.isInteger(day) || day < 1 || day > 30) {
  console.error("Usage: node scripts/grok-bots.cjs --day 22 [--bot author|bosnian-editor|...] [--dry-run] [--apply-draft]");
  process.exit(1);
}
if (applyDraft && requestedBot && requestedBot !== "author") {
  console.error("--apply-draft is only valid with --bot author.");
  process.exit(1);
}

const dayDir = path.join(root, "content", "book1", `day-${String(day).padStart(2, "0")}`);
const chapterPath = path.join(dayDir, "chapter.json");
const outlinePath = path.join(root, "content", "book1", "outline.json");
const guidePath = path.join(root, "content", "book1", "LESSON_AUTHORING_GUIDE.md");
const stylePath = path.join(root, "CONTENT-STYLE.md");

for (const file of [chapterPath, outlinePath, guidePath, stylePath]) {
  if (!fs.existsSync(file)) throw new Error(`Missing required input: ${file}`);
}

const chapter = JSON.parse(fs.readFileSync(chapterPath, "utf8"));
const outline = JSON.parse(fs.readFileSync(outlinePath, "utf8"));
const outlineDay = (outline.days || []).find((item) => item.day === day) || null;
const context = [
  `TARGET LESSON: ${day}`,
  "\nOUTLINE ENTRY:\n" + JSON.stringify(outlineDay, null, 2),
  "\nCURRENT CHAPTER JSON:\n" + JSON.stringify(chapter, null, 2),
  "\nAUTHORING GUIDE:\n" + fs.readFileSync(guidePath, "utf8"),
  "\nCONTENT STYLE:\n" + fs.readFileSync(stylePath, "utf8")
].join("\n");
const manifestContext = manifestArg
  ? "\n\nIMAGE CANDIDATE MANIFEST:\n" + fs.readFileSync(path.resolve(manifestArg), "utf8")
  : "";

const bots = config.bots.filter((bot) => !requestedBot || bot.id === requestedBot);
if (!bots.length) throw new Error(`Unknown bot: ${requestedBot}`);

function responseShape(bot) {
  if (bot.output === "integration") {
    return "Return only a JSON object shaped as { decision: \"apply\" | \"reject\" | \"needs_human_review\", candidateIndex: <number|null>, reason: <string>, command: <string|null>, checks: <string[]> }. Never return a fabricated URL or attribution.";
  }
  if (bot.output === "coordination") {
    return "Return only a JSON object shaped as { verdict: \"continue\" | \"needs_human_review\" | \"blocked\", nextActions: [{ owner: <bot or human>, action: <string>, artifact: <string> }], conflicts: <string[]>, summary: <string> }. Never publish.";
  }
  return bot.output === "draft"
    ? "Return only a JSON object shaped as { chapter: <complete chapter object>, videoScript: <markdown string>, notes: <string[]> }."
    : "Return only a JSON object shaped as { verdict: \"pass\" | \"needs_revision\", summary: <string>, issues: [{ severity: \"blocker\" | \"major\" | \"minor\", path: <JSON path>, evidence: <string>, fix: <string> }], requiredHumanChecks: <string[]> }.";
}

function buildPrompt(bot, priorResults = []) {
  const handoffs = priorResults.length
    ? "\n\nPRECEDING BOT HANDOFFS:\n" + JSON.stringify(priorResults, null, 2)
    : "";
  return [
    "You are one member of an editorial team finishing a Bosnian language-learning website.",
    bot.instruction,
    responseShape(bot),
    "Treat the supplied repository content as authoritative context. Do not claim to have checked external sources unless a URL is supplied in the context.",
    context + manifestContext + handoffs
  ].join("\n\n");
}

async function callBot(bot, priorResults) {
  const prompt = buildPrompt(bot, priorResults);
  if (dryRun || exportPrompts) return { offline: true, bot: bot.id, promptPreview: prompt.slice(0, 600) };
  if (!process.env.GROK_API_KEY) throw new Error("Set GROK_API_KEY before calling Grok, or use --dry-run.");

  const response = await fetch(config.apiUrl, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.GROK_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: process.env.GROK_MODEL || config.model,
      temperature: bot.output === "draft" ? 0.35 : 0.1,
      response_format: { type: "json_object" },
      messages: [
        { role: "system", content: "You are a precise editorial bot. Output valid JSON only." },
        { role: "user", content: prompt }
      ]
    })
  });
  if (!response.ok) throw new Error(`Grok ${response.status}: ${await response.text()}`);
  const payload = await response.json();
  const content = payload.choices?.[0]?.message?.content;
  if (!content) throw new Error(`Grok returned no message for ${bot.id}`);
  return JSON.parse(content);
}

function runDirectory() {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const dir = path.join(root, ".grok", "runs", `day-${String(day).padStart(2, "0")}-${stamp}`);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

(async () => {
  const outputDir = runDirectory();
  const manifest = { day, createdAt: new Date().toISOString(), model: process.env.GROK_MODEL || config.model, bots: bots.map((bot) => bot.id) };
  fs.writeFileSync(path.join(outputDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  const priorResults = [];
  for (const bot of bots) {
    const handoffs = chain ? priorResults : [];
    if (exportPrompts) {
      fs.writeFileSync(path.join(outputDir, `${bot.id}.prompt.md`), buildPrompt(bot, handoffs) + "\n");
      console.log(`exported prompt for ${bot.id}`);
      continue;
    }
    console.log(`${dryRun ? "previewing" : "running"} ${bot.id}`);
    const result = await callBot(bot, handoffs);
    fs.writeFileSync(path.join(outputDir, `${bot.id}.json`), JSON.stringify(result, null, 2) + "\n");
    if (chain) priorResults.push({ bot: bot.id, result });
  }

  if (applyDraft) {
    const draft = JSON.parse(fs.readFileSync(path.join(outputDir, "author.json"), "utf8"));
    if (!draft.chapter || !draft.videoScript) throw new Error("Author response must contain chapter and videoScript.");
    if (draft.chapter.status === "published") throw new Error("Refusing to apply a published chapter from a bot response.");
    draft.chapter.status = "draft";
    fs.writeFileSync(chapterPath, JSON.stringify(draft.chapter, null, 2) + "\n");
    fs.writeFileSync(path.join(dayDir, "video-script.md"), draft.videoScript.trimEnd() + "\n");
    console.log(`Applied draft to ${path.relative(root, dayDir)}. Human review is still required.`);
  }
  console.log(`Run saved to ${path.relative(root, outputDir)}`);
})().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
