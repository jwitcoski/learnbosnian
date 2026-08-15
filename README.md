# Learn Bosnian in 30 Days

React website + portable Book 1 content for Scribus print and YouTube companions.

## Quick start

```bash
node scripts/sync-content.cjs
cd frontend && npm install && npm start
```

Open [http://localhost:3000/learn](http://localhost:3000/learn).

## Nightly workflow

See [docs/NIGHTLY-SOP.md](docs/NIGHTLY-SOP.md) and [CONTENT-STYLE.md](CONTENT-STYLE.md).

1. Draft `content/book1/day-NN/chapter.json`
2. Human review
3. Set `status: "published"`, sync content, deploy
4. Optional: `node scripts/export-youtube.cjs --day N`

## Exports

```bash
node scripts/export-scribus.cjs --all-drafts
node scripts/export-youtube.cjs --day 1
```

## Stack

- Frontend: React (CRA) + TypeScript + styled-components
- Content: JSON under `content/` (source of truth)
- Voice recorder: private Vite SPA (`recorder/`) → S3 uploads → lesson tap-to-play
- Backend: AWS Lambda + DynamoDB (audio API + stubs)
- **Speak Check:** learner mic → S3 → Amazon Transcribe (`bs-BA`) → Amazon Bedrock (Nova) “what to fix” coaching via API Gateway / Lambda (~$0.002–0.01 per attempt)

## Voice-overs

Tap vocab cards and dialogue lines on lesson pages to play recordings when available.

Private recording studio (shared password, iPhone Safari): see [docs/VOICE-RECORDING.md](docs/VOICE-RECORDING.md).

```bash
node scripts/sync-content.cjs
cd recorder && npm install && npm run dev
```

## YouTube

[How to speak Bosnian](https://www.youtube.com/@HowtospeakBosnian) — pipeline in [docs/YOUTUBE-PIPELINE.md](docs/YOUTUBE-PIPELINE.md).

## Progress tracker

[project_specs.md](project_specs.md)
