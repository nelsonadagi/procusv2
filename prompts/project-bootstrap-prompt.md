# Project Bootstrap Prompt

Use this when you want the assistant to load the project correctly before doing any work.

```md
You are working inside the `construction-marketplace` repository.

Before making changes:
- Read `context/README.md`
- Read `context/01-platform-overview.md`
- Read `context/02-architecture.md`
- Read `context/10-source-map.md`
- Inspect the relevant code before proposing or changing anything

Your job:
- Build context from the curated `context/` folder first
- Use the original docs in `docs/` only when extra detail is needed
- Identify the backend app, frontend route, API namespace, and workflow affected
- Call out any mismatch between documentation, frontend usage, and backend implementation
- Then implement or analyze the requested task carefully
```
