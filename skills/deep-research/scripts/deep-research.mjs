#!/usr/bin/env node
// deep-research.mjs — OpenClaw deep-research CLI
// ESM, no external deps

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ANSI colors
const c = {
  green:  '\x1b[32m',
  yellow: '\x1b[33m',
  cyan:   '\x1b[36m',
  red:    '\x1b[31m',
  bold:   '\x1b[1m',
  reset:  '\x1b[0m',
};

const WORKSPACE = '/Users/cyperx/.openclaw/agents/researcher';
const ACTIVE_DIR    = path.join(WORKSPACE, 'research', 'active');
const COMPLETED_DIR = path.join(WORKSPACE, 'research', 'completed');
const REPORTS_DIR   = path.join(WORKSPACE, 'research', 'reports');

function ensureDirs() {
  for (const d of [ACTIVE_DIR, COMPLETED_DIR, REPORTS_DIR]) {
    fs.mkdirSync(d, { recursive: true });
  }
}

function slugify(query) {
  return query
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 40)
    .replace(/-+$/, '');
}

function listRuns() {
  ensureDirs();
  const active    = fs.readdirSync(ACTIVE_DIR).filter(f => f.endsWith('.json'));
  const completed = fs.readdirSync(COMPLETED_DIR).filter(f => f.endsWith('.json'));

  if (active.length === 0 && completed.length === 0) {
    console.log(`${c.yellow}No research runs found.${c.reset}`);
    return;
  }

  if (active.length > 0) {
    console.log(`\n${c.bold}${c.cyan}Active Runs${c.reset}`);
    console.log('─'.repeat(60));
    for (const f of active) {
      const id = f.replace('.json', '');
      try {
        const data = JSON.parse(fs.readFileSync(path.join(ACTIVE_DIR, f), 'utf8'));
        const learnings = (data.learnings || []).length;
        const urls = (data.visitedUrls || []).length;
        console.log(`  ${c.green}${id}${c.reset}`);
        console.log(`    Query: ${data.query || '(unknown)'}`);
        console.log(`    Depth: ${data.currentDepth || 0}/${data.maxDepth || '?'} | Learnings: ${learnings} | URLs: ${urls}`);
        console.log(`    Status: ${data.status || 'running'}`);
      } catch {
        console.log(`  ${c.green}${id}${c.reset} (unreadable)`);
      }
    }
  }

  if (completed.length > 0) {
    console.log(`\n${c.bold}${c.cyan}Completed Runs${c.reset}`);
    console.log('─'.repeat(60));
    for (const f of completed) {
      const id = f.replace('.json', '');
      try {
        const data = JSON.parse(fs.readFileSync(path.join(COMPLETED_DIR, f), 'utf8'));
        console.log(`  ${c.green}${id}${c.reset}`);
        console.log(`    Query: ${data.query || '(unknown)'}`);
        console.log(`    Learnings: ${(data.learnings || []).length} | URLs: ${(data.visitedUrls || []).length}`);
      } catch {
        console.log(`  ${c.green}${id}${c.reset} (unreadable)`);
      }
    }
  }
  console.log();
}

function showStatus(id) {
  ensureDirs();
  const activePath    = path.join(ACTIVE_DIR, `${id}.json`);
  const completedPath = path.join(COMPLETED_DIR, `${id}.json`);

  let filePath = null;
  if (fs.existsSync(activePath))    filePath = activePath;
  else if (fs.existsSync(completedPath)) filePath = completedPath;

  if (!filePath) {
    console.error(`${c.red}Run not found: ${id}${c.reset}`);
    console.error(`Check available runs with: deep-research --list`);
    process.exit(1);
  }

  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    console.log(`\n${c.bold}${c.cyan}Research Status: ${id}${c.reset}`);
    console.log('─'.repeat(60));
    console.log(`  Query:        ${data.query || '(unknown)'}`);
    console.log(`  Status:       ${data.status || 'running'}`);
    console.log(`  Depth:        ${data.currentDepth || 0} / ${data.maxDepth || '?'}`);
    console.log(`  Breadth:      ${data.breadth || '?'}`);
    console.log(`  Learnings:    ${(data.learnings || []).length}`);
    console.log(`  URLs visited: ${(data.visitedUrls || []).length}`);
    if (data.createdAt)  console.log(`  Started:      ${data.createdAt}`);
    if (data.updatedAt)  console.log(`  Updated:      ${data.updatedAt}`);

    const reportPath = path.join(REPORTS_DIR, `${id}.md`);
    if (fs.existsSync(reportPath)) {
      console.log(`  Report:       ${c.green}research/reports/${id}.md${c.reset}`);
    }
    console.log();
  } catch (e) {
    console.error(`${c.red}Failed to parse state file: ${e.message}${c.reset}`);
    process.exit(1);
  }
}

function printReport(id) {
  ensureDirs();
  const reportPath = path.join(REPORTS_DIR, `${id}.md`);
  if (!fs.existsSync(reportPath)) {
    console.error(`${c.red}Report not found: research/reports/${id}.md${c.reset}`);
    console.error(`The research may still be running. Check with: deep-research --status ${id}`);
    process.exit(1);
  }
  const content = fs.readFileSync(reportPath, 'utf8');
  console.log(content);
}

function startResearch(query, opts) {
  ensureDirs();
  const slug = slugify(query);
  const activePath = path.join(ACTIVE_DIR, `${slug}.json`);

  if (fs.existsSync(activePath) && !opts.resume) {
    console.warn(`${c.yellow}⚠️  Research already in progress for: ${slug}${c.reset}`);
    console.warn(`   Use --resume to continue, or --status ${slug} to check progress.`);
    process.exit(1);
  }

  const now = new Date().toISOString();
  const state = {
    id: slug,
    query,
    status: 'initializing',
    breadth: opts.breadth,
    maxDepth: opts.depth,
    currentDepth: 0,
    learnings: [],
    visitedUrls: [],
    createdAt: now,
    updatedAt: now,
    vault: opts.vault,
    discord: opts.discord,
  };

  fs.writeFileSync(activePath, JSON.stringify(state, null, 2));

  console.log(`\n${c.green}🔍 Starting research: ${query}${c.reset}`);
  console.log(`${c.cyan}📁 State: research/active/${slug}.json${c.reset}`);
  console.log(`${c.yellow}⏳ Research is running as an OpenClaw sub-agent. Check Discord for progress updates.${c.reset}`);
  console.log(`${c.cyan}💡 Monitor with: deep-research --status ${slug}${c.reset}\n`);
}

function vaultWrite(id) {
  const reportPath = path.join(REPORTS_DIR, `${id}.md`);
  if (!fs.existsSync(reportPath)) {
    console.error(`${c.red}Report not found: research/reports/${id}.md${c.reset}`);
    console.error(`The research may still be running. Check with: deep-research --status ${id}`);
    process.exit(1);
  }
  const scriptPath = path.join(__dirname, 'vault-write.mjs');
  try {
    execFileSync('node', [scriptPath, reportPath], { stdio: 'inherit' });
  } catch (e) {
    console.error(`${c.red}vault-write failed: ${e.message}${c.reset}`);
    process.exit(1);
  }
}

function printHelp() {
  console.log(`
${c.bold}deep-research${c.reset} — OpenClaw deep research CLI

${c.cyan}Usage:${c.reset}
  deep-research "query here" [options]
  deep-research --list
  deep-research --status <id>
  deep-research --report <id>
  deep-research --vault-write <id>

${c.cyan}Options:${c.reset}
  --breadth N       Parallel queries per level (default: 4)
  --depth N         Recursive depth (default: 2)
  --no-vault        Skip Obsidian vault output
  --no-discord      Skip Discord notification
  --resume          Resume from interrupted state if found
  --list            List all research runs (active + completed)
  --status <id>     Show status of a specific run
  --report <id>     Print the final report for a completed run
  --vault-write <id>  Manually trigger vault write for a completed run
  --help, -h        Show this help
`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  printHelp();
  process.exit(0);
}

if (args.includes('--list')) {
  listRuns();
  process.exit(0);
}

const statusIdx = args.indexOf('--status');
if (statusIdx !== -1) {
  const id = args[statusIdx + 1];
  if (!id) { console.error(`${c.red}--status requires an id${c.reset}`); process.exit(1); }
  showStatus(id);
  process.exit(0);
}

const reportIdx = args.indexOf('--report');
if (reportIdx !== -1) {
  const id = args[reportIdx + 1];
  if (!id) { console.error(`${c.red}--report requires an id${c.reset}`); process.exit(1); }
  printReport(id);
  process.exit(0);
}

const vaultWriteIdx = args.indexOf('--vault-write');
if (vaultWriteIdx !== -1) {
  const id = args[vaultWriteIdx + 1];
  if (!id) { console.error(`${c.red}--vault-write requires an id${c.reset}`); process.exit(1); }
  vaultWrite(id);
  process.exit(0);
}

// Parse options for new research
const opts = {
  breadth: 4,
  depth: 2,
  vault: true,
  discord: true,
  resume: false,
};

let query = null;
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--breadth')    { opts.breadth  = parseInt(args[++i], 10); }
  else if (a === '--depth') { opts.depth    = parseInt(args[++i], 10); }
  else if (a === '--no-vault')   { opts.vault   = false; }
  else if (a === '--no-discord') { opts.discord = false; }
  else if (a === '--resume')     { opts.resume  = true; }
  else if (!a.startsWith('-'))   { query = a; }
}

if (!query) {
  console.error(`${c.red}No query provided.${c.reset}`);
  printHelp();
  process.exit(1);
}

startResearch(query, opts);
