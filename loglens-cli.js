#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
let configPath = null;
let logPath = null;
let printTree = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--config') configPath = args[++i];
  else if (args[i] === '--log') logPath = args[++i];
  else if (args[i] === '--tree') printTree = true;
  else if (args[i] === '--help' || args[i] === '-h') {
    console.log(`Usage: node loglens-cli.js --config <config.json> --log <app.log> [--tree]`);
    process.exit(0);
  }
}

if (!configPath || !logPath) {
  console.error('Error: --config and --log parameters are required.');
  console.log(`Usage: node loglens-cli.js --config <config.json> --log <app.log> [--tree]`);
  process.exit(2);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) {
  console.error('Failed to read config file:', e.message);
  process.exit(2);
}

let logContent;
try {
  logContent = fs.readFileSync(logPath, 'utf8');
} catch (e) {
  console.error('Failed to read log file:', e.message);
  process.exit(2);
}

const rules = (config.elementRules || []).map(r => ({
  ...r,
  _rx: new RegExp(r.regexPattern)
}));
const tp = config.globalSettings && config.globalSettings.globalTimestampPattern;
const tsRx = tp ? new RegExp(tp) : null;

function pts(s) {
  if (!s) return null;
  const c = s.trim().replace(',', '.');
  const m = Date.parse(c);
  if (!isNaN(m)) return m;
  const n = parseFloat(c);
  return isNaN(n) ? null : n;
}

function gts(l) {
  if (!tsRx) return null;
  const m = tsRx.exec(l);
  return m ? pts(m[1] || m[0]) : null;
}

function caps(m, mp) {
  const o = {};
  for (const [i, f] of Object.entries(mp || {})) {
    const n = parseInt(i, 10);
    if (!isNaN(n) && m[n] !== undefined) o[f] = m[n];
  }
  return o;
}

const stacks = {};
const trees = {};
const allThreads = new Set();
let nodeIndex = 0;
const uid = () => 'n' + (++nodeIndex);
let errorCount = 0;

const lines = logContent.split(/\r?\n/);
let processedLines = 0;

for (const line of lines) {
  const trimmed = line.trim();
  if (!trimmed) continue;
  processedLines++;
  
  for (const r of rules) {
    const m = r._rx.exec(trimmed);
    if (!m) continue;
    
    const c = caps(m, r.captureMapping);
    const thr = (c.thread || 'default').trim();
    allThreads.add(thr);
    
    const ts = c.timestamp ? pts(c.timestamp) : gts(trimmed);
    if (!stacks[thr]) stacks[thr] = [];
    if (!trees[thr]) trees[thr] = [];
    
    const stk = stacks[thr], tr = trees[thr];
    const nd = {
      id: uid(),
      ruleId: r.id,
      ruleName: r.name,
      elementName: (c.elementName || r.name || '').trim(),
      payload: (c.payload || '').trim(),
      thread: thr,
      timestamp: ts,
      endTimestamp: null,
      duration: null,
      behavior: r.stackBehavior,
      visualStyle: r.visualStyle || {},
      events: [],
      correlationId: c.correlationId || null,
      slaThresholdMs: r.slaThresholdMs || null,
      rawLine: trimmed.length > 260 ? trimmed.slice(0, 260) + '…' : trimmed
    };
    
    if (r.name.toLowerCase().includes('error') || r.name.toLowerCase().includes('fail')) {
      errorCount++;
    }
    
    switch (r.stackBehavior) {
      case 'push':
        if (stk.length > 0) stk[stk.length - 1].events.push(nd);
        else tr.push(nd);
        stk.push(nd);
        break;
      case 'pop':
        if (stk.length > 0) {
          const o = stk.pop();
          o.endTimestamp = ts;
          o.duration = (ts != null && o.timestamp != null) ? (ts - o.timestamp) : null;
        }
        break;
      case 'inline':
        if (stk.length > 0) stk[stk.length - 1].events.push(nd);
        else tr.push(nd);
        break;
    }
    break;
  }
}

for (const s of Object.values(stacks)) s.length = 0;

const ruleDurs = {};
function collect(nodes) {
  for (const n of nodes) {
    if (n.behavior === 'push' && n.duration != null) {
      if (!ruleDurs[n.ruleId]) ruleDurs[n.ruleId] = [];
      ruleDurs[n.ruleId].push(n.duration);
    }
    if (n.events && n.events.length) collect(n.events);
  }
}
for (const tree of Object.values(trees)) collect(tree);

const ruleStats = {};
for (const [rid, durs] of Object.entries(ruleDurs)) {
  const cnt = durs.length;
  if (cnt === 0) continue;
  const sum = durs.reduce((s, x) => s + x, 0);
  const mean = sum / cnt;
  const vari = durs.reduce((s, x) => s + Math.pow(x - mean, 2), 0) / cnt;
  const stddev = Math.sqrt(vari);
  ruleStats[rid] = { mean, stddev, thresh: mean + 2 * stddev };
}

let outlierCount = 0;
let slaBreachCount = 0;
function mark(nodes) {
  for (const n of nodes) {
    const stats = ruleStats[n.ruleId];
    if (n.behavior === 'push' && n.duration != null && stats && n.duration > stats.thresh) {
      n._isOutlier = true;
      outlierCount++;
    } else {
      n._isOutlier = false;
    }
    
    if (n.behavior === 'push' && n.duration != null && n.slaThresholdMs != null && n.duration > n.slaThresholdMs) {
      n._isSlaBreach = true;
      slaBreachCount++;
    } else {
      n._isSlaBreach = false;
    }
    
    if (n.events && n.events.length) mark(n.events);
  }
}
for (const tree of Object.values(trees)) mark(tree);

function countNodes(ns) {
  return (ns || []).reduce((n, nd) => n + 1 + countNodes(nd.events), 0);
}

if (printTree) {
  console.log(JSON.stringify(trees, null, 2));
} else {
  const totalEvents = Object.values(trees).reduce((sum, tr) => sum + countNodes(tr), 0);
  const summary = {
    linesProcessed: processedLines,
    threads: [...allThreads].sort(),
    eventCount: totalEvents,
    outliers: outlierCount,
    slaBreaches: slaBreachCount,
    errors: errorCount,
    status: (outlierCount > 0 || slaBreachCount > 0 || errorCount > 0) ? 'FAIL' : 'PASS'
  };
  console.log(JSON.stringify(summary, null, 2));
}

const exitCode = (outlierCount > 0 || slaBreachCount > 0 || errorCount > 0) ? 1 : 0;
process.exit(exitCode);
