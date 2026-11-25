/** @typedef {{ key: string, label: string, type: string, required?: string }} FieldSpec */

/** @type {{ story_fields: FieldSpec[], project_statuses: string[] }} */
let schema = { story_fields: [], project_statuses: [] };
let pages = [];
let slug = "";
/** @type {Record<string, unknown>} */
let meta = {};
let step = 0;
let dirty = false;

const $ = (id) => document.getElementById(id);

const STORY_KEYS = new Set([
  "title",
  "structural_problem",
  "insight",
  "what_fraser_did",
  "outcome",
]);

function fields() {
  return schema.story_fields;
}

function setStatus(msg, isDirty = dirty) {
  const el = $("status");
  el.textContent = msg;
  el.classList.toggle("dirty", isDirty);
}

function fieldFilled(spec) {
  const val = meta[spec.key];
  if (typeof val === "string") return val.trim().length > 0;
  return val != null && val !== "";
}

function storyFilledCount() {
  return fields().filter((f) => f.required === "1" && fieldFilled(f)).length;
}

function updateProgress() {
  const sf = storyFilledCount();
  const st = fields().length;
  $("progress").textContent = `Fields: ${sf} / ${st}`;
  renderFieldNav();
}

function renderFieldNav() {
  const ul = $("fieldNav");
  ul.replaceChildren();
  fields().forEach((spec, i) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = spec.label;
    if (i === step) btn.classList.add("active");
    if (fieldFilled(spec)) btn.classList.add("done");
    btn.addEventListener("click", () => {
      step = i;
      renderStep();
    });
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

function bindInput(el, key) {
  el.addEventListener("input", () => {
    meta[key] = el.value;
    markDirty();
  });
}

function markDirty() {
  dirty = true;
  $("save").disabled = false;
  setStatus("Unsaved changes.", true);
  updateProgress();
}

function renderStep() {
  const list = fields();
  const spec = list[step];
  if (!spec) return;
  const { type, key, label } = spec;
  $("stepLabel").textContent = `${step + 1} / ${list.length} · ${label}`;
  $("prev").disabled = step === 0;
  $("next").disabled = step >= list.length - 1;

  const host = $("fieldHost");
  host.replaceChildren();
  const panel = document.createElement("div");
  panel.className = "field-panel";
  const h2 = document.createElement("h2");
  h2.textContent = label;
  panel.appendChild(h2);
  const help = document.createElement("p");
  help.className = "help";
  help.textContent =
    key === "title"
      ? "Index name and page H1."
      : "Saved to the page body and YAML — this is what agents read.";
  panel.appendChild(help);

  const inputHost = document.createElement("div");
  panel.appendChild(inputHost);

  if (type === "text") {
    const inp = document.createElement("input");
    inp.value = meta[key] || "";
    bindInput(inp, key);
    inputHost.appendChild(inp);
    inp.focus();
  } else if (type === "textarea") {
    const ta = document.createElement("textarea");
    ta.rows = 14;
    ta.value = meta[key] || "";
    ta.spellcheck = true;
    bindInput(ta, key);
    inputHost.appendChild(ta);
    ta.focus();
  }

  host.appendChild(panel);
  renderFieldNav();
}

async function loadSchema() {
  const res = await fetch("/api/schema");
  schema = await res.json();
}

async function loadPageList() {
  const res = await fetch("/api/pages");
  pages = (await res.json()).pages;
  const sel = $("pageSelect");
  sel.replaceChildren();
  for (const p of pages) {
    const opt = document.createElement("option");
    opt.value = p.slug;
    const s = p.story;
    const st = p.status ? ` · ${p.status}` : "";
    opt.textContent = `${p.title}${st} (${s.filled}/${s.total})`;
    sel.appendChild(opt);
  }
}

async function loadPage(newSlug) {
  if (dirty && !confirm("Discard unsaved changes?")) return;
  const data = await (await fetch(`/api/page/${newSlug}`)).json();
  slug = data.slug;
  meta = data.meta;
  dirty = false;
  step = 0;
  $("pageStatus").value = meta.status || "building";
  $("pageWebsite").value = meta.website_url || "";
  $("pageGithub").value = meta.github_url || "";
  $("save").disabled = true;
  setStatus(`Editing ${meta.title || slug}`, false);
  renderStep();
  updateProgress();
}

async function save() {
  $("save").disabled = true;
  const res = await fetch(`/api/page/${slug}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ meta }),
  });
  const data = await res.json();
  if (!res.ok) {
    setStatus(data.error || "Save failed", true);
    $("save").disabled = false;
    return;
  }
  dirty = false;
  await loadPageList();
  $("pageSelect").value = slug;
  const st = data.story;
  setStatus(`Saved. Fields ${st.filled}/${st.total}.`, false);
  updateProgress();
}

async function regenerate() {
  const res = await fetch("/api/generate", { method: "POST", body: "{}" });
  const data = await res.json();
  if (!res.ok) {
    setStatus(data.error || "Generate failed", dirty);
    return;
  }
  setStatus("Regenerated site/below-banner.md", dirty);
}

$("pageSelect").addEventListener("change", () => loadPage($("pageSelect").value));
$("pageStatus").addEventListener("change", () => {
  meta.status = $("pageStatus").value;
  markDirty();
});
$("pageWebsite").addEventListener("input", () => {
  meta.website_url = $("pageWebsite").value.trim();
  markDirty();
});
$("pageGithub").addEventListener("input", () => {
  meta.github_url = $("pageGithub").value.trim();
  markDirty();
});
$("prev").addEventListener("click", () => {
  step = Math.max(0, step - 1);
  renderStep();
});
$("next").addEventListener("click", () => {
  step = Math.min(fields().length - 1, step + 1);
  renderStep();
});
$("save").addEventListener("click", save);
$("regen").addEventListener("click", regenerate);

(async () => {
  try {
    await loadSchema();
    await loadPageList();
    if (pages.length) {
      $("pageSelect").value = pages[0].slug;
      await loadPage(pages[0].slug);
    }
  } catch (e) {
    setStatus(String(e), true);
  }
})();