# Integration Fix Prompt

```md
Fix integration drift in this repository.

Start with:
- `context/12-api-truth-map.md`
- `context/13-role-permission-matrix.md`
- `context/14-known-gaps-and-mismatches.md`
- `context/15-build-order.md`
- `docs/VENDOR_INVENTORY_SYSTEM.md` when fixing vendor inventory or stock behavior

Then:
- compare the relevant frontend calls, backend routes, serializers, and workflow expectations
- identify the exact mismatch causing the problem
- prefer fixing the smallest number of files that restores alignment
- preserve backward compatibility where practical
- update context or docs if the implementation truth changes
- if the drift touches inventory, compare product serializers, stock mutations, and order reconciliation together

Possible drift types:
- wrong route namespace
- wrong HTTP method
- wrong payload shape
- missing backend action
- frontend assumes stale behavior
- docs describe a non-live contract

Deliver:
- root cause
- implementation changes
- verification
- any docs/context updates needed
```
