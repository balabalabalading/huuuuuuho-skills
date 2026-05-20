---
name: ardot-generate-library
description: |
  Use this skill when building a reusable component library or design system in Ardot.
  Covers the full workflow from variable/design-token creation through component 
  building with proper variable bindings, to final verification.

  Triggers: "create a component library", "build a design system", 
  "make reusable buttons", "create UI components", "build a component set",
  "design system", "component library", "reusable components".
disable-model-invocation: false
---

# ardot-generate-library — Build Component Libraries

Builds reusable component libraries and design systems in Ardot. Components are 
created with proper variable bindings so they respond to theme/mode changes.

## Skill Boundaries

- Use this skill when building **reusable components** (buttons, cards, inputs, nav bars, etc.)
- Use this skill when creating a **design system** with tokens and components
- If building a one-off page/screen, use [ardot-generate-design](../ardot-generate-design/SKILL.md) instead

## Prerequisites

- `ardot-use` — for batch_edit DSL rules, variable binding, gotchas
- `ardot-create-new-file` — for creating the Components page

---

## Phase 1: Foundation

### 1a: Create the Components page

```
create_new_page({name: "Components", select: false})
  → Record the pageId (e.g. "3:1672")
```

### 1b: Create design tokens (variables)

Use `apply_variables` to create the variable foundation. Components will bind to 
these variables.

```json
apply_variables({
  "variables": {
    "Colors": {
      "modes": ["Dark", "Light"],
      "variables": {
        "accent-primary": {
          "type": "COLOR", "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.91, "g": 0.44, "b": 0.29, "a": 1},
            "Light": {"r": 0.83, "g": 0.38, "b": 0.23, "a": 1}
          }
        },
        "accent-primary-text": {
          "type": "COLOR", "scopes": ["TEXT_FILL"],
          "valuesByMode": {
            "Dark": {"r": 1, "g": 1, "b": 1, "a": 1},
            "Light": {"r": 1, "g": 1, "b": 1, "a": 1}
          }
        },
        "bg-secondary": {
          "type": "COLOR", "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.15, "g": 0.15, "b": 0.15, "a": 1},
            "Light": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1}
          }
        },
        "text-primary": {
          "type": "COLOR", "scopes": ["TEXT_FILL"],
          "valuesByMode": {
            "Dark": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1},
            "Light": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}
          }
        },
        "border-default": {
          "type": "COLOR", "scopes": ["STROKE"],
          "valuesByMode": {
            "Dark": {"r": 0.25, "g": 0.25, "b": 0.25, "a": 1},
            "Light": {"r": 0.85, "g": 0.85, "b": 0.85, "a": 1}
          }
        }
      }
    },
    "Spacing": {
      "modes": ["Dark", "Light"],
      "variables": {
        "spacing-xs": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 4, "Light": 4}},
        "spacing-sm": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 8, "Light": 8}},
        "spacing-md": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 16, "Light": 16}},
        "spacing-lg": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 24, "Light": 24}},
        "radius-sm": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 6, "Light": 6}},
        "radius-md": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 8, "Light": 8}},
        "radius-lg": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 12, "Light": 12}}
      }
    }
  }
})
```

**Record all returned Variable IDs** in a tracking table for later binding.

> **Hard gate:**
> - **Forbidden:** Creating components before variables exist
> - **Forbidden:** Creating components with hardcoded colors (cornerRadius excepted)

---

## Phase 2: Component Creation

Build components one at a time, in dependency order:

```
Atomic (no dependencies):
  → Button, Input, Label, Icon, Badge, Avatar, Divider

Molecular (depends on atomic):
  → Card (uses Button, Badge), NavBar (uses Button), FormField (uses Input, Label)
```

### Per-component workflow

```
1. batch_edit (I) → Create component with reusable:true on Components page
   - Use boundVariables for frame fills (NOT for TEXT fills yet)
   - TEXT children use fill: "#HEX" placeholder
   - Record the returned component node ID

2. batch_read → Verify the component structure

3. batch_edit (U) → Bind variables to TEXT children
   - Apply fills+boundVariables to each TEXT node

4. batch_read → Verify variable bindings are present

5. capture_screenshot → Visual check of the component
```

### Example: Button/Primary/md

```js
// Step 1: Create the component
btnPrimaryMd = I("3:1672", {
  "type": "FRAME",
  "name": "Button/Primary/md",
  "reusable": true,
  "width": "hug_contents", "height": 32,
  "layout": "horizontal",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 6, "paddingBottom": 6,
  "cornerRadius": 8,
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "fills": [{"type": "SOLID", "color": {"r": 0.91, "g": 0.44, "b": 0.29},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "Label", "characters": "Button",
      "fontSize": 14, "fill": "#FFFFFF"}
  ]
})
// Returns: btnPrimaryMd → "3:544", TEXT child → "3:545"

// Step 3 (separate batch_edit): Bind text color variable
U("3:545", {
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1},
    "boundVariables": {"color": {"id": "VariableID:3:15", "type": "VARIABLE_ALIAS"}}}]
})
```

### Example: Card with children

```js
card = I("3:1672", {
  "type": "FRAME",
  "name": "Card/Default",
  "reusable": true,
  "width": 320, "height": "hug_contents",
  "layout": "vertical",
  "paddingLeft": 20, "paddingRight": 20,
  "paddingTop": 20, "paddingBottom": 20,
  "cornerRadius": 12,
  "fills": [{"type": "SOLID", "color": {"r": 0.15, "g": 0.15, "b": 0.15},
    "boundVariables": {"color": {"id": "VariableID:3:16", "type": "VARIABLE_ALIAS"}}}],
  "strokes": [{"type": "SOLID", "color": {"r": 0.25, "g": 0.25, "b": 0.25},
    "boundVariables": {"color": {"id": "VariableID:3:18", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "Title", "characters": "Card Title",
      "fontSize": 18, "fill": "#F2F2F2"},
    {"type": "TEXT", "name": "Body", "characters": "Card description text.",
      "fontSize": 14, "fill": "#AAAAAA"}
  ]
})
```

## Phase 3: Verification

### 3a: Structural verification

```json
batch_read({parentId: "<ComponentsPageId>"})
```

Check that:
- All planned components exist with correct names
- All have `reusable: true`
- All have expected children

### 3b: Variable binding verification

For each component, verify variable bindings are present:

```json
batch_read({nodeIds: ["<componentId1>", "<componentId2>", ...]})
```

Check `fills[].boundVariables` and `strokes[].boundVariables` are not empty.

### 3c: Visual verification

```json
capture_screenshot({
  "nodeIds": ["<all component IDs>"],
  "screenShotDir": "/tmp/ardot-components"
})
```

Review all component screenshots for visual correctness.

## Hard Gates — Forbidden Shortcuts

- **Forbidden:** Creating components before variables exist
- **Forbidden:** Hardcoding hex colors in component fills (use boundVariables)
- **Forbidden:** Skipping TEXT two-step variable binding
- **Forbidden:** Using hardcoded font sizes that don't match design tokens
- **Forbidden:** Creating dependent (molecular) components before their atomic dependencies

## Recommended Naming Convention

```
<Category>/<Variant>/<Size>

Examples:
  Button/Primary/sm
  Button/Primary/md
  Button/Primary/lg
  Button/Secondary/md
  Button/Ghost/md
  Card/Default
  Card/Elevated
  Input/Default
  Input/Error
  Badge/Success
  Badge/Warning
```

Use `/` as separator — this creates Figma-compatible component grouping.