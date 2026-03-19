# Monitoring & Alerting Roadmap — Technical Reference

> **Version**: 2.0
> **Date**: 2026-03-20
> **Author**: IT Operations
> **Status**: Revised — incorporating CIO review findings (R-001 through R-043)
> **Audience**: IT Operations, DevOps, Application Support, Engineering
> **Companion document**: `monitoring-alerting-roadmap-overview.md` (executive overview)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Team Structure & Staffing Plan](#2-team-structure--staffing-plan)
3. [Current State Assessment](#3-current-state-assessment)
4. [Monitoring Strategy](#4-monitoring-strategy)
5. [Alerting Strategy](#5-alerting-strategy)
6. [Tool Mapping](#6-tool-mapping)
7. [EbaoTech Insuremo Integration](#7-ebaotech-insuremo-integration)
8. [Batch Job & File Exchange Monitoring](#8-batch-job--file-exchange-monitoring)
9. [Dashboard Strategy](#9-dashboard-strategy)
10. [Key Metrics & KPIs](#10-key-metrics--kpis)
11. [Compliance & Audit](#11-compliance--audit)
12. [Data Protection & PII Policy](#12-data-protection--pii-policy)
13. [Training Plan](#13-training-plan)
14. [Roadmap Phases](#14-roadmap-phases)
15. [Cost Considerations](#15-cost-considerations)
16. [Risks & Dependencies](#16-risks--dependencies)
17. [CIO Review Findings — Resolution Matrix](#17-cio-review-findings--resolution-matrix)
18. [Appendix: Cross-References to Existing Work](#18-appendix-cross-references-to-existing-work)

---

## 1. Executive Summary

TCLife operates a fully AWS-hosted life insurance platform serving policyholders, sales agents, and internal operations across Unit-Linked (UL), Critical Illness (CI), Health Insurance (HI), and Medical Reimbursement (MR) product lines. The core insurance system (EbaoTech Insuremo) is vendor-managed, and the company exchanges batch files with partners for printing, general ledger (GL), and datalake integrations.

Today, TCLife has foundational monitoring components in place — Amazon Managed Grafana, Amazon Managed Service for Prometheus (AMP), and Amazon OpenSearch Service — but lacks a unified, layered monitoring strategy that covers infrastructure, application, business process, and security dimensions. The existing Grafana TV dashboard work (see `solutions/dashboards/`) covers EKS health metrics but does not extend to business-critical flows such as policy issuance, claims processing, premium collection, or the vendor-managed core system.

This roadmap defines a **four-phase implementation plan** to build a comprehensive monitoring and alerting capability over 12 months, delivered by a 7-person team (3 App Ops, 1 Service Quality, 3 DevOps). The phases deliver incremental value: Phase 1 establishes foundational infrastructure monitoring and team training, Phase 2 extends to application-level observability and security, Phase 3 adds insurance-specific business metrics and batch job monitoring, and Phase 4 introduces advanced capabilities including capacity planning and audit-grade compliance reporting.

**Target state**: Every P1/P2 incident is detected by monitoring before users report it. Every business-critical batch job is tracked for timeliness and success. The CIO has a single dashboard showing system health, SLA compliance, and business processing status.

**Changes from v1.0**: This version incorporates all 43 CIO review findings (10 high, 21 medium, 12 low). Major additions: team structure and staffing plan, training as Phase 1 deliverable, missing monitoring domains (RUM, AWS cost, commission batch), PII scrubbing policy, human cost model, and regulatory citation qualification. See Section 17 for the full resolution matrix.

---

## 2. Team Structure & Staffing Plan

### 2.1 Team Composition

| Role | Headcount | Primary Skills | Monitoring Focus |
|------|-----------|---------------|-----------------|
| **Application Operations (App Ops)** | 3 | Production operations, incident response, L1/L2 support | Alert triage, on-call rotation, runbook execution, batch job monitoring, dashboard daily use |
| **Service Quality** | 1 | SLA management, process improvement, compliance reporting | KPI framework, alert quality review, compliance dashboard, SLA reporting, stakeholder coordination |
| **DevOps / Cloud Engineers** | 3 | AWS, Kubernetes, Terraform, Prometheus, Grafana, OpenSearch | Monitoring infrastructure, alert rule engineering, instrumentation, custom probers, IaC |

### 2.2 On-Call Rotation

> _Addresses R-008: minimum team size for sustainable on-call rotation._

With 6 engineers eligible for on-call (3 App Ops + 3 DevOps):

- **Primary on-call**: 1 person per week, rotating through 6-week cycle
- **Secondary on-call (escalation)**: IT Manager or senior DevOps engineer
- **Coverage**: 24/7 for SEV1; business hours for SEV2-4
- **Sustainability**: Each person is on-call once every 6 weeks. This is sustainable for a team of this size.
- **Compensation**: Per company HR policy (on-call allowance). Budget estimate: $500-1,500/month across the team.
- **Handoff**: 09:00 daily with 15-minute verbal handoff covering active alerts, recent incidents, pending items.

### 2.3 Staffing Allocation Per Phase

| Phase | App Ops (3 FTE) | Service Quality (1 FTE) | DevOps (3 FTE) | Risk |
|-------|-----------------|------------------------|----------------|------|
| **Phase 1** (Mo 1-3) | 40% | 20% | 60% | DevOps overloaded if daily ops are not covered |
| **Phase 2** (Mo 4-6) | 30% | 30% | 50% | Instrumentation depends on dev team cooperation |
| **Phase 3** (Mo 7-9) | 40% | 40% | 40% | Business KPI validation may delay dashboard delivery |
| **Phase 4** (Mo 10-12) | 20% | 40% | 30% | Scope must be managed to allow Year 2 planning |

> _Addresses R-031 and R-036: staffing plan and human cost model._

**External support needs**:
- **Phase 1**: AWS training for Prometheus/Grafana/OpenSearch (all 7 staff). Budget: $3,600-7,200 one-time.
- **Phase 1-2 (optional)**: AWS Professional Services or partner for OpenSearch tuning and initial Prometheus rule development. Budget: $0-3,000/month for 2-3 months.
- **No new hires assumed** in Year 1. If the team is consistently unable to meet phase deliverables alongside daily operations, escalate to CIO for additional headcount or contractor budget.

---

## 3. Current State Assessment

### 3.1 What We Have

| Component | Status | Coverage |
|-----------|--------|----------|
| **Amazon Managed Grafana** | Active | EKS TV dashboard (4 systems), basic health/latency/error panels |
| **Amazon Managed Service for Prometheus (AMP)** | Active | Container metrics via kube-state-metrics, cAdvisor; application metrics where instrumented |
| **Amazon OpenSearch Service** | Active | Log aggregation (scope and completeness unknown — **pre-Phase 1 discovery required per R-002**) |
| **EbaoTech Insuremo** | Vendor-managed | Separate monitoring stack; TCLife has realtime query/search access only |
| **CloudWatch** | Active (inherent to AWS) | AWS service metrics, EKS control plane, ALB, RDS, S3, Lambda |
| **Grafana TV Dashboard** | Implemented | Per-system health, uptime/SLA gauge, P95 latency, error rate, throughput, CPU/memory, critical alerts |

### 3.2 Known Gaps

| Gap Area | Description | Risk |
|----------|-------------|------|
| **No business-process monitoring** | No dashboards or alerts for policy issuance latency, claims processing throughput, premium collection success, NAV calculation, or surrender value computation | Silent P1 incidents — business logic errors that produce wrong financial outcomes with no alert |
| **No batch job monitoring** | GL file exchange, printing partner files, datalake feeds, **commission calculation (R-016)** — no tracking of job success/failure, file arrival time, or reconciliation | Missed SLA deadlines, undetected data gaps, regulatory reporting failures |
| **No EbaoTech Insuremo health visibility** | Vendor monitors their own stack; TCLife has no independent view of core system responsiveness, API health, or data freshness | Total dependency on vendor notification; no ability to detect degradation proactively |
| **Limited application instrumentation** | Prometheus scraping exists for EKS workloads, but coverage of HTTP histograms, custom business counters, and distributed traces is inconsistent | Latency P95 and error rate panels may show incomplete data |
| **No structured log alerting** | OpenSearch collects logs but no systematic alerting on error patterns, exception spikes, or security events | Logs are reactive (searched after an incident) rather than proactive |
| **No security monitoring integration** | No SIEM, no GuardDuty alerting pipeline, no WAF logging dashboards | Security incidents rely on manual discovery; gaps identified in IM-002 of the incident management backlog |
| **No on-call alerting pipeline** | Alert rules exist in Prometheus/Alertmanager, but no integration with PagerDuty/OpsGenie for after-hours escalation | After-hours P1 incidents have no automated wake-up mechanism (gap IM-005) |
| **No SLA measurement system** | Uptime/SLA gauge on TV dashboard uses `avg_over_time(up[30d])` — measures scrape availability, not user-facing service availability | SLA reporting does not reflect actual policyholder or agent experience |
| **No synthetic monitoring** | No external probes testing login flows, quote creation, or portal availability from outside the VPC | Cannot distinguish between "system is up" and "users can actually transact" |
| **Incomplete CloudWatch integration** | CloudWatch metrics for managed AWS services (RDS, S3, SQS, Lambda) are not pulled into Grafana/Prometheus dashboards | Blind spots on database performance, queue depths, storage, and serverless workloads |
| **No Real User Monitoring (R-003)** | No frontend instrumentation capturing actual user experience (page load, JS errors, session drop-off, mobile vs desktop) | Synthetic probes from inside VPC cannot detect performance issues experienced by agents in remote areas of Vietnam |
| **No AWS cost monitoring (R-004)** | No automated detection of unexpected AWS cost spikes | Runaway Lambda invocations, storage explosion, data transfer charges can be significant |
| **No PII scrubbing in logs (R-040)** | Logs may contain policyholder PII (policy numbers in URLs, customer names in error messages, health data in claims processing logs) | Monitoring stack becomes an uncontrolled PII store subject to data protection regulation |

### 3.3 Maturity Assessment

| Domain | Current Level | Target Level (12 months) | Notes |
|--------|--------------|--------------------------|-------|
| Infrastructure monitoring | 2.5 | 4 | Full stack with alerting and capacity planning |
| Application monitoring | 1.5 | 3 | Instrumented services, log-based alerting, error tracking |
| Business process monitoring | 1 | 3 | Key business KPIs tracked and alerted |
| Security monitoring | 1 | **2.0 (revised per R-001)** | GuardDuty, WAF logs, basic threat detection; 2.5 is stretch goal |
| Batch/file monitoring | 1 | 3 | Automated tracking with SLA alerts |
| Alerting & escalation | 1.5 | 3.5 | Tiered alerting with on-call rotation |
| Reporting & compliance | 1 | 3 | Automated SLA and availability reports |
| User experience (RUM) | 0 | 2.5 | New domain added per R-003 |
| Cost monitoring | 0 | 2 | New domain added per R-004 |

> _Security monitoring target revised from 2.5 to 2.0 per R-001. Moving to 2.5 requires security operations skills, runbooks, and regular threat review that may not be achievable in 12 months with current staffing. Target 2.0 with 2.5 as stretch goal._

### 3.4 Pre-Phase 1 Discovery Tasks

> _Added per R-002 and R-037._

Before Phase 1 execution begins, complete these discovery tasks:

| Task | Owner | Output | Why |
|------|-------|--------|-----|
| Inventory current OpenSearch log coverage | DevOps | Document of what is and is not flowing into OpenSearch | Required for log pipeline verification (Phase 1) and OpenSearch cost estimate |
| Measure current log volume (GB/day) | DevOps | Log volume measurement | Required for accurate OpenSearch sizing and cost |
| Measure current Prometheus metric cardinality | DevOps | Cardinality report | Required for accurate AMP cost estimate |
| Verify EKS cluster version and support window | DevOps | Version status report | Per R-006: ensure cluster is on supported version |

---

## 4. Monitoring Strategy

### 4.1 Layered Monitoring Model

TCLife's monitoring covers four layers plus two cross-cutting domains:

```
  Layer 4: BUSINESS PROCESS
  "Are policies being issued? Are claims being paid? Are premiums collected?"
  ────────────────────────────────────────────────────────────────────────
  Layer 3: APPLICATION
  "Are our applications responding correctly and within acceptable latency?"
  ────────────────────────────────────────────────────────────────────────
  Layer 2: PLATFORM / MIDDLEWARE
  "Are our databases, queues, caches, and managed services healthy?"
  ────────────────────────────────────────────────────────────────────────
  Layer 1: INFRASTRUCTURE
  "Are our servers, containers, networks, and cloud services running?"
  ────────────────────────────────────────────────────────────────────────
  Cross-cutting: SECURITY
  "Are we under attack? Is there unauthorized access? Is data being exfiltrated?"
  ────────────────────────────────────────────────────────────────────────
  Cross-cutting: USER EXPERIENCE (RUM)       [NEW — per R-003]
  "What is the actual end-user experience in the browser/device?"
  ────────────────────────────────────────────────────────────────────────
  Cross-cutting: COST MONITORING             [NEW — per R-004]
  "Are we spending within expected bounds? Are there cost anomalies?"
```

### 4.2 Layer 1 — Infrastructure Monitoring

**Scope**: EKS clusters, EC2 instances, RDS databases, S3 buckets, VPC networking, ALB/NLB, Lambda functions, SQS queues, and all AWS managed services.

**Data sources**: Prometheus (kube-state-metrics, cAdvisor, node-exporter), CloudWatch metrics.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Node health | `kube_node_status_condition{condition="Ready"}` | Prometheus | Any node NotReady > 2 min |
| Pod restarts | `kube_pod_container_status_restarts_total` | Prometheus | > 3 restarts in 15 min |
| CPU utilization | `container_cpu_usage_seconds_total` / limits | Prometheus | > 80% sustained 5 min |
| Memory utilization | `container_memory_working_set_bytes` / limits | Prometheus | > 85% sustained 5 min |
| Disk I/O and capacity | `node_filesystem_avail_bytes` | Prometheus | < 15% free |
| RDS connections | `DatabaseConnections` | CloudWatch | > 80% max connections |
| RDS CPU | `CPUUtilization` | CloudWatch | > 75% sustained 10 min |
| RDS storage | `FreeStorageSpace` | CloudWatch | < 20% free |
| RDS replication lag | `ReplicaLag` | CloudWatch | > 10 seconds |
| ALB 5xx rate | `HTTPCode_ELB_5XX_Count` | CloudWatch | > 1% of total requests |
| ALB latency | `TargetResponseTime` | CloudWatch | P99 > 2 seconds |
| SQS queue depth | `ApproximateNumberOfMessagesVisible` | CloudWatch | > age threshold (queue-specific) |
| SQS dead letter queue | `ApproximateNumberOfMessagesVisible` on DLQ | CloudWatch | > 0 messages |
| Lambda errors | `Errors` | CloudWatch | > 5% invocation error rate |
| Lambda duration | `Duration` | CloudWatch | P95 > 80% of timeout |
| S3 request errors | `4xxErrors`, `5xxErrors` | CloudWatch | Sustained spike |
| VPC flow anomalies | VPC Flow Logs | OpenSearch | Unusual traffic patterns |
| **EKS cluster version** | Custom check or `kube_node_info` | Prometheus / CloudWatch | **EKS version within 60 days of EOL (R-006)** |

### 4.3 Layer 2 — Platform / Middleware Monitoring

**Scope**: Message queues, caching layers, API gateways, service mesh (if any), DNS resolution, certificate expiry.

| What to Monitor | Why | Tool |
|----------------|-----|------|
| Message queue consumer lag | Backlog buildup means processing is behind | Prometheus custom metrics or CloudWatch |
| Cache hit/miss ratio | Cache degradation causes latency spikes | Prometheus (ElastiCache metrics via CloudWatch exporter) |
| API Gateway latency and error rates | Gateway is the front door for all API traffic | CloudWatch + Prometheus |
| TLS certificate expiry | Expired certs cause outages | Prometheus blackbox_exporter or cert-manager metrics |
| DNS resolution time | DNS failures are silent killers | Prometheus blackbox_exporter |
| Secrets rotation status | Expired credentials cause auth failures | Custom metric from Secrets Manager events |

### 4.4 Layer 3 — Application Monitoring

**Scope**: All TCLife-owned applications — Sale Portal, Customer Portal, middleware/integration services, batch processing applications.

**Instrumentation standard**: All applications MUST expose:
- HTTP request duration histogram (`http_request_duration_seconds_bucket`)
- HTTP request counter by status code (`http_requests_total`)
- Custom business event counters (per application)
- Structured JSON logging to OpenSearch
- **Health check endpoint** (`/health` or `/healthz`) returning structured status including downstream dependency checks **(R-005)**

| What to Monitor | Metric | Tool |
|----------------|--------|------|
| Request latency (P50, P95, P99) | `histogram_quantile` on HTTP duration | Prometheus + Grafana |
| Error rate (4xx, 5xx) | `rate(http_requests_total{status=~"[45].."}[5m])` | Prometheus + Grafana |
| Throughput (RPM) | `rate(http_requests_total[5m]) * 60` | Prometheus + Grafana |
| Application error logs | Error/exception patterns | OpenSearch + alerting |
| Slow query detection | Database query duration > threshold | Application logs -> OpenSearch |
| Dependency health | Circuit breaker state, downstream call latency | Prometheus custom metrics |
| Session/authentication metrics | Login success/failure rate, session count | Prometheus custom metrics |
| API endpoint-level breakdown | Per-endpoint latency/error/throughput | Prometheus labels |
| **Health check status** | `/health` endpoint per service **(R-005)** | Prometheus blackbox_exporter or custom |

**Distributed tracing** (future consideration): Instrument with OpenTelemetry for request tracing across services. Not in Phase 1-2 scope, but the instrumentation standard should be OTel-compatible from the start.

### 4.5 Layer 4 — Business Process Monitoring

**Scope**: Insurance-specific business flows that directly impact policyholders, agents, and regulatory compliance.

| Business Process | What to Monitor | Why |
|-----------------|----------------|-----|
| **Policy issuance** | End-to-end time from submission to policy activation; conversion rate; rejection rate by reason | Agents blocked = revenue impact; SLA to policyholders |
| **Claims processing** | Claim registration to assessment time; assessment to payment time; auto-approval rate; rejection rate | Regulatory SLA; policyholder experience; fraud detection signal |
| **Premium collection** | Collection success rate; failed payment retry rate; grace period utilization; lapse rate | Revenue assurance; policyholder retention |
| **UL NAV calculation** | NAV calculation completion time; variance from expected; fund price freshness | Regulatory requirement; policyholder statements depend on accurate NAV |
| **Surrender value** | Calculation accuracy (compare with actuarial baseline); batch completion | Scenario from IM backlog — 347 policies with zero surrender value |
| **Quotation engine** | Quote generation time; quote-to-proposal conversion rate | Agent productivity; system responsiveness |
| **Document generation** | Document generation success rate; printing partner file delivery timeliness | Policyholder communication; regulatory filings |
| **Regulatory reporting** | Report generation completion; data freshness; submission timeliness; **regulatory filing countdown (R-017)** | MOF compliance; audit trail |
| **Reinsurance data** | Cession data generation timeliness; reconciliation status | Treaty compliance; financial accuracy |
| **Commission calculation (R-016)** | Commission run completion; agent count processed; accuracy vs expected; timeliness | **Agent/sales force compensation — failed commission run creates immediate pain across entire distribution channel** |

### 4.6 Security Monitoring

**Scope**: Threat detection, access anomalies, data exfiltration, compliance violations.

| What to Monitor | Tool | Priority |
|----------------|------|----------|
| AWS GuardDuty findings | CloudWatch Events -> OpenSearch | **Late Phase 1 / Phase 1.5 for basic integration (R-007)**; full alerting Phase 2 |
| WAF blocked requests and rate limiting | AWS WAF logs -> OpenSearch | Phase 2 |
| IAM anomalies (root login, new admin users, policy changes) | CloudTrail -> OpenSearch | Phase 2 |
| Failed authentication attempts (brute force) | Application logs -> OpenSearch | Phase 2 |
| S3 public access or policy changes | CloudTrail -> OpenSearch + Config Rules | Phase 2 |
| Unusual database query patterns | RDS audit logs -> OpenSearch | Phase 3 |
| Data exfiltration signals (large data exports) | VPC Flow Logs + S3 access logs | Phase 3 |
| Certificate and key usage anomalies | CloudTrail -> OpenSearch | Phase 3 |
| **Monitoring stack access patterns (R-041)** | CloudTrail + Grafana audit logs | **Phase 2 — monitor who accesses the monitoring system itself** |

> _GuardDuty basic integration pulled into late Phase 1 per R-007. It is a managed service requiring minimal setup — enable, route findings to OpenSearch, alert on High-severity findings. Incremental effort is small; risk reduction is meaningful given TCLife handles policyholder PII and health data._

### 4.7 User Experience / Real User Monitoring (RUM)

> _New section — addresses R-003._

**Scope**: Actual end-user experience for Sale Portal and Customer Portal, captured from the browser/device.

**Why this matters**: Synthetic probes from inside the VPC cannot detect performance issues experienced by agents in remote areas of Vietnam (slow mobile networks, high latency). RUM captures what real users actually experience.

**Approach**: Grafana Faro (open-source RUM agent) or equivalent lightweight frontend instrumentation.

| What to Monitor | Metric | Source |
|----------------|--------|--------|
| Page load time (LCP, FCP, TTFB) | Web Vitals metrics | Grafana Faro |
| JavaScript errors | Error count and type by page | Grafana Faro |
| Session drop-off / rage clicks | User frustration signals | Grafana Faro |
| Mobile vs desktop performance | Segmented load times | Grafana Faro |
| Geographic performance (Vietnam regions) | Latency by region | Grafana Faro |
| API call latency (from browser) | XHR/Fetch timing | Grafana Faro |

**Phasing**:
- **Phase 2**: Foundation — deploy Faro agent on Sale Portal and Customer Portal; collect baseline data
- **Phase 3**: Full — dashboards, alerting on performance degradation, geographic segmentation
- **Phase 4**: Advanced — correlation with backend metrics, user journey tracking

> _R-022 note: Engineering dashboard "JS error rates" metric for Sale Portal requires this RUM infrastructure. Until Phase 2, this metric comes from backend error logs only (incomplete view)._

### 4.8 AWS Cost Monitoring

> _New section — addresses R-004._

**Scope**: AWS spend anomaly detection, budget alerts, cost visibility in Grafana.

**Why this matters**: For a fully AWS-hosted company, unexpected cost spikes (runaway Lambda, S3 storage explosion, RDS upsizing, data transfer charges) are operational events.

| Component | Implementation | Phase |
|-----------|---------------|-------|
| CloudWatch Billing Alarms | Set budget thresholds; alert on exceeding 80%, 100% | **Phase 1** — simple to implement, immediate value |
| AWS Cost Anomaly Detection | Enable; route anomaly findings to Slack/email | **Phase 1** |
| Cost dashboard in Grafana | CloudWatch billing metrics visualized in Grafana | **Phase 1** |
| Monitoring stack cost tracking | Dedicated dashboard for AMP, AMG, OpenSearch, CloudWatch costs | **Phase 4** — optimize after steady state reached |

---

## 5. Alerting Strategy

### 5.1 Severity Levels

Alerting severity aligns with the incident classification system defined in `solutions/incident-management/classification.md`:

| Alert Severity | Maps to Incident Priority | Response Expectation | Examples |
|---------------|--------------------------|---------------------|----------|
| **SEV1 — Critical** | P1 | Immediate page; 15-min response | Core system down, data breach detected, all users blocked, financial data corruption |
| **SEV2 — Major** | P2 | Urgent notification; 30-min response | Significant degradation, key function unavailable, batch job SLA at risk |
| **SEV3 — Warning** | P3 | Business hours notification; 2-hr response | Elevated error rate, capacity approaching threshold, single-service degradation |
| **SEV4 — Info** | P4 / no incident | Logged for review; no immediate action | Transient anomaly, below-threshold metric deviation, informational event |

### 5.2 Alert Routing and Notification Channels

> _Escalation title corrected per R-009: CIO, not CTO._

| Severity | Primary Channel | Secondary Channel | Escalation |
|----------|----------------|-------------------|------------|
| **SEV1** | PagerDuty/OpsGenie (on-call engineer) | Slack #incidents + SMS to IC and IT Manager | Auto-escalate to **CIO** at 15 min if unacknowledged |
| **SEV2** | PagerDuty/OpsGenie (on-call engineer) | Slack #incidents | Auto-escalate to IT Manager at 30 min if unacknowledged |
| **SEV3** | Slack #monitoring-alerts | Email to team lead | Review in daily standup if unresolved |
| **SEV4** | Slack #monitoring-info (low-priority channel) | None | Weekly review |

### 5.3 On-Call Model

This directly addresses gap IM-005 from the incident management backlog.

See Section 2.2 for on-call rotation details with the 7-person team structure.

### 5.4 Alert Quality Principles

| Principle | Implementation |
|-----------|---------------|
| **Every alert must be actionable** | If no human action is required, it is a log entry, not an alert |
| **Alert on symptoms, not causes** | Alert on "error rate > 5%" not "CPU > 80%" (unless CPU directly causes user impact) |
| **Tune aggressively in first 30 days** | Every new alert gets a 30-day review; adjust thresholds based on actual behavior |
| **No duplicate alerts** | Suppress child alerts when parent alert fires (e.g., don't alert on every pod restart when the node is down) |
| **Alert routing matches responsibility** | Infrastructure alerts go to infra on-call; application alerts go to app on-call |
| **Document every alert** | Each alert rule has a linked runbook explaining: what it means, what to check, how to resolve |
| **Weekly alert review** | Review all alerts from the past week; identify false positives, tune, or retire. **Owned by Service Quality.** |

### 5.5 Alert Inhibition and Grouping

> _Repeat interval should be severity-based per R-010._

```yaml
# Alertmanager configuration pattern
inhibit_rules:
  # If a node is down, suppress all pod alerts on that node
  - source_matchers: [severity="critical", alertname="NodeDown"]
    target_matchers: [severity=~"warning|critical"]
    equal: [node]

  # If EbaoTech API is unreachable, suppress downstream alerts
  - source_matchers: [alertname="InsuremoAPIUnreachable"]
    target_matchers: [alertname=~"PolicyIssuance.*|ClaimsProcessing.*"]

group_by: [alertname, namespace, severity]
group_wait: 30s
group_interval: 5m

# Severity-based repeat intervals (R-010):
# Implement via route-level configuration:
route:
  routes:
    - matchers: [severity="critical"]
      repeat_interval: 1h
    - matchers: [severity="major"]
      repeat_interval: 4h
    - matchers: [severity="warning"]
      repeat_interval: 12h
```

---

## 6. Tool Mapping

### 6.1 Tool Responsibilities

| Tool | Primary Role | Data Types | Retention |
|------|-------------|------------|-----------|
| **Prometheus (AMP)** | Metrics collection, alerting rules, recording rules | Time-series numeric metrics | 150 days (AMP default) |
| **Grafana (AMG)** | Visualization, dashboards, unified query interface | Renders data from all sources | N/A (dashboards are config) |
| **OpenSearch** | Log aggregation, log-based alerting, security event analysis | Structured/unstructured logs, traces | 30-90 days hot, archive to S3 |
| **CloudWatch** | AWS service metrics, CloudTrail events, billing alerts, cost anomalies | AWS-native metrics and logs | Per metric class (default varies) |
| **PagerDuty/OpsGenie** | On-call management, alert routing, escalation | Alert state, acknowledgements, incidents | Per vendor plan |
| **Grafana Faro** | Real User Monitoring (RUM) **(R-003)** | Frontend performance, JS errors, user sessions | Via Grafana Cloud or self-hosted |
| **AWS Cost Anomaly Detection** | Cost spike detection **(R-004)** | Billing anomalies | AWS managed |
| **Status page** (TBD) **(R-011)** | External communication of portal status | Incident/degradation notices | Per vendor |

### 6.2 Data Flow Architecture

```
                                    ┌─────────────────────┐
                                    │   Amazon Managed     │
                                    │      Grafana         │
                                    │   (Dashboards)       │
                                    └──┬──────┬──────┬─────┘
                                       │      │      │
                          ┌────────────┘      │      └────────────┐
                          │                   │                   │
                          ▼                   ▼                   ▼
              ┌───────────────────┐ ┌──────────────────┐ ┌───────────────────┐
              │  Prometheus (AMP) │ │    OpenSearch     │ │    CloudWatch     │
              │                   │ │                   │ │                   │
              │ - Container metrics│ │ - Application logs│ │ - AWS service     │
              │ - App metrics     │ │ - Security events │ │   metrics         │
              │ - Custom business │ │ - Audit logs      │ │ - CloudTrail      │
              │   counters        │ │ - Trace data      │ │ - Billing +       │
              │ - Recording rules │ │ - RUM data (Faro) │ │   Cost Anomaly    │
              │ - Alerting rules  │ │                   │ │                   │
              │        │          │ │ - Log-based alerts│ │ - CloudWatch      │
              │        ▼          │ │                   │ │   Alarms          │
              │  Alertmanager     │ │                   │ │                   │
              └────────┬──────────┘ └──────────┬────────┘ └─────────┬─────────┘
                       │                       │                    │
                       └───────────┬───────────┘                    │
                                   │                                │
                                   ▼                                │
                       ┌───────────────────┐                        │
                       │   PagerDuty /     │◄───────────────────────┘
                       │   OpsGenie        │   (via CloudWatch -> SNS
                       │                   │    or EventBridge)
                       │ - On-call routing │
                       │ - Escalation      │
                       │ - SMS / Phone     │
                       └───────────────────┘
```

### 6.3 Monitoring Domain to Tool Matrix

| Monitoring Domain | Prometheus | OpenSearch | CloudWatch | Notes |
|-------------------|:----------:|:----------:|:----------:|-------|
| EKS node/pod health | **Primary** | | Secondary | kube-state-metrics, cAdvisor |
| Application latency/errors/throughput | **Primary** | Secondary (logs) | | Requires app instrumentation |
| Application logs and error patterns | | **Primary** | | Structured JSON logs |
| RDS performance | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| S3/SQS/Lambda metrics | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| ALB/NLB metrics | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| EbaoTech Insuremo health | **Primary** (custom probes) | Secondary (query logs) | | Custom exporter (see Section 7) |
| Batch job status | **Primary** (custom metrics) | **Primary** (job logs) | | Dual: metrics for status, logs for detail |
| Security events (GuardDuty, WAF) | | **Primary** | Secondary | CloudWatch Events -> OpenSearch |
| IAM/CloudTrail audit | | **Primary** | Secondary | CloudTrail -> OpenSearch |
| Business process metrics | **Primary** (counters/gauges) | Secondary (event logs) | | Custom instrumentation required |
| Certificate/DNS health | **Primary** (blackbox_exporter) | | | External probe approach |
| Cost and billing | | | **Primary** | CloudWatch billing metrics + Cost Anomaly Detection |
| **User experience (RUM)** | | **Primary** (Faro -> OpenSearch/Grafana) | | **New: R-003** |
| **EKS version currency** | **Primary** | | | **New: R-006** |

### 6.4 Monitoring Stack Resilience

> _Addresses R-012._

| Concern | Mitigation |
|---------|------------|
| AMP regional outage | Maintain CloudWatch Alarms as secondary alerting for P1-triggering conditions (node down, all pods unhealthy, ALB 5xx > threshold) |
| AMG regional outage | CloudWatch console provides basic metric visibility as fallback |
| OpenSearch outage | Critical security events route through CloudWatch Events as backup path |
| Status page | Host on S3 (static) — survives most infrastructure failures |

### 6.5 Status Page for External Communication

> _Addresses R-011. Connects to IM-004 from incident management backlog._

When Sale Portal or Customer Portal is degraded, agents and policyholders need to be informed. Options:
- **Atlassian Statuspage** — full-featured, $79/month
- **Instatus** — lighter, $20/month
- **S3-hosted static page** — minimal cost, updated by Lambda trigger from alert

**Recommendation**: Evaluate in Phase 2; deploy in Phase 2 or 3. Integrate with PagerDuty/OpsGenie to auto-update status when incidents are declared.

---

## 7. EbaoTech Insuremo Integration

### 7.1 The Challenge

EbaoTech Insuremo is vendor-managed. TCLife cannot install agents, export metrics, or access the internal monitoring stack. The only interface is realtime query/search access — we can call the system's APIs and query its database, but we cannot instrument it.

### 7.2 Monitoring Strategy for a Vendor-Managed Core System

**Approach: External Observation + Data Freshness + SLA Tracking**

#### 7.2.1 API Health Probes

Deploy a dedicated **Insuremo Health Prober** service (lightweight, runs on EKS) that periodically calls Insuremo APIs and records response metrics.

```
Insuremo Health Prober (EKS pod)
  │
  ├── Every 30s: Call /api/health or equivalent health endpoint
  │   → Record: response_time, status_code, success/failure
  │
  ├── Every 60s: Execute lightweight read-only business queries
  │   → Policy lookup by designated test policy number
  │   → Premium calculation for test scenario
  │   → Product list retrieval
  │   → Record: response_time, result_hash (detect silent changes)
  │
  ├── Every 5m: Check data freshness
  │   → Query latest policy creation timestamp
  │   → Query latest transaction timestamp
  │   → Compare against expected freshness window
  │
  └── Expose all metrics as Prometheus /metrics endpoint
      → Scraped by AMP
      → Alerted via Alertmanager
      → Visualized in Grafana
```

**Prometheus metrics exposed by the prober**:

| Metric | Type | Labels | Purpose |
|--------|------|--------|---------|
| `insuremo_api_response_time_seconds` | Histogram | `endpoint`, `method` | Track latency per API endpoint |
| `insuremo_api_requests_total` | Counter | `endpoint`, `status_code` | Track success/failure rates |
| `insuremo_api_up` | Gauge | `endpoint` | Binary up/down per endpoint |
| `insuremo_data_freshness_seconds` | Gauge | `entity` (policy, transaction, etc.) | Time since last record update |
| `insuremo_query_result_hash` | Gauge | `query_name` | Detect unexpected result changes |
| `insuremo_health_check_duration_seconds` | Histogram | `check_type` | Probe execution time |

#### 7.2.2 Test Data Strategy

> _Addresses R-013._

- **Designated test dataset**: Coordinate with EbaoTech to establish a stable, designated set of test policies and test scenarios specifically for monitoring probes.
- **Avoid production policy numbers**: Using real production data risks test noise in audit trails and analytics.
- **Document in vendor agreement**: The test data set, its maintenance responsibility, and the expectation that it will not be cleaned up during vendor maintenance.
- **Phase 2 prerequisite**: Test data approach documented and agreed with EbaoTech before prober deployment.

#### 7.2.3 Result Hash Alert Threshold

> _Addresses R-014._

The `insuremo_query_result_hash` metric detects unexpected result changes. Alert logic must account for legitimate changes:

| Query Type | Expected Change Frequency | Alert Logic |
|-----------|--------------------------|-------------|
| Product list | Business hours only; infrequent | Alert on change outside 09:00-17:00 Mon-Fri |
| Test policy lookup | Should never change | Alert on any change |
| Premium calculation (test) | Should not change unless product rules updated | Alert on change; correlate with known product updates |

#### 7.2.4 Integration Point Monitoring

| Integration | What to Monitor | Alert Condition |
|------------|----------------|-----------------|
| Policy creation API | Call latency, success rate, error codes | Latency > 5s or error rate > 1% |
| Premium calculation API | Call latency, result validation | Latency > 3s or unexpected results |
| Claims submission API | Call latency, success rate | Latency > 5s or error rate > 1% |
| Product/rate retrieval | Response time, data staleness | Data unchanged for > 24h (should update daily) |
| Fund price feed (UL) | Price freshness, variance from market | Price older than 4 hours during trading hours |
| Policyholder data sync | Record count, sync latency | Sync gap > 30 min |

#### 7.2.5 SLA Tracking

| SLA Metric | Target | Measurement | Reporting |
|-----------|--------|-------------|-----------|
| API availability | 99.9% (contractual) | `avg_over_time(insuremo_api_up[30d])` | Monthly |
| API response time (P95) | < 3s (contractual) | `histogram_quantile(0.95, ...)` | Weekly |
| Data freshness (policy) | < 15 min during business hours | `insuremo_data_freshness_seconds{entity="policy"}` | Continuous |
| Incident resolution time | Per vendor SLA | Manual tracking (ITSM ticket) | Monthly |
| Planned maintenance windows | Agreed schedule | Calendar tracking | Monthly |

#### 7.2.6 Vendor Communication Protocol

When the health prober detects degradation:

1. **Auto-alert** fires to TCLife on-call (SEV2+)
2. **TCLife on-call** validates the issue is not on TCLife side
3. **Contact vendor** through agreed escalation channel with: timestamp, affected endpoint, error details, impact scope
4. **Track in ITSM** as vendor-related incident
5. **Update SLA log** with incident details for monthly review

#### 7.2.7 Probe Frequency Validation

> _Addresses R-015._

- **Phase 2 prerequisite**: Formal vendor sign-off on probe frequency (30s health, 60s business) and target endpoints before deployment.
- Confirm probing is within acceptable load and will not be rate-limited or flagged.
- Document in vendor monitoring agreement.

### 7.3 Limitations to Acknowledge

- We cannot monitor Insuremo's internal performance (DB queries, queue depths, memory usage)
- We depend on vendor notification for planned maintenance and known issues
- Our probes test the API contract, not the full system; internal degradation that does not yet affect API responses will be invisible
- Probe traffic must be discussed with the vendor to avoid being rate-limited or flagged

---

## 8. Batch Job & File Exchange Monitoring

### 8.1 Batch Job Landscape

> _Commission calculation added per R-016._

| Partner/Process | Direction | Frequency | File Type | Criticality |
|----------------|-----------|-----------|-----------|-------------|
| **General Ledger (GL)** | TCLife -> GL system | Daily | Accounting entries, journal vouchers | High — financial reporting |
| **Printing partner** | TCLife -> Printing vendor | Daily/on-demand | Policy documents, statements, letters | Medium — policyholder communication |
| **Datalake** | TCLife -> Datalake | Daily/near-realtime | Policy, claims, premium, product data | High — analytics, reporting |
| **Reinsurance** | TCLife -> Reinsurer | Monthly/quarterly | Cession data, bordereau | High — treaty compliance |
| **Regulatory reports** | TCLife -> MOF/regulator | Monthly/quarterly/annual | Statutory reports, solvency data | Critical — regulatory compliance |
| **NAV calculation (UL)** | Fund prices -> Insuremo -> TCLife | Daily | Fund prices, NAV values | High — policyholder statements |
| **Premium collection** | Payment gateway -> TCLife | Daily batch reconciliation | Payment files, reconciliation | High — revenue assurance |
| **Bank reconciliation** | Bank -> TCLife | Daily | Bank statement files | High — financial accuracy |
| **Commission calculation** | Insuremo -> TCLife -> agents | Monthly/as scheduled | Agent compensation data | **High — agent/distribution channel satisfaction (R-016)** |

### 8.2 Monitoring Framework for Batch Jobs

Each batch job must be monitored across five dimensions:

```
  ┌──────────────────────────────────────────────────────┐
  │                  BATCH JOB MONITORING                 │
  │                                                      │
  │  1. DID IT START?     - Job trigger confirmation     │
  │  2. DID IT COMPLETE?  - Success/failure/partial      │
  │  3. WAS IT ON TIME?   - SLA adherence               │
  │  4. WAS IT CORRECT?   - Record count, checksums     │
  │  5. WAS IT RECEIVED?  - Partner acknowledgment       │
  │                 (6. WAS IT RECONCILED? - R-019)      │
  └──────────────────────────────────────────────────────┘
```

> _Dimension 6 ("Reconciled") added per R-019 for critical financial files (GL, regulatory). The file was not just received but its contents were successfully processed and matched._

### 8.3 Implementation Pattern: Batch Job Monitor Service

> _Architecture adjusted per R-018: use pull-based model, not Pushgateway._

Deploy a **Batch Job Monitor** as a persistent service on EKS. Since it is a long-running service, it exposes a `/metrics` endpoint for Prometheus scraping (pull model). **Pushgateway is reserved only for truly ephemeral jobs (one-shot Lambda functions).**

**Prometheus metrics**:

| Metric | Type | Labels | Purpose |
|--------|------|--------|---------|
| `batch_job_last_success_timestamp` | Gauge | `job_name`, `partner` | When did the job last succeed? |
| `batch_job_last_run_timestamp` | Gauge | `job_name`, `partner` | When did the job last run (success or failure)? |
| `batch_job_duration_seconds` | Histogram | `job_name`, `partner` | How long did the job take? |
| `batch_job_records_processed` | Gauge | `job_name`, `partner` | How many records were processed? |
| `batch_job_records_failed` | Gauge | `job_name`, `partner` | How many records failed? |
| `batch_job_status` | Gauge | `job_name`, `partner`, `status` | 1 = success, 0 = failure, 0.5 = partial |
| `batch_file_size_bytes` | Gauge | `job_name`, `partner` | File size (detect anomalies) |
| `batch_file_arrival_delay_seconds` | Gauge | `job_name`, `partner` | Time between expected and actual arrival |
| `batch_reconciliation_status` | Gauge | `job_name`, `partner` | 1 = reconciled, 0 = mismatch **(R-019)** |

**Alert rules**:

| Alert | Condition | Severity |
|-------|-----------|----------|
| Batch job did not start | `time() - batch_job_last_run_timestamp > expected_interval * 1.5` | SEV2 |
| Batch job failed | `batch_job_status == 0` | SEV2 (GL, regulatory, commission) / SEV3 (others) |
| Batch job SLA breach | `batch_file_arrival_delay_seconds > sla_threshold` | SEV2 |
| Record count anomaly | `batch_job_records_processed` deviates > 30% from rolling average | SEV3 |
| File size anomaly | `batch_file_size_bytes` deviates > 50% from rolling average | SEV3 |
| Zero records processed | `batch_job_records_processed == 0` when expected > 0 | SEV2 |
| Partner acknowledgment missing | No ACK within expected window | SEV3 |
| **Commission job failed** | `batch_job_status{job_name="commission"} == 0` | **SEV2 (R-016)** |
| **Regulatory filing countdown** | Filing deadline < T-2 days and job not started | **SEV2 (R-017)** |

### 8.4 File Exchange Monitoring Pattern

```
FILE LIFECYCLE:
  Generated -> Validated -> Transferred -> Acknowledged -> Reconciled (R-019)
      │            │            │              │               │
      ▼            ▼            ▼              ▼               ▼
   Timestamp   Checksum     Transfer        ACK file       Contents
   Record cnt  Validation   confirmation    or API         matched and
   File size   result       (S3 event,      confirmation   processed OK
                            SFTP log)
```

**S3-based file exchange monitoring** (most TCLife partners likely use S3):
- S3 Event Notifications -> Lambda -> **Batch Job Monitor service** (which exposes `/metrics` for Prometheus pull)
- Track: file arrival time, file size, file name pattern compliance
- Alert on: missing expected file, unexpected file, file size anomaly

### 8.5 Reconciliation Monitoring

| Reconciliation Type | Check | Frequency | Alert On |
|--------------------|-------|-----------|----------|
| GL record count | Records sent vs. records posted in GL | Daily | Mismatch > 0 |
| Premium collection | Payments collected vs. bank settlement | Daily | Variance > threshold |
| Print job status | Documents sent vs. partner print confirmation | Daily | Unconfirmed after 24h |
| Datalake freshness | Last record timestamp in datalake vs. source | Hourly | Lag > 2 hours |
| NAV values | Published NAV vs. expected NAV from fund manager | Daily | Variance > 0.01% |
| **Commission** | Agents processed vs. expected; total amounts vs. expected range | Per commission run | **Any mismatch or unexpected deviation (R-016)** |

### 8.6 Regulatory Filing Calendar

> _Addresses R-017._

The monitoring system needs a calendar-aware component for regulatory deadlines:

| Report Type | Deadline Pattern | Alert Schedule |
|------------|-----------------|----------------|
| Monthly statistical reports | 15th of following month | T-5 days (warning), T-2 days (critical if not started) |
| Quarterly solvency reports | 45 days after quarter end | T-10 days (warning), T-3 days (critical) |
| Annual audited financial statements | 90 days after year end | T-30 days (warning), T-7 days (critical) |

**Implementation**: Regulatory filing calendar stored as configuration; Batch Job Monitor checks calendar daily and emits countdown metrics. Compliance dashboard shows regulatory filing countdown panel.

---

## 9. Dashboard Strategy

### 9.1 Dashboard Hierarchy

```
  LEVEL 1: CIO / Management Dashboard
  "Is the business running?"
  ─────────────────────────────────────
  LEVEL 2: Operations Dashboard
  "What needs attention right now?"
  ─────────────────────────────────────
  LEVEL 3: Engineering / Debug Dashboards
  "What is the root cause?"
  ─────────────────────────────────────
  TV DISPLAY: NOC / War Room
  "At-a-glance system health"
```

### 9.2 Dashboard Inventory

#### Level 1: CIO / Management Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Business Health** | Policy issuance rate, claims processing time, premium collection success, portal uptime SLA | 5 min | CIO, COO, CFO |
| **Service Availability** | Per-service uptime (30-day rolling), SLA status (met/at-risk/breached), major incident timeline | 5 min | CIO, IT Manager |
| **Vendor SLA** | Insuremo availability, API latency trend, vendor incident count, SLA compliance | 15 min | CIO, Vendor Manager |
| **Batch Job Status** | Daily batch completion matrix (green/yellow/red per partner), SLA adherence trend | 15 min | CIO, Operations |
| **Financial Operations** | GL posting status, premium collection health, NAV calculation, bank reconciliation **(R-020)** | 15 min | **CFO, Finance, CIO** |
| **Cost Overview** | AWS spend trend, anomalies, monitoring stack cost **(R-004)** | Daily | CIO, IT Manager |

> _Financial Operations dashboard added per R-020. Validate design with CFO before building._

#### Level 2: Operations Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Infrastructure Overview** | EKS cluster health, RDS performance, ALB metrics, resource utilization | 1 min | ITO, Infra team |
| **Application Health** | Per-application latency/error/throughput, top slow endpoints, error log stream | 1 min | ITO, App support |
| **Batch Job Operations** | Per-job timeline (expected vs. actual), failure detail, file sizes, reconciliation status | 5 min | ITO, Operations |
| **Alert Overview** | Active alerts by severity, alert history (24h), top flapping alerts, alert response time | 1 min | ITO, On-call |
| **Insuremo Health** | API response times, endpoint availability, data freshness gauges, SLA tracking | 1 min | ITO, Integration team |
| **Security Overview** | GuardDuty findings, WAF blocks, failed auth attempts, CloudTrail anomalies | 5 min | ITO, Security |
| **User Experience (RUM)** | Page load times by portal, JS errors, geographic performance, mobile vs desktop | 5 min | ITO, Dev team |

#### Level 3: Engineering / Debug Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Sale Portal Deep Dive** | Per-endpoint latency/errors, user session metrics, JS error rates (from RUM — R-022), database query performance | 30s | Dev team |
| **Customer Portal Deep Dive** | Per-endpoint latency/errors, authentication flow, claim submission flow, document upload metrics | 30s | Dev team |
| **Database Performance** | Query latency histogram, slow query log, connection pool utilization, lock wait time | 30s | DBA, Dev team |
| **Queue & Integration** | Queue depth over time, consumer lag, message age, DLQ volume, per-integration latency | 30s | Dev team, Integration |

#### TV Display / NOC Dashboards

| TV Dashboard | Content | Kiosk Rotation |
|-------------|---------|----------------|
| **System Health** (existing) | Per-system health, uptime, latency, errors, throughput, resources, alerts | 60s per view |
| **Business Pulse** (new) | Policy issuance count today, claims in progress, premium collection status, batch job matrix, commission status | 60s per view |
| **Alert Board** (new) | Active SEV1/SEV2 alerts, recent incident timeline, on-call contact | Always visible or 30s rotation |

### 9.3 Dashboard Access Control

> _Addresses R-021._

| Dashboard Level | Access Policy |
|----------------|---------------|
| Level 1 (CIO/Management) | Grafana folder with restricted access: CIO, IT Manager, department heads. Contains sensitive business KPIs. |
| Level 2 (Operations) | Grafana folder for ITO team + on-call engineers. |
| Level 3 (Engineering) | Open to all IT staff. |
| TV Display | Read-only kiosk mode; no authentication required on office network. |
| Compliance | Restricted: Compliance team + CIO + IT Manager. |
| Security | Restricted: Security-cleared staff + IT Manager. |

**Phase 1 deliverable**: Define and implement Grafana folder structure and access model.

### 9.4 Dashboard Design Standards

| Standard | Specification |
|----------|--------------|
| **Color scheme** | Green = normal, Yellow = warning, Red = critical. Never use red for non-critical states. |
| **Time range** | Default to "Last 6 hours" for operational; "Last 30 days" for management/SLA |
| **Variables** | Use Grafana template variables for environment (prod/staging), namespace, service |
| **Annotations** | Display deployment events and incident markers on time-series graphs |
| **Links** | Every high-level panel should link to its drill-down dashboard |
| **Documentation** | Each dashboard has a "?" panel or linked wiki page explaining what it shows |
| **Ownership** | Every dashboard has a named owner responsible for keeping it accurate |
| **Review cadence** | Quarterly review of all dashboards for relevance and accuracy |

---

## 10. Key Metrics & KPIs

### 10.1 Infrastructure KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| System availability (Sale Portal) | 99.95% | Synthetic monitoring success rate, 30-day rolling |
| System availability (Customer Portal) | 99.9% | Synthetic monitoring success rate, 30-day rolling |
| Mean Time to Detect (MTTD) | < 5 min for P1 | Time from incident start to first alert |
| Mean Time to Acknowledge (MTTA) | < 15 min for P1 | Time from alert to human acknowledgment |
| P95 response time (Sale Portal) | < 500ms | Prometheus histogram |
| P95 response time (Customer Portal) | < 1s | Prometheus histogram |
| Error rate (5xx) | < 0.1% | Prometheus counter ratio |
| Resource utilization (CPU/memory) | 40-70% average (headroom for spikes) | Prometheus gauges |
| Certificate expiry | > 30 days remaining | Blackbox exporter |
| Database connection utilization | < 70% of max connections | CloudWatch |

> _R-024: Differential SLA targets rationale — Sale Portal (99.95%) serves agents during business hours generating revenue; Customer Portal (99.9%) is primarily self-service. If regulatory SLAs apply to Customer Portal claims submission, revisit this target._

### 10.2 Application KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| Deployment success rate | > 95% | CI/CD pipeline metrics |
| Error log volume (per hour) | Trending down month-over-month | OpenSearch aggregation |
| Slow query rate | < 1% of total queries | Application logs |
| Cache hit rate | > 90% | ElastiCache metrics |
| API endpoint latency (per endpoint) | Within defined SLO per endpoint | Prometheus histogram |

### 10.3 Insurance Business KPIs

> _R-023: All targets below require validation by business line owners (Head of Underwriting, Head of Claims, Head of Finance, Head of Operations) before they become monitoring thresholds. Setting alert thresholds on unvalidated targets creates either noise or false confidence. **This validation is a prerequisite for Phase 3 implementation.** Start business KPI conversations in Phase 1-2 per R-034._

| KPI | Target (pending validation) | Source | Alert Threshold |
|-----|---------------------------|--------|----------------|
| **Policy issuance end-to-end time** | < 4 hours (standard), < 24h (underwritten) | Insuremo API timestamps | > 8 hours for standard products |
| **Policy issuance daily count** | Within 20% of 30-day average | Insuremo query | > 30% deviation |
| **Quote-to-proposal conversion rate** | > 40% (benchmark) | Sale Portal metrics | < 25% (signals system friction) |
| **Claims registration-to-assessment** | < 2 business days | Insuremo API timestamps | > 3 business days |
| **Claims assessment-to-payment** | < 5 business days | Insuremo API timestamps | > 7 business days |
| **Premium collection success rate** | > 98% | Payment gateway + Insuremo | < 95% |
| **Failed payment retry success** | > 70% | Payment gateway metrics | < 50% |
| **Policy lapse rate (monthly)** | < 2% | Insuremo query | > 3% (signals collection issue) |
| **UL NAV calculation timeliness** | By 10:00 AM next business day | Batch job monitor | Not completed by 10:00 AM |
| **UL fund price freshness** | < 4 hours during trading hours | Insuremo API query | > 6 hours |
| **Surrender value accuracy** | 100% match with actuarial baseline | Reconciliation batch | Any mismatch > 0 |
| **GL posting timeliness** | By 08:00 AM T+1 | Batch job monitor | Not completed by 08:00 AM |
| **Regulatory report submission** | Per MOF schedule | Manual tracking + batch monitor | T-2 days before deadline and not started |
| **Document printing delivery** | T+1 for daily batch | Printing partner ACK | Not ACK'd by T+1 18:00 |
| **Commission run completion** | Per schedule (monthly) | Batch job monitor | **Not completed within 24h of expected schedule (R-016)** |
| **Commission accuracy** | 100% match with expected | Reconciliation | **Any deviation from expected range (R-016)** |

### 10.4 Incident Management KPIs

Cross-reference with IM-015 from the incident management backlog:

| KPI | Target | Source |
|-----|--------|--------|
| MTTD (Mean Time to Detect) | < 5 min (P1), < 15 min (P2) | Alert timestamp vs. incident start |
| MTTA (Mean Time to Acknowledge) | Per SLA (15 min P1, 30 min P2) | PagerDuty/OpsGenie |
| MTTR (Mean Time to Resolve) | Per SLA in classification.md | ITSM ticket timestamps |
| Incident SLA adherence | > 95% | ITSM reporting |
| Alert-to-incident ratio | **> 60% of P1/P2 detected by monitoring (Year 1, revised per R-025)** | Compare alert timestamps to incident tickets |
| False positive rate | < 20% | Weekly alert review |
| RCA completion rate | 100% for P1/P2 | ITSM tracking |

> _R-025: Alert-to-incident ratio target revised from 80% to 60% for Year 1. Industry benchmarks for organizations building from near-zero are 40-60% in Year 1. Target 80% as Year 2 goal._

### 10.5 Reporting Cadence

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| **Daily Ops Report** | ITO, IT Manager | Daily 09:00 | Active alerts, overnight batch status, key metrics summary |
| **Weekly Availability Report** | IT Manager, CIO | Weekly Monday | Service availability %, incident count by priority, top issues |
| **Monthly SLA Report** | CIO, Board | Monthly | SLA compliance per service, vendor SLA tracking, trend analysis, capacity forecast |
| **Quarterly Business Metrics** | CIO, COO, CFO | Quarterly | Business KPIs trend, system investment recommendations, risk assessment |
| **Regulatory Availability Report** | Compliance, CIO | Per regulatory schedule | System availability for regulated services, incident impact on policyholders |

---

## 11. Compliance & Audit

### 11.1 Vietnam Regulatory Context

> _R-026, R-027: All regulatory citations below are **pending verification by Legal/Compliance**. These represent the team's current understanding and must not be presented as authoritative until validated. Specific action: send this section to the Compliance team for review before finalizing._

TCLife is regulated by the Vietnam Ministry of Finance (MOF) and the Insurance Supervisory Authority (ISA).

| Requirement Area | Regulatory Basis (PENDING VERIFICATION) | Monitoring Implication |
|-----------------|----------------------------------------|----------------------|
| **Business continuity** | Circular 125/2018/TT-BTC and related MOF guidance on IT risk management for insurers (pending Legal review) | Must demonstrate system availability measurement and incident response capability |
| **Data protection** | Cybersecurity Law 2018, Decree 13/2023/ND-CP on personal data protection (pending Legal review) | Must detect and report data breaches; monitoring must cover access anomalies and data exfiltration signals; **breach notification timelines, data processing logs, and cross-border data transfer monitoring requirements apply (R-027)** |
| **Financial reporting accuracy** | Insurance Law 2022 (amended), Circular 50/2017/TT-BTC (pending Legal review) | Must ensure accuracy of financial data processing — monitoring of GL, NAV, premium, and claims calculations |
| **Operational risk management** | MOF guidelines on operational risk for financial institutions (pending Legal review) | Must demonstrate operational risk controls including system monitoring and incident management |
| **Outsourcing and vendor management** | MOF guidance on outsourcing of critical functions (pending Legal review) | Must independently monitor vendor-managed systems (Insuremo) and track vendor SLA compliance |
| **IT risk management** | **Circular 09/2020/TT-NHNN or insurance-sector equivalent (pending Legal review) (R-027)** | **IT risk management requirements for financial institutions — may mandate specific monitoring and reporting controls** |

> **Action required**: Legal/Compliance team must review this section to: (a) verify citations are correct and currently in force, (b) identify any missing regulations, (c) confirm retention requirements with legal basis, (d) assess data protection implications for the monitoring stack itself (see Section 12).

### 11.2 Audit Trail Requirements

| Audit Need | Monitoring Component | Retention | Regulatory Basis (pending — R-030) |
|-----------|---------------------|-----------|-------------------------------------|
| Who accessed what data | Application access logs -> OpenSearch | 5 years | Pending Legal citation |
| System availability evidence | Prometheus metrics (uptime, SLA) | 3 years (export to S3 for long-term) | Pending Legal citation |
| Incident response records | ITSM tickets + communication logs | 5 years | Pending Legal citation |
| Change and deployment history | CI/CD logs + CloudTrail | 3 years | Pending Legal citation |
| Batch job execution proof | Batch job monitor metrics + logs | 5 years (financial records) | Pending Legal citation |
| Security event history | GuardDuty findings + WAF logs + CloudTrail | 5 years | Pending Legal citation |

> _R-030: Retention periods need mapping to specific regulatory instruments. Legal/Compliance review will provide this._

### 11.3 Compliance Dashboards

> _R-028: Basic compliance dashboard moved to Phase 2 (availability and incident history); full dashboard remains Phase 4._

**Phase 2 — Basic Compliance Dashboard**:
- System availability: Monthly/quarterly availability by regulated service
- Incident history: Timeline of P1/P2 incidents affecting policyholders with resolution time

**Phase 4 — Full Compliance Dashboard**:
- Data breach tracking: Any security events involving policyholder data
- Batch processing evidence: Daily batch completion for GL, regulatory reporting, premium collection
- Vendor SLA compliance: Insuremo availability and performance against contractual SLA
- Regulatory filing status: Countdown to filing deadlines

This dashboard serves as the "evidence pack" for regulatory inquiries and internal/external audits.

### 11.4 Log Retention Architecture

```
  Real-time (0-30 days):  OpenSearch hot storage
  Warm (30-90 days):      OpenSearch warm/cold storage (UltraWarm)
  Archive (90 days-5 years): S3 Glacier + Athena for ad-hoc query
```

Ensure all log pipelines include immutable timestamps and cannot be retroactively modified (use S3 Object Lock for archived logs if required by audit).

---

## 12. Data Protection & PII Policy

> _New section — addresses R-040, R-029, and R-027._

### 12.1 The Risk

Logs and metrics may contain policyholder PII:
- **Policy numbers in URLs** (e.g., `/api/policy/POL-2026-001234`)
- **Customer names in error messages** (e.g., `"Failed to process claim for Nguyen Van A"`)
- **Health data in claims processing logs** (e.g., diagnosis codes, hospital names)
- **Customer IDs in request parameters**
- **Phone numbers, email addresses in authentication logs**

If this data flows into OpenSearch and Grafana, **the monitoring stack itself becomes a PII store** subject to data protection regulation (Decree 13/2023/ND-CP on personal data protection, pending Legal verification).

### 12.2 PII Scrubbing Policy

**Phase 1 deliverable**: Design the PII scrubbing policy (what to scrub, how, where in the pipeline).
**Phase 2 deliverable**: Implement scrubbing before expanding the log pipeline.

| Approach | Implementation | Phase |
|----------|---------------|-------|
| **Log scrubbing at ingestion** | OpenSearch ingest pipeline with regex-based PII detection and masking (e.g., policy numbers, phone numbers, email addresses, national ID patterns) | Phase 2 |
| **Application-level scrubbing** | Logging framework configuration to mask sensitive fields before emission | Phase 2 (part of instrumentation audit) |
| **Dashboard access control** | Restrict access to log dashboards that may contain residual PII (see Section 9.3) | Phase 1 |
| **Structured logging standard** | Define which fields may contain PII and mandate masking in the logging standard | Phase 1 (design), Phase 2 (enforce) |

### 12.3 Data Sovereignty

> _Addresses R-029._

- **AWS Region**: Confirm all monitoring components (AMP, AMG, OpenSearch, S3 archive) are deployed in the same region as production workloads.
- **Cross-border transfer**: If any monitoring data stores are outside Vietnam, assess whether policyholder PII in logs triggers cross-border data transfer requirements under Decree 13/2023/ND-CP (pending Legal review).
- **Phase 1 action**: Document the AWS region for all monitoring components and confirm alignment with data residency requirements.

---

## 13. Training Plan

> _New section — addresses R-032. Training is a Phase 1 deliverable, not a risk-section note._

### 13.1 Skills Gap Assessment

| Skill Area | Current Level | Required Level | Gap |
|-----------|--------------|----------------|-----|
| Prometheus / PromQL | Basic (some team members) | Intermediate (create rules, recording rules, debug queries) | Medium |
| Grafana dashboards | Basic (TV dashboard experience) | Intermediate (build production dashboards, variables, annotations) | Low-Medium |
| OpenSearch / log analysis | Low (logs are reactive) | Intermediate (log-based alerting, query syntax, ingest pipelines) | Medium-High |
| Alertmanager configuration | Low | Intermediate (routing, inhibition, silencing) | Medium |
| AWS managed services (AMP, AMG) | Low | Intermediate (configuration, troubleshooting, cost management) | Medium |
| On-call practices | Low (no formal on-call) | Proficient (incident response, escalation, handoff) | High |

### 13.2 Training Schedule (Phase 1 — Month 1)

| Training | Who | Format | Duration | Budget |
|----------|-----|--------|----------|--------|
| **Prometheus Fundamentals + PromQL** | All 7 staff | AWS training or online course (e.g., PromLabs) | 2-3 days | $500-1,000 per person |
| **Grafana Dashboard Building** | All 7 staff | Hands-on workshop (AWS or partner) | 1-2 days | Included with Prometheus or separate $300-500/person |
| **OpenSearch Fundamentals** | DevOps (3) + Service Quality (1) | AWS training | 2 days | $500-800 per person |
| **On-call and Incident Response** | All 7 staff | Internal workshop + PagerDuty/OpsGenie vendor training | 1 day | Minimal (vendor provides free onboarding) |
| **AWS Managed Monitoring Services** | DevOps (3) | AWS training (AMP, AMG specific) | 1-2 days | $500-800 per person |

**Total training budget estimate**: $3,600-7,200 (one-time)

### 13.3 Ongoing Learning

- **Monthly**: Internal knowledge-sharing session (30 min) — one team member presents a monitoring topic
- **Quarterly**: Review training needs based on phase deliverables; schedule additional training if needed
- **Year 2**: Evaluate advanced training (distributed tracing, SRE practices, chaos engineering)

---

## 14. Roadmap Phases

### Phase 1: Foundation (Months 1-3)

> _Extended considerations per R-033: Phase 1 is dense for 3 months. If the team is overwhelmed, consider extending to 4 months or splitting pre-Phase 1 discovery tasks into a "Phase 0" sprint. Training in Month 1 is a hard prerequisite before implementation starts._

**Goal**: Establish reliable infrastructure monitoring, alerting pipeline, on-call process, and team skills.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Team training** | Prometheus, Grafana, OpenSearch, on-call practices (see Section 13) **(R-032)** | IT Manager + all staff | Training completed in Month 1 |
| **Pre-Phase 1 discovery** | OpenSearch inventory, log volume measurement, Prometheus cardinality **(R-002, R-037)** | DevOps | Discovery report completed |
| **PII scrubbing policy (design)** | Define what PII to scrub, where, and how **(R-040)** | Service Quality + DevOps | Policy document completed |
| **CloudWatch-to-Grafana integration** | Import all CloudWatch metrics (RDS, ALB, S3, SQS, Lambda) into Grafana dashboards | DevOps | All AWS services visible in Grafana |
| **Node and pod alerting** | Complete Prometheus alert rules for node health, pod restarts, OOM, resource saturation | DevOps | Alert rules deployed and tested |
| **EKS version monitoring** | Track EKS cluster version currency **(R-006)** | DevOps | Version check in place; alert at 60 days before EOL |
| **On-call tooling setup** | Select and deploy PagerDuty or OpsGenie; configure Alertmanager integration | App Ops + DevOps | SEV1/SEV2 alerts route to on-call phone |
| **On-call rotation** | Define rotation schedule using 6-person pool, compensation, handoff procedure **(R-008)** | IT Manager + App Ops | Published rotation, first 4 weeks staffed |
| **Alert runbooks** | Write runbook for every Phase 1 alert rule | App Ops | 100% alert-to-runbook coverage |
| **Log pipeline verification** | Verify all application and infrastructure logs flow to OpenSearch; identify gaps | DevOps | Log coverage inventory document |
| **Infrastructure dashboards** | Build Level 2 infrastructure overview + RDS + ALB dashboards in Grafana | DevOps | Dashboards published and reviewed |
| **Synthetic monitoring (basic)** | Deploy blackbox_exporter probes for Sale Portal and Customer Portal login URLs | DevOps | Uptime based on real probe, not `up` metric |
| **Certificate monitoring** | Monitor all TLS certificate expiry dates | DevOps | Alert at 30 and 7 days before expiry |
| **AWS cost monitoring** | CloudWatch billing alarms + AWS Cost Anomaly Detection **(R-004)** | DevOps | Cost spike alerts active |
| **GuardDuty basic integration** | Enable GuardDuty; route High-severity findings to OpenSearch + alert **(R-007)** | DevOps | High-severity GuardDuty findings generate alerts |
| **Dashboard access model** | Define Grafana folder structure and access control **(R-021)** | Service Quality + DevOps | Access model documented and implemented |
| **ITSM tool decision** | Select or confirm approach for incident management tooling **(R-043)** | IT Manager | Decision documented |
| **Baseline documentation** | Document all monitored services, alert rules, thresholds, and dashboard inventory | Service Quality | Living document in `solutions/monitoring-alerting/` |
| **IaC foundation** | Alert rules and dashboard JSON stored in git from the start **(R-035)** | DevOps | All Phase 1 monitoring config in version control |
| **Start business KPI conversations** | Initiate discussions with Finance, Claims, Underwriting on business metric targets **(R-034)** | Service Quality | First meetings scheduled; not blocked for Phase 1 |
| **Monitoring Steering Committee** | Establish governance structure with monthly checkpoints **(R-042)** | IT Manager + CIO | First meeting scheduled |

**Phase 1 exit criteria**:
- Team trained on Prometheus, Grafana, OpenSearch
- All P1-triggering infrastructure conditions have automated alerts
- On-call engineer receives phone alerts for SEV1/SEV2 within 30 seconds
- Infrastructure dashboards show real data for all production services
- Synthetic probes confirm portal reachability every 60 seconds
- PII scrubbing policy designed (implementation in Phase 2)
- AWS cost monitoring active

### Phase 2: Application & Security (Months 4-6)

**Goal**: Extend monitoring to application layer, deploy Insuremo health prober, establish security monitoring baseline, begin RUM.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Application instrumentation audit** | Verify all applications expose HTTP histogram and counter metrics + health endpoints **(R-005)**; remediate gaps | DevOps + App Ops | All apps expose standard metrics + `/health` |
| **Application dashboards** | Build Level 2 + Level 3 dashboards for Sale Portal and Customer Portal | DevOps + App Ops | Per-endpoint latency/error/throughput visible |
| **PII scrubbing implementation** | OpenSearch ingest pipeline + application-level scrubbing **(R-040)** | DevOps | PII masked in log pipeline before expansion |
| **Insuremo Health Prober** | Deploy health prober service with agreed test data **(R-013, R-015)**; expose Prometheus metrics; build Grafana dashboard | DevOps | Insuremo availability and latency visible in Grafana |
| **Insuremo SLA dashboard** | Build Level 1 vendor SLA tracking dashboard | Service Quality | Monthly SLA reporting automated |
| **Log-based alerting** | Configure OpenSearch alerting for: error spikes, exception patterns, auth failures | App Ops + DevOps | At least 10 log-based alert rules active |
| **GuardDuty full integration** | Complete alerting rules for all GuardDuty severity levels | DevOps | GuardDuty findings visible in Grafana/OpenSearch |
| **WAF logging** | Enable WAF logging to OpenSearch; build WAF dashboard | DevOps | WAF block/allow patterns visible |
| **CloudTrail monitoring** | Route high-risk CloudTrail events to OpenSearch alerting (root login, IAM changes, S3 policy changes) | DevOps | Critical IAM events generate alerts |
| **Monitoring stack security** | Restrict network access to Grafana/OpenSearch; enforce MFA; audit log access **(R-041)** | DevOps | Monitoring stack hardened |
| **RUM foundation** | Deploy Grafana Faro on Sale Portal and Customer Portal **(R-003)** | DevOps | RUM data being collected; baseline established |
| **Basic compliance dashboard** | Availability metrics + incident history for regulator queries **(R-028)** | Service Quality | Basic evidence available for auditor/regulator |
| **Status page evaluation** | Evaluate and select status page solution **(R-011)** | App Ops | Decision documented |
| **Alert tuning cycle** | Review all Phase 1 alerts; adjust thresholds; retire false positives | Service Quality | False positive rate < 20% |
| **Operations dashboards** | Build Level 2 alert overview and application health dashboards | App Ops | Operational dashboards in daily use |

**Phase 2 exit criteria**:
- Application-level alerts detect error rate spikes and latency degradation before users report
- Insuremo health prober running in production with 30-day baseline
- Security events from GuardDuty, WAF, and CloudTrail are centralized and alerting
- Log-based alerting catches critical error patterns
- PII scrubbing active in log pipeline
- RUM baseline data available
- Basic compliance evidence available

### Phase 3: Business Metrics & Batch Monitoring (Months 7-9)

**Goal**: Extend monitoring to business processes and batch job operations. This is the phase where monitoring becomes insurance-specific.

> _R-023: Business KPI targets must be validated by business owners before Phase 3 alert thresholds are finalized. Conversations should have started in Phase 1-2 per R-034._

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Batch Job Monitor** | Deploy batch job monitoring service (pull-based, R-018); expose metrics for all batch jobs | DevOps + App Ops | All batch jobs tracked for start/complete/SLA |
| **Commission batch monitoring** | Track commission calculation completion, accuracy, timeliness **(R-016)** | App Ops | Commission run monitored end-to-end |
| **GL batch monitoring** | Track GL file generation, transfer, posting confirmation, **reconciliation (R-019)** daily | App Ops + Finance | GL SLA tracked and alerted |
| **Printing batch monitoring** | Track document generation, file delivery to printing partner, ACK | App Ops | Print partner SLA tracked |
| **Datalake feed monitoring** | Track data freshness and record counts for datalake feeds | DevOps + App Ops | Datalake lag visible and alerted |
| **NAV calculation monitoring** | Track UL NAV calculation completion time and accuracy | App Ops | NAV timeliness alerted by 10:00 AM |
| **Premium collection dashboard** | Build business metrics dashboard for premium collection success, retry, lapse | Service Quality + App Ops | Premium collection health visible |
| **Claims processing dashboard** | Build business metrics dashboard for claims registration-to-payment lifecycle | Service Quality + App Ops | Claims processing time visible |
| **Policy issuance dashboard** | Build business metrics dashboard for policy issuance pipeline | Service Quality + App Ops | Policy issuance latency visible |
| **Financial Operations dashboard** | CFO-facing dashboard: GL, premium, NAV, bank reconciliation **(R-020)** | Service Quality | Validated with CFO |
| **Reconciliation checks** | Implement automated reconciliation for GL, premium, NAV, commission | DevOps + App Ops | Daily reconciliation runs with alerts on mismatch |
| **Regulatory filing countdown** | Calendar-aware component alerting as deadlines approach **(R-017)** | Service Quality | Regulatory deadlines tracked proactively |
| **RUM full deployment** | Dashboards, alerting, geographic segmentation **(R-003)** | DevOps | Real user performance visible across regions |
| **Business Pulse TV dashboard** | Build TV-mode dashboard showing daily business health | App Ops | Displayed in operations area |
| **CIO Management dashboard** | Build Level 1 business health dashboard | Service Quality | CIO can view business processing status in one screen |
| **Status page deployment** | Deploy selected status page solution **(R-011)** | App Ops | External communication channel operational |

**Phase 3 exit criteria**:
- Every daily batch job has automated monitoring with SLA alerting
- Commission batch is tracked and alerted
- Business process KPIs (policy issuance, claims, premium) are visible and trended
- Reconciliation mismatches generate alerts within 2 hours of batch completion
- CIO dashboard provides single-pane view of business + system health
- Regulatory filing countdown active

### Phase 4: Advanced Capabilities (Months 10-12)

**Goal**: Mature the monitoring practice with capacity planning, compliance reporting, automation, and continuous improvement.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Capacity planning dashboards** | Trend-based resource forecasting; predict when current capacity is insufficient | DevOps | Quarterly capacity review uses data-driven forecasts |
| **Anomaly detection** | Deploy statistical anomaly detection on key metrics | DevOps | At least 5 anomaly detection rules active |
| **SLA reporting automation** | Auto-generate monthly SLA reports from Grafana/Prometheus data | Service Quality + DevOps | Monthly SLA report requires < 1 hour of manual effort |
| **Compliance dashboard (full)** | Build audit-grade compliance dashboard with availability evidence, incident history, batch processing proof, regulatory filing status **(R-028)** | Service Quality | Dashboard reviewed and accepted by internal audit |
| **Log retention lifecycle** | Implement hot -> warm -> cold -> archive pipeline in OpenSearch + S3 | DevOps | Logs retained per policy; archive queryable via Athena |
| **Distributed tracing (evaluation)** | Evaluate OpenTelemetry tracing for critical request paths (policy creation, claims submission) | DevOps | Decision document on tracing adoption |
| **Monitoring stack cost tracking** | Track and optimize AWS monitoring costs **(R-004)** | DevOps | Monthly cost report for monitoring services |
| **Runbook automation** | Automate response for top 5 most common alerts (auto-remediation via Lambda or SSM) | DevOps | At least 3 auto-remediation playbooks active |
| **Monitoring-as-Code (full)** | Terraform/CDK for all Grafana dashboards, Prometheus rules, OpenSearch configurations **(R-035 — started Phase 1)** | DevOps | All monitoring config in version control |
| **Process review** | Full review of monitoring effectiveness; update roadmap for Year 2 | All + CIO | Year 2 roadmap drafted |

**Phase 4 exit criteria**:
- Capacity planning prevents resource exhaustion incidents
- Compliance dashboard passes internal audit review
- Monitoring stack costs are tracked and optimized
- All monitoring configuration is in version control (Infrastructure as Code)
- Year 2 roadmap addresses gaps found during Year 1

---

## 15. Cost Considerations

### 15.1 AWS Managed Service Pricing Model

| Service | Pricing Basis | Key Cost Drivers |
|---------|--------------|------------------|
| **Amazon Managed Grafana** | Per active editor/viewer per month ($9/$5) | Number of dashboard users |
| **Amazon Managed Prometheus (AMP)** | Ingestion ($/10M samples), storage ($/GB-month), query ($/10B samples queried) | Metric cardinality, retention period, query frequency |
| **Amazon OpenSearch** | Instance hours + storage (EBS) + UltraWarm/Cold storage | Instance type, storage volume, data retention |
| **CloudWatch** | Metrics ($0.30/metric/month beyond free tier), logs ($0.50/GB ingested), alarms ($0.10/alarm/month) | Number of custom metrics, log volume |
| **PagerDuty/OpsGenie** | Per user per month ($21-49/user for PagerDuty) | Number of on-call responders |
| **AWS Synthetics** | $0.0012/canary run **(R-038)** | Number of canaries and frequency |

### 15.2 Estimated Monthly Cost — AWS Services (Steady State)

| Component | Estimated Monthly Cost (USD) | Notes |
|-----------|---------------------------|-------|
| Amazon Managed Grafana | $100-200 | 5-10 editors, 10-20 viewers |
| Amazon Managed Prometheus | $200-500 | Dependent on metric cardinality and ingestion rate |
| Amazon OpenSearch | $800-2,000 | 3-node cluster + UltraWarm; scales with log volume **(R-037: refine after log volume measurement)** |
| CloudWatch (incremental) | $100-300 | Custom metrics, additional alarms, log insights queries |
| PagerDuty/OpsGenie | $200-500 | 5-10 on-call responders. **Start with Business plan per R-039** |
| **AWS Synthetics** | $150-300 | 5 canaries at per-minute frequency **(R-038)** |
| Insuremo Health Prober (EKS resources) | $50-100 | Small pod, minimal compute |
| Batch Job Monitor (EKS resources) | $50-100 | Small pod, minimal compute |
| S3 archive storage | $50-200 | Long-term log and metric archive |
| **Total AWS estimated** | **$1,700-4,200/month** | |

### 15.3 Estimated Monthly Cost — Human Resources

> _New section — addresses R-036._

| Component | Estimated Monthly Cost (USD) | Notes |
|-----------|---------------------------|-------|
| On-call allowances | $500-1,500 | 6-person rotation; per HR policy |
| Training (amortized over 12 months) | $300-600 | One-time $3,600-7,200 spread over Year 1 |
| External support (Phase 1-2) | $0-3,000 | AWS Professional Services or partner; optional |
| **Total human cost estimated** | **$800-5,100/month** | |

> **Note**: The largest "cost" is the time allocation of existing staff. The staffing plan in Section 2.3 shows the percentage of team time dedicated to monitoring. This is not a new expense — it is a redirection of existing capacity. However, it represents real opportunity cost: time spent on monitoring is time not spent on other projects. The CIO should evaluate this trade-off explicitly.

### 15.4 Total Program Cost

| | Monthly (Steady State) | Annual Estimate |
|-|----------------------|----------------|
| AWS services | $1,700-4,200 | $20,400-50,400 |
| Human costs | $800-5,100 | $9,600-61,200 |
| **Total** | **$2,500-9,300** | **$30,000-111,600** |

### 15.5 Cost Optimization Strategies

| Strategy | Savings Potential | Implementation Phase |
|----------|------------------|---------------------|
| **Prometheus recording rules** | Reduce query cost by pre-aggregating expensive queries | Phase 1 |
| **Metric cardinality management** | Reduce ingestion cost by dropping high-cardinality labels | Phase 2 |
| **OpenSearch UltraWarm tiering** | Reduce hot storage cost by moving aged data to warm/cold | Phase 2 |
| **Log sampling for non-critical services** | Reduce OpenSearch ingestion by sampling verbose logs | Phase 3 |
| **S3 Intelligent-Tiering for archives** | Automatically optimize archive storage class | Phase 4 |
| **Dashboard query optimization** | Reduce Prometheus query cost by optimizing PromQL | Ongoing |
| **Unused metric cleanup** | Remove metrics that no dashboards or alerts reference | Quarterly |

---

## 16. Risks & Dependencies

### 16.1 Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Alert fatigue** | On-call ignores critical alerts due to noise | High (if thresholds are not tuned) | Aggressive tuning in first 30 days per alert; weekly alert review; mandatory runbooks |
| **PII in monitoring data (R-040)** | Monitoring stack becomes uncontrolled PII store subject to data protection regulation | **High** | **PII scrubbing policy in Phase 1; implementation in Phase 2; dashboard access controls; Legal review of monitoring data classification** |
| **Monitoring stack as attack target (R-041)** | Centralized monitoring is high-value target; compromise gives attacker full visibility and ability to suppress alerts | **Medium-High** | **Restrict network access; MFA for Grafana/OpenSearch; audit log access patterns; separate monitoring credentials from production** |
| **Incomplete application instrumentation** | Blind spots in application monitoring; dashboards show incomplete data | Medium | Phase 2 instrumentation audit; define minimum instrumentation standard including health endpoints (R-005) |
| **EbaoTech vendor cooperation** | Vendor may restrict probe frequency, change APIs, or not share maintenance schedules | Medium | Establish vendor monitoring agreement; document probe frequency in contract (R-015); maintain relationship; formalize test data strategy (R-013) |
| **Skills gap** | Team lacks Prometheus/Grafana/OpenSearch expertise to build and maintain | Medium | **Training as Phase 1 deliverable (R-032)**; consider AWS partner support for initial setup |
| **Cost overrun** | Metric cardinality explosion or log volume exceeds estimates | Medium | Cardinality budgets per service; log sampling policies; monthly cost review; **measure current volumes before Phase 1 (R-037)** |
| **Monitoring system as single point of failure** | If Grafana/Prometheus/OpenSearch is down, all visibility is lost | Low-Medium | AMP and AMG are managed services with built-in HA; **CloudWatch Alarms as secondary alerting for P1 conditions (R-012)** |
| **Organizational resistance** | Teams do not adopt monitoring practices, dashboards go stale | Medium | Embed monitoring in incident post-mortems; make dashboards part of daily standup; CIO sponsorship; **Monitoring Steering Committee (R-042)** |
| **Scope creep** | Trying to monitor everything at once delays delivery of core capability | Medium | Strict phase gating; Phase 1 must be complete before Phase 2 starts |
| **Business KPI targets unvalidated (R-023)** | Alert thresholds based on IT assumptions, not business requirements | Medium | **Start business stakeholder conversations in Phase 1-2 (R-034); Phase 3 blocked until sign-off** |
| **Overambitious Phase 1 timeline (R-033)** | 3-month Phase 1 with many deliverables stalls due to daily ops workload | Medium | **Pre-Phase 1 discovery sprint; extend to 4 months if needed; protect DevOps time** |

### 16.2 Dependencies

| Dependency | Required By | Risk if Not Met |
|-----------|-------------|-----------------|
| **On-call budget approval** | Phase 1 (month 1) | Cannot implement after-hours alerting; P1 incidents at night go undetected |
| **PagerDuty/OpsGenie procurement** | Phase 1 (month 1) | Alert routing remains manual; escalation is unreliable |
| **Training budget approval** | Phase 1 (month 1) | Slower adoption; higher error rate in monitoring configuration |
| **Application team cooperation** | Phase 2 (month 4) | Cannot instrument applications; application monitoring remains blind |
| **EbaoTech vendor agreement on probing** | Phase 2 (month 4) | Cannot deploy health prober; core system monitoring remains vendor-dependent |
| **Finance/Operations input on batch SLAs** | **Phase 1-2 start conversations; Phase 3 finalize (R-034)** | Cannot define batch job alert thresholds; monitoring without meaningful thresholds is noise |
| **Compliance team input on retention** | Phase 2 (basic), Phase 4 (full) **(R-028)** | Log retention may not meet regulatory requirements; audit risk |
| **ITSM tool selection** | **Phase 1 decision (R-043)** | Monitoring-to-incident integration blocked |
| **Legal/Compliance review of regulatory citations** | **Before document finalization (R-026, R-027)** | Credibility risk if incorrect citations presented to auditors |
| **CIO sponsorship** | All phases | Without executive backing, cross-team coordination stalls |

### 16.3 Governance

> _Addresses R-042._

**Monitoring Steering Committee**:
- **Chair**: IT Manager
- **Executive sponsor**: CIO
- **Members**: App Ops lead, DevOps lead, Service Quality, representatives from Finance and Operations (as needed)
- **Cadence**: Monthly
- **Agenda**: Phase progress review, blocker resolution, staffing issues, cross-team coordination, budget tracking

### 16.4 Open Questions

| Question | Needs Answer From | Impact |
|---------|-------------------|--------|
| What is the exact EbaoTech API contract for health probing? | Vendor/Integration team | Determines health prober design |
| Do we have an existing on-call policy/compensation framework? | HR/IT Manager | Determines Phase 1 timeline for on-call setup |
| What are the contractual SLA targets with EbaoTech? | Vendor Manager/Legal | Determines Insuremo SLA dashboard thresholds |
| What is the current log volume (GB/day) in OpenSearch? | DevOps (pre-Phase 1) | Determines OpenSearch sizing and cost estimate accuracy |
| Which batch jobs currently have monitoring? (Any?) | App Ops | Determines Phase 3 starting point |
| Are there existing regulatory reporting requirements for system availability? | Compliance | Determines compliance dashboard priority |
| What is the current Prometheus metric cardinality? | DevOps (pre-Phase 1) | Determines AMP cost estimate accuracy |
| **What is the AWS region for all monitoring components?** **(R-029)** | DevOps | Determines data sovereignty compliance |
| **Does the CFO need a dedicated financial operations dashboard?** **(R-020)** | CFO | Determines Phase 3 dashboard scope |

---

## 17. CIO Review Findings — Resolution Matrix

This section maps every CIO review finding (R-001 through R-043) to its resolution in this v2.0 document.

### High Severity

| ID | Finding | Resolution | Section |
|----|---------|------------|---------|
| R-003 | Missing: Real User Monitoring (RUM) | Added as new monitoring domain; Grafana Faro; Phase 2 foundation, Phase 3 full | 4.7, 14 |
| R-004 | Missing: AWS Cost Monitoring | Added as new monitoring domain; Phase 1 billing alarms + Cost Anomaly Detection | 4.8, 14 |
| R-016 | Missing: Commission batch monitoring | Added to batch job landscape, alert rules, reconciliation | 8.1, 8.3, 8.5 |
| R-023 | Business KPI targets need validation | Targets marked "pending validation"; business conversations start Phase 1-2; Phase 3 blocked until sign-off | 10.3 |
| R-026 | Regulatory citations need Legal verification | All citations marked "PENDING VERIFICATION"; action item to send to Legal/Compliance | 11.1 |
| R-027 | Missing regulatory references (data protection, IT risk management) | Added Decree 13/2023/ND-CP personal data protection and Circular 09/2020/TT-NHNN references (pending verification); new PII section | 11.1, 12 |
| R-031 | No staffing plan | Full team structure (7 people), role mapping, per-phase allocation, on-call rotation | 2 |
| R-032 | Training must be Phase 1 deliverable | New training plan section; training in Month 1; budget estimate | 13, 14 |
| R-036 | Human costs missing from cost model | Human cost section added: on-call allowances, training, external support, opportunity cost | 15.3 |
| R-040 | Missing risk: PII in monitoring data | New Data Protection & PII Policy section; scrubbing policy Phase 1 (design), Phase 2 (implement) | 12 |

### Medium Severity

| ID | Finding | Resolution | Section |
|----|---------|------------|---------|
| R-001 | Security maturity target overambitious | Revised from 2.5 to 2.0 (12-month target); 2.5 as stretch goal | 3.3 |
| R-005 | Health check endpoint standardization missing | Added `/health` endpoint to instrumentation standard | 4.4 |
| R-006 | EKS cluster version monitoring missing | Added EKS version metric and alert | 4.2, 14 |
| R-008 | On-call needs minimum team size | Documented 6-person pool (3 App Ops + 3 DevOps); 6-week rotation cycle | 2.2 |
| R-009 | Escalation: CTO vs CIO | Corrected to CIO in all escalation references | 5.2 |
| R-011 | Status page missing | Added to tool stack; evaluate Phase 2, deploy Phase 2-3 | 6.5, 14 |
| R-013 | Test data strategy for Insuremo prober | Documented designated test dataset approach; vendor coordination | 7.2.2 |
| R-014 | Result hash alert threshold undefined | Defined per-query-type expected change frequency and alert logic | 7.2.3 |
| R-017 | Regulatory filing calendar monitoring | Added regulatory filing countdown with calendar-aware alerting | 8.6 |
| R-018 | Pushgateway anti-pattern | Batch Job Monitor uses pull-based `/metrics` endpoint; Pushgateway reserved for ephemeral Lambda jobs only | 8.3 |
| R-020 | CFO/Finance may need dedicated dashboard | Financial Operations dashboard added to Level 1; validate with CFO | 9.2 |
| R-024 | Differential SLA targets need rationale | Documented rationale; flagged Customer Portal for regulatory SLA review | 10.1 |
| R-025 | Alert-to-incident ratio 80% overambitious | Revised to 60% Year 1; 80% Year 2 target | 10.4 |
| R-028 | Compliance dashboard too late (Phase 4) | Basic compliance dashboard moved to Phase 2; full remains Phase 4 | 11.3, 14 |
| R-029 | Data sovereignty: AWS region and PII in logs | Addressed in PII section; Phase 1 action to document AWS region | 12.3 |
| R-033 | Phase 1 too dense for 3 months | Pre-Phase 1 discovery acknowledged; extend to 4 months if needed | 14 |
| R-034 | Business SLA conversations should start earlier | Moved to Phase 1-2 (start conversations), not Phase 3 | 14, 16.2 |
| R-037 | OpenSearch cost unreliable without log volume | Pre-Phase 1 discovery task added; cost estimate flagged as pending | 3.4, 15.2 |
| R-038 | Synthetic monitoring cost (AWS Synthetics) missing | Added AWS Synthetics cost line item ($150-300/month) | 15.2 |
| R-041 | Monitoring stack as attack target | Added as risk; mitigation in Phase 2 deliverables | 4.6, 16.1, 14 |
| R-042 | Monitoring Steering Committee recommended | Governance section added with committee structure | 16.3 |

### Low Severity

| ID | Finding | Resolution | Section |
|----|---------|------------|---------|
| R-002 | Resolve OpenSearch scope before Phase 1 | Pre-Phase 1 discovery task | 3.4 |
| R-007 | Pull GuardDuty into late Phase 1 | Basic GuardDuty integration added to Phase 1 | 4.6, 14 |
| R-010 | Alertmanager repeat_interval should be severity-based | YAML updated with severity-based routing | 5.5 |
| R-012 | DR plan for monitoring stack | Monitoring stack resilience section with CloudWatch fallback | 6.4 |
| R-015 | Vendor sign-off on probe frequency | Documented as Phase 2 prerequisite | 7.2.7 |
| R-019 | Add "Reconciled" state to file lifecycle | Added as 6th monitoring dimension and to file lifecycle diagram | 8.2, 8.4 |
| R-021 | Dashboard access control model | Access control matrix defined; Phase 1 deliverable | 9.3 |
| R-022 | JS error metrics require RUM infrastructure | Noted dependency on RUM (Phase 2) | 4.7 |
| R-030 | Retention periods need regulatory citation | Retention table updated with "pending Legal citation" | 11.2 |
| R-035 | Start IaC in Phase 1, not Phase 4 | IaC foundation added to Phase 1; full migration in Phase 4 | 14 |
| R-039 | Start with PagerDuty Business plan | Noted in cost section | 15.2 |
| R-043 | ITSM tool selection should be Phase 1 | Moved to Phase 1 decision | 14 |

---

## 18. Appendix: Cross-References to Existing Work

This roadmap builds on and connects to several existing documents in the TCLife workspace:

| Document | Location | Relationship |
|----------|----------|-------------|
| **Grafana TV Dashboard Review** | `solutions/dashboards/grafana-tv-dashboard-review.md` | Phase 1 TV dashboard is an extension of this existing work; PromQL patterns are reusable |
| **Grafana Dashboard Implementation Notes** | `solutions/dashboards/grafana-dashboard-implementation-notes.md` | Implementation guidance for dashboard deployment; namespace and metric name mapping |
| **Incident Classification** | `solutions/incident-management/classification.md` | Alert severity levels (Section 5) are aligned with incident priority matrix (P1-P4) |
| **Incident Management Backlog** | `solutions/incident-management/backlog.md` | This roadmap addresses: IM-005 (on-call model), IM-009 (tooling specification), IM-015 (metrics/KPIs) |
| **ITO Capability Declaration** | `solutions/ito-responsible/capability-declaration.md` | Section 2.7 (Monitoring & Alerting) and 2.13 (Reporting) define ITO's monitoring responsibilities; this roadmap operationalizes them |
| **Incident Scenarios** | `solutions/incident-management/scenarios.md` | Business scenarios (e.g., 347 policies with zero surrender value) inform which business metrics to monitor |
| **L1 Support Frontline** | `solutions/L1-support-frontline/l1-support-frontline.md` | L1 uses monitoring dashboards for incident detection and triage; dashboard design must support L1 workflows |
| **CIO Review** | `solutions/monitoring-alerting/cio-review-monitoring-roadmap.md` | 43 findings incorporated in v2.0; resolution matrix in Section 17 |

### Incident Management Backlog Items Addressed

| Backlog ID | Item | How This Roadmap Addresses It |
|-----------|------|------------------------------|
| IM-004 | Customer communication plan | Status page for external communication (R-011, Section 6.5) |
| IM-005 | On-call and after-hours coverage model | Section 2.2 and 5.3 define on-call rotation with 7-person team |
| IM-009 | Incident management tooling specification | Section 6 specifies monitoring stack; ITSM tool selection is Phase 1 decision |
| IM-015 | Metrics and KPI framework | Section 10 defines comprehensive KPIs with targets and measurement approach |
| IM-018 | Vendor management integration | Section 7 defines Insuremo vendor SLA tracking and incident attribution |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | IT Operations | Initial draft |
| 2.0 | 2026-03-20 | IT Operations | Restructured into overview + detail; incorporated 43 CIO review findings; added: team structure (7 people), staffing plan, training plan, RUM, cost monitoring, commission batch, PII scrubbing policy, human costs, regulatory citation qualification, governance structure. Full resolution matrix in Section 17. |
