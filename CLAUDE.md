# CLAUDE.md — YouTube Audio Extractor

## Project Overview

YouTube Audio Extractor is a Python tool that extracts audio from YouTube videos and playlists. It provides both a Flask web interface and a command-line tool with features including bitrate control, automatic file splitting, and chapter-based audio extraction.

- **Language / Runtime**: Python 3.12
- **Framework**: Flask 3.0 (web UI), Click 8 (CLI)
- **Architecture**: Layered — CLI entry points → extractor core → Flask API
- **Package / Namespace**: `youtube_audio_extractor`

---

## Required Skills — ALWAYS Invoke These

These skills **must** be invoked when the relevant situation arises. Never skip them.

| Situation | Skill |
|-----------|-------|
| Before any new feature or screen | `superpowers:brainstorming` |
| Planning multi-step changes | `superpowers:writing-plans` |
| Writing or fixing core logic | `superpowers:test-driven-development` |
| First sign of a bug or failure | `superpowers:systematic-debugging` |
| Before completing a feature branch | `superpowers:requesting-code-review` |
| Before claiming any task done | `superpowers:verification-before-completion` |
| Working on UI / frontend | `frontend-design:frontend-design` |
| After implementing — reviewing quality | `simplify` |

---

## Architecture

```
yt-audio-extractor/
├── youtube_audio_extractor/   ← Core extraction logic
├── api/                       ← Flask REST API endpoints
├── web/                       ← Static web UI assets
├── web_app.py                 ← Flask app entry point
├── youtube_audio_extractor.py ← CLI entry point
├── requirements.txt           ← Python dependencies
└── scripts/                   ← Dev tooling scripts
```

### Layer Rules

- `youtube_audio_extractor/` must never import from `api/` or `web/`
- `api/` imports from `youtube_audio_extractor/` only
- CLI scripts import from `youtube_audio_extractor/` only

---

## Coding Conventions

- [ ] All functions are **typed** with Python type hints
- [ ] Functions are **pure** where possible — no hidden side effects
- [ ] No hardcoded strings — use constants or config
- [ ] `ruff` enforced on every commit via pre-commit hook

---

## Engineering Principles

### File Size
- **200-line maximum per file** — extract a class, function, or module when approaching the limit

### DRY · SOLID · KISS · YAGNI
- Extract shared logic into named utilities; never copy-paste
- Single Responsibility: one class/function does one thing
- Don't add features not yet needed
- Delete dead code immediately

### TDD
- Write the failing test first, make it pass, then refactor
- Test names describe behaviour: `"should reject invalid youtube url"`
- One assertion per test — keep tests focused and readable

### Commit hygiene
- Follow Conventional Commits: `feat: ...` / `fix: ...` / `chore: ...`
- The `commit-msg` hook enforces this automatically

---

## Build Commands

```bash
pip install -r requirements.txt    # Install dependencies
ruff check .                       # Lint
pytest --tb=short                  # Run tests
ruff check . && pytest --tb=short  # Smoke check (CI and pre-commit)
python web_app.py                  # Start web server
```

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file — project conventions and session startup |
| `version.txt` | Semantic version (MAJOR.MINOR.PATCH) |
| `.github/workflows/` | CI, release, and Pages automation |
| `.githooks/` | Pre-commit and commit-msg hooks |
| `scripts/install-hooks.sh` | One-time hook installer |
| `scripts/setup-repo.sh` | Branch protection setup (run once after first CI) |

---

## Starting a New Session

1. Read this file
2. Run `ruff check . && pytest --tb=short` to confirm everything passes
3. Invoke `superpowers:brainstorming` before touching any feature
4. Follow the Required Skills table — every skill is mandatory, not optional
