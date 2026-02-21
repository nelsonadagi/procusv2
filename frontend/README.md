# Frontend — Procus v2

Vue 3 + Vite single-page application for the Procus v2 Construction Marketplace.

## Tech Stack

- **Vue 3** with `<script setup>` SFCs
- **Vite 7** — lightning-fast dev server & bundler
- **Vue Router 5** — client-side routing
- **Pinia 3** — state management
- **Axios** — HTTP client
- **Vanilla CSS** — custom design system (no Tailwind/Bootstrap)

## Development

```bash
npm install
npm run dev       # Start dev server at http://localhost:5173
npm run build     # Production bundle
npm run preview   # Preview production build
```

## Structure

```
src/
├── views/        # 20 role-specific page components
├── components/   # Reusable UI (Button, Badge, Modal, Card ...)
├── styles/       # Design system CSS (tokens, base, layout, components)
├── stores/       # Pinia state stores
├── services/     # Axios API service layer
├── router/       # Vue Router configuration
├── App.vue       # Root component
└── main.js       # Entry point
```

## Environment

Set the backend API URL via the environment variable:

```env
VITE_API_URL=http://localhost:8000/api
```

## Style Guide

See [`FRONTEND_STYLE_GUIDE.md`](./FRONTEND_STYLE_GUIDE.md) for design tokens, component usage, and CSS authoring rules.
