# Monitoring & Alerting Roadmap

> **Version**: 2.3
> **Technical reference**: `monitoring-alerting-roadmap-detail.md`

---

## 1. What We Monitor

### 1.1 Design Principle: Journey-First Monitoring

Technical metrics alone cannot prove the business is running. A healthy infrastructure can still hide a broken application submit flow or a stalled underwriting queue. TCLife's monitoring is therefore organized around **customer and business journeys first**, with technical layers supporting them.

The nine core journeys we monitor end-to-end:

| Journey | What we trace |
|---------|--------------|
| **J1 Digital acquisition** | Landing > product browse > quote/illustration > lead capture > agent assignment |
| **J2 Sales submission** | Illustration > rider selection > proposal save > document upload > declaration > payment > submit |
| **J3 Identity & payment** | eKYC/liveness > payment auth/capture > callback > receipt |
| **J4 Underwriting** | STP rules > referrals > manual underwriting > evidence > decision |
| **J5 Policy issuance** | Policy number > schedule/posting > document generation > delivery > rider activation |
| **J6 After-sales servicing** | Contact/beneficiary change, premium mode change, loan/withdrawal, rider add/drop |
| **J7 Billing & persistency** | Renewal due > debit attempt > grace > arrears > reinstatement/lapse |
| **J8 Claims & benefits** | FNOL > intake > assessment > fraud checks > approval/reject > payment |
| **J9 Agent/Ops productivity** | Queue receive > case work > handoff > closure > quality check |

Each journey is supported by metrics from the technical monitoring layers below. When a journey metric degrades, technical layers help diagnose why.

### 1.2 Monitoring Domains

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

  Cross-cutting: DATA PROTECTION & PRIVACY
  PII scrubbing in logs/traces, access controls on dashboards, data
  sovereignty, privacy-incident alerting (72-hour breach notification
  support per Personal Data Protection Law 91/2025/QH15, pending Legal
  verification). Observability data itself may be regulated personal data.

  Cross-cutting: RIDER MONITORING
  Rider attachment, eligibility, pricing, issuance, renewal, and claimability
  treated as first-class monitoring dimensions across all relevant journeys

  Cross-cutting: AML / FRAUD PRODUCTION TELEMETRY
  Real-time detection for premium/payment anomalies, early surrender,
  unusual beneficiary changes, agent/channel anomalies
  (AML Law 14/2022/QH15, pending Legal verification)
```

### Domain Coverage by Phase

| Domain | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|:-------:|:-------:|:-------:|:-------:|
| Infrastructure | Full | Maintained | Maintained | Capacity planning |
| Application | — | Full | Maintained | Tracing evaluation |
| Business Process | — | — | Full | Anomaly detection |
| Vendor / Insuremo | — | Full | Enhanced | Maintained |
| Batch Jobs | — | — | Full | Automation |
| Security | Basic (GuardDuty) | Core (WAF, CloudTrail, Security Hub, Macie, privacy-incident detection) | Enhanced (AML/fraud telemetry) | Advanced |
| Cost | Basic (billing alarms) | — | — | Optimization |
| User Experience (RUM) | — | Basic | Full | Maintained |

---

## 2. Metrics by Stakeholder

What each department sees — why it matters to them — and what "good" looks like.

### Operations Department (ITO)

**Goal**: Work queues stay current and SLA compliant. No stuck cases or silent failures.

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| System health status (all services) | Detect and respond to outages | "Customer Portal error rate spiked to 5% at 14:22" |
| Active alerts by severity | Prioritize response | "2 SEV2 alerts, 1 SEV3 — address SEV2 first" |
| On-call dashboard | Know who is responsible | "Nguyen is primary on-call this week" |
| Batch job completion matrix | Verify daily operations | "GL file delivered on time; NAV calculation pending" |
| Incident metrics (MTTD, MTTR) | Track operational performance | "P1 MTTD improved from 45 min to 4 min" |
| Work queue backlogs and SLA breach counts | Prevents queue pile-up | "Underwriting queue: 0 items past SLA; oldest case: 4h" |
| Exception taxonomy by reason/product/rider | Root-cause lens for process improvement | "Top exception: missing medical evidence (32 cases)" |

**Top risks to surface**: Queue pile-up, integration failures, document/image delays, rules-engine errors, payment posting mismatch, stuck cases with no status change.

### Sales / Distribution

**Goal**: Illustrate, quote, submit, and track case status quickly. High conversion, low dropout.

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| Sale Portal availability and performance | Agent productivity — lost selling time hurts NBP | "Sale Portal P95 response time: 380ms" |
| Quote-to-proposal conversion rate | System friction detection | "Conversion dropped to 22% — investigate UX issue" |
| Policy issuance pipeline status | Revenue visibility | "127 policies issued today, within normal range" |
| Commission batch processing status | Agent compensation assurance | "Commission run completed; 412 agents processed" |
| Lead routing and assignment lag | Prevents lead decay | "Hot lead queue: 0 unassigned > 15 min" |
| Rider pricing/eligibility accuracy | Rider defects create complaints and leakage | "Rider conflict rate this week: 0.1%" |
| Case-status visibility and sync lag | Agents need accurate next actions | "Portal-to-core status sync lag: < 2 min average" |
| Post-issue quality (free-look, early cancellation) | Detects mis-selling or process defects | "Free-look rate by channel: within normal range" |

**Top risks to surface**: Portal outage, quote errors, rider pricing defects, lead assignment delays, case status not updating, high cancellation/free-look rate.

### Customer / End User

**Goal**: Buy, view, pay, service, and claim without friction.

| What They See (via operations) | Why It Matters | Example |
|-------------------------------|----------------|---------|
| Customer Portal availability | Policyholder self-service | "99.92% availability this month" |
| Claims processing time | Policyholder experience | "Average registration-to-assessment: 1.8 days" |
| Policy servicing response time | Policyholder satisfaction | "Surrender request processing: within SLA" |
| Real user performance (RUM) | Actual user experience in the field | "Mobile users in Mekong Delta: 3.2s page load" |
| Login and session health | Customers must access policies | "Login success rate: 99.7%; OTP delivery P95: 2.1s" |
| Payment success and receipt delivery | Immediate premium/revenue protection | "Payment callback success: 99.9%; 0 duplicate charges" |
| Rider display and eligibility accuracy | Rider mismatch creates complaints | "Quote-to-issue rider consistency: 100%" |

**Top risks to surface**: Slow portals, broken eKYC, payment failures, policy pack not delivered, rider mismatch, duplicate charges.

### Underwriting

**Goal**: High STP rate, fast turnaround, clean data, no silent rule misconfiguration.

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| STP rate by product/channel/rider | Primary cost and turnaround metric | "STP rate: 78% (target: 75%); CI rider STP: 65%" |
| Decision turnaround time (P50/P95) | Customer and sales experience | "P95 underwriting TAT: 6h (standard), 18h (underwritten)" |
| Referral backlog and oldest case age | Detects capacity or rule defects | "Manual referral backlog: 12 cases; oldest: 8h" |
| Rules-engine health and error count | STP depends on stable decisioning | "Rule evaluation errors: 0 in last 24h" |
| Decision mix by product/rider/channel | Catches silent misconfiguration | "Approve/refer/decline mix: within normal distribution" |

### Finance

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| GL posting timeliness | Financial close | "GL file delivered at 07:42, before 08:00 deadline" |
| Premium collection success rate | Revenue assurance | "98.3% collection success; 1.7% failed — retry scheduled" |
| NAV calculation completion | UL fund reporting | "NAV calculated by 09:48 — within 10:00 AM deadline" |
| Bank reconciliation status | Financial accuracy | "Reconciliation complete; zero variances" |
| Renewal due pipeline (7/30 day view) | Forward-looking revenue risk | "Premium at risk next 30 days: VND 2.1B; collection gap: 3%" |
| Billing posting controls | Prevents complaints and leakage | "Duplicate retries: 0; premium allocation errors: 0" |

### Management / CIO

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| Business health — single dashboard | "Is the business running?" | Green/yellow/red status for all business processes |
| Journey health summary | End-to-end flow status | "J2 Sales submission: green; J4 Underwriting: yellow (STP dip)" |
| SLA compliance (30-day rolling) | Risk and performance posture | "Sale Portal: 99.96% (target: 99.95%)" |
| Vendor (Insuremo) SLA tracking | Vendor accountability | "Insuremo: 99.87% availability (contract: 99.9%) — vendor notified" |
| Incident trend (monthly) | Operational maturity | "P1 incidents: 2 this month vs. 5 last month" |
| Monitoring program progress | Investment tracking | "Phase 2: 80% complete, on schedule" |

### Compliance / Risk

**Goal**: Complete audit trails, access anomalies surfaced, report completeness, policy wording traceability.

| What They See | Why It Matters | Example |
|--------------|----------------|---------|
| System availability evidence | Regulatory reporting | "Regulated services: 99.9%+ for Q1 2026" |
| Incident history (policyholder impact) | Audit trail | "3 incidents affected policyholders in Q1; all resolved within SLA" |
| Batch processing proof | Financial reporting integrity | "All GL, regulatory, and NAV batches completed within SLA for 90 consecutive days" |
| Data breach / security event log | Data protection compliance | "Zero data breach events in Q1" |
| Privacy-incident alert status | 72-hour notification readiness (Personal Data Protection Law 91/2025/QH15, pending Legal verification) | "0 privacy incidents requiring notification; 72-hour workflow tested quarterly" |
| AML/fraud detection telemetry | Suspicious activity monitoring (AML Law 14/2022/QH15, pending Legal verification) | "AML detection active; 0 escalations to regulators this quarter" |
| Audit trail completeness | No audit trail = control failure | "% critical actions logged with actor/time/object/result: 100%" |
| Consent and privacy controls | Required governance evidence | "Consent capture success: 100%; DSAR SLA adherence: 100%" |

---

## 3. Tool Landscape

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
  - CloudWatch RUM or Grafana Faro (RUM — evaluate in Phase 2)
  - AWS Security Hub (security finding aggregation) — Phase 2
  - AWS Cost Anomaly Detection — Phase 1
  - Insuremo Health Prober (custom) — Phase 2
  - Batch Job Monitor (custom) — Phase 3
  - Status page (external communication) — Phase 2/3
```

All components are AWS managed services except the Insuremo Health Prober and Batch Job Monitor, which are lightweight services running on the existing EKS cluster.

---

## 4. Roadmap Summary

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
| InsureMO monitoring (leverage native eBaoCloud API telemetry first, then deploy Health Prober for independent verification) | DevOps | Insuremo availability and latency visible; 30-day baseline |
| Security monitoring (GuardDuty, WAF, CloudTrail, Security Hub as aggregation point, Macie for S3 PII detection) | DevOps | Security events centralized and alerting; privacy-incident detection foundation |
| Log-based alerting (error patterns, auth failures) | App Ops + DevOps | 10+ log-based alert rules active |
| Real User Monitoring — foundation (evaluate CloudWatch RUM vs Grafana Faro; select and deploy) | DevOps | RUM data collected for Sale Portal and Customer Portal |
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
| SLO burn-rate alerting | DevOps + Service Quality | SLO targets set; error budget burn-rate alerts active for customer-facing services (reduces alert fatigue vs. simple thresholds) |
| Privacy-incident workflow | DevOps + Compliance | Full 72-hour notification workflow with evidence capture |
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

