---
name: frsr-studio
description: >-
  Query and update the FRSR venture studio registry (company.md, projects/*.md).
  Use when classifying a repo, picking a LinkedIn URL, or adding a studio project
  card.
---

# FRSR studio

Registry repo: `fraserbrownirl/FRSR` (local path `~/FRSR`).

## Before changing anything

1. Read `company.md` at the FRSR repo root.
2. Run `python3 scripts/frsr-query.py` (or `--slug <id> --json`).

## Classify a project

| Situation | `studio_class` | LinkedIn field |
|-----------|------------------|----------------|
| Public repo + live product site | `oss-live` | `live_url` |
| Private repo + live product site | `private-live` | `live_url` |
| Public repo, no live product | `oss-repo` | README |
| Private repo, no live product | `private-pages` | `pages_url` |

Live product ≠ GitHub Pages article. Pages are for type 4 (and optional public write-ups).

## Add or edit

1. Copy `templates/project.md` → `projects/<slug>.md`
2. Fill frontmatter; set `updated`
3. `python3 scripts/frsr-query.py --slug <slug>` until no errors
4. Commit in **FRSR**, not in the product repo (unless also publishing pages there via **repo-page**)

## Related skills

- **repo-page** — `docs/` GitHub Pages in the **product** repo
- **bip** — HeyGen script only; does not update FRSR