# Testing And Verification Prompt

```md
Verify the changes in this repository thoroughly.

Before testing:
- read `context/09-deployment-and-operations.md`
- inspect the relevant test files
- confirm whether the project expects Docker services, PostGIS, Redis, or local fallbacks

Then:
- run the most relevant tests first
- note environment blockers clearly if they prevent execution
- distinguish setup failures from application logic failures
- identify missing tests for the changed behavior
- suggest the minimum additional tests needed for confidence

Deliver:
- commands run
- results
- blockers
- residual risks
```
