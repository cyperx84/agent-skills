#!/usr/bin/env node

// research-flywheel.mjs — Research Flywheel CLI
// Mine conversations → deep research → store findings → digest

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";

const STATE_DIR = join(homedir(), ".openclaw/agents/researcher/research/flywheel");
const STATE_FILE = join(STATE_DIR, "state.json");
const REPORTS_DIR = join(homedir(), ".openclaw/agents/researcher/research/reports");

function loadState() {
  if (!existsSync(STATE_FILE)) {
    const defaults = {
      candidates: [],
      completed: [],
      config: {
        defaultBreadth: 4,
        defaultDepth: 2,
        topN: 3,
        notifyChannel: "1483345530363973768",
        dryRun: false,
      },
    };
    mkdirSync(STATE_DIR, { recursive: true });
    writeFileSync(STATE_FILE, JSON.stringify(defaults, null, 2));
    return defaults;
  }
  return JSON.parse(readFileSync(STATE_FILE, "utf-8"));
}

function saveState(state) {
  mkdirSync(STATE_DIR, { recursive: true });
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function slugify(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 60);
}

function normalizeTopic(topic) {
  return topic.toLowerCase().trim();
}

// ── Commands ──────────────────────────────────────────────

function cmdMine(args) {
  const since = args["--since"] || getDefaultSince();
  const agents = args["--agents"] || "all";
  const state = loadState();

  console.log(`🔄 Mining conversations since ${since}...`);
  console.log(`   Agents: ${agents}`);
  console.log(`   Completed research: ${state.completed.length} topics`);
  console.log(`   Existing candidates: ${state.candidates.length}`);
  console.log();

  // Completed topics for dedup
  const completedTopics = new Set(
    state.completed.map((c) => normalizeTopic(c.topic))
  );
  const pendingTopics = new Set(
    state.candidates
      .filter((c) => c.status === "pending")
      .map((c) => normalizeTopic(c.topic))
  );

  console.log("⚠️  Mining requires OpenClaw LCM tools (lcm_grep).");
  console.log("   Run this skill from within an OpenClaw agent session.");
  console.log();
  console.log("Mine patterns to use (see references/mine-patterns.md):");

  const patterns = [
    { label: "Research directives", pattern: "(?i)(research this|look into|investigate|deep dive on?|find out about) (.+)" },
    { label: "How/what questions", pattern: "(?i)how (does|do|can|to) (.+?)[.?]" },
    { label: "What is/are questions", pattern: "(?i)what('?s| is| are) (the )?(best|difference|state of|future of) (.+?)[.?]" },
    { label: "Evaluation language", pattern: "(?i)(compare|versus|vs\\.?|better than|alternative[s]? to) (.+)" },
    { label: "Topic mentions in build context", pattern: "(?i)(build|create|make|ship) (a |an )?(.+?)(app|tool|cli|service|platform)" },
  ];

  patterns.forEach((p) => {
    console.log(`   ${p.label}: ${p.pattern}`);
  });

  console.log();
  console.log("💡 Tip: Use the SKILL.md instructions from an OpenClaw agent to run lcm_grep with these patterns.");
  console.log("   The agent will extract topics, score them, and update state.json.");

  // Show pending candidates if any
  const pending = state.candidates.filter((c) => c.status === "pending");
  if (pending.length > 0) {
    console.log();
    console.log("📋 Current pending candidates:");
    pending
      .sort((a, b) => (b.score || 0) - (a.score || 0))
      .forEach((c, i) => {
        console.log(
          `   ${i + 1}. [${c.priority || "med"}] ${c.topic} (score: ${c.score || "?"}, source: ${c.source})`
        );
      });
  }
}

function cmdResearch(args) {
  const topic = args._[0];
  if (!topic) {
    console.error("❌ Usage: research-flywheel research <topic> [--breadth N] [--depth N]");
    process.exit(1);
  }

  const breadth = parseInt(args["--breadth"]) || 4;
  const depth = parseInt(args["--depth"]) || 2;
  const state = loadState();

  // Check if already completed
  const existing = state.completed.find(
    (c) => normalizeTopic(c.topic) === normalizeTopic(topic)
  );
  if (existing) {
    console.log(`✅ Already researched: "${topic}"`);
    console.log(`   Report: ${existing.reportPath}`);
    console.log(`   Completed: ${existing.completedAt}`);
    return;
  }

  // Check pending
  const candidate = state.candidates.find(
    (c) => normalizeTopic(c.topic) === normalizeTopic(topic) && c.status === "pending"
  );
  if (candidate) {
    candidate.status = "researching";
    candidate.researchedAt = new Date().toISOString();
    saveState(state);
  }

  const slug = slugify(topic);
  const deepResearchScript = resolve(
    homedir(),
    ".openclaw/skills/deep-research/scripts/deep-research.mjs"
  );

  console.log(`🔍 Dispatching deep research: "${topic}"`);
  console.log(`   Breadth: ${breadth}, Depth: ${depth}`);
  console.log(`   Slug: ${slug}`);
  console.log(`   Report: ${REPORTS_DIR}/${slug}.md`);
  console.log();

  if (!existsSync(deepResearchScript)) {
    console.log("⚠️  deep-research.mjs not found. Run from OpenClaw agent session.");
    console.log("   The agent will dispatch via the deep-research skill flow.");
    console.log();
    console.log("To dispatch manually from an OpenClaw agent:");
    console.log(`   sessions_send({ label: "researcher", message: "RESEARCH_DISPATCH: query: \\"${topic}\\" breadth: ${breadth} depth: ${depth}" })`);
    return;
  }

  console.log(`✅ State updated. Dispatch via OpenClaw agent for full research flow.`);
  console.log(`   Deep-research script: ${deepResearchScript}`);
}

function cmdStatus(args) {
  const topicFilter = args["--topic"] || null;
  const state = loadState();

  if (topicFilter) {
    const norm = normalizeTopic(topicFilter);
    const completed = state.completed.filter(
      (c) => normalizeTopic(c.topic).includes(norm)
    );
    const pending = state.candidates.filter(
      (c) => normalizeTopic(c.topic).includes(norm) && c.status === "pending"
    );

    console.log(`📊 Status for "${topicFilter}":`);
    console.log();
    if (completed.length > 0) {
      console.log("✅ Completed:");
      completed.forEach((c) => {
        console.log(`   ${c.topic} → ${c.reportPath} (${c.completedAt})`);
      });
    }
    if (pending.length > 0) {
      console.log("📋 Pending:");
      pending.forEach((c) => {
        console.log(`   [${c.priority}] ${c.topic} (score: ${c.score})`);
      });
    }
    if (completed.length === 0 && pending.length === 0) {
      console.log("   No matches found.");
    }
    return;
  }

  console.log("📊 Research Flywheel Status");
  console.log("═".repeat(50));
  console.log(`   Completed: ${state.completed.length}`);
  console.log(`   Pending:   ${state.candidates.filter((c) => c.status === "pending").length}`);
  console.log(`   In-flight: ${state.candidates.filter((c) => c.status === "researching").length}`);
  console.log();

  if (state.completed.length > 0) {
    console.log("✅ Completed Research:");
    state.completed.forEach((c, i) => {
      const date = c.completedAt?.split("T")[0] || "?";
      console.log(`   ${i + 1}. ${c.topic}`);
      console.log(`      ${c.reportPath} · ${date}`);
      if (c.vaultNote) console.log(`      Vault: ${c.vaultNote}`);
    });
    console.log();
  }

  const pending = state.candidates
    .filter((c) => c.status === "pending")
    .sort((a, b) => (b.score || 0) - (a.score || 0));

  if (pending.length > 0) {
    console.log("📋 Pending Candidates:");
    pending.forEach((c, i) => {
      const tags = c.tags?.length ? ` [${c.tags.join(", ")}]` : "";
      console.log(
        `   ${i + 1}. [${c.priority || "med"}] ${c.topic}${tags} (score: ${c.score || "?"})`
      );
    });
  }
}

function cmdDigest(args) {
  const since = args["--since"] || getDefaultSince();
  const output = args["--output"] || "stdout";
  const state = loadState();

  const completed = state.completed.filter(
    (c) => c.completedAt && c.completedAt >= since
  );

  if (completed.length === 0) {
    console.log("📭 No research completed since " + since);
    return;
  }

  console.log(`📝 Research Digest — since ${since}`);
  console.log("═".repeat(50));
  console.log();

  completed.forEach((c, i) => {
    console.log(`${i + 1}. **${c.topic}**`);
    if (c.digest) {
      console.log(`   ${c.digest}`);
    } else {
      console.log(`   → ${c.reportPath}`);
    }
    console.log();
  });

  if (output === "discord") {
    console.log("💡 To post to Discord, run from an OpenClaw agent session.");
    console.log("   The agent will use the message tool to deliver the digest.");
  } else if (output === "vault") {
    console.log("💡 To write to vault, run from an OpenClaw agent session.");
    console.log("   The agent will use obsidian-cli to create the digest note.");
  }
}

function cmdRun(args) {
  const dryRun = args["--dry-run"] || false;
  const auto = args["--auto"] || false;
  const topN = parseInt(args["--top"]) || loadState().config.topN || 3;

  const state = loadState();
  const pending = state.candidates
    .filter((c) => c.status === "pending")
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, topN);

  console.log("🔄 Research Flywheel — Full Cycle");
  console.log("═".repeat(50));
  console.log();
  console.log(`   Step 1: Mine — scanning for candidates`);
  console.log(`   Step 2: Filter — top ${topN} by score`);
  console.log(`   Step 3: Research — deep research each topic`);
  console.log(`   Step 4: Digest — summarize and deliver`);
  console.log();

  if (pending.length === 0) {
    console.log("📭 No pending candidates. Run 'mine' first from an OpenClaw agent.");
    return;
  }

  console.log(`📋 Top ${pending.length} candidates:`);
  pending.forEach((c, i) => {
    console.log(`   ${i + 1}. [${c.priority}] ${c.topic} (score: ${c.score})`);
  });
  console.log();

  if (dryRun) {
    console.log("🔍 --dry-run: Would research the above topics.");
    console.log("   Remove --dry-run to execute.");
    return;
  }

  if (!auto) {
    console.log("💡 Run with --auto to skip confirmations.");
    console.log("   Or dispatch from an OpenClaw agent session for the full flow.");
    return;
  }

  console.log("🚀 Auto mode: dispatching research for each topic...");
  pending.forEach((c) => {
    console.log(`   → ${c.topic}`);
  });
  console.log();
  console.log("⚠️  Auto-dispatch requires OpenClaw agent session.");
  console.log("   Use from within Researcher agent or dispatch via sessions_send.");
}

// ── Helpers ──────────────────────────────────────────────

function getDefaultSince() {
  const d = new Date();
  d.setDate(d.getDate() - 7);
  return d.toISOString().split("T")[0];
}

function parseArgs(argv) {
  const args = { _: [] };
  let i = 2; // skip node and script
  while (i < argv.length) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) {
        args[key] = next;
        i += 2;
      } else {
        args[key] = true;
        i++;
      }
    } else {
      args._.push(arg);
      i++;
    }
  }
  return args;
}

// ── Main ─────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv);
  const command = args._[0];

  switch (command) {
    case "mine":
      cmdMine(args);
      break;
    case "research":
      cmdResearch(args);
      break;
    case "status":
      cmdStatus(args);
      break;
    case "digest":
      cmdDigest(args);
      break;
    case "run":
      cmdRun(args);
      break;
    default:
      console.log("research-flywheel — Research flywheel CLI");
      console.log();
      console.log("Commands:");
      console.log("  mine [--since DATE] [--agents all|name]    Find research candidates");
      console.log("  research <topic> [--breadth N] [--depth N]  Deep research a topic");
      console.log("  status [--topic <filter>]                   Show research state");
      console.log("  digest [--since DATE] [--output stdout|discord|vault]  Summarize findings");
      console.log("  run [--dry-run] [--auto] [--top N]          Full cycle: mine → research → digest");
      break;
  }
}

main();
