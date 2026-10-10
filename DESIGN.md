---
name: LogLens
description: Metadata-Driven Offline Log Analyzer & Telemetry Console
colors:
  primary: "#f0883e"
  secondary: "#58a6ff"
  tertiary: "#3fb950"
  danger: "#f85149"
  warning: "#d29922"
  purple: "#bc8cff"
  cyan: "#39c5cf"
  bg-dark: "#060a0f"
  bg-dark-low: "#0d1117"
  bg-dark-panel: "#161b22"
  bg-light: "#f2efea"
  bg-light-low: "#faf8f5"
  bg-light-panel: "#ffffff"
  text-dark: "#f0f6fc"
  text-dark-secondary: "#8b949e"
  text-light: "#18181b"
  text-light-secondary: "#52525b"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    letterSpacing: "-0.01em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    letterSpacing: "0em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "12px"
    lineHeight: 1.5
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "10.5px"
    fontWeight: 600
  mono:
    fontFamily: "'SF Mono', Menlo, Monaco, 'JetBrains Mono', 'Geist Mono', Consolas, monospace"
    fontSize: "11px"
rounded:
  sm: "6px"
  md: "8px"
  lg: "14px"
  full: "99px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#060a0f"
    rounded: "{rounded.sm}"
    padding: "6px 14px"
  button-primary-hover:
    backgroundColor: "#f5a36c"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.sm}"
    padding: "6px 12px"
  input-text:
    backgroundColor: "{colors.bg-dark-low}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.sm}"
    padding: "6px 10px"
  card-grouped:
    backgroundColor: "{colors.bg-dark-panel}"
    rounded: "{rounded.lg}"
    padding: "16px"
  sheet-modal:
    backgroundColor: "{colors.bg-dark-panel}"
    rounded: "{rounded.lg}"
    padding: "20px"
---

# Design System: LogLens

## 1. Overview

**Creative North Star: "The macOS Developer Console"**

LogLens is an offline-first, browser-native log forensics and distributed tracing console. It fuses high-density telemetry visualization (Gantt timelines, execution trees, flamegraphs, dependency topologies) with native Apple Human Interface Guidelines (HIG) craft: San Francisco typography, frosted translucent backdrops, double-layer sheet depth, and grouped card layouts.

The design strictly serves developer velocity: zero telemetry or tracking, zero cloud friction, and zero decorative bloat. Visual chrome remains unobtrusive so the user's log stream, latency bottlenecks, and anomaly signals remain the heroes of every view.

**Key Characteristics:**
- **High Information Density**: Compact 38px toolbars, horizontal timeline swimlanes, and structured data tables maximize vertical and horizontal canvas efficiency.
- **Apple HIG Refinement**: Native San Francisco font stack (`-apple-system`, `SF Pro`, `SF Mono`), 26px circular close buttons, macOS sheet elevations, and segmented pill controls.
- **Strictly Local & Calibrated Theming**: 6 distinct calibrated themes (Obsidian, Ivory, Aurora, Midnight, Forest, Crimson) built with OKLCH perceptually uniform color ramps.
- **Earned Familiarity**: Standard developer shortcuts (Alt+1 through Alt+0, Cmd/Ctrl+K Spotlight, j/k navigation) and zero invented navigation paradigms.

---

## 2. Colors

The color system combines perceptually calibrated OKLCH layout neutrals with diagnostic semantic overlays.

### Primary
- **Console Amber** (`oklch(67% 0.16 55)` / `#f0883e` in Obsidian; `oklch(60% 0.18 55)` / `#c2620a` in Ivory): Used exclusively for primary call-to-actions, active thread indicators, timeline cursor highlights, and parsing progress meters.

### Secondary
- **Diagnostics Blue** (`oklch(70% 0.12 250)` / `#58a6ff` in Obsidian; `oklch(55% 0.16 250)` / `#2563eb` in Ivory): Active view tabs, selection indicators, search match badges, and HTTP/API element tags.

### Tertiary
- **Health Green** (`oklch(68% 0.14 140)` / `#3fb950` in Obsidian; `oklch(55% 0.16 140)` / `#16a34a` in Ivory): Rule coverage progress tracks, valid syntax badges, and FS API connection status.

### Status & Accents
- **Breach Red** (`oklch(62% 0.18 25)` / `#f85149`): SLA violation flags, error log events, and delete confirmations.
- **Outlier Amber/Yellow** (`oklch(78% 0.15 85)` / `#d29922`): IQR duration anomaly badges and warning entries.
- **Trace Purple** (`oklch(65% 0.18 310)` / `#bc8cff`): Distributed trace correlation IDs and span groupings.
- **Stream Cyan** (`oklch(72% 0.11 210)` / `#39c5cf`): Live file-streaming rate and cache status tags.

### Neutrals & Theme Surfaces
- **Obsidian (Default Dark)**: Base `oklch(14% 0.015 250)`, cards `oklch(17% 0.015 250)`, borders `oklch(26% 0.015 250)`.
- **Ivory (Calibrated Light)**: Base `oklch(94.5% 0.012 55)`, cards `oklch(99% 0.003 55)`, borders `oklch(75% 0.022 55)`.
- **Aurora, Midnight, Forest, Crimson**: Full identity ramps sharing identical semantic token interfaces (`--bg-0` to `--bg-4`, `--t1` to `--t4`, `--bdr`, `--bdr-h`).

### Named Rules
**The 10% Accent Rule.** Saturated semantic accents (Amber, Blue, Green, Red) must never exceed 10% of any viewport surface area. They carry diagnostic state, not decorative wallpaper.

**The Contrast Floor Rule.** Body text, timestamps, and log payload strings must maintain ≥4.5:1 contrast against their card background across all 6 themes.

---

## 3. Typography

**Display Font:** `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro", Inter, Geist, system-ui, sans-serif`  
**Body Font:** `-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro", Inter, Geist, system-ui, sans-serif`  
**Mono Font:** `"SF Mono", Menlo, Monaco, "JetBrains Mono", "Geist Mono", Consolas, monospace`  

**Character:** Native Apple San Francisco typography delivering instant system-level rendering with zero runtime web font downloads or layout shifts.

### Hierarchy
- **Display** (700 weight, 18px, letter-spacing: -0.02em): Main modal titles and command palette headers.
- **Headline** (600 weight, 15px, letter-spacing: -0.01em): Dashboard card headers and primary section titles.
- **Title** (600 weight, 13px, letter-spacing: 0em): Summary card titles, table headers, and toolbar section labels.
- **Body** (400 weight, 12px, line-height: 1.5): Settings descriptions, inspector metadata text, and guide tooltips.
- **Label** (600 weight, 10.5px, uppercase, letter-spacing: 0.04em): Metric card badges, SLA status pills, and keyboard shortcut hints (`.cmd-kbd`).
- **Mono** (400/700 weight, 11px, line-height: 1.4): Raw log lines, timestamps, regex patterns, execution durations (`325.0ms`), and thread IDs.

### Named Rules
**The Monospace Data Rule.** Any value originating from a log file, duration calculation, capture token, or LQL query expression must render in `--mono` to preserve tabular column alignment.

---

## 4. Elevation

LogLens uses a hybrid elevation model: flat tonal layering for in-canvas timeline components, combined with Apple sheet elevation and frosted glass backdrops for overlays.

### Shadow Vocabulary
- **Surface Rest** (`box-shadow: none; border: 1px solid var(--bdr)`): Base timeline tracks, tree rows, and editor cards.
- **Grouped Card Depth** (`box-shadow: var(--shd-xs)`): Inset `.dashboard-card` and top `.stats` metric strips (`0 1px 4px rgba(0,0,0,.35)` dark / `.09` light).
- **macOS Floating HUD** (`box-shadow: var(--shd)` with `backdrop-filter: blur(14px) saturate(160%)`): Timeline floating controllers, hover tooltip inspection cards, and quick-edit popovers.
- **Apple Sheet Modal** (`box-shadow: 0 0 0 1px rgba(255,255,255,.07), 0 24px 64px -12px rgba(0,0,0,.55), 0 12px 28px -6px rgba(0,0,0,.35)` dark / `0 0 0 1px rgba(0,0,0,.08), 0 24px 64px -12px rgba(0,0,0,.22), 0 12px 28px -6px rgba(0,0,0,.12)` light): Applied to `#cmd-palette` Spotlight search and full-screen dialog modals with spring entrance easing (`cubic-bezier(0.16, 1, 0.3, 1)`).

### Named Rules
**The Frosted Backdrop Rule.** All modal backdrops and floating toolbars must pair translucent backgrounds (`rgba(..., 0.8)`) with `backdrop-filter: blur(14px) saturate(160%)` to maintain background context without visual clutter.

---

## 5. Components

### Buttons
- **Shape:** Rounded-sm (`6px`, `var(--rounded-sm)`).
- **Primary:** Background `var(--amber)`, color `var(--bg-0)`, padding `6px 14px`, font-weight 600. Hover shifts brightness, active scales to `0.98`.
- **Ghost / Tool:** Transparent background, border `1px solid var(--bdr)`, padding `4px 10px`.
- **Apple Circular Close:** `26px × 26px`, `border-radius: 50%`, centered `✕`, subtle border, hover `transform: scale(1.06)`, active press `scale(0.94)`.

### Segmented Controls & Tabs
- **Shape:** Pill wrapper with `border-radius: var(--rounded-md)` (8px), padding `2px`.
- **Active Pill:** Sliding background `var(--bg-2)` with subtle border and crisp text contrast.
- **Toggles:** Apple toggle switches (`.toggle-sw`) with 14px white drop-shadowed thumbs and spring ease transition.

### Cards & Top Bars
- **Grouped Cards:** `.dashboard-card` with `14px` border radius (`var(--rounded-lg)`), hairline borders, and double depth.
- **Top Stats Bar:** Single-row flex container with `flex-shrink: 0`, height `62px`, border `1px solid var(--bdr)`, rounded `var(--rounded-lg)`. Inner `.sc` cells with `border-right: 1px solid var(--bdr)` extending cleanly from top to bottom border.

### Spotlight Command Palette
- **Width:** `620px`, max-width `90vw`.
- **Input:** 16px search input with zero outline and seamless integration into results list.
- **Item Rows:** `8px` rounded hover/selection highlights with keyboard shortcut pills (`.cmd-kbd`).

---

## 6. Do's and Don'ts

### Do:
- **Do** preserve full vertical real estate for timeline and execution tree views by limiting summary cards exclusively to the dedicated Stats dashboard.
- **Do** wrap all interactive dialogs and HUD cards with macOS frosted blurs and double-layer shadows.
- **Do** use `flex-shrink: 0` on structural metric bars (`#stats-bar`, `#res-summary-cards`) to prevent layout squashing inside scrollable containers.
- **Do** maintain strict keyboard navigation parity (Alt+keys, Cmd+K, Escape to close drawers/modals).

### Don't:
- **Don't** add bulky decorative hero cards above the timeline canvas or execution tree.
- **Don't** use generic fluid clamp scales that distort dashboard information density.
- **Don't** import external CSS frameworks, icon libraries, or runtime web fonts; rely strictly on vanilla CSS and native San Francisco stacks.
- **Don't** use side-stripe borders or gradient text for emphasis.
