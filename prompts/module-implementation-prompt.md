# Module Implementation Prompt

```md
Implement or complete a specific module in this repository.

Read first:
- `context/11-implementation-status.md`
- `context/12-api-truth-map.md`
- `context/13-role-permission-matrix.md`
- `context/15-build-order.md`

Then inspect the relevant code for the target module.

Your job:
- identify whether the module is already partially implemented
- identify its owning backend app and related frontend surfaces
- identify missing routes, serializers, views, tests, and UI integrations
- distinguish implementation gaps from integration gaps
- implement the missing pieces in the smallest coherent slice
- do not create duplicate endpoints if an app-level or versioned route already exists

Deliver:
- module status before changes
- changes made
- routes affected
- permissions affected
- tests or verification steps
- remaining gaps
```
