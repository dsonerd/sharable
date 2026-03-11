# Incident Triage Guideline

> Practical guide for L1/L2 ITO and on-call engineers to classify and triage IT incidents.
>
> Related: [`swimlane-flow.md`](swimlane-flow.md) · [`severity-triage.md`](severity-triage.md) · [`incident-knowledge-base.md`](incident-knowledge-base.md) · [`scenario-1.md`](scenario-1.md)

---

## 1. Incident Classification

We classify incidents by **where the problem lives** — this determines who owns the fix.

| Type | Definition | Owner |
|------|-----------|-------|
| **Infrastructure Incident** | The platform layer is broken — servers, network, database, cloud services. The application cannot run because the ground underneath it is broken. | Infra / DevOps |
| **Application Incident** | Infrastructure is healthy, but the application layer has a problem — crash, wrong output, design flaw, logic error, missing information. | Dev / BA team |

Both can be **any priority level**. An application design flaw silently miscalculating premiums for all customers is P1 — even though infra is green and no errors appear in logs.

### How This Maps to ITIL

"Infrastructure Incident" and "Application Incident" are not ITIL terms. ITIL defines only **Incident** (any unplanned service disruption). We split it into two types because the response teams and strategies differ.

Likewise, "production defect" / "production issue" / "bug" are SDLC terms, not ITIL. A production defect that impacts a live service **becomes an incident**. After resolution, the underlying defect is tracked as a **Problem** for permanent fix.

| ITIL Term | What It Means | When It Applies |
|-----------|--------------|-----------------|
| **Incident** | Unplanned service disruption or quality reduction | Something is broken in production |
| **Service Request** | User asking for something (not reporting breakage) | Access, information, standard change |
| **Problem** | Root cause of one or more incidents | After incident is resolved — "why did this happen?" |
| **Known Error** | Problem with documented cause and workaround | Cause understood, permanent fix pending |

---

## 2. Triage Flow

Triage answers: **(1) Is it an incident? (2) What type? (3) How urgent? (4) Who acts?**

```
Something reported / alert fires
        │
        ▼
   Is it an incident?  ── NO ──→  Service Request / Backlog / Change
        │                          (see "What Is NOT an Incident" below)
       YES
        │
        ▼
   Is infrastructure healthy?
   (servers, network, DB, cloud)
        │
   ┌────┴─────────────────┐
   │                      │
   NO                    YES
   │                      │
   ▼                      ▼
 INFRA INCIDENT        APPLICATION INCIDENT
   │                      │
   ▼                      ▼
 Check Knowledge Base   Check Knowledge Base
        │                      │
   ┌────┴────┐            ┌────┴────┐
 MATCH    NO MATCH      MATCH    NO MATCH
   │         │            │         │
   ▼         ▼            ▼         ▼
 Assign P  Assign P     Assign P  Assign
 from KB   by scope     from KB   preliminary P
   │         │            │         │
   ▼         ▼            ▼         ▼
 Escalate  Escalate     Execute   Collaborate
 to Infra  to Infra     response  with Tech Team
 / DevOps  / DevOps     from KB   within 30 min
                          │         │
                          ▼         ▼
                        Notify    Confirm /
                        Tech Team adjust P
                        (don't    based on
                         wait)    blast radius
```

### Why Two Paths?

**Infrastructure Incidents are clear-cut.** System is down → L1 can see it → assign P based on scope → escalate immediately. No ambiguity.

**Application Incidents need collaboration.** Infra is fine but something is wrong at the application level. L1 cannot assess blast radius or business impact alone. They need tech team (Dev, BA) and sometimes business input to determine the real priority. This collaboration must happen **within 30 minutes** — L1 assigns a preliminary P and loops in the right people, who then confirm or adjust.

### The Knowledge Base — Fast Lane

L1 should check the [Incident Knowledge Base](incident-knowledge-base.md) during triage **before assigning priority**. It contains known scenarios from past incidents — matching symptoms to incident types, priorities, and response actions.

**If a KB match is found:**
- **Assign P directly** from the KB entry — no need for a preliminary P
- **Execute the documented first response** immediately
- **Notify the tech team** (inform, don't wait) — they can intervene if they see something off
- The tech team session still happens and **can re-evaluate P** if investigation reveals the situation differs from the KB scenario

**If no KB match:**
- Follow the standard path — preliminary P for application incidents, collaborate within 30 min

The KB effectively gives L1 **confidence to act immediately** on known scenarios, while the tech team review still provides a safety net.

The knowledge base starts empty and grows from every RCA. After 20-30 incidents, it becomes L1's most valuable triage tool.

---

## 3. What Is NOT an Incident

| Situation | What It Actually Is | Route To |
|-----------|-------------------|----------|
| User asking for new functionality | **Service Request** | Product backlog |
| User needs access / password reset | **Service Request** | Access management |
| Bug found in UAT (not production) | **Defect** (SDLC) | Development backlog |
| Planned maintenance | **Standard Change** | Change management |
| Performance slightly below optimal but within SLA | **Event** (monitor) | No action |
| Same bug reported again, workaround exists | **Known Error** | Apply workaround |

**Rules:**
- If the user is asking for something *new* → never an incident
- If it's not in production → never an incident
- Planned downtime is not an incident (but overrunning the window *is*)
- One user can't log in → likely a service request. All users can't log in → incident.

---

## 4. Infrastructure Incident

### What L1 Sees

System is down, unreachable, returning errors, or severely degraded. Multiple users affected. Monitoring alerts firing.

### Categories

| Category | Examples |
|----------|---------|
| **Server / Compute** | Server crash, disk full, EC2 terminated, OOM kill |
| **Network** | DNS failure, VPN down, load balancer misconfigured, firewall blocking |
| **Database** | DB crash, connections refused, replication lag, storage full |
| **Cloud Service** | AWS/Azure outage, managed service degradation |
| **Security** | DDoS, compromised credentials, ransomware, data breach |
| **Deployment** | Bad config pushed, migration failed, container image pull error |
| **Scheduled Job** | Batch didn't start, ETL timed out, scheduler failed |

### Detection

Infrastructure incidents are **loud** — monitoring catches them quickly.

Key signals: HTTP 5xx surge, health check failure, "connection timeout" in logs, CPU > 90% sustained, deployment just happened + errors started, multiple users reporting same issue.

### L1 Response

Check Knowledge Base → if match, assign P from KB and follow documented response → if no match, assign P based on scope → escalate to Infra/DevOps immediately → do not debug, restore first.

---

## 5. Application Incident

### What L1 Sees

Infrastructure dashboards are green. No server errors. But something is wrong — users report incorrect data, unexpected behavior, or the application crashes despite healthy infra.

### Categories

| Category | Examples |
|----------|---------|
| **Application Crash** | App OOM, unhandled exception, deadlock — infra is fine but app won't run |
| **Calculation / Logic Error** | Wrong premium, incorrect claim amount, wrong tax rate |
| **Design Flaw** | Feature works as coded but produces wrong business outcome (never caught in testing) |
| **Data Integrity** | Duplicate records, missing transactions, orphaned data |
| **Integration Error** | Wrong field mapping, message format mismatch, stale cache |
| **UI / Display** | Wrong status shown, amounts in wrong currency, missing information |
| **Workflow / State** | Policy stuck in "pending", claim auto-approved incorrectly |
| **Configuration** | Wrong interest rate, incorrect eligibility rule, feature flag misconfigured |

### Detection

Application incidents are often **quiet** — the system looks healthy but the output is wrong.

Key signals: Business metric deviates from pattern, finance reports reconciliation mismatch, customer complaints about specific values, batch completes but output is wrong, one feature broken while everything else works.

**Important:** Some application incidents (design flaws, silent calculation errors) produce no alerts and no errors. They are detected by **people** — business users, finance team, customers — not by monitoring. This is the most dangerous type.

### L1 Response

Check Knowledge Base → **if match: assign P from KB, execute documented response immediately, notify tech team (don't wait)** → **if no match: assign preliminary P, collaborate with Tech Team (Dev + BA) within 30 min** → confirm or re-evaluate P based on blast radius → Tech Team owns the response.

---

## 6. Priority Assignment

| Priority | Name | Definition | Response | Resolution Target | Escalation |
|----------|------|-----------|----------|-------------------|------------|
| **P1** | Critical | Full outage, data breach, or financial data affected | Immediate | < 1 hour | CTO 15 min, CEO 1 hr |
| **P2** | Major | Significant degradation, key function unavailable | < 15 min | < 4 hours | IT Manager 30 min |
| **P3** | Minor | Partial impact, workaround available | < 1 hour | < 1 business day | Team lead if no progress 2 hrs |
| **P4** | Low | Cosmetic, minimal impact | Next business day | < 5 business days | None |

### Decision Questions (in order)

1. Data breach or security event? → **P1**
2. Financial data may be incorrect? → **P1**
3. All users affected / full outage? → **P1**
4. Many users affected + business hours? → **P2**
5. Few users / workaround exists? → **P3**
6. Cosmetic / no user impact? → **P4**

### Infra vs Application — Priority Nuance

For **Infrastructure Incidents**, L1 can assign P directly — the scope is visible (system down = P1/P2, partial = P3). If a KB match exists, use the documented P.

For **Application Incidents**, the path depends on the Knowledge Base:
- **KB match**: L1 assigns P from KB and acts immediately. Tech team is notified and can re-evaluate P in their session.
- **No KB match**: L1 assigns a **preliminary P** based on initial report, then the Tech Team confirms or adjusts within 30 minutes.

Common adjustments during tech team session:

| Initial report | Preliminary P | After investigation | Final P |
|---|---|---|---|
| "One policy has wrong premium" | P3 | "It's a formula bug affecting all policies" | **P1** |
| "Report shows wrong total" | P3 | "Only affects one report, easy workaround" | **P3** (confirmed) |
| "App crashes intermittently" | P2 | "Happens under specific load, affects 5% of users" | **P2** (confirmed) |
| "Customer got wrong statement" | P3 | "Batch sent wrong statements to 2,000 customers" | **P1** |

---

## 7. Scenario Guide

### Infra Scenarios

| Scenario | Classification | P | Why |
|----------|---------------|---|-----|
| Core system unreachable, all agents blocked | Infra Incident | P1 | Full outage, revenue impact |
| Portal loads in 30s instead of 3s | Infra Incident | P2 | Degraded but functional |
| Nightly batch scheduler didn't trigger | Infra Incident | P2 | Job platform failed, not code |
| Vendor API changed, integration broken | Infra Incident | P1-P2 | External dependency, we own the service |
| DB password compromised | Infra Incident | P1 | Security event |

### Application Scenarios

| Scenario | Classification | P | Why |
|----------|---------------|---|-----|
| Premium calculation wrong for all products | App Incident | P1 | Financial data, all customers |
| One report shows wrong totals | App Incident | P3 | Limited scope, workaround exists |
| Claim auto-approved when it shouldn't be | App Incident | P1 | Financial + compliance risk |
| UI shows wrong currency symbol | App Incident | P4 | Cosmetic |
| Batch ran but output has wrong figures | App Incident | P1-P2 | Depends on blast radius |
| App crashes under specific load (5% users) | App Incident | P2 | Partial availability, app-level issue |
| Design flaw: missing info on customer statement | App Incident | P1-P3 | Depends on regulatory/customer impact |

### Not an Incident

| Scenario | What It Is |
|----------|-----------|
| "Can you add a report to the dashboard?" | Service Request |
| "I can't log in" (only this user) | Service Request |
| "Bug found in UAT" | Development backlog |
| "Server maintenance this weekend" | Planned Change |
| "DB password expiring, need rotation" | Standard Change |
| "It fixed itself last night" | Log it, investigate — self-healing issues recur |

---

## 8. Common Triage Mistakes

| Mistake | How to Avoid |
|---------|-------------|
| Calling a service request an incident | Ask: is something *broken*? Or is the user *requesting* something? |
| UAT bug logged as an incident | Incidents are production only |
| L1 assigning final P for application incidents alone | Application incidents need Tech Team collaboration within 30 min |
| Debugging during P1 infra incident | Restore first, investigate later |
| Rushing an application fix without testing | A bad fix creates a second incident |
| Ignoring "it fixed itself" | Self-healing issues recur. Log and investigate. |
| Not checking the Knowledge Base | Check known scenarios before escalating blind |

---

## 9. Triage Checklist

```
INCIDENT TRIAGE CHECKLIST
─────────────────────────

□ 1. IS THIS AN INCIDENT?
     □ Is something broken in production?              → YES = continue
     □ Is this a service request / feature request?    → Route to service desk
     □ Is this a non-production bug?                   → Route to dev backlog
     □ Is this a known error with workaround?          → Apply workaround

□ 2. CLASSIFY:
     □ Is infrastructure healthy?                      → NO  = Infrastructure Incident
                                                       → YES = Application Incident

□ 3. CHECK KNOWLEDGE BASE:
     □ Search for matching scenario in Knowledge Base
     □ If match found:
       □ Assign P from KB entry
       □ Execute documented first response immediately
       □ Notify tech team (inform, don't wait)
       □ Go to step 6 (tech team can re-evaluate P later)
     □ If no match → continue to step 4

□ 4. ASSIGN PRIORITY (no KB match):
     INFRA INCIDENT: assign P now (scope is clear)
     APP INCIDENT: assign preliminary P, then collaborate

     □ Data breach / security event?                   → P1
     □ Financial data affected?                        → P1
     □ Full outage / all users?                        → P1
     □ Major degradation + business hours?             → P2
     □ Partial impact / workaround exists?             → P3
     □ Cosmetic / no user impact?                      → P4

□ 5. COLLABORATE (Application Incidents, no KB match):
     □ Loop in Tech Team (Dev + BA) within 30 min
     □ Assess blast radius and business impact together
     □ Confirm or adjust priority

□ 6. ESCALATE:
     □ P1/P2 → assign Incident Commander, notify management
     □ P3/P4 → assign engineer, notify team channel

□ 7. COMMUNICATE:
     □ Post in #incidents channel
     □ Notify affected business units (P1/P2)
     □ Set next update time
```

---

## 10. Glossary

| Term | Definition |
|------|-----------|
| **Incident** | Unplanned interruption or reduction in quality of a live service |
| **Infrastructure Incident** | Incident caused by failure in the platform layer — servers, network, DB, cloud |
| **Application Incident** | Incident caused by the application layer — crash, logic error, design flaw, wrong output. Infra is healthy. |
| **Service Request** | User request for information, access, or a standard change — not a disruption |
| **Problem** | The underlying root cause of one or more incidents |
| **Known Error** | A problem with documented cause and workaround |
| **Knowledge Base** | Library of known incident scenarios, symptoms, and responses — built from RCAs over time. A KB match allows L1 to assign P and act immediately (fast lane). |
| **IC** | Incident Commander — coordinates the response |
| **Blast Radius** | Scope of impact — how many users, records, or transactions are affected |
| **Preliminary P** | Initial priority assigned by L1 for application incidents, subject to confirmation by Tech Team |
