# Incident Classification

> Single source of truth for classifying and prioritizing incidents.
> Used by L1/L2 ITO, Incident Commander, Tech Team, and Management.
>
> Related: [`swimlane-flow.drawio`](swimlane-flow.drawio) · [`incident-knowledge-base.md`](incident-knowledge-base.md)

---

## 1. Is It an Incident?

An **incident** is an unplanned interruption or quality reduction of a live production service. Not everything reported is an incident.

| Situation | Classification | Route To |
|-----------|---------------|----------|
| Something is broken in production | **Incident** | Continue to Section 2 |
| User asking for new functionality | **Service Request** | Product backlog |
| User needs access / password reset | **Service Request** | Access management |
| Bug found in UAT (not production) | **Defect** (SDLC) | Development backlog |
| Planned maintenance | **Standard Change** | Change management |
| Performance below optimal but within SLA | **Event** (monitor) | No action |
| Same bug reported again, workaround exists | **Known Error** | Apply workaround, track in Problem |
| "It fixed itself" | **Log and investigate** | Self-healing issues recur |

**Rules:**
- If the user is asking for something *new* → never an incident
- If it's not in production → never an incident
- Planned downtime is not an incident (but overrunning the window *is*)
- One user can't log in → likely a service request. All users can't log in → incident.

---

## 2. Incident Type: Infrastructure vs Application

We classify incidents by **where the problem lives** — this determines who owns the fix and how triage works.

| | Infrastructure Incident | Application Incident |
|---|---|---|
| **Definition** | Platform layer is broken — servers, network, DB, cloud services. The application cannot run because the ground underneath it is broken. | Infrastructure is healthy. Problem is at the application layer — crash, wrong output, logic error, design flaw, missing information. |
| **Key Question** | Is infrastructure healthy? → **NO** | Is infrastructure healthy? → **YES** |
| **Owner** | Infra / DevOps | Dev / BA team |
| **Detection** | **Loud** — monitoring catches it. HTTP 5xx surge, health check failure, connection timeouts, CPU > 90%. | **Often quiet** — detected by people, not alerts. Business metrics deviate, finance reconciliation fails, customer complaints about specific values. |
| **Priority Assignment** | L1 assigns directly — scope is visible. KB match → assign P from KB. No match → assign P by scope. | **KB match** → assign P from KB, act immediately, notify tech team. **No match** → assign preliminary P, collaborate with Tech Team within 30 min. |
| **Response Strategy** | Restore first, investigate later. Rollback, restart, failover. | Assess blast radius → fix correctly → remediate data. |

Both types can be **any priority level**. A silent design flaw miscalculating premiums for all customers is P1 — even though infra is green and no errors appear in logs.

### How This Maps to ITIL

"Infrastructure Incident" and "Application Incident" are not ITIL terms. ITIL defines only **Incident** (any unplanned service disruption). We split it because the response teams and strategies differ.

| ITIL Term | What It Means | When It Applies |
|-----------|--------------|-----------------|
| **Incident** | Unplanned service disruption or quality reduction | Something is broken in production |
| **Service Request** | User asking for something (not reporting breakage) | Access, information, standard change |
| **Problem** | Root cause of one or more incidents | After incident is resolved — "why did this happen?" |
| **Known Error** | Problem with documented cause and workaround | Cause understood, permanent fix pending |

### Infrastructure Incident Categories

| Category | Examples |
|----------|---------|
| **Server / Compute** | Server crash, disk full, EC2 terminated, OOM kill |
| **Network** | DNS failure, VPN down, load balancer misconfigured, firewall blocking |
| **Database** | DB crash, connections refused, replication lag, storage full |
| **Cloud Service** | AWS/Azure outage, managed service degradation |
| **Security** | DDoS, compromised credentials, ransomware, data breach |
| **Deployment** | Bad config pushed, migration failed, container image pull error |
| **Scheduled Job** | Batch didn't start, ETL timed out, scheduler failed |
| **External Dependency** | Third-party API changed, vendor gateway down |

### Application Incident Categories

| Category | Examples |
|----------|---------|
| **Application Crash** | App OOM, unhandled exception, deadlock — infra is fine but app won't run |
| **Calculation / Logic Error** | Wrong premium, incorrect claim amount, wrong tax rate |
| **Design Flaw** | Feature works as coded but produces wrong business outcome |
| **Data Integrity** | Duplicate records, missing transactions, orphaned data |
| **Integration Error** | Wrong field mapping, message format mismatch, stale cache |
| **UI / Display** | Wrong status shown, amounts in wrong currency, missing information |
| **Workflow / State** | Policy stuck in "pending", claim auto-approved incorrectly |
| **Configuration** | Wrong interest rate, incorrect eligibility rule, feature flag misconfigured |

---

## 3. Priority Matrix

| Priority | Name | Definition | Response | Escalation | Containment | Full Resolution |
|----------|------|-----------|----------|------------|-------------|-----------------|
| **P1** | Critical | Full outage, data breach, or financial data affected | < 15 min | CTO 15 min, CEO 1 hr | < 2 hours | < 24 hours |
| **P2** | Major | Significant degradation, key function unavailable | < 30 min | IT Manager 30 min | < 4 hours | < 5 business days |
| **P3** | Minor | Partial impact, workaround available | < 2 hours | Team lead if no progress 2 hrs | < 1 business day | < 10 business days |
| **P4** | Low | Cosmetic, minimal impact | Next business day | None | — | < 15 business days |

> **Containment** = service usable (even if degraded). **Full Resolution** = root cause fixed + data remediated.

### Priority Decision Questions (in order)

1. Data breach or security event? → **P1**
2. Financial data may be incorrect? → **P1**
3. All users affected / full outage? → **P1**
4. Many users affected + business hours? → **P2**
5. Few users / workaround exists? → **P3**
6. Cosmetic / no user impact? → **P4**

### Infra vs Application — Priority Nuance

**Infrastructure Incidents**: L1 assigns P directly — scope is visible (system down = P1/P2, partial = P3). If a KB match exists, use the documented P.

**Application Incidents** — path depends on Knowledge Base:
- **KB match**: L1 assigns P from KB and acts immediately. Tech team is notified and can re-evaluate.
- **No KB match**: L1 assigns a **preliminary P**, then Tech Team confirms or adjusts within 30 minutes.

Common adjustments during tech team session:

| Initial Report | Preliminary P | After Investigation | Final P |
|---|---|---|---|
| "One policy has wrong premium" | P3 | "Formula bug affecting all policies" | **P1** |
| "Report shows wrong total" | P3 | "Only one report, easy workaround" | **P3** (confirmed) |
| "App crashes intermittently" | P2 | "5% of users under specific load" | **P2** (confirmed) |
| "Customer got wrong statement" | P3 | "Batch sent wrong statements to 2,000 customers" | **P1** |

---

## 4. Severity Decision Tree

```
INCIDENT REPORTED
       │
       ▼
  Data breach or security event?  ── YES ──→  P1 CRITICAL (Security)
       │                                       → Security incident playbook
      NO                                       → Isolate, notify CISO + Legal
       │                                       → Assess regulatory obligation
       ▼
  Financial data affected?  ── YES (data may be wrong) ──→  P1 CRITICAL (Financial)
       │                                                      → Stop writes
      NO ←── (delayed but correct)                            → Scope blast radius
       │                                                      → Notify Finance + Actuarial
       ▼
  How many users affected?
       │
   ┌───┴───────────────────┬───────────────────┐
   │                       │                   │
 ALL users /             MANY users /        FEW users /      COSMETIC /
 full outage             major feature       partial impact    no user impact
   │                       │                   │                   │
   ▼                       ▼                   ▼                   ▼
P1 CRITICAL            Peak hours?          P3 MINOR           P4 LOW
 → All hands            │                    → Assigned          → Backlog
 → IC activated    YES: P2 MAJOR             engineer            → Next sprint
 → CTO 15 min      → On-call + escalation
 → Status q30m    NO: P3 MINOR
                   → Fix next business day
```

### Regulatory Reporting Triggers

These conditions may require regulatory notification regardless of priority:

| Trigger | Condition |
|---------|-----------|
| Personal data exposed or lost | Data of policyholders compromised |
| Financial transactions incorrectly processed | Above defined threshold |
| Core systems unavailable > 4 hours | During business hours |
| Any event affecting policyholder rights or benefits | Including delayed or wrong payouts |

---

## 5. Ownership and Routing

### Technical vs Business — Who Owns What

| IT Operation Owns | Operation Department Owns |
|---|---|
| System down / slow / erroring | Product/business rules |
| Login / access / MFA issues | How to use the sales system |
| Technical failures (break/fix) | Underwriting/product guidance |
| Integration timeout / data sync | Sales process exceptions |
| Browser/device/printer issues | Document sufficiency (business) |
| Known bug workarounds | Compliance interpretation |
| Incident intake, triage, KB | Frontline business coaching |

**Boundary rule**: IT Operation answers "is the system working?" — Operations answers "how do I use the system to do my job?"

### Cross-Team Grey Zone

Some issues have both a technical and business angle:

| User Reports | Technical Angle | Business Angle |
|---|---|---|
| "Error code UW-403 on proposal" | Error code → system issue | UW-403 = underwriting rule rejection |
| "Premium calculation looks wrong" | Could be a bug | Could be correct, user misunderstands rules |
| "Can't find rider option" | Screen/UI issue | Rider may not be available for this product |
| "Upload succeeded but still 'pending'" | Workflow bug | Document requirements not released |
| "System won't let me backdate" | System validation | Requires business exception approval |

**No-Bounce Protocol:**
1. First receiver owns the ticket until the other team accepts it
2. Transfer with context — never redirect the user
3. If unclear after 15 min → shared triage queue, reviewed jointly twice daily
4. If rejected by both teams → escalates to IT + Operations managers within 4 hours
5. Grey-zone patterns reviewed monthly → converted to explicit ownership rules

### Escalation Paths

| Path | When | Target |
|------|------|--------|
| **L2 Application Support** | App defects, config issues, data mismatches | Dev / BA team |
| **Infrastructure / Platform** | Servers, network, DB, cloud, deployment | Infra / DevOps |
| **L3 / Vendor** | Specialist investigation, third-party failures | External vendor or deep specialist |
| **Security / IAM** | Access anomalies, MFA, suspicious activity | Security team |
| **Operation Department** | Product rules, business clarification | Operations L1 |

---

## 6. SLA Targets

### Incident SLA

| Priority | Response | Escalation (if L1 can't resolve) | L1 Resolution / Workaround | Measurement |
|---|---|---|---|---|
| **P1** | 15 min | 30 min | 4 hours | Clock time (24/7 if on-call) |
| **P2** | 30 min | 1 hour | 8 business hours | Business hours |
| **P3** | 2 business hours | 4 business hours | 2 business days | Business hours |
| **P4** | 4 business hours | 1 business day | 5 business days | Business hours |

### Service Request Fulfillment

| Request Type | Target |
|---|---|
| Password reset / account unlock | 1 business hour |
| MFA issue | 2 business hours |
| New user access (approved) | 1 business day |
| Role/profile change | 1 business day |
| Device setup / replacement | 3 business days |

### SLA Boundaries

- **Resolution SLA applies to what L1 controls.** If L1 escalates to L2 or vendor, the L1 resolution clock pauses. L1 SLA covers response, initial diagnosis, escalation quality, and user communication.
- **SLA clock starts at triage** — when L1 confirms "this is a real incident" and logs INC-xxxx, not when the report is received.
- **Confirmation must happen within the Detect window** (< 5 min for alerts, < 15 min for user reports). L1 cannot delay confirmation to game the SLA.

---

## 7. P3/P4 Handling

Most incidents are P3/P4. The full IC / war-room machinery does not apply.

| Aspect | P3 — Minor | P4 — Low |
|--------|------------|----------|
| **Coordinator** | Senior L1 or team lead | Assigned engineer (self-managed) |
| **Response window** | Business hours, within 2 hours | Next business day |
| **Reporter updates** | At triage + resolution. On request between. | At triage + resolution only. |
| **Post-incident review** | Simplified note in ticket (5 business days) | Not required unless recurs 3+ times |
| **KB update** | Add if likely to recur | Only if pattern emerges |

P3/P4 do NOT get: Incident Commander, war room, periodic status updates, management notification, or formal RCA — unless triggered by financial/data impact or 3+ recurrences.

---

## 8. Scenario Quick Reference

### Infrastructure Scenarios

| Scenario | Type | P | Why |
|----------|------|---|-----|
| Core system unreachable, all agents blocked | Infra | P1 | Full outage, revenue impact |
| Portal loads in 30s instead of 3s | Infra | P2 | Degraded but functional |
| Nightly batch scheduler didn't trigger | Infra | P2 | Job platform failed |
| Payment gateway not responding | Infra | P1-P2 | External dependency, we own the service |
| DB password compromised | Infra | P1 | Security event |
| System slow after no deployment | Infra | P2 | Resource exhaustion |

### Application Scenarios

| Scenario | Type | P | Why |
|----------|------|---|-----|
| Premium calculation wrong for all products | App | P1 | Financial data, all customers |
| One report shows wrong totals | App | P3 | Limited scope, workaround exists |
| Claim auto-approved when it shouldn't be | App | P1 | Financial + compliance risk |
| UI shows wrong currency symbol | App | P4 | Cosmetic |
| Batch ran but output has wrong figures | App | P1-P2 | Depends on blast radius |
| 347 policies show surrender value of zero | App | P1 | Financial data + regulatory deadline |
| System slow after deployment | App | P2 | Performance regression from code |

### Not an Incident

| Scenario | What It Is |
|----------|-----------|
| "Can you add a report to the dashboard?" | Service Request |
| "I can't log in" (only this user) | Service Request |
| "Bug found in UAT" | Development backlog |
| "Server maintenance this weekend" | Planned Change |
| "How do I create a quote?" | Route to Operations L1 |
| "It fixed itself last night" | Log and investigate — self-healing issues recur |

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
     □ Is this a business/usage question?              → Route to Operations L1

□ 2. CLASSIFY:
     □ Is infrastructure healthy?                      → NO  = Infrastructure Incident
                                                       → YES = Application Incident

□ 3. CHECK KNOWLEDGE BASE:
     □ Search for matching scenario
     □ If match found:
       □ Assign P from KB entry
       □ Execute documented first response immediately
       □ Notify tech team (inform, don't wait)
       □ Go to step 6
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

## 10. Common Triage Mistakes

| Mistake | How to Avoid |
|---------|-------------|
| Calling a service request an incident | Ask: is something *broken*? Or is the user *requesting*? |
| UAT bug logged as an incident | Incidents are production only |
| L1 assigning final P for app incidents alone | App incidents need Tech Team within 30 min |
| Debugging during P1 infra incident | Restore first, investigate later |
| Rushing an app fix without testing | A bad fix creates a second incident |
| Ignoring "it fixed itself" | Self-healing issues recur. Log and investigate. |
| Not checking the Knowledge Base | Check known scenarios before escalating blind |
| Assuming "slow = infra" | Check the change calendar. Post-deployment → assume app first. |
| "Vendor's fault" as a reason to do nothing | We own the service, we own the response |
| "No errors in logs" = everything is correct | The most dangerous bugs don't throw errors |

---

## 11. Glossary

| Term | Definition |
|------|-----------
| **Incident** | Unplanned interruption or reduction in quality of a live service |
| **Infrastructure Incident** | Incident caused by failure in the platform layer — servers, network, DB, cloud |
| **Application Incident** | Incident caused by the application layer — crash, logic error, design flaw, wrong output. Infra is healthy. |
| **Service Request** | User request for information, access, or a standard change — not a disruption |
| **Problem** | The underlying root cause of one or more incidents |
| **Known Error** | A problem with documented cause and workaround |
| **Knowledge Base** | Library of known incident scenarios, symptoms, and responses — built from RCAs. KB match allows L1 to assign P and act immediately. |
| **IC** | Incident Commander — coordinates the response for P1/P2 |
| **Blast Radius** | Scope of impact — how many users, records, or transactions are affected |
| **Preliminary P** | Initial priority assigned by L1 for app incidents (no KB match), subject to Tech Team confirmation |
| **Containment** | Service usable again, even if degraded or with feature disabled |
| **Full Resolution** | Root cause fixed, data remediated, monitoring confirms stable |
| **RFC** | Request for Change — required for emergency changes during incident response |
| **Major Incident** | P1 incident requiring War Room, IC, and stakeholder notification |
