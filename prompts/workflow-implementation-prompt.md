# Workflow Implementation Prompt

```md
Implement or refine a business workflow in this repository.

Start with:
- `context/01-platform-overview.md`
- `context/03-phases-and-domains.md`
- `context/07-workflows.md`
- `context/08-security-compliance-and-risk.md`
- `docs/VENDOR_INVENTORY_SYSTEM.md` when the workflow touches supplier stock

Then:
- identify the full workflow from trigger to completion
- map which apps own each step
- identify statuses, transitions, permissions, and edge cases
- confirm where notifications, disputes, audit logging, or holds should apply
- implement the missing workflow pieces with minimal duplication
- if inventory is involved, define when stock commits, restores, or logs movement events

Examples of workflows:
- quote request to order
- tender to awarded contract
- milestone approval to escrow release
- onboarding to KYC approval
- project commitment to agreement

Deliver:
- updated workflow behavior
- touched modules
- status model or transition logic
- tests or verification steps
```
