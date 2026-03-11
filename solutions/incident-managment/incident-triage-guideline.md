# Incident Triage Guideline

> A practical guide for L1/L2 support and on-call engineers to correctly identify, classify, and triage IT incidents.
>
> Related: [`swimlane-flow.md`](swimlane-flow.md) (process flow) · [`severity-triage.md`](severity-triage.md) (decision tree) · [`lightweight.md`](lightweight.md) (detailed flowchart)

---

## 1. Is "Production Defect" an ITIL Term?

**No.** ITIL does not define "production defect", "production issue", or "bug". These are software development terms from the SDLC world.

ITIL defines a precise vocabulary for service management. Understanding this vocabulary is essential to avoid confusion during triage.

### What ITIL Actually Defines

| ITIL Term | Definition | Key Point |
|-----------|-----------|-----------|
| **Incident** | An unplanned interruption to a service, or reduction in the quality of a service | Anything that disrupts what the user expects from a live service — whether the system is down OR producing wrong results |
| **Service Request** | A request from a user for something that is part of normal service delivery — information, access, a standard change | Not a disruption. The user is asking for something, not reporting something broken. |
| **Problem** | The underlying cause of one or more incidents | A problem is identified *after* incidents occur. It explains *why* the incident happened. |
| **Known Error** | A problem that has been analyzed and has a documented root cause and workaround | The cause is understood, a workaround exists, but the permanent fix hasn't been deployed yet. |
| **Event** | Any change of state that has significance for the management of a service | Not all events are incidents. An event becomes an incident only when it disrupts or degrades service. |

### So Where Does "Production Defect" Fit?

A **production defect** is a bug in code that exists in the production environment. In ITIL terms:

- If the defect **disrupts service or produces incorrect results** → it is an **Incident** (because service quality is reduced)
- After the incident is resolved (service restored or workaround applied) → the underlying bug is tracked as a **Problem**
- Once the bug is analyzed and a workaround is documented → it becomes a **Known Error**
- The code fix goes through **Change Management** → deployed via **Release Management**

**The defect itself is never triaged. The incident it causes is triaged.** This is an important distinction — during triage, you are classifying the *impact on service*, not diagnosing the *technical root cause*.

```
Production Defect (SDLC term)
    │
    ├── Is it impacting a live service? ── YES ──→ It's an INCIDENT (ITIL)
    │                                                   │
    │                                                   ├── Resolve the incident (restore/workaround)
    │                                                   └── Track the bug as a PROBLEM (ITIL)
    │                                                         └── Fix via CHANGE MANAGEMENT (ITIL)
    │
    └── Is it NOT impacting a live service? ── YES ──→ It's a BACKLOG ITEM (SDLC)
                                                        Not an incident. Fix in the next sprint.
```

---

## 2. What Happens During Triage?

Triage is about answering **three questions fast**:

1. **Is this actually an incident?** (or is it something else?)
2. **How bad is it?** (severity)
3. **Who needs to act?** (assignment and escalation)

Triage is explicitly **not** about:
- Finding root cause (that's Problem Management)
- Fixing anything (that's the Respond phase)
- Deciding whether it's a "bug" or "infra issue" at a technical level

### Do We Classify "Production Defects" During Triage?

**Not exactly.** During triage, we classify the **type of service impact**, not the technical root cause. We use two categories:

| Classification | Service Impact | Example |
|---|---|---|
| **Technology Incident** | Service is **unavailable or degraded** — users cannot use the system | "The claims portal is down" |
| **Production Issue** | Service is **running but producing incorrect results** — outputs are wrong | "Premium calculations are showing wrong amounts" |

Both are **incidents** in ITIL terms. We split them because they require **different response strategies**:

- Technology Incident → **restore service immediately** (restart, rollback, failover)
- Production Issue → **assess impact first, then fix correctly** (investigate, test, deploy, remediate data)

A "production defect" typically surfaces as a **Production Issue** — but the triage responder doesn't need to confirm it's a code bug. They only need to determine: *is the system down, or is it up but wrong?*

### The Triage Flow

```
    Something is reported
            │
            ▼
    ┌───────────────────┐
    │ Is this actually   │
    │ an incident?       │──── NO ──→ Route elsewhere (see Section 3)
    └───────┬───────────┘
            │ YES
            ▼
    ┌───────────────────┐
    │ Can users access   │
    │ the system?        │
    └───────┬───────────┘
            │
     ┌──────┴──────┐
     │             │
     NO           YES
     │             │
     ▼             ▼
 TECHNOLOGY    ┌────────────────┐
 INCIDENT      │ Are results    │
               │ correct?       │
               └──────┬─────────┘
                      │
               ┌──────┴──────┐
               │             │
              YES            NO
               │             │
               ▼             ▼
          Not an         PRODUCTION
          incident       ISSUE
          (close/monitor)
```

After classification, assign priority (P1–P4) based on business impact, then assign ownership and escalate per priority level.

---

## 3. What Is NOT a Technology Incident — Scenario-Based Guide

This is where most triage confusion happens. The following scenarios walk through common situations and how to classify them correctly.

### Scenario 1: "I can't log in to the system"

| Question | Answer | Classification |
|---|---|---|
| Can other users log in? | Yes, it's just this one user | **Not an incident** — it's likely a user account issue |
| What to do? | Check if the account is locked, password expired, or permissions missing | Route as a **Service Request** (access management) |

**But if**: No users can log in → **Technology Incident** (authentication service may be down)

---

### Scenario 2: "Can you add a new report to the dashboard?"

| Question | Answer | Classification |
|---|---|---|
| Is something broken? | No — the user is asking for new functionality | **Not an incident** |
| What to do? | Log as a **Service Request** or **Feature Request** | Route to product backlog |

**Rule**: If the user is asking for something *new* rather than reporting something *broken*, it is never an incident.

---

### Scenario 3: "The system is slow today"

| Question | Answer | Classification |
|---|---|---|
| How slow? Can users complete transactions? | Takes 30 seconds instead of 3 seconds, but eventually works | **Technology Incident** — service quality is degraded below acceptable threshold |
| How slow? | Takes 1-2 seconds longer than usual but within SLA | **Not an incident** — performance is within acceptable range. Monitor. |

**Rule**: "Slow" becomes an incident when it degrades the service below the agreed service level or prevents users from completing tasks within a reasonable time.

---

### Scenario 4: "The premium amount on this policy looks wrong"

| Question | Answer | Classification |
|---|---|---|
| Is the system accessible? | Yes — running fine | Not a technology incident |
| Is the output correct? | No — the premium amount is incorrect | **Production Issue** (incident caused by a defect) |
| Is it one policy or many? | Need to investigate | Determines priority — one policy might be P3, systematic error across all policies is P1 |

---

### Scenario 5: "The nightly batch didn't run"

| Question | Answer | Classification |
|---|---|---|
| Did the job fail to start, or did it start and produce wrong results? | It didn't start at all | **Technology Incident** — scheduled job failure |
| Did the job run but produce wrong data? | Yes, it completed but output files have wrong figures | **Production Issue** — logic/data error in batch processing |

---

### Scenario 6: "We need to reset the database password"

| Question | Answer | Classification |
|---|---|---|
| Is something broken? | No — the password is expiring per policy and needs rotation | **Not an incident** |
| What to do? | This is a **Standard Change** — a pre-approved, routine operational task | Route via Change Management or as a Service Request |

**But if**: The database password was compromised → **Technology Incident** (security event, likely P1)

---

### Scenario 7: "This bug was found in UAT"

| Question | Answer | Classification |
|---|---|---|
| Is it affecting a live production service? | No — it's in UAT (non-production) | **Not an incident** |
| What to do? | Log as a **Defect** in the development backlog | Fix before release. This is SDLC, not incident management. |

**Rule**: Incidents only apply to **live services in production**. Bugs found in testing environments are defects in the development pipeline — they never enter the incident management process.

---

### Scenario 8: "The vendor's API changed and our integration is broken"

| Question | Answer | Classification |
|---|---|---|
| Is a live service affected? | Yes — payment processing is failing | **Technology Incident** — third-party dependency failure |
| Is it our system that's wrong? | No — the vendor changed their API without notice | Still our incident — we own the service to our users regardless of whose fault it is |

**Rule**: Incident ownership follows the service, not the fault. If your users are impacted, it's your incident to manage — even if the root cause is a third party.

---

### Scenario 9: "The system crashed last night but it's fine now"

| Question | Answer | Classification |
|---|---|---|
| Is the service currently impacted? | No — it recovered on its own | The incident is **resolved**, but still needs to be **logged** |
| What to do? | Log it as a past incident. Investigate to prevent recurrence. | Self-healing incidents often recur. Ignoring them is how intermittent outages become chronic. |

---

### Scenario 10: "We're planning server maintenance this weekend"

| Question | Answer | Classification |
|---|---|---|
| Is it unplanned? | No — it's planned and communicated | **Not an incident** — it's a **Planned Change** |
| What if the maintenance goes wrong and service isn't restored on time? | Then it becomes a **Technology Incident** at the point when the planned maintenance window is exceeded |

**Rule**: Planned downtime is not an incident. Unplanned extension of planned downtime *is* an incident.

---

### Summary: Classification Quick Reference

| Situation | Classification | Route To |
|-----------|---------------|----------|
| System is down or unreachable | **Technology Incident** | Incident Management |
| System is up but producing wrong results | **Production Issue** (Incident) | Incident Management |
| User asking for something new | **Service Request** | Service Desk / Backlog |
| User needs access, password reset, permissions | **Service Request** | Access Management |
| Planned maintenance or routine change | **Standard Change** | Change Management |
| Bug found in non-production environment | **Defect** (SDLC) | Development Backlog |
| Performance slightly below optimal but within SLA | **Event** (monitor) | Monitoring / No action |
| Root cause investigation after incident is resolved | **Problem** | Problem Management |
| Known bug with a documented workaround | **Known Error** | Problem Management |

---

## 4. Technology Incident — Categories and Detection

### Categories

| Category | Description | Examples |
|----------|------------|---------|
| **Infrastructure Failure** | Hardware or cloud infrastructure component fails | Server crash, disk full, EC2 instance terminated, RDS failover, AZ outage |
| **Network / Connectivity** | Network path between components or to users is broken | DNS resolution failure, VPN tunnel down, load balancer misconfiguration, firewall rule blocking traffic |
| **Platform / Middleware** | Application platform or middleware layer fails | Application server out of memory, message queue full, connection pool exhausted, certificate expired |
| **Deployment-Related** | A recent deployment breaks the running service | Bad configuration pushed, incompatible dependency deployed, migration script failed, container image pull error |
| **Security Event** | Unauthorized access or attack degrades service | DDoS attack, compromised credentials, ransomware, data breach |
| **Third-Party / External** | External dependency becomes unavailable | Payment gateway down, SMS provider unreachable, cloud service outage, vendor API change |
| **Capacity / Performance** | System overwhelmed by load or resource exhaustion | CPU/memory saturation, database connection limit, storage full, auto-scaling failure |
| **Scheduled Job Failure** | Batch or scheduled process fails to run or complete | Nightly batch didn't start, ETL job timed out, report generation failed |

### Detection — Technology Incidents Are Loud

| Detection Method | What It Catches | Tools / Sources |
|-----------------|----------------|-----------------|
| **Infrastructure monitoring** | Server down, CPU/memory/disk saturation, instance health | CloudWatch, Prometheus, Datadog, Zabbix |
| **Application health checks** | Service unresponsive, endpoint returning errors | Load balancer health checks, K8s liveness/readiness probes |
| **Synthetic monitoring** | End-to-end user journey broken | CloudWatch Synthetics, Pingdom, Uptime Robot |
| **Error rate spike** | Sudden increase in HTTP 5xx, application exceptions | APM tools, CloudWatch Logs |
| **Latency spike** | Response times above acceptable threshold | APM, CloudWatch, custom metrics |
| **Heartbeat / dead man's switch** | Batch job didn't run or complete on time | Cron watchdog, CloudWatch Events |
| **User reports** | System inaccessible, error pages | Help desk, Slack/Teams, phone |
| **Cloud provider notifications** | AWS/Azure service degradation | AWS Health Dashboard, status pages |

**Key signals**: HTTP 5xx surge, health check failure, DB connections refused, "connection timeout" in logs, CPU > 90% sustained, deployment just happened + errors started, multiple users reporting same access issue.

---

## 5. Production Issue — Categories and Detection

### Categories

| Category | Description | Examples |
|----------|------------|---------|
| **Calculation / Logic Error** | Business logic produces wrong results | Premium calculated incorrectly, wrong tax rate, claim amount miscalculated |
| **Data Integrity** | Data is corrupted, duplicated, or lost | Duplicate policy records, missing transactions, orphaned records |
| **Integration Defect** | Data exchange between systems is incorrect | Wrong field mapping, message format mismatch, stale cache |
| **UI / Display Error** | User interface shows incorrect information | Wrong policy status, amounts in wrong currency, incorrect name |
| **Workflow / State Error** | Business process reaches an invalid state | Policy stuck in "pending", claim auto-approved when it shouldn't be |
| **Report / Output Error** | Reports or exports contain wrong data | Regulatory report with wrong figures, reconciliation mismatch |
| **Configuration Error** | Feature flag, rule, or parameter set incorrectly | Wrong interest rate configured, incorrect eligibility rule |

### Detection — Production Issues Are Quiet

| Detection Method | What It Catches | Tools / Sources |
|-----------------|----------------|-----------------|
| **Business metric anomaly** | Unusual pattern in KPIs (policy count, premium volume, claims rate) | BI dashboards, custom alerts |
| **Data reconciliation** | Numbers don't match between systems | Scheduled reconciliation jobs, finance team |
| **User / business report** | "This number doesn't look right" | Help desk, business unit escalation |
| **QA / regression testing** | Previously passing test now fails | Test automation, manual QA |
| **Audit / compliance check** | Regulatory report doesn't match source data | Internal audit, compliance review |
| **Integration error logs** | Messages rejected by downstream system | Middleware logs, API error responses |
| **Customer complaint** | Wrong statement, incorrect premium charge | Customer service, complaints channel |

**Key signals**: Business metric deviates from historical pattern, finance reports reconciliation mismatch, customer complaints about specific values, batch completes but output data is wrong, one feature produces wrong results while everything else works.

---

## 6. Priority Assignment

| Priority | Name | Definition | Response | Resolution Target | Escalation |
|----------|------|-----------|----------|-------------------|------------|
| **P1** | Critical | Full outage, data breach, or financial data corruption | Immediate | < 1 hour | CTO 15 min, CEO 1 hr |
| **P2** | Major | Significant degradation, key function unavailable | < 15 min | < 4 hours | IT Manager 30 min |
| **P3** | Minor | Partial impact, workaround available | < 1 hour | < 1 business day | Team lead if no progress 2 hrs |
| **P4** | Low | Cosmetic, minimal impact | Next business day | < 5 business days | None |

### Priority Decision Questions (in order)

1. Data breach or security event? → **P1**
2. Financial data may be incorrect? (premiums, claims, policy values) → **P1**
3. All users affected / full outage? → **P1**
4. Many users affected + during business hours? → **P2**
5. Few users / partial impact / workaround exists? → **P3**
6. Cosmetic / no user impact? → **P4**

---

## 7. Common Triage Mistakes

| Mistake | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Calling a service request an incident** | User says "urgent" so it gets logged as an incident | Ask: is something *broken*? Or is the user *requesting* something? |
| **Calling a defect in UAT an incident** | QA found a bug and wants it fixed immediately | Incidents are for **production services only**. UAT bugs are development backlog items. |
| **Treating a defect as an outage** | System returns errors for one feature, triage assumes full outage | Check: are other features working? Is the system accessible overall? |
| **Treating an outage as a defect** | Service is slow, triage logs it as a bug for the dev team | Check: is response time below SLA? Are users unable to complete tasks? That's a technology incident. |
| **Logging a known error as a new incident** | The same bug is reported again by a different user | Check the known error database first. Apply the documented workaround. |
| **Under-classifying priority** | Fear of escalation, "it's probably not that bad" | When in doubt, escalate. Downgrading is easy. Explaining why you didn't escalate a P1 is not. |
| **Over-classifying priority** | Business pressure, "everything is critical" | Require evidence: how many users? What function is impacted? |
| **Debugging during P1** | Engineer instinct to understand before acting | Technology Incidents: restore first, investigate later. |
| **Rushing a code fix without testing** | Pressure to resolve quickly | Production Issues: a bad fix creates a second incident. Test properly. |
| **Ignoring "it fixed itself"** | Issue disappeared before investigation | Self-healing issues recur. Log it. Investigate when possible. |
| **Confusing planned downtime with an incident** | Maintenance overran and triage doesn't know it was planned | Maintain a change calendar. Check it during triage. |

---

## 8. How It All Connects

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    User reports     Alert fires     Batch fails     Business finds          │
│    "it's broken"    (monitoring)    (heartbeat)     wrong numbers           │
│         │               │               │               │                  │
│         └───────────────┴───────────────┴───────────────┘                  │
│                                   │                                        │
│                                   ▼                                        │
│                        ┌─────────────────────┐                             │
│                        │     TRIAGE           │                             │
│                        │  (this document)     │                             │
│                        │                      │                             │
│                        │  1. Is it incident?  │──── NO ──→ Service Request │
│                        │  2. What type?       │            Feature Request  │
│                        │  3. How severe?      │            Standard Change  │
│                        │  4. Who handles it?  │            Backlog item     │
│                        └──────────┬───────────┘                             │
│                                   │ YES — it's an incident                 │
│                                   │                                        │
│                    ┌──────────────┴──────────────┐                         │
│                    │                             │                          │
│                    ▼                             ▼                          │
│           Technology Incident           Production Issue                    │
│           (service unavailable)         (service incorrect)                │
│                    │                             │                          │
│                    ▼                             ▼                          │
│            RESTORE SERVICE             ASSESS IMPACT                       │
│            restart / rollback /        reproduce / quantify /              │
│            failover                    stop if corrupting                   │
│                    │                             │                          │
│                    └──────────────┬──────────────┘                         │
│                                   │                                        │
│                                   ▼                                        │
│                           SERVICE RESTORED                                 │
│                           or workaround applied                            │
│                                   │                                        │
│                                   ▼                                        │
│                        ┌─────────────────────┐                             │
│                        │  PROBLEM MANAGEMENT  │                            │
│                        │  (root cause)        │                            │
│                        └──────────┬───────────┘                            │
│                                   │                                        │
│                                   ▼                                        │
│                        ┌─────────────────────┐                             │
│                        │  CHANGE MANAGEMENT   │                            │
│                        │  (permanent fix)     │                            │
│                        └──────────┬───────────┘                            │
│                                   │                                        │
│                                   ▼                                        │
│                        ┌─────────────────────┐                             │
│                        │  RELEASE MANAGEMENT  │                            │
│                        │  (deploy fix)        │                            │
│                        └─────────────────────┘                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Triage Checklist (Quick Reference)

```
INCIDENT TRIAGE CHECKLIST
─────────────────────────

□ 1. IS THIS AN INCIDENT?
     □ Is something broken in production?           → YES = continue
     □ Is this a request for something new?         → NO  = Service Request
     □ Is this a bug in a test environment?          → NO  = Development backlog
     □ Is this planned maintenance?                  → NO  = Change Management
     □ Is this a known error with a workaround?      → NO  = Apply workaround, link to problem

□ 2. CLASSIFY THE IMPACT:
     □ Can users access the system?                 → NO  = Technology Incident
     □ Is the system producing correct results?     → NO  = Production Issue

□ 3. ASSIGN PRIORITY:
     □ Data breach / security event?                → P1
     □ Financial data incorrect?                    → P1
     □ Full outage / all users affected?            → P1
     □ Major degradation + business hours?          → P2
     □ Partial impact / few users?                  → P3
     □ Cosmetic / no user impact?                   → P4

□ 4. IMMEDIATE ACTIONS:
     □ Technology Incident → attempt restore (restart / rollback / failover)
     □ Production Issue    → assess blast radius, stop writes if data corrupting
     □ Open incident ticket with: type, priority, affected system, description

□ 5. ASSIGN & ESCALATE:
     □ P1/P2 → assign Incident Commander, notify management
     □ P3/P4 → assign engineer, notify team channel

□ 6. COMMUNICATE:
     □ Post initial status in #incidents channel
     □ Notify affected business units (P1/P2)
     □ Set next update time
```

---

## 10. Glossary

| Term | Definition |
|------|-----------|
| **Incident** | Unplanned interruption or reduction in quality of a live service |
| **Technology Incident** | Incident where the service is down, unreachable, or degraded — an availability problem |
| **Production Issue** | Incident where the service is running but producing incorrect results — a correctness problem. Not a formal ITIL term; used operationally to distinguish from availability incidents. |
| **Service Request** | A user request for information, access, or a standard change — not a disruption |
| **Problem** | The underlying root cause of one or more incidents |
| **Known Error** | A problem with a documented root cause and workaround |
| **Event** | Any change of state significant to a service — not all events are incidents |
| **Standard Change** | A pre-approved, low-risk, routine change (e.g., password rotation, scheduled patching) |
| **Workaround** | A temporary solution that reduces impact without resolving root cause |
| **RCA** | Root Cause Analysis — structured investigation into why an incident occurred |
| **MTTR** | Mean Time To Restore — average time from detection to service restoration |
| **MTTD** | Mean Time To Detect — average time from occurrence to detection |
| **IC** | Incident Commander — person coordinating the incident response |
| **Blast Radius** | The scope of impact — how many users, records, transactions, or systems are affected |
