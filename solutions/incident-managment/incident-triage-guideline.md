# Incident Triage Guideline

> A practical guide for L1/L2 support and on-call engineers to correctly identify, classify, and triage IT incidents. Aligned with ITIL 4 practices.
>
> Related: [`swimlane-flow.md`](swimlane-flow.md) (process flow) · [`severity-triage.md`](severity-triage.md) (decision tree) · [`lightweight.md`](lightweight.md) (detailed flowchart)

---

## 1. ITIL Foundations — What Is an Incident?

### ITIL 4 Definition

> **Incident**: An unplanned interruption to a service, or reduction in the quality of a service.
>
> — ITIL 4: Service Value System

The goal of Incident Management is **not** to find root cause. It is to **restore normal service operation as quickly as possible** and minimize business impact. Root cause analysis belongs to the Problem Management practice.

### The Critical Distinction: Incident vs Problem vs Defect

| ITIL Concept | Definition | Goal | Timeframe | Owner |
|---|---|---|---|---|
| **Incident** | An event that disrupts or degrades a live service | Restore service | Minutes to hours | Incident Manager / On-call |
| **Problem** | The underlying cause of one or more incidents | Eliminate root cause | Days to weeks | Problem Manager / Engineering |
| **Known Error** | A problem with a documented root cause and workaround | Document and manage | Ongoing | Problem Manager |
| **Change Request** | A planned modification to a service or component | Implement improvement | Planned schedule | Change Manager |

A **defect** (bug) is not an ITIL term — it lives in the software development lifecycle. However, a defect in production **becomes** an incident when it disrupts service or produces incorrect results. After the incident is resolved, the defect is tracked as a **problem** for permanent fix.

---

## 2. Technology Incident vs Production Issue (Defect)

This is the most common source of confusion during triage. Both are incidents, but they require **different response strategies**.

### Technology Incident

**Definition**: An unplanned interruption or degradation where the IT infrastructure, platform, or service is **unavailable, unreachable, or performing below acceptable thresholds**.

The system **cannot do its job**.

#### Characteristics

- Service is down, unresponsive, or extremely slow
- Users receive errors when trying to access the system (HTTP 5xx, connection timeout, "service unavailable")
- Infrastructure components have failed (server, database, network, storage, cloud service)
- The issue is typically **environment-related**, not code-related
- Restoring service does not require a code change — it requires operational action

#### Categories of Technology Incidents

| Category | Description | Examples |
|----------|------------|---------|
| **Infrastructure Failure** | Hardware or cloud infrastructure component fails | Server crash, disk full, EC2 instance terminated, RDS failover, AZ outage |
| **Network / Connectivity** | Network path between components or to users is broken | DNS resolution failure, VPN tunnel down, load balancer misconfiguration, firewall rule blocking traffic |
| **Platform / Middleware** | Application platform or middleware layer fails | Application server out of memory, message queue full, connection pool exhausted, certificate expired |
| **Deployment-Related** | A recent deployment breaks the running service | Bad configuration pushed, incompatible dependency deployed, migration script failed, container image pull error |
| **Security Event** | Unauthorized access or attack degrades service | DDoS attack, compromised credentials, ransomware, data breach |
| **Third-Party / External** | External dependency becomes unavailable | Payment gateway down, SMS provider unreachable, cloud service outage (AWS, Azure), vendor API change |
| **Capacity / Performance** | System overwhelmed by load or resource exhaustion | CPU/memory saturation, database connection limit, storage full, auto-scaling failure |
| **Scheduled Job Failure** | Batch or scheduled process fails to run or complete | Nightly batch didn't start, ETL job timed out, report generation failed, data sync missed window |

#### Response Strategy

```
Priority: RESTORE SERVICE FIRST, investigate later.

Immediate actions:
1. Failover to healthy replica/region
2. Rollback recent deployment or config change
3. Restart failed services/processes
4. Enable maintenance page / circuit breakers
5. Scale up resources if capacity-related

Do NOT spend time debugging during a SEV1/2 outage.
Restore first. Understand later.
```

---

### Production Issue (Defect)

**Definition**: The system is **running and accessible**, but producing **incorrect results**. A bug, logic error, or data corruption in production that causes wrong business outcomes.

The system **can do its job, but does it wrong**.

#### Characteristics

- Service appears healthy — monitoring may show green
- Users can access the system, but outputs/calculations/data are wrong
- The issue is typically **code-related** or **data-related**, not infrastructure
- Restoring correctness requires a code fix, configuration correction, or data remediation
- Impact may be **silent** — no alerts fire, no users complain immediately, but business data is being corrupted

#### Categories of Production Issues

| Category | Description | Examples |
|----------|------------|---------|
| **Calculation / Logic Error** | Business logic produces wrong results | Premium calculated incorrectly, wrong tax rate applied, claim amount miscalculated, policy value off |
| **Data Integrity** | Data is corrupted, duplicated, or lost | Duplicate policy records, missing transaction entries, orphaned records after failed operation |
| **Integration Defect** | Data exchange between systems is incorrect | Wrong field mapping, message format mismatch, API contract violation, stale cache serving old data |
| **UI / Display Error** | User interface shows incorrect information | Wrong policy status displayed, amounts shown in wrong currency, incorrect beneficiary name |
| **Workflow / State Error** | Business process reaches an invalid state | Policy stuck in "pending" forever, claim auto-approved when it should require manual review |
| **Report / Output Error** | Generated reports or exports contain wrong data | Regulatory report with wrong figures, financial reconciliation mismatch, incorrect customer statements |
| **Configuration Defect** | Feature flag, rule, or parameter set incorrectly | Wrong interest rate configured, incorrect product eligibility rule, feature enabled for wrong user segment |

#### Response Strategy

```
Priority: ASSESS BLAST RADIUS, then fix correctly.

Immediate actions:
1. Reproduce and confirm the incorrect behavior
2. Quantify impact: how many records/customers/transactions affected?
3. If data is actively being corrupted → stop writes (disable feature, pause batch)
4. Root cause analysis: code bug, config error, or data issue?
5. Develop fix with proper testing
6. Deploy through normal CI/CD pipeline (not a hotfix bypass)
7. Remediate corrupted data (backup first!)

Do NOT rush a code fix without testing.
A bad fix on top of a bad bug makes things worse.
```

---

### Side-by-Side Comparison

| Dimension | Technology Incident | Production Issue (Defect) |
|-----------|-------------------|--------------------------|
| **System state** | Down, unreachable, or degraded | Running but producing wrong results |
| **User experience** | "I can't access the system" | "The system gave me a wrong number" |
| **Alerts** | Monitoring fires immediately | Often silent — may go undetected for hours/days |
| **Root cause** | Infrastructure, platform, environment | Code, logic, configuration, data |
| **Fix type** | Operational action (restart, rollback, failover) | Code change + testing + deployment |
| **Speed vs correctness** | Speed wins — restore first | Correctness wins — test before deploying |
| **Data remediation** | Rarely needed | Often needed |
| **ITIL mapping** | Incident → restore → Problem (optional) | Incident → workaround → Problem → Change → deploy fix |
| **Typical owner** | Infra / DevOps / SRE | Development team |
| **Biggest risk** | Extended outage → revenue loss, SLA breach | Silent corruption → financial/regulatory impact |

---

## 3. How to Detect — Signals by Category

### Technology Incident Detection

These are typically **loud** — someone or something tells you quickly.

| Detection Method | What It Catches | Tools / Sources |
|-----------------|----------------|-----------------|
| **Infrastructure monitoring** | Server down, CPU/memory/disk saturation, instance health | CloudWatch, Prometheus, Datadog, Zabbix |
| **Application health checks** | Service unresponsive, endpoint returning errors | Load balancer health checks, Kubernetes liveness/readiness probes |
| **Synthetic monitoring** | End-to-end user journey broken | CloudWatch Synthetics, Pingdom, Uptime Robot |
| **Error rate spike** | Sudden increase in HTTP 5xx, application exceptions | APM tools (New Relic, Dynatrace), CloudWatch Logs |
| **Latency spike** | Response times above acceptable threshold | APM, CloudWatch, custom metrics |
| **Heartbeat / dead man's switch** | Batch job didn't run or didn't complete on time | Scheduled check (cron watchdog), CloudWatch Events |
| **User reports** | System inaccessible, error pages displayed | Help desk, Slack/Teams channel, phone calls |
| **Cloud provider notifications** | AWS/Azure service degradation or maintenance | AWS Health Dashboard, status pages |

#### Key Signals That Scream "Technology Incident"

- HTTP 5xx error rate > 1% (or any 503/502 surge)
- Service health check failing
- Database connections refused or timed out
- "Connection timeout" or "Service unavailable" in logs
- CPU > 90% sustained, memory > 85%, disk > 90%
- Deployment just happened + errors started
- Multiple users reporting the same access issue simultaneously

---

### Production Issue Detection

These are typically **quiet** — the system looks healthy but the output is wrong.

| Detection Method | What It Catches | Tools / Sources |
|-----------------|----------------|-----------------|
| **Business metric anomaly** | Unusual pattern in business KPIs (policy count, premium volume, claims rate) | BI dashboards, custom alerts on business metrics |
| **Data reconciliation** | Numbers don't match between systems or between system and manual records | Scheduled reconciliation jobs, finance team checks |
| **User/business report** | "This number doesn't look right" — business user notices incorrect output | Help desk, direct escalation from business unit |
| **QA / regression testing** | Test case that was passing now fails, or new test reveals existing bug | Test automation, manual QA cycles |
| **Audit / compliance check** | Regulatory report doesn't match source data, audit trail has gaps | Internal audit, compliance review, external audit |
| **Integration error logs** | Messages rejected by downstream system, data format mismatches | Integration middleware logs, API error responses |
| **Customer complaint** | Policyholder receives wrong statement, incorrect premium charge | Customer service, complaints channel |

#### Key Signals That Suggest "Production Issue"

- Business metric deviates from historical pattern without business explanation
- Finance reports "numbers don't add up" during reconciliation
- Customer complaints about specific incorrect values
- Integration partner reports receiving malformed or incorrect data
- Batch job completes successfully but output data is wrong
- One specific feature produces wrong results while everything else works
- "It was working fine last week" + a recent deployment happened

---

## 4. Triage Decision Flow

When an event is reported, the triage responder (L1 Support / On-call) should follow this sequence:

### Step 1 — Is This an Incident?

Not everything reported is an incident. Filter first.

| It IS an incident if... | It is NOT an incident if... |
|---|---|
| A live service is disrupted or degraded | It's a feature request ("can we add...") |
| Production data is incorrect | It's a known limitation documented in release notes |
| Multiple users are affected | It's a user error (wrong input, forgot password) |
| Business operations are impacted | It's already being tracked as a known problem with a workaround |
| It was working before and now it's not | It only occurs in non-production environments |

### Step 2 — Classify the Type

```
                    ┌─────────────────────────┐
                    │   Is the system          │
                    │   accessible and         │
                    │   responding?            │
                    └────────┬────────────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
            NO / DEGRADED           YES / NORMAL
                 │                       │
                 ▼                       ▼
    ┌─────────────────────┐  ┌──────────────────────┐
    │  TECHNOLOGY          │  │  Are the outputs     │
    │  INCIDENT            │  │  and results         │
    │                      │  │  correct?             │
    │  → Restore service   │  └─────────┬────────────┘
    └──────────────────────┘            │
                              ┌────────┴────────┐
                              │                 │
                           YES                 NO
                              │                 │
                              ▼                 ▼
                    ┌──────────────┐  ┌──────────────────┐
                    │  NOT AN      │  │  PRODUCTION       │
                    │  INCIDENT    │  │  ISSUE (DEFECT)   │
                    │              │  │                    │
                    │  → Close or  │  │  → Fix & remediate│
                    │    monitor   │  └────────────────────┘
                    └──────────────┘
```

### Step 3 — Assign Severity

| Question | If YES → | If NO → |
|----------|----------|---------|
| Data breach or security event? | **SEV 1** — invoke security playbook | Continue ↓ |
| Financial data may be incorrect? (premiums, claims, policy values) | **SEV 1** — stop writes, assess blast radius | Continue ↓ |
| All users affected / full outage? | **SEV 1** — all-hands response | Continue ↓ |
| Many users affected + during business hours? | **SEV 2** — on-call + escalation | Continue ↓ |
| Few users affected / partial impact? | **SEV 3** — assigned engineer, business hours | Continue ↓ |
| Cosmetic / no user impact? | **SEV 4** — backlog, next sprint | — |

### Step 4 — Assign and Escalate

| Severity | Assign To | Escalate To | Notify | Communication |
|----------|-----------|-------------|--------|---------------|
| **SEV 1** | Incident Commander + all available engineers | CTO within 15 min, CEO within 1 hr | All IT + affected business units | Status update every 30 min |
| **SEV 2** | Incident Commander + on-call engineer | IT Manager within 30 min | On-call team + affected business units | Status update every 1 hr |
| **SEV 3** | Assigned engineer | Team lead if no progress in 2 hrs | Team channel | Update when resolved |
| **SEV 4** | Assigned developer | None | None | Resolved in sprint |

---

## 5. ITIL Process Mapping — How It All Connects

Understanding where incident triage fits within the broader ITIL service management:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        ITIL 4 — Incident Lifecycle                      │
│                                                                          │
│   EVENT                                                                  │
│     │                                                                    │
│     ▼                                                                    │
│   INCIDENT MANAGEMENT ─────────────────────────────────────────────┐     │
│   (this document)                                                  │     │
│     │                                                              │     │
│     ├── Detect ──► Triage ──► Respond ──► Resolve ──► Close       │     │
│     │                                                              │     │
│     │   If recurring or root cause unknown:                        │     │
│     │     │                                                        │     │
│     │     ▼                                                        │     │
│     │   PROBLEM MANAGEMENT                                         │     │
│     │     │                                                        │     │
│     │     ├── Investigate root cause                               │     │
│     │     ├── Document as Known Error (with workaround)            │     │
│     │     └── Request permanent fix                                │     │
│     │           │                                                  │     │
│     │           ▼                                                  │     │
│     │         CHANGE MANAGEMENT                                    │     │
│     │           │                                                  │     │
│     │           ├── Evaluate change (risk, impact, schedule)       │     │
│     │           ├── Approve change                                 │     │
│     │           └── Implement change (code fix, infra change)      │     │
│     │                 │                                            │     │
│     │                 ▼                                            │     │
│     │               RELEASE MANAGEMENT                             │     │
│     │                 │                                            │     │
│     │                 └── Deploy to production                     │     │
│     │                                                              │     │
│     └──────────────────────────────────────────────────────────────┘     │
│                                                                          │
│   Continuous feedback:                                                   │
│   • Incident metrics feed CONTINUAL IMPROVEMENT                         │
│   • Known Errors feed KNOWLEDGE MANAGEMENT                              │
│   • SLA breaches feed SERVICE LEVEL MANAGEMENT                          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Where Technology Incident and Production Issue Differ in ITIL Flow

| ITIL Stage | Technology Incident | Production Issue (Defect) |
|---|---|---|
| **Incident Management** | Restore service (restart, failover, rollback) | Apply workaround (disable feature, manual override) |
| **Problem Management** | Investigate why infra failed (capacity? config? vendor?) | Investigate code bug (logic error? data issue? regression?) |
| **Change Management** | Infrastructure change (resize, add redundancy, update config) | Code change (bug fix, logic correction, data migration script) |
| **Release Management** | Infrastructure deployment (Terraform, config push) | Application deployment (CI/CD pipeline, hotfix release) |

---

## 6. Common Triage Mistakes

| Mistake | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Treating a defect as an outage** | System returns errors for one feature, triage assumes full outage | Check: are other features working? Is the system accessible? |
| **Treating an outage as a defect** | Service is slow but not completely down, triage logs as a bug | Check: are response times acceptable? Are users able to complete transactions? |
| **Under-classifying severity** | Fear of escalation, "it's probably not that bad" | Use the decision tree objectively. When in doubt, escalate — it's easier to downgrade than to explain why you didn't escalate |
| **Over-classifying severity** | Business pressure, "everything is critical" | Require evidence: how many users affected? What business function is impacted? |
| **Debugging during SEV 1** | Engineer instinct to understand before acting | For Technology Incidents: restore first. You can investigate after service is back |
| **Rushing a code fix without testing** | Pressure to resolve quickly | For Production Issues: a bad fix creates a second incident. Test properly. |
| **Missing silent data corruption** | No alerts fire, system looks healthy | Invest in business metric monitoring and reconciliation checks |
| **Ignoring "it fixed itself"** | Issue resolved before anyone investigated | Self-healing issues often recur. Log it, investigate when possible. |

---

## 7. Triage Checklist (Quick Reference)

For L1 Support / On-call to use when an incident is reported:

```
INCIDENT TRIAGE CHECKLIST
─────────────────────────

□ 1. CONFIRM: Is this a real incident? (not a feature request, user error, or known issue)

□ 2. CLASSIFY:
     □ Can users access the system?          → NO  = Technology Incident
     □ Is the system producing correct results? → NO  = Production Issue (Defect)

□ 3. SEVERITY:
     □ Data breach / security event?         → SEV 1
     □ Financial data incorrect?             → SEV 1
     □ Full outage / all users affected?     → SEV 1
     □ Major degradation + business hours?   → SEV 2
     □ Partial impact / few users?           → SEV 3
     □ Cosmetic / no user impact?            → SEV 4

□ 4. IMMEDIATE ACTIONS:
     □ Technology Incident → attempt restore (restart/rollback/failover)
     □ Production Issue    → assess blast radius, stop writes if data corrupting
     □ Open incident ticket with: type, severity, affected system, description

□ 5. ASSIGN & ESCALATE:
     □ SEV 1/2 → assign Incident Commander, notify management
     □ SEV 3/4 → assign engineer, notify team channel

□ 6. COMMUNICATE:
     □ Post initial status in #incidents channel
     □ Notify affected business units (SEV 1/2)
     □ Set next update time
```

---

## 8. Glossary

| Term | Definition |
|------|-----------|
| **Incident** | Unplanned interruption or reduction in quality of a live service (ITIL 4) |
| **Technology Incident** | Incident where the service is down, unreachable, or degraded — an availability problem |
| **Production Issue / Defect** | Incident where the service is running but producing incorrect results — a correctness problem |
| **Problem** | The underlying root cause of one or more incidents (ITIL 4) |
| **Known Error** | A problem with a documented root cause and workaround (ITIL 4) |
| **Workaround** | A temporary solution that reduces or eliminates the impact of an incident without resolving the root cause |
| **RCA** | Root Cause Analysis — structured investigation to identify why an incident occurred |
| **MTTR** | Mean Time To Restore — average time from incident detection to service restoration |
| **MTTD** | Mean Time To Detect — average time from incident occurrence to detection |
| **IC** | Incident Commander — person coordinating the incident response |
| **SLA** | Service Level Agreement — agreed service availability and performance targets |
| **SLI** | Service Level Indicator — the metric used to measure service level |
| **Blast Radius** | The scope of impact — how many users, records, transactions, or systems are affected |
