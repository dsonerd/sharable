# Project Backlog

## Active Tasks
| ID | Task | Category | Assigned To | Status | Created | Updated |
|----|------|----------|-------------|--------|---------|---------|
| TCL-003 | Monitoring roadmap v2.1 — CIO re-review | solution | tcl-cio | todo | 2026-03-20 | 2026-03-20 |

## Completed Tasks
| ID | Task | Category | Completed By | Completed Date |
|----|------|----------|-------------|----------------|
| TCL-000 | Monitoring & alerting roadmap — draft | solution | tcl-orch | 2026-03-20 |
| TCL-001 | Monitoring & alerting roadmap — CIO review | solution | tcl-cio | 2026-03-20 |
| TCL-002 | Monitoring roadmap — restructure into overview + detail, incorporate CIO feedback | solution | tcl-orch | 2026-03-20 |
| TCL-004 | Monitoring roadmap v2.1 — incorporate insurance-domain monitoring research | solution | tcl-orch | 2026-03-20 |

## Notes / Decisions
- TCL-000: Comprehensive 4-phase roadmap covering infrastructure, application, business, and security monitoring. Cross-references existing incident management backlog items IM-005, IM-009, IM-015, IM-018. No duplicate work found — existing dashboard files are tactical (Grafana TV); this roadmap is strategic.
- TCL-001: CIO review completed. 43 findings (10 high, 21 medium, 12 low). Conditionally approved. Top 5 blockers: staffing plan, regulatory citations, missing monitoring domains, training, PII scrubbing.
- TCL-002: Roadmap v1.0 (single doc) restructured into two documents: overview (CIO/board presentation) and detail (technical reference). All 43 CIO findings addressed. Team structure (7 people: 3 App Ops, 1 Service Quality, 3 DevOps) incorporated. New domains added: RUM, AWS cost monitoring, commission batch. Training added as Phase 1 deliverable. PII scrubbing policy added. Human costs added to investment section. Regulatory citations marked pending Legal/Compliance verification. Original v1.0 document preserved at `monitoring-alerting-roadmap.md`.
- TCL-003: Pending CIO re-review of roadmap v2.1. Primary document: `monitoring-alerting-roadmap-overview.md`. Technical reference: `monitoring-alerting-roadmap-detail.md`.
- TCL-004: Incorporated insights from `reference.research.md` (insurance-domain monitoring blueprint). Key additions: 9 core business journeys (J1-J9), rider monitoring as first-class dimension, domain-specific monitoring matrices (UW/STP, billing/persistency, claims, ops workflow, security/fraud/compliance), formal SLO set, prioritized first 25 alerts, canonical telemetry data model (14 domains), composite multi-signal alert patterns, InsureMO instrumentation checklist, strengthened regulatory citations (Insurance Law 08/2022/QH15, Decree 46/2023, Circular 67/2023).
