#!/usr/bin/env node
// vault-write.mjs — Write a completed deep-research report to the Obsidian vault
// ESM, no external deps

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const WORKSPACE    = '/Users/cyperx/.openclaw/agents/researcher';
const COMPLETED_DIR = path.join(WORKSPACE, 'research', 'completed');
const REPORTS_DIR   = path.join(WORKSPACE, 'research', 'reports');

const STOP_WORDS = new Set([
  'the','a','an','is','are','was','were','be','been','for','and','or','but',
  'in','on','at','to','of','with','how','what','why','when','who','about',
  'that','this','it','its','by','from','as','into','through','about','over',
]);

function topicTags(query) {
  return query
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !STOP_WORDS.has(w))
    .slice(0, 5);
}

function extractTitle(markdown) {
  const m = markdown.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : null;
}

function slugify(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 60)
    .replace(/-+$/, '');
}

function checkObsidianCli() {
  try {
    execSync('command -v obsidian-cli', { stdio: 'pipe' });
    return 'obsidian-cli';
  } catch {}
  try {
    execSync('command -v notesmd-cli', { stdio: 'pipe' });
    return 'notesmd-cli';
  } catch {}
  return null;
}

function buildFrontmatter({ id, title, now, tags, topics, refs }) {
  const tagsYaml  = tags.map(t => `  - ${t}`).join('\n');
  const topicsYaml = topics.map(t => `  - ${t}`).join('\n');
  const refsYaml  = refs.slice(0, 20).map(r => `  - "${r.replace(/"/g, '\\"')}"`).join('\n');

  return `---
id: research-${id}
title: "${title.replace(/"/g, '\\"')}"
created: ${now}
modified: ${now}
tags:
${tagsYaml}
topics:
${topicsYaml}
refs:
${refsYaml}
aliases: []
---`;
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
vault-write.mjs — Write a deep-research report to the Obsidian vault

Usage:
  node vault-write.mjs <report-path> [--tags tag1,tag2]

Examples:
  node vault-write.mjs research/reports/peter-steinberger.md
  node vault-write.mjs research/reports/my-topic.md --tags ai,tools
`);
    process.exit(0);
  }

  // Parse args
  let reportArg = null;
  let extraTags = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--tags' && args[i + 1]) {
      extraTags = args[++i].split(',').map(t => t.trim()).filter(Boolean);
    } else if (!args[i].startsWith('-')) {
      reportArg = args[i];
    }
  }

  if (!reportArg) {
    console.error('❌ No report path provided.');
    process.exit(1);
  }

  // Resolve report path (support relative to workspace or absolute)
  let reportPath = reportArg;
  if (!path.isAbsolute(reportPath)) {
    reportPath = path.join(WORKSPACE, reportPath);
  }

  if (!fs.existsSync(reportPath)) {
    console.error(`❌ Report file not found: ${reportPath}`);
    process.exit(1);
  }

  const cli = checkObsidianCli();
  if (!cli) {
    console.error('❌ obsidian-cli (or notesmd-cli) not found in PATH.');
    console.error('   Install with: npm install -g @obsidian-tools/obsidian-cli');
    console.error('   Or: npm install -g notesmd-cli');
    process.exit(1);
  }

  // Derive the run ID from the file name
  const id = path.basename(reportPath, '.md');

  // Read report
  const reportContent = fs.readFileSync(reportPath, 'utf8');

  // Read state if available
  let state = null;
  const completedPath = path.join(COMPLETED_DIR, `${id}.json`);
  if (fs.existsSync(completedPath)) {
    try {
      state = JSON.parse(fs.readFileSync(completedPath, 'utf8'));
    } catch {
      // non-fatal
    }
  }

  const query = state?.query || id.replace(/-/g, ' ');
  const visitedUrls = state?.visitedUrls || [];

  // Extract title from report markdown
  const title = extractTitle(reportContent) || query;

  const now = new Date().toISOString().replace('T', ' ').slice(0, 16);

  // Build tags
  const derived = topicTags(query);
  const tags = ['research', 'deep-research', ...derived, ...extraTags]
    .filter((v, i, a) => a.indexOf(v) === i); // dedupe

  const topics = derived.length ? derived : [id];

  const frontmatter = buildFrontmatter({
    id,
    title,
    now,
    tags,
    topics,
    refs: visitedUrls,
  });

  // Strip existing frontmatter from report if present
  let body = reportContent;
  if (body.startsWith('---')) {
    const end = body.indexOf('\n---', 4);
    if (end !== -1) {
      body = body.slice(end + 4).trimStart();
    }
  }

  const noteContent = `${frontmatter}\n\n${body}`;

  // Vault note path
  const titleSlug = slugify(title);
  const vaultNotePath = `research/${titleSlug}.md`;

  // Write to vault
  try {
    // Escape content for shell — write to temp file first, then pipe
    const tmpFile = `/tmp/vault-write-${id}-${Date.now()}.md`;
    fs.writeFileSync(tmpFile, noteContent, 'utf8');

    execSync(
      `${cli} create "${vaultNotePath}" --overwrite --content "$(cat ${tmpFile})"`,
      { stdio: 'inherit', shell: '/bin/zsh' }
    );

    fs.unlinkSync(tmpFile);

    console.log(`✅ Written to vault: ${vaultNotePath}`);
  } catch (err) {
    console.error(`❌ Failed to write to vault: ${err.message}`);
    process.exit(1);
  }
}

main().catch(err => {
  console.error(`❌ Unexpected error: ${err.message}`);
  process.exit(1);
});
