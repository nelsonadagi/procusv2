# Bug Investigation Prompt

```md
Investigate a bug in this repository.

Start by reading:
- `context/01-platform-overview.md`
- `context/04-backend-context.md`
- `context/05-frontend-context.md`
- `context/07-workflows.md`

Then:
- reproduce the issue from code and available tests
- identify whether it is a frontend bug, backend bug, API mismatch, workflow bug, or environment issue
- trace the exact files involved
- explain the root cause
- implement the safest fix
- add a test if feasible

Deliver:
- root cause
- fix
- verification
- any related risks
```
