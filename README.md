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
- Backend (optional later): AWS Lambda + DynamoDB stubs already in repo

## YouTube

[How to speak Bosnian](https://www.youtube.com/@HowtospeakBosnian) — pipeline in [docs/YOUTUBE-PIPELINE.md](docs/YOUTUBE-PIPELINE.md).

## Progress tracker

[project_specs.md](project_specs.md)
