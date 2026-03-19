# CIO Review — Monitoring & Alerting Roadmap

> **Reviewer**: CIO
> **Date**: 2026-03-20
> **Document reviewed**: `solutions/monitoring-alerting/monitoring-alerting-roadmap.md` v1.0
> **Status**: Review complete

---

## Overall Verdict: CONDITIONALLY APPROVED

This is a strong, well-structured roadmap that demonstrates genuine understanding of what monitoring means for a life insurance operation. The layered monitoring model, the explicit treatment of the vendor-managed core system (EbaoTech Insuremo), and the insurance-specific business process monitoring section are exactly the right areas of focus. The document is not a generic IT monitoring plan bolted onto an insurance company — it reads like it was written for TCLife's specific context.

That said, several concerns prevent unconditional approval. The most significant are: (1) staffing and skills readiness is underspecified, (2) the compliance section references regulatory instruments that need verification, (3) the cost model omits human resource costs that will dwarf the AWS spend, and (4) two critical monitoring domains are missing entirely. These must be addressed before Phase 1 execution begins.

I am conditionally approving this roadmap for planning and procurement purposes. Phase 1 execution should not begin until the high-severity items below are resolved.

---

## Section-by-Section Review

### Section 1: Executive Summary

**Verdict**: APPROVED

**Strengths**:
- Clear articulation of current state, gap, and target state
- The target state statement ("Every P1/P2 incident is detected by monitoring before users report it") is measurable and the right aspiration
- Correctly identifies that the existing Grafana TV dashboard work covers only EKS health metrics

**Issues**: None material.

---

### Section 2: Current State Assessment

**Verdict**: APPROVED WITH CONCERNS

**Strengths**:
- Honest and unflinching assessment of the current state — nine gaps identified with clear descriptions and risk statements
- The maturity model is a useful framing device for tracking progress
- Correctly flags that the current SLA gauge uses `avg_over_time(up[30d])` which measures scrape availability, not user-facing availability — this is a common mistake and good that it is called out

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-001 | Medium | The maturity targets for 12 months are ambitious in places. Moving Security monitoring from 1 to 2.5 requires not just tooling (GuardDuty, WAF logs) but security operations skills, runbooks, and regular threat review. A target of 2.0 for security at 12 months may be more honest, with 2.5 as a stretch goal. |
| R-002 | Low | The current state table says OpenSearch has "scope and completeness unknown." This unknown should be resolved before Phase 1 starts — it is an input to the log pipeline verification deliverable. Recommend adding a pre-Phase 1 discovery task to inventory what is currently flowing into OpenSearch. |

---

### Section 3: Monitoring Strategy

**Verdict**: APPROVED WITH CONCERNS

**Strengths**:
- The four-layer model (Infrastructure / Platform / Application / Business Process + Security cross-cutting) is sound and well-articulated
- Layer 1 (Infrastructure) metrics and thresholds are specific, measurable, and tool-mapped — this is executable, not aspirational
- Layer 4 (Business Process) is the standout section. Monitoring policy issuance, claims processing, premium collection, NAV calculation, surrender value, and regulatory reporting is exactly what differentiates insurance monitoring from generic IT monitoring. This section demonstrates domain understanding.
- The note on distributed tracing as "future consideration" with OTel-compatible instrumentation from the start is the right call — avoid the tracing rabbit hole now but do not paint yourself into a corner

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-003 | **High** | **Missing monitoring domain: User Experience / Real User Monitoring (RUM).** The roadmap covers synthetic monitoring (blackbox probes from inside the VPC) but does not address Real User Monitoring. For a company with a Sale Portal and Customer Portal, understanding actual user experience (page load times, JS errors, session drop-off, mobile vs desktop performance) is critical. Agents working in remote areas of Vietnam may experience performance that synthetic probes from within the VPC cannot detect. Add RUM as either a Phase 2 or Phase 3 deliverable. This does not require a separate tool — Grafana Faro (open source RUM agent) or a lightweight frontend instrumentation approach would suffice. |
| R-004 | **High** | **Missing monitoring domain: Cost and Budget Monitoring.** Section 12 discusses cost of the monitoring stack itself, but the monitoring strategy does not include AWS cost monitoring as a monitoring domain. For a fully AWS-hosted company, unexpected cost spikes (runaway Lambda invocations, S3 storage explosion, RDS instance upsizing, data transfer charges) can be significant operational events. Add an AWS cost monitoring component: CloudWatch billing alarms, AWS Cost Anomaly Detection, and a cost dashboard in Grafana. This should be Phase 1 — it is simple to implement and has immediate value. |
| R-005 | Medium | Layer 3 (Application) instrumentation standard mandates HTTP histograms, counters, and structured JSON logging. Good. However, there is no mention of **health check endpoint standardization**. Every TCLife-owned service should expose a `/health` or `/healthz` endpoint returning structured health status (including downstream dependency checks). This is a prerequisite for meaningful synthetic monitoring and should be part of the instrumentation standard. |
| R-006 | Medium | Layer 2 (Platform/Middleware) lists secrets rotation status monitoring but does not mention **EKS cluster version and add-on version monitoring**. EKS versions have support windows, and running on an unsupported version is both a security risk and an operational risk (AWS stops patching). Add a metric or check for EKS cluster version currency. |
| R-007 | Low | The security monitoring section (3.6) schedules GuardDuty and WAF as Phase 2. Given that TCLife handles policyholder PII and health data subject to the Cybersecurity Law 2018, I would recommend pulling at least basic GuardDuty integration into late Phase 1 or Phase 1.5. GuardDuty is a managed service that requires minimal setup — enable it, route findings to OpenSearch, and create a simple alert rule for High-severity findings. The incremental effort is small; the risk reduction is meaningful. |

---

### Section 4: Alerting Strategy

**Verdict**: APPROVED

**Strengths**:
- Severity-to-incident-priority mapping is clean and aligned with the classification matrix
- The alert quality principles section is excellent — "Every alert must be actionable" and "Alert on symptoms, not causes" are the right cultural foundations to set
- Alert inhibition and grouping configuration (Alertmanager YAML) is practical and shows understanding of how alert storms work in production
- The 30-day tuning window per alert is a strong practice
- The weekly alert review is the right cadence

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-008 | Medium | The on-call model specifies "Primary on-call: 1 infrastructure engineer + 1 application engineer, rotating weekly." This assumes the team is large enough to sustain a rotation without burnout. With a typical small-to-mid insurance IT team, a weekly rotation of 2 people means each person is on call roughly every 2-3 weeks. This is sustainable only if there are at least 6-8 qualified on-call engineers. **The roadmap does not state the current team size or the minimum team size needed.** This must be documented. |
| R-009 | Medium | SEV1 auto-escalation to "CTO at 15 min if unacknowledged." TCLife's organizational chart and escalation titles should be verified — does the company have a CTO, or should this be CIO? Additionally, the CIO review of the classification matrix (Appendix C.6) specified CIO involvement thresholds for P1 incidents. Ensure the alerting escalation chain is consistent with the classification matrix's communication requirements. |
| R-010 | Low | The `repeat_interval` comment says "SEV1: 1h, SEV2: 4h, SEV3: 12h" but the YAML shows a single `repeat_interval: 4h`. This should be implemented as severity-based routing with different repeat intervals, not a global setting. Document how Alertmanager route configuration will differentiate these. |

---

### Section 5: Tool Mapping

**Verdict**: APPROVED

**Strengths**:
- Clean separation of concerns between Prometheus (metrics), OpenSearch (logs), CloudWatch (AWS-native), and PagerDuty/OpsGenie (on-call management)
- The data flow architecture diagram is clear and shows how the pieces connect
- The domain-to-tool matrix in 5.3 is a useful reference that will prevent confusion about where to look for what
- Correct identification that batch jobs need dual monitoring (Prometheus for status metrics, OpenSearch for job logs)

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-011 | Medium | **No mention of a status page for external communication.** When Sale Portal or Customer Portal is degraded, how are agents and policyholders informed? A status page (Atlassian Statuspage, Instatus, or even a simple S3-hosted static page updated by Lambda) should be in the tooling stack. This connects to IM-004 (customer communication plan) from the incident management backlog. Recommend Phase 2 or Phase 3 delivery. |
| R-012 | Low | The tool mapping does not address **backup and disaster recovery for the monitoring stack itself.** If AMP or AMG has a regional outage, what is the fallback? The document notes "AMP and AMG are managed services with built-in HA" in the risk section, but managed services are not immune to regional incidents. At minimum, ensure CloudWatch Alarms exist as a secondary alerting path for the most critical P1-triggering conditions. This is mentioned in passing in Section 13.1 but should be explicitly architected. |

---

### Section 6: EbaoTech Insuremo Integration

**Verdict**: APPROVED — This is the strongest section of the document.

**Strengths**:
- This section reflects a mature understanding of the vendor-managed PAS challenge. The "External Observation + Data Freshness + SLA Tracking" approach is exactly right.
- The health prober design is well-specified — API health probes, lightweight business queries, data freshness checks, result hash for detecting silent changes
- The Prometheus metric definitions for the prober are production-ready
- Integration point monitoring with specific alert conditions per integration type shows domain knowledge
- The SLA tracking approach with independent measurement (not relying on vendor's own reporting) is the right posture for a regulated insurer
- The vendor communication protocol is practical and correctly sequences validation before vendor contact
- Section 6.3 (Limitations to Acknowledge) is refreshingly honest. Too many roadmaps pretend they can see into vendor systems. Stating what you cannot monitor is as important as stating what you can.

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-013 | Medium | The health prober design uses a test policy number for business queries. **The test data strategy needs careful thought.** Using real production policy numbers risks test noise in audit trails and analytics. Using synthetic test policies risks them being cleaned up by vendor maintenance. Recommend documenting the test data approach explicitly and coordinating with EbaoTech on maintaining a stable, designated test dataset for monitoring probes. |
| R-014 | Medium | The `insuremo_query_result_hash` metric for detecting unexpected result changes is clever, but the alert threshold needs definition. A hash change on a product list query could be a legitimate product update or a data corruption. **Define the expected change frequency per query type** and alert only on changes outside the expected window (e.g., product list changes during business hours but not at 3 AM). |
| R-015 | Low | Probe frequency of 30s for health and 60s for business queries should be validated with EbaoTech to confirm this is within acceptable load. The document mentions this in Section 6.3 but should formalize it as a Phase 2 prerequisite: "Vendor sign-off on probe frequency and endpoints before deployment." |

---

### Section 7: Batch Job & File Exchange Monitoring

**Verdict**: APPROVED WITH CONCERNS

**Strengths**:
- The batch job landscape table is comprehensive — covers GL, printing, datalake, reinsurance, regulatory, NAV, premium, and bank reconciliation
- The five-dimension monitoring framework (Did it start? Did it complete? Was it on time? Was it correct? Was it received?) is clean and memorable — this is the kind of framework that teams actually use
- The Prometheus metric definitions for batch jobs are well-designed, including file size anomaly detection
- Reconciliation monitoring (Section 7.5) addresses the data quality dimension that most batch monitoring frameworks miss

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-016 | **High** | **Missing batch partner: Commission calculation and agent compensation.** Commission runs are a critical batch process for any life insurance company — they directly affect agent/sales force motivation and retention. A failed or incorrect commission run creates immediate pain across the entire distribution channel. Add commission calculation to the batch job landscape table with appropriate criticality (High) and monitoring dimensions. |
| R-017 | Medium | **Missing batch consideration: Regulatory filing calendars.** The regulatory reports row says "Monthly/quarterly/annual" but does not specify which reports have hard deadlines. Vietnam MOF reporting has specific filing dates (e.g., quarterly solvency reports, annual audited financial statements, monthly statistical reports). The monitoring system needs a calendar-aware component that starts alerting as deadlines approach — not just when the batch runs, but when it should have run and has not yet started. Recommend a "regulatory filing countdown" panel on the compliance dashboard. |
| R-018 | Medium | The S3-based file exchange monitoring pattern (S3 Event Notifications -> Lambda -> Prometheus Pushgateway -> AMP) is sound. However, **Pushgateway is an anti-pattern for long-running services** (per Prometheus project guidance). Since the Batch Job Monitor is described as a persistent service, it should use a pull-based model (expose `/metrics` endpoint) rather than pushing to Pushgateway. Reserve Pushgateway only for truly ephemeral jobs (one-shot Lambda functions). |
| R-019 | Low | The file lifecycle diagram shows "Acknowledged" as the final state. For critical financial files (GL, regulatory), also consider a **"Reconciled"** state as the ultimate confirmation — the file was not just received but its contents were successfully processed and matched. |

---

### Section 8: Dashboard Strategy

**Verdict**: APPROVED

**Strengths**:
- The four-level hierarchy (CIO/Management, Operations, Engineering/Debug, TV/NOC) is exactly right — different audiences need different data at different granularity
- Dashboard design standards (color scheme, time ranges, drill-down links, documentation, ownership, review cadence) show maturity in thinking about dashboards as a managed product, not a one-off creation
- The TV dashboard extension plan (adding Business Pulse and Alert Board to the existing System Health) is a natural evolution of the existing work
- Dashboard ownership and quarterly review cadence will prevent dashboard rot

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-020 | Medium | The Level 1 CIO/Management dashboards do not include a **Financial Operations dashboard** specifically for CFO/Finance. Premium collection, GL posting, NAV calculation, and bank reconciliation are finance-critical and the CFO is a stakeholder listed in the audience for the Business Health dashboard. Consider whether the CFO needs a dedicated view that combines financial batch status, premium collection health, and GL posting confirmation — or whether the Business Health dashboard adequately serves this need. At minimum, validate the dashboard design with the actual CFO before building it. |
| R-021 | Low | No mention of **dashboard access control.** Grafana supports organization-based and folder-based access control. Define who can view which dashboards — the CIO dashboard with business KPIs should not be visible to all Grafana users if it contains sensitive business metrics. Define the access model in Phase 1. |
| R-022 | Low | The Engineering/Debug dashboards include "Sale Portal Deep Dive" with "JS error rates" — this implies frontend error monitoring, which ties back to R-003 (missing RUM). Clarify whether this metric comes from backend logs or from actual frontend instrumentation. If the latter, RUM infrastructure is a prerequisite. |

---

### Section 9: Key Metrics & KPIs

**Verdict**: APPROVED WITH CONCERNS

**Strengths**:
- Comprehensive KPI framework spanning infrastructure, application, insurance business, and incident management
- Insurance business KPIs (Section 9.3) are specific, measurable, and mapped to alert thresholds — this is production-ready specification
- The reporting cadence (daily/weekly/monthly/quarterly/regulatory) is appropriate and maps to the right audiences
- Cross-reference to IM-015 from the incident management backlog demonstrates continuity of work

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-023 | **High** | **KPI targets need validation with business owners.** The insurance business KPIs contain specific targets (policy issuance < 4 hours, claims registration-to-assessment < 2 business days, premium collection > 98%, NAV by 10:00 AM, etc.). These are reasonable benchmarks, but **who validated them?** If these are aspirational targets set by IT, they need sign-off from the business lines (Head of Underwriting, Head of Claims, Head of Finance, Head of Operations) before they become monitoring thresholds. Setting alert thresholds on unvalidated targets creates either noise (too tight) or false confidence (too loose). **This is a prerequisite for Phase 3 implementation.** |
| R-024 | Medium | The Sale Portal availability target (99.95%) is higher than the Customer Portal (99.9%). The rationale is not stated. If the reasoning is that agents use the Sale Portal during business hours and generate revenue, that should be documented. If the Customer Portal is used for claims submission (where regulatory SLAs may apply), 99.9% may be insufficient. **Document the rationale for differential SLA targets.** |
| R-025 | Medium | The "Alert-to-incident ratio > 80%" KPI (percentage of P1/P2 incidents detected by monitoring before user report) is the right metric, but 80% in Year 1 is ambitious. Industry benchmarks for organizations building monitoring from near-zero are typically 40-60% in Year 1. Recommend setting 60% as the Year 1 target and 80% as the Year 2 target. Failing to meet an overly ambitious target in Year 1 demoralizes the team. |

---

### Section 10: Compliance & Audit

**Verdict**: NEEDS REVISION

**Strengths**:
- Correctly identifies the key regulatory bodies (MOF, ISA)
- Audit trail requirements with 5-year retention for insurance records and 3-year for system records are in the right range
- The compliance dashboard as an "evidence pack" for regulators and auditors is the right concept
- Log retention architecture (hot -> warm -> archive) with S3 Object Lock for immutability is well-designed

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-026 | **High** | **Regulatory citations need verification.** The section references "Circular 125/2018/TT-BTC," "Decree 13/2023/ND-CP," "Insurance Law 2022 (amended)," and "Circular 50/2017/TT-BTC." These citations must be verified by Legal or Compliance to confirm they are: (a) the correct instruments, (b) currently in force and not superseded, and (c) accurately summarized. Presenting incorrect regulatory references in a document that will be shown to auditors creates credibility risk. **Compliance team must review and validate Section 10.1 before this document is finalized.** |
| R-027 | **High** | **Missing regulation: Circular 09/2020/TT-NHNN** (or its insurance-sector equivalent) on information technology risk management for financial institutions. Also missing: any reference to **Vietnam's Personal Data Protection Decree (Decree 13/2023/ND-CP on personal data protection)** and its specific requirements for breach notification timelines, data processing logs, and cross-border data transfer monitoring. If policyholder data transits through monitoring systems (log aggregation includes PII), the monitoring stack itself falls under data protection regulation. **This is a gap that must be addressed.** |
| R-028 | Medium | The compliance dashboard is scheduled for Phase 4 (months 10-12). For a regulated insurer, this feels late. If a regulator or auditor visits at month 8, the company cannot produce system availability evidence in a structured format. Recommend building a **basic** compliance dashboard in Phase 2 (availability metrics and incident history) and enhancing it in Phase 4 (batch processing evidence, full audit trail). |
| R-029 | Medium | **Data sovereignty.** If OpenSearch or S3 archive stores are in an AWS region outside Vietnam, policyholder data in logs may trigger cross-border data transfer requirements. The document does not specify which AWS region the monitoring stack uses or whether log data that may contain PII (error messages with policy numbers, customer IDs in URLs, etc.) is subject to data residency requirements. **Clarify the AWS region strategy and log data PII scrubbing approach.** |
| R-030 | Low | Retention periods (5 years for insurance records, 3 years for system records) are stated without citing the specific regulatory requirement. These should be mapped to the relevant circular or decree that mandates the retention period. |

---

### Section 11: Roadmap Phases

**Verdict**: CONDITIONALLY APPROVED

**Strengths**:
- Four-phase structure delivers incremental value — each phase has a clear goal, specific deliverables, named owners, and measurable exit criteria
- Phase sequencing is logical: infrastructure first, then application, then business, then advanced. This is the right order.
- Exit criteria are specific and testable (e.g., "Synthetic probes confirm portal reachability every 60 seconds")
- Cross-references to incident management backlog items (IM-005, IM-009, IM-015, IM-018) show integration with existing work

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-031 | **High** | **No staffing plan.** The roadmap assigns owners (Infra team, ITO, Dev team, Integration team, Data team, Operations, Finance, Compliance, Actuarial) but does not state: (a) how many people are on each team, (b) what percentage of their time this roadmap requires, (c) whether any external resources (contractors, AWS professional services, consultants) are needed. For a mid-sized insurance IT team, this roadmap represents a significant workload alongside daily operations. Without a staffing plan, Phase 1 alone could stall because the infra team is also handling daily operational work. **Produce a staffing impact assessment before Phase 1 starts.** |
| R-032 | **High** | **Training is buried in Phase 4.** The risk section (13.1) identifies skills gap as a medium risk and suggests "Training in Phase 1." But no training deliverable appears in the Phase 1 table. If the team does not have Prometheus/Grafana/OpenSearch expertise today, training must be a Phase 1 deliverable, not a hopeful note in the risk section. **Add a training deliverable to Phase 1:** identify skills gaps, enroll team in Prometheus/Grafana/OpenSearch training (AWS offers managed service-specific training), and complete training before or concurrently with implementation. |
| R-033 | Medium | Phase 1 is three months and has 10 deliverables including on-call setup. For a team that is simultaneously running production operations, this is dense. Consider whether Phase 1 should be four months, or whether some deliverables (baseline documentation, log pipeline verification) can start as a "Phase 0" discovery sprint in month 0. |
| R-034 | Medium | Phase 3 depends on "Finance/Operations input on batch SLAs" (Section 13.2). This dependency should be pulled forward — start the conversation with Finance and Operations in Phase 1 or 2, not at the start of Phase 3. SLA definition with business stakeholders takes time because it requires multiple rounds of discussion and sign-off. |
| R-035 | Low | Phase 4 includes "Monitoring-as-Code" (Terraform/CDK for all monitoring config). This is good practice but should be started earlier. Phase 1 dashboard and alert rule creation should use Infrastructure-as-Code from the beginning, even if it is simple YAML files in git. Retrofitting IaC onto manually-created dashboards and alert rules at month 10 is painful and error-prone. |

---

### Section 12: Cost Considerations

**Verdict**: NEEDS REVISION

**Strengths**:
- The pricing model table accurately describes the cost structure of each AWS managed service
- The steady-state estimate of $1,550-3,900/month for AWS services is in a reasonable range for a mid-sized deployment
- Cost optimization strategies are practical and phased

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-036 | **High** | **Human costs are entirely missing.** The largest cost of this roadmap is not the AWS bill — it is the people. On-call compensation, training costs, potential contractor/consultant costs for initial setup, the opportunity cost of engineers building monitoring instead of features, and potentially a dedicated monitoring/SRE hire if the workload demands it. A roadmap that shows $2,500/month in AWS costs but ignores $10,000-20,000/month in human costs presents an incomplete picture to the budget authority. **Add a section on human resource costs**, at minimum including: on-call allowances (monthly estimate), training budget (one-time), external support (if needed), and time allocation from existing staff. |
| R-037 | Medium | The cost estimate for OpenSearch ($800-2,000/month) is the largest line item and also the widest range. The document itself notes that current log volume is unknown (open question in 13.3). This makes the OpenSearch estimate unreliable. **Before finalizing the budget request, measure current log volume** (the pre-Phase 1 discovery task from R-002 serves double duty here). |
| R-038 | Medium | **No cost for synthetic monitoring infrastructure.** The blackbox_exporter is free, but if external synthetic monitoring (from outside the VPC, simulating real user access) is desired, this typically requires a service like AWS Synthetics (CloudWatch Canaries) which has per-canary pricing ($0.0012/run). If 5 canaries run every minute, that is approximately $260/month. This should be included. |
| R-039 | Low | PagerDuty pricing is listed at $21-49/user. The lower end ($21) is the Business plan; the higher end ($49) is the Digital Operations plan. For a small team, the Business plan is sufficient. Recommend starting with the Business plan and upgrading only if advanced features (event intelligence, AIOps) are needed. |

---

### Section 13: Risks & Dependencies

**Verdict**: APPROVED WITH CONCERNS

**Strengths**:
- Risk identification is comprehensive — alert fatigue, skills gap, vendor cooperation, cost overrun, organizational resistance, and scope creep are all real risks
- Mitigations are practical and specific
- The dependency table correctly identifies budget approval and vendor agreement as prerequisites
- Open questions are well-framed and assigned to the right parties

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| R-040 | **High** | **Missing risk: PII in monitoring data.** Logs and metrics may contain policyholder PII (policy numbers in URLs, customer names in error messages, health data in claims processing logs). If this data flows into OpenSearch and Grafana, the monitoring stack becomes a PII store that is subject to data protection regulation. **Add a risk item for PII leakage into monitoring data** with mitigation: define a PII scrubbing policy for logs before ingestion into OpenSearch, and restrict access to log dashboards. |
| R-041 | Medium | **Missing risk: Monitoring stack becomes a target.** A centralized monitoring system that aggregates logs from all systems, security events, and business data is a high-value target for attackers. If the monitoring stack is compromised, the attacker gains visibility into the entire operation and can suppress alerts. **Add a risk item for monitoring stack security** with mitigation: restrict network access to Grafana/OpenSearch, enforce MFA for dashboard access, audit log access patterns. |
| R-042 | Medium | The dependency "CIO sponsorship — All phases" is listed but understates what is needed. This roadmap requires active cross-team coordination (Infra, Dev, ITO, Finance, Compliance, Operations, Actuarial, Vendor Manager). **Recommend establishing a Monitoring Steering Committee** with monthly checkpoints, chaired by IT Manager with CIO as executive sponsor. Without a governance structure, "CIO sponsorship" is a passive concept. |
| R-043 | Low | The open question "Is there a preferred ITSM tool?" connects to IM-009 from the incident management backlog. If the ITSM tool decision is delayed, the monitoring-to-incident integration (creating tickets from alerts) will be blocked. **Recommend making ITSM tool selection a Phase 1 decision**, even if full implementation is later. |

---

### Section 14: Appendix — Cross-References

**Verdict**: APPROVED

**Strengths**:
- Thorough cross-referencing to existing work (Grafana TV dashboard, incident classification, incident backlog, ITO capability declaration, L1 support frontline)
- Explicit mapping of incident management backlog items (IM-005, IM-009, IM-015, IM-018) to roadmap sections — this demonstrates that the monitoring roadmap and incident management work are being treated as a coherent program rather than isolated deliverables
- Reference to specific incident scenarios (347 policies with zero surrender value) grounds the business process monitoring in real examples

**Issues**: None material.

---

## Summary of Findings by Severity

### Critical / High (must address before Phase 1 starts)

| ID | Summary | Section |
|----|---------|---------|
| R-003 | Missing monitoring domain: Real User Monitoring (RUM) | 3 |
| R-004 | Missing monitoring domain: AWS Cost and Budget Monitoring | 3 |
| R-016 | Missing batch partner: Commission calculation and agent compensation | 7 |
| R-023 | Business KPI targets need validation with business owners | 9 |
| R-026 | Regulatory citations must be verified by Legal/Compliance | 10 |
| R-027 | Missing regulatory references (personal data protection, IT risk management) | 10 |
| R-031 | No staffing plan — human resource requirements unspecified | 11 |
| R-032 | Training must be a Phase 1 deliverable, not a risk-section note | 11 |
| R-036 | Human costs entirely missing from cost model | 12 |
| R-040 | Missing risk: PII leakage into monitoring data | 13 |

### Medium (address during Phase 1 or before the relevant phase starts)

| ID | Summary | Section |
|----|---------|---------|
| R-001 | Security monitoring maturity target may be overambitious | 2 |
| R-005 | Health check endpoint standardization missing from instrumentation standard | 3 |
| R-006 | EKS cluster version monitoring missing | 3 |
| R-008 | On-call rotation requires minimum team size documentation | 4 |
| R-009 | Escalation titles (CTO vs CIO) need verification | 4 |
| R-011 | Status page for external communication missing from tool stack | 5 |
| R-013 | Test data strategy for Insuremo health prober | 6 |
| R-014 | `insuremo_query_result_hash` alert threshold needs definition | 6 |
| R-017 | Regulatory filing calendar-aware monitoring missing | 7 |
| R-018 | Pushgateway anti-pattern — use pull model for persistent services | 7 |
| R-020 | CFO/Finance may need dedicated financial operations dashboard | 8 |
| R-024 | Differential portal SLA targets need documented rationale | 9 |
| R-025 | Alert-to-incident ratio target (80%) is overambitious for Year 1 | 9 |
| R-028 | Compliance dashboard should start in Phase 2, not Phase 4 | 10 |
| R-029 | Data sovereignty: AWS region and PII in logs | 10 |
| R-033 | Phase 1 timeline may be too dense for 3 months | 11 |
| R-034 | Business SLA conversations should start in Phase 1-2, not Phase 3 | 11 |
| R-037 | OpenSearch cost estimate unreliable without log volume measurement | 12 |
| R-038 | Synthetic monitoring cost (AWS Synthetics) not included | 12 |
| R-041 | Missing risk: monitoring stack as attack target | 13 |
| R-042 | Monitoring Steering Committee recommended for governance | 13 |

### Low (address as part of normal refinement)

| ID | Summary | Section |
|----|---------|---------|
| R-002 | Resolve OpenSearch "scope unknown" before Phase 1 | 2 |
| R-007 | Pull GuardDuty integration into late Phase 1 | 3 |
| R-010 | Alertmanager repeat_interval should be severity-based | 4 |
| R-012 | DR plan for monitoring stack itself | 5 |
| R-015 | Vendor sign-off on probe frequency as Phase 2 prerequisite | 6 |
| R-019 | Add "Reconciled" state to file lifecycle | 7 |
| R-021 | Dashboard access control model needed | 8 |
| R-022 | JS error metrics require RUM or frontend instrumentation | 8 |
| R-030 | Retention periods need regulatory citation mapping | 10 |
| R-035 | Start IaC for monitoring in Phase 1, not Phase 4 | 11 |
| R-039 | Start with PagerDuty Business plan, not Digital Operations | 12 |
| R-043 | ITSM tool selection should be Phase 1 decision | 13 |

---

## Top 5 Priority Actions

These are the items I want resolved before this roadmap moves from "conditionally approved" to "approved for execution."

1. **Produce a staffing impact assessment** (R-031, R-036). Identify how many FTEs this roadmap requires across each phase, whether external support is needed, and what the human cost is. Present this alongside the AWS cost estimates as a complete budget picture.

2. **Validate regulatory citations with Legal/Compliance** (R-026, R-027). Send Section 10 to the Compliance team for review. Ask them to verify citations, identify any missing regulations (particularly personal data protection and IT risk management circulars), and confirm retention requirements with legal basis.

3. **Add missing monitoring domains** (R-003, R-004, R-016). Add Real User Monitoring, AWS cost monitoring, and commission batch monitoring to the appropriate phases. These are not optional — they represent real operational blind spots.

4. **Add training as a Phase 1 deliverable** (R-032). Before the team starts building Prometheus alert rules and Grafana dashboards, ensure they have the skills. Identify training needs and schedule training in month 1.

5. **Address PII in monitoring data** (R-040, R-029). Define a log scrubbing policy for PII before the log pipeline is expanded. This intersects with data protection regulation and should be designed into the architecture from the start, not retrofitted.

---

## Commendations

This review has been necessarily critical, but I want to explicitly acknowledge what this document does well:

1. **Insurance-specific thinking.** This is not a generic monitoring playbook with insurance labels pasted on. Sections 3.5 (Business Process Monitoring), 6 (Insuremo Integration), 7 (Batch Job Monitoring), and 9.3 (Insurance Business KPIs) demonstrate genuine understanding of what matters in a life insurance operation. The team clearly thought about what happens when NAV calculations are late, when surrender values are wrong, and when GL postings miss their window.

2. **Honest gap assessment.** The current state assessment does not sugarcoat the situation. Saying "security monitoring level 1" and "batch job monitoring level 1" takes courage. It also creates trust — a roadmap that starts from an honest baseline is more credible than one that inflates the starting position.

3. **Cross-referencing discipline.** This roadmap does not exist in isolation. It connects to the incident management work, the ITO capability declaration, the L1 support design, and the existing dashboard work. This is how operational documentation should be built — as an interconnected system, not a collection of standalone documents.

4. **Vendor monitoring realism.** The Insuremo integration section is the best part of this document. It acknowledges what cannot be monitored, designs around the constraint, and includes a vendor communication protocol. Many organizations either pretend they have full visibility into vendor systems or give up and do nothing. This document finds the right middle ground.

5. **Actionability.** The Prometheus metric names, alert rules, dashboard specifications, and Alertmanager configuration patterns mean an engineer could start implementing from this document. It is a roadmap that doubles as a design specification — that is rare and valuable.

---

## Verdict for tcl-orch

**CONDITIONALLY APPROVED.** The roadmap is strategically sound, technically competent, and insurance-aware. It can proceed to planning and procurement (Phase 1 tool selection, on-call budget request, training identification).

Phase 1 execution should not begin until the 10 high-severity items are addressed or have a documented plan for resolution. The five priority actions above are the critical path.

I am satisfied that the IT Operations team has produced a credible, well-researched document. With the revisions noted above, this roadmap will provide a solid foundation for TCLife's monitoring capability.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | CIO | Initial review of monitoring-alerting-roadmap.md v1.0 |
