# Common Patterns

> Part of the [ardot-use skill](../SKILL.md). Frequently used operation patterns for `batch_edit`.

## Contents

1. [Create a simple frame with auto-layout](#1-create-a-simple-frame-with-auto-layout)
2. [Create a reusable button component](#2-create-a-reusable-button-component)
3. [Bind color variables to fills](#3-bind-color-variables-to-fills)
4. [Create text with variable-bound color](#4-create-text-with-variable-bound-color)
5. [Create a card with children](#5-create-a-card-with-children)
6. [Move components to a Components page](#6-move-components-to-a-components-page)
7. [Create component instances and position them](#7-create-component-instances-and-position-them)
8. [Apply spacing between auto-layout children](#8-apply-spacing-between-auto-layout-children)

---

## 1. Create a simple frame with auto-layout

```js
wrapper = I("0:1", {
  "type": "FRAME",
  "name": "Login Screen",
  "width": 375,
  "height": "hug_contents",
  "layout": "vertical",
  "paddingLeft": 24,
  "paddingRight": 24,
  "paddingTop": 48,
  "paddingBottom": 48,
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}]
})
```

---

## 2. Create a reusable button component

```js
// On Components page (3:1672)
btnPrimary = I("3:1672", {
  "type": "FRAME",
  "name": "Button/Primary/md",
  "reusable": true,
  "width": "hug_contents",
  "height": 32,
  "layout": "horizontal",
  "paddingLeft": 16,
  "paddingRight": 16,
  "paddingTop": 6,
  "paddingBottom": 6,
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
```

---

## 3. Bind color variables to fills

```js
// Bind to a frame's background
U("3:914", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.96, "g": 0.96, "b": 0.96},
    "boundVariables": {
      "color": {"id": "VariableID:3:10", "type": "VARIABLE_ALIAS"}
    }
  }]
})

// Bind to a frame's border
U("3:915", {
  "strokes": [{
    "type": "SOLID",
    "color": {"r": 0.85, "g": 0.85, "b": 0.85},
    "boundVariables": {
      "color": {"id": "VariableID:3:11", "type": "VARIABLE_ALIAS"}
    }
  }]
})
```

**Variable ID format**: `"VariableID:<page>:<id>"` — e.g. `"VariableID:3:14"`.
Obtain IDs from `apply_variables` return values or `fetch_variables` output.

---

## 4. Create text with variable-bound color (two-step)

```js
// Step 1: Create the text node with hex fill
title = I("0:1", {
  "type": "TEXT",
  "name": "Page Title",
  "characters": "Welcome Back",
  "fontSize": 24,
  "fill": "#1A1A1A"
})
// Returns: title → "3:1680"

// Step 2 (separate batch_edit call): Bind the color variable
U("3:1680", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.1, "g": 0.1, "b": 0.1},
    "boundVariables": {
      "color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}
    }
  }]
})
```

---

## 5. Create a card with children

```js
card = I("0:1", {
  "type": "FRAME",
  "name": "Feature Card",
  "width": 320,
  "height": "hug_contents",
  "layout": "vertical",
  "paddingLeft": 20,
  "paddingRight": 20,
  "paddingTop": 20,
  "paddingBottom": 20,
  "cornerRadius": 12,
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
  "strokes": [{"type": "SOLID", "color": {"r": 0.9, "g": 0.9, "b": 0.9}}],
  "children": [
    {"type": "TEXT", "name": "Card Title", "characters": "Feature Name",
      "fontSize": 18, "fill": "#1A1A1A"},
    {"type": "TEXT", "name": "Card Body", "characters": "Description goes here.",
      "fontSize": 14, "fill": "#666666"}
  ]
})
```

---

## 6. Move components to a Components page

```js
// Create button on current page, then move to Components
btnSecondary = I("0:1", {
  "type": "FRAME", "name": "Button/Secondary/md",
  "reusable": true,
  "width": "hug_contents", "height": 32,
  "layout": "horizontal",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 6, "paddingBottom": 6,
  "cornerRadius": 8,
  "fills": [{"type": "SOLID", "color": {"r": 0.95, "g": 0.95, "b": 0.95}}],
  "children": [
    {"type": "TEXT", "characters": "Cancel", "fontSize": 14, "fill": "#333333"}
  ]
})
// Returns: btnSecondary → "3:545"

// Move it to Components page
M("3:545", "3:1672")
// Component remains at 3:545, now on Components page
```

**Alternative — create directly on Components page:**

```js
btnSecondary = I("3:1672", {
  "type": "FRAME", "name": "Button/Secondary/md",
  "reusable": true, ...
})
// Directly on Components page — no M() needed
```

---

## 7. Create component instances and position them

```js
// Create instances of a reusable button
btn1 = C("3:544")   // Button/Primary/md instance
btn2 = C("3:544")   // Another instance of the same component
// Returns: btn1 → "3:1200", btn2 → "3:1201"

// Position the instances
U("3:1200", {"x": 24, "y": 200})
U("3:1201", {"x": 200, "y": 200})
```

---

## 8. Apply spacing between auto-layout children

Use `counterAxisAlignItems: "CENTER"` for centering children in cross-axis, 
and `primaryAxisAlignItems` for main-axis alignment.

```js
nav = I("0:1", {
  "type": "FRAME", "name": "Nav Bar",
  "width": "fill_container", "height": 56,
  "layout": "horizontal",
  "paddingLeft": 16, "paddingRight": 16,
  "counterAxisAlignItems": "CENTER",
  "primaryAxisAlignItems": "MAX",  // Push content to the right
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
  "children": [
    {"type": "TEXT", "characters": "Logo", "fontSize": 18, "fill": "#1A1A1A"}
  ]
})
```

For explicit gaps between children, use `gap` property (if supported) or add 
spacer frames between items.