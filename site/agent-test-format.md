# Test-agent output (optional harness)

Use when scoring sample users against frsr.com. The **live brief** is on the homepage (`preamble` in `below-banner.md`).

Thin runner prompt:

```markdown
Fetch https://frsr.com/ and read everything below the hero. Follow Method and reply with the headings under "Your answer" on that page exactly. Do not invent facts about Fraser. Do not output an insight-scan table or a Limits section.

[Paste sample user profile]
```

Structured checklist (for scoring only — not extra sections in the user-facing reply):

### B. Hypothesised structural problems

2–3, `[known]` / `[inferred]`, one line each. End with correction invite.

### C. (Internal) Insight scan

Evaluator only: did the agent read beyond Amplify/Bursar/reintro? No table required in the published answer.

### D. What Fraser did → what he would do here

Per match: **Lesson** first (bold), then insight / did / inference / reasoning bullets. Max 3 problems × 2 projects.

### E. Combined read

≤4 lines.

### F. First experiment

Hypothesis, do, success, fail.

### G. Ask Fraser today

One question.

**Pass signals:** Lesson-first blocks; full-page read visible in match choices; `[inference]` labels; one Fraser question; no scan table; no Limits nanny section.
**Fail signals:** Essay walls; 23-row table; limits lecture; only famous projects used.