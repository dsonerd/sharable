# IT Incident Management — Swimlane Flow

> Lean ITIL-aligned incident management process.
> Designed for 1–2 slide presentation. Shows who does what at each stage.
>
> Related: [`lightweight.md`](lightweight.md) (detailed flowchart) · [`severity-triage.md`](severity-triage.md) (decision tree)

---

## Incident Classification

| Category | Definition | Examples | Trigger |
|----------|-----------|----------|---------|
| **Technology Incident** | An unplanned interruption or degradation of an IT service. The system is **down, unreachable, or performing below acceptable thresholds**. Focus: **restore service ASAP**. | Server/network outage, database crash, SSL cert expiry, infrastructure failure, cloud service disruption | Monitoring alert, user unable to access system, health check failure |
| **Production Issue (Defect)** | The system is **running but producing incorrect results** — a bug or defect in production. Data integrity or business logic is wrong. Focus: **fix the defect, remediate bad data**. | Wrong premium calculation, incorrect policy status, failed batch with wrong output, integration sending malformed messages | User report, QA finding, data reconciliation mismatch, business metric anomaly |

**Key Difference**: Technology Incident = **service availability** problem. Production Issue = **correctness** problem.

---

## Severity Matrix

| Severity | Name | Definition | Response Time | Resolution Target | Who's Involved |
|----------|------|-----------|---------------|-------------------|----------------|
| **SEV 1** | Critical | Full service outage or data breach affecting customers | Immediate | < 1 hour | All hands: IC + Tech + Mgmt + Comms |
| **SEV 2** | Major | Significant degradation, key function unavailable | < 15 min | < 4 hours | IC + On-call team + Mgmt notified |
| **SEV 3** | Minor | Partial impact, workaround available | < 1 hour | < 1 business day | On-call / assigned team |
| **SEV 4** | Low | Cosmetic, minimal impact | Next business day | < 5 business days | Assigned developer |

---

## Swimlane Flow — Who Does What

### Slide Layout (5 Stages × 6 Roles)

```
 STAGE ▸       ① DETECT         ② TRIAGE          ③ RESPOND & FIX      ④ VERIFY          ⑤ CLOSE
               (< 5 min)        (< 15 min)        (SEV-dependent)      (< 30 min)        (< 48 hrs)
─────────────┬────────────────┬─────────────────┬──────────────────────┬─────────────────┬──────────────────
             │                │                 │                      │                 │
 ANYONE      │ Report issue   │                 │                      │                 │
 (User /     │ via channel    │                 │                      │                 │
  Alert)     │ or alert fires │                 │                      │                 │
             │                │                 │                      │                 │
─────────────┼────────────────┼─────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                 │                      │                 │
 L1 SUPPORT  │ Receive &      │ Confirm real?   │                      │                 │
 (On-call /  │ acknowledge    │ Classify:       │                      │                 │
  Help Desk) │                │  Tech Incident  │                      │                 │
             │                │  or Prod Issue? │                      │                 │
             │                │ Assign SEV 1–4  │                      │                 │
             │                │                 │                      │                 │
─────────────┼────────────────┼─────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                 │                      │                 │
 INCIDENT    │                │ Assigned as IC  │ Coordinate team      │ Confirm service │ Lead RCA meeting
 COMMANDER   │                │ (SEV1/2 only)   │ Manage comms         │ restored or fix │ Publish report
 (IC)        │                │                 │ Decide: rollback?    │ deployed        │ Track action
             │                │                 │   escalate? war room?│                 │ items
             │                │                 │                      │                 │
─────────────┼────────────────┼─────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                 │                      │                 │
 TECH TEAM   │                │ Provide initial │ TECH INCIDENT:       │ Monitor 15 min  │ Contribute to
 (Dev /      │                │ assessment      │  → Rollback/restart/ │ for regression  │ RCA findings
  Infra /    │                │                 │    failover          │                 │
  DBA)       │                │                 │  → Apply infra fix   │                 │
             │                │                 │                      │                 │
             │                │                 │ PROD ISSUE:          │                 │
             │                │                 │  → Root cause        │                 │
             │                │                 │  → Develop & test fix│                 │
             │                │                 │  → Deploy via CI/CD  │                 │
             │                │                 │  → Remediate bad data│                 │
             │                │                 │                      │                 │
─────────────┼────────────────┼─────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                 │                      │                 │
 QA          │                │                 │                      │ Validate fix in │ Verify no
             │                │                 │                      │ staging (Prod   │ regression
             │                │                 │                      │ Issue only)     │
             │                │                 │                      │                 │
─────────────┼────────────────┼─────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                 │                      │                 │
 MANAGEMENT  │                │ Notified        │ Receive status       │ Approve service │ Review RCA
 (IT Mgr /   │                │ (SEV1/2)        │ updates              │ restoration     │ Sign off
  CTO)       │                │ Approve         │ (SEV1: every 30 min, │                 │ action items
             │                │ escalation      │  SEV2: every 1 hr)   │                 │
             │                │                 │                      │                 │
─────────────┴────────────────┴─────────────────┴──────────────────────┴─────────────────┴──────────────────
```

---

## RACI Matrix

| Stage | L1 Support | Incident Commander | Tech Team | QA | Management |
|-------|-----------|-------------------|-----------|-----|------------|
| ① Detect | **R** | I | I | — | — |
| ② Triage | **R/A** | **A** (SEV1/2) | **C** | — | **I** (SEV1/2) |
| ③ Respond & Fix | I | **A** | **R** | **R** (Prod Issue) | **I** |
| ④ Verify | I | **A** | **R** | **R** | **I** |
| ⑤ Close (RCA) | — | **R** | **C** | **C** | **A** |

> **R** = Responsible (does the work) · **A** = Accountable (owns the outcome) · **C** = Consulted · **I** = Informed

---

## Quick Reference — Technology Incident vs Production Issue

| | Technology Incident | Production Issue (Defect) |
|---|---|---|
| **System state** | Down or degraded | Running but incorrect |
| **Priority** | Restore service availability | Fix correctness, remediate data |
| **Typical actions** | Failover, restart, rollback, maintenance mode | Reproduce, root cause, fix, test, deploy, data remediation |
| **Typical owner** | Infra / DevOps | Dev team |
| **RCA trigger** | Always for SEV1/2 | Always for SEV1/2 + if financial/data impact |
| **Data remediation** | Rarely needed | Often needed |

---

## PPT Design Notes

- **Slide 1**: Swimlane flow as the main visual. Use horizontal lanes per role, left-to-right stage progression. Color-code Technology Incident path (red) vs Production Issue path (amber). Place classification table as a header or callout.
- **Slide 2**: Severity matrix (color-coded red→green) + RACI grid + Quick Reference comparison (two side-by-side boxes).
- **Colors**: SEV1 = Red, SEV2 = Orange, SEV3 = Blue, SEV4 = Green.
- **Font**: 14pt minimum for screen/projector readability.
