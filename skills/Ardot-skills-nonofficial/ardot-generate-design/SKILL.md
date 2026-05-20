---
name: ardot-generate-design
description: |
  Use this skill alongside ardot-use when building complete pages, screens, or 
  multi-section UI layouts from scratch in Ardot. Orchestrates multiple MCP tools 
  through a 6-step workflow: init → style system → variables → skeleton → 
  section-by-section build → verification.

  Triggers: "create a landing page in Ardot", "build a login screen", 
  "design a dashboard in Ardot", "make a settings page", "create a profile screen",
  "build this page in Ardot", "convert this design to Ardot".
disable-model-invocation: false
---

# ardot-generate-design — Build Pages & Screens

Builds complete pages, views, and multi-section UI containers in Ardot using 
design system components, variables, and styles. No hardcoded hex/pixel values.

## Skill Boundaries

- Use this skill when the deliverable is a **composed page or screen** 
  (login page, dashboard, settings panel, landing page, etc.)
- If the user wants to create **reusable components**, switch to [ardot-generate-library](../ardot-generate-library/SKILL.md)
- If the user only wants to **query style guides**, use [ardot-style-guide](../ardot-style-guide/SKILL.md) directly

## Prerequisites

**Must load before starting:**
- `ardot-use` — for batch_edit DSL rules, variable binding, gotchas
- `ardot-create-new-file` — for create_new_page usage
- `ardot-style-guide` — for search_style_guide → build_style_guide workflow

---

## Required Workflow (6 Steps)

### Step 1: Initialize

Get the editor state and design guidelines for the target page type.

```
fetch_editor_state(includeSchema: true)
fetch_guidelines(topic)          // landing-page | web-app | mobile-app | slides | table
fetch_file_info                  // Check write permissions
```

### Step 2: Establish the Style System

If no design system exists yet:

```
search_style_guide → build_style_guide  (see ardot-style-guide for full protocol)
get_available_fonts                    (verify font availability)
```

If a design system already exists in the file:

```
fetch_variables                        (get existing variable IDs and values)
batch_read({parentId: "<ComponentsPage>"})  (discover existing reusable components)
```

### Step 3: Create Variables

Translate the style guide tokens into Ardot variables:

```
apply_variables({
  "Colors": {
    "modes": ["Dark"],
    "variables": {
      "bg-primary": { "type": "COLOR", "scopes": ["ALL_FILLS"],
        "valuesByMode": {"Dark": {r: ..., g: ..., b: ..., a: 1}} },
      "text-primary": { "type": "COLOR", "scopes": ["TEXT_FILL"],
        "valuesByMode": {"Dark": {r: ..., g: ..., b: ..., a: 1}} },
      ...all colors from build_style_guide...
    }
  },
  "Spacing": {
    "modes": ["Dark"],
    "variables": {
      "spacing-sm": { "type": "FLOAT", "scopes": ["GAP"],
        "valuesByMode": {"Dark": 8} },
      "spacing-md": { "type": "FLOAT", "scopes": ["GAP"],
        "valuesByMode": {"Dark": 16} },
      "radius-sm": { "type": "FLOAT", "scopes": ["CORNER_RADIUS"],
        "valuesByMode": {"Dark": 6} }
    }
  }
})
```

**Record all returned Variable IDs** — you'll need them for binding in Step 5.

> **Hard gate — forbidden shortcuts:**
> - **Forbidden:** Starting batch_edit before variables are created
> - **Forbidden:** Using hardcoded hex values instead of variables (cornerRadius excepted)

### Step 4: Create the Page Skeleton

```
create_new_page({name: "<Page Name>", select: false})
  → Record the pageId
```

Then create the wrapper frame and section containers:

```js
// Single batch_edit call for the skeleton
wrapper = I("<pageId>", {
  "type": "FRAME", "name": "<Screen Name>",
  "width": 375, "height": "hug_contents",
  "layout": "vertical",
  "fills": [{"type": "SOLID", "color": {r:..., g:..., b:...},
    "boundVariables": {"color": {"id": "VariableID:X:Y", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "FRAME", "name": "Header", "width": "fill_container", "height": 56,
      "layout": "horizontal", "paddingLeft": 16, "paddingRight": 16,
      "counterAxisAlignItems": "CENTER"},
    {"type": "FRAME", "name": "Content", "width": "fill_container",
      "height": "hug_contents", "layout": "vertical",
      "paddingLeft": 24, "paddingRight": 24, "paddingTop": 24, "paddingBottom": 24},
    {"type": "FRAME", "name": "Footer", "width": "fill_container", "height": 48}
  ]
})
```

Record the node IDs of each section frame (Header, Content, Footer, etc.).

### Step 5: Build Each Section

Build one section at a time. Each section gets its own `batch_edit` call (≤25 operations).

```
For each section:
  1. Prepare the operations string for that section
  2. batch_edit → create section contents
  3. batch_read → verify structure
  4. batch_edit (U) → bind variables (especially for TEXT nodes)
  5. batch_read → verify bindings
```

**TEXT nodes require two-step binding** (see ardot-use gotcha #4):
- I() → create with `fill: "#HEX"`
- Separate batch_edit U() → bind variable with fills+boundVariables

> **Hard gate — forbidden shortcuts:**
> - **Forbidden:** Binding variables to TEXT nodes directly in I()
> - **Forbidden:** Using binding names from a previous batch_edit call
> - **Forbidden:** Exceeding 25 operations per batch_edit call

### Step 6: Verify

```
capture_screenshot({
  "nodeIds": ["<screenNodeId>", ...all screen node IDs],
  "screenShotDir": "/tmp/ardot-verify"
})
```

**Review ALL screenshots** for:
- Visual correctness (colors, spacing, alignment)
- Text not clipped or overflowing
- All sections present and properly laid out

If issues found → `batch_edit` fix → `capture_screenshot` again.

## Variable ID Tracking

Maintain a running record of all variable IDs:

| Variable Name | Variable ID |
|---------------|-------------|
| bg-primary | VariableID:3:14 |
| text-primary | VariableID:3:15 |
| accent-warm | VariableID:3:16 |
| spacing-md | VariableID:3:17 |
| radius-sm | VariableID:3:18 |

Obtained from `apply_variables` return values or `fetch_variables`.

## Batch Management — 25-Operation Limit

When a section needs more than 25 operations:

1. **Split by logical sub-sections** — header items in one call, content cards in another
2. **Separate creation from binding** — I() in one call, U() bindings in the next
3. **Combine small, independent updates** — merge multiple single-node U() calls into one batch

## Error Recovery

If a batch_edit fails:
1. Read the error — it's atomic, file is unchanged
2. Fix the issue (usually: wrong node ID, wrong pageId, or syntax error)
3. Retry the batch_edit call

See [ardot-use references/validation-and-recovery.md](../ardot-use/references/validation-and-recovery.md) 
for detailed recovery strategies.