# Contributing to YouTube Audio Extractor

## Local Setup

1. Install Python 3.12+.
2. Clone the repository and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv/bin/activate.fish on Fish shell
   pip install -r requirements.txt
   pip install ruff pytest
   ```

## Install Git Hooks

```bash
./scripts/install-hooks.sh
```

## Local Git Setup

Run these once after cloning:

```bash
git config pull.rebase true
git config core.autocrlf input
git config push.autoSetupRemote true
git config init.defaultBranch main
```

## Build and Test Commands

```bash
ruff check .          # Lint
pytest --tb=short     # Run tests
python web_app.py     # Start web server
```

## Coding Style

- Follow PEP 8 via `ruff`.
- Keep files small and focused (200-line maximum per file).
- Use type hints everywhere.

## Branch Naming

| Prefix | Use |
|---|---|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance |
| `docs/` | Documentation |
| `refactor/` | Code restructuring |
| `ci/` | CI/CD changes |

Branch names use **kebab-case**. Never commit directly to `main` — always open a PR.

## PR Checklist

- [ ] `ruff check .` passes.
- [ ] `pytest` passes (or new tests added).
- [ ] Manual test completed for changed functionality.
- [ ] Updated docs if behavior changed.
