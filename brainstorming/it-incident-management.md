# IT Incident Management — Brainstorming

> **Context**: A life insurance company in Vietnam. Small-to-mid IT team managing core insurance systems (policy admin, claims, billing, agency, digital channels) likely running on AWS in ap-southeast-1.
>
> **Existing work**: A process flowchart already exists at `solutions/incident-managment/lightweight.md` covering detection → triage → containment/fix → RCA → close. This brainstorming goes broader and deeper.

---

## 1. Topic Decomposition

Using **functional decomposition** crossed with an **organizational lens** (people, process, technology, governance):

| # | Sub-Area | Core Question |
|---|----------|---------------|
| A | Detection & Monitoring | How do we know something is wrong — before users tell us? |
| B | Triage & Classification | How do we quickly decide what matters and who owns it? |
| C | Response & Resolution | How do we contain damage and restore service fast? |
| D | Communication | How do we keep the right people informed without creating noise? |
| E | Post-Incident Learning | How do we turn incidents into lasting improvements? |
| F | Tooling & Automation | What technology supports the process? Build vs buy? |
| G | People & Organization | Who is on call? How do we avoid burnout? How do we train? |
| H | Governance & Compliance | What does the regulator expect? What SLAs do we owe? |

**Leverage point**: Sub-areas A (detection) and G (people) are the highest-leverage. Good detection reduces MTTR dramatically. Good people practices prevent attrition of the humans who actually resolve incidents.

---

## 2. Ideas Per Sub-Area

### A. Detection & Monitoring

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| A1 | **Layered alerting pyramid** — Synthetic checks (outside-in) → APM (application) → Infrastructure metrics → Log-based anomalies | High | Standard best practice. Catches issues at different layers. |
| A2 | **Business-metric monitors** — Alert on unusual patterns in policy issuance count, premium collection volume, claims processing rate, not just CPU/memory | Medium | Requires understanding of "normal" business patterns. More valuable than infra metrics for a life insurer. |
| A3 | **Canary transactions** — Synthetic policy quote, premium payment, or claim submission running every N minutes against production | Medium | Catches end-to-end breakage that component monitors miss. Must be carefully isolated from real data. |
| A4 | **Dead man's switch / heartbeat monitoring** — If a batch job (e.g., nightly premium allocation, regulatory report generation) doesn't phone home by expected time, alert | High | Critical for insurance — many processes are batch-based. Missed batch = regulatory/financial impact. |
| A5 | **Anomaly detection on logs** — ML-based log pattern detection (CloudWatch Anomaly Detection, or simple statistical baselines) | Low-Med | Nice in theory, noisy in practice. Start with simple threshold alerts first. |
| A6 | **User-facing error rate as primary SLI** — Instead of infrastructure metrics, make HTTP 5xx rate and latency P99 the primary indicators | High | Aligns monitoring with user experience. Simple to implement. |

### B. Triage & Classification

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| B1 | **Insurance-aware severity matrix** — SEV levels tied to business impact, not technical impact. E.g., "claims payment system down" = SEV1 regardless of technical simplicity | High | Existing flowchart has SEV1-4. Enrich with insurance-specific criteria. |
| B2 | **Decision tree for first responder** — Runbook-style: "Is core policy system affected? → Is it during premium collection window? → SEV1" | High | Reduces triage time. Empowers junior staff. |
| B3 | **Auto-classification from alert source** — Alerts from specific systems automatically tagged with severity and owning team | Medium | Reduces manual triage. Requires good alert taxonomy. |
| B4 | **Regulatory impact flag** — Every incident triage includes explicit check: "Does this affect regulatory reporting? Data privacy? Financial transactions?" | High | Critical for insurance. A data breach has different handling than a UI bug. MoF reporting obligations kick in for certain incident types. |
| B5 | **Customer-impact estimation** — Quick formula: affected system × active users at time of day × duration estimate = impact score | Medium | Helps prioritize. "50 agents can't submit applications during peak hours" vs "3 users see a styling bug" |

### C. Response & Resolution

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| C1 | **Pre-built playbooks per system** — Runbooks for the top 10 failure modes of each critical system (policy admin, claims, billing, digital channels) | High | Highest-ROI investment. Most incidents are variations of known failures. |
| C2 | **"Rollback first, investigate later"** culture — Default action for any deployment-related incident is immediate rollback | High | Requires good deployment practices (blue/green, immutable artifacts). Dramatically reduces MTTR. |
| C3 | **Break-glass access procedures** — Pre-approved emergency access to production for incident commanders, with audit trail | Medium | Balances speed (no waiting for approvals during SEV1) with security (audit log, auto-revoke). |
| C4 | **Data remediation playbook** — Step-by-step process for when an incident corrupts financial data (premium allocations, policy values, claim payments) | High | Insurance-specific. Financial data corruption can have regulatory consequences. The existing flowchart covers this path. |
| C5 | **Circuit breaker + graceful degradation patterns** — If claims system is down, policy servicing should still work. Design for partial availability. | Medium | Requires loose coupling between systems. May need architectural changes. |
| C6 | **War room automation** — Script that creates a Slack/Teams channel, adds relevant people, posts initial context, starts a timeline doc | Medium | Reduces coordination overhead during SEV1/2. |
| C7 | **Pair debugging for SEV1** — Two engineers on the problem simultaneously, one driving, one reviewing/researching | High | Simple, effective, reduces tunnel vision. |

### D. Communication

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| D1 | **Tiered notification matrix** — SEV1: CEO, CTO, business heads, regulators (if applicable). SEV2: IT management + affected business units. SEV3-4: IT team only | High | Must be pre-agreed with business. No improvising during an incident. |
| D2 | **Status page (internal)** — Single URL showing current system health. Business users check this before calling IT. | Medium | Reduces "is the system down?" calls during incidents. Can be as simple as a static page updated manually. |
| D3 | **Template-based updates** — Pre-written templates: "We are aware of issue with [system]. Impact: [X]. ETA: [Y]. Next update: [Z]." | High | Removes cognitive load of writing updates during crisis. Ensures consistent, professional communication. |
| D4 | **Regulatory notification checklist** — For incidents involving data breach, system outages affecting policyholder access, or financial transaction errors: specific notification requirements to MoF/ISA | High | Vietnam regulatory context — certain incidents trigger mandatory reporting. Must be codified. |
| D5 | **Agent/distribution channel notification** — Insurance agents in the field need to know if quoting/application systems are down, with workarounds | Medium | Agents are the front line. If they can't sell, revenue stops. |
| D6 | **Dedicated incident communication role** — During SEV1, one person handles all comms so engineers can focus on fixing | High | Prevents engineers from being pulled into status update meetings. |

### E. Post-Incident Learning

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| E1 | **Blameless post-mortems** — Structured format: timeline, root cause, contributing factors, action items with owners and deadlines | High | Already in the existing flowchart. The key is actually doing it consistently. |
| E2 | **Action item tracking with teeth** — RCA action items go into sprint backlog, not a separate tracker that gets ignored | High | Biggest failure mode of post-incident learning: action items rot in a spreadsheet. |
| E3 | **Incident pattern analysis (quarterly)** — Monthly/quarterly review: What categories recur? Which systems are most fragile? Where are we spending the most incident-hours? | Medium | Shifts from reactive to proactive. Requires consistent categorization (see B3). |
| E4 | **"Fix the detection" as mandatory RCA action** — Every RCA must answer: "How could we have detected this sooner or automatically?" and produce a monitoring improvement | High | Forces continuous improvement of detection. |
| E5 | **Incident metrics dashboard** — MTTD, MTTR, incident count by severity, by system, trend over time | Medium | Enables management visibility and improvement tracking. |
| E6 | **Game day / fire drills** — Periodically simulate an incident to test the process, runbooks, and communication chain | Medium | Reveals gaps that real incidents find painfully. Start with tabletop exercises before injecting real failures. |
| E7 | **Cross-team RCA sharing** — Anonymized incident learnings shared across teams. "Here's what the claims team learned from their outage that applies to billing too." | Medium | Breaks silos. Common in mature orgs but rare in practice. |

### F. Tooling & Automation

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| F1 | **Start minimal: ChatOps + ticketing** — Slack/Teams for coordination, Jira/ServiceNow for tracking. No over-tooling. | High | Avoid tooling fetishism. Process discipline matters more than tool sophistication for small teams. |
| F2 | **PagerDuty / Opsgenie for on-call management** — Scheduling, escalation, phone/SMS alerts that can't be missed | Medium | Worth it once you have 24/7 on-call. Overkill for business-hours-only support. |
| F3 | **CloudWatch + SNS as alerting backbone** — Native AWS, no extra cost for basic metrics, integrates with everything | High | Good starting point for AWS workloads. Add Grafana later for visualization. |
| F4 | **Runbook automation** — AWS Systems Manager Automation or simple scripts triggered from Slack for common remediation actions | Medium | "Restart the claims service" shouldn't require SSH access and tribal knowledge. |
| F5 | **Centralized logging (OpenSearch / CloudWatch Logs Insights)** — All systems log to one place with structured format | High | Non-negotiable for effective incident investigation. |
| F6 | **Incident timeline tool** — Auto-capture events (deploys, alerts, actions taken) into a timeline during incidents | Low-Med | Nice for post-mortems. Can be as simple as a shared Google Doc during the incident. |
| F7 | **AIOps — intelligent alert correlation** — Tools that correlate multiple alerts into a single incident automatically | Low | Premature for small teams. Adds complexity without proportional value until you have alert volume problems. |

### G. People & Organization

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| G1 | **"You build it, you run it" ownership** — Teams that develop a system also operate it and respond to its incidents | High | Strongest incentive to build reliable systems. Requires team maturity. |
| G2 | **On-call rotation with fair compensation** — Clear rotation schedule, on-call allowance, compensatory time off after incidents | High | Without fair compensation, on-call becomes a retention problem. Vietnam labor law considerations apply. |
| G3 | **Incident Commander role** — Trained individuals who coordinate response, not necessarily the deepest technical expert | Medium | Separates coordination from debugging. Needs explicit training. |
| G4 | **Cross-training and knowledge sharing** — No single point of failure in people. At least 2 people can handle each critical system. | High | Bus factor > 1 for every critical system. Document operational knowledge in runbooks. |
| G5 | **Incident response drills for new hires** — Part of onboarding: walk through a past incident, role-play the response | Medium | Accelerates new hire readiness. Low cost. |
| G6 | **Burnout monitoring** — Track on-call load, incident frequency per person, time-to-acknowledge at 3 AM. Redistribute if uneven. | Medium | Sustainable operations require this. Easy to neglect until someone quits. |
| G7 | **External escalation contacts** — Pre-arranged contacts at key vendors (core system vendor, AWS support, network provider) for critical incidents | High | During SEV1 is not the time to figure out how to reach AWS Enterprise Support. |

### H. Governance & Compliance

| # | Idea | Feasibility | Notes |
|---|------|-------------|-------|
| H1 | **SLA framework tied to business functions** — Policy issuance: 99.5% uptime during business hours. Digital channels: 99.9%. Batch processing: completed by 06:00 daily. | High | SLAs should reflect business priority, not uniform "five nines" aspirations. |
| H2 | **Regulatory incident reporting procedure** — Documented process for when and how to report to MoF/ISA. Trigger criteria, templates, timelines, responsible person. | High | Vietnamese insurance regulation may require reporting of significant system outages, data breaches, or events affecting policyholder interests. Verify specific requirements. |
| H3 | **Incident classification for regulatory reporting** — Not all incidents are reportable. Define clear criteria: data breach involving PII, financial transaction errors above threshold, extended outage of customer-facing systems. | High | Prevents both under-reporting (regulatory risk) and over-reporting (crying wolf). |
| H4 | **Annual incident management review** — Formal review of the incident management process itself: Is it working? What metrics improved? What needs to change? | Medium | Continuous improvement of the process, not just the systems. |
| H5 | **Audit trail for all incident actions** — Every action during an incident is logged: who did what, when, why. For compliance and learning. | Medium | Required for regulated environments. Also invaluable for post-mortems. |
| H6 | **Data privacy incident handling** — Separate sub-process for incidents involving personal data. Vietnam's data privacy regulations (PDPD) and insurance data protection requirements. | High | Personal data of policyholders, insureds, and beneficiaries is highly sensitive. Breach handling has specific legal requirements. |

---

## 3. Top 5 Candidates — Trade-off Analysis

### Candidate 1: Business-Metric Monitoring + Canary Transactions (A2 + A3)

**What**: Monitor insurance business KPIs (policy issuance rate, premium collection volume, claims processing throughput) alongside synthetic transactions that simulate real user journeys.

| Criterion | Assessment |
|-----------|------------|
| **MTTR impact** | High — catches issues that infrastructure monitoring misses entirely (e.g., system is "up" but producing wrong calculations) |
| **Implementation cost** | Medium — requires understanding of normal business patterns and careful canary design |
| **Maintenance burden** | Medium — canaries need updating when business logic changes |
| **Reversibility** | Easily reversible (two-way door) |

**Trade-off**: You're investing in monitoring that catches fewer but higher-impact incidents (business logic failures) vs broad infrastructure monitoring that catches more but often lower-impact issues. **You give up**: engineering time that could go to feature work. **You gain**: the ability to detect "silent failures" — the system works but produces wrong results.

**Risk**: Canary transactions in production can pollute real data if not isolated properly. For a life insurer, a synthetic policy or claim created accidentally in the production system could cause regulatory and financial issues. **Response**: Mitigate — use dedicated test markers, separate canary data paths, automatic cleanup.

---

### Candidate 2: Pre-Built Runbooks for Top 10 Failure Modes (C1)

**What**: Document step-by-step remediation playbooks for the most common failure scenarios of each critical system.

| Criterion | Assessment |
|-----------|------------|
| **MTTR impact** | Very high — transforms incident response from "figure it out" to "follow the steps" |
| **Implementation cost** | Low — requires time, not money. Can be built incrementally from actual incidents. |
| **Maintenance burden** | Medium — runbooks go stale if not updated. Assign owners. |
| **Reversibility** | N/A — documentation, zero risk |

**Trade-off**: You're investing in documentation (boring, invisible work) over tooling (visible, exciting). **You give up**: the feeling of progress that comes from building new tools. **You gain**: dramatically faster response by junior staff and on-call engineers who aren't the system's original developer.

**Risk**: Runbooks become stale and misleading. Following an outdated runbook during a SEV1 could make things worse. **Response**: Mitigate — review runbooks quarterly, test during fire drills (E6), mark runbooks with "last verified" dates.

---

### Candidate 3: Blameless Post-Mortems with Sprint-Tracked Action Items (E1 + E2)

**What**: Mandatory blameless RCA for every SEV1/SEV2, with action items injected directly into team sprint backlogs (not a separate RCA tracker).

| Criterion | Assessment |
|-----------|------------|
| **MTTR impact** | Indirect but compounding — each RCA prevents future incidents or reduces their severity |
| **Implementation cost** | Low — process change, not tool change |
| **Maintenance burden** | Low — becomes a habit |
| **Reversibility** | Easily reversible |

**Trade-off**: You're investing in learning over speed. Post-mortems take 2-4 hours per incident. Action items consume sprint capacity. **You give up**: sprint velocity in the short term. **You gain**: fewer and shorter incidents over time. The compound effect is massive.

**Risk**: "Blameless" culture is hard to establish in hierarchical organizations (common in Vietnamese corporate culture). If people fear blame, they hide information, and post-mortems become theater. **Response**: Mitigate — leadership must visibly model blameless behavior. Start with facilitator-led sessions. Focus language on systems and processes, not individuals.

---

### Candidate 4: Insurance-Aware Severity Matrix + Regulatory Incident Reporting (B1 + H2 + H3)

**What**: A severity classification system that reflects insurance business impact (not just technical metrics), integrated with a clear regulatory reporting procedure.

| Criterion | Assessment |
|-----------|------------|
| **MTTR impact** | Medium — faster correct prioritization means resources go to the right problem |
| **Implementation cost** | Low — one workshop with business stakeholders to define criteria |
| **Maintenance burden** | Low — update annually or when regulations change |
| **Reversibility** | Easily reversible |

**Trade-off**: You're investing in governance upfront (slows down initial setup) for correct prioritization during incidents (speeds up response when it matters). **You give up**: simplicity — a generic SEV1-4 scale is easier to explain. **You gain**: alignment between IT and business on what matters, and regulatory compliance.

**Risk**: Over-classification — if everything is SEV1, nothing is. Business stakeholders tend to escalate everything. **Response**: Mitigate — strict criteria with examples. Quarterly review of severity assignments to calibrate.

---

### Candidate 5: On-Call Rotation with Fair Compensation + Cross-Training (G2 + G4)

**What**: Structured on-call schedule with proper compensation, ensuring at least 2 people can handle each critical system.

| Criterion | Assessment |
|-----------|------------|
| **MTTR impact** | High — someone is always available and capable of responding |
| **Implementation cost** | Medium — on-call compensation costs money; cross-training takes time |
| **Maintenance burden** | Ongoing — rotation management, training updates |
| **Reversibility** | Medium — harder to take away compensation once granted |

**Trade-off**: You're investing in people sustainability over system investment. **You give up**: budget that could go to tooling or infrastructure. **You gain**: reliable human response capability and reduced single-points-of-failure.

**Risk**: On-call without adequate tooling/runbooks leads to burnout faster. Waking up at 3 AM with no runbook and no observability is demoralizing. **Response**: Mitigate — implement this alongside Candidates 1 and 2. Tooling and runbooks reduce on-call burden.

---

## 4. Creative Challenges & Non-Obvious Angles

### Assumption Audit

1. **Assumption: The team needs a formal incident management process.**
   — What if: The team is so small (< 5 engineers) that formal process adds overhead without value? For very small teams, "everyone knows everything" and "just call each other" might actually work. The trigger to formalize is when the team grows past the point where informal coordination breaks down (~8-10 people, or when on-call rotation becomes necessary).

2. **Assumption: Incidents are primarily technical.**
   — What if: The most damaging "incidents" for a life insurer aren't system outages but data quality issues — wrong premium calculations, incorrect policy values, miscalculated claims — that go undetected for weeks? These silent failures may not trigger any alert but have massive financial and regulatory impact. The incident management process should explicitly cover "delayed discovery" scenarios.

3. **Assumption: 24/7 availability is necessary.**
   — What if: Most of the company's business happens during Vietnamese business hours (8 AM - 6 PM, Mon-Sat)? If digital channels have low nighttime usage, business-hours-only support with automated failover for infrastructure failures might be sufficient and far cheaper than 24/7 on-call. Analyze actual traffic patterns before committing to round-the-clock staffing.

### Cross-Domain Analogies

- **Insurance claims processing ↔ Incident management**: Both are triage → investigate → resolve workflows with severity classification and SLA targets. The claims team already thinks in these patterns. Could they share frameworks, tools, or even review each other's processes?

- **Medical triage ↔ Incident triage**: Emergency medicine's triage system (immediate/urgent/delayed/expectant) is battle-tested for high-stakes, time-pressured prioritization. The principle "treat the most survivable critical patients first" translates to "fix the incident where quick action has the highest impact."

- **Aviation incident reporting ↔ Blameless post-mortems**: Aviation's mandatory incident reporting with legal protection for reporters is the gold standard for learning cultures. The key insight: you must make it *safer to report than to hide*.

### Unasked Questions

1. **What is the actual cost of downtime?** Without this number, all severity matrices and SLA decisions are arbitrary. Calculate: lost premium collection per hour, cost of delayed claims processing, regulatory fine exposure, reputational damage estimate. This number justifies (or doesn't justify) every investment in incident management.

2. **Who owns incident management?** Is it IT operations? DevOps? A dedicated SRE function? The application development team? In many insurance companies, this falls between the cracks — everyone assumes someone else owns it. Explicit ownership is prerequisite to everything else.

3. **What about vendor/partner incidents?** Core insurance systems often involve third-party vendors (policy admin system, payment gateway, reinsurance interfaces). When the vendor's system causes an incident, the process must handle: vendor escalation, SLA enforcement, interim workarounds, and communication to stakeholders that "it's not our system" without absolving responsibility to end users.

4. **Is the existing solutions/incident-managment flowchart being used?** There's already a detailed process flow. Before brainstorming new ideas, the first question should be: Is the existing process followed? If not, why? Adding more process on top of unused process is waste.

### The Simplest Version

If the team had to implement incident management tomorrow with zero budget and minimal process overhead:

1. **A shared Slack/Teams channel** called `#incidents` — all incidents discussed here, nowhere else
2. **A severity definition** on a single page taped to every monitor: SEV1 = customers can't transact, SEV2 = degraded, SEV3 = minor, SEV4 = cosmetic
3. **One runbook per critical system** — even if it's just "restart steps + who to call"
4. **A post-mortem template** in Google Docs — filled out within 48 hours for SEV1/2
5. **CloudWatch alarms** on the 3 most critical metrics per system, sending to the #incidents channel

This gets you 80% of the value. Everything else is optimization.

### The Elephant in the Room

For many mid-size insurance IT teams in Vietnam:

- **The real incident management problem is not process — it's people.** Key-person dependencies, underpaid on-call staff, no knowledge documentation, and tribal knowledge held by 1-2 senior engineers who could leave at any time. No amount of process or tooling fixes this if the organizational investment in people isn't there.

- **Legacy core systems are the root cause of most incidents.** If the policy admin system is a 15-year-old monolith with no automated testing, no CI/CD, and manual deployments, incident management is treating symptoms. The real conversation is about modernization — but that's a multi-year, high-risk investment that nobody wants to start.

---

## 5. Recommended Starting Sequence

For a team starting from low maturity, implement in this order:

```
Phase 1 (Week 1-2): Foundation
├── Define severity matrix with business stakeholders (B1)
├── Set up #incidents channel and communication templates (D3, D6)
├── Identify on-call ownership per system (G1, G2)
└── Basic CloudWatch alerting on critical systems (F3)

Phase 2 (Month 1-2): Core Process
├── Write runbooks for top 5 failure modes (C1)
├── Implement blameless post-mortem process (E1)
├── Track action items in sprint backlogs (E2)
└── Establish regulatory incident reporting procedure (H2)

Phase 3 (Month 3-6): Maturation
├── Add business-metric monitoring (A2)
├── Build canary transactions for critical flows (A3)
├── Quarterly incident pattern analysis (E3)
├── Game day / fire drill exercises (E6)
└── Cross-training program (G4)

Phase 4 (Month 6+): Optimization
├── Runbook automation (F4)
├── War room automation (C6)
├── Incident metrics dashboard (E5)
└── Annual process review (H4)
```

---

---

## 6. Slide-Ready Incident Management Flow (ITIL-Lean)

> **Goal**: A 1-2 slide presentation showing who does what at each stage. ITIL-aligned but lean. Includes classification of Technology Incident vs Production Issue.

### Slide 1 — Incident Classification & Swimlane Flow

#### Incident Classification

| Category | Definition | Examples | Trigger |
|----------|-----------|----------|---------|
| **Technology Incident** | An unplanned interruption or degradation of an IT service. The system is **down, unreachable, or performing below acceptable thresholds**. Focus: **restore service ASAP**. | Server/network outage, database crash, SSL certificate expiry, infrastructure failure, DDoS, cloud service disruption | Monitoring alert, user unable to access system, health check failure |
| **Production Issue (Defect)** | The system is **running but producing incorrect results** — a bug or defect in production. Data integrity or business logic is wrong. Focus: **fix the defect, remediate bad data**. | Wrong premium calculation, incorrect policy status, failed batch processing with wrong output, UI displaying wrong data, integration sending malformed messages | User report, QA finding, data reconciliation mismatch, business metric anomaly |

**Key Difference**: Technology Incident = **service availability** problem. Production Issue = **correctness** problem. Both follow the same flow but diverge at the Fix stage.

#### Swimlane Flow — Who Does What

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  STAGE ▸   ① DETECT        ② TRIAGE         ③ RESPOND & FIX    ④ VERIFY        ⑤ CLOSE    │
│            (< 5 min)       (< 15 min)       (SEV-dependent)    (< 30 min)      (< 48 hrs) │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  ANYONE     Report issue ─────────────────────────────────────────────────────────────────▶ │
│  (User/     via channel                                                                     │
│   Alert)    or alert fires                                                                  │
│                                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  L1 SUPPORT  ──────────▶  Confirm real?     ──────────────────────────────────────────────▶ │
│  (On-call /               Classify type:                                                    │
│   Help Desk)              Tech Incident or                                                  │
│                           Prod Issue?                                                       │
│                           Assign severity                                                   │
│                           (SEV 1-4)                                                         │
│                                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  INCIDENT    ◄──────────  Assigned as IC  ─▶ Coordinate        Confirm         Lead RCA     │
│  COMMANDER                (SEV1/2 only)      response team     service         meeting      │
│  (IC)                                        Manage comms      restored        Publish      │
│                                              Make decisions     or fix          report       │
│                                              (rollback? war     deployed        Track        │
│                                               room? escalate?)                 actions      │
│                                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  TECH TEAM   ◄──────────────────────────────▶ TECH INCIDENT:   Monitor for                  │
│  (Dev /                                       → Rollback /      regression                  │
│   Infra /                                       restart /       (15 min                     │
│   DBA)                                          failover        watch)                      │
│                                               PROD ISSUE:                                   │
│                                               → Root cause                                  │
│                                               → Develop fix                                 │
│                                               → Test & deploy                               │
│                                               → Remediate data                              │
│                                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  QA          ◄──────────────────────────────────────────────▶  Validate fix    Verify no     │
│                                                                in staging      regression    │
│                                                                (Prod Issue                   │
│                                                                 only)                       │
│                                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  MANAGEMENT  ◄─ Notified  Approve           Receive status     Approve         Review RCA   │
│  (IT Mgr /   (SEV1/2)    escalation         updates            service         Sign off     │
│   CTO)                   if needed          (SEV1: 30min,      restoration     action items │
│                                              SEV2: 1hr)                                     │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Slide 2 — Severity Matrix & RACI

#### Severity Levels (ITIL-aligned)

| Severity | Name | Definition | Response Time | Resolution Target | Who's Involved |
|----------|------|-----------|---------------|-------------------|----------------|
| **SEV 1** | Critical | Full service outage or data breach affecting customers | Immediate | < 1 hour | All hands: IC + Tech + Mgmt + Comms |
| **SEV 2** | Major | Significant degradation, key function unavailable | < 15 min | < 4 hours | IC + On-call team + Mgmt notified |
| **SEV 3** | Minor | Partial impact, workaround available | < 1 hour | < 1 business day | On-call / assigned team |
| **SEV 4** | Low | Cosmetic, minimal impact | Next business day | < 5 business days | Assigned developer |

#### RACI per Stage

| Stage | L1 Support | Incident Commander | Tech Team | QA | Management |
|-------|-----------|-------------------|-----------|-----|------------|
| ① Detect | **R** | I | I | - | - |
| ② Triage | **R/A** | **A** (SEV1/2) | **C** | - | **I** (SEV1/2) |
| ③ Respond & Fix | I | **A** | **R** | **R** (Prod Issue) | **I** |
| ④ Verify | I | **A** | **R** | **R** | **I** |
| ⑤ Close (RCA) | - | **R** | **C** | **C** | **A** |

> R = Responsible (does the work) · A = Accountable (owns the outcome) · C = Consulted · I = Informed

#### Quick Reference — Technology Incident vs Production Issue

```
Technology Incident (Service Down)     Production Issue (Defect)
──────────────────────────────         ──────────────────────────
Priority: RESTORE SERVICE              Priority: FIX CORRECTNESS

Actions:                                Actions:
• Failover / restart / rollback         • Reproduce & root cause
• Enable maintenance mode               • Develop & test fix
• Apply infrastructure fix              • Deploy via normal CI/CD
• Monitor for stability                 • Remediate corrupted data

RCA trigger: Always for SEV1/2          RCA trigger: Always for SEV1/2
                                        + if financial/data impact

Typical owner: Infra / DevOps          Typical owner: Dev team
```

### Design Notes for PPT

- **Slide 1**: Use the swimlane table as a visual flow (horizontal lanes per role, left-to-right progression through stages). Color-code Tech Incident path (red) vs Production Issue path (amber). Place the classification table as a callout box.
- **Slide 2**: Severity matrix as a colored table (red → green gradient). RACI as a compact grid. Quick reference comparison as two side-by-side boxes.
- **Font**: Keep to 14pt minimum for readability on screen/projector.
- **Colors**: SEV1=Red, SEV2=Orange, SEV3=Blue, SEV4=Green (standard convention).

---

*Updated on 2026-03-11. Added slide-ready swimlane flow with ITIL-lean stages, role assignments (RACI), and Technology Incident vs Production Issue classification.*
