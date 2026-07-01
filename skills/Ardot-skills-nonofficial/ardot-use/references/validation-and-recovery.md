# Validation & Recovery

> Part of the [ardot-use skill](../SKILL.md). Verification workflows and error recovery 
> strategies for Ardot operations.

## Contents

1. [Validation workflow](#1-validation-workflow)
2. [Using batch_read for verification](#2-using-batch_read-for-verification)
3. [Using capture_screenshot for visual checks](#3-using-capture_screenshot-for-visual-checks)
4. [Error recovery flow](#4-error-recovery-flow)
5. [Recommended workflow per operation type](#5-recommended-workflow-per-operation-type)

---

## 1. Validation workflow

After each batch of `batch_edit` calls, follow this verification flow:

```
1. batch_edit    →  Create / modify nodes
2. batch_read    →  Verify structure: node IDs, names, property values
3. [if issues]   →  batch_edit to fix
4. capture_screenshot → Visual check of key screens
5. [if issues]   →  batch_edit to fix → capture_screenshot again
```

**Golden rule**: Never assume an operation succeeded. Always verify.

## 2. Using batch_read for verification

### Check a specific node's properties

```json
// Read a node to verify its current state
batch_read({nodeIds: ["3:914"]})
```

Check for:
- `fills` — are boundVariables present?
- `cornerRadius` — is the value correct?
- `name` — is the node name what you expect?
- `children` — are all expected children present?
- `layout` — is auto-layout enabled?

### Check a page's structure

```json
// Read top-level nodes for the current context
batch_read({})

// Read a specific page's children (cross-page)
batch_read({nodeIds: ["3:1672"], properties: ["children"], readDepth: 1})
```

### The `updated: {}` verification pattern

```js
// Your U() call
U("3:544", {"cornerRadius": 8})
// Returns: updated: {}

// DON'T assume failure — VERIFY:
batch_read({nodeIds: ["3:544"]})
// → Check if cornerRadius is now 8
```

## 3. Using capture_screenshot for visual checks

```json
// Screenshot specific nodes (up to 10 per call)
capture_screenshot({
  "nodeIds": ["3:914", "3:940", "3:1185"],
  "screenShotDir": "/tmp/ardot-verify"
})
```

**Best practices:**
- Screenshot AFTER structural verification (batch_read), not before
- Batch all screenshots into one call (≤10 nodes)
- Review ALL returned images for visual issues (misalignment, overflow, clipping)
- Re-screenshot after any fixes
- Avoid screenshotting oversized nodes (>2000px in either dimension) — screenshot sections individually

### What to look for in screenshots:
- Text clipping or overflow
- Misaligned elements
- Incorrect colors
- Missing elements
- Unexpected spacing

## 4. Error recovery flow

```
Operation fails
  │
  ├─ Read the error message carefully
  │   Common causes:
  │   - Invalid node ID (using binding name from previous call)
  │   - Wrong parentId or invalid insertion index
  │   - Syntax error in DSL string
  │   - Exceeded 25 operations limit
  │
  ├─ Fix the root cause
  │   - Replace binding names with real node IDs
  │   - Verify parentId exists and the index is valid for its children
  │   - Check JSON syntax in the operations string
  │   - Split into multiple calls if over 25 operations
  │
  └─ Retry the batch_edit call
      (The file was NOT modified by the failed call — batch_edit is atomic)
```

**Important**: Each `batch_edit` call is **atomic**. If the operations string has an error, 
none of the operations are applied. The file remains in its previous state. So you can 
safely fix and retry.

## 5. Recommended workflow per operation type

### For creating new structures (I)

```
1. I() → create nodes with basic properties
2. batch_read → verify nodes exist with correct names and types
3. U() → add variable bindings, adjust positions
4. batch_read → verify bindings
5. capture_screenshot → visual check
```

### For updating existing nodes (U)

```
1. U() → update properties
2. batch_read → verify property changes (especially boundVariables)
3. capture_screenshot → visual check if appearance changed
```

### For moving nodes (M)

```
1. M() → move node
2. batch_read({nodeIds: ["targetParentId"], properties: ["children"], readDepth: 1})
   → verify node appears under the target parent in the intended order
```

### For creating instances (C)

```
1. C("componentId", "parentId", {x, y, width, height}) → create instance
2. batch_read({nodeIds: ["parentId"], properties: ["children"], readDepth: 1})
   → verify instance appears under the target parent
3. capture_screenshot → verify instance appears correctly positioned
```

### For building a full page

```
1. create_new_page → setup
2. batch_edit (I) → create page skeleton (wrapper frame + sections)
3. batch_read → verify structure
4. batch_edit (U) → add variable bindings
5. batch_read → verify bindings
6. capture_screenshot → visual check of entire page
7. [iterate 2-6 for each section until complete]
```
