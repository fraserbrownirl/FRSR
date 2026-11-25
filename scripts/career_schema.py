"""Shared schema for frsr.com career / experience pages."""

from __future__ import annotations

PROJECT_STATUSES: tuple[str, ...] = (
    "completed",
    "live",
    "building",
)

STORY_KEYS: tuple[str, ...] = (
    "title",
    "structural_problem",
    "insight",
    "activities",
    "what_fraser_did",
    "transfer_principle",
    "outcome",
)

STORY_FIELDS: tuple[dict[str, str], ...] = (
    {"key": "title", "label": "Title", "type": "text", "group": "story", "required": "1"},
    {
        "key": "structural_problem",
        "label": "Structural problem",
        "type": "textarea",
        "group": "story",
        "required": "1",
    },
    {"key": "insight", "label": "Insight", "type": "textarea", "group": "story", "required": "1"},
    {
        "key": "activities",
        "label": "Activities",
        "type": "textarea",
        "group": "story",
        "required": "0",
    },
    {
        "key": "what_fraser_did",
        "label": "What Fraser did",
        "type": "textarea",
        "group": "story",
        "required": "1",
    },
    {
        "key": "transfer_principle",
        "label": "Transfer principle",
        "type": "textarea",
        "group": "story",
        "required": "0",
    },
    {"key": "outcome", "label": "Status", "type": "textarea", "group": "story", "required": "1"},
)

# Optional YAML (sidebar in console); not part of the five-field agent read.
SIDEBAR_KEYS: tuple[str, ...] = ("status", "website_url", "github_url")

FRONTMATTER_FIELDS: tuple[dict[str, str], ...] = STORY_FIELDS

REQUIRED_KEYS = set(STORY_KEYS) | {"status"}


def infer_project_status(meta: dict) -> str:
    period = str(meta.get("period") or "").lower()
    if "present" in period:
        return "live"
    title = str(meta.get("title") or "").lower()
    outcome = str(meta.get("outcome") or "").lower()
    if any(w in outcome for w in ("building", "in development", "prototype")):
        return "building"
    if meta.get("status") in PROJECT_STATUSES:
        return str(meta["status"])
    return "completed"


def _filled(meta: dict, key: str) -> bool:
    val = meta.get(key)
    if isinstance(val, list):
        return len(val) > 0
    if isinstance(val, str):
        return bool(val.strip())
    return val is not None and val != ""


def story_completion(meta: dict) -> tuple[int, int]:
    required = [f["key"] for f in STORY_FIELDS if f.get("required") == "1"]
    total = len(required)
    filled = sum(1 for key in required if _filled(meta, key))
    return filled, total


def completion_score(meta: dict) -> tuple[int, int]:
    return story_completion(meta)


def prune_meta(meta: dict) -> dict:
    """Keep only fields we still use."""
    allowed = set(STORY_KEYS) | set(SIDEBAR_KEYS)
    out: dict = {}
    for k, v in meta.items():
        if k not in allowed or v is None:
            continue
        if k in ("website_url", "github_url") and not str(v).strip():
            continue
        out[k] = v
    if not out.get("status"):
        out["status"] = infer_project_status(meta)
    return out


LEGACY_KEYS = (
    "role",
    "period",
    "industry",
    "outcome_status",
    "transfer_conditions",
    "relevant_when",
    "evidence",
    "moves",
)