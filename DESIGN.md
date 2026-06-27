---
name: LogLens
description: Metadata-Driven Log Analyzer
colors:
  primary: "#f0883e"
  secondary: "#58a6ff"
  tertiary: "#3fb950"
  danger: "#f85149"
  bg-dark: "#060a0f"
  bg-dark-low: "#0d1117"
  bg-dark-panel: "#161b22"
  bg-light: "#edecea"
  bg-light-low: "#f8f7f5"
  bg-light-panel: "#fff"
  text-dark: "#f0f6fc"
  text-dark-secondary: "#c9d1d9"
  text-light: "#1c1b1a"
  text-light-secondary: "#403f3d"
  # Light theme variables
  light-primary: "#c2620a"
  light-primary-grad: "#a35000"
  light-bg-0: "#f2efea"
  light-bg-1: "#faf8f5"
  light-bg-2: "#f0ede8"
  light-bg-3: "#e8e4dd"
  light-bg-4: "#dad6cf"
  light-bdr: "#cac5bc"
  light-bdr-d: "#e0dbd3"
  light-bdr-h: "#a9a49b"
  light-t1: "#18181b"
  light-t2: "#27272a"
  light-t3: "#52525b"
  light-t4: "#a1a1aa"
  light-blue: "#2563eb"
  light-green: "#16a34a"
  light-red: "#dc2626"
  light-yellow: "#b45309"
  light-purple: "#7c3aed"
  light-cyan: "#0891b2"
typography:
  display:
    fontFamily: "Inter, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "32px"
    fontWeight: 800
    letterSpacing: "-0.6px"
  body:
    fontFamily: "Inter, Geist, system-ui, -apple-system, sans-serif"
    fontSize: "12px"
    lineHeight: 1.6
  mono:
    fontFamily: "JetBrains Mono, Geist Mono, monospace"
    fontSize: "10.5px"
rounded:
  sm: "6px"
  md: "8px"
  lg: "10px"
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
    textColor: "{colors.bg-dark}"
    rounded: "{rounded.sm}"
    padding: "6px 14px"
  button-primary-hover:
    backgroundColor: "#f5a36c"
  input-text:
    backgroundColor: "{colors.bg-dark-low}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.sm}"
    padding: "6px 10px"
---

# Design System: LogLens

## 1. Overview

**Creative North Star: "The Developer's Console"**

LogLens is built to look like a terminal-adjacent, low-chrome dark dashboard focused entirely on high information density, clear grids, and immediate utility. Visual styling should be highly professional, avoiding decorative elements and emphasizing a private, local-first environment for developers and SREs.

**Key Characteristics:**
- **Zero Decorative Noise**: Every border, outline, and background shift must serve a structural or interactive purpose.
- **High Information Density**: Sizing and spacing are compact, designed to display thousands of log messages and complex Gantt timelines without wasting vertical viewport space.
- **Theme-Agnostic Structure**: Dark mode is the primary console layout, but the visual hierarchy maps 1:1 onto a clean, high-contrast light mode.

---

## 2. Colors

The color palette is divided into strict layout neutrals and functional semantic overlays.

### Primary
- **Console Amber** (#f0883e): Used exclusively for primary buttons, focus highlights, warning tags, and critical timeline markers.

### Secondary
- **Diagnostics Blue** (#58a6ff): Highlights information nodes, active view selections, and search match tags.

### Tertiary
- **Success Green** (#3fb950): Represents matching filters, valid rules, and normal performance ranges.

### Neutral
- **Deep Void / Off-White** (#060a0f / #edecea): Deep viewport background.
- **Surface / Paper** (#0d1117 / #f8f7f5): Secondary panels and sidebar base.
- **Container Panel** (#161b22 / #fff): Interactive inputs, logs table background, and modals.
- **Border Outline** (#30363d / #d0cfcd): Card margins and input boundaries.

**The 10% Accent Rule.** Accent colors (Amber, Blue, Green, Red) must never cover more than 10% of any given viewport surface area. Their primary purpose is diagnostic feedback.

---

## 3. Typography

**Display Font:** Inter, system-ui, sans-serif  
**Body Font:** Inter, system-ui, sans-serif  
**Label/Mono Font:** JetBrains Mono, monospace  

### Hierarchy
- **Display** (800 weight, 32px, letter-spacing: -0.6px): Used only for main app name badge and primary onboarding header.
- **Headline** (600 weight, 18px): Tab view labels and primary drawer headers.
- **Title** (600 weight, 13px): Panel headings and modal subtitles.
- **Body** (400 weight, 12px, line-height: 1.6): Sidebar quick guide descriptions and inputs helper tips.
- **Label** (400 weight, 10.5px): Log timestamp rows, duration badges, and LQL table metrics.

**The Monospace Code Rule.** Any string output that originates from a log stream, regex pattern, or LQL query statement must be strictly wrapped in a monospaced font block (`JetBrains Mono` or default fallback) to preserve horizontal indentation and parsing alignment.

---

## 4. Elevation

LogLens utilizes tonal layering to convey hierarchy, utilizing flat layouts with background offsets and keeping shadow effects to a strict minimum.

**The Flat-First Rule.** Surfaces are completely flat at rest. Drop shadows (`0 4px 24px rgba(0,0,0,0.15)`) are only permitted on floating elements, such as dropdown menus, help popovers, and modal dialog overlays.

---

## 5. Components

### Buttons
- **Shape:** Rounded-sm (6px)
- **Primary:** Background `#f0883e`, text color `#060a0f`, padding `6px 14px`.
- **Hover / Focus:** Hover shifts background to `#f5a36c`. Focus displays outline ring with `2px` offset.
- **Ghost:** Transparent background, outline border `1px solid var(--bdr)`.

### Chips
- **Style:** Compact rounded-full (99px) border, font-size `10px`.
- **State:** Unselected has background `var(--bg-1)`; selected has border-color `var(--blue)` or `var(--amber)` depending on context.

### Cards / Containers
- **Corner Style:** Rounded-md (8px) for major dashboard panels, Rounded-lg (10px) for floating popups.
- **Background:** `var(--bg-1)` or `var(--bg-2)`.
- **Border:** `1px solid var(--bdr)`.

### Inputs / Fields
- **Style:** Background `var(--bg-0)`, border `1px solid var(--bdr)`, corner radius `6px`.
- **Focus:** Outline glow with border-color `var(--bdr-h)` or `var(--primary)`.

---

## 6. Do's and Don'ts

### Do:
- **Do** respect the 10% accent rule: keep visual prominence focused on log data rows, not colored header panels.
- **Do** use strict variable mappings (`var(--bg-0)` to `var(--bg-4)`) to ensure instant theme toggling works reliably.
- **Do** outline form items with visible keyboard focus rings.

### Don't:
- **Don't** use glowing neon gradients, purple shadows, or frosted glass panels that evoke a generic consumer-facing SaaS layout.
- **Don't** insert margin spacing exceeding 16px around log panels, as space must be optimized for developer timeline density.
- **Don't** hide critical help hints inside submenus; use inline context tooltips (`?`) beside controls.
