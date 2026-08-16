# YouTube pipeline — Learn Bosnian in 30 Days

Videos for [@HowtospeakBosnian](https://www.youtube.com/@HowtospeakBosnian) after a chapter is human-approved.

There are **two** companion products:

| Product | Length | Source | Export |
|---------|--------|--------|--------|
| **Vocab supplement** (primary drill series) | 5–10 min | `vocab-video-script.md` | `export-youtube-vocab.cjs` |
| Full lesson companion (A/B + dialogue) | 8–10 min | `video-script.md` | `export-youtube.cjs` |

Vocab supplements are **not** a reload of the website lesson. Full guide: [`docs/YOUTUBE-VOCAB-SUPPLEMENT.md`](YOUTUBE-VOCAB-SUPPLEMENT.md).

## Free toolchain

| Step | Tool |
|------|------|
| Vocab scripts | `node scripts/generate-vocab-video-scripts.cjs` |
| Vocab export | `node scripts/export-youtube-vocab.cjs --day N` |
| Full companion export | `node scripts/export-youtube.cjs --day N` |
| Voice | Live speaker, [Piper TTS](https://github.com/rhasspy/piper), or CapCut TTS |
| B-roll | Rights-safe BiH drone/street (Pexels, Pixabay, Commons). Do not rip other YouTube videos. |
| Edit | **CapCut** (desktop) or **DaVinci Resolve** |
| Scale later | Remotion + FFmpeg |
| Thumbnails | CapCut / GIMP / Canva free |

## Vocab supplement steps (recommended first)

1. Chapter vocab/grammar reviewed in `chapter.json`.
2. Regenerate if needed: `node scripts/generate-vocab-video-scripts.cjs --day 1`
3. Export:

```bash
node scripts/export-youtube-vocab.cjs --day 1
```

4. Open `exports/youtube-vocab/day-01/` — `narration.md`, `cues.md`, `assets.json`, `CAPCUT.txt`.
5. Assemble in CapCut (gold text over BiH B-roll). Fixed intro, grammar beat, vocab slow×2 + definition×2, ending.
6. Upload to playlist **How to Speak Bosnian · Vocab** with `/learn/lesson/N` and B-roll credits.

## Full lesson companion steps

1. Chapter `status` → `published` (or explicitly approve a draft).
2. Run:

```bash
node scripts/export-youtube.cjs --day 1
```

3. Open `exports/youtube/day-01/` — `narration.md`, `cues.md`, `assets.json`, `CAPCUT.txt`.
4. Assemble in CapCut master template (yellow/gold text on scenic BiH stills, 6–12 min).
5. Upload to playlist **Learn Bosnian in 30 Days — Book 1** with link to `/learn/lesson/N` and image credits in the description.

Do not cut video from unreviewed `outlined` stubs.
