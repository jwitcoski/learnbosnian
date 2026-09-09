# Grok editorial bots

The bot team helps finish and review Book 1 lessons. It does not publish content automatically.

## Roles

- **Lesson author** creates or repairs a complete `chapter.json` and `video-script.md` from the outline.
- **Bosnian language editor** checks forms, accents, pronunciation, translations, and answers.
- **A1 pedagogy editor** checks the Book 1 locks and required lesson counts.
- **Bosnia fact checker** checks civic, culture, geography, attribution, and link claims.
- **Copy and export editor** checks `CONTENT-STYLE.md` and video-export wording.
- **Release gate** reports blockers and whether the lesson is ready for human review.
- **Open image researcher** prepares subject and search briefs. The repository image gatherer then verifies and downloads a human-selected open-license Commons candidate.
- **Image integrator** selects the best verified candidate and produces the exact integration command. With repository execution available, it may run the existing image gatherer. It cannot publish a lesson.

Every response is saved under `.grok/runs/`. Review responses are findings only. A generated chapter can be applied with an explicit flag, but it is always forced back to `draft`.

By default, bots are independent. Use `--chain` to pass each completed bot response to the next bot in the configured order. The final workflow coordinator then turns the handoffs into one action list.

## Setup

Use Node 18 or newer and set the xAI key in the shell session. Do not put the key in a file or commit it.

```powershell
$env:GROK_API_KEY = "your-key"
```

The default model is `grok-3-latest`. Override it when needed:

```powershell
$env:GROK_MODEL = "your-xai-model"
```

## Commands

Preview inputs without calling xAI:

```powershell
node scripts/grok-bots.cjs --day 22 --dry-run
```

Cursor users can export complete prompts without an API key:

```powershell
node scripts/grok-bots.cjs --day 22 --export-prompts
```

Open the generated `.prompt.md` files in `.grok/runs/` one at a time in Cursor Chat, select Grok as the model, and ask it to return the requested JSON. Cursor's included usage cannot be accessed by this Node script as an external API.

Run the full team for one lesson:

```powershell
node scripts/grok-bots.cjs --day 22
```

Run the team as a conversation with shared handoffs:

```powershell
node scripts/grok-bots.cjs --day 22 --chain
```

Run one role:

```powershell
node scripts/grok-bots.cjs --day 22 --bot bosnian-editor
```

Generate a complete draft and explicitly apply it to the lesson folder:

```powershell
node scripts/grok-bots.cjs --day 22 --bot author --apply-draft
```

After any applied draft:

1. Read the author output and all review outputs.
2. Check sources, image credits, and Bosnian with a human reviewer.
3. Run `npm run sync-content`.
4. Run the frontend tests and build.
5. Change `status` to `published` only by human decision after review.

The runner never creates image assets, invents citations, or changes `status` to `published`.

## Image gatherer

Discover candidates from Wikimedia Commons:

```powershell
node scripts/image-gatherer.cjs --day 22 --slot hero --query "Travnik Sulejmanija mosque" --discover
```

Review the printed candidates and the generated `candidates.json`. Then explicitly select one candidate by index:

```powershell
node scripts/image-gatherer.cjs --day 22 --slot hero --manifest .grok/image-runs/day-22-.../candidates.json --candidate 0 --apply
```

Have the Image integrator choose the candidate first:

```powershell
node scripts/grok-bots.cjs --day 22 --bot image-integrator --manifest .grok/image-runs/day-22-.../candidates.json
```

Give the integrator the manifest for the correct slot. It returns a candidate index and exact apply command. With Cursor's Grok, export the prompt instead and run it in Cursor:

```powershell
node scripts/grok-bots.cjs --day 22 --bot image-integrator --manifest .grok/image-runs/day-22-.../candidates.json --export-prompts
```

Valid slots are `hero`, `conversation`, and `civic`. The apply step requires an open-license record, downloads the source, runs the existing polygon image treatment, writes the image metadata into the lesson, and keeps the lesson unpublished. It does not replace a human visual comparison or attribution check. Run `npm run sync-content` after approval.
