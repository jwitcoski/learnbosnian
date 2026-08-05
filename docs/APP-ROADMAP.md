# App roadmap — Learn Bosnian (Expo)

## Why Expo

- Share `content/book1/**` JSON with the React website
- One TypeScript mental model
- OTA updates for lesson text without store review for copy tweaks

## v1 screens

1. **Home** — brand + continue learning
2. **Day list** — 30 tiles (published only)
3. **Lesson** — same section order as web `LessonShell`
4. **Quiz** — section quiz with local progress
5. **Dictionary** — aggregated entries

## Data

- Bundle published chapters at build time from `content/book1`
- Progress in AsyncStorage (mirror `learnbosnian-progress-v1` shape)
- No auth in v1

## Not in this pass

Native app binary, push notifications, offline audio packs.

## Suggested next milestone

After ~7 published web chapters: `npx create-expo-app`, add `packages/content` or copy JSON, port `LessonShell` section by section.
