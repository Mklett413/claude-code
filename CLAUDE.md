# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is (and isn't)

This is the public companion repo for the `@anthropic-ai/claude-code` CLI. It does **not** contain the CLI source. It holds:

- `plugins/` — bundled first-party plugins (commands, agents, skills, hooks)
- `.claude-plugin/marketplace.json` — the marketplace manifest that exposes the plugins above
- `.claude/commands/` — slash commands used when developing *this* repo (`/commit-push-pr`, `/dedupe`, `/triage-issue`)
- `scripts/` — Bun/TypeScript scripts for issue triage, deduping, and lifecycle sweeping, invoked from GitHub Actions
- `.github/workflows/` — `@claude`-mention automation plus scheduled issue hygiene jobs
- `examples/` — reference hook scripts, managed-settings templates, and MDM deployment configs

There is no `package.json`, no bundler, and no test suite at the repo root. Don't add one unless asked.

## Running the scripts

Scripts use Bun directly (shebang `#!/usr/bin/env bun`) and hit the GitHub REST API via `fetch`:

```bash
GITHUB_TOKEN=<token> bun run scripts/sweep.ts --dry-run
GITHUB_TOKEN=<token> bun run scripts/auto-close-duplicates.ts
```

`scripts/issue-lifecycle.ts` is the single source of truth for label → timeout → nudge/close message mappings; `sweep.ts` consumes it. If you change lifecycle labels, update that file rather than duplicating the table.

`scripts/gh.sh` is a sandbox wrapper that only permits `issue view`, `issue list`, `search issues`, and `label list` with an allow-list of flags. The GitHub Actions jobs shell out through it so Claude can't invoke arbitrary `gh` commands. Preserve those restrictions when editing — don't widen the allow-list casually.

## Plugins

Each plugin under `plugins/<name>/` follows the standard layout documented in `plugins/README.md` (`.claude-plugin/plugin.json` + optional `commands/`, `agents/`, `skills/`, `hooks/`, `.mcp.json`).

Two things to remember when adding or renaming a plugin:

1. Add/update the corresponding entry in `.claude-plugin/marketplace.json`. The `source` path must match the directory name. If the marketplace manifest and directory drift apart, installation from this marketplace breaks silently.
2. Keep plugin versions in `plugin.json` and the marketplace entry in sync.

Plugins here are intentionally varied in shape — some ship only a skill, some only hooks, some a full command+agent bundle — so use the closest existing plugin as a template rather than a generic scaffold.

## Issue automation architecture

The `@claude` GitHub Action (`.github/workflows/claude.yml`) responds to mentions in issues, PR reviews, and comments using `anthropics/claude-code-action@v1`. Other workflows run on schedules or specific events and delegate to the `scripts/` Bun files — they share the same `GITHUB_TOKEN`-based `githubRequest` helper pattern you'll see duplicated across `sweep.ts`, `auto-close-duplicates.ts`, and `backfill-duplicate-comments.ts`. That duplication is deliberate to keep each script standalone; don't extract a shared module without a strong reason.

## Committing

Use the `/commit-push-pr` slash command for the standard path (`.claude/commands/commit-push-pr.md`). It enforces: branch off main if needed → single commit → push → open PR, all in one message. Follow that flow rather than chaining commits manually.
