# Frontend Style Guide

This frontend uses the **Paanguzo** design language: industrial, precise, high-contrast, and premium without drifting into generic SaaS visuals.

## 1. Source Of Truth

Design tokens now center on:

- `src/styles/variables.css`: primary Paanguzo brand tokens
- `src/styles/base.css`: typography, resets, and global atmosphere
- `src/styles/layout.css`: layout, nav, hero, dashboard, and shell patterns
- `src/styles/components.css`: compatibility layer for older `c-*` styles
- `src/styles/tokens.css`: legacy token bridge for older files

Use `variables.css` as the real source of truth.

## 2. Visual Direction

### Brand palette

- foundation black
- structural steel
- limestone white
- earth orange
- copper circuit
- steel blue
- savanna green
- african violet

### Typography

- `Sora` for display headlines and major brand moments
- `IBM Plex Sans` for body and interface copy
- `IBM Plex Mono` for labels, telemetry, badges, metrics, and system language

### Shape language

- sharp to lightly radiused edges
- strong borders
- structural panel separation
- restrained shadows
- limited, purposeful glass effects

## 3. Styling Rules

1. Prefer `pz-*` classes and components over legacy `c-*` patterns for new work.
2. Use `Button`, `Card`, `Badge`, and `Modal` from `src/components/ui/` for shared primitives.
3. Do not introduce new ad hoc color values in components. Use CSS variables.
4. Reserve accent colors semantically:
   - earth = primary action
   - copper = finance
   - steel blue = info/system
   - savanna = success
   - violet = innovation/AI
5. Keep display typography intentional. Not every heading should look like a hero.

## 4. Preferred Component Feel

### Buttons

- mono labels
- uppercase by default
- strong border presence
- offset or structural shadow on major actions

### Cards

- clear frame
- quiet header treatment
- high legibility
- hover lift only where interactive

### Badges

- mono labels
- uppercase
- bordered pills or capsules
- compact and scannable

### Modals

- dark command header
- strong frame
- minimal ornament

## 5. Layout Principles

- mobile first
- use grid for dashboards and index pages
- use mono labels to establish hierarchy in operational screens
- avoid overusing glow, blur, and floating effects
- use atmospheric backgrounds sparingly and consistently

## 6. Migration Guidance

If you touch an older file that still depends on the legacy token system:

- do not rewrite everything blindly
- map it onto Paanguzo tokens
- preserve behavior
- reduce visual drift rather than creating a third design language
