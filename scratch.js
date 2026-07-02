const fs = require('fs');

function hexToOklch(hex) {
  // A simple approximation or we can just use oklch() with color mix if we don't have a library.
  // Actually, CSS supports oklch directly. We can just write oklch strings.
}
// Since we don't have culori or color.js, I will just output the oklch string directly by using the hex values and tinting them.
// Wait, the prompt says "Use OKLCH for color... Tinted neutrals: add 0.005–0.015 chroma toward the brand's hue."

// Let's just use CSS `color-mix` or write out the OKLCH manually.
// Brand Amber: #f0883e -> approx OKLCH(67% 0.16 55)
// Brand Blue: #58a6ff -> approx OKLCH(70% 0.12 250)
// Brand Green: #3fb950 -> approx OKLCH(68% 0.14 140)
// Brand Red: #f85149 -> approx OKLCH(62% 0.18 25)

console.log(`
:root {
  /* OKLCH depth system — tinted toward Amber (Hue 55) for brand cohesion */
  --bg-0: oklch(14% 0.008 55);
  --bg-1: oklch(17% 0.009 55);
  --bg-2: oklch(20% 0.010 55);
  --bg-3: oklch(24% 0.011 55);
  --bg-4: oklch(29% 0.012 55);
  
  --bdr-d: oklch(24% 0.011 55);
  --bdr: oklch(28% 0.012 55);
  --bdr-h: oklch(35% 0.013 55);
  
  /* Text — warm whites */
  --t1: oklch(95% 0.005 55);
  --t2: oklch(85% 0.01 55);
  --t3: oklch(70% 0.015 55);
  --t4: oklch(50% 0.015 55);
  
  /* Accent palette — premium, warm amber signal */
  --amber: oklch(67% 0.16 55);
  --amber-g: oklch(67% 0.16 55 / 0.13);
  --amber-d: oklch(67% 0.16 55 / 0.06);
  
  --blue: oklch(70% 0.12 250);
  --blue-g: oklch(70% 0.12 250 / 0.12);
  
  --green: oklch(68% 0.14 140);
  --green-g: oklch(68% 0.14 140 / 0.11);
  
  --red: oklch(62% 0.18 25);
  --red-g: oklch(62% 0.18 25 / 0.11);
  
  --yellow: oklch(78% 0.15 85);
  --yellow-g: oklch(78% 0.15 85 / 0.10);
  
  --purple: oklch(65% 0.18 310);
  --purple-g: oklch(65% 0.18 310 / 0.11);
  
  --cyan: oklch(72% 0.11 210);
  --cyan-g: oklch(72% 0.11 210 / 0.11);
}
`);
