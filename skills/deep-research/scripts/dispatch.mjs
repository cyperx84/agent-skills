#!/usr/bin/env node
/**
 * dispatch.mjs — Research dispatch helper
 * Usage: node dispatch.mjs "query here" [--breadth N] [--depth N] [--notify-channel CHANNEL_ID] [--requested-by AGENT]
 *
 * Prints the RESEARCH_DISPATCH message to stdout (paste into sessions_send).
 * Appends a pending entry to: /Users/cyperx/.openclaw/agents/researcher/research/pending.json
 */

import { readFileSync, writeFileSync } from 'fs';
import { randomBytes } from 'crypto';

const PENDING_FILE = '/Users/cyperx/.openclaw/agents/researcher/research/pending.json';

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node dispatch.mjs "query" [--breadth N] [--depth N] [--notify-channel ID] [--requested-by NAME]');
  process.exit(1);
}

// Parse args
let query = null;
let breadth = 4;
let depth = 2;
let notifyChannel = null;
let requestedBy = 'claw';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--breadth') breadth = parseInt(args[++i], 10);
  else if (args[i] === '--depth') depth = parseInt(args[++i], 10);
  else if (args[i] === '--notify-channel') notifyChannel = args[++i];
  else if (args[i] === '--requested-by') requestedBy = args[++i];
  else if (!query) query = args[i];
}

if (!query) {
  console.error('Error: query is required');
  process.exit(1);
}

// Generate slug id
const slug = query
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-+|-+$/g, '')
  .slice(0, 40) + '-' + randomBytes(3).toString('hex');

const entry = {
  id: slug,
  query,
  breadth,
  depth,
  notifyChannel: notifyChannel || null,
  requestedBy,
  dispatchedAt: new Date().toISOString(),
  status: 'pending',
};

// Append to pending.json
let pending = [];
try {
  pending = JSON.parse(readFileSync(PENDING_FILE, 'utf8'));
} catch {}
pending.push(entry);
writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2));

// Print dispatch message to stdout
const channelLine = notifyChannel ? `notify_channel: ${notifyChannel}` : '';
const msg = `RESEARCH_DISPATCH:
query: "${query}"
breadth: ${breadth}
depth: ${depth}
${channelLine ? channelLine + '\n' : ''}requestedBy: ${requestedBy}
dispatchId: ${slug}`;

console.log(msg);
