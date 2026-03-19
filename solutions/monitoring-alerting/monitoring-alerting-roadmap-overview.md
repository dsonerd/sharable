# Monitoring & Alerting Roadmap — Overview

> **Version**: 2.0
> **Date**: 2026-03-20
> **Author**: IT Operations
> **Status**: Revised — incorporating CIO review feedback
> **Audience**: CIO, Board, Department Heads, IT Management
> **Companion document**: `monitoring-alerting-roadmap-detail.md` (technical reference)

---

## 1. Executive Summary

TCLife operates a fully AWS-hosted life insurance platform serving policyholders, agents, and internal operations across Unit-Linked, Critical Illness, Health Insurance, and Medical Reimbursement product lines. The core insurance system (EbaoTech Insuremo) is vendor-managed.

**The problem**: Today, most incidents are discovered by users before IT detects them. Business-critical processes — policy issuance, claims payments, premium collection, NAV calculations — have no automated monitoring. Batch jobs that feed the general ledger, regulators, and printing partners are tracked manually. There is no after-hours alert escalation.

**The solution**: A four-phase monitoring and alerting program that builds detection and visibility across infrastructure, applications, business processes, and security — delivered incrementally over 12 months by our existing 7-person team.

**Target state**: Every P1/P2 incident is detected by monitoring before users report it. Every business-critical batch job is tracked for timeliness and correctness. Management has a single dashboard showing system health, SLA compliance, and business processing status.

---

## 2. Our Team

The monitoring program will be delivered by the IT Operations department's existing staff. No new hires are assumed in Year 1, though the staffing plan below identifies where external support may be needed.

| Role | Headcount | Monitoring Responsibilities |
|------|-----------|----------------------------|
| **Application Operations (App Ops)** | 3 | Day-to-day monitoring operations, alert triage and response, on-call rotation (primary), dashboard maintenance, runbook execution, batch job oversight |
| **Service Quality** | 1 | KPI definition and tracking, SLA reporting, alert tuning and quality review, compliance dashboard ownership, process improvement |
| **DevOps / Cloud Engineers** | 3 | Monitoring infrastructure (Prometheus, Grafana, OpenSearch), alert rule development, instrumentation standards, Insuremo health prober, batch job monitor service, IaC for monitoring |
| | **7 total** | |

### On-Call Model

With 3 App Ops + 3 DevOps = 6 engineers eligible for on-call, the rotation supports:
- **Primary on-call**: 1 person per week (6-week rotation cycle)
- **Secondary escalation**: Team lead or senior DevOps engineer
- **Sustainability**: Each person is on-call approximately once every 6 weeks — sustainable long-term

### Staffing Allocation Per Phase

| Phase | App Ops (3 FTE) | Service Quality (1 FTE) | DevOps (3 FTE) | External Support |
|-------|-----------------|------------------------|----------------|------------------|
| **Phase 1** (Mo 1-3) | 40% — on-call setup, runbooks, log verification | 20% — KPI framework, SLA definition | 60% — infrastructure build, alerting pipeline, tooling | Recommended: AWS training (Prometheus, Grafana, OpenSearch) |
| **Phase 2** (Mo 4-6) | 30% — alert triage, dashboard adoption, operations | 30% — alert tuning, false positive review | 50% — app instrumentation, Insuremo prober, security integration | Optional: AWS Professional Services for OpenSearch tuning |
| **Phase 3** (Mo 7-9) | 40% — batch monitoring ops, business dashboards, reconciliation | 40% — business KPI validation, compliance dashboard (basic) | 40% — batch job monitor service, business metric instrumentation | None expected |
| **Phase 4** (Mo 10-12) | 20% — steady-state operations, process review | 40% — compliance dashboard, SLA automation, Year 2 planning | 30% — capacity planning, anomaly detection, IaC migration | Optional: External audit of monitoring coverage |

> **Note**: Percentages represent estimated time allocation alongside regular operational duties. During Phase 1, DevOps engineers will need protected time — daily operations must be covered by App Ops to avoid Phase 1 stalling.

---

## 3. What We Monitor

TCLife's monitoring covers eight domains. Each addresses a distinct operational risk.

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                    MONITORING DOMAINS                           │
  │                                                                 │
  │  1. INFRASTRUCTURE    Servers, containers, databases, network   │
  │  2. APPLICATION       Portal performance, API health, errors    │
  │  3. BUSINESS PROCESS  Policy, claims, premium, NAV, surrender   │
  │  4. VENDOR / INSUREMO Core system health, API SLA, data fresh.  │
  │  5. BATCH JOBS        GL, printing, datalake, reinsurance,      │
  │                       commission, regulatory, NAV, reconcil.    │
  │  6. SECURITY          Threat detection, access anomalies, WAF   │
  │  7. COST              AWS spend anomalies, budget alerts        │
  │  8. USER EXPERIENCE   Real user performance (Sale + Customer    │
  │                       Portal), page load, JS errors, mobile     │
  └─────────────────────────────────────────────────────────────────┘

  Cross-cutting: DATA PROTECTION
  PII scrubbing in logs, access controls on dashboards, data sovereignty
```

### Domain Coverage by Phase

| Domain | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|:-------:|:-------:|:-------:|:-------:|
| Infrastructure | Full | Maintained | Maintained | Capacity planning |
| Application | — | Full | Maintained | Tracing evaluation |
| Business Process | — | — | Full | Anomaly detection |
| Vendor / Insuremo | — | Full | Enhanced | Maintained |
| Batch Jobs | — | — | Full | Automation |
| Security | Basic (GuardDuty) | Core (WAF, CloudTrail) | Enhanced | Advanced |
| Cost | Basic (billing alarms) | — | — | Optimization |
| User Experience (RUM) | — | Basic | Full | Maintained |

---

## 4. Metrics by Stakeholder

What each department sees — and why it matters to them.

### Operations Department (ITO)

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| System health status (all services) | Detect and respond to outages | "Customer Portal error rate spiked to 5% at 14:22" |
| Active alerts by severity | Prioritize response | "2 SEV2 alerts, 1 SEV3 — address SEV2 first" |
| On-call dashboard | Know who is responsible | "Nguyen is primary on-call this week" |
| Batch job completion matrix | Verify daily operations | "GL file delivered on time; NAV calculation pending" |
| Incident metrics (MTTD, MTTR) | Track operational performance | "P1 MTTD improved from 45 min to 4 min" |

### Sales / Distribution

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| Sale Portal availability and performance | Agent productivity | "Sale Portal P95 response time: 380ms" |
| Quote-to-proposal conversion rate | System friction detection | "Conversion dropped to 22% — investigate UX issue" |
| Policy issuance pipeline status | Revenue visibility | "127 policies issued today, within normal range" |
| Commission batch processing status | Agent compensation assurance | "Commission run completed; 412 agents processed" |

### Customer / End User

| What They See (via operations) | Why It Matters | Example |
|-------------------------------|----------------|---------|
| Customer Portal availability | Policyholder self-service | "99.92% availability this month" |
| Claims processing time | Policyholder experience | "Average registration-to-assessment: 1.8 days" |
| Policy servicing response time | Policyholder satisfaction | "Surrender request processing: within SLA" |
| Real user performance (RUM) | Actual user experience in the field | "Mobile users in Mekong Delta: 3.2s page load" |

### Finance

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| GL posting timeliness | Financial close | "GL file delivered at 07:42, before 08:00 deadline" |
| Premium collection success rate | Revenue assurance | "98.3% collection success; 1.7% failed — retry scheduled" |
| NAV calculation completion | UL fund reporting | "NAV calculated by 09:48 — within 10:00 AM deadline" |
| Bank reconciliation status | Financial accuracy | "Reconciliation complete; zero variances" |

### Management / CIO

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| Business health — single dashboard | "Is the business running?" | Green/yellow/red status for all business processes |
| SLA compliance (30-day rolling) | Risk and performance posture | "Sale Portal: 99.96% (target: 99.95%)" |
| Vendor (Insuremo) SLA tracking | Vendor accountability | "Insuremo: 99.87% availability (contract: 99.9%) — vendor notified" |
| Incident trend (monthly) | Operational maturity | "P1 incidents: 2 this month vs. 5 last month" |
| Monitoring program progress | Investment tracking | "Phase 2: 80% complete, on schedule" |

### Compliance

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| System availability evidence | Regulatory reporting | "Regulated services: 99.9%+ for Q1 2026" |
| Incident history (policyholder impact) | Audit trail | "3 incidents affected policyholders in Q1; all resolved within SLA" |
| Batch processing proof | Financial reporting integrity | "All GL, regulatory, and NAV batches completed within SLA for 90 consecutive days" |
| Data breach / security event log | Data protection compliance | "Zero data breach events in Q1" |

> **Note on regulatory citations**: Specific Vietnamese regulatory instruments referenced in this roadmap (Circular 125/2018/TT-BTC, Decree 13/2023/ND-CP, Insurance Law 2022, Circular 50/2017/TT-BTC) are **pending verification by Legal/Compliance**. Compliance requirements described here represent the team's current understanding and must be validated before being presented as authoritative.

---

## 5. Tool Landscape

TCLife's monitoring stack uses AWS managed services to minimize operational overhead.

```
                            ┌──────────────────────┐
                            │   Amazon Managed      │
                            │      Grafana          │
                            │   (Visualization)     │
                            └──┬──────┬──────┬──────┘
                               │      │      │
                  ┌────────────┘      │      └────────────┐
                  │                   │                    │
                  ▼                   ▼                    ▼
     ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
     │  Prometheus (AMP) │  │    OpenSearch     │  │   CloudWatch     │
     │                   │  │                   │  │                  │
     │  Metrics:         │  │  Logs:            │  │  AWS Services:   │
     │  - Infrastructure │  │  - App logs       │  │  - RDS, S3, SQS  │
     │  - Application    │  │  - Security events│  │  - ALB, Lambda   │
     │  - Business KPIs  │  │  - Audit trail    │  │  - Billing       │
     │  - Custom probes  │  │  - Trace data     │  │  - Cost anomaly  │
     │                   │  │                   │  │                  │
     │  Alerting rules   │  │  Log-based alerts │  │  CloudWatch      │
     │  via Alertmanager │  │                   │  │  Alarms          │
     └────────┬─────────┘  └────────┬──────────┘  └────────┬─────────┘
              │                     │                       │
              └─────────┬───────────┘                       │
                        ▼                                   │
            ┌──────────────────┐                            │
            │   PagerDuty /    │◄───────────────────────────┘
            │   OpsGenie       │
            │                  │
            │  On-call routing │
            │  Escalation      │
            │  SMS / Phone     │
            └──────────────────┘

  Additional components (phased):
  - Grafana Faro (RUM agent) — Phase 2/3
  - AWS Cost Anomaly Detection — Phase 1
  - Insuremo Health Prober (custom) — Phase 2
  - Batch Job Monitor (custom) — Phase 3
  - Status page (external communication) — Phase 2/3
```

All components are AWS managed services except the Insuremo Health Prober and Batch Job Monitor, which are lightweight services running on the existing EKS cluster.

---

## 6. Roadmap Summary

### Timeline

```
  Month:  1────2────3────4────5────6────7────8────9────10───11───12
          ├─── Phase 1 ───┤├─── Phase 2 ───┤├─── Phase 3 ───┤├── Phase 4 ──┤
          Foundation       Application &     Business Metrics  Advanced
          & Infrastructure Security          & Batch Jobs      Capabilities
```

### Phase 1: Foundation (Months 1-3)

**Goal**: Reliable infrastructure monitoring, alerting pipeline, on-call process, and team training.

| Key Deliverables | Who Delivers | Exit Criteria |
|-----------------|-------------|---------------|
| Team training (Prometheus, Grafana, OpenSearch) | All — via AWS training or partner | Team can independently create dashboards and alert rules |
| CloudWatch-to-Grafana integration (all AWS services) | DevOps | All AWS services visible in Grafana |
| Infrastructure alerting (nodes, pods, RDS, ALB) | DevOps | All P1-triggering conditions have automated alerts |
| On-call tooling (PagerDuty/OpsGenie) + rotation | App Ops + DevOps | SEV1/SEV2 alerts reach on-call phone within 30 seconds |
| Alert runbooks (100% coverage for Phase 1 alerts) | App Ops | Every alert has a documented response procedure |
| Log pipeline verification | DevOps | All apps confirmed logging to OpenSearch; gaps documented |
| Synthetic monitoring (Sale Portal, Customer Portal) | DevOps | Portal reachability tested every 60 seconds |
| AWS cost monitoring (billing alarms, Cost Anomaly Detection) | DevOps | Unexpected cost spikes generate alerts |
| PII scrubbing policy (design) | Service Quality + DevOps | Policy defined for log scrubbing before pipeline expansion |
| OpenSearch discovery (current scope, log volume) | DevOps | Log volume measured; OpenSearch cost estimate refined |

### Phase 2: Application & Security (Months 4-6)

**Goal**: Application-level observability, Insuremo independent monitoring, security baseline, RUM foundation.

| Key Deliverables | Who Delivers | Exit Criteria |
|-----------------|-------------|---------------|
| Application instrumentation (HTTP metrics, structured logging) | DevOps + App Ops | All applications expose standard metrics |
| Insuremo Health Prober (independent core system monitoring) | DevOps | Insuremo availability and latency visible; 30-day baseline |
| Security monitoring (GuardDuty, WAF, CloudTrail) | DevOps | Security events centralized and alerting |
| Log-based alerting (error patterns, auth failures) | App Ops + DevOps | 10+ log-based alert rules active |
| Real User Monitoring — foundation (Grafana Faro or equivalent) | DevOps | RUM data collected for Sale Portal and Customer Portal |
| Basic compliance dashboard (availability, incident history) | Service Quality | Availability evidence available for regulator/auditor queries |
| Alert tuning (30-day review of all Phase 1 alerts) | Service Quality | False positive rate < 20% |
| Status page evaluation and setup | App Ops | External communication channel for portal degradation |

### Phase 3: Business Metrics & Batch Monitoring (Months 7-9)

**Goal**: Insurance-specific monitoring — business process KPIs, batch job tracking, financial operations.

| Key Deliverables | Who Delivers | Exit Criteria |
|-----------------|-------------|---------------|
| Batch Job Monitor service (all batch jobs tracked) | DevOps + App Ops | Every daily batch job has automated SLA alerting |
| Commission batch monitoring | App Ops | Commission run tracked for completion, accuracy, timeliness |
| GL, printing, datalake, reinsurance batch monitoring | App Ops | All batch partners tracked |
| Business KPI dashboards (policy, claims, premium, NAV) | Service Quality + App Ops | Business KPIs visible and trended |
| Reconciliation automation (GL, premium, NAV) | DevOps + App Ops | Daily reconciliation with alerts on mismatch |
| CIO Management dashboard | Service Quality | Single-pane view of business + system health |
| RUM — full deployment | DevOps | Real user performance visible across regions and devices |
| Regulatory filing countdown panel | Service Quality | Proactive alerting as regulatory deadlines approach |

### Phase 4: Advanced Capabilities (Months 10-12)

**Goal**: Mature the practice — capacity planning, compliance reporting, automation, Year 2 planning.

| Key Deliverables | Who Delivers | Exit Criteria |
|-----------------|-------------|---------------|
| Capacity planning dashboards (trend-based forecasting) | DevOps | Quarterly capacity review uses data-driven forecasts |
| Compliance dashboard — full (audit-grade evidence pack) | Service Quality | Passes internal audit review |
| SLA reporting automation (monthly reports auto-generated) | Service Quality + DevOps | Monthly SLA report requires < 1 hour manual effort |
| Anomaly detection (statistical baseline + deviation alerting) | DevOps | 5+ anomaly detection rules active |
| Monitoring-as-Code (Terraform/CDK for all config) | DevOps | All monitoring configuration in version control |
| Runbook automation (top 5 common alerts auto-remediated) | DevOps | 3+ auto-remediation playbooks active |
| Year 2 roadmap and process review | All + CIO | Year 2 roadmap drafted based on Year 1 findings |

---

## 7. Investment

### AWS Costs (Monthly, Steady State)

| Component | Estimated Monthly Cost (USD) |
|-----------|----------------------------|
| Amazon Managed Grafana | $100-200 |
| Amazon Managed Prometheus (AMP) | $200-500 |
| Amazon OpenSearch Service | $800-2,000 |
| CloudWatch (incremental custom metrics, alarms) | $100-300 |
| PagerDuty/OpsGenie (5-10 responders) | $200-500 |
| AWS Synthetics (external canaries) | $150-300 |
| Insuremo Health Prober + Batch Job Monitor (EKS) | $100-200 |
| S3 archive storage | $50-200 |
| **AWS total** | **$1,700-4,200/month** |

### Human Costs (Monthly, Estimated)

| Component | Estimated Monthly Cost (USD) | Notes |
|-----------|----------------------------|-------|
| On-call allowances | $500-1,500 | 6-person rotation; per HR policy |
| Training (amortized over 12 months) | $300-600 | AWS training courses for 7 staff; one-time ~$3,600-7,200 |
| Time allocation (opportunity cost) | Not separately budgeted | Existing staff; time allocation per phase above |
| External support (if needed) | $0-3,000 | AWS Professional Services or partner; Phase 1-2 only |
| **Human total** | **$800-5,100/month** |

### Total Program Cost

| | Monthly (Steady State) | Annual Estimate |
|-|----------------------|----------------|
| AWS services | $1,700-4,200 | $20,400-50,400 |
| Human costs | $800-5,100 | $9,600-61,200 |
| **Total** | **$2,500-9,300** | **$30,000-111,600** |

> **Note**: The wide range reflects uncertainty in log volume (OpenSearch is the largest variable). A pre-Phase 1 discovery task will measure current log volume and refine the OpenSearch estimate.

### ROI Justification

| Value Driver | Impact |
|-------------|--------|
| Faster incident detection | Reduce MTTD from ~45 min (user-reported) to < 5 min (automated). Each hour of P1 downtime costs agent productivity and policyholder trust. |
| Batch job failure prevention | Catch GL, NAV, and regulatory batch failures before they cause downstream financial or compliance impact. |
| Vendor accountability | Independent Insuremo SLA measurement replaces reliance on vendor self-reporting. |
| Regulatory readiness | Structured availability evidence for regulator/auditor queries — reduces audit preparation from days to hours. |
| Operational efficiency | Automated alerting and dashboards reduce manual checking, overnight uncertainty, and "war room" diagnosis time. |

---

## 8. Key Risks and Dependencies

### Top Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Alert fatigue** | On-call ignores critical alerts | Aggressive 30-day tuning per alert; weekly review; mandatory runbooks |
| **Skills gap** | Team cannot build/maintain monitoring | Training as Phase 1 deliverable; optional AWS partner support |
| **Scope creep** | Trying to do everything delays core delivery | Strict phase gating; Phase 1 complete before Phase 2 starts |
| **PII in monitoring data** | Logs contain policyholder data (policy numbers, customer IDs, health data); monitoring stack becomes a PII store subject to data protection regulation | PII scrubbing policy designed in Phase 1; log pipeline applies scrubbing before ingestion; dashboard access controls enforced |
| **Vendor cooperation** | EbaoTech restricts probe access or changes APIs | Vendor monitoring agreement; document probing in contract |
| **Monitoring stack as target** | Centralized monitoring is a high-value attack target | Network access restrictions; MFA for Grafana/OpenSearch; audit log access |

### Critical Dependencies

| Dependency | Required By | Impact if Delayed |
|-----------|-------------|-------------------|
| On-call budget approval | Phase 1 start | Cannot implement after-hours alerting |
| PagerDuty/OpsGenie procurement | Phase 1, month 1 | Alert routing remains manual |
| Training budget approval | Phase 1, month 1 | Team cannot build monitoring independently |
| EbaoTech vendor agreement on probing | Phase 2 start | Core system monitoring remains vendor-dependent |
| Business KPI validation by department heads | Phase 3 start | Alert thresholds may be meaningless without sign-off |
| ITSM tool selection (per IM-009) | Phase 1 decision | Monitoring-to-incident integration blocked |

> **Governance recommendation**: Establish a Monitoring Steering Committee with monthly checkpoints, chaired by IT Manager with CIO as executive sponsor. This replaces passive "CIO sponsorship" with active cross-team coordination.

---

## 9. Next Steps

To move this roadmap from "conditionally approved" to "approved for execution":

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | Approve this roadmap (v2.0) for planning and procurement | CIO | Week 1 |
| 2 | Approve on-call budget and training budget | CIO + HR | Week 1-2 |
| 3 | Send regulatory citations (Section 10 of detail doc) to Legal/Compliance for verification | Service Quality | Week 1 |
| 4 | Select on-call tool (PagerDuty vs. OpsGenie) | IT Manager + DevOps | Week 2 |
| 5 | Select ITSM tool (per IM-009) or confirm approach | IT Manager | Week 2-3 |
| 6 | Begin OpenSearch discovery task (current log volume, scope) | DevOps | Week 2 |
| 7 | Schedule Prometheus/Grafana/OpenSearch training for team | IT Manager | Month 1 |
| 8 | Initiate business KPI validation conversations with Finance, Claims, Underwriting | Service Quality | Month 1-2 |
| 9 | Contact EbaoTech vendor regarding health probe agreement | Integration / Vendor Manager | Month 2 |
| 10 | Establish Monitoring Steering Committee and schedule first meeting | IT Manager + CIO | Month 1 |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | IT Operations | Initial draft (single document) |
| 2.0 | 2026-03-20 | IT Operations | Restructured into overview + detail; incorporated CIO review (43 findings); added team structure, staffing plan, human costs, missing monitoring domains (RUM, cost, commission), PII scrubbing, training as Phase 1 deliverable |
