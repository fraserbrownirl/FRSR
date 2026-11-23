# AGENTS.md — FRSR venture studio

Read [company.md](company.md) before adding or editing a project.

## What this repo is

A **catalog**, not product code. Each project lives in its own GitHub repo. This repo holds studio metadata: classification, public links, headline copy, and agent query rules.

## Project classes (LinkedIn URL)

| `studio_class` | Open? | Live product site? | LinkedIn points to |
|----------------|-------|--------------------|--------------------|
| `oss-live` | yes | yes | `live_url` |
| `private-live` | no | yes | `live_url` |
| `oss-repo` | yes | no | GitHub README (`readme_url` or `github`) |
| `private-pages` | no | no | `pages_url` (GitHub Pages from that repo) |

Do not guess URLs. Set fields in the project file. Run `python3 scripts/frsr-query.py` to validate.

## Adding a project

1. Copy [templates/project.md](templates/project.md) to `projects/<slug>.md`.
2. Fill frontmatter. Set `studio_class` and the URL fields that class requires.
3. Add a short body: what it is, status, repo path for agents.
4. Run `python3 scripts/frsr-query.py --slug <slug>` and fix any errors.

## Publishing a private project page

Use the **repo-page** skill in the **project repo**, not here. After Pages is live, set `pages_url` and `studio_class: private-pages` in that project's file here.

## Hard rules

- Never store API keys, tokens, or `.env` contents in this repo.
- `github` is always `owner/repo` (e.g. `fraserbrownirl/T`).
- If `live_url` and `pages_url` both exist, `studio_class` still picks which one LinkedIn uses.