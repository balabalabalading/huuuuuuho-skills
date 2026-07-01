# DSL Reference — batch_edit Operators

> Part of the [ardot-use skill](../SKILL.md). Complete reference for all `batch_edit` DSL operators.

## Contents

1. [I() — Insert Node](#i--insert-node)
2. [U() — Update Node](#u--update-node)
3. [M() — Move Node](#m--move-node)
4. [D() — Delete Node](#d--delete-node)
5. [C() — Create Component Instance](#c--create-component-instance)
6. [G() — Generate Image](#g--generate-image)
7. [Common Properties](#common-properties)

---

## I() — Insert Node

Creates a new node on a specified page. Every I() call MUST include a binding name.

```
bindingName = I("pageId", {nodeProperties})
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `pageId` | Yes | Target page ID (e.g. `"3:1672"`, or use `"0:1"` for default page) |
| `nodeProperties` | Yes | Object describing the node to create |

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | `"FRAME"`, `"TEXT"`, `"RECTANGLE"`, `"ELLIPSE"`, etc. |
| `name` | string | Display name in the layer panel |
| `reusable` | boolean | Set `true` to create a component (only for FRAME type) |
| `width` | number or string | Numeric px value, `"hug_contents"`, or `"fill_container"` |
| `height` | number or string | Numeric px value, `"hug_contents"`, or `"fill_container"` |
| `x` | number | X position (optional; 0 if omitted) |
| `y` | number | Y position (optional; 0 if omitted) |
| `layout` | string | `"horizontal"` or `"vertical"` — enables auto-layout |
| `paddingLeft/Right/Top/Bottom` | number | Inner padding (px) — requires `layout` |
| `primaryAxisAlignItems` | string | `"MIN"`, `"CENTER"`, `"MAX"` |
| `counterAxisAlignItems` | string | `"MIN"`, `"CENTER"`, `"MAX"` |
| `fills` | array | Array of fill objects (see fills format below) |
| `strokes` | array | Array of stroke objects |
| `cornerRadius` | number | Border radius in px |
| `characters` | string | Text content (TEXT type only) |
| `fontSize` | number | Font size (TEXT type only) |
| `fill` | string | Text color as `"#HEX"` (TEXT type in I() only) |
| `children` | array | Array of child node objects |

### Fills format

```json
{
  "type": "SOLID",
  "color": {"r": 0.91, "g": 0.44, "b": 0.29},
  "boundVariables": {
    "color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}
  }
}
```

Colors use **0–1 range** (not 0–255, not hex).

### TEXT node in I() — special rule

TEXT children inside I() MUST use `"fill": "#HEX"` string format. They CANNOT use 
`fills: [{boundVariables: {...}}]`. Variable binding must be done in a separate 
U() call after creation.

### Examples

```js
// Simple frame with auto-layout
card = I("0:1", {
  "type": "FRAME", "name": "Card",
  "width": 320, "height": "hug_contents",
  "layout": "vertical",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 16, "paddingBottom": 16,
  "cornerRadius": 12,
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}]
})

// Reusable component on Components page
btn = I("3:1672", {
  "type": "FRAME", "name": "Button/Primary/md",
  "reusable": true,
  "width": "hug_contents", "height": 32,
  "layout": "horizontal",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 6, "paddingBottom": 6,
  "cornerRadius": 8,
  "primaryAxisAlignItems": "CENTER",
  "fills": [{"type": "SOLID", "color": {"r": 0.91, "g": 0.44, "b": 0.29},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "label", "characters": "Button",
      "fontSize": 14, "fill": "#FFFFFF"}
  ]
})
```

---

## U() — Update Node

Modifies properties of an existing node.

```
U("nodeId", {propertiesToUpdate})
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `nodeId` | Yes | Real node ID (e.g. `"3:544"`) — NOT a binding name from a previous call |
| `properties` | Yes | Object with only the properties to change |

### Examples

```js
// Bind color variable to existing frame fill
U("3:914", {
  "fills": [{"type": "SOLID", "color": {"r": 0.96, "g": 0.96, "b": 0.96},
    "boundVariables": {"color": {"id": "VariableID:3:10", "type": "VARIABLE_ALIAS"}}}]
})

// Change corner radius (hardcoded — variable binding not supported)
U("3:914", {"cornerRadius": 12})

// Set position
U("3:544", {"x": 100, "y": 200})
```

---

## M() — Move Node

Moves a node to a new parent. The parent may be a page or a frame.

```
M("nodeId", "parentId", index?)
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `nodeId` | Yes | Node to move |
| `parentId` | Yes | Target parent node ID. Can be a page or frame. |
| `index` | No | Optional insertion index among the target parent's children |

### Notes

- Node retains its original ID after moving.
- Component instances remain connected to their source component after moving.
- After moving, verify the target parent's `children` order with `batch_read`.

### Example

```js
M("3:544", "3:1672")     // Move button to Components page
M("3:544", "3:200", 0)   // Move button into frame 3:200 at index 0
```

---

## D() — Delete Node

Deletes a node and all its children.

```
D("nodeId")
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `nodeId` | Yes | Node to delete |

### Warning

Deleting a parent node **cascades** — all children are also deleted. 
Be careful when deleting frames that contain many children.

```js
D("3:544")  // Deletes node 3:544 and all its descendants
```

---

## C() — Create Component Instance

Creates an instance of a reusable component under a parent node.

```
bindingName = C("componentId", "parentId", copyNodeData?)
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `componentId` | Yes | ID of the reusable component to instantiate |
| `parentId` | Yes | Parent node to receive the instance |
| `copyNodeData` | No | Optional overrides such as x/y, width/height, or descendants |

### Notes

- Instance inherits all properties from the source component
- Position and size may be set in `copyNodeData`; use subsequent U() only when needed
- Changes to the source component propagate to all instances
- Use `descendants` in `copyNodeData` when overriding children inside copied component instances

```js
instance = C("3:544", "3:200", {x: 24, y: 200})  // Create instance of component 3:544 inside parent 3:200
// Returns binding: instance → "3:1200"
```

---

## G() — Generate Image

Applies an AI-generated or stock image fill to an existing frame/shape node.
Use sparingly — results are non-deterministic and slow.

```
imageFrame = I("3:1672", {type: "FRAME", name: "Hero Image", width: 400, height: 240})
G(imageFrame, "ai", "clean dashboard hero image")
G("3:544", "stock", "")
```

There is no standalone image node type. Create a frame or shape first, then use
G() to apply the image as that node's fill.

---

## Common Properties

### Layout properties (auto-layout frames)

| Property | Values | Description |
|----------|--------|-------------|
| `layout` | `"horizontal"`, `"vertical"` | Enables auto-layout |
| `width` | number, `"hug_contents"`, `"fill_container"` | Width behavior |
| `height` | number, `"hug_contents"`, `"fill_container"` | Height behavior |
| `paddingLeft` | number | Left inner padding (px) |
| `paddingRight` | number | Right inner padding (px) |
| `paddingTop` | number | Top inner padding (px) |
| `paddingBottom` | number | Bottom inner padding (px) |
| `primaryAxisAlignItems` | `"MIN"`, `"CENTER"`, `"MAX"` | Alignment along main axis |
| `counterAxisAlignItems` | `"MIN"`, `"CENTER"`, `"MAX"` | Alignment along cross axis |

### Color format

All colors use **0–1 range** for r, g, b components:
```json
{"r": 0.91, "g": 0.44, "b": 0.29}
```

This represents a warm orange (#E8714A in hex → r=232/255≈0.91, g=113/255≈0.44, b=74/255≈0.29).
