# Repository Guidelines

## Project Structure & Module Organization

This repository is a content-creation workspace for AI tutorial visuals, not a single application. Main outputs are static HTML decks and generated assets.

- `deck/` contains the original full-screen HTML presentation, shared `style-claymation.css`, `fit.js`, character assets, and `_preview/` screenshots.
- `claude-code-deepseek/` is a standalone video/deck project. Its source script is `字幕.md`; generated deck versions live in `deck/`, `deck_v2/`, `deck_v3/`, etc.
- `claude-code-deepseek/CLAUDE.md` defines project-specific rules, especially the fixed character identity.
- `.claude/skills/` and `.agents/skills/` hold local agent skills. Treat these as tooling/vendor content unless explicitly updating skills.

## Build, Test, and Development Commands

There is no package manifest or build pipeline at the repository root. Decks are static files.

- Open a deck directly: `claude-code-deepseek/deck_v3/index.html`
- Search files: `rg --files`
- Inspect text: `rg "DeepSeek" claude-code-deepseek`
- Generate previews with a browser/headless Chromium when changing layouts; save screenshots under the deck’s `preview/` or `_preview/` directory.

## Coding Style & Naming Conventions

Use concise static HTML/CSS/JS. Keep Chinese display text in HTML so generated images do not need to render exact Chinese. Prefer existing claymation deck styles and 1920x1080 slide dimensions. Name new deck iterations monotonically, for example `deck_v4/`, and do not overwrite earlier versions unless requested.

Use UTF-8 for Chinese files. Keep comments short and only where they clarify layout or generation constraints.

## Testing Guidelines

No automated test suite exists. Verification is visual:

- Open the changed `index.html`.
- Check keyboard/click navigation.
- Export or capture every slide.
- Confirm no text overflow, missing assets, or unreadable Chinese.

For `claude-code-deepseek`, validate content against `字幕.md`; do not add unprovided command details, numbers, or claims.

## Commit & Pull Request Guidelines

Recent commits use short Conventional Commit-style prefixes, such as `feat:` and `chore:`. Continue that pattern: `feat: add deck_v4 previews`, `chore: update character guide`.

Pull requests should include a brief description, affected directories, and screenshots or preview paths for visual changes. Mention whether existing decks were preserved or intentionally replaced.

## Agent-Specific Instructions

Before editing inside `claude-code-deepseek/`, read `claude-code-deepseek/CLAUDE.md`. The fixed character reference is `character/reference-fixed.png`; older purple hoodie assets are historical only.
