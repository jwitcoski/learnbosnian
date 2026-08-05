# YouTube pipeline — Learn Bosnian in 30 Days

Companion videos for [@HowtospeakBosnian](https://www.youtube.com/@HowtospeakBosnian) after a chapter is human-approved.

## Free toolchain

| Step | Tool |
|------|------|
| Script | `node scripts/export-youtube.cjs --day N` |
| Voice | [Piper TTS](https://github.com/rhasspy/piper) (offline) or CapCut free TTS |
| Stills / B-roll | Chapter images + Pexels/Pixabay (free) |
| Edit | **CapCut** (desktop) or **DaVinci Resolve** |
| Scale later | Remotion + FFmpeg |
| Thumbnails | CapCut / GIMP / Canva free |

## Steps

1. Chapter `status` → `published` (or explicitly approve a draft).
2. Run:

```bash
node scripts/export-youtube.cjs --day 1
```

3. Open `exports/youtube/day-01/` — `narration.md`, `cues.md`, `assets.json`, `CAPCUT.txt`.
4. Assemble in CapCut master template (yellow/gold text on scenic BiH stills, 6–12 min).
5. Upload to playlist **Learn Bosnian in 30 Days — Book 1** with link to `/learn/day/N` and image credits in the description.

Do not cut video from unreviewed `outlined` stubs.
