# IT Incident Management Process — Full Version

> **Visual reference**: `swimlane-flow.drawio` (same directory)
>
> This document describes the complete incident management process as depicted in the official swimlane diagram.
> For classification details, priority matrix, and SLA targets, see [`classification.md`](classification.md).
> For known incident scenarios, see [`incident-knowledge-base.md`](incident-knowledge-base.md).

---

## Overview

This process covers the end-to-end lifecycle of an IT incident at TCLife, from initial detection through triage, response, verification, and formal closure. It distinguishes between **infrastructure incidents** and **application incidents**, with dedicated paths for each. The IC Coordination hub handles P1 War Room activation, emergency change (RFC) creation, and team dispatch as integrated behaviors — not separate decision gates.

Every box in the swimlane diagram has a **step number** for easy reference during incident response and training.

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
| ① | DETECT | < 5 minutes |
| ② | TRIAGE | < 15 minutes |
| ②b | COLLABORATE | < 30 minutes (App incidents with no KB match) |
| ③ | RESPOND & FIX | Priority-dependent |
| ④ | VERIFY | < 30 minutes |
| ⑤ | CLOSE | P1/P2: < 48 hours |

---

## Numbered Step-by-Step Process Flow

### Stage ① DETECT (< 5 min)

**Step 1 — Alert / User Report / Health Check Fails**
Lane: ANYONE

Three detection sources feed into the process:
1. **Monitoring alert fires** — Automated alerts from CloudWatch, health checks, or other monitoring tools
2. **User / stakeholder reports** — Manual reports from in-house users, policyholders, or agents
3. **Health check fails** — Automated health-check probes detecting service degradation

All three sources flow down to the L1/L2 lane for acknowledgement.

---

### Stage ② TRIAGE (< 15 min)

**Step 2 — Receive & Acknowledge**
Lane: L1/L2 ITO

- Receive and acknowledge the alert or report
- Auto-create ticket on ITSM
- Send 1st communication: *"Received, looking into it"*

> **Reference**: Incident Triage Guide

**Step 3 — Real Incident?** ◇
Lane: L1/L2 ITO

- **NO** → Route to: Service Request / User error / Backlog. Notify reporter and close. **— END** (Path G)
- **YES** → Proceed to Step 4

**Step 4 — Log INC-xxxx, SLA starts, Classify**
Lane: L1/L2 ITO

- Log as INC-xxxx
- SLA clock starts
- Classify: Infrastructure or Application?
- Send 2nd communication: Notify reporter of priority and expected timeline

**Step 5 — Infra or App?** ◇
Lane: L1/L2 ITO

- **INFRA** → Go to Step 6
- **APP** → Go to Step 8

---

#### INFRA INCIDENT Path

**Step 6 — KB Match? (Infra)** ◇
Lane: L1/L2 ITO

- **YES** → L1 assigns priority from Knowledge Base; execute documented response → Go to Step 10
- **NO** → L1 assigns priority by scope assessment → Go to Step 10

> **Reference**: Incident Knowledge Base

---

#### APP INCIDENT Path

**Step 8 — KB Match? (App)** ◇
Lane: L1/L2 ITO

- **YES** → L1 assigns priority from KB; execute first response; notify tech team (don't wait) → Go to Step 10
- **NO** → L1 assigns preliminary priority → Go to Step 9

### Stage ②b COLLABORATE (< 30 min) — App Incidents Without KB Match

**Step 9 — Collaborate: Assess Blast Radius**
Lane: L1/L2 ITO + Tech Team + BA

- L1 + Tech Team + BA collaborate to assess blast radius
- Confirm or adjust priority
- → Go to Step 10

> **Note**: After hours — L1 + on-call dev assess; BA joins next business day

---

### Stage ③ RESPOND & FIX (Priority-dependent)

**Step 10 — IC Coordination** ⭐ (Central hub, P1/P2 only)
Lane: INCIDENT COMMANDER

- **P1: Activate War Room / Bridge Call immediately**
- Apply workaround first if available
- Coordinate team and manage communications
- **Create RFC** (all P1/P2 changes are emergency changes by definition)
- Status updates: P1 every 30 min, P2 every 1 hr (include reporter)
- Dispatch to: **Step 11** (Infra) · **Step 12** (App) · **Step 14** (L3/Vendor)

> **Reference**: Incident Response Playbook
>
> **Note**: For P3/P4, a senior L1 or team lead performs IC duties (no formal IC). After hours: IC engages on-call tech; Mgmt next business day unless P1.

---

#### Infrastructure Response

**Step 11 — Infra: Rollback / Restart / Failover**
Lane: TECH TEAM (Infra / DevOps)

- Execute immediate remediation (rollback, restart, failover)
- Apply infrastructure fix
- → Go to Step 15

---

#### Application Response

**Step 12 — Dev: Root Cause & Develop Fix**
Lane: TECH TEAM (Dev Team)

- Investigate root cause and develop the fix
- Once fix is ready, dispatch in parallel:
  - → **Step 13a** (QA: Validate in staging)
  - → **Step 13b** (Management: Approve deploy — P1/P2 App only)

**Step 13a — QA: Validate Fix in Staging**
Lane: QA

- Validate fix in staging environment
- *(Rework until pass — implicit loop, not a separate routing decision)*

**Step 13b — Management: Approve Fix Deploy**
Lane: MANAGEMENT

- For P1/P2 application incidents, management approves the fix deployment
- For P3/P4: this step is skipped

> **Important**: Both Step 13a (QA pass) AND Step 13b (Management approval) must complete before proceeding to Step 12b. For P3/P4, only QA validation is required.

**Step 12b — Dev/DBA: Deploy via CI/CD, Remediate Data**
Lane: TECH TEAM (Dev / DBA)

- Deploy via CI/CD pipeline
- Remediate bad data if applicable
- → Go to Step 15

---

#### L3 / Vendor Escalation

**Step 14 — L3 / Vendor: Specialist Investigation**
Lane: L3 / VENDOR

- Specialist investigation: Patch / Replace / Vendor fix
- Implement specialist fix
- → Go to Step 15

---

### Stage ④ VERIFY (< 30 min)

**Step 15 — Monitor 15 min for Regression**
Lane: TECH TEAM

- Monitor production for 15 minutes to check for regression
- → Go to Step 16

**Step 16 — Reporter Confirms?** ◇
Lane: INCIDENT COMMANDER

- **YES** → Go to Step 17
- **Not resolved** → Loop back to Step 10 (IC Coordination) for another round (Path F)

**Step 17 — Confirm Service Restored**
Lane: INCIDENT COMMANDER

- IC / Team Lead confirms service is restored
- Send final communication: *"Resolved, you can resume"*
- Management notified of all-clear
- → Go to Step 18

---

### Stage ⑤ CLOSE (P1/P2: < 48 hrs)

**Step 18 — Post-Incident Review (Blameless RCA)**
Lane: INCIDENT COMMANDER

- IC / Team Lead leads a blameless Root Cause Analysis
- P3/P4: simplified review only

> **Reference**: Post-Incident Review Template

**Step 19 — Tech: Identify Root Cause**
Lane: TECH TEAM

- Detailed root cause identification

**Step 20 — Define Action Items, Update KB**
Lane: INCIDENT COMMANDER

- Define action items from RCA
- Update Knowledge Base with findings

**Step 21 — Management Review RCA & Sign Off**
Lane: MANAGEMENT

- Review RCA and sign off (P1/P2 only)
- P3/P4: this step is skipped

**Step 22 — INCIDENT CLOSED**

- RCA published
- Actions placed in backlog
- Knowledge Base updated

---

## Scenario Paths (Quick Reference)

Use these numbered paths for training, runbook references, and audit trails. When L1 calls the IC at 2am and says *"I'm at step 7"*, everyone immediately knows the state.

### Path A: Infra Incident, KB Match, P1 (Happy Path)
```
1 → 2 → 3(YES) → 4 → 5(INFRA) → 6(YES) → 10 → 11 → 15 → 16(YES) → 17 → 18 → 19 → 20 → 21 → 22
```
**Narrative**: Alert fires. L1 acknowledges, confirms real incident, logs it. Classified as infra. KB has a match — L1 assigns P1, executes documented response. IC takes over: activates war room, coordinates. Infra team rolls back. Monitor 15 min, reporter confirms. Service restored. RCA, management sign-off, closed.

### Path B: Infra Incident, No KB Match, P2
```
1 → 2 → 3(YES) → 4 → 5(INFRA) → 6(NO) → 10 → 11 → 15 → 16(YES) → 17 → 18 → 19 → 20 → 21 → 22
```
**Narrative**: Same as Path A, but no KB match. L1 assigns priority by scope assessment. IC coordinates response. Same resolution flow.

### Path C: App Incident, KB Match, P1 (with Mgmt Approval)
```
1 → 2 → 3(YES) → 4 → 5(APP) → 8(YES) → 10 → 12 → 13a + 13b → 12b → 15 → 16(YES) → 17 → 18 → 19 → 20 → 21 → 22
```
**Narrative**: User reports issue. L1 acknowledges, confirms real incident, logs it. Classified as app. KB match — L1 assigns P1, executes first response, notifies dev. IC coordinates. Dev develops fix. QA validates in staging while management approves deploy (parallel). Both pass. Deploy via CI/CD. Monitor, confirm. RCA with management sign-off, closed.

### Path D: App Incident, No KB Match, P2 (with Collaboration)
```
1 → 2 → 3(YES) → 4 → 5(APP) → 8(NO) → 9 → 10 → 12 → 13a + 13b → 12b → 15 → 16(YES) → 17 → 18 → 19 → 20 → 21 → 22
```
**Narrative**: Same as Path C, but no KB match so L1 collaborates with Tech Team + BA to assess blast radius and confirm priority before IC takes over.

### Path E: L3/Vendor Escalation (any type)
```
1 → 2 → 3(YES) → 4 → 5(either) → 6 or 8 → 10 → 14 → 15 → 16(YES) → 17 → 18 → 19 → 20 → 21 → 22
```
**Narrative**: After IC coordination, internal teams cannot resolve. IC escalates to L3/vendor. Specialist investigates and implements fix. Same verification and closure flow.

### Path F: Verification Fails (Loop Back)
```
... → 15 → 16(NOT RESOLVED) → 10 → (dispatch again) → 15 → 16(YES) → 17 → ...
```
**Narrative**: After fix and monitoring, reporter says not resolved. Flow loops back to IC Coordination for another round.

### Path G: Not an Incident
```
1 → 2 → 3(NO) → END
```
**Narrative**: Alert received, L1 determines it is not a real incident. Routes to service request / user error. Notifies reporter. Done.

### Path H: App Incident, P3/P4 (No Mgmt Approval Needed)
```
1 → 2 → 3(YES) → 4 → 5(APP) → 8(YES or NO) → [9 if NO] → 10* → 12 → 13a → 12b → 15 → 16(YES) → 17 → 18(simplified) → 19 → 20 → 22
```
*Note*: For P3/P4, Step 10 is handled by senior L1 or team lead (no formal IC). Step 13b (Mgmt approval) is skipped. Step 21 (Mgmt RCA sign-off) is skipped. Step 18 is a simplified review.

---

## Management Parallel Track

Throughout the process, Management (IT Mgr / CTO) receives parallel notifications and participates at key gates:

| Trigger | Management Action |
|---------|-------------------|
| P1/P2 identified during triage | Notified; approve escalation |
| P1 activated (via IC Coordination) | Stakeholders notified |
| During response (P1/P2) | Receive status updates (P1: every 30 min, P2: every 1 hr) |
| P1/P2 App fix ready to deploy | Approve fix deployment (Step 13b) |
| Service restored | Notified of all-clear |
| RCA complete (P1/P2) | Review RCA & sign off (Step 21) |

---

## Escalation Paths

1. **L1 to L2** — Standard escalation within ITO for incidents outside L1 capability
2. **L2 to Incident Commander** — All confirmed P1/P2 incidents are coordinated by an IC
3. **IC to L3 / Vendor** — Specialist escalation when internal teams cannot resolve (Step 10 → Step 14)
4. **IC to Management** — Automatic notification for P1/P2; approval required for P1/P2 app deployments (Step 13b)

> **After-hours operations**: L1 on-call responds to all alerts. For P1/P2, the IC and tech team are engaged per the on-call rotation. BA, QA, and Management join at the next business day unless the IC explicitly escalates.

---

## RACI Matrix

| Stage | L1/L2 ITO | Incident Commander | Tech Team | QA | L3/Vendor | Management |
|-------|-----------|-------------------|-----------|-----|-----------|------------|
| ① Detect | **R** | I | I | -- | -- | -- |
| ② Triage | **R/A** | **A** (P1/P2) | **C** | -- | -- | **I** (P1/P2) |
| ②b Collaborate | **R** | I | **R/A** | -- | -- | -- |
| ③ Respond & Fix | I | **A** (P1/P2) | **R** | **R** (App) | **R** (if escalated) | **I** |
| ④ Verify | I | **A** | **R** | -- | -- | **I** |
| ⑤ Close (RCA) | -- | **R** | **C** | -- | -- | **A** (P1/P2) |

> **R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed
>
> For P3/P4: senior L1 or team lead assumes IC accountability. No formal IC role assigned.
>
> Stage ④ verification is always performed by the Tech Team, regardless of who implemented the fix (including L3/Vendor fixes). QA's validation scope is limited to staging environment testing during Stage ③.

---

## Communication Checkpoints

| # | When | Who Sends | Message |
|---|------|-----------|---------|
| 1st | Upon acknowledgement (Step 2) | L1/L2 | *"Received, looking into it"* |
| 2nd | After priority assignment (Step 4) | L1/L2 | Notify reporter of priority and expected timeline |
| Ongoing | During response (Step 10) | IC | Status updates (P1: every 30 min, P2: every 1 hr) — include reporter |
| Last | Service confirmed restored (Step 17) | IC / Team Lead | *"Resolved, you can resume"* |

---

## Referenced Documents

| Document | Used At |
|----------|---------|
| Incident Triage Guide | Step 2 — Detection, acknowledgement and initial triage |
| Incident Knowledge Base | Steps 6, 8 — KB match checks for both Infra and App paths |
| Escalation Policy | Steps 4, 10 — Management notification and escalation decisions |
| Incident Response Playbook | Step 10 — IC coordination and response activities |
| Post-Incident Review Template | Step 18 — Blameless RCA |

---

## What Was Simplified (vs. previous version)

1. **Removed "Major Incident?" diamond** — P1 War Room activation is now a behavior within IC Coordination (Step 10), not a separate decision gate
2. **Removed "Emergency Change?" diamond + RFC box** — All P1/P2 changes are emergency changes by definition; RFC creation is noted in Step 10
3. **Removed QA Fail/Rework loop** — Rework is implicit and noted on the QA box
4. **Added step numbers** on every box in the diagram for quick reference
5. **Added scenario paths (A-H)** for training, audit trails, and operational communication

---

**Prepared by**: tcl-ito (IT Operations)
**Date**: 2026-03-19
