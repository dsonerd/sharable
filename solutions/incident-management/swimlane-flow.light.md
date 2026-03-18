# IT Incident Management Process — Lightweight (Presentation) Version

> **Visual reference**: `swimlane-flow.light.drawio` (same directory)
> This document describes the simplified incident management process as depicted in the presentation-grade swimlane diagram.

---

## Overview

This is a streamlined version of the incident management process designed for presentations and high-level communication. It covers the same lifecycle — Detect, Triage, Respond & Fix, Verify, and Close — but consolidates roles into four lanes and omits detailed sub-steps like KB checks, QA validation, and L3/vendor escalation.

---

## Swimlane Participants (Roles)

| Lane | Role | Description |
|------|------|-------------|
| **REPORTER / MONITORING** | Reporter / Alert | Any internal person or monitoring system that detects an issue |
| **L1 / L2** | First/Second-line Support | Acknowledge, log, classify, and route incidents |
| **RESPONSE TEAM** | Technical Responders | Infrastructure and application teams who investigate, fix, and verify |
| **MGMT** | Management | Receives P1/P2 notifications, approves deployments, reviews and signs off on closure |

---

## Management Involvement

| Trigger | Management Action |
|---------|-------------------|
| P1/P2 identified during triage | Notified of the incident |
| P1/P2 App fix ready to deploy | Approve deployment |
| Post-Incident Review complete (P1/P2) | Review and sign off |

---

## Process Stages and Response Targets

| Stage | Name | Target Time |
|-------|------|-------------|
| 1 | DETECT | < 5 minutes |
| 2 | TRIAGE | < 15 minutes |
| 3 | RESPOND & FIX | Priority-dependent |
| 4 | VERIFY | < 30 minutes |
| 5 | CLOSE | P1/P2: < 48 hours |

---

## Step-by-Step Process Flow

### Stage 1: DETECT

**Lane: REPORTER / MONITORING**

**Step 1.1: Alert / User Report**
- An alert fires from monitoring, or a user/stakeholder reports an issue
- This is the single entry point into the process

### Stage 2: TRIAGE

**Lane: L1 / L2**

**Step 2.1: Acknowledge & Log**
- L1/L2 receives the alert or report
- Acknowledge receipt and log the incident in the ITSM system

**Step 2.2: Decision — Incident?**

- **NO** — Route to **Service Request** process. *(Process ends here for non-incidents)*
- **YES** — Proceed to classification

**Step 2.3: Decision — Classify**

Classify the incident type to determine the response path. L1/L2 determines whether the root issue is in infrastructure (network, servers, storage, cloud services) or in the application (software bugs, data errors, business logic). The classification guide provides decision criteria.

- **INFRA** — Route to Infrastructure Response (Step 3.1)
- **APP** — Route to Application Response (Step 3.2)

### Stage 3: RESPOND & FIX

**Lane: RESPONSE TEAM**

#### Infrastructure Path

**Step 3.1: Infrastructure Response**
- Actions: Rollback, Restart, Failover
- The infrastructure/DevOps team executes immediate remediation
- Once resolved, proceed to Verify (Step 4.1)

#### Application Path

**Step 3.2: Application Response**
- Actions: Root cause analysis, Fix development, Deploy
- The development team investigates, develops a fix, and prepares for deployment

**Step 3.2a: Approval Gate — P1/P2 App Incidents**
- For P1/P2 application incidents, the Response Team requests management approval before deploying the fix
- **MGMT lane**: Approve Deploy (P1/P2 App Incident)
- Once **approved**, the Response Team proceeds with deployment
- After deployment, proceed to Verify (Step 4.1)

**Lane: MGMT (parallel)**

**Step 3.3: Management Notified**
- Management is notified when a P1/P2 incident is identified during triage
- Notification includes priority level

### Stage 4: VERIFY

**Lane: RESPONSE TEAM**

**Step 4.1: Verify & Confirm**
- Both infrastructure and application paths converge here
- Response Team verifies the fix is effective and service is restored
- Confirm resolution before proceeding to closure

### Stage 5: CLOSE

**Lane: RESPONSE TEAM and MGMT**

**Step 5.1: Post-Incident Review**
- Conduct a Post-Incident Review (blameless — focused on systemic improvement, not individual fault)
- Identify the root cause and contributing factors
- Define action items
- Update Knowledge Base with findings

**Step 5.2: Management Review & Sign Off (P1/P2)**
- Management reviews the Post-Incident Review and signs off
- Applicable to P1/P2 incidents only

**Step 5.3: INCIDENT CLOSED**
- Incident record is formally closed
- Post-Incident Review actions tracked in backlog

---

## Flow Summary

```
Alert / User Report  (REPORTER / MONITORING)
        |
        v
  Acknowledge & Log  (L1/L2)
        |
        v
   Incident? ----NO----> Service Request [END]
        |
       YES
        |
        v
   Classify  (Infra vs. App — see classification guide)
    /       \
  INFRA      APP
   |           |
   v           v
 Infra       App Response ---(P1/P2 request)---> Mgmt: Approve Deploy
 Response     (Root cause,                              |
 (Rollback,    Fix, Deploy) <-------(approved)----------+
  Restart,        |
  Failover)       |
   \             /
    \           /
     v         v
   Verify & Confirm  (RESPONSE TEAM)
        |
        v
   Post-Incident Review
   (Root cause, Actions, Update KB)
        |
        v
   Mgmt Review & Sign Off (P1/P2)
        |
        v
   INCIDENT CLOSED
```

---

## P3/P4 Incidents

P3/P4 incidents follow the same Detect-Triage-Respond-Verify-Close flow but skip Management notification, the approval gate, and the formal Post-Incident Review sign-off. They are handled by L1/L2 and the Response Team directly.

---

> A detailed operational version with additional roles, time targets, and procedural steps exists for the response team.

---

**Review Required**: This document should be reviewed by **tcl-cio** before implementation.
**Prepared by**: tcl-ito (IT Operations)
**Date**: 2026-03-18
