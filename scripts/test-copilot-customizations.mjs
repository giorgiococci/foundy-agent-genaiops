import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillName = "foundry-guided-engineering";
const skillRoot = path.join(".github", "skills", skillName);
const setupRoot = path.join(
  ".copilot-tracking", "projects", "copilot-engineer-setup",
);

function read(relativePath) {
  return fs.readFileSync(path.resolve(root, relativePath), "utf8")
    .replace(/\r\n/g, "\n");
}

function frontmatter(relativePath) {
  const text = read(relativePath);
  const match = text.match(/^---\n([\s\S]*?)\n---\n/);
  assert.ok(match, `${relativePath}: missing frontmatter`);
  const fields = {};
  for (const line of match[1].split("\n")) {
    const pair = line.match(/^([a-z][a-z0-9_.-]*): (.+)$/);
    assert.ok(pair, `${relativePath}: line outside the supported subset`);
    const [, key, value] = pair;
    assert.ok(!Object.hasOwn(fields, key), `${relativePath}: duplicate key ${key}`);
    fields[key] = JSON.parse(value);
  }
  return fields;
}

function markdownFiles(directory) {
  const generated = new Set([
    ".git", "node_modules", ".venv", "venv", "bin", "obj",
    "dist", "coverage", ".azure", "artifacts",
  ]);
  return fs.readdirSync(directory, { withFileTypes: true })
    .filter((entry) => !entry.isDirectory() || !generated.has(entry.name))
    .flatMap((entry) => {
      const location = path.join(directory, entry.name);
      return entry.isDirectory()
        ? markdownFiles(location)
        : location.endsWith(".md") ? [location] : [];
    });
}

function withoutCode(text) {
  return text.replace(/^```[^\n]*\n[\s\S]*?^```[ \t]*$/gm, "");
}

function headingIds(text) {
  return new Set([...withoutCode(text).matchAll(/^#{1,6} (.+)$/gm)]
    .map((match) => match[1].toLowerCase()
      .replace(/[^\p{L}\p{N}\s_-]/gu, "").replace(/\s/g, "-")));
}

const agentFields = new Set([
  "name", "description", "target", "tools", "skills",
  "user-invocable", "disable-model-invocation",
]);

function agentProfile(file) {
  const data = frontmatter(file);
  assert.equal(data.target, "github-copilot", file);
  assert.equal(typeof data.description, "string", file);
  assert.ok(data.description.length > 10, file);
  assert.ok(read(file).length <= 30_000, `${file}: profile too long`);
  for (const key of Object.keys(data)) {
    assert.ok(agentFields.has(key), `${file}: unexpected field ${key}`);
  }
  assert.ok(!Object.hasOwn(data, "model"), `${file}: unrequested model`);
  return data;
}

test("principal: target, tools, skill, and manual invocation", () => {
  const data = agentProfile(path.join(
    ".github", "agents", "foundry-ai-engineer.agent.md",
  ));
  assert.equal(data.name, "Foundry AI Engineer");
  assert.equal(data["user-invocable"], true);
  assert.equal(data["disable-model-invocation"], true);
  assert.deepEqual(data.skills, [skillName]);
  assert.deepEqual(data.tools, [
    "read", "search", "edit", "execute", "web", "agent", "todo", "ask_user",
  ]);
});

test("structured confirmation: explicit native tool and discovery before blocking", () => {
  const principal = read(path.join(
    ".github", "agents", "foundry-ai-engineer.agent.md",
  ));
  const skill = read(path.join(skillRoot, "SKILL.md"));
  assert.match(principal, /native `ask_user`/);
  assert.match(principal, /tool-discovery facility/);
  assert.match(principal, /deferred, not absent/);
  assert.match(principal, /rejected or cancelled call is not a missing tool or approval/);
  assert.match(skill, /host must also support interactive user input/);
  assert.match(skill, /Do not silently substitute text-only confirmation/);
});

test("specialists: stable names, hidden, and no editing, shell, or delegation", () => {
  const profiles = [
    ["foundry-research-advisor", "Foundry Research Advisor", ["read", "search", "web"]],
    ["foundry-design-reviewer", "Foundry Design Reviewer", ["read", "search"]],
  ];
  for (const [file, name, tools] of profiles) {
    const data = agentProfile(path.join(".github", "agents", `${file}.agent.md`));
    assert.equal(data.name, name);
    assert.equal(data["user-invocable"], false);
    assert.equal(data["disable-model-invocation"], false);
    assert.deepEqual(data.tools, tools);
    assert.ok(!Object.hasOwn(data, "skills"));
  }
});

test("skill: discovery, directory name, and inline loading", () => {
  const file = path.join(skillRoot, "SKILL.md");
  const data = frontmatter(file);
  assert.equal(data.name, skillName);
  assert.match(data.name, /^[a-z0-9-]{1,64}$/);
  assert.equal(typeof data.description, "string");
  assert.ok(data.description.length <= 1024);
  assert.equal(data["user-invocable"], true);
  assert.equal(data["disable-model-invocation"], false);
  assert.ok(!Object.hasOwn(data, "context"));
  assert.ok(read(file).split("\n").length < 500);
});

test("language policy: English documents and default responses, with labeled historical translations", () => {
  const principal = read(path.join(
    ".github", "agents", "foundry-ai-engineer.agent.md",
  ));
  assert.match(principal, /Respond in English by default/);
  assert.match(principal, /unless the user explicitly requests another language/);
  assert.match(principal, /Keep project documents\nin English/);
  for (const specialist of ["foundry-research-advisor", "foundry-design-reviewer"]) {
    assert.match(read(path.join(".github", "agents", `${specialist}.agent.md`)),
      /Return in English:/);
  }
  const skill = read(path.join(skillRoot, "SKILL.md"));
  assert.match(skill, /Write project documents in English/);
  const questions = read(path.join(setupRoot, "questions.md"));
  assert.match(questions, /translations, not verbatim English user messages/);
});

test("eight templates available, linked, and with metadata", () => {
  const names = [
    "state", "questions", "decisions", "analysis",
    "research", "plan", "implementation", "review",
  ];
  for (const name of names) {
    const file = path.join(skillRoot, "assets", `${name}.template.md`);
    const data = frontmatter(file);
    for (const key of ["title", "description", "ms.date"]) {
      assert.equal(typeof data[key], "string", `${file}: ${key}`);
    }
    assert.ok(read(path.join(skillRoot, "SKILL.md"))
      .includes(`./assets/${name}.template.md`), `${file}: template not linked`);
  }
  const state = frontmatter(path.join(skillRoot, "assets", "state.template.md"));
  assert.equal(state.kind, "foundry-solution");
  assert.equal(state.autonomy, "single-step");
  assert.equal(state.step_status, "proposed");
});

test("Markdown: metadata, headings, and explicit code fences", () => {
  for (const absolute of markdownFiles(root)) {
    const file = path.relative(root, absolute);
    const text = read(file);
    const metadata = text.match(/^---\n([\s\S]*?)\n---\n/);
    assert.ok(metadata, `${file}: missing metadata`);
    assert.match(metadata[1], /^description: .+/m, file);
    assert.ok(text.endsWith("\n"), `${file}: missing final newline`);
    if (/^title:/m.test(metadata[1])) {
      assert.doesNotMatch(withoutCode(text), /^# /m, `${file}: duplicate title`);
    }
    const fences = [...text.matchAll(/^```([^\n]*)$/gm)];
    assert.equal(fences.length % 2, 0, `${file}: unclosed code fence`);
    fences.forEach((fence, index) => {
      if (index % 2 === 0) assert.ok(fence[1], `${file}: missing code fence language`);
    });
  }
});

test("all local Markdown links and anchors resolve", () => {
  for (const absolute of markdownFiles(root)) {
    const file = path.relative(root, absolute);
    for (const match of withoutCode(read(file)).matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
      const target = match[1];
      if (/^https?:\/\//.test(target)) continue;
      const [relative, fragment] = target.split("#");
      const resolved = relative
        ? path.resolve(path.dirname(absolute), relative.replaceAll("/", path.sep))
        : absolute;
      assert.ok(fs.existsSync(resolved), `${file}: unresolved link ${target}`);
      if (fragment) {
        assert.ok(headingIds(read(path.relative(root, resolved))).has(fragment),
          `${file}: unresolved anchor ${target}`);
      }
    }
  }
});

test("actual tracking is distinct from templates and the candidate Foundry use case", () => {
  const state = frontmatter(path.join(setupRoot, "state.md"));
  assert.equal(state.project_id, "copilot-engineer-setup");
  assert.equal(state.kind, "customization-setup");
  assert.equal(state.autonomy, "single-step");
  assert.ok([
    "proposed", "approved", "in-progress", "completed", "blocked", "cancelled",
  ].includes(state.step_status));
  for (const file of markdownFiles(path.resolve(root, setupRoot))) {
    assert.doesNotMatch(read(path.relative(root, file)), /\{\{[^}]+\}\}/,
      `${file}: unfilled placeholder`);
  }
  for (const destination of [
    "questions.md", "decisions.md", path.join("research", "analysis.md"),
    path.join("plan", "plan.md"), path.join("implementation", "log.md"),
  ]) {
    assert.ok(fs.existsSync(path.resolve(root, setupRoot, destination)), destination);
  }
});

test("Foundry register unchanged and Copilot sources separate", () => {
  const sources = [...read(path.join("docs", "research", "sources.md"))
    .matchAll(/^## S(\d{2})$/gm)].map((match) => Number(match[1]));
  assert.deepEqual(sources, Array.from({ length: 33 }, (_, index) => index + 1));
  const guide = read(path.join("docs", "engineering", "copilot-guide.md"));
  const copilotSources = [...guide.matchAll(/^### C(\d{2})$/gm)]
    .map((match) => Number(match[1]));
  assert.deepEqual(copilotSources, Array.from({ length: 10 }, (_, index) => index + 1));
});
