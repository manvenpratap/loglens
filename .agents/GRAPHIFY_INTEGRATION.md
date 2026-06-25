# Graphify — LogLens Integration Guide

> **Status:** Attached ✅  
> **Skill:** `claude-d3js-skill` (d3.js visualization)  
> **Purpose:** This document defines how and where Graphify (d3.js-powered data visualization) is used in LogLens across all roadmap phases.

---

## What Graphify Means Here

"Graphify" in the LogLens context refers to the capability of generating rich, interactive **graph and chart visualizations** from parsed log data. It is powered by the `claude-d3js-skill`, which provides d3.js patterns for:
- Force-directed graphs (transaction dependency diagrams)
- Histograms and bar charts (latency distributions)
- Heatmaps (frequency/time analysis)
- Swimlane timelines (multi-thread Gantt)
- Chord diagrams (cross-thread correlation)

> **Important constraint:** LogLens is zero-dependency. D3.js will be loaded via **ES Module CDN import** (`import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7/+esm'`) only when a Graphify feature is activated. This is a dynamic import, so it does not affect startup time or offline usage. The core parse engine never requires D3.

---

## Graphify Integration Points by Phase

### Phase 1 — Foundation (SVG Export)
**Feature:** SVG/PNG export of the Gantt chart  
**D3 usage:** Reconstruct current Gantt layout as SVG using `d3.scaleLinear()` for time axis positioning  
**Pattern:** Headless rendering (no DOM manipulation — generate SVG string)

```javascript
// Phase 1: Gantt → SVG export
// Uses d3 scales to match existing GR.render() layout math
async function ganttToSvg(tree, totalMs) {
  const d3 = await import('https://cdn.jsdelivr.net/npm/d3@7/+esm');
  const xScale = d3.scaleLinear().domain([0, totalMs]).range([0, 900]);
  // ... render rects as SVG elements
}
```

---

### Phase 2 — Intelligence (Core Graphify Features)

#### 2a. Per-Rule Latency Histogram
**Trigger:** User clicks a rule name in the new Stats panel  
**Chart type:** Bar chart (duration buckets vs count)  
**D3 patterns:** `d3.scaleBand()`, `d3.scaleLinear()`, `d3.bin()` for bucketing  

```javascript
// §JS-21 STATS ENGINE — histogram per rule
function renderHistogram(durations, containerEl) {
  // durations: number[] in milliseconds
  // Buckets auto-computed via d3.bin()
  const bins = d3.bin().thresholds(20)(durations);
  // ... render as bar chart with amber fill matching LogLens theme
}
```

**Styling:** Use LogLens design tokens (`--amber`, `--bg-1`, `--bdr`) via CSS variables in the SVG/canvas.

---

#### 2b. Transaction Dependency Graph ⭐ (Primary Graphify Use Case)
**Trigger:** New "Graph" view tab added alongside Gantt/Tree/Split  
**Chart type:** Force-directed network graph  
**D3 patterns:** `d3.forceSimulation()`, `d3.forceLink()`, `d3.forceManyBody()`

**Data model:**
```javascript
// Built from parsed trees after each parse
function buildDependencyGraph(trees, activeThr) {
  const nodes = [];  // { id: elementName, ruleId, color }
  const links = [];  // { source: elementName, target: elementName, duration }
  // For each push→pop pair, add a node + link to its parent
  // Cross-thread links added when correlationId matches (Phase 2 feature)
  return { nodes, links };
}
```

**Visual encoding:**
- Node size → total self-time (larger = slower)
- Node color → rule's `accentColor`
- Edge width → average duration of the call
- Red edge → edge where child > 80% of parent duration (hotspot)

---

#### 2c. Swimlane Multi-Thread Gantt
**Trigger:** Activated by clicking "All Threads" toggle in Timeline tab  
**Chart type:** Multi-row horizontal Gantt (Canvas 2D preferred for performance)  
**D3 patterns:** `d3.scaleLinear()` for shared X-axis, `d3.zoom()` for zoom/pan

**Architecture note:** This replaces the current `innerHTML` Gantt rendering. Use a `<canvas>` element; d3 handles only the data → pixel math, not DOM manipulation.

```javascript
// §JS-15b CANVAS GANTT RENDERER (Phase 2 upgrade)
function renderCanvasGantt(allThreadTrees, canvas) {
  const ctx = canvas.getContext('2d');
  const xScale = d3.scaleLinear()
    .domain([globalStartMs, globalEndMs])
    .range([labelColWidth, canvas.width]);
  // Draw each thread as a horizontal lane
  // Use canvas.addEventListener('wheel') for zoom
}
```

---

#### 2d. Frequency Heatmap
**Trigger:** New "Heatmap" toggle in Stats panel  
**Chart type:** Heatmap (time bucket × rule name → event count)  
**D3 patterns:** `d3.scaleSequential(d3.interpolateYlOrRd)` for color encoding

**Data shape:**
```javascript
// { rule: "Transaction Begin", bucket: "00:05", count: 42 }
```

---

### Phase 3 — Collaboration (Report Embeds)

Graphify charts are serialized as **self-contained SVG strings** and embedded in:
- PDF reports (via Print API)
- Standalone HTML reports
- Session files (.lls format)

Use `new XMLSerializer().serializeToString(svgElement)` to capture rendered d3 SVG.

---

### Phase 4 — Integration (Live Graphs)

**Real-time dependency graph:** As WebSocket events arrive, update the force simulation incrementally using `simulation.nodes(newNodes).force('link').links(newLinks); simulation.alpha(0.3).restart()`.

---

## Graphify Coding Rules

When implementing any Graphify feature in `loglens.html`:

1. **Lazy-load D3**: Always use `const d3 = await import('https://cdn.jsdelivr.net/npm/d3@7/+esm')` inside an async function. Never import at module top level.

2. **Respect zero-dep offline mode**: If D3 fails to load (network unavailable), fall back gracefully to the existing innerHTML render or show a toast: `toast('Graphify unavailable offline — using basic renderer', 'warn')`.

3. **Match LogLens color tokens**: Read CSS variables at render time:
   ```javascript
   const amber = getComputedStyle(document.documentElement)
     .getPropertyValue('--amber').trim();
   ```

4. **Canvas for performance, SVG for export**: Use Canvas 2D for interactive live charts (>1000 data points). Use SVG for exported reports (vector quality, no resolution issues).

5. **New section comment**: Add Graphify features under `§JS-22 GRAPHIFY ENGINE` in `loglens.html`.

6. **Read the skill**: Before implementing any new chart type, read `/Users/manvenpratapsingh/.gemini/config/skills/claude-d3js-skill/SKILL.md` for the exact d3 pattern to follow.

---

## Implementation Checklist (ordered by priority)

- [ ] **Phase 1:** SVG/PNG Gantt export (use d3 scales, no DOM manipulation)
- [ ] **Phase 2a:** Rule latency histogram (bar chart, d3.bin() bucketing)
- [ ] **Phase 2b:** Transaction dependency graph (force-directed, core Graphify feature)
- [ ] **Phase 2c:** Swimlane Gantt with Canvas 2D + d3 zoom/pan
- [ ] **Phase 2d:** Frequency heatmap (d3 color scale over time buckets)
- [ ] **Phase 3:** SVG serialization for report embedding
- [ ] **Phase 4:** Real-time incremental graph updates (force simulation hot reload)

---

*Attached: 2026-06-25*  
*Integration Skill: `claude-d3js-skill`*  
*Primary D3 source: `https://cdn.jsdelivr.net/npm/d3@7/+esm` (lazy-loaded)*
