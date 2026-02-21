# Frontend Style Guide & Design System

This project uses a **Vanilla CSS Design System** without utility libraries (No Tailwind, No Bootstrap).
The system is built on modern CSS features: Variables (Custom Properties), Flexbox, and Grid.

## 1. Directory Structure (`src/styles/`)

We strictly separate concerns:

- `tokens.css`: **The Source of Truth**. Hex codes, spacing units, and raw values.
- `base.css`: CSS Resets and element defaults (h1, p, a).
- `layout.css`: Global layout helpers (.container, .grid, .flex).
- `components.css`: Reusable UI classes (.btn, .card, .input).
- `style.css`: The main entry point (imports all others).

## 2. Design Tokens available

Use these CSS variables instead of hardcoded values.

### Colors
| Brand | Variable | Hex |
|-------|----------|-----|
| Primary | `--color-primary` | #1a73e8 |
| Secondary | `--color-secondary` | #ff6d00 |
| Background | `--color-bg-body` | #f4f6f9 |

### Spacing
Scale: 4px increments.
`--space-1` (4px), `--space-2` (8px), `--space-4` (16px), `--space-6` (24px), `--space-8` (32px).

## 3. Component Usage

### Buttons (`.btn`)
Use the `<Button>` Vue component or `.btn` classes.

```html
<button class="btn btn-primary">Action</button>
<button class="btn btn-outline btn-sm">Small</button>
```

### Cards (`.card`)
Use `<Card>` or standard markup:

```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>
```

### Badges (`.badge`)
Status indicators:
- `.badge-success` (In Stock, Verified)
- `.badge-warning` (Pending)
- `.badge-danger` (Out of stock)

## 4. Layout Principles

### Container
Wrap page content in `.container` (max-width 1280px).

### Grid System
Use CSS Grid for layouts.

```css
.my-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}
```

### Flexbox Utilities
Common helpers are available in `layout.css`:
- `.flex`
- `.justify-between`
- `.items-center`
- `.gap-4`

## 5. CSS Authoring Rules

1.  **Semantic Classes**: Use `.product-card`, not `.p-4.bg-white.rounded`.
2.  **Scoped Styles**: In Vue components, always use `<style scoped>`.
3.  **Variables**: Never use hex codes in component styles. Use `var(--color-primary)`.
4.  **Mobile First**: Write base styles for mobile, then use `@media (min-width: 768px)` for desktop.

## 6. Migration Guide (Tailwind Removal)

Tailwind has been completely removed.
- **Do not use**: `text-xl`, `p-4`, `flex-row`.
- **Use**: Normal CSS properties with our variables.
