# FRSR

**Cursor workspace:** open this folder (`~/FRSR`) in Cursor. That is the studio workspace.

This GitHub repo (`fraserbrownirl/FRSR`) is the same files in git — the registry agents edit — not a substitute for opening the folder locally.

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

## frsr.com content

Live **frsr.com** keeps its existing hero (boat + socials). This repo produces the text **under** that hero.

| Path | Purpose |
|------|---------|
| [site/below-banner.md](site/below-banner.md) | **Generated** single-page dump (agents + humans) — publish under the hero |
| [site/preamble.md](site/preamble.md) | Agent instructions at top of dump (edit by hand) |
| [site/experience/*.md](site/experience/) | Project sources (console) |
| [site/llms.txt](site/llms.txt) | Points agents at the homepage only |

```bash
python3 scripts/frsr-experience-console.py   # edit experience pages → :8766
python3 scripts/generate-career-site.py        # rebuild site/below-banner.md
python3 scripts/frsr-site-preview.py           # hero + dump preview → :8767
```

The live **frsr.com** homepage is [`entropy-studio-vault`](https://github.com/fraserbrownirl/entropy-studio-vault) (Lovable → GitHub → Cloudflare). **studio.frsr.com** is [`fraserbrownirl.github.io`](https://github.com/fraserbrownirl/fraserbrownirl.github.io). Career copy is authored in this repo under `site/`; sync to the site repo with:

```bash
python3 scripts/sync-below-banner-to-vault.py --generate   # ~/entropy-studio-vault
cd ~/entropy-studio-vault && npm run dev
```