# Monitoring & Alerting Roadmap — TCLife

> **Version**: 1.0
> **Date**: 2026-03-20
> **Author**: IT Operations
> **Status**: Draft — pending CIO review
> **Audience**: CIO, IT Operations, Infrastructure Team, Application Support, Management

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current State Assessment](#2-current-state-assessment)
3. [Monitoring Strategy](#3-monitoring-strategy)
4. [Alerting Strategy](#4-alerting-strategy)
5. [Tool Mapping](#5-tool-mapping)
6. [EbaoTech Insuremo Integration](#6-ebaotech-insuremo-integration)
7. [Batch Job & File Exchange Monitoring](#7-batch-job--file-exchange-monitoring)
8. [Dashboard Strategy](#8-dashboard-strategy)
9. [Key Metrics & KPIs](#9-key-metrics--kpis)
10. [Compliance & Audit](#10-compliance--audit)
11. [Roadmap Phases](#11-roadmap-phases)
12. [Cost Considerations](#12-cost-considerations)
13. [Risks & Dependencies](#13-risks--dependencies)
14. [Appendix: Cross-References to Existing Work](#14-appendix-cross-references-to-existing-work)

---

## 1. Executive Summary

TCLife operates a fully AWS-hosted life insurance platform serving policyholders, sales agents, and internal operations across Unit-Linked (UL), Critical Illness (CI), Health Insurance (HI), and Medical Reimbursement (MR) product lines. The core insurance system (EbaoTech Insuremo) is vendor-managed, and the company exchanges batch files with partners for printing, general ledger (GL), and datalake integrations.

Today, TCLife has foundational monitoring components in place — Amazon Managed Grafana, Amazon Managed Service for Prometheus (AMP), and Amazon OpenSearch Service — but lacks a unified, layered monitoring strategy that covers infrastructure, application, business process, and security dimensions. The existing Grafana TV dashboard work (see `solutions/dashboards/`) covers EKS health metrics but does not extend to business-critical flows such as policy issuance, claims processing, premium collection, or the vendor-managed core system.

This roadmap defines a **four-phase implementation plan** to build a comprehensive monitoring and alerting capability. The phases are designed to deliver incremental value: Phase 1 establishes foundational infrastructure monitoring, Phase 2 extends to application-level observability, Phase 3 adds insurance-specific business metrics, and Phase 4 introduces advanced capabilities including predictive alerting, capacity planning, and audit-grade reporting.

**Target state**: Every P1/P2 incident is detected by monitoring before users report it. Every business-critical batch job is tracked for timeliness and success. The CIO has a single dashboard showing system health, SLA compliance, and business processing status.

---

## 2. Current State Assessment

### 2.1 What We Have

| Component | Status | Coverage |
|-----------|--------|----------|
| **Amazon Managed Grafana** | Active | EKS TV dashboard (4 systems), basic health/latency/error panels |
| **Amazon Managed Service for Prometheus (AMP)** | Active | Container metrics via kube-state-metrics, cAdvisor; application metrics where instrumented |
| **Amazon OpenSearch Service** | Active | Log aggregation (scope and completeness unknown) |
| **EbaoTech Insuremo** | Vendor-managed | Separate monitoring stack; TCLife has realtime query/search access only |
| **CloudWatch** | Active (inherent to AWS) | AWS service metrics, EKS control plane, ALB, RDS, S3, Lambda |
| **Grafana TV Dashboard** | Implemented | Per-system health, uptime/SLA gauge, P95 latency, error rate, throughput, CPU/memory, critical alerts |

### 2.2 Known Gaps

| Gap Area | Description | Risk |
|----------|-------------|------|
| **No business-process monitoring** | No dashboards or alerts for policy issuance latency, claims processing throughput, premium collection success, NAV calculation, or surrender value computation | Silent P1 incidents — business logic errors that produce wrong financial outcomes with no alert |
| **No batch job monitoring** | GL file exchange, printing partner files, datalake feeds — no tracking of job success/failure, file arrival time, or reconciliation | Missed SLA deadlines, undetected data gaps, regulatory reporting failures |
| **No EbaoTech Insuremo health visibility** | Vendor monitors their own stack; TCLife has no independent view of core system responsiveness, API health, or data freshness | Total dependency on vendor notification; no ability to detect degradation proactively |
| **Limited application instrumentation** | Prometheus scraping exists for EKS workloads, but coverage of HTTP histograms, custom business counters, and distributed traces is inconsistent | Latency P95 and error rate panels may show incomplete data |
| **No structured log alerting** | OpenSearch collects logs but no systematic alerting on error patterns, exception spikes, or security events | Logs are reactive (searched after an incident) rather than proactive |
| **No security monitoring integration** | No SIEM, no GuardDuty alerting pipeline, no WAF logging dashboards | Security incidents rely on manual discovery; gaps identified in IM-002 of the incident management backlog |
| **No on-call alerting pipeline** | Alert rules exist in Prometheus/Alertmanager, but no integration with PagerDuty/OpsGenie for after-hours escalation | After-hours P1 incidents have no automated wake-up mechanism (gap IM-005) |
| **No SLA measurement system** | Uptime/SLA gauge on TV dashboard uses `avg_over_time(up[30d])` — measures scrape availability, not user-facing service availability | SLA reporting does not reflect actual policyholder or agent experience |
| **No synthetic monitoring** | No external probes testing login flows, quote creation, or portal availability from outside the VPC | Cannot distinguish between "system is up" and "users can actually transact" |
| **Incomplete CloudWatch integration** | CloudWatch metrics for managed AWS services (RDS, S3, SQS, Lambda) are not pulled into Grafana/Prometheus dashboards | Blind spots on database performance, queue depths, storage, and serverless workloads |

### 2.3 Maturity Assessment

Using a simple maturity model (1 = Ad-hoc, 2 = Reactive, 3 = Proactive, 4 = Managed, 5 = Optimized):

| Domain | Current Level | Target Level (12 months) |
|--------|--------------|--------------------------|
| Infrastructure monitoring | 2.5 — EKS metrics collected, basic dashboards | 4 — Full stack with alerting and capacity planning |
| Application monitoring | 1.5 — Partial instrumentation, no distributed tracing | 3 — Instrumented services, log-based alerting, error tracking |
| Business process monitoring | 1 — No monitoring of business flows | 3 — Key business KPIs tracked and alerted |
| Security monitoring | 1 — No SIEM, no automated detection | 2.5 — GuardDuty, WAF logs, basic threat detection |
| Batch/file monitoring | 1 — Manual checking | 3 — Automated tracking with SLA alerts |
| Alerting & escalation | 1.5 — Basic Alertmanager, no on-call integration | 3.5 — Tiered alerting with on-call rotation |
| Reporting & compliance | 1 — No systematic reporting | 3 — Automated SLA and availability reports |

---

## 3. Monitoring Strategy

### 3.1 Layered Monitoring Model

TCLife's monitoring must cover four distinct layers. Each layer answers a different question:

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
```

### 3.2 Layer 1 — Infrastructure Monitoring

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

### 3.3 Layer 2 — Platform / Middleware Monitoring

**Scope**: Message queues, caching layers, API gateways, service mesh (if any), DNS resolution, certificate expiry.

| What to Monitor | Why | Tool |
|----------------|-----|------|
| Message queue consumer lag | Backlog buildup means processing is behind | Prometheus custom metrics or CloudWatch |
| Cache hit/miss ratio | Cache degradation causes latency spikes | Prometheus (ElastiCache metrics via CloudWatch exporter) |
| API Gateway latency and error rates | Gateway is the front door for all API traffic | CloudWatch + Prometheus |
| TLS certificate expiry | Expired certs cause outages | Prometheus blackbox_exporter or cert-manager metrics |
| DNS resolution time | DNS failures are silent killers | Prometheus blackbox_exporter |
| Secrets rotation status | Expired credentials cause auth failures | Custom metric from Secrets Manager events |

### 3.4 Layer 3 — Application Monitoring

**Scope**: All TCLife-owned applications — Sale Portal, Customer Portal, middleware/integration services, batch processing applications.

**Instrumentation standard**: All applications MUST expose:
- HTTP request duration histogram (`http_request_duration_seconds_bucket`)
- HTTP request counter by status code (`http_requests_total`)
- Custom business event counters (per application)
- Structured JSON logging to OpenSearch

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

**Distributed tracing** (future consideration): Instrument with OpenTelemetry for request tracing across services. Not in Phase 1-2 scope, but the instrumentation standard should be OTel-compatible from the start.

### 3.5 Layer 4 — Business Process Monitoring

**Scope**: Insurance-specific business flows that directly impact policyholders, agents, and regulatory compliance.

This is where most life insurance companies have the biggest monitoring gap. Infrastructure can be green while business processes are silently broken.

| Business Process | What to Monitor | Why |
|-----------------|----------------|-----|
| **Policy issuance** | End-to-end time from submission to policy activation; conversion rate; rejection rate by reason | Agents blocked = revenue impact; SLA to policyholders |
| **Claims processing** | Claim registration to assessment time; assessment to payment time; auto-approval rate; rejection rate | Regulatory SLA; policyholder experience; fraud detection signal |
| **Premium collection** | Collection success rate; failed payment retry rate; grace period utilization; lapse rate | Revenue assurance; policyholder retention |
| **UL NAV calculation** | NAV calculation completion time; variance from expected; fund price freshness | Regulatory requirement; policyholder statements depend on accurate NAV |
| **Surrender value** | Calculation accuracy (compare with actuarial baseline); batch completion | Scenario from IM backlog — 347 policies with zero surrender value |
| **Quotation engine** | Quote generation time; quote-to-proposal conversion rate | Agent productivity; system responsiveness |
| **Document generation** | Document generation success rate; printing partner file delivery timeliness | Policyholder communication; regulatory filings |
| **Regulatory reporting** | Report generation completion; data freshness; submission timeliness | MOF compliance; audit trail |
| **Reinsurance data** | Cession data generation timeliness; reconciliation status | Treaty compliance; financial accuracy |

### 3.6 Security Monitoring

**Scope**: Threat detection, access anomalies, data exfiltration, compliance violations.

| What to Monitor | Tool | Priority |
|----------------|------|----------|
| AWS GuardDuty findings | CloudWatch Events -> OpenSearch | Phase 2 |
| WAF blocked requests and rate limiting | AWS WAF logs -> OpenSearch | Phase 2 |
| IAM anomalies (root login, new admin users, policy changes) | CloudTrail -> OpenSearch | Phase 2 |
| Failed authentication attempts (brute force) | Application logs -> OpenSearch | Phase 2 |
| S3 public access or policy changes | CloudTrail -> OpenSearch + Config Rules | Phase 2 |
| Unusual database query patterns | RDS audit logs -> OpenSearch | Phase 3 |
| Data exfiltration signals (large data exports) | VPC Flow Logs + S3 access logs | Phase 3 |
| Certificate and key usage anomalies | CloudTrail -> OpenSearch | Phase 3 |

---

## 4. Alerting Strategy

### 4.1 Severity Levels

Alerting severity aligns with the incident classification system defined in `solutions/incident-management/classification.md`:

| Alert Severity | Maps to Incident Priority | Response Expectation | Examples |
|---------------|--------------------------|---------------------|----------|
| **SEV1 — Critical** | P1 | Immediate page; 15-min response | Core system down, data breach detected, all users blocked, financial data corruption |
| **SEV2 — Major** | P2 | Urgent notification; 30-min response | Significant degradation, key function unavailable, batch job SLA at risk |
| **SEV3 — Warning** | P3 | Business hours notification; 2-hr response | Elevated error rate, capacity approaching threshold, single-service degradation |
| **SEV4 — Info** | P4 / no incident | Logged for review; no immediate action | Transient anomaly, below-threshold metric deviation, informational event |

### 4.2 Alert Routing and Notification Channels

| Severity | Primary Channel | Secondary Channel | Escalation |
|----------|----------------|-------------------|------------|
| **SEV1** | PagerDuty/OpsGenie (on-call engineer) | Slack #incidents + SMS to IC and IT Manager | Auto-escalate to CTO at 15 min if unacknowledged |
| **SEV2** | PagerDuty/OpsGenie (on-call engineer) | Slack #incidents | Auto-escalate to IT Manager at 30 min if unacknowledged |
| **SEV3** | Slack #monitoring-alerts | Email to team lead | Review in daily standup if unresolved |
| **SEV4** | Slack #monitoring-info (low-priority channel) | None | Weekly review |

### 4.3 On-Call Model

This directly addresses gap IM-005 from the incident management backlog.

**Proposed rotation**:
- **Primary on-call**: 1 infrastructure engineer + 1 application engineer, rotating weekly
- **Secondary on-call**: Team lead / senior engineer as escalation
- **Hours**: 24/7 for SEV1, business hours only for SEV2-4
- **Tooling**: PagerDuty or OpsGenie (to be selected in Phase 1)
- **Compensation**: Per company HR policy (on-call allowance)
- **Handoff**: 09:00 daily with a 15-minute verbal handoff covering active alerts, recent incidents, and pending items

### 4.4 Alert Quality Principles

Poor alerting is worse than no alerting — alert fatigue leads to ignored critical alerts.

| Principle | Implementation |
|-----------|---------------|
| **Every alert must be actionable** | If no human action is required, it is a log entry, not an alert |
| **Alert on symptoms, not causes** | Alert on "error rate > 5%" not "CPU > 80%" (unless CPU directly causes user impact) |
| **Tune aggressively in first 30 days** | Every new alert gets a 30-day review; adjust thresholds based on actual behavior |
| **No duplicate alerts** | Suppress child alerts when parent alert fires (e.g., don't alert on every pod restart when the node is down) |
| **Alert routing matches responsibility** | Infrastructure alerts go to infra on-call; application alerts go to app on-call |
| **Document every alert** | Each alert rule has a linked runbook explaining: what it means, what to check, how to resolve |
| **Weekly alert review** | Review all alerts from the past week; identify false positives, tune, or retire |

### 4.5 Alert Inhibition and Grouping

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
repeat_interval: 4h  # SEV1: 1h, SEV2: 4h, SEV3: 12h
```

---

## 5. Tool Mapping

### 5.1 Tool Responsibilities

| Tool | Primary Role | Data Types | Retention |
|------|-------------|------------|-----------|
| **Prometheus (AMP)** | Metrics collection, alerting rules, recording rules | Time-series numeric metrics | 150 days (AMP default) |
| **Grafana (AMG)** | Visualization, dashboards, unified query interface | Renders data from all sources | N/A (dashboards are config) |
| **OpenSearch** | Log aggregation, log-based alerting, security event analysis | Structured/unstructured logs, traces | 30-90 days hot, archive to S3 |
| **CloudWatch** | AWS service metrics, CloudTrail events, billing alerts | AWS-native metrics and logs | Per metric class (default varies) |
| **PagerDuty/OpsGenie** | On-call management, alert routing, escalation | Alert state, acknowledgements, incidents | Per vendor plan |

### 5.2 Data Flow Architecture

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
              │   counters        │ │ - Trace data      │ │ - Billing         │
              │ - Recording rules │ │                   │ │                   │
              │ - Alerting rules  │ │ - Log-based alerts│ │ - CloudWatch      │
              │        │          │ │                   │ │   Alarms          │
              │        ▼          │ │                   │ │                   │
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

### 5.3 Monitoring Domain to Tool Matrix

| Monitoring Domain | Prometheus | OpenSearch | CloudWatch | Notes |
|-------------------|:----------:|:----------:|:----------:|-------|
| EKS node/pod health | **Primary** | | Secondary | kube-state-metrics, cAdvisor |
| Application latency/errors/throughput | **Primary** | Secondary (logs) | | Requires app instrumentation |
| Application logs and error patterns | | **Primary** | | Structured JSON logs |
| RDS performance | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| S3/SQS/Lambda metrics | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| ALB/NLB metrics | | | **Primary** | CloudWatch exporter to Prometheus for Grafana |
| EbaoTech Insuremo health | **Primary** (custom probes) | Secondary (query logs) | | Custom exporter (see Section 6) |
| Batch job status | **Primary** (custom metrics) | **Primary** (job logs) | | Dual: metrics for status, logs for detail |
| Security events (GuardDuty, WAF) | | **Primary** | Secondary | CloudWatch Events -> OpenSearch |
| IAM/CloudTrail audit | | **Primary** | Secondary | CloudTrail -> OpenSearch |
| Business process metrics | **Primary** (counters/gauges) | Secondary (event logs) | | Custom instrumentation required |
| Certificate/DNS health | **Primary** (blackbox_exporter) | | | External probe approach |
| Cost and billing | | | **Primary** | CloudWatch billing metrics |

---

## 6. EbaoTech Insuremo Integration

### 6.1 The Challenge

EbaoTech Insuremo is vendor-managed. TCLife cannot install agents, export metrics, or access the internal monitoring stack. The only interface is realtime query/search access — we can call the system's APIs and query its database, but we cannot instrument it.

This is a common pattern in insurance IT: the core policy administration system (PAS) is a black box from a monitoring perspective.

### 6.2 Monitoring Strategy for a Vendor-Managed Core System

**Approach: External Observation + Data Freshness + SLA Tracking**

We monitor the system from the outside — through the interfaces we control.

#### 6.2.1 API Health Probes

Deploy a dedicated **Insuremo Health Prober** service (lightweight, runs on EKS) that periodically calls Insuremo APIs and records response metrics.

```
Insuremo Health Prober (EKS pod)
  │
  ├── Every 30s: Call /api/health or equivalent health endpoint
  │   → Record: response_time, status_code, success/failure
  │
  ├── Every 60s: Execute lightweight read-only business queries
  │   → Policy lookup by known test policy number
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

#### 6.2.2 Integration Point Monitoring

Every integration between TCLife systems and Insuremo is a monitoring point:

| Integration | What to Monitor | Alert Condition |
|------------|----------------|-----------------|
| Policy creation API | Call latency, success rate, error codes | Latency > 5s or error rate > 1% |
| Premium calculation API | Call latency, result validation | Latency > 3s or unexpected results |
| Claims submission API | Call latency, success rate | Latency > 5s or error rate > 1% |
| Product/rate retrieval | Response time, data staleness | Data unchanged for > 24h (should update daily) |
| Fund price feed (UL) | Price freshness, variance from market | Price older than 4 hours during trading hours |
| Policyholder data sync | Record count, sync latency | Sync gap > 30 min |

#### 6.2.3 SLA Tracking

Maintain a formal SLA tracking dashboard for Insuremo based on the vendor contract:

| SLA Metric | Target | Measurement | Reporting |
|-----------|--------|-------------|-----------|
| API availability | 99.9% (contractual) | `avg_over_time(insuremo_api_up[30d])` | Monthly |
| API response time (P95) | < 3s (contractual) | `histogram_quantile(0.95, ...)` | Weekly |
| Data freshness (policy) | < 15 min during business hours | `insuremo_data_freshness_seconds{entity="policy"}` | Continuous |
| Incident resolution time | Per vendor SLA | Manual tracking (ITSM ticket) | Monthly |
| Planned maintenance windows | Agreed schedule | Calendar tracking | Monthly |

#### 6.2.4 Vendor Communication Protocol

When the health prober detects degradation:

1. **Auto-alert** fires to TCLife on-call (SEV2+)
2. **TCLife on-call** validates the issue is not on TCLife side
3. **Contact vendor** through agreed escalation channel with: timestamp, affected endpoint, error details, impact scope
4. **Track in ITSM** as vendor-related incident
5. **Update SLA log** with incident details for monthly review

### 6.3 Limitations to Acknowledge

- We cannot monitor Insuremo's internal performance (DB queries, queue depths, memory usage)
- We depend on vendor notification for planned maintenance and known issues
- Our probes test the API contract, not the full system; internal degradation that does not yet affect API responses will be invisible
- Probe traffic must be discussed with the vendor to avoid being rate-limited or flagged

---

## 7. Batch Job & File Exchange Monitoring

### 7.1 Batch Job Landscape

TCLife exchanges files with external partners and runs internal batch processes:

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

### 7.2 Monitoring Framework for Batch Jobs

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
  └──────────────────────────────────────────────────────┘
```

### 7.3 Implementation Pattern: Batch Job Exporter

Deploy a **Batch Job Monitor** service that tracks all batch jobs and exposes metrics:

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

**Alert rules**:

| Alert | Condition | Severity |
|-------|-----------|----------|
| Batch job did not start | `time() - batch_job_last_run_timestamp > expected_interval * 1.5` | SEV2 |
| Batch job failed | `batch_job_status == 0` | SEV2 (GL, regulatory) / SEV3 (others) |
| Batch job SLA breach | `batch_file_arrival_delay_seconds > sla_threshold` | SEV2 |
| Record count anomaly | `batch_job_records_processed` deviates > 30% from rolling average | SEV3 |
| File size anomaly | `batch_file_size_bytes` deviates > 50% from rolling average | SEV3 |
| Zero records processed | `batch_job_records_processed == 0` when expected > 0 | SEV2 |
| Partner acknowledgment missing | No ACK within expected window | SEV3 |

### 7.4 File Exchange Monitoring Pattern

For file-based integrations, implement a file watcher that tracks the lifecycle:

```
FILE LIFECYCLE:
  Generated -> Validated -> Transferred -> Acknowledged
      │            │            │              │
      ▼            ▼            ▼              ▼
   Timestamp   Checksum     Transfer        ACK file
   Record cnt  Validation   confirmation    or API
   File size   result       (S3 event,      confirmation
                            SFTP log)
```

**S3-based file exchange monitoring** (most TCLife partners likely use S3):
- S3 Event Notifications -> Lambda -> Prometheus Pushgateway -> AMP
- Track: file arrival time, file size, file name pattern compliance
- Alert on: missing expected file, unexpected file, file size anomaly

### 7.5 Reconciliation Monitoring

For each batch exchange, implement automated reconciliation checks:

| Reconciliation Type | Check | Frequency | Alert On |
|--------------------|-------|-----------|----------|
| GL record count | Records sent vs. records posted in GL | Daily | Mismatch > 0 |
| Premium collection | Payments collected vs. bank settlement | Daily | Variance > threshold |
| Print job status | Documents sent vs. partner print confirmation | Daily | Unconfirmed after 24h |
| Datalake freshness | Last record timestamp in datalake vs. source | Hourly | Lag > 2 hours |
| NAV values | Published NAV vs. expected NAV from fund manager | Daily | Variance > 0.01% |

---

## 8. Dashboard Strategy

### 8.1 Dashboard Hierarchy

Dashboards serve different audiences with different information needs:

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

### 8.2 Dashboard Inventory

#### Level 1: CIO / Management Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Business Health** | Policy issuance rate, claims processing time, premium collection success, portal uptime SLA | 5 min | CIO, COO, CFO |
| **Service Availability** | Per-service uptime (30-day rolling), SLA status (met/at-risk/breached), major incident timeline | 5 min | CIO, IT Manager |
| **Vendor SLA** | Insuremo availability, API latency trend, vendor incident count, SLA compliance | 15 min | CIO, Vendor Manager |
| **Batch Job Status** | Daily batch completion matrix (green/yellow/red per partner), SLA adherence trend | 15 min | CIO, Operations |

#### Level 2: Operations Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Infrastructure Overview** | EKS cluster health, RDS performance, ALB metrics, resource utilization | 1 min | ITO, Infra team |
| **Application Health** | Per-application latency/error/throughput, top slow endpoints, error log stream | 1 min | ITO, App support |
| **Batch Job Operations** | Per-job timeline (expected vs. actual), failure detail, file sizes, reconciliation status | 5 min | ITO, Operations |
| **Alert Overview** | Active alerts by severity, alert history (24h), top flapping alerts, alert response time | 1 min | ITO, On-call |
| **Insuremo Health** | API response times, endpoint availability, data freshness gauges, SLA tracking | 1 min | ITO, Integration team |
| **Security Overview** | GuardDuty findings, WAF blocks, failed auth attempts, CloudTrail anomalies | 5 min | ITO, Security |

#### Level 3: Engineering / Debug Dashboards

| Dashboard | Key Panels | Refresh | Audience |
|-----------|-----------|---------|----------|
| **Sale Portal Deep Dive** | Per-endpoint latency/errors, user session metrics, JS error rates, database query performance | 30s | Dev team |
| **Customer Portal Deep Dive** | Per-endpoint latency/errors, authentication flow, claim submission flow, document upload metrics | 30s | Dev team |
| **Database Performance** | Query latency histogram, slow query log, connection pool utilization, lock wait time | 30s | DBA, Dev team |
| **Queue & Integration** | Queue depth over time, consumer lag, message age, DLQ volume, per-integration latency | 30s | Dev team, Integration |

#### TV Display / NOC Dashboards

The existing Grafana TV dashboard (`solutions/dashboards/grafana-tv-dashboard-review.md`) covers the EKS health view. Extend with:

| TV Dashboard | Content | Kiosk Rotation |
|-------------|---------|----------------|
| **System Health** (existing) | Per-system health, uptime, latency, errors, throughput, resources, alerts | 60s per view |
| **Business Pulse** (new) | Policy issuance count today, claims in progress, premium collection status, batch job matrix | 60s per view |
| **Alert Board** (new) | Active SEV1/SEV2 alerts, recent incident timeline, on-call contact | Always visible or 30s rotation |

### 8.3 Dashboard Design Standards

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

## 9. Key Metrics & KPIs

### 9.1 Infrastructure KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| System availability (per service) | 99.95% (Sale Portal), 99.9% (Customer Portal) | Synthetic monitoring success rate, 30-day rolling |
| Mean Time to Detect (MTTD) | < 5 min for P1 | Time from incident start to first alert |
| Mean Time to Acknowledge (MTTA) | < 15 min for P1 | Time from alert to human acknowledgment |
| P95 response time (Sale Portal) | < 500ms | Prometheus histogram |
| P95 response time (Customer Portal) | < 1s | Prometheus histogram |
| Error rate (5xx) | < 0.1% | Prometheus counter ratio |
| Resource utilization (CPU/memory) | 40-70% average (headroom for spikes) | Prometheus gauges |
| Certificate expiry | > 30 days remaining | Blackbox exporter |
| Database connection utilization | < 70% of max connections | CloudWatch |

### 9.2 Application KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| Deployment success rate | > 95% | CI/CD pipeline metrics |
| Error log volume (per hour) | Trending down month-over-month | OpenSearch aggregation |
| Slow query rate | < 1% of total queries | Application logs |
| Cache hit rate | > 90% | ElastiCache metrics |
| API endpoint latency (per endpoint) | Within defined SLO per endpoint | Prometheus histogram |

### 9.3 Insurance Business KPIs

These are the metrics that distinguish TCLife monitoring from generic IT monitoring.

| KPI | Target | Source | Alert Threshold |
|-----|--------|--------|----------------|
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

### 9.4 Incident Management KPIs

Cross-reference with IM-015 from the incident management backlog:

| KPI | Target | Source |
|-----|--------|--------|
| MTTD (Mean Time to Detect) | < 5 min (P1), < 15 min (P2) | Alert timestamp vs. incident start |
| MTTA (Mean Time to Acknowledge) | Per SLA (15 min P1, 30 min P2) | PagerDuty/OpsGenie |
| MTTR (Mean Time to Resolve) | Per SLA in classification.md | ITSM ticket timestamps |
| Incident SLA adherence | > 95% | ITSM reporting |
| Alert-to-incident ratio | > 80% of P1/P2 detected by monitoring | Compare alert timestamps to incident tickets |
| False positive rate | < 20% | Weekly alert review |
| RCA completion rate | 100% for P1/P2 | ITSM tracking |

### 9.5 Reporting Cadence

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| **Daily Ops Report** | ITO, IT Manager | Daily 09:00 | Active alerts, overnight batch status, key metrics summary |
| **Weekly Availability Report** | IT Manager, CIO | Weekly Monday | Service availability %, incident count by priority, top issues |
| **Monthly SLA Report** | CIO, Board | Monthly | SLA compliance per service, vendor SLA tracking, trend analysis, capacity forecast |
| **Quarterly Business Metrics** | CIO, COO, CFO | Quarterly | Business KPIs trend, system investment recommendations, risk assessment |
| **Regulatory Availability Report** | Compliance, CIO | Per regulatory schedule | System availability for regulated services, incident impact on policyholders |

---

## 10. Compliance & Audit

### 10.1 Vietnam Regulatory Context

TCLife is regulated by the Vietnam Ministry of Finance (MOF) and the Insurance Supervisory Authority (ISA). While Vietnam does not yet have prescriptive IT monitoring regulations comparable to MAS (Singapore) or EIOPA (EU), the following requirements apply:

| Requirement Area | Regulatory Basis | Monitoring Implication |
|-----------------|-----------------|----------------------|
| **Business continuity** | Circular 125/2018/TT-BTC and related MOF guidance on IT risk management for insurers | Must demonstrate system availability measurement and incident response capability |
| **Data protection** | Cybersecurity Law 2018, Decree 13/2023/ND-CP | Must detect and report data breaches; monitoring must cover access anomalies and data exfiltration signals |
| **Financial reporting accuracy** | Insurance Law 2022 (amended), Circular 50/2017/TT-BTC | Must ensure accuracy of financial data processing — monitoring of GL, NAV, premium, and claims calculations |
| **Operational risk management** | MOF guidelines on operational risk for financial institutions | Must demonstrate operational risk controls including system monitoring and incident management |
| **Outsourcing and vendor management** | MOF guidance on outsourcing of critical functions | Must independently monitor vendor-managed systems (Insuremo) and track vendor SLA compliance |

### 10.2 Audit Trail Requirements

| Audit Need | Monitoring Component | Retention |
|-----------|---------------------|-----------|
| Who accessed what data | Application access logs -> OpenSearch | 5 years (aligned with insurance record retention) |
| System availability evidence | Prometheus metrics (uptime, SLA) | 3 years (export to S3 for long-term) |
| Incident response records | ITSM tickets + communication logs | 5 years |
| Change and deployment history | CI/CD logs + CloudTrail | 3 years |
| Batch job execution proof | Batch job monitor metrics + logs | 5 years (financial records) |
| Security event history | GuardDuty findings + WAF logs + CloudTrail | 5 years |

### 10.3 Compliance Dashboards

Build a dedicated compliance dashboard (Level 1) that provides:

- **System availability**: Monthly/quarterly availability by regulated service
- **Incident history**: Timeline of P1/P2 incidents affecting policyholders with resolution time
- **Data breach tracking**: Any security events involving policyholder data
- **Batch processing evidence**: Daily batch completion for GL, regulatory reporting, premium collection
- **Vendor SLA compliance**: Insuremo availability and performance against contractual SLA

This dashboard serves as the "evidence pack" for regulatory inquiries and internal/external audits.

### 10.4 Log Retention Architecture

```
  Real-time (0-30 days):  OpenSearch hot storage
  Warm (30-90 days):      OpenSearch warm/cold storage (UltraWarm)
  Archive (90 days-5 years): S3 Glacier + Athena for ad-hoc query
```

Ensure all log pipelines include immutable timestamps and cannot be retroactively modified (use S3 Object Lock for archived logs if required by audit).

---

## 11. Roadmap Phases

### Phase 1: Foundation (Months 1-3)

**Goal**: Establish reliable infrastructure monitoring, alerting pipeline, and on-call process.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **CloudWatch-to-Grafana integration** | Import all CloudWatch metrics (RDS, ALB, S3, SQS, Lambda) into Grafana dashboards | Infra team | All AWS services visible in Grafana |
| **Node and pod alerting** | Complete Prometheus alert rules for node health, pod restarts, OOM, resource saturation | Infra team | Alert rules deployed and tested |
| **On-call tooling setup** | Select and deploy PagerDuty or OpsGenie; configure Alertmanager integration | ITO + Infra | SEV1/SEV2 alerts route to on-call phone |
| **On-call rotation** | Define rotation schedule, compensation, handoff procedure | ITO Manager | Published rotation, first 4 weeks staffed |
| **Alert runbooks** | Write runbook for every Phase 1 alert rule | ITO + Infra | 100% alert-to-runbook coverage |
| **Log pipeline verification** | Verify all application and infrastructure logs flow to OpenSearch; identify gaps | Infra team | Log coverage inventory document |
| **Infrastructure dashboards** | Build Level 2 infrastructure overview + RDS + ALB dashboards in Grafana | Infra team | Dashboards published and reviewed |
| **Synthetic monitoring (basic)** | Deploy blackbox_exporter probes for Sale Portal and Customer Portal login URLs | Infra team | Uptime based on real probe, not `up` metric |
| **Certificate monitoring** | Monitor all TLS certificate expiry dates | Infra team | Alert at 30 and 7 days before expiry |
| **Baseline documentation** | Document all monitored services, alert rules, thresholds, and dashboard inventory | ITO | Living document in `solutions/monitoring-alerting/` |

**Phase 1 exit criteria**:
- All P1-triggering infrastructure conditions have automated alerts
- On-call engineer receives phone alerts for SEV1/SEV2 within 30 seconds
- Infrastructure dashboards show real data for all production services
- Synthetic probes confirm portal reachability every 60 seconds

### Phase 2: Application & Security (Months 4-6)

**Goal**: Extend monitoring to application layer, deploy Insuremo health prober, establish security monitoring baseline.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Application instrumentation audit** | Verify all applications expose HTTP histogram and counter metrics; remediate gaps | Dev team + ITO | All apps expose standard metrics |
| **Application dashboards** | Build Level 2 + Level 3 dashboards for Sale Portal and Customer Portal | Dev team + ITO | Per-endpoint latency/error/throughput visible |
| **Insuremo Health Prober** | Deploy health prober service; expose Prometheus metrics; build Grafana dashboard | Infra + Integration team | Insuremo availability and latency visible in Grafana |
| **Insuremo SLA dashboard** | Build Level 1 vendor SLA tracking dashboard | ITO | Monthly SLA reporting automated |
| **Log-based alerting** | Configure OpenSearch alerting for: error spikes, exception patterns, auth failures | ITO + Dev team | At least 10 log-based alert rules active |
| **GuardDuty integration** | Route GuardDuty findings to OpenSearch; build security overview dashboard | Infra + Security | GuardDuty findings visible in Grafana/OpenSearch |
| **WAF logging** | Enable WAF logging to OpenSearch; build WAF dashboard | Infra | WAF block/allow patterns visible |
| **CloudTrail monitoring** | Route high-risk CloudTrail events to OpenSearch alerting (root login, IAM changes, S3 policy changes) | Infra | Critical IAM events generate alerts |
| **Alert tuning cycle** | Review all Phase 1 alerts; adjust thresholds; retire false positives | ITO | False positive rate < 20% |
| **Operations dashboards** | Build Level 2 alert overview and application health dashboards | ITO | Operational dashboards in daily use |

**Phase 2 exit criteria**:
- Application-level alerts detect error rate spikes and latency degradation before users report
- Insuremo health prober running in production with 30-day baseline
- Security events from GuardDuty, WAF, and CloudTrail are centralized and alerting
- Log-based alerting catches critical error patterns

### Phase 3: Business Metrics & Batch Monitoring (Months 7-9)

**Goal**: Extend monitoring to business processes and batch job operations. This is the phase where monitoring becomes insurance-specific.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Batch Job Monitor** | Deploy batch job monitoring service; expose metrics for all batch jobs | Infra + Operations | All batch jobs tracked for start/complete/SLA |
| **GL batch monitoring** | Track GL file generation, transfer, and posting confirmation daily | Operations + Finance | GL SLA tracked and alerted |
| **Printing batch monitoring** | Track document generation, file delivery to printing partner, ACK | Operations | Print partner SLA tracked |
| **Datalake feed monitoring** | Track data freshness and record counts for datalake feeds | Data team + ITO | Datalake lag visible and alerted |
| **NAV calculation monitoring** | Track UL NAV calculation completion time and accuracy | Operations + Actuarial | NAV timeliness alerted by 10:00 AM |
| **Premium collection dashboard** | Build business metrics dashboard for premium collection success, retry, lapse | ITO + Finance | Premium collection health visible |
| **Claims processing dashboard** | Build business metrics dashboard for claims registration-to-payment lifecycle | ITO + Claims ops | Claims processing time visible |
| **Policy issuance dashboard** | Build business metrics dashboard for policy issuance pipeline | ITO + Underwriting ops | Policy issuance latency visible |
| **Reconciliation checks** | Implement automated reconciliation for GL, premium, NAV | Operations + Dev team | Daily reconciliation runs with alerts on mismatch |
| **Business Pulse TV dashboard** | Build TV-mode dashboard showing daily business health | ITO | Displayed in operations area |
| **CIO Management dashboard** | Build Level 1 business health dashboard | ITO | CIO can view business processing status in one screen |

**Phase 3 exit criteria**:
- Every daily batch job has automated monitoring with SLA alerting
- Business process KPIs (policy issuance, claims, premium) are visible and trended
- Reconciliation mismatches generate alerts within 2 hours of batch completion
- CIO dashboard provides single-pane view of business + system health

### Phase 4: Advanced Capabilities (Months 10-12)

**Goal**: Mature the monitoring practice with predictive capabilities, capacity planning, compliance reporting, and continuous improvement.

| Deliverable | Description | Owner | Done When |
|-------------|-------------|-------|-----------|
| **Capacity planning dashboards** | Trend-based resource forecasting; predict when current capacity is insufficient | Infra team | Quarterly capacity review uses data-driven forecasts |
| **Anomaly detection** | Deploy statistical anomaly detection on key metrics (OpenSearch ML or Prometheus recording rules with deviation tracking) | ITO + Data team | At least 5 anomaly detection rules active |
| **SLA reporting automation** | Auto-generate monthly SLA reports from Grafana/Prometheus data | ITO | Monthly SLA report requires < 1 hour of manual effort |
| **Compliance dashboard** | Build audit-grade compliance dashboard with availability evidence, incident history, batch processing proof | ITO + Compliance | Dashboard reviewed and accepted by internal audit |
| **Log retention lifecycle** | Implement hot -> warm -> cold -> archive pipeline in OpenSearch + S3 | Infra team | Logs retained per policy; archive queryable via Athena |
| **Distributed tracing (evaluation)** | Evaluate OpenTelemetry tracing for critical request paths (policy creation, claims submission) | Dev team + ITO | Decision document on tracing adoption |
| **Cost monitoring** | Track AWS monitoring stack costs; optimize Prometheus cardinality, OpenSearch storage | ITO + Infra | Monthly cost report for monitoring services |
| **Runbook automation** | Automate response for top 5 most common alerts (auto-remediation via Lambda or SSM) | Infra team | At least 3 auto-remediation playbooks active |
| **Monitoring-as-Code** | Terraform/CDK for all Grafana dashboards, Prometheus rules, OpenSearch configurations | Infra team | All monitoring config in version control |
| **Process review** | Full review of monitoring effectiveness; update roadmap for Year 2 | ITO + CIO | Year 2 roadmap drafted |

**Phase 4 exit criteria**:
- Capacity planning prevents resource exhaustion incidents
- Compliance dashboard passes internal audit review
- Monitoring stack costs are tracked and optimized
- All monitoring configuration is in version control (Infrastructure as Code)
- Year 2 roadmap addresses gaps found during Year 1

---

## 12. Cost Considerations

### 12.1 AWS Managed Service Pricing Model

| Service | Pricing Basis | Key Cost Drivers |
|---------|--------------|------------------|
| **Amazon Managed Grafana** | Per active editor/viewer per month ($9/$5) | Number of dashboard users |
| **Amazon Managed Prometheus (AMP)** | Ingestion ($/10M samples), storage ($/GB-month), query ($/10B samples queried) | Metric cardinality, retention period, query frequency |
| **Amazon OpenSearch** | Instance hours + storage (EBS) + UltraWarm/Cold storage | Instance type, storage volume, data retention |
| **CloudWatch** | Metrics ($0.30/metric/month beyond free tier), logs ($0.50/GB ingested), alarms ($0.10/alarm/month) | Number of custom metrics, log volume |
| **PagerDuty/OpsGenie** | Per user per month ($21-49/user for PagerDuty) | Number of on-call responders |

### 12.2 Estimated Monthly Cost (Steady State)

These are rough estimates for a mid-sized life insurance operation. Actual costs depend on data volume, cardinality, and retention.

| Component | Estimated Monthly Cost (USD) | Notes |
|-----------|---------------------------|-------|
| Amazon Managed Grafana | $100-200 | 5-10 editors, 10-20 viewers |
| Amazon Managed Prometheus | $200-500 | Dependent on metric cardinality and ingestion rate |
| Amazon OpenSearch | $800-2,000 | 3-node cluster + UltraWarm; scales with log volume |
| CloudWatch (incremental) | $100-300 | Custom metrics, additional alarms, log insights queries |
| PagerDuty/OpsGenie | $200-500 | 5-10 on-call responders |
| Insuremo Health Prober (EKS resources) | $50-100 | Small pod, minimal compute |
| Batch Job Monitor (EKS resources) | $50-100 | Small pod, minimal compute |
| S3 archive storage | $50-200 | Long-term log and metric archive |
| **Total estimated** | **$1,550-3,900/month** | |

### 12.3 Cost Optimization Strategies

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

## 13. Risks & Dependencies

### 13.1 Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Alert fatigue** | On-call ignores critical alerts due to noise | High (if thresholds are not tuned) | Aggressive tuning in first 30 days per alert; weekly alert review; mandatory runbooks |
| **Incomplete application instrumentation** | Blind spots in application monitoring; dashboards show incomplete data | Medium | Phase 2 instrumentation audit; define minimum instrumentation standard |
| **EbaoTech vendor cooperation** | Vendor may restrict probe frequency, change APIs, or not share maintenance schedules | Medium | Establish vendor monitoring agreement; document probe frequency in contract; maintain relationship |
| **Skills gap** | Team lacks Prometheus/Grafana/OpenSearch expertise to build and maintain | Medium | Training in Phase 1; consider AWS partner support for initial setup |
| **Cost overrun** | Metric cardinality explosion or log volume exceeds estimates | Medium | Cardinality budgets per service; log sampling policies; monthly cost review |
| **Monitoring system as single point of failure** | If Grafana/Prometheus/OpenSearch is down, all visibility is lost | Low-Medium | AMP and AMG are managed services with built-in HA; cross-region backup for critical alerts via CloudWatch |
| **Organizational resistance** | Teams do not adopt monitoring practices, dashboards go stale | Medium | Embed monitoring in incident post-mortems; make dashboards part of daily standup; CIO sponsorship |
| **Scope creep** | Trying to monitor everything at once delays delivery of core capability | Medium | Strict phase gating; Phase 1 must be complete before Phase 2 starts |

### 13.2 Dependencies

| Dependency | Required By | Risk if Not Met |
|-----------|-------------|-----------------|
| **On-call budget approval** | Phase 1 (month 1) | Cannot implement after-hours alerting; P1 incidents at night go undetected |
| **PagerDuty/OpsGenie procurement** | Phase 1 (month 1) | Alert routing remains manual; escalation is unreliable |
| **Application team cooperation** | Phase 2 (month 4) | Cannot instrument applications; application monitoring remains blind |
| **EbaoTech vendor agreement on probing** | Phase 2 (month 4) | Cannot deploy health prober; core system monitoring remains vendor-dependent |
| **Finance/Operations input on batch SLAs** | Phase 3 (month 7) | Cannot define batch job alert thresholds; monitoring without meaningful thresholds is noise |
| **Compliance team input on retention** | Phase 4 (month 10) | Log retention may not meet regulatory requirements; audit risk |
| **Training budget** | Phase 1 (month 1) | Slower adoption; higher error rate in monitoring configuration |
| **CIO sponsorship** | All phases | Without executive backing, cross-team coordination stalls |

### 13.3 Open Questions

| Question | Needs Answer From | Impact |
|---------|-------------------|--------|
| What is the exact EbaoTech API contract for health probing? | Vendor/Integration team | Determines health prober design |
| Do we have an existing on-call policy/compensation framework? | HR/IT Manager | Determines Phase 1 timeline for on-call setup |
| What are the contractual SLA targets with EbaoTech? | Vendor Manager/Legal | Determines Insuremo SLA dashboard thresholds |
| What is the current log volume (GB/day) in OpenSearch? | Infra team | Determines OpenSearch sizing and cost estimate accuracy |
| Which batch jobs currently have monitoring? (Any?) | Operations | Determines Phase 3 starting point |
| Are there existing regulatory reporting requirements for system availability? | Compliance | Determines compliance dashboard priority |
| What is the current Prometheus metric cardinality? | Infra team | Determines AMP cost estimate accuracy |
| Is there a preferred ITSM tool? | IT Manager | Determines integration approach for incident correlation (per IM-009) |

---

## 14. Appendix: Cross-References to Existing Work

This roadmap builds on and connects to several existing documents in the TCLife workspace:

| Document | Location | Relationship |
|----------|----------|-------------|
| **Grafana TV Dashboard Review** | `solutions/dashboards/grafana-tv-dashboard-review.md` | Phase 1 TV dashboard is an extension of this existing work; PromQL patterns are reusable |
| **Grafana Dashboard Implementation Notes** | `solutions/dashboards/grafana-dashboard-implementation-notes.md` | Implementation guidance for dashboard deployment; namespace and metric name mapping |
| **Incident Classification** | `solutions/incident-management/classification.md` | Alert severity levels (Section 4) are aligned with incident priority matrix (P1-P4) |
| **Incident Management Backlog** | `solutions/incident-management/backlog.md` | This roadmap addresses: IM-005 (on-call model), IM-009 (tooling specification), IM-015 (metrics/KPIs) |
| **ITO Capability Declaration** | `solutions/ito-responsible/capability-declaration.md` | Section 2.7 (Monitoring & Alerting) and 2.13 (Reporting) define ITO's monitoring responsibilities; this roadmap operationalizes them |
| **Incident Scenarios** | `solutions/incident-management/scenarios.md` | Business scenarios (e.g., 347 policies with zero surrender value) inform which business metrics to monitor |
| **L1 Support Frontline** | `solutions/L1-support-frontline/l1-support-frontline.md` | L1 uses monitoring dashboards for incident detection and triage; dashboard design must support L1 workflows |

### Incident Management Backlog Items Addressed

| Backlog ID | Item | How This Roadmap Addresses It |
|-----------|------|------------------------------|
| IM-005 | On-call and after-hours coverage model | Section 4.3 defines on-call rotation, tooling, and escalation |
| IM-009 | Incident management tooling specification | Section 5 specifies Prometheus/Grafana/OpenSearch/PagerDuty as the monitoring and alerting stack |
| IM-015 | Metrics and KPI framework | Section 9 defines comprehensive KPIs with targets and measurement approach |
| IM-018 | Vendor management integration | Section 6 defines Insuremo vendor SLA tracking and incident attribution |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | IT Operations | Initial draft |

---

> **Next step**: CIO review. This document should be reviewed by tcl-cio for strategic alignment, risk assessment, and prioritization feedback before implementation begins.
