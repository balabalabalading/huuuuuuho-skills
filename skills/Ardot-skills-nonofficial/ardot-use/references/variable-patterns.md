# Variable Patterns

> Part of the [ardot-use skill](../SKILL.md). Patterns for creating and binding variables 
> with `apply_variables` and `batch_edit`.

## Contents

1. [Creating color variables with modes](#1-creating-color-variables-with-modes)
2. [Creating spacing/number variables](#2-creating-spacingnumber-variables)
3. [Binding variables in batch_edit](#3-binding-variables-in-batch_edit)
4. [Two-step TEXT variable binding](#4-two-step-text-variable-binding)
5. [Variable ID tracking workflow](#5-variable-id-tracking-workflow)
6. [Scope reference](#6-scope-reference)

---

## 1. Creating color variables with modes

```json
// apply_variables call
{
  "variables": {
    "Colors": {
      "modes": ["Dark", "Light"],
      "variables": {
        "bg-primary": {
          "type": "COLOR",
          "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.08, "g": 0.08, "b": 0.08, "a": 1},
            "Light": {"r": 1, "g": 1, "b": 1, "a": 1}
          }
        },
        "accent-warm": {
          "type": "COLOR",
          "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.91, "g": 0.44, "b": 0.29, "a": 1},
            "Light": {"r": 0.83, "g": 0.38, "b": 0.23, "a": 1}
          }
        },
        "text-primary": {
          "type": "COLOR",
          "scopes": ["TEXT_FILL"],
          "valuesByMode": {
            "Dark": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1},
            "Light": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}
          }
        }
      }
    }
  }
}
```

**Key rules:**
- Variable names do NOT include `$` or `:` prefix (use `accent-warm`, not `$accent-warm`)
- `collection` is a string name (not an ID) — e.g. `"Colors"`
- COLOR values use `{r, g, b, a}` 0–1 range
- Create all variables BEFORE binding them in batch_edit

## 2. Creating spacing/number variables

```json
{
  "variables": {
    "Spacing": {
      "modes": ["Dark", "Light"],
      "variables": {
        "spacing-sm": {
          "type": "FLOAT",
          "scopes": ["GAP"],
          "valuesByMode": {"Dark": 8, "Light": 8}
        },
        "spacing-md": {
          "type": "FLOAT",
          "scopes": ["GAP"],
          "valuesByMode": {"Dark": 16, "Light": 16}
        },
        "radius-sm": {
          "type": "FLOAT",
          "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 6, "Light": 6}
        }
      }
    }
  }
}
```

**Warning**: `CORNER_RADIUS` scope variables may not actually bind (see gotcha #3). 
Create them but use hardcoded values for `cornerRadius` in batch_edit.

## 3. Binding variables in batch_edit

### Fills binding (frame background)

```js
U("3:914", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.08, "g": 0.08, "b": 0.08},
    "boundVariables": {
      "color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}
    }
  }]
})
```

### Strokes binding (border)

```js
U("3:915", {
  "strokes": [{
    "type": "SOLID",
    "color": {"r": 0.85, "g": 0.85, "b": 0.85},
    "boundVariables": {
      "color": {"id": "VariableID:3:15", "type": "VARIABLE_ALIAS"}
    }
  }]
})
```

### Binding in I() (for non-TEXT nodes)

Frame fills CAN include boundVariables directly in I():

```js
frame = I("0:1", {
  "type": "FRAME",
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}]
})
```

But TEXT nodes inside I() CANNOT — use two-step binding (see below).

## 4. Two-step TEXT variable binding

```js
// Step 1: Create TEXT with hex fill
label = I("0:1", {
  "type": "FRAME", "name": "Card",
  "children": [
    {"type": "TEXT", "name": "title", "characters": "Hello World",
      "fontSize": 16, "fill": "#1A1A1A"}
  ]
})
// Returns: label → "3:1200", and the TEXT child gets a node ID like "3:1201"

// Step 2 (separate batch_edit call): Bind variable to text
U("3:1201", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.1, "g": 0.1, "b": 0.1},
    "boundVariables": {
      "color": {"id": "VariableID:3:16", "type": "VARIABLE_ALIAS"}
    }
  }]
})
```

## 5. Variable ID tracking workflow

```
1. apply_variables → record all returned VariableID values
2. batch_edit (I) → record all returned node IDs
3. batch_edit (U) → use VariableID + nodeID to bind
4. batch_read → verify bindings took effect
```

**Important**: Variable IDs have format `"VariableID:<page>:<id>"`. 
The page/id portion is NOT the same as the node ID of the variable — 
it's a separate namespace.

## 6. Scope reference

| Scope | Applies To |
|-------|-----------|
| `ALL_FILLS` | Any node's fill color |
| `FRAME_FILL` | Frame backgrounds only |
| `SHAPE_FILL` | Shape fills only |
| `TEXT_FILL` | Text color only |
| `STROKE` | Border/stroke colors |
| `CORNER_RADIUS` | Border radius (**may not work** — see gotcha) |
| `GAP` | Auto-layout gap spacing |
| `WIDTH_HEIGHT` | Width and height dimensions |
| `OPACITY` | Layer opacity |
| `FONT_SIZE` | Font size |
| `LINE_HEIGHT` | Line height |
| `LETTER_SPACING` | Letter spacing |
| `ALL_SCOPES` | All of the above |