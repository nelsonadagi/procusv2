# API Alignment Prompt

```md
Audit and fix API alignment issues in this repository.

Read first:
- `context/04-backend-context.md`
- `context/05-frontend-context.md`
- `context/10-source-map.md`

Your goal:
- compare frontend API calls against backend URL registrations
- identify broken, outdated, or inconsistent namespaces
- identify payload mismatches between frontend requests and backend serializers/views
- identify documentation drift in `docs/`
- propose the smallest safe set of changes to realign the system

Output format:
- findings ordered by severity
- affected frontend files
- affected backend files
- recommended fixes
- optional implementation plan
```
