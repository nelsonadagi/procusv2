# 🤝 Contributing to Procus v2

Thank you for your interest in contributing to Procus v2! As a massive multi-module construction marketplace, we rely on structured contributions to maintain system integrity.

---

## 🏗️ Development Standards

### Backend (Django)
- **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/).
- **Models**: Always use UUIDs for primary keys.
- **Transactions**: Financial operations must be wrapped in `transaction.atomic`.
- **API Versions**: When adding features to existing apps, consider if a new API version namespace is required (`v7+`).

### Frontend (Vue 3)
- **Style**: Components must be `<script setup>` SFCs.
- **CSS**: Use **Vanilla CSS** with our design system tokens. Do not introduce Tailwind or utility frameworks.
- **Scoped**: Always use `<style scoped>` in components.

---

## 🌿 Branching Strategy

We follow a simplified Gitflow model:

- `main`: Production-ready code.
- `develop`: Integration branch for features.
- `feature/*`: New features (e.g., `feature/payment-webhook`).
- `fix/*`: Bug fixes.

---

## 💬 Commit Message Convention

Internal policy requires [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

- `feat:` — A new feature.
- `fix:` — A bug fix.
- `docs:` — Documentation only changes.
- `style:` — Changes that do not affect the meaning of the code (white-space, formatting, etc).
- `refactor:` — A code change that neither fixes a bug nor adds a feature.
- `perf:` — A code change that improves performance.
- `test:` — Adding missing tests or correcting existing tests.
- `chore:` — Changes to the build process or auxiliary tools and libraries.

**Example:** `feat(escrow): add row-level locking for milestone releases`

---

## 🚀 Pull Request Process

1. Fork the repository and create your branch from `develop`.
2. Ensure any new backend logic has accompanying unit tests.
3. Update relevant documentation in the `docs/` folder if the PR changes architecture or user workflows.
4. Issue your Pull Request against the `develop` branch.
5. Once reviewed and passed CI, it will be merged.

---

## 🧪 Running Tests

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

---

*Procus v2 Engineering Team · 2026*
