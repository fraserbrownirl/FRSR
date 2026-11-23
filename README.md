# FRSR

Venture studio registry: what each project is, how it is classified, and which URL goes on LinkedIn.

| File | Purpose |
|------|---------|
| [company.md](company.md) | Studio rules, frontmatter schema, link routing, agent queries |
| [projects/](projects/) | One markdown file per project (YAML frontmatter + notes) |
| [templates/project.md](templates/project.md) | Blank project card |
| [scripts/frsr-query.py](scripts/frsr-query.py) | List/filter projects and resolve `linkedin_url` |

Skills (personal, in `~/.cursor/skills/`):

- **repo-page** — publish a plain GitHub Pages article from a project repo (`docs/`).
- **bip** — 90-second HeyGen spoken script for X (does not publish a page).

When a closed project needs a public link, use **repo-page** in that repo, then register the `pages_url` here with `studio_class: private-pages`.