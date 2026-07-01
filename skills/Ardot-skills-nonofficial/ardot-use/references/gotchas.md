# Gotchas & Common Mistakes

> Part of the [ardot-use skill](../SKILL.md). Every known pitfall with WRONG/CORRECT code examples.

## Contents

1. [updated: {} doesn't mean failure](#1-updated--doesnt-mean-failure)
2. [Binding names expire after each batch_edit](#2-binding-names-expire-after-each-batch_edit)
3. [cornerRadius variable binding not supported](#3-cornerradius-variable-binding-not-supported)
4. [TEXT nodes can't bind variables in I()](#4-text-nodes-cant-bind-variables-in-i)
5. [variableModes are unreliable](#5-variablemodes-are-unreliable)
6. [Cross-page insertion needs explicit pageId](#6-cross-page-insertion-needs-explicit-pageid)
7. [batch_read can't discover all page IDs](#7-batch_read-cant-discover-all-page-ids)
8. [M() target parent and index must be valid](#8-m-target-parent-and-index-must-be-valid)

---

## 1. updated: {} doesn't mean failure

**Symptom**: U() returns `updated: {}` instead of `updated: {"nodeId": {...}}`, 
making it look like the update didn't take effect.

**Reality**: The operation actually succeeded — this is just how the response format 
works for certain updates.

```js
// WRONG — assuming the update failed because of empty response
U("3:544", {"cornerRadius": 8})
// Returns: updated: {} 
// → "It didn't work, let me try again or do it differently"
```

```js
// CORRECT — verify with batch_read instead of trusting return value
U("3:544", {"cornerRadius": 8})
// Returns: updated: {} 
// → "Let me batch_read node 3:544 to check if cornerRadius is now 8"
batch_read({nodeIds: ["3:544"]})
// → cornerRadius: 8 confirmed
```

---

## 2. Binding names expire after each batch_edit

**Symptom**: Using a binding name from a previous `batch_edit` call in a new call 
causes the operation to fail or target the wrong node.

**Reality**: Binding names (`btn1`, `label2`, etc.) are temporary — they only exist 
during the single `batch_edit` call they were created in.

```js
// WRONG — using binding name from previous call
// Call 1:
btn = I("0:1", {"type": "FRAME", "name": "Button", ...})
// Call 2:
U("btn", {"cornerRadius": 8})  // ❌ "btn" is NOT recognized here
```

```js
// CORRECT — using real node ID in subsequent calls
// Call 1:
btn = I("0:1", {"type": "FRAME", "name": "Button", ...})
// Returns binding: btn → real ID "3:544"
// Call 2:
U("3:544", {"cornerRadius": 8})  // ✅ Use the real node ID
```

**Always record the real node IDs** returned from each batch_edit response.

---

## 3. cornerRadius variable binding not supported

**Symptom**: Attempting to bind a radius variable to `cornerRadius` returns 
`updated: {}` and re-reading the node shows `boundVariables` is empty.

```js
// WRONG — Ardot doesn't support this yet
U("3:544", {
  "cornerRadius": 6,
  "boundVariables": {
    "cornerRadius": {"id": "VariableID:3:30", "type": "VARIABLE_ALIAS"}
  }
})
// Returns: updated: {} — variable was NOT bound
```

```js
// CORRECT — use hardcoded numeric values
U("3:544", {"cornerRadius": 6})
```

---

## 4. TEXT nodes can't bind variables in I()

**Symptom**: When creating a TEXT node inside I(), using `fills: [{boundVariables: {...}}]` 
doesn't work — the variable binding is silently ignored.

```js
// WRONG — variable binding in I() for TEXT is silently ignored
I("0:1", {
  "type": "FRAME", "name": "Card",
  "children": [
    {"type": "TEXT", "characters": "Hello",
      "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.2, "b": 0.2},
        "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}}]
    }
  ]
})
```

```js
// CORRECT — two-step approach
// Step 1: Create TEXT with hex fill
label = I("0:1", {
  "type": "TEXT", "characters": "Hello",
  "fontSize": 14, "fill": "#333333"
})
// Returns: label → "3:1676"

// Step 2: Bind variable in a separate call
U("3:1676", {
  "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.2, "b": 0.2},
    "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}}]
})
```

---

## 5. variableModes are unreliable

**Symptom**: Setting `variableModes` on a frame to switch between Light/Dark mode 
returns `updated: {}` and may not take effect.

```js
// WRONG — may not work reliably
U("3:914", {"variableModes": {"3:2": "3:3"}})
// Returns: updated: {} — can't confirm if mode switched
```

```js
// CORRECT — use dedicated pages per mode
// Light Mode page: use light color values directly
// Dark Mode page: use dark color values directly
// Each page has its own frames with hardcoded mode-appropriate values
```

---

## 6. Cross-page insertion needs explicit pageId

**Symptom**: Trying to create a node on the Components page, but it appears on the 
currently active page instead.

```js
// WRONG — node ends up on current page (e.g. Dark Mode page)
I({"type": "FRAME", "name": "Button", "reusable": true, ...})
// Created on the wrong page!
```

```js
// CORRECT — explicitly specify the target page ID
I("3:1672", {"type": "FRAME", "name": "Button", "reusable": true, ...})
// Created on Components page (3:1672) as intended
```

---

## 7. batch_read page discovery is limited

**Symptom**: Calling `batch_read({})` without nodeIds only returns the top-level
children for the current context, which is not a reliable way to enumerate all pages
in a large document.

```js
// WRONG — assuming this returns ALL pages in the file
batch_read({})  
// It may only return the current context, depending on editor state
```

```js
// CORRECT — record page IDs at creation time and store them in your handoff/manifest
// When creating pages:
page = create_new_page({name: "Components", select: false})
// → Returns pageId: "3:1672" — SAVE THIS

// To read from a known page, use the page ID or a known node ID:
batch_read({nodeIds: ["3:1672"]})
batch_read({nodeIds: ["3:914"]})  // Cross-page read works with known IDs
```

---

## 8. M() target parent and index must be valid

**Symptom**: Attempting to move a node via M() doesn't work as expected, or the node
appears in the wrong layer order.

```js
// WRONG — target parent does not exist, or index is invalid for that parent's children
M("3:544", "missing-parent")
M("3:544", "3:100", 999)
```

```js
// CORRECT — use a valid page or frame parent, optionally with a valid index
M("3:544", "3:1672")     // move to Components page
M("3:544", "3:100", 0)   // move into frame 3:100 as first child

// Then verify:
batch_read({nodeIds: ["3:100"], properties: ["children"], readDepth: 1})
```
