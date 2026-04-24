# Release Readiness Prompt

```md
Prepare this repository for a stable release candidate.

Read first:
- `context/11-implementation-status.md`
- `context/12-api-truth-map.md`
- `context/14-known-gaps-and-mismatches.md`
- `context/15-build-order.md`
- `context/09-deployment-and-operations.md`

Then inspect:
- backend settings and URLs
- frontend API usage
- test configuration
- Docker and environment files
- auth and permission setup
- critical workflows

Your output should include:
- release blockers
- high-risk mismatches
- environment blockers
- must-pass workflows
- recommended fixes in priority order
- a short go/no-go assessment
```
