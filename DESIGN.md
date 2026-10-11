---
name: LogLens
description: Offline-First High-Density Log Forensics & Telemetry Console
colors:
  primary: "#f0883e"
  secondary: "#58a6ff"
  tertiary: "#3fb950"
  danger: "#f85149"
  warning: "#d29922"
  purple: "#bc8cff"
  cyan: "#39c5cf"
  bg-dark: "#060a0f"
  bg-dark-surface: "#161b22"
  bg-dark-border: "#30363d"
  bg-light: "#f2efea"
  bg-light-surface: "#ffffff"
  bg-light-border: "#d0d7de"
  text-dark: "#f0f6fc"
  text-dark-muted: "#8b949e"
  text-light: "#18181b"
  text-light-muted: "#52525b"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro', Inter, Geist, system-ui, sans-serif"
    fontSize: "10.5px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.04em"
  mono:
    fontFamily: "'SF Mono', Menlo, Monaco, 'JetBrains Mono', 'Geist Mono', Consolas, monospace"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "normal"
rounded:
  xs: "2px"
  sm: "4px"
  md: "6px"
  lg: "10px"
  xl: "14px"
  full: "9999px"
spacing:
  xxs: "2px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg-dark}"
    rounded: "{rounded.md}"
    padding: "6px 14px"
  button-primary-hover:
    backgroundColor: "#f5a36c"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.md}"
    padding: "4px 10px"
  input-text:
    backgroundColor: "{colors.bg-dark-surface}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.md}"
    padding: "6px 10px"
  nav-pill:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.md}"
    padding: "4px 12px"
  card-grouped:
    backgroundColor: "{colors.bg-dark-surface}"
    rounded: "{rounded.xl}"
    padding: "16px"
  sheet-modal:
    backgroundColor: "{colors.bg-dark-surface}"
    rounded: "{rounded.xl}"
    padding: "20px"
---

# Design System: LogLens

## Overview

**Creative North Star: "The macOS Developer Console"**

LogLens is an offline-first, browser-native log forensics and distributed tracing console. It pairs extreme information density (Gantt waterfall timelines, Swiss-aligned execution trees, flamegraphs, dependency topologies) with Apple Human Interface Guidelines (HIG) craft: native San Francisco typography, translucent frosted backdrops, double-layer sheet depth, and grouped card layouts.

The design strictly serves developer velocity: zero telemetry or tracking, zero cloud friction, zero dependencies, and zero decorative noise. Visual chrome remains disciplined and quiet so the user's raw log streams, latency bottlenecks, and anomaly signals remain the heroes of every viewport.

**Key Characteristics:**
- **Extreme Information Density**: Compact 50px header, collapsible 322px sidebar, Swiss 3-zone execution tree grid, and bounded viewport flex layouts that never waste vertical canvas space.
- **Apple HIG Refinement**: Native San Francisco font stack (`-apple-system`, `SF Pro`, `SF Mono`), 26px circular close buttons, macOS sheet modal elevations (`backdrop-filter: blur(14px) saturate(160%)`), and spring-animated sliding pills (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Perceptually Calibrated Theming**: 6 distinct calibrated themes (Obsidian, Ivory, Aurora, Midnight, Forest, Crimson) built on OKLCH color ramps sharing uniform semantic token interfaces (`--bg-0` to `--bg-4`, `--t1` to `--t4`, `--bdr`, `--bdr-h`).
- **Tactile Developer Ergonomics**: Seamless keyboard shortcuts (`Alt+1`..`0`, direct single-keystroke `1`..`0` navigation, `⌘K / Ctrl+K` Spotlight, `J`/`K` tree traversal), instant zero-network file processing, and zero layout shift.

## Colors

The LogLens color system pairs perceptually uniform OKLCH neutrals with diagnostic semantic overlays. Accents convey operational state rather than decorative styling.

### Primary
- **Console Amber** (`oklch(67% 0.16 55)` / `#f0883e` in Obsidian; `oklch(60% 0.18 55)` in Ivory): Reserved for primary call-to-actions, active navigation pills (`#vtabs-pill`), active thread badges, timeline cursor needles, and parsing progress bars.

### Secondary
- **Diagnostics Blue** (`oklch(70% 0.12 250)` / `#58a6ff` in Obsidian; `oklch(55% 0.16 250)` in Ivory): Secondary selection states, search query match counters, HTTP/REST element tags, and informational guide badges.

### Tertiary
- **Health Green** (`oklch(68% 0.14 140)` / `#3fb950` in Obsidian; `oklch(55% 0.16 140)` in Ivory): Regex rule coverage progress meters, valid syntax indicators, and Local File System API connection status.

### Status & Accents
- **Breach Red** (`oklch(63.5% 0.18 25)` / `#f85149`): SLA violation chips (`SLA BREACH`), error log entries, critical exception markers (`✦ CRIT`), and destructive action confirmation.
- **Outlier Yellow** (`oklch(78% 0.15 85)` / `#d29922`): IQR duration anomaly chips (`OUTLIER`), warning events, and thread resource alerts.
- **Trace Purple** (`oklch(65% 0.18 310)` / `#bc8cff`): Distributed trace correlation IDs (`#TraceID`), span linkages, and microservice boundary hops.
- **Stream Cyan** (`oklch(72% 0.11 210)` / `#39c5cf`): Live file-streaming rate meters, thread isolation indicators, and cache telemetry chips.

### Neutrals & Theme Surfaces
- **Obsidian (Default Dark)**: Base `oklch(12% 0.012 240)` (`#060a0f`), panels `oklch(15% 0.014 240)` to `oklch(18% 0.016 240)`, hairline borders `oklch(24% 0.018 240)` (`#30363d`). Text scales from warm white `oklch(95% 0.005 55)` down to muted slate `oklch(62% 0.012 55)`.
- **Ivory (Calibrated Light)**: Base `oklch(94.5% 0.012 55)` (`#f2efea`), panels `oklch(99% 0.003 55)` (`#ffffff`), borders `oklch(75% 0.022 55)` (`#d0d7de`). High-contrast dark text `oklch(25% 0.015 55)`.
- **Aurora, Midnight, Forest, Crimson**: Specialized palettes (Aurora navy/cyan, Midnight OLED pure black/neon purple, Forest deep emerald, Crimson dark ruby) mapping 1:1 onto identical semantic token variables (`--bg-0` through `--bg-4`).

### Named Rules
**The 10% Accent Rule.** Saturated semantic accents (Amber, Blue, Green, Red) must never exceed 10% of any viewport surface area. They carry diagnostic state, not decorative wallpaper.

**The Contrast Floor Rule.** Body text, timestamps, and log payload strings must maintain ≥4.5:1 contrast against their card background across all 6 themes.

## Typography

**Display Font:** `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro", Inter, Geist, system-ui, "Segoe UI", Roboto, sans-serif`  
**Body Font:** `-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro", Inter, Geist, system-ui, "Segoe UI", Roboto, sans-serif`  
**Mono Font:** `"SF Mono", Menlo, Monaco, "JetBrains Mono", "Geist Mono", Consolas, "Cascadia Code", monospace`  

**Character:** Native Apple San Francisco typography delivering instant system-level rendering with zero runtime web font downloads and zero layout shift.

### Hierarchy
- **Display** (700 weight, 18px, line-height 1.2, letter-spacing -0.02em): Main modal titles, welcome banners, and Spotlight command palette headers.
- **Headline** (600 weight, 15px, line-height 1.3, letter-spacing -0.01em): Dashboard card headers, primary section titles, and modal sub-headings.
- **Title** (600 weight, 13px, line-height 1.4, letter-spacing 0em): Summary card titles, table column headers, and view toolbar labels.
- **Body** (400 weight, 12px, line-height 1.5, letter-spacing normal): Settings descriptions, inspector metadata text, help guidance, and general UI copy.
- **Label** (600 weight, 10.5px, line-height 1.2, letter-spacing 0.04em, uppercase): Metric card badges, SLA status pills, thread pills, and keyboard shortcut hints (`.cmd-kbd`).
- **Mono** (400/600 weight, 11px, line-height 1.4, letter-spacing normal): Raw log lines, timestamps (`HH:mm:ss.SSS`), regex patterns, execution durations (`325.0ms`), thread IDs, and LQL query statements.

### Named Rules
**The Monospace Data Rule.** Any value originating from a log file, duration calculation, capture token, or LQL query expression must render in `--mono` to preserve strict tabular column alignment.

**The Native System Zero-Shift Rule.** All font stacks prioritize native system fonts (`-apple-system`, `SF Pro`, `SF Mono`). Web fonts must never be downloaded at runtime, guaranteeing zero layout shift (CLS = 0) and zero offline font failures.

## Layout

LogLens organizes complex telemetry through an uncompromised spatial grid designed for developer screens.

### Spatial Model & Grid
- **Header Bar (`.hdr`)**: Fixed 50px height (`--hh: 50px`) spanning 100% width. Features a 120px branding anchor on the left, utility actions on the right, and the view switcher (`.hdr .vtabs.on`) mathematically centered (`position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 10`).
- **Sidebar (`#sb`)**: Fixed 322px width (`--sw: 322px`), collapsible to 0px via toggle button or `Alt+B`. Houses file upload dropzone, regex pattern editor, thread filter dropdown, and rule management cards.
- **Canvas Container (`#res`)**: Bounded viewport container (`flex: 1; min-height: 0; overflow: hidden;`). Child views (Split, Timeline, Tree, Traces, Stats) inherit `flex: 1; min-height: 0; display: flex; flex-direction: column;` to guarantee isolated scrolling without parent page expansion.
- **Swiss 3-Zone Execution Tree (`TR.renderRow`)**:
  - **Zone 1 (Left — 420px Fixed Spine)**: Contains SVG branch guide lines (15px step increments), micro-chevrons, icons, operation name, element pill, and high-signal alert badges (`ERR`, `WARN`, `SLA BREACH`, `OUTLIER`, `✦ CRIT`, `#TraceID`).
  - **Zone 2 (Center — Flexible Payload)**: Single-line monospace chip (`.tree-payload-preview`) with `white-space: nowrap !important; text-overflow: ellipsis !important; line-height: 18px; height: 20px;`, preventing multi-line wrap staircases.
  - **Zone 3 (Right — 306px Fixed Telemetry Strip)**: Rigidly aligned columns: 44px sparkbar, 60px duration, 66px self-time, 60px thread pill, 76px timestamp.

### Responsive Breakpoints
- **Desktop Wide (≥1280px)**: Full side-by-side split views, pinned 420px spine, expanded telemetry strips, detached minimap.
- **Desktop Compact (1051px – 1279px)**: Centered view switcher maintained; payload preview truncates dynamically.
- **Tablet / Narrow (769px – 1050px)**: Header view switcher reverts from absolute centering to standard flex flow (`@media (max-width: 1050px)`).
- **Mobile (<768px)**: Header height drops to 48px (`--hh: 48px`), sidebar becomes full-screen drawer overlay, search collapses to Spotlight icon, navigation pills compact.

### Named Rules
**The Bounded Viewport Rule.** Canvas containers must define `min-height: 0` and `flex: 1` with strict overflow isolation. Outer parent pages must never scroll vertically when a timeline, tree, or table is active.

**The Swiss Ledger Alignment Rule.** Numbers, durations, sparkbars, and timestamps in telemetry columns must occupy fixed-width sub-columns with right alignment, ensuring clean vertical scanning like a Swiss financial ledger.

## Elevation & Depth

LogLens uses a hybrid elevation model: strictly flat tonal layering for in-canvas timeline components, combined with Apple sheet elevation and frosted glass backdrops for floating HUDs and modals.

### Shadow Vocabulary
- **Surface Rest** (`box-shadow: none; border: 1px solid var(--bdr)`): Base timeline tracks, tree rows, editor cards, and data table rows.
- **Grouped Card Depth** (`box-shadow: var(--shd-xs)`): Inset `.dashboard-card` and top `.stats` metric strips (`0 1px 4px rgba(0,0,0,.35)` dark / `.09` light).
- **macOS Floating HUD** (`box-shadow: var(--shd)` with `backdrop-filter: blur(14px) saturate(160%)`): Timeline floating controllers, hover tooltip inspection cards (`#app-tooltip`), and quick-edit popovers (`0 4px 16px rgba(0,0,0,.5), 0 1px 3px rgba(0,0,0,.4)` dark / `.10` light).
- **Apple Sheet Modal** (`box-shadow: 0 0 0 1px rgba(255,255,255,.07), 0 24px 64px -12px rgba(0,0,0,.55), 0 12px 28px -6px rgba(0,0,0,.35)` dark / `0 0 0 1px rgba(0,0,0,.08), 0 24px 64px -12px rgba(0,0,0,.22), 0 12px 28px -6px rgba(0,0,0,.12)` light): Applied to `#cmd-palette` Spotlight search and full-screen dialog modals with spring entrance easing (`cubic-bezier(0.16, 1, 0.3, 1)`).

### Named Rules
**The Frosted Backdrop Rule.** All modal backdrops and floating toolbars must pair translucent backgrounds (`rgba(..., 0.8)`) with `backdrop-filter: blur(14px) saturate(160%)` to maintain background context without visual clutter.

**The Flat-At-Rest Rule.** All in-canvas data surfaces (tables, Gantt tracks, tree nodes) are completely flat at rest with 1px hairline borders. Drop shadows appear solely as responses to elevation states (floating HUDs, hovering popovers, dialog sheets).

## Shapes

LogLens maintains a disciplined corner radius and form language inspired by Apple macOS Sonoma / Sequoia design language.

### Corner Radius Hierarchy
- **Micro (`2px`, `--radius-xs`)**: Micro guide notches, sparkbar fill corners, and code tag corners.
- **Small (`4px`, `--radius-sm`)**: Syntax badges, SLA tags, inline keyboard shortcut hints (`.cmd-kbd`).
- **Medium (`6px`, `--radius-md` / `--rounded-sm`)**: Standard buttons (`.btn`), text inputs (`.inp`), segmented tab items, and filter chips.
- **Large (`10px`, `--radius-lg` / `--rounded-md`)**: Secondary popovers, dropdown menus, and nested card containers.
- **Extra Large (`14px`, `--radius-xl` / `--rounded-lg`)**: Grouped dashboard cards (`.dashboard-card`), top stats bar (`#stats-bar`), and modal dialog sheets (`.modal`).
- **Pill (`9999px`, `--radius-pill` / `--rounded-full`)**: Status badges, thread pills (`.tree-thread-pill`), and toggle switch tracks.

### Circular Affordances
- **Apple Circular Close Buttons**: Strict `26px × 26px` dimensions, `border-radius: 50%`, centered `✕` glyph, subtle hairline border, spring hover scale (`1.06`), and active press scale (`0.94`).

### Form Geometry & Borders
- **Hairline Borders**: 1px solid borders (`var(--bdr)`) using perceptually calibrated neutral tokens. Heavy 2px+ borders are banned except on high-contrast focus rings (`outline: 2px solid var(--amber)`).

### Named Rules
**The Hierarchy-Driven Radius Rule.** Corner radius scales strictly with container area: 4px for tags, 6px for controls, 14px for grouped cards/modals. Controls inside cards must never have a larger corner radius than their parent card.

## Components

### Buttons
- **Shape:** Rounded-md (`6px`, `var(--rounded-sm)` / `var(--radius-md)`).
- **Primary (`.btn-p`):** Background `var(--amber)`, color `var(--bg-0)`, font-weight 600, padding `6px 14px`. Hover increases brightness; active scales to `0.98`.
- **Ghost / Tool (`.btn-gh`, `.btn-sub`):** Transparent background, border `1px solid var(--bdr)`, color `var(--t2)`, padding `4px 10px`. Hover illuminates border to `var(--bdr-h)` and text to `var(--t1)`.
- **Apple Circular Close (`.modal-close`, `.c-close`):** `26px × 26px`, `border-radius: 50%`, centered `✕`, subtle border, hover `transform: scale(1.06)`, active press `scale(0.94)`.

### Segmented Controls & Navigation Pills
- **Top View Switcher (`.hdr .vtabs`):** Pill container with `height: 34px`, border `1px solid var(--bdr)`, rounded `var(--rounded-md)`.
- **Gliding Active Indicator (`#vtabs-pill`):** Glides smoothly behind the active view tab using spring physics (`cubic-bezier(0.16, 1, 0.3, 1)`), filled with `var(--amber)` (or theme accent) and dark contrasting label.
- **Analysis Dropdown Button (`#btn-analysis`):** Transparent background with zero inner border, perfectly aligning with navigation tabs when `#vtabs-pill` slides behind it.
- **Tree Depth Controls (`.tree-depth-group`):** Grouped segmented buttons (`D1`, `D2`, `D3`, `All`) with 4px radii for instant call tree depth filtering.

### Inputs & Fields
- **Search & Filter Inputs (`.inp`, `#f-q`, `#rg-inp`):** Background `var(--bg-1)` / `var(--bg-2)`, border `1px solid var(--bdr)`, color `var(--t1)`, font-size `12px`, padding `6px 10px`, rounded `6px`.
- **Focus Treatment:** Smooth border shift to `var(--amber)` accompanied by zero outline bleed or jarring layout shift (`transition: border-color 0.15s ease`).

### Cards & Top Bars
- **Grouped Cards (`.dashboard-card`, `.p-box`):** `14px` border radius (`var(--rounded-lg)`), hairline borders, double depth (`var(--shd-xs)`), and `16px` internal padding.
- **Top Stats Bar (`#stats-bar`):** Single-row flex container with `flex-shrink: 0`, height `62px`, border `1px solid var(--bdr)`, rounded `var(--rounded-lg)`. Inner `.sc` metric cells separated by `1px solid var(--bdr)` borders extending cleanly from top to bottom edge.

### Execution Tree Swiss Telemetry Rows (`TR.renderRow`)
- **Row Architecture:** Strict 3-zone layout with hover highlight `background: var(--bg-1)`.
- **Zone 1 (Spine & Identity):** Fixed 420px anchor across all tree depths; SVG guide lines with 15px step increments meeting chevrons at midpoints; operational icons (`.tico`), span name (`.tnm`), element pill (`.tel`), and diagnostic badges. Healthy `INFO` rows suppress redundant badges.
- **Zone 2 (Payload Preview):** Single-line monospace chip (`.tree-payload-preview`) with `white-space: nowrap !important; text-overflow: ellipsis !important; line-height: 18px; height: 20px;`.
- **Zone 3 (Pinned Telemetry Strip):** 306px fixed right cluster: 44px sparkbar with proportional fill (`var(--blue)`, `var(--yellow)`, `var(--red)`), 60px bold duration (`.tree-metric-dur`), 66px self-time (`.tree-metric-self`), 60px thread pill, and 76px millisecond timestamp (`HH:mm:ss.SSS`).

### Waterfall Gantt Timeline (`.gw`)
- **Container Structure:** Pinned `.g-toolbar` and `.g-hdr` at top, scrollable `.g-rows` occupying remaining flex height (`overflow-y: auto`), pinned `.tl-nav-wrap` minimap at bottom.
- **Horizontal Scroll Synchronization:** Panned and zoomed via trackpad or mouse wheel; header timescale (`.g-hdr`) dynamically syncs scroll offset with `.g-rows`.

### Spotlight Command Palette (`#cmd-palette`)
- **Dimensions:** Width `620px`, max-width `90vw`.
- **Elevation:** Frosted backdrop blur (`backdrop-filter: blur(14px) saturate(160%)`) with Apple sheet modal double-layer shadow.
- **Input:** 16px search input with zero outline and seamless integration into filtered action list.
- **Action Rows:** 8px rounded selection highlights with keyboard shortcut pills (`.cmd-kbd`).

## Do's and Don'ts

### Do:
- **Do** maintain strict single-file HTML architecture (`loglens.html`) with zero runtime npm or CDN dependencies.
- **Do** preserve full vertical real estate for timeline and execution tree views by limiting metric summary cards exclusively to the dedicated Stats dashboard.
- **Do** lock Zone 1 of the Execution Tree to a 420px spine anchor across all nesting depths to prevent payload preview jitter.
- **Do** wrap all interactive dialogs and HUD cards with macOS frosted blurs (`backdrop-filter: blur(14px) saturate(160%)`) and double-layer shadows.
- **Do** use `flex-shrink: 0` on structural metric bars (`#stats-bar`, `#res-summary-cards`) to prevent layout squashing inside scrollable containers.
- **Do** maintain strict keyboard navigation parity (Alt+1..0, direct 1..0 navigation, `⌘K / Ctrl+K`, `Escape` to close drawers/modals, `J`/`K` tree traversal).
- **Do** enforce `white-space: nowrap` on tree row payload previews to prevent multi-line word wrap staircases.

### Don't:
- **Don't** add bulky decorative hero cards above the timeline canvas or execution tree.
- **Don't** use generic fluid clamp scales that distort dashboard information density.
- **Don't** import external CSS frameworks (Tailwind, Bootstrap), icon libraries (FontAwesome, Lucide), or runtime web fonts; rely strictly on vanilla CSS and native San Francisco stacks.
- **Don't** display redundant blue `INFO` badges on healthy execution tree rows.
- **Don't** allow saturated semantic accents to exceed 10% of any viewport surface area.
- **Don't** use side-stripe borders or gradient text for emphasis.
