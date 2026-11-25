# Test-agent output (optional harness)

Use when scoring sample users against frsr.com. The **live brief** is on the homepage (`preamble` in `below-banner.md`).

Thin runner prompt:

```markdown
Fetch https://frsr.com/ and read everything below the hero. Follow Method and reply with the headings under "Your answer" on that page exactly. Do not invent facts about Fraser.

[Paste sample user profile]
```

Structured checklist (maps to homepage sections):

### B. Hypothesised structural problems

2–3, each marked `[known]` or `[inferred]`, at least one the user has not named. End with: *Correct me if any of these are wrong.*

### C. Insight scan

Table: **every** project | insight (one line) | which problem or `none`.

### D. What Fraser did → what he would do here

Per problem (max 3), per strongest insight (max 2): project, what he did, what he would do here `[inference]`, reasoning, lesson (one transferable sentence).

### E. Combined read

How insights compose.

### F. First experiment

Hypothesis, build/test, success signal, fail signal, ~two-week scope.

### G. Limits and source check

What the page does not support; which URL was read; whether project text was present.

### H. Ask Fraser today

One forwardable question.

**Pass signals:** full insight table; at least one `[inference]` problem; lessons present; did vs would separated; one Fraser question.
**Fail signals:** only Amplify/Bursar cited; essay with no table; no `[inference]` labels; invented capabilities.