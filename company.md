# FRSR company registry

Agents: **query projects by reading YAML frontmatter** in `projects/*.md`. This file defines the schema and link rules. The body under each project file is human notes; agents should treat frontmatter as authoritative for links and classification.

## Studio

- **Operator:** Fraser Brown (frsr.com)
- **GitHub org/user:** `fraserbrownirl`
- **This repo:** `fraserbrownirl/FRSR` — venture studio index only

## Four project types

User-facing names map to `studio_class`:

1. **Open source + live product** → `oss-live` → LinkedIn **`live_url`**
2. **Closed source + live product** → `private-live` → LinkedIn **`live_url`**
3. **Open source + no live product** → `oss-repo` → LinkedIn **README** (`readme_url` or derived from `github`)
4. **Closed source + no live product** → `private-pages` → LinkedIn **`pages_url`** (GitHub Pages article in that repo, usually `docs/`)

“Live product” means a deployed site or app strangers can use, not the GitHub repo and not a studio article page. A public repo may still have a `pages_url` for a write-up; for `oss-repo`, LinkedIn stays on the README unless you change `studio_class`.

## Frontmatter schema

Every file in `projects/` must start with:

```yaml
---
slug: kebab-case-id
name: Display Name
github: fraserbrownirl/repo-name
visibility: public | private
studio_class: oss-live | private-live | oss-repo | private-pages
status: active | prototype | parked | retired

# Required depending on studio_class:
live_url: https://...          # oss-live, private-live
pages_url: https://...         # private-pages (and optional note for oss)
readme_url: https://github.com/owner/repo#readme  # optional override for oss-repo

headline: One line for LinkedIn or cards
tags: [telegram, agents]
updated: YYYY-MM-DD
---
```

Optional:

```yaml
product: Short product name if different from name
pages_repo_path: docs           # hint for repo-page skill
linkedin_url: https://...       # only if manually overriding computed URL
notes_public: false             # if true, body may be quoted externally
```

### Computed `linkedin_url`

If `linkedin_url` is omitted, agents and `scripts/frsr-query.py` compute:

| `studio_class` | URL |
|----------------|-----|
| `oss-live` | `live_url` |
| `private-live` | `live_url` |
| `oss-repo` | `readme_url` else `https://github.com/{github}#readme` |
| `private-pages` | `pages_url` |

## Agent queries

**List all projects**

```bash
python3 scripts/frsr-query.py
```

**One project**

```bash
python3 scripts/frsr-query.py --slug t-rex
```

**Filter**

```bash
python3 scripts/frsr-query.py --class oss-live
python3 scripts/frsr-query.py --tag telegram
python3 scripts/frsr-query.py --visibility private
```

**JSON (for tools)**

```bash
python3 scripts/frsr-query.py --json
```

**Ripgrep frontmatter only**

```bash
rg '^studio_class:' projects/
rg '^slug: t-rex' projects/ -l
```

When updating a project in its code repo, update the matching `projects/<slug>.md` here in the same session if classification or URLs changed.

## Projects index

Maintained in `projects/`. Run `python3 scripts/frsr-query.py` for the current list with resolved LinkedIn URLs.