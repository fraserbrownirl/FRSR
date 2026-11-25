# frsr.com content

The live site keeps its existing **hero** (boat image and social links). Do not change that in this repo.

**Under the hero**, publish [`below-banner.md`](below-banner.md) — one continuous page for humans and agents.

| Edit | File |
|------|------|
| Agent intro + method | [preamble.md](preamble.md) |
| Each project | [experience/](experience/) via console |

```bash
python3 scripts/generate-career-site.py
python3 scripts/frsr-site-preview.py   # http://127.0.0.1:8767/
```

**GitHub:** career text is in `fraserbrownirl/FRSR`. Hero: `entropy-studio-vault`.

Agent reply: [preamble.md](preamble.md). Test harness: [agent-test-format.md](agent-test-format.md).