# IT Incident Management Process — Full Version

> **Visual reference**: `swimlane-flow.drawio` (same directory)
>
> This document describes the complete incident management process as depicted in the official swimlane diagram.
> For classification details, priority matrix, and SLA targets, see [`classification.md`](classification.md).
> For known incident scenarios, see [`incident-knowledge-base.md`](incident-knowledge-base.md).

---

## Overview

This process covers the end-to-end lifecycle of an IT incident at TCLife, from initial detection through triage, response, verification, and formal closure. It distinguishes between **infrastructure incidents** and **application incidents**, with dedicated paths for each. The process includes Major Incident activation for P1 events, emergency change management, L3/vendor escalation, QA validation, management approval gates, and a blameless post-incident review.

---

## Swimlane Participants (Roles)

| Lane | Role | Description |
|------|------|-------------|
| **ANYONE** | User / Alert | Any person or automated monitoring system that detects an issue |
| **L1/L2 ITO** | On-call / Help Desk | First- and second-line IT Operations staff who receive, acknowledge, triage, and classify incidents |
| **INCIDENT COMMANDER (IC)** | IC | Senior responder who coordinates P1/P2 response, manages communications, and drives resolution |
| **TECH TEAM** | Dev / Infra / BA / DBA | Technical specialists who investigate root causes, develop fixes, and deploy changes |
| **L3 / VENDOR** | Specialist | Third-level support or external vendors engaged for specialist investigation and fixes |
| **QA** | Quality Assurance | Validates fixes in staging before production deployment (application incidents) |
| **MANAGEMENT** | IT Mgr / CTO | Receives notifications for P1/P2, approves escalations, approves fix deployments, and signs off on RCA |

---

## Process Stages and Time Targets

| Stage | Name | Time Target |
|-------|------|-------------|
| 1 | DETECT | < 5 minutes |
| 2 | TRIAGE | < 15 minutes |
| 2b | COLLABORATE | < 30 minutes (App incidents with no KB match) |
| 3 | RESPOND & FIX | Priority-dependent |
| 4 | VERIFY | < 30 minutes |
| 5 | CLOSE | P1/P2: < 48 hours |

---

## Step-by-Step Process Flow

### Stage 1: DETECT (< 5 min)

**Lane: ANYONE**

Three detection sources feed into the process:

1. **Monitoring alert fires** -- Automated alerts from CloudWatch, health checks, or other monitoring tools
2. **User / stakeholder reports** -- Manual reports from in-house users, policyholders, or agents
3. **Health check fails** -- Automated health-check probes detecting service degradation

All three sources flow down to the L1/L2 lane for acknowledgement.

### Stage 2: TRIAGE (< 15 min)

**Lane: L1/L2 ITO**

**Step 2.1: Receive & Acknowledge**
- L1/L2 receives and acknowledges the alert or report
- Auto-create ticket on ITSM
- Send 1st communication: *"Received, looking into it"*

> **Reference**: Incident Triage Guide

**Step 2.2: Decision -- Real Incident?**

- **NO** -- Route to: Service Request / User error / Backlog. Notify reporter and close. *(Process ends for this item)*
- **YES** -- Proceed to logging and classification

**Step 2.3: Log Incident**
- L1/L2 logs as INC-xxxx
- SLA clock starts
- Classify: Infrastructure or Application?
- Send 2nd communication: Notify reporter of priority and expected timeline

> **Reference**: Incident Knowledge Base

**Step 2.4: Decision -- Infra Issue?**

This decision point splits the process into two parallel tracks:

- **YES (Infrastructure problem)** -- Follow the **INFRA INCIDENT** path
- **NO (Application problem)** -- Follow the **APP INCIDENT** path

#### INFRA INCIDENT Path

**Step 2.5a: Decision -- KB Match? (Infrastructure)**

- **YES** -- L1 assigns priority from Knowledge Base; execute documented response. Proceed to Step 2.7.
- **NO** -- L1 assigns priority by scope assessment. Proceed to Step 2.7.

> **Reference**: Priority & Severity Matrix

**Step 2.7: Decision -- Major Incident? (P1)**

- **YES (P1)** -- Activate Major Incident procedure (Step 3.0)
- **NO** -- Proceed directly to IC Coordination (Step 3.1)

#### APP INCIDENT Path

**Step 2.5b: Decision -- KB Match? (Application)**

- **YES** -- L1 assigns priority from Knowledge Base; execute first response; notify tech team (don't wait). Proceed to IC Coordination (Step 3.1).
- **NO** -- L1 assigns preliminary priority. Proceed to Collaborate (Step 2b).

### Stage 2b: COLLABORATE (< 30 min) -- App Incidents Without KB Match

**Lane: L1/L2 ITO (with Tech Team and BA)**

- L1 + Tech Team + BA collaborate to assess blast radius
- Confirm or adjust priority
- After collaboration, proceed to IC Coordination (Step 3.1)

> **Note**: After hours -- L1 + on-call dev assess; BA joins next business day

### Stage 3: RESPOND & FIX (Priority-dependent)

**Lane: INCIDENT COMMANDER**

**Step 3.0: Activate Major Incident (P1 only)**
- Establish War Room / Bridge Call
- Assign Incident Commander
- Notify Stakeholders (Major Incident only) -- flows to Management lane

> **Reference**: Incident Response Playbook

**Step 3.1: IC Coordination (P1/P2 only)**
- Apply workaround first if available
- Coordinate team and manage communications
- Decide: rollback? escalate? war room?
- Status updates: P1 every 30 minutes, P2 every 1 hour
- Include reporter in updates

**Step 3.2: Decision -- Emergency Change?**
- **YES** -- Create RFC (Request for Change)
- **NO** -- Proceed with standard response

> **Reference**: Change Management Policy

The IC dispatches work to the appropriate teams:

#### Infrastructure Response (Tech Team Lane)

**Step 3.3a: Rollback / Restart / Failover**
- Infra / DevOps team executes immediate remediation

**Step 3.3b: Apply Infrastructure Fix**
- Infra / DevOps team applies the definitive infrastructure fix
- Proceed to Verify (Stage 4)

#### Application Response (Tech Team Lane)

**Step 3.4a: Root Cause & Develop Fix**
- Dev Team investigates root cause and develops the fix
- Once fix is ready, route to QA validation (Step 3.4b) and, for P1/P2, request management approval (Step 3.4c) in parallel

**Step 3.4b: QA Validate (QA Lane)**
- QA validates fix in staging environment
- If validation fails, loop back to Dev for rework

**Step 3.4c: Approval Gate -- P1/P2 App Incidents (parallel with QA)**
- For P1/P2 application incidents, the Dev Team requests management approval to deploy the fix
- **Management lane**: Approve Fix Deploy (P1/P2 App Incident)

> **Note**: For P1/P2 app incidents, QA validation and management approval run in parallel. Deployment proceeds only when BOTH are complete (management approval received AND QA validation passed). For P3/P4 app incidents, only QA validation is required.

**Step 3.4d: Deploy via CI/CD**
- Dev / DBA deploy via CI/CD pipeline
- Remediate bad data if applicable
- Proceed to Verify (Stage 4)

#### L3 / Vendor Escalation

**Step 3.5a: Specialist Investigation**
- L3 / Vendor performs specialist investigation
- Options: Patch / Replace / Vendor fix

**Step 3.5b: Implement Specialist Fix**
- L3 / Vendor implements the specialist fix
- Proceed to Verify (Stage 4)

### Stage 4: VERIFY (< 30 min)

**Lane: TECH TEAM and INCIDENT COMMANDER**

**Step 4.1: Monitor for Regression**
- Tech Team monitors production for 15 minutes to check for regression

**Step 4.2: Decision -- Reporter Confirms?**
- **YES** -- Proceed to confirmation
- **Not resolved** -- Loop back to IC Coordination (Step 3.1) for further investigation

**Step 4.3: Confirm Service Restored**
- IC / Team Lead confirms service is restored
- Send final communication: *"Resolved, you can resume"*
- Management is notified of all-clear

### Stage 5: CLOSE (P1/P2: < 48 hrs)

**Lane: INCIDENT COMMANDER, TECH TEAM, and MANAGEMENT**

**Step 5.1: Lead Post-Incident Review (Blameless RCA)**
- IC / Team Lead leads a blameless Root Cause Analysis (focused on systemic improvement, not individual fault)
- P3/P4: simplified review only

> **Reference**: Post-Incident Review Template

**Step 5.2: Identify Root Cause**
- Tech Team performs detailed root cause identification

**Step 5.3: Define Action Items & Update Knowledge Base**
- IC / Team Lead defines action items from RCA
- Update Knowledge Base with findings

**Step 5.4: Management Review & Sign Off (P1/P2 only)**
- Management reviews RCA and signs off

**Step 5.5: INCIDENT CLOSED**
- RCA published
- Actions placed in backlog
- Knowledge Base updated

---

## Management Parallel Track

Throughout the process, Management (IT Mgr / CTO) receives parallel notifications and participates at key gates:

| Trigger | Management Action |
|---------|-------------------|
| P1/P2 identified during triage | Notified; approve escalation |
| Major Incident activated | Stakeholders notified |
| P1/P2 App fix ready to deploy | Approve fix deployment |
| During response (P1/P2) | Receive status updates (P1: every 30 min, P2: every 1 hr) |
| Service restored | Notified of all-clear |
| RCA complete (P1/P2) | Review RCA & sign off |

---

## Escalation Paths

1. **L1 to L2** -- Standard escalation within ITO for incidents outside L1 capability
2. **L2 to Incident Commander** -- All confirmed P1/P2 incidents are coordinated by an IC
3. **IC to L3 / Vendor** -- Specialist escalation when internal teams cannot resolve
4. **IC to Management** -- Automatic notification for P1/P2; approval required for P1/P2 app deployments

> **After-hours operations**: L1 on-call responds to all alerts. For P1/P2, the IC and tech team are engaged per the on-call rotation. BA, QA, and Management join at the next business day unless the IC explicitly escalates. See the On-Call Model (to be defined per IM-005) for full after-hours coverage details.

---

## RACI Matrix

| Stage | L1/L2 ITO | Incident Commander | Tech Team | QA | L3/Vendor | Management |
|-------|-----------|-------------------|-----------|-----|-----------|------------|
| 1 Detect | **R** | I | I | -- | -- | -- |
| 2 Triage | **R/A** | **A** (P1/P2) | **C** | -- | -- | **I** (P1/P2) |
| 2b Collaborate | **R** | I | **R/A** | -- | -- | -- |
| 3 Respond & Fix | I | **A** (P1/P2) | **R** | **R** (App) | **R** (if escalated) | **I** |
| 4 Verify | I | **A** | **R** | -- | -- | **I** |
| 5 Close (RCA) | -- | **R** | **C** | -- | -- | **A** (P1/P2) |

> **R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed
>
> For P3/P4: senior L1 or team lead assumes IC accountability. No formal IC role assigned.
>
> Stage 4 verification is always performed by the Tech Team, regardless of who implemented the fix (including L3/Vendor fixes). QA's validation scope is limited to staging environment testing during Stage 3.

---

## Communication Checkpoints

| # | When | Who Sends | Message |
|---|------|-----------|---------|
| 1st | Upon acknowledgement | L1/L2 | *"Received, looking into it"* |
| 2nd | After priority assignment | L1/L2 | Notify reporter of priority and expected timeline |
| Ongoing | During response | IC | Status updates (P1: every 30 min, P2: every 1 hr) -- include reporter |
| Last | Service confirmed restored | IC / Team Lead | *"Resolved, you can resume"* |

> For Management-specific notifications (P1/P2 identification, major incident stakeholder alerts, all-clear, and RCA sign-off requests), see the **Management Parallel Track** table above.

---

## Referenced Documents

| Document | Used At |
|----------|---------|
| Incident Triage Guide | Stage 1-2 -- Detection, acknowledgement and initial triage |
| Incident Knowledge Base | Stage 2 -- KB match checks for both Infra and App paths |
| Priority & Severity Matrix | Stage 2 -- Priority assignment after classification |
| Escalation Policy | Stage 2/3 -- Management notification and escalation decisions |
| Incident Response Playbook | Stage 3 -- IC coordination and response activities |
| Change Management Policy | Stage 3 -- Emergency change / RFC decisions |
| Post-Incident Review Template | Stage 5 -- Blameless RCA |

---

**Review Required**: This document should be reviewed by **tcl-cio** before implementation.
**Prepared by**: tcl-ito (IT Operations)
**Date**: 2026-03-18
