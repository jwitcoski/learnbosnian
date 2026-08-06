#!/usr/bin/env node
/**
 * Build content/audio/clips.json from all chapter vocabulary + dialogue lines.
 */
const fs = require("fs");
const path = require("path");
const { buildClipsCatalog } = require("./lib/audio-clips.cjs");

const root = path.join(__dirname, "..");
const catalog = buildClipsCatalog(root);
const outPath = path.join(root, "content", "audio", "clips.json");

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(catalog, null, 2) + "\n");
console.log(`Wrote ${catalog.total} audio clips → content/audio/clips.json`);
