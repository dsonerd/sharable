# Project Backlog

## Active Tasks
| ID | Task | Category | Assigned To | Status | Created | Updated |
|----|------|----------|-------------|--------|---------|---------|
| TCL-003 | Monitoring roadmap v2.0 — CIO re-review | solution | tcl-cio | todo | 2026-03-20 | 2026-03-20 |

## Completed Tasks
| ID | Task | Category | Completed By | Completed Date |
|----|------|----------|-------------|----------------|
| TCL-000 | Monitoring & alerting roadmap — draft | solution | tcl-orch | 2026-03-20 |
| TCL-001 | Monitoring & alerting roadmap — CIO review | solution | tcl-cio | 2026-03-20 |
| TCL-002 | Monitoring roadmap — restructure into overview + detail, incorporate CIO feedback | solution | tcl-orch | 2026-03-20 |

## Notes / Decisions
- TCL-000: Comprehensive 4-phase roadmap covering infrastructure, application, business, and security monitoring. Cross-references existing incident management backlog items IM-005, IM-009, IM-015, IM-018. No duplicate work found — existing dashboard files are tactical (Grafana TV); this roadmap is strategic.
- TCL-001: CIO review completed. 43 findings (10 high, 21 medium, 12 low). Conditionally approved. Top 5 blockers: staffing plan, regulatory citations, missing monitoring domains, training, PII scrubbing.
- TCL-002: Roadmap v1.0 (single doc) restructured into two documents: overview (CIO/board presentation) and detail (technical reference). All 43 CIO findings addressed. Team structure (7 people: 3 App Ops, 1 Service Quality, 3 DevOps) incorporated. New domains added: RUM, AWS cost monitoring, commission batch. Training added as Phase 1 deliverable. PII scrubbing policy added. Human costs added to investment section. Regulatory citations marked pending Legal/Compliance verification. Original v1.0 document preserved at `monitoring-alerting-roadmap.md`.
- TCL-003: Pending CIO re-review of restructured roadmap v2.0. Primary document: `monitoring-alerting-roadmap-overview.md`. Technical reference: `monitoring-alerting-roadmap-detail.md`.
