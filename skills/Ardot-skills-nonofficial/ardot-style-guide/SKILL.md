---
name: ardot-style-guide
description: |
  Use this skill when designing from scratch or applying a visual theme to an Ardot project.
  Covers the `search_style_guide` → `build_style_guide` workflow for discovering and 
  applying complete design systems (colors, typography, spacing, layout patterns).

  Triggers: "design a landing page", "create a dashboard", "apply a dark theme",
  "set up a design system", "choose a color palette", "pick fonts for my app",
  "style guide", "visual style", "look and feel".
disable-model-invocation: false
---

# ardot-style-guide — Style Guide Search & Build

Discovers and applies complete design systems via the `search_style_guide` → 
`build_style_guide` toolchain. Ardot-unique capability with no Figma equivalent.

## Skill Boundaries

- Use this skill when the user wants to establish a visual style from scratch
- Use this skill BEFORE any `batch_edit` that creates styled UI (colors, typography)
- Skip this skill if the user already has an established design system with known tokens
- The output of `build_style_guide` is **authoritative** — all downstream tools MUST 
  follow its values exactly

## Prerequisites

- `fetch_editor_state(includeSchema: true)` must have been called
- `fetch_guidelines(topic)` should be loaded for the target design type

---

## search_style_guide — Three-Round Fallback Protocol

### Round 1: Keyword Search

Provide specific keywords to target the user's intent.

```
search_style_guide({
  "topic": "landing-page",        // or web-app, mobile-app, slides, table
  "designKeywords": "SaaS dashboard modern clean professional",
  "colorKeywords": "dark mode cool blue professional",
  "typographyKeywords": "modern sans-serif clean readable",
  "layoutKeywords": "dashboard analytics cards grid"
})
```

**After receiving results**, review EACH domain individually:

- **style**: Does the Style Category match the requested visual style?
- **color**: Check Background, Card, and Foreground values. If user wants dark mode 
  but all Background values are light (#F_xxxx range), this domain has NO suitable match.
- **typography**: Does the mood match? Is the font available (check with `get_available_fonts`)?
- **layout**: Does the pattern fit the page type?

If ALL candidates in a domain are suitable → proceed to `build_style_guide`.

### Round 2: Full Catalog (if any domain has no suitable match)

For domains with no suitable match in Round 1, call `search_style_guide` again with 
`true` for that domain's keyword to get the full catalog:

```
search_style_guide({
  "topic": "landing-page",
  "designKeywords": "SaaS dashboard",
  "colorKeywords": true,           // Full catalog for colors
  "typographyKeywords": true       // Full catalog for typography
})
```

### Round 3: Own Design Knowledge (only if Round 2 also fails)

Only for domains that still have no suitable match after Round 2, you may use your 
own design knowledge. This should be rare.

---

## build_style_guide — Authority Constraint

Once you've made selections across all domains, call `build_style_guide`:

```json
build_style_guide({
  "selections": {
    "style": 2,          // Index or name from search results
    "color": 1,
    "typography": 3,
    "layout": 0
  }
})
```

### CRITICAL: The returned design system is AUTHORITATIVE

The `build_style_guide` response provides **exact values** that MUST be used:

- **Colors**: Use the exact `#HEX` or `{r, g, b}` values — do NOT adjust
- **Typography**: Use the exact font family, sizes, weights specified
- **Border radius**: Use the exact px values
- **Spacing**: Use the exact px values
- **Effects**: Use the exact shadow/blur parameters

> **Hard gate**: If the design system says Background is `#FAF5FF`, use `#FAF5FF` 
> (converted to 0–1 range for batch_edit). If you realize it conflicts with the 
> user's intent (e.g., user wanted dark but got light), go BACK to `search_style_guide` 
> with corrected keywords — do NOT silently override values.

### Converting style guide values to batch_edit

Style guide hex colors → batch_edit {r, g, b} 0–1 format:
```
#FAF5FF → {r: 0.98, g: 0.96, b: 1.0}
#1A1A2E → {r: 0.10, g: 0.10, b: 0.18}
#E8714A → {r: 0.91, g: 0.44, b: 0.29}
```

---

## Selection Strategy Per Domain

### Style
Match the Style Category name against the user's description. Trust the content 
over the search score — a lower-scored candidate that matches the intent is better 
than a high-scored irrelevant one.

### Color
Check Background (primary surface color), Card (secondary surface), and Foreground 
(text/icon) values specifically. These three tell you if the palette is light or dark.

### Typography
Verify font availability with `get_available_fonts` BEFORE selecting. A font pairing 
is useless if neither font is available. Check both heading and body fonts.

### Layout
Match the pattern name to the functional intent. For example, "pricing" → look for 
comparison/table layouts; "dashboard" → look for card grid layouts.

---

## topic Parameter Guide

| topic | Use For | Typical designKeywords |
|-------|---------|----------------------|
| `landing-page` | Marketing pages, homepages, promotional sites | "hero section", "CTA", "features" |
| `web-app` | SaaS dashboards, admin panels, internal tools | "dashboard", "data table", "sidebar" |
| `mobile-app` | iOS/Android app screens | "bottom nav", "cards", "list" |
| `slides` | Presentation decks | "title slide", "content", "chart" |
| `table` | Data tables and dashboards | "data grid", "filters", "pagination" |

---

## Full Workflow Summary

```
1. fetch_editor_state(includeSchema: true)
2. fetch_guidelines(topic)                          → Design rules for the page type
3. get_available_fonts                              → Check font availability
4. search_style_guide (Round 1)                     → Keyword search
5. [if needed] search_style_guide (Round 2)         → Full catalog fallback
6. build_style_guide(selections)                    → Get authoritative design tokens
7. apply_variables                                  → Create variables matching the tokens
8. batch_edit                                       → Build UI using the exact token values
```