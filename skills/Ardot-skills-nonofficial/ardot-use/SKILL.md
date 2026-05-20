---
name: ardot-use
description: |
  **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `batch_edit` tool call.
  NEVER call `batch_edit` directly without loading this skill first.

  Trigger whenever the user wants to create, update, move, or delete nodes in an Ardot design file — 
  e.g. inserting frames, text, shapes, components; binding variables to fills/strokes; 
  building screens, components, or design libraries. Also load when batch_edit DSL operations 
  are involved (I/U/M/D/C/G operators).
disable-model-invocation: false
---

# ardot-use — Ardot batch_edit DSL Skill

Core skill for all Ardot write operations via the `batch_edit` DSL. Provides critical rules, 
operator reference, variable binding patterns, validation strategies, and error recovery.

## 1. Critical Rules

**1. Maximum 25 operations per `batch_edit` call.** Split larger work into multiple calls. 
Recommend staying at 20 or fewer to leave headroom.

**2. Binding names expire after each `batch_edit` call.** The binding names assigned in one 
call (e.g. `btn1 = I(...)`) are ONLY valid within that same call. In the next `batch_edit`, 
you MUST use the real node ID (e.g. `"3:544"`) — never a binding name from a previous call.

**3. TEXT nodes in I() only support `fill: "#HEX"` string format.** You cannot use 
`fills: [{..., boundVariables: {...}}]` when creating a TEXT node inside I(). 
**Workaround**: Create the TEXT node in I() with `fill: "#HEX"`, then in a subsequent 
`batch_edit` call, use U() to apply `fills` with `boundVariables`.

**4. `updated: {}` does NOT mean failure.** U() operations often return `updated: {}` 
instead of `updated: {"nodeId": {...}}`. The operation likely succeeded — verify by 
running `batch_read` on the node immediately after, rather than trusting the return value.

**5. Cross-page insertion requires explicit `pageId` in I().** By default, I() creates nodes 
on the currently active page. To create on a different page, use `I("pageId", {...})`.

**6. M() target MUST be a pageId, not a frameId.** M() only supports moving nodes between 
pages. To reparent within the same page, delete and recreate or restructure via U().

**7. cornerRadius variable binding is NOT supported.** Ardot currently does not support 
`boundVariables` for `cornerRadius`. Use hardcoded numeric values instead (e.g. `cornerRadius: 6`).

**8. variableModes on frames is unreliable.** Setting `variableModes: {"3:2": "3:3"}` 
to switch color modes may not take effect. Use dedicated pages for light/dark mode instead.

**9. Always `return` all created/mutated node IDs.** Every `batch_edit` response includes 
binding names and node IDs. Record these — you'll need them in subsequent calls.

**10. Work incrementally.** Build skeleton first with placeholders, then fill in details 
one section at a time. Each `use_figma` script failure is atomic — the file is not modified.

**11. Captured screenshots are separate from editing.** Don't mix `capture_screenshot` 
calls inside `batch_edit` operations. Do screenshots as a separate verification step.

## 2. DSL Operators Reference

| Operator | Syntax | Purpose | Key Notes |
|----------|--------|---------|-----------|
| `I` | `I("pageId", {type, name, ...})` | Insert new node | `reusable: true` for components; `width: "hug_contents"\|"fill_container"` |
| `U` | `U("nodeId", {props...})` | Update existing node | Must use real node ID, NOT binding names from previous calls |
| `M` | `M("nodeId", "pageId")` | Move node between pages | Target MUST be a pageId, not frameId |
| `D` | `D("nodeId")` | Delete node | Deleting a parent cascades to all children |
| `C` | `C("componentId")` | Create component instance | Instance inherits component properties; set x/y via subsequent U() |
| `G` | `G(...)` | AI-generated image/graphic | Slow; results are non-deterministic |

### I() — Insert Node

```js
// Create a reusable button component on the Components page
btn = I("3:1672", {
  "type": "FRAME",
  "name": "Button/Primary/sm",
  "reusable": true,
  "width": "hug_contents",
  "height": 24,
  "paddingLeft": 12,
  "paddingRight": 12,
  "paddingTop": 4,
  "paddingBottom": 4,
  "layout": "horizontal",
  "cornerRadius": 6,
  "primaryAxisAlignItems": "CENTER",
  "fills": [{"type": "SOLID", "color": {"r": 0.91, "g": 0.44, "b": 0.29},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "label", "characters": "Button",
      "fontSize": 12, "fill": "#FFFFFF"}
  ]
})
```

**Key points:**
- `width: "hug_contents"` — shrink to fit content (requires auto-layout)
- `width: "fill_container"` — expand to fill parent
- `layout: "horizontal"` — enable horizontal auto-layout (padding required)
- TEXT `fill` must be `"#HEX"` string format in I()
- Color values use 0–1 range ({r, g, b}) for SOLID fills
- `primaryAxisAlignItems`: `"MIN"` / `"CENTER"` / `"MAX"`
- `counterAxisAlignItems`: `"MIN"` / `"CENTER"` / `"MAX"`

### U() — Update Node

```js
// Bind a color variable to a TEXT node's fill
U("3:1676", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.61, "g": 0.59, "b": 0.56},
    "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}
  }]
})
```

### M() — Move Between Pages

```js
M("3:544", "3:1672")  // Move node 3:544 to Components page
```

- Node retains its original ID after moving
- Component instances are NOT broken by moving the source component

### C() — Create Component Instance

```js
C("3:544")  // Create instance of component 3:544
```

- Set x/y position via subsequent U() call

## 3. Variable Binding Patterns

### Color variable binding format (universal)

```json
"boundVariables": {
  "color": {"id": "VariableID:<variable-id>", "type": "VARIABLE_ALIAS"}
}
```

- In `fills[]`: `boundVariables.color` on each fill object
- In `strokes[]`: same format, on each stroke object
- `cornerRadius` binding: NOT supported (see Critical Rule 7)

### TEXT node: two-step binding

Step 1 — Create with `fill: "#HEX"` in I():
```js
I("0:1", {
  "type": "TEXT", "characters": "Hello",
  "fontSize": 14, "fill": "#333333"
})
```

Step 2 — Bind variable in a separate batch_edit U() call:
```js
U("<textNodeId>", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.2, "g": 0.2, "b": 0.2},
    "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}
  }]
})
```

### Variable ID format

```
"VariableID:3:14"  — prefix "VariableID:" + variable node ID
```

Obtain variable IDs from `apply_variables` return values or `fetch_variables`.

## 4. Validation & Recovery

### Validation workflow

After every batch of U() operations:
1. Run `batch_read` on the key nodes to verify property changes
2. Do NOT rely on `updated: {}` — it may be misleading
3. For visual verification, use `capture_screenshot` on the affected nodes
4. If something is wrong, fix in the next `batch_edit` call

### Error recovery

- Each `batch_edit` call is **atomic** — if the script fails, the file is unchanged
- On error: read the error message → fix the operations string → retry
- Most common causes: invalid node IDs, wrong pageId, syntax errors in the DSL string

## 5. Pre-Flight Checklist

Before submitting ANY `batch_edit` call, verify:

- [ ] Total operations ≤ 25 (recommend ≤ 20)
- [ ] All parent references use binding names from THIS call, NOT previous calls
- [ ] I() creates on the correct page (explicit pageId for cross-page)
- [ ] TEXT nodes use `fill: "#HEX"` (not fills array with boundVariables)
- [ ] U() and M() use real node IDs (not binding names from previous calls)
- [ ] M() targets are pageIds, not frameIds
- [ ] Color values in {r, g, b} 0–1 range, not 0–255
- [ ] cornerRadius uses hardcoded numeric value, not boundVariables
- [ ] All created node IDs are captured for later reference
- [ ] Auto-layout frames have `layout` + `padding*` properties set
- [ ] `fetch_editor_state(includeSchema: true)` has been called at least once

## 6. Error Matrix

| Error / Symptom | Likely Cause | How to Fix |
|---|---|---|
| `updated: {}` on U() | Normal — operation likely succeeded | Verify with batch_read, don't trust return value |
| Node created on wrong page | Missing explicit pageId in I() | Use `I("pageId", {...})` instead of `I({...})` |
| TEXT variable binding not working | Used fills+boundVariables in I() | Two-step: I() with fill:"#HEX", then U() with fills+boundVariables |
| Binding name not recognized | Using binding name from previous batch_edit | Use real node ID (e.g. "3:544") in the next call |
| cornerRadius variable not bound | Ardot doesn't support this | Use hardcoded value (e.g. cornerRadius: 6) |
| M() moved node to wrong place | Target was a frameId, not pageId | Ensure target is a page ID, not a frame ID |
| Can't discover other page IDs | batch_read without nodeIds only returns current page | Record page IDs from create_new_page return values |
| variableModes not taking effect | Feature may be unstable | Use separate pages for light/dark mode variants |

## 7. Reference Docs

| Reference | Content |
|-----------|---------|
| [Gotchas](references/gotchas.md) | All 8 known pitfalls with WRONG/CORRECT examples |
| [DSL Reference](references/dsl-reference.md) | Complete I/U/M/D/C/G operator reference |
| [Common Patterns](references/common-patterns.md) | Frequently used operation patterns |
| [Variable Patterns](references/variable-patterns.md) | apply_variables + batch_edit binding patterns |
| [Validation & Recovery](references/validation-and-recovery.md) | Verification workflow and error recovery strategies |