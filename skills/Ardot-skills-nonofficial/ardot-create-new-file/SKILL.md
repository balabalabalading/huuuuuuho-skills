---
name: ardot-create-new-file
description: |
  **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `create_new_page` tool call.
  NEVER call `create_new_page` directly without loading this skill first.

  Trigger whenever the user wants to create a new page in an Ardot design file.
  Keywords: "create a new page", "add a page", "new canvas" in the context of Ardot.
disable-model-invocation: false
---

# ardot-create-new-file — Create a New Ardot Page

Handles page creation in Ardot design files. Lightweight prerequisite skill that 
ensures proper page ID tracking and editor state management.

## Workflow

### Step 1: Determine the page name and position

Decide on a descriptive page name based on the user's intent:
- `"Components"` — for reusable component libraries
- `"Light Mode"` / `"Dark Mode"` — for theme-specific pages
- `"Screens"` — for design mockups
- Use `leftPageId` if the new page needs to appear after a specific existing page

### Step 2: Call create_new_page

```json
create_new_page({
  "name": "Components",
  "select": false
})
```

**Use `select: false`** by default — this creates the page without switching 
the editor focus, allowing you to continue working on the current page.

Use `select: true` only when you need to immediately switch to the new page 
for subsequent operations.

### Step 3: Record the returned pageId

The response includes the new page's ID. **Save this immediately** — there is 
no other way to discover page IDs later.

```
Example response: pageId = "3:1672"
```

Use this pageId for:
- Cross-page `I("3:1672", {...})` operations
- `M("nodeId", "3:1672")` to move nodes to this page
- `batch_read({parentId: "3:1672"})` to read this page's contents

## Important Notes

- **pageId discovery is limited**: `batch_read({})` without nodeIds only returns 
  the currently active page's contents. You cannot enumerate all pages via batch_read.
- **Record page IDs at creation time** — there is no `list_pages` tool.
- **`select: true`** (the default) switches the editor to the new page. This may 
  disrupt your workflow if you're building across multiple pages.
- **`leftPageId`** allows inserting the new page after a specific sibling page, 
  useful for maintaining page order.

## Cross-page Operations Reference

Once you have page IDs recorded:

| Operation | How | Example |
|-----------|-----|---------|
| Create on specific page | `I("pageId", {...})` | `I("3:1672", {type: "FRAME", ...})` |
| Move node to page | `M("nodeId", "pageId")` | `M("3:544", "3:1672")` |
| Read page contents | `batch_read({parentId: "pageId"})` | `batch_read({parentId: "3:1672"})` |
| Screenshot page contents | `capture_screenshot({nodeIds: [...]})` | Cross-page by node ID |