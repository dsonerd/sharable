# Monitoring & Alerting Roadmap — Technical Reference

> **Version**: 2.2
> **Date**: 2026-03-20
> **Author**: IT Operations
> **Status**: Revised — incorporating CIO review findings (R-001 through R-043), insurance-domain monitoring research, and deep expansion of monitoring and alerting strategy sections
> **Audience**: IT Operations, DevOps, Application Support, Engineering
> **Companion document**: `monitoring-alerting-roadmap-overview.md` (executive overview)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Team Structure & Staffing Plan](#2-team-structure--staffing-plan)
3. [Current State Assessment](#3-current-state-assessment)
4. [Monitoring Strategy](#4-monitoring-strategy)
   - 4.1 Layered Monitoring Model
   - 4.2 Layer 1 — Infrastructure Monitoring (Core Metrics, EKS Deep Dive, Database Deep Dive, Deployment Health)
   - 4.3 Layer 2 — Platform / Middleware (SQS/EventBridge, Cache, API Gateway, Certificates/DNS)
   - 4.4 Layer 3 — Application (Instrumentation, Golden Signals, Health Checks, Log Levels, Correlation IDs)
   - 4.5 Layer 4 — Business Process (Journey-First Monitoring, Failure Detection, Rider Lifecycle, Segmentation)
   - 4.6 Security (AWS Services, SIEM-Lite, PII Access, Fraud Indicators)
   - 4.7 RUM (Web Vitals SLOs, Segmentation, Alerting)
   - 4.8 Cost Monitoring (Anomaly Scenarios, Reserved Capacity Tracking)
5. [Alerting Strategy](#5-alerting-strategy)
   - 5.1 Severity Levels
   - 5.2 Alert Routing and Notification Channels
   - 5.3 On-Call Model
   - 5.4 Alert Quality Principles
   - 5.5 Alert Inhibition and Grouping
   - 5.6 Alert Lifecycle Management (States, ITSM Integration)
   - 5.7 Alert Runbook Template (Standard Template, Example Runbook)
   - 5.8 Alert Naming Convention (Format, Label Taxonomy)
   - 5.9 Escalation Flow (Flowchart, Auto-Escalation, Business/After-Hours)
   - 5.10 Alert Testing Strategy (Unit Testing, Game Days, Promotion)
   - 5.11 Alert Noise Management (Composite Alerts, Noise Budget, Quality Report)
   - 5.12 Business Alert Routing (Technical vs Business, Routing Matrix, Format)
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
18. [Core Business Journeys to Monitor](#18-core-business-journeys-to-monitor)
19. [Domain-Specific Monitoring Matrices](#19-domain-specific-monitoring-matrices)
20. [Service Level Objectives (SLOs)](#20-service-level-objectives-slos)
21. [First 25 Alerts — Prioritized Implementation List](#21-first-25-alerts--prioritized-implementation-list)
22. [Canonical Telemetry Data Model](#22-canonical-telemetry-data-model)
23. [Composite Alert Patterns](#23-composite-alert-patterns)
24. [Appendix: Cross-References to Existing Work](#24-appendix-cross-references-to-existing-work)

---

## 1. Executive Summary

TCLife operates a fully AWS-hosted life insurance platform serving policyholders, sales agents, and internal operations across Unit-Linked (UL), Critical Illness (CI), Health Insurance (HI), and Medical Reimbursement (MR) product lines. The core insurance system (EbaoTech Insuremo) is vendor-managed, and the company exchanges batch files with partners for printing, general ledger (GL), and datalake integrations.

Today, TCLife has foundational monitoring components in place — Amazon Managed Grafana, Amazon Managed Service for Prometheus (AMP), and Amazon OpenSearch Service — but lacks a unified, layered monitoring strategy that covers infrastructure, application, business process, and security dimensions. The existing Grafana TV dashboard work (see `solutions/dashboards/`) covers EKS health metrics but does not extend to business-critical flows such as policy issuance, claims processing, premium collection, or the vendor-managed core system.

This roadmap defines a **four-phase implementation plan** to build a comprehensive monitoring and alerting capability over 12 months, delivered by a 7-person team (3 App Ops, 1 Service Quality, 3 DevOps). The phases deliver incremental value: Phase 1 establishes foundational infrastructure monitoring and team training, Phase 2 extends to application-level observability and security, Phase 3 adds insurance-specific business metrics and batch job monitoring, and Phase 4 introduces advanced capabilities including capacity planning and audit-grade compliance reporting.

**Target state**: Every P1/P2 incident is detected by monitoring before users report it. Every business-critical batch job is tracked for timeliness and success. The CIO has a single dashboard showing system health, SLA compliance, and business processing status.

**Changes from v1.0**: v2.0 incorporates all 43 CIO review findings (10 high, 21 medium, 12 low). Major additions: team structure and staffing plan, training as Phase 1 deliverable, missing monitoring domains (RUM, AWS cost, commission batch), PII scrubbing policy, human cost model, and regulatory citation qualification. See Section 17 for the full resolution matrix.

**Changes from v2.0 to v2.1**: Added journey-first monitoring framework (9 core journeys, Section 18), domain-specific monitoring matrices (Section 19), formal SLO set (Section 20), prioritized first 25 alerts (Section 21), canonical telemetry data model (Section 22), composite alert patterns (Section 23), rider monitoring as first-class dimension throughout, strengthened InsureMO instrumentation checklist (Section 7), and strengthened regulatory citations (Section 11). Reference: `reference.research.md`.

**Changes from v2.1 to v2.2**: Deep expansion of Sections 4 (Monitoring Strategy) and 5 (Alerting Strategy). Section 4 now includes: EKS cluster-level monitoring, RDS/Aurora connection pooling and slow query detection, deployment health tracking, full SQS/EventBridge/cache/API Gateway metrics with thresholds, golden signals per service, health check endpoint specification, log level strategy, correlation ID propagation, journey-first business process failure detection with concrete scenarios, AWS security services integration (GuardDuty/Security Hub/Inspector/Macie), SIEM-lite approach using OpenSearch, PII access monitoring, fraud indicators, RUM Web Vitals SLO targets with segmentation, and insurance-specific cost anomaly scenarios. Section 5 now includes: alert lifecycle with ITSM integration, runbook template with example, naming convention and label taxonomy, escalation flowchart with auto-escalation, alert testing strategy with game days, noise management with composite alerts and noise budget, and business alert routing distinguishing technical from business stakeholder alerts.

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

#### 4.2.1 Core Infrastructure Metrics

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Node health | `kube_node_status_condition{condition="Ready"}` | Prometheus | Any node NotReady > 2 min |
| Pod restarts | `kube_pod_container_status_restarts_total` | Prometheus | > 3 restarts in 15 min |
| CPU utilization | `container_cpu_usage_seconds_total` / limits | Prometheus | > 80% sustained 5 min |
| Memory utilization | `container_memory_working_set_bytes` / limits | Prometheus | > 85% sustained 5 min |
| Disk I/O and capacity | `node_filesystem_avail_bytes` | Prometheus | < 15% free |
| ALB 5xx rate | `HTTPCode_ELB_5XX_Count` | CloudWatch | > 1% of total requests |
| ALB latency | `TargetResponseTime` | CloudWatch | P99 > 2 seconds |
| ALB unhealthy targets | `UnHealthyHostCount` | CloudWatch | > 0 sustained 2 min |
| Lambda errors | `Errors` | CloudWatch | > 5% invocation error rate |
| Lambda duration | `Duration` | CloudWatch | P95 > 80% of timeout |
| Lambda throttles | `Throttles` | CloudWatch | > 0 for critical functions |
| S3 request errors | `4xxErrors`, `5xxErrors` | CloudWatch | Sustained spike |
| VPC flow anomalies | VPC Flow Logs | OpenSearch | Unusual traffic patterns |
| **EKS cluster version** | Custom check or `kube_node_info` | Prometheus / CloudWatch | **EKS version within 60 days of EOL (R-006)** |
| AWS Health events | `AWS Health` via EventBridge | CloudWatch / EventBridge | Any event impacting critical services |

#### 4.2.2 EKS-Specific Deep Dive

TCLife runs all application workloads on Amazon EKS. Beyond basic node and pod metrics, EKS-specific monitoring must cover cluster-level health, managed node groups, scheduling behavior, and auto-scaling dynamics.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Cluster API server health | `apiserver_request_total`, `apiserver_request_duration_seconds` | Prometheus | Error rate > 1% or P99 latency > 1s |
| etcd health | `etcd_server_has_leader`, `etcd_disk_wal_fsync_duration_seconds` | Prometheus (control plane metrics) | Leader loss or WAL fsync P99 > 100ms |
| Node group scaling | `kube_node_status_condition` by node group | Prometheus | Node group at min capacity and pods pending > 2 min |
| Pending pods | `kube_pod_status_phase{phase="Pending"}` | Prometheus | Any pod pending > 5 min (excludes expected job scheduling) |
| Failed scheduling | `scheduler_schedule_attempts_total{result="error"}` | Prometheus | > 0 sustained 5 min |
| HPA behavior | `kube_horizontalpodautoscaler_status_current_replicas` vs `_desired_replicas` | Prometheus | Desired != current for > 5 min; current at max replicas sustained 10 min |
| HPA scaling ceiling | `kube_horizontalpodautoscaler_spec_max_replicas` vs current replicas | Prometheus | Current = max for > 15 min (capacity risk) |
| Pod evictions | `kube_pod_status_reason{reason="Evicted"}` | Prometheus | > 3 evictions in 15 min per node |
| Container OOMKills | `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}` | Prometheus | Any OOMKill on business-critical workload |
| CoreDNS latency | `coredns_dns_request_duration_seconds` | Prometheus | P99 > 200ms (DNS failures cause silent cascading issues) |
| Node resource pressure | `kube_node_status_condition{condition=~"DiskPressure\|MemoryPressure\|PIDPressure"}` | Prometheus | Any pressure condition True > 1 min |

**Why this matters for TCLife**: Pod scheduling failures and HPA ceiling hits during peak hours (e.g., start of business when agents log in simultaneously, or end of day during batch processing) can cause portal slowness or submission failures that appear as application-layer problems but originate in infrastructure capacity.

#### 4.2.3 Database Deep Dive (RDS/Aurora)

TCLife's databases hold policy, claims, financial, and customer data. Database degradation directly impacts every business journey.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| RDS connections | `DatabaseConnections` | CloudWatch | > 80% max connections |
| RDS CPU | `CPUUtilization` | CloudWatch | > 75% sustained 10 min |
| RDS storage | `FreeStorageSpace` | CloudWatch | < 20% free |
| RDS replication lag | `ReplicaLag` | CloudWatch | > 10 seconds |
| Connection pool utilization | Application-level pool metrics (e.g., HikariCP `active_connections` / `max_pool_size`) | Prometheus | > 80% pool utilization sustained 5 min |
| Connection pool wait time | `hikaricp_connections_pending` or equivalent | Prometheus | > 0 pending connections sustained 2 min |
| Slow query count | `slow_query_count` from Performance Insights or application logs | CloudWatch / OpenSearch | > 10 slow queries (>1s) in 5 min window |
| Long-running queries | Queries running > 30 seconds (Performance Insights) | CloudWatch | Any query > 60s (potential lock holder) |
| Read/write IOPS | `ReadIOPS`, `WriteIOPS` | CloudWatch | > 80% provisioned IOPS sustained 10 min |
| Buffer cache hit ratio | `BufferCacheHitRatio` | CloudWatch | < 95% (indicates insufficient memory) |
| Deadlocks | `Deadlocks` (Performance Insights or pg_stat) | CloudWatch / Prometheus | > 0 deadlocks per 5 min |
| Failover events | RDS event notifications | CloudWatch Events / EventBridge | Any failover event (SEV2) |
| Burst balance (gp3/gp2) | `BurstBalance` | CloudWatch | < 20% (I/O throttling imminent) |

**Connection pooling requirements**: All application services connecting to RDS must use connection pooling (e.g., HikariCP for Java/Spring, pgBouncer for direct connections). Monitor pool-level metrics alongside database-level connections to distinguish between application-side pool exhaustion and database-side connection limits.

**Slow query detection flow**:
1. Enable RDS Performance Insights (no additional agent required for RDS)
2. Set `log_min_duration_statement = 1000` (1 second) in PostgreSQL parameter group
3. Route slow query logs to OpenSearch for pattern analysis
4. Alert on slow query volume spikes (not individual queries) to avoid noise

**Failover monitoring**: If using Multi-AZ RDS or Aurora, monitor failover events via EventBridge. A failover causes a brief outage (typically 30-60 seconds for Aurora, 60-120 seconds for RDS Multi-AZ). The monitoring system must detect this and suppress downstream application alerts for the failover window.

#### 4.2.4 Deployment and Release Health Monitoring

Deployments are the most common cause of production incidents. Monitoring must detect bad releases quickly enough to roll back before business impact accumulates.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Error budget burn post-deploy | 5xx rate delta in 15 min after deploy vs. 1h pre-deploy baseline | Prometheus | > 2x baseline error rate within 15 min of deploy |
| Rollback detection | Deployment version reverted (Kubernetes rollout undo) | Prometheus / Kubernetes events | Any rollback on production namespace |
| Canary health (if applicable) | Canary pod error rate vs stable pods | Prometheus | Canary error rate > 5x stable error rate |
| Deploy frequency | Deployments per day/week | Prometheus (custom metric from CI/CD) | Informational — no alert, trend only |
| Deploy duration | Time from deploy start to all pods healthy | Prometheus / CI/CD | > 2x rolling average deploy duration |
| Failed deploys | CI/CD pipeline failures on production | CI/CD system -> Prometheus | Any failed production deploy |
| Post-deploy latency shift | P95 latency delta in 30 min after deploy | Prometheus | P95 increases > 50% vs pre-deploy |

**Implementation**: Annotate Grafana dashboards with deployment events (timestamp + version + deployer). This makes visual correlation between deploys and metric changes immediate. Use Kubernetes deployment annotations or CI/CD webhook to emit deploy events.

**Error budget burn rule**: After a production deployment, if the 5xx error rate exceeds 2x the pre-deployment baseline within 15 minutes, fire a SEV2 alert to the deploying team. If the error budget burn rate for the affected SLO exceeds 1% in 1 hour post-deploy, fire a SEV1 alert recommending immediate rollback.

### 4.3 Layer 2 — Platform / Middleware Monitoring

**Scope**: Message queues (SQS), event bus (EventBridge), caching layers (ElastiCache), API gateways, DNS resolution, certificate expiry, secrets management.

**Why this layer is critical**: Platform services sit between application code and infrastructure. A degraded SQS queue or an exhausted ElastiCache cluster causes application-level symptoms (slow responses, failed transactions) that are hard to diagnose if platform metrics are not monitored independently.

#### 4.3.1 SQS and EventBridge Deep Dive

SQS queues and EventBridge are the asynchronous backbone for TCLife's integration layer — connecting portals to InsureMO, batch job triggers, payment callbacks, and notification delivery.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Queue message age | `ApproximateAgeOfOldestMessage` | CloudWatch | > SLA threshold per queue (see below) |
| Queue depth | `ApproximateNumberOfMessagesVisible` | CloudWatch | > 2x normal depth sustained 10 min |
| DLQ message count | `ApproximateNumberOfMessagesVisible` on DLQ | CloudWatch | > 0 messages (SEV1 for payment/issuance queues, SEV2 for others) |
| Messages sent vs received | `NumberOfMessagesSent` vs `NumberOfMessagesReceived` | CloudWatch | Sustained divergence > 10 min (producer/consumer mismatch) |
| Empty receives | `NumberOfEmptyReceives` | CloudWatch | Informational — high empty receive rate wastes compute but is not urgent |
| EventBridge failed invocations | `FailedInvocations` | CloudWatch | > 0 sustained 5 min (SEV2) |
| EventBridge rule throttling | `ThrottledRules` | CloudWatch | > 0 (SEV2 — events being dropped) |
| EventBridge invocation latency | `InvocationLatency` | CloudWatch | P95 > 5s for business-critical rules |

**Queue-specific SLA thresholds** (adjust after baseline measurement):

| Queue | Max acceptable message age | DLQ severity |
|-------|---------------------------|-------------|
| Payment callbacks | 2 min | SEV1 |
| Policy issuance events | 5 min | SEV1 |
| Notification delivery | 15 min | SEV2 |
| Batch job triggers | Per job schedule tolerance | SEV2 |
| Audit/logging events | 30 min | SEV3 |

**DLQ management**: Every SQS queue handling business transactions must have a DLQ configured. DLQ messages represent events that failed processing after max retries — they are potential data loss. Alert immediately and require manual review before purging.

#### 4.3.2 Cache Layer (ElastiCache)

Caching protects downstream databases and accelerates frequently-accessed data (product configurations, rider pricing tables, agent sessions, frequently-viewed policy summaries).

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Cache hit ratio | `CacheHitRate` | CloudWatch | < 90% sustained 15 min (SEV3 — potential cache invalidation issue) |
| Evictions | `Evictions` | CloudWatch | > 0 sustained and rising (memory pressure) |
| Current connections | `CurrConnections` | CloudWatch | > 80% max connections |
| Memory utilization | `DatabaseMemoryUsagePercentage` | CloudWatch | > 80% (SEV3), > 90% (SEV2 — eviction storm imminent) |
| CPU utilization | `EngineCPUUtilization` | CloudWatch | > 75% sustained 10 min |
| Replication lag | `ReplicationLag` | CloudWatch | > 1s (if using read replicas) |
| Swap usage | `SwapUsage` | CloudWatch | > 50MB (indicates memory pressure) |

**Why cache matters for insurance**: Product configuration and rider pricing table lookups happen on every quotation. If cache is cold or degraded, these lookups fall through to the database, causing latency spikes in the quotation engine that directly impact agent productivity.

#### 4.3.3 API Gateway Monitoring

If TCLife uses API Gateway as the front door for external and internal API traffic, it is the single chokepoint where all client requests enter.

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| 4xx error rate | `4XXError` | CloudWatch | > 5% sustained 5 min (client errors — may indicate breaking API change) |
| 5xx error rate | `5XXError` | CloudWatch | > 1% sustained 5 min (SEV2), > 5% (SEV1) |
| Latency | `Latency` (P50, P95, P99) | CloudWatch | P99 > 3s sustained 5 min |
| Integration latency | `IntegrationLatency` | CloudWatch | P99 > 2s (backend response time) |
| Request count | `Count` | CloudWatch | Informational; alert on sudden traffic drop > 50% (signals possible routing issue or outage) |
| Throttling | `ThrottleCount` | CloudWatch | > 0 sustained (SEV2 — legitimate traffic being rejected) |
| Cache hit ratio (if enabled) | `CacheHitCount` / `CacheMissCount` | CloudWatch | Informational — drop in cache hits after deploy may indicate changed API patterns |

#### 4.3.4 Certificate and DNS Health

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| TLS certificate expiry | Certificate remaining days | Prometheus blackbox_exporter or cert-manager | < 30 days (SEV3), < 14 days (SEV2), < 7 days (SEV1) |
| DNS resolution time | DNS lookup latency | Prometheus blackbox_exporter | > 500ms (SEV3 — DNS failures cascade silently) |
| DNS resolution failure | DNS lookup failure rate | Prometheus blackbox_exporter | Any resolution failure for critical endpoints |
| Secrets rotation status | Last rotation timestamp | Custom metric from Secrets Manager events | Secret not rotated within policy window |
| Certificate chain validity | Full chain verification | Prometheus blackbox_exporter | Any chain validation failure |

### 4.4 Layer 3 — Application Monitoring

**Scope**: All TCLife-owned applications — Sale Portal, Customer Portal, middleware/integration services, batch processing applications.

#### 4.4.1 Instrumentation Standard

All applications MUST expose:
- HTTP request duration histogram (`http_request_duration_seconds_bucket`)
- HTTP request counter by status code (`http_requests_total`)
- Custom business event counters (per application)
- Structured JSON logging to OpenSearch
- **Health check endpoint** (`/health` or `/healthz`) returning structured status including downstream dependency checks **(R-005)**

**Business event instrumentation**: At every significant state transition, the application must emit both a **business event** (for business monitoring) and a **technical event** (for operational monitoring). Business events use domain language; technical events use standard observability fields.

| Transition | Business event example | Technical event |
|-----------|----------------------|-----------------|
| Quote created | `quote_created{product="UL", channel="agency", rider_set="CI+HI"}` | HTTP 200, latency histogram, trace span |
| Application submitted | `application_submitted{product="UL", channel="digital"}` | HTTP 200, latency, payload size |
| Payment authorized | `payment_authorized{gateway="bank_X", amount_range="high"}` | HTTP 200, callback latency, idempotency key |
| Underwriting decided | `underwriting_decision{path="STP", decision="approve", product="UL"}` | Rules engine latency, external dependency calls |
| Policy issued | `policy_issued{product="UL", rider_count="2"}` | Document generation time, posting success |
| Rider activated | `rider_activated{rider_code="CI", product="UL"}` | Rider validation latency, rider-package version match |
| Claim registered | `claim_registered{event_type="hospitalization", product="HI"}` | FNOL intake latency, attachment upload success |

Every failed customer step must include: machine-readable failure code, human-readable message, and ownership tag (which team is responsible).

#### 4.4.2 Golden Signals Framework

Apply the four golden signals (traffic, latency, errors, saturation) to each TCLife service. This ensures consistent coverage and makes it easy to compare service health across the platform.

| Service | Traffic | Latency (P95 target) | Errors (target) | Saturation |
|---------|---------|---------------------|-----------------|------------|
| **Sale Portal** | Requests/sec, active sessions, quotes/hour | < 500ms page load, < 2s API calls | < 0.1% 5xx, < 1% business errors | CPU/memory vs limits, connection pool, concurrent sessions |
| **Customer Portal** | Requests/sec, active sessions, self-service transactions/hour | < 1s page load, < 3s API calls | < 0.1% 5xx, < 1% business errors | CPU/memory vs limits, connection pool |
| **Integration/Middleware** | Messages/sec, API calls to InsureMO/hour | < 1s per API call, < 5s per complex operation | < 0.5% failed integrations | Queue depth, thread pool utilization, connection pool |
| **Batch Processing** | Jobs/hour, records/batch | Per-job SLA (see Section 8) | 0% failed jobs (every failure is an incident) | CPU during batch windows, I/O throughput |
| **Notification Service** | Emails/SMS per hour, push notifications | < 30s delivery for transactional messages | < 2% delivery failure | Queue depth, provider rate limits |

#### 4.4.3 Metric Table

| What to Monitor | Metric | Tool | Threshold (Alert) |
|----------------|--------|------|-------------------|
| Request latency (P50, P95, P99) | `histogram_quantile` on HTTP duration | Prometheus + Grafana | P95 > service-specific target (see golden signals above) |
| Error rate (4xx, 5xx) | `rate(http_requests_total{status=~"[45].."}[5m])` | Prometheus + Grafana | 5xx > 0.1% sustained 5 min; 4xx spike > 3x baseline |
| Throughput (RPM) | `rate(http_requests_total[5m]) * 60` | Prometheus + Grafana | Drop > 50% from baseline (possible outage or routing issue) |
| Application error logs | Error/exception patterns | OpenSearch + alerting | Error volume spike > 3x rolling average |
| Slow query detection | Database query duration > threshold | Application logs -> OpenSearch | > 10 slow queries (>1s) per 5 min window |
| Dependency health | Circuit breaker state, downstream call latency | Prometheus custom metrics | Circuit breaker open on any critical dependency |
| Session/authentication metrics | Login success/failure rate, session count | Prometheus custom metrics | Login success < 95% for 10 min |
| API endpoint-level breakdown | Per-endpoint latency/error/throughput | Prometheus labels | Endpoint-specific SLO breach |
| **Health check status** | `/health` endpoint per service **(R-005)** | Prometheus blackbox_exporter or custom | Health check failure > 2 consecutive checks |

#### 4.4.4 Health Check Endpoint Specification

Every TCLife service must expose a `/health` endpoint that returns a structured response. The health check is the single source of truth for "is this service ready to serve traffic?"

**Required response format**:

```json
{
  "status": "healthy | degraded | unhealthy",
  "timestamp": "2026-03-20T10:15:30Z",
  "version": "1.4.2",
  "uptime_seconds": 86400,
  "checks": {
    "database": { "status": "healthy", "latency_ms": 5 },
    "cache": { "status": "healthy", "latency_ms": 2 },
    "insuremo_api": { "status": "healthy", "latency_ms": 120 },
    "sqs_queue": { "status": "healthy", "queue_depth": 12 }
  }
}
```

**Rules**:
- `status` is `healthy` only when ALL dependency checks pass.
- `status` is `degraded` when non-critical dependencies fail (e.g., cache is down but database is up).
- `status` is `unhealthy` when any critical dependency fails (e.g., database unreachable).
- Kubernetes readiness probe should use `/health` — an unhealthy response removes the pod from the load balancer.
- Kubernetes liveness probe should use a simpler `/livez` endpoint that checks only process health (not dependencies) to avoid restart loops when dependencies are temporarily unavailable.
- Health checks must complete within 5 seconds. If a dependency check times out, report it as unhealthy rather than hanging.

#### 4.4.5 Log Level Strategy

Consistent log levels across all services ensure that log-based alerting works reliably and operators can filter effectively.

| Level | When to use | Alerting behavior |
|-------|------------|-------------------|
| **FATAL** | Process cannot continue — data corruption risk, unrecoverable state, security breach detected | SEV1 alert immediately. Any FATAL log entry is an incident. |
| **ERROR** | Operation failed but process continues — failed API call after retries, failed transaction, unhandled exception | Alert on volume spike (> 3x rolling average in 5 min). Individual errors logged but not alerted unless sustained. |
| **WARN** | Unexpected condition that may lead to errors — retry attempts, deprecated API usage, approaching resource limits, slow queries | No immediate alert. Review in daily ops standup. Alert if WARN volume trends upward for 3+ days. |
| **INFO** | Normal business events — successful transactions, state transitions, batch job completion | Never alert. Used for operational dashboards and audit trail. |
| **DEBUG** | Detailed diagnostic information — request/response payloads, internal state | Never in production by default. Enable per-service via runtime flag for troubleshooting only. Must not contain PII. |

**Sensitive data rules**: No log level may contain unmasked PII (see Section 12). Policy numbers, customer names, national IDs, and health data must be masked or tokenized before logging. Use structured fields with masking applied at the logging framework level.

#### 4.4.6 Correlation ID and Trace Context Propagation

Every request entering TCLife's system must carry a correlation ID (also called trace ID) that propagates across all services and is included in every log entry, metric label, and event. This is the single most important requirement for debugging cross-service issues.

**Requirements**:
- Generate a unique correlation ID (`X-Correlation-ID` header) at the API gateway or load balancer for every inbound request.
- Propagate the correlation ID to all downstream service calls, queue messages, and database operations.
- Include the correlation ID in every structured log entry as a top-level field (`correlation_id`).
- Include the correlation ID in Prometheus exemplars (where supported) to link metrics to traces.
- For business journeys, also propagate a business context (application ID, policy ID, claim ID) alongside the technical correlation ID.

**Propagation chain example**:
```
Browser -> ALB (generates correlation_id) -> Sale Portal -> SQS message (carries correlation_id in attributes) -> Integration Service -> InsureMO API (passes correlation_id)
```

**Implementation**: Use OpenTelemetry context propagation (W3C Trace Context format) even before full distributed tracing is implemented. This ensures the header format and propagation logic are in place for Phase 3-4 when tracing is enabled.

**Distributed tracing** (Phase 3-4): Instrument with OpenTelemetry for full request tracing across services. The correlation ID and context propagation implemented in Phase 1-2 forms the foundation. Not in Phase 1-2 scope, but the instrumentation standard must be OTel-compatible from the start.

### 4.5 Layer 4 — Business Process Monitoring

**Scope**: Insurance-specific business flows that directly impact policyholders, agents, and regulatory compliance.

#### 4.5.1 Design Principle: Monitor by Journey, Not Just by Service

A healthy microservice estate can still hide a broken submission flow or a stalled underwriting queue. Business process monitoring must be organized by **customer journey first, service second**. Every journey uses a unique journey ID / application ID / policy ID / rider instance ID to stitch events end-to-end across portals, InsureMO services, underwriting engines, payment, messaging, and document services.

The nine core business journeys (J1-J9) defined in Section 18 provide the framework. This section defines HOW each business process is monitored — the data source, collection method, and specific detection patterns.

#### 4.5.2 Business Process Monitoring Matrix

| Business Process | What to Monitor | Why | Data Source | Collection Method | Key Metric Type |
|-----------------|----------------|-----|-------------|-------------------|----------------|
| **Policy issuance** | End-to-end time from submission to policy activation; conversion rate; rejection rate by reason | Agents blocked = revenue impact; SLA to policyholders | InsureMO API timestamps + Portal events | Prometheus counters emitted at each state transition; InsureMO API polling for timestamps | Duration histogram, success counter |
| **Claims processing** | Claim registration to assessment time; assessment to payment time; auto-approval rate; rejection rate | Regulatory SLA; policyholder experience; fraud detection signal | InsureMO claims API + FNOL portal events | Event-driven: business events emitted at registration, assessment, decision, payment | Duration histogram, ratio gauge |
| **Premium collection** | Collection success rate; failed payment retry rate; grace period utilization; lapse rate | Revenue assurance; policyholder retention | Payment gateway callbacks + InsureMO billing API | Payment callback events -> Prometheus counter; daily InsureMO query for grace/lapse | Success rate gauge, aging buckets |
| **UL NAV calculation** | NAV calculation completion time; variance from expected; fund price freshness | Regulatory requirement; policyholder statements depend on accurate NAV | Batch job monitor + InsureMO fund management API | Batch completion event -> Prometheus; periodic NAV freshness check | Batch completion gauge, variance gauge |
| **Surrender value** | Calculation accuracy (compare with actuarial baseline); batch completion | Scenario from IM backlog — 347 policies with zero surrender value | Reconciliation batch output + actuarial baseline | Batch reconciliation: compare computed values vs actuarial expected range | Reconciliation status gauge |
| **Quotation engine** | Quote generation time; quote-to-proposal conversion rate | Agent productivity; system responsiveness | Sale Portal application metrics | Prometheus histogram on quote API; conversion funnel counter | Duration histogram, conversion ratio |
| **Rider lifecycle** | Rider eligibility, premium computation, attach/detach, issue consistency, renewal, claim events | For a UL-focused insurer with CI, HI, MR riders, rider defects are a major source of complaints, leakage, and regulatory risk | InsureMO rider APIs + Portal events + Batch reconciliation | Event-driven at each rider lifecycle stage; daily reconciliation for drift detection | Multi-stage success counters |
| **Document generation** | Document generation success rate; printing partner file delivery timeliness | Policyholder communication; regulatory filings | Document service metrics + S3 file exchange events | Prometheus counter on document generation; S3 event for partner file delivery | Success rate gauge, SLA gauge |
| **Regulatory reporting** | Report generation completion; data freshness; submission timeliness; **regulatory filing countdown (R-017)** | MOF compliance; audit trail | Batch job monitor + regulatory calendar | Calendar-aware countdown metric; batch completion event | Countdown gauge, completion status |
| **Reinsurance data** | Cession data generation timeliness; reconciliation status | Treaty compliance; financial accuracy | Batch job monitor + reconciliation output | Batch completion + reconciliation status metric | Reconciliation gauge |
| **Commission calculation (R-016)** | Commission run completion; agent count processed; accuracy vs expected; timeliness | **Agent/sales force compensation — failed commission run creates immediate pain across entire distribution channel** | Batch job monitor + commission reconciliation | Batch event + reconciliation: agent count and total amount vs expected range | Completion gauge, accuracy gauge |

#### 4.5.3 Journey-Level Monitoring: How to Detect Common Failure Modes

Business process monitoring must answer specific detection questions. For each critical scenario, the table below defines what signals to watch and how the monitoring system detects the problem.

| Failure scenario | How we detect it | Signals combined | Alert severity |
|-----------------|------------------|-----------------|---------------|
| **Policy issuance is stuck** | No `policy_issued` events for > 1 hour during business hours, while `application_submitted` events continue arriving | Submit counter rising + issue counter flat + InsureMO API latency normal | SEV1 — new business is blocked |
| **Premium collection failed silently** | Auto-debit success rate drops below threshold, but no payment gateway error alerts fired (gateway reports success, but funds not collected) | Payment callback success rate dropping + bank reconciliation mismatch next morning | SEV1 — revenue leakage |
| **Underwriting queue is stalled** | Oldest pending case age exceeds SLA, referral backlog growing, but no rules-engine errors (cases are arriving but not being processed) | Referral backlog age rising + zero decisions in 30 min + no system errors | SEV2 — may be staffing or manual process issue, escalate to operations |
| **Rider mismatch at issuance** | Rider set on issued policy differs from rider set on accepted quote | Quote-to-issue rider reconciliation detects mismatch (daily batch or real-time event comparison) | SEV1 — policyholder has wrong coverage |
| **Surrender value calculation error** | Batch produces policies with surrender value outside actuarial expected range (e.g., zero surrender value) | Reconciliation batch flags deviation > threshold vs actuarial baseline | SEV1 — direct financial and regulatory impact (IM backlog scenario) |
| **NAV calculation missed deadline** | NAV batch not completed by 10:00 AM on business day | Batch completion timestamp > deadline threshold | SEV2 — policyholder statements and regulatory reporting affected |
| **Commission run failure** | Commission batch fails or produces agent count significantly below expected | Batch status = failed OR agent count deviation > 10% from expected | SEV2 — entire sales force compensation affected |
| **Document generation halted** | Document generation success rate drops to zero while policy issuance continues | Policy issued counter rising + document generation counter flat | SEV2 — policyholders not receiving policy packs |

#### 4.5.4 Rider Lifecycle Monitoring

For a UL-focused insurer with CI, HI, and MR riders, rider monitoring is a first-class dimension that cuts across multiple journeys. Rider defects create policyholder complaints, financial leakage, and regulatory risk (per Decree 46/2023 and Circular 67/2023 rider separation requirements).

| Rider lifecycle stage | Journey | What to monitor | Data source | Collection method | Alert trigger |
|----------------------|---------|----------------|-------------|-------------------|---------------|
| **Eligibility decision** | J2 Sales | Rider eligibility rule error %, mismatch between offer and rules | InsureMO rules engine + Sale Portal | Event on eligibility check; Prometheus counter by result | SEV2 if eligibility engine errors rise above threshold |
| **Premium computation** | J2 Sales | Rider premium calculation inputs, rider-package version, computation accuracy | InsureMO premium calc API | Event on premium computation; compare output vs expected range | SEV2 if premium calculation errors detected |
| **Offer display** | J2 Sales | Rider offer visibility %, offer acceptance rate by rider type | Sale Portal metrics | Prometheus counter on rider offers shown vs accepted | Business alert if offer visibility drops |
| **Attachment at quote** | J2 Sales | Rider attach rate by product/channel, rider conflict rate | Sale Portal + InsureMO | Counter on rider attach events; conflict detection on save | SEV3 on rising conflict rate |
| **Issuance** | J5 Policy | Rider issue success %, quote-to-issue rider mismatch, rider effective-date mismatch | InsureMO issuance API + reconciliation | Real-time event comparison or daily reconciliation batch | SEV1 if quote/issue rider mismatch exceeds threshold |
| **Premium posting** | J7 Billing | Rider premium posting %, rider premium allocation accuracy | InsureMO billing API + finance reconciliation | Batch reconciliation: rider premium posted vs expected | SEV1 on posting failure for riders |
| **Renewal** | J7 Billing | Rider renewal status, rider lapse distinct from base policy | InsureMO renewal processing | Daily query: riders not renewed while base policy active | Business alert on rider-specific lapse patterns |
| **Claimability** | J8 Claims | Rider claim events, rider-specific benefit payouts, rider coverage verification | InsureMO claims API | Event on rider claim submission; cross-check with active coverage | SEV2 if rider claimability status conflicts with active policy |

#### 4.5.5 Metric Segmentation

All business process metrics must be segmented by the following dimensions to enable meaningful analysis:

| Dimension | Examples | Why |
|-----------|---------|-----|
| **Channel** | Agency, bancassurance, digital direct, partner | Different channels have different volume patterns and SLAs |
| **Product** | UL, CI, HI, MR | Product-specific issues need product-specific routing |
| **Rider** | CI rider, HI rider, MR rider | Rider-level issues are distinct from base product issues |
| **Geography** | Province, region | Network quality and agent density vary across Vietnam |
| **Release version** | Application version tag | Enables immediate correlation between deploys and business metric changes |

> **Cardinality warning**: Use only stable business dimensions in Prometheus metrics. High-cardinality fields (agent ID, customer ID, free-text error messages) belong in OpenSearch logs, not Prometheus labels.

### 4.6 Security Monitoring

**Scope**: Threat detection, access anomalies, data exfiltration, compliance violations, fraud indicators.

TCLife holds policyholder PII, health data (for HI and MR products), and financial data. Security monitoring is not optional — it is a regulatory requirement under Vietnam's Cybersecurity Law 2018 and Decree 13/2023/ND-CP on personal data protection. Without a dedicated SIEM, TCLife uses OpenSearch as a SIEM-lite platform for security event aggregation, correlation, and alerting.

#### 4.6.1 AWS-Native Security Services Integration

| Service | What it detects | Integration | Phase | Alert routing |
|---------|----------------|-------------|-------|--------------|
| **GuardDuty** | Threat intelligence-based detection: unauthorized access, cryptocurrency mining, data exfiltration, compromised credentials, malicious IP contact | Enable in all regions -> EventBridge -> OpenSearch. Alert on High/Medium findings. | **Late Phase 1 (R-007)** — managed service, minimal setup | High findings -> SEV1 (immediate page); Medium -> SEV2 |
| **Security Hub** | Aggregated security posture: CIS benchmarks, PCI-DSS checks, best practices compliance | Enable with AWS Foundational Security Best Practices standard -> findings to OpenSearch | Phase 2 | Critical/High findings -> SEV2; review others weekly |
| **Inspector** | Vulnerability scanning of EC2 instances and container images | Enable for EKS workloads -> findings to Security Hub -> OpenSearch | Phase 2 | Critical CVEs on production workloads -> SEV2 |
| **Macie** | Sensitive data discovery in S3 (PII, health data in unexpected locations) | Enable on S3 buckets containing logs and exports -> findings to Security Hub | Phase 2-3 | Any PII/health data found in non-designated buckets -> SEV2 |
| **CloudTrail** | API activity logging for all AWS account actions | Already active -> route management events to OpenSearch; enable data events for S3 and Lambda in Phase 2 | Phase 1 (management), Phase 2 (data events) | Specific anomaly rules (see below) |
| **AWS Config** | Configuration compliance: detects drift from security baselines | Enable rules for critical resources (S3, RDS, IAM) -> non-compliant findings to Security Hub | Phase 2 | Non-compliant critical resource -> SEV3 |

#### 4.6.2 SIEM-Lite Approach with OpenSearch

TCLife does not have a dedicated SIEM (Splunk, Sentinel, etc.). OpenSearch serves as the centralized security event store with correlation and alerting capabilities.

**Data sources flowing into OpenSearch for security analysis**:

| Source | Log type | Volume estimate | Retention |
|--------|---------|----------------|-----------|
| CloudTrail | Management events, data events | Medium | 90 days hot, 5 years archive (S3) |
| GuardDuty findings | Threat detection findings | Low | 1 year hot, 5 years archive |
| WAF logs | Blocked/allowed request details | High during attacks | 30 days hot, 90 days archive |
| VPC Flow Logs | Network traffic metadata | High | 30 days hot, 90 days archive |
| Application auth logs | Login success/failure, session events | Medium | 90 days hot, 1 year archive |
| RDS audit logs | Database query audit trail | Medium-High | 90 days hot, 5 years archive |
| S3 access logs | Object-level access patterns | Medium | 90 days hot, 1 year archive |

**OpenSearch security alerting rules** (implement in Phase 2):

| Rule | Detection logic | Severity |
|------|----------------|----------|
| Root account login | CloudTrail: `userIdentity.type = "Root"` and event = `ConsoleLogin` | SEV1 — root login should never happen in normal operations |
| New IAM admin user created | CloudTrail: `CreateUser` or `AttachUserPolicy` with admin policy | SEV1 |
| IAM policy change on production | CloudTrail: `PutRolePolicy`, `AttachRolePolicy` on production roles | SEV2 |
| S3 bucket made public | CloudTrail: `PutBucketPolicy` or `PutBucketAcl` with public access | SEV1 |
| Brute force login attempts | Application logs: > 10 failed logins from same IP in 5 min | SEV2 |
| After-hours privileged access | CloudTrail: admin actions between 22:00-06:00 on weekdays or anytime on weekends | SEV2 |
| Mass data export | S3 access logs: > 1000 object downloads from single principal in 1 hour | SEV1 — potential data exfiltration |
| Security group modification | CloudTrail: `AuthorizeSecurityGroupIngress` opening 0.0.0.0/0 | SEV1 |

#### 4.6.3 PII and Sensitive Data Access Monitoring

TCLife processes health data (HI and MR claims), financial data (premium, NAV, surrender values), and personal identification data. Access to this data must be monitored.

| What to monitor | Detection method | Alert trigger | Owner |
|----------------|-----------------|---------------|-------|
| Sensitive data read volume | Track read operations on tables/S3 paths containing PII/health data | Volume > 2x baseline in 1 hour | SecOps / DPO |
| Unusual query patterns | RDS audit logs: queries on customer/claims tables from new or unusual principals | New principal accessing sensitive tables | SecOps |
| After-hours access | Application auth logs + database audit: access to customer data outside business hours | Any access to health/claims data between 22:00-06:00 without on-call justification | SecOps / DPO |
| Mass download attempts | S3 access logs + application logs: bulk export of customer records | > 100 customer records exported in single session | SEV1 — SecOps / DPO |
| PII in logs | Log scanning for patterns matching national ID, phone number, health data in non-designated log fields | Any unmasked PII detected in application logs | SEV2 — DevOps (fix masking) |
| Consent and privacy controls | Consent capture success, consent withdrawal processing, data-subject request SLA, deletion completion | Requests miss SLA (SEV2); consent control mechanism breaks (SEV1) | Compliance / DPO |

#### 4.6.4 Fraud Indicators

Insurance fraud detection is primarily a business function, but the monitoring system should surface early signals.

| Indicator | Detection method | Alert routing |
|-----------|-----------------|---------------|
| Duplicate identities | Application data: same national ID / phone / address with different customer records | Business alert to fraud team (daily report) |
| Repeated failed KYC | eKYC service: > 3 failed verifications from same device/IP in 24 hours | Business alert to fraud team |
| Payment anomalies | Payment gateway: card used across multiple policies with different holders | Business alert to fraud team |
| Suspicious claim clusters | Claims data: multiple claims from same hospital/provider in short period, or claims filed immediately after policy activation | Business alert to claims + fraud team (weekly analysis) |
| High-value application patterns | Unusually high sum assured applications with minimal documentation | Business alert to underwriting + fraud team |

#### 4.6.5 Security Monitoring Routing Table

| What to Monitor | Tool | Priority |
|----------------|------|----------|
| AWS GuardDuty findings | EventBridge -> OpenSearch | **Late Phase 1 (R-007)** |
| Security Hub findings | Security Hub -> OpenSearch | Phase 2 |
| WAF blocked requests and rate limiting | AWS WAF logs -> OpenSearch | Phase 2 |
| IAM anomalies (root login, admin users, policy changes) | CloudTrail -> OpenSearch | Phase 2 |
| Failed authentication attempts (brute force) | Application logs -> OpenSearch | Phase 2 |
| S3 public access or policy changes | CloudTrail -> OpenSearch + Config Rules | Phase 2 |
| Inspector vulnerability findings | Inspector -> Security Hub -> OpenSearch | Phase 2 |
| Macie sensitive data findings | Macie -> Security Hub -> OpenSearch | Phase 2-3 |
| Unusual database query patterns | RDS audit logs -> OpenSearch | Phase 3 |
| Data exfiltration signals (large data exports) | VPC Flow Logs + S3 access logs -> OpenSearch | Phase 3 |
| Certificate and key usage anomalies | CloudTrail -> OpenSearch | Phase 3 |
| **Monitoring stack access patterns (R-041)** | CloudTrail + Grafana audit logs | **Phase 2 — monitor who accesses the monitoring system itself** |

> _GuardDuty basic integration pulled into late Phase 1 per R-007. It is a managed service requiring minimal setup — enable, route findings to OpenSearch, alert on High-severity findings. Incremental effort is small; risk reduction is meaningful given TCLife handles policyholder PII and health data._

### 4.7 User Experience / Real User Monitoring (RUM)

> _New section — addresses R-003._

**Scope**: Actual end-user experience for Sale Portal and Customer Portal, captured from the browser/device.

**Why this matters**: Synthetic probes from inside the VPC cannot detect performance issues experienced by agents in remote areas of Vietnam (slow mobile networks, high latency, varied device quality). RUM captures what real users actually experience. For TCLife, where agents operate across all 63 provinces with varying network infrastructure, the gap between synthetic health and real-user experience can be substantial.

**Approach**: Grafana Faro (open-source RUM agent) or equivalent lightweight frontend instrumentation.

#### 4.7.1 Core Web Vitals with SLO Targets

| Metric | Description | Good | Needs Improvement | Poor | TCLife SLO Target |
|--------|------------|------|-------------------|------|------------------|
| **LCP** (Largest Contentful Paint) | Time until the largest content element is visible | < 2.5s | 2.5s - 4.0s | > 4.0s | 75th percentile < 2.5s |
| **FID** (First Input Delay) | Time from first user interaction to browser response | < 100ms | 100ms - 300ms | > 300ms | 75th percentile < 100ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — unexpected layout movements | < 0.1 | 0.1 - 0.25 | > 0.25 | 75th percentile < 0.1 |
| **TTFB** (Time to First Byte) | Server response time as experienced by the user | < 800ms | 800ms - 1.8s | > 1.8s | 75th percentile < 800ms |
| **FCP** (First Contentful Paint) | Time until first content is painted on screen | < 1.8s | 1.8s - 3.0s | > 3.0s | 75th percentile < 1.8s |

#### 4.7.2 Full RUM Metric Table

| What to Monitor | Metric | Source | Threshold (Alert) |
|----------------|--------|--------|-------------------|
| Page load time (LCP, FCP, TTFB) | Web Vitals metrics | Grafana Faro | LCP P75 > 4.0s sustained 15 min (SEV2) |
| JavaScript errors | Error count and type by page | Grafana Faro | JS error rate > 1% of sessions (SEV3); > 5% (SEV2) |
| Session drop-off / rage clicks | User frustration signals (rapid repeated clicks on same element) | Grafana Faro | Rage click rate > 5% of sessions on critical pages (SEV3) |
| Mobile vs desktop performance | Segmented load times by device class | Grafana Faro | Mobile LCP > 2x desktop LCP sustained (SEV3 — investigate) |
| Geographic performance (Vietnam regions) | Latency by province/region | Grafana Faro | Specific province P75 > 2x national average (SEV3) |
| API call latency (from browser) | XHR/Fetch timing by endpoint | Grafana Faro | API call P95 > 5s from browser (SEV3) |
| Login flow performance | End-to-end login duration including OTP | Grafana Faro | Login flow > 10s P75 (SEV2) |
| Quote/submission flow completion | Funnel completion rate by step | Grafana Faro | Step drop-off rate > 20% vs baseline (business alert) |
| Error boundary triggers | React error boundary activations | Grafana Faro | Any error boundary on critical page (SEV3) |

#### 4.7.3 Segmentation Dimensions

All RUM data must be segmented by the following dimensions to enable targeted diagnosis:

| Dimension | Values | Why |
|-----------|--------|-----|
| **Portal** | Sale Portal, Customer Portal | Different user populations and performance expectations |
| **Device type** | Desktop, Mobile, Tablet | Agents in the field use mobile; office agents use desktop |
| **Browser** | Chrome, Safari, Edge, Firefox, Samsung Internet | Browser-specific rendering issues |
| **OS** | Windows, macOS, Android, iOS | Mobile OS differences affect performance |
| **Network type** | WiFi, 4G, 3G (where available from Network Information API) | Agents in rural provinces may be on 3G |
| **Geography / Province** | Vietnam province or region grouping | Network infrastructure quality varies significantly |
| **Application version** | Frontend build version | Correlate performance regressions with specific releases |

#### 4.7.4 Alerting Thresholds for RUM

| Alert | Condition | Severity | Routing |
|-------|-----------|----------|---------|
| Portal performance degradation | LCP P75 > 4.0s for 15 min | SEV2 | Dev team + Ops |
| JS error spike | JS error rate doubles vs 7-day baseline for 10 min | SEV3 | Dev team |
| Login flow degradation | Login success rate < 95% AND login duration P75 > 10s for 10 min | SEV2 | Identity team + Ops |
| Geographic hotspot | Any province LCP P75 > 3x national median for 30 min | SEV3 | Ops (investigate CDN/routing) |
| Mobile-specific degradation | Mobile LCP P75 > 6s while desktop < 3s for 30 min | SEV3 | Dev team (mobile optimization) |
| Critical page error | Error boundary triggered on payment, submission, or claims page | SEV2 | Dev team |

**Phasing**:
- **Phase 2**: Foundation — deploy Faro agent on Sale Portal and Customer Portal; collect baseline data; establish initial segmentation
- **Phase 3**: Full — dashboards with geographic heatmaps, alerting on performance degradation, funnel analysis by segment
- **Phase 4**: Advanced — correlation with backend metrics, user journey tracking, proactive performance budgets per page

> _R-022 note: Engineering dashboard "JS error rates" metric for Sale Portal requires this RUM infrastructure. Until Phase 2, this metric comes from backend error logs only (incomplete view)._

### 4.8 AWS Cost Monitoring

> _New section — addresses R-004._

**Scope**: AWS spend anomaly detection, budget alerts, cost visibility in Grafana, insurance-specific cost pattern awareness.

**Why this matters**: For a fully AWS-hosted company, unexpected cost spikes (runaway Lambda, S3 storage explosion, RDS upsizing, data transfer charges) are operational events. Insurance operations have distinct cost patterns — batch processing windows consume significant compute, data replication generates transfer charges, and OpenSearch storage grows steadily with log retention.

#### 4.8.1 Core Cost Monitoring Components

| Component | Implementation | Phase |
|-----------|---------------|-------|
| CloudWatch Billing Alarms | Set budget thresholds; alert on exceeding 80%, 100% | **Phase 1** — simple to implement, immediate value |
| AWS Cost Anomaly Detection | Enable; route anomaly findings to Slack/email | **Phase 1** |
| Cost dashboard in Grafana | CloudWatch billing metrics visualized in Grafana | **Phase 1** |
| Service-level cost breakdown | Cost Explorer data surfaced per service (EKS, RDS, OpenSearch, S3, Lambda) | **Phase 2** |
| Monitoring stack cost tracking | Dedicated dashboard for AMP, AMG, OpenSearch, CloudWatch costs | **Phase 4** — optimize after steady state reached |

#### 4.8.2 Insurance-Specific Cost Anomaly Scenarios

| Scenario | Root cause pattern | Detection method | Alert |
|----------|-------------------|-----------------|-------|
| **Batch processing cost spike** | End-of-month batch runs (commission, GL, regulatory reports) consume more compute than expected; stuck batch job runs indefinitely | Cost Anomaly Detection + batch job duration monitoring | SEV3 if cost > 150% of expected batch window; SEV2 if batch job runs > 3x expected duration (compute waste) |
| **Data transfer during replication** | Cross-region or cross-AZ data transfer charges from database replication, S3 replication, or log shipping | CloudWatch billing: data transfer line item trending up | SEV3 if data transfer cost increases > 30% month-over-month |
| **OpenSearch storage growth** | Log volume grows as monitoring coverage expands; retention policies not tuned | OpenSearch cluster storage utilization + billing | SEV3 at 70% storage; review retention policies. Budget impact review quarterly. |
| **Lambda invocation runaway** | Failed Lambda retries in a loop (e.g., DLQ handler or event-driven function with bad data) | Lambda invocation count spike + cost anomaly | SEV2 if invocation count > 10x baseline in 1 hour |
| **RDS storage auto-scaling** | RDS storage auto-scales beyond budget due to slow query log growth, audit log volume, or data growth | RDS allocated storage metric vs budget | SEV3 when RDS storage reaches 80% of budgeted maximum |
| **EKS node group over-provisioning** | HPA scales out during peak but does not scale in (incorrect scale-down configuration) | Node count vs workload utilization off-peak | SEV4 (informational) — review in monthly cost analysis |

#### 4.8.3 Reserved Capacity vs On-Demand Tracking

| Resource | Current commitment | What to track | Review frequency |
|----------|-------------------|---------------|-----------------|
| RDS instances | Document current RI/Savings Plan status | On-demand hours vs reserved hours; RI utilization % | Quarterly |
| EKS node group EC2 | Document current RI/Savings Plan status | On-demand instance hours; spot instance interruptions if using spot | Quarterly |
| OpenSearch | Document current RI status | Reserved vs on-demand node hours; storage tier utilization | Quarterly |
| Data transfer | No commitment model | Cross-AZ and cross-region transfer trends | Monthly |

**Cost governance**: Include a cost summary panel in the monthly SLA report (Section 10.5). Flag any service where actual spend exceeds budget by > 20%. Cost optimization decisions (e.g., purchasing reserved capacity, adjusting retention policies, right-sizing instances) should be reviewed quarterly by IT Manager and CIO.

---

## 5. Alerting Strategy

### 5.1 Severity Levels

Alerting severity aligns with the incident classification system defined in `solutions/incident-management/classification.md`:

| Alert Severity | Maps to Incident Priority | Response Expectation | Insurance-Specific Examples |
|---------------|--------------------------|---------------------|---------------------------|
| **SEV1 — Critical** | P1 | Immediate page; 15-min response | Sale Portal or Customer Portal completely down; application submit or payment callback halted (new business blocked); data breach with policyholder PII/health data exposure; InsureMO core system unreachable (all operations stopped); rider mismatch between quote and issued policy (wrong coverage delivered); auto-debit gateway failure affecting all premium collections |
| **SEV2 — Major** | P2 | Urgent notification; 30-min response | Significant portal degradation (P95 latency > 3x normal); STP rate collapses > 10 pts (underwriting queue building); batch job SLA at risk (GL, commission, regulatory report); RDS connection pool exhaustion; DLQ messages accumulating on business-critical queues; surrender value calculation batch produces unexpected results |
| **SEV3 — Warning** | P3 | Business hours notification; 2-hr response | Elevated 5xx error rate on non-critical endpoint; cache hit ratio dropping; single province experiencing slow portal performance; quota approaching for individual agent; certificate expiry < 30 days; cost anomaly detected but not impacting service |
| **SEV4 — Info** | P4 / no incident | Logged for review; no immediate action | Transient metric deviation; OpenSearch storage approaching threshold; rider attach rate slightly below historical average; single failed KYC attempt; deployment completed successfully |

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
| **Document every alert** | Each alert rule has a linked runbook explaining: what it means, what to check, how to resolve (see Section 5.7 for template) |
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

  # If RDS is down, suppress application-level database error alerts
  - source_matchers: [severity="critical", alertname="RDSConnectionFailure"]
    target_matchers: [alertname=~"SlowQuery.*|AppDatabaseError.*"]

  # If payment gateway is down, suppress individual payment failure alerts
  - source_matchers: [alertname="PaymentGatewayDown"]
    target_matchers: [alertname=~"PremiumCollection.*|PaymentCallback.*"]

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

### 5.6 Alert Lifecycle Management

Every alert follows a defined lifecycle from firing to post-mortem. Clear state transitions ensure alerts are not forgotten, responsibility is explicit, and resolution is tracked.

#### 5.6.1 Alert States

```
  FIRING ─────► ACKNOWLEDGED ─────► INVESTIGATING ─────► RESOLVED ─────► POST-MORTEM
    │               │                     │                   │               │
    │  On-call acks │  Responder begins   │  Issue fixed,     │  For SEV1/2:  │
    │  within SLA   │  diagnosis work     │  monitoring       │  RCA within   │
    │               │                     │  confirms normal  │  5 biz days   │
    │               │                     │                   │               │
    └── Auto-escalate if not acked ───────┘                   │               │
                                                              │               │
    If alert re-fires within 24h of resolve ─────────────────►│ REOPENED      │
```

#### 5.6.2 State Transition Rules

| State | Who transitions | When | Required actions |
|-------|----------------|------|-----------------|
| **Firing** | System (Alertmanager/PagerDuty) | Alert condition met | Alert delivered to routing targets |
| **Acknowledged** | On-call engineer | Within SLA (15 min SEV1, 30 min SEV2) | Engineer confirms they are aware and investigating. If they cannot handle, must escalate immediately. |
| **Investigating** | Responder | After initial triage | Update incident channel with initial assessment: scope, impact, and estimated time to resolution |
| **Resolved** | Responder | When monitoring confirms the condition has cleared | Document what was done. If a workaround was applied, create a follow-up ticket for root fix. |
| **Post-mortem** | Incident Commander or Service Quality | Within 5 business days for SEV1/SEV2 | Complete RCA document. Identify action items. Update runbooks if needed. |

#### 5.6.3 ITSM Integration

| Severity | ITSM behavior |
|----------|--------------|
| **SEV1** | Auto-create P1 incident ticket when alert fires. Link alert ID to ticket. Ticket must be resolved before alert can be closed. |
| **SEV2** | Auto-create P2 incident ticket when alert fires. Same linking and resolution requirement. |
| **SEV3** | Create ticket only if alert persists > 4 hours or on-call engineer manually escalates. |
| **SEV4** | No ticket. Reviewed in weekly alert review. |

**Implementation**: PagerDuty/OpsGenie webhook creates ITSM ticket on SEV1/SEV2 alert creation. Ticket ID is attached to the alert as an annotation. When the alert resolves, the ITSM ticket is updated but not auto-closed (human must confirm resolution).

### 5.7 Alert Runbook Template

Every alert rule must have an associated runbook. No alert goes to production without a runbook. The runbook is linked from the alert notification (PagerDuty/OpsGenie custom field or Alertmanager annotation).

#### 5.7.1 Standard Runbook Template

```markdown
# Runbook: {alert_name}

## Overview
- **Alert name**: {alert_name}
- **Severity**: {SEV1|SEV2|SEV3|SEV4}
- **Owner team**: {team}
- **Last updated**: {date}
- **Related SLO**: {SLO name if applicable}

## What is happening?
{Plain-language description of what this alert means. Include business impact.}

## Who is affected?
{Policyholders? Agents? Internal operations? Regulatory reporting? Which product lines?}

## Investigation steps
1. {Step 1: Check dashboard X — link}
2. {Step 2: Check log query Y — link}
3. {Step 3: Verify dependent service Z status}
4. {Step 4: Check recent deployments — link to deploy dashboard}

## Common causes and fixes
| Cause | How to confirm | Fix |
|-------|---------------|-----|
| {Cause 1} | {Diagnostic step} | {Resolution step} |
| {Cause 2} | {Diagnostic step} | {Resolution step} |
| {Cause 3} | {Diagnostic step} | {Resolution step} |

## Escalation
- If not resolved within {X minutes}: escalate to {team/person}
- If vendor-related: contact {vendor} at {contact info}
- If data integrity issue: involve {data team} immediately

## Related alerts
- {List of alerts that often fire together or are related}

## History
- {Date}: {Notable incident and resolution}
```

#### 5.7.2 Example Runbook: RDS Connection Pool Exhausted

```markdown
# Runbook: infra_rds_connection_pool_exhausted

## Overview
- **Alert name**: infra_rds_connection_pool_exhausted
- **Severity**: SEV2
- **Owner team**: DevOps / Platform
- **Last updated**: 2026-03-20
- **Related SLO**: Customer Portal availability (99.9%), Sale Portal availability (99.95%)

## What is happening?
RDS database connections have exceeded 80% of the maximum allowed connections.
Application services are likely experiencing connection timeouts or slow query
performance. If connections reach 100%, new requests will fail entirely.

## Who is affected?
All portal users (agents and policyholders). All business processes that
require database access (policy issuance, claims, premium collection, quotation).

## Investigation steps
1. Check RDS CloudWatch dashboard: DatabaseConnections metric
   Link: {Grafana dashboard URL}
2. Check application connection pool metrics (HikariCP active/pending)
   Link: {Grafana dashboard URL}
3. Check for long-running queries in Performance Insights
   Link: {AWS Console Performance Insights URL}
4. Check if a batch job is running that may consume extra connections
5. Check recent deployments that may have changed pool configuration

## Common causes and fixes
| Cause | How to confirm | Fix |
|-------|---------------|-----|
| Batch job consuming connections | Check batch job dashboard for running jobs | Wait for batch completion or terminate if stuck |
| Connection leak in application | HikariCP pending connections rising while active is stable | Restart affected application pods (rolling restart) |
| Slow queries holding connections | Performance Insights shows long-running queries | Identify and kill blocking queries; create follow-up ticket for query optimization |
| Pool misconfiguration after deploy | Recent deployment changed pool settings | Rollback deployment or adjust pool configuration |

## Escalation
- If not resolved within 30 minutes: escalate to IT Manager
- If connection count reaches 95%: escalate immediately to SEV1
- If root cause is database performance: engage AWS support

## Related alerts
- infra_rds_cpu_high
- app_slow_query_spike
- app_portal_error_rate_high

## History
- (No incidents recorded yet — update after first occurrence)
```

### 5.8 Alert Naming Convention

Consistent alert naming enables filtering, routing, and analysis. Every alert follows a standard naming pattern.

#### 5.8.1 Naming Format

```
{domain}_{service}_{condition}
```

**Examples**:
- `infra_rds_connection_pool_exhausted`
- `infra_eks_node_not_ready`
- `infra_alb_5xx_rate_high`
- `app_sale_portal_error_rate_high`
- `app_customer_portal_login_success_low`
- `biz_policy_issuance_halted`
- `biz_premium_collection_success_low`
- `biz_rider_quote_issue_mismatch`
- `biz_commission_run_failed`
- `sec_guardduty_high_finding`
- `sec_iam_root_login`
- `sec_pii_mass_download`
- `batch_gl_posting_failed`
- `batch_nav_calculation_late`

#### 5.8.2 Label Taxonomy

Every alert must carry the following labels:

| Label | Purpose | Values |
|-------|---------|--------|
| `severity` | Routing and escalation | `critical`, `major`, `warning`, `info` |
| `domain` | Top-level category | `infra`, `app`, `biz`, `sec`, `batch`, `cost` |
| `team` | Responsible team for routing | `devops`, `appops`, `security`, `business`, `vendor` |
| `service` | Affected service or component | `sale_portal`, `customer_portal`, `rds`, `eks`, `insuremo`, `payment_gateway` |
| `environment` | Deployment environment | `prod`, `staging`, `dr` |
| `product` | Insurance product (if applicable) | `ul`, `ci`, `hi`, `mr`, `all` |
| `channel` | Distribution channel (if applicable) | `agency`, `bancassurance`, `digital`, `all` |

### 5.9 Escalation Flow

#### 5.9.1 Escalation Flowchart

```
  ALERT FIRES
       │
       ▼
  ┌─────────────────────────────────┐
  │  Delivered to on-call via       │
  │  PagerDuty/OpsGenie             │
  └──────────────┬──────────────────┘
                 │
       ┌─────────┴──────────┐
       │                    │
       ▼                    ▼
  ACKNOWLEDGED         NOT ACKNOWLEDGED
  within SLA           within SLA
       │                    │
       ▼                    ▼
  ┌────────────┐    ┌──────────────────────┐
  │  TRIAGE    │    │  AUTO-ESCALATION     │
  │            │    │  SEV1: 15 min -> CIO │
  │  Can I     │    │  SEV2: 30 min -> ITM │
  │  resolve?  │    └──────────────────────┘
  └──┬─────┬───┘
     │     │
     ▼     ▼
   YES     NO
     │     │
     ▼     ▼
  RESOLVE  ESCALATE MANUALLY
     │     │
     │     ├── Vendor issue? ──► Contact EbaoTech / AWS support
     │     ├── App code issue? ──► Dev team
     │     ├── Security event? ──► IT Manager + Security
     │     ├── Business impact? ──► Business stakeholder
     │     └── Cross-team? ──► Incident Commander
     │
     ▼
  CONFIRM RESOLUTION
  (monitoring shows normal)
     │
     ▼
  CLOSE ALERT
     │
     ├── SEV1/SEV2: Post-mortem within 5 business days
     └── SEV3: Update runbook if new root cause found
```

#### 5.9.2 Time-Based Auto-Escalation Rules

| Condition | Escalation action |
|-----------|------------------|
| SEV1 not acknowledged in 15 min | Page IT Manager + CIO via SMS and phone |
| SEV1 not resolved in 1 hour | CIO notified; bridge call initiated |
| SEV1 not resolved in 4 hours | Executive escalation; vendor engagement if applicable |
| SEV2 not acknowledged in 30 min | Page IT Manager |
| SEV2 not resolved in 2 hours | IT Manager reviews; considers upgrading to SEV1 |
| SEV3 not resolved in 24 hours | Team lead review in daily standup |

#### 5.9.3 Business Hours vs After-Hours Behavior

| Severity | Business hours (08:00-18:00 Mon-Fri) | After hours (18:00-08:00, weekends, holidays) |
|----------|-------------------------------------|-----------------------------------------------|
| **SEV1** | Immediate page to on-call + IT Manager | Immediate page to on-call; auto-escalate to IT Manager at 15 min; CIO SMS at 30 min |
| **SEV2** | Immediate page to on-call | Page on-call; auto-escalate to IT Manager at 30 min. If non-time-sensitive (e.g., batch job that can retry in morning), on-call may defer to next business day with documented justification. |
| **SEV3** | Slack notification; daily standup review | No notification. Queued for next business day review. |
| **SEV4** | Slack low-priority channel | No notification. Weekly review only. |

### 5.10 Alert Testing Strategy

Alerts are production code. Untested alerts give false confidence. TCLife must validate that alerts fire correctly, reach the right people, and produce actionable notifications.

#### 5.10.1 Alert Rule Unit Testing

Before deploying any new or modified alert rule to production:

| Test type | How | When | Owner |
|-----------|-----|------|-------|
| **Syntax validation** | `promtool check rules <file>` for Prometheus rules; OpenSearch alerting API validation | Before every rule deployment | DevOps |
| **Threshold validation** | Replay historical metrics against the new rule to verify it would have fired (or not) at the correct times | Before every new alert | DevOps + Service Quality |
| **Routing validation** | Send a test alert through Alertmanager to verify it reaches the correct PagerDuty/Slack channel | Before every new alert | DevOps |
| **Runbook validation** | Walk through the runbook steps and verify all dashboard links and log queries work | Before every new alert | App Ops |
| **Inhibition testing** | Verify that child alerts are correctly suppressed when parent alert fires | After any inhibition rule change | DevOps |

#### 5.10.2 Game Day Exercises

Periodic game days validate that the end-to-end alerting pipeline works: alert fires, notification reaches on-call, responder follows runbook, resolution is achieved.

| Exercise | Frequency | Scope | Owner |
|----------|-----------|-------|-------|
| **Alert delivery test** | Monthly | Fire a synthetic SEV2 alert; verify it reaches on-call via PagerDuty/OpsGenie; verify Slack notification; verify ITSM ticket creation | Service Quality |
| **Tabletop incident drill** | Quarterly | Walk through a realistic incident scenario (e.g., "InsureMO API is unreachable") without actually breaking production. Review what alerts would fire, who responds, what runbooks to follow. | IT Manager + Service Quality |
| **Controlled fault injection** (Phase 3+) | Semi-annually | Introduce a controlled failure in staging (e.g., kill a pod, saturate a queue) and verify detection, alerting, and response. | DevOps |
| **On-call handoff drill** | With each new on-call rotation | New on-call confirms they can access PagerDuty, Grafana, OpenSearch, and runbooks; reviews active alerts and recent incidents | App Ops |

#### 5.10.3 Alert Rule Promotion Process

```
DEV/LOCAL ──► STAGING ──► PRODUCTION
   │              │            │
   Test with      Run for      Monitor for
   synthetic      3-5 days     30 days;
   data           to validate  tune thresholds
                  thresholds   based on
                  against      actual behavior
                  real-like
                  traffic
```

### 5.11 Alert Noise Management

Alert fatigue is the primary threat to alerting effectiveness. If the on-call engineer receives 50 alerts per shift, they will ignore all of them. TCLife targets a high signal-to-noise ratio from day one.

#### 5.11.1 Composite Alert Patterns

Single-metric alerts generate noise. A brief dip in submit success rate might be a network blip; a brief rise in queue backlog might be a normal batch cycle. Composite alerts combine multiple signals to page only when the evidence of real customer or business harm is strong.

| Composite alert | Signals combined | Page when | Rationale |
|----------------|-----------------|-----------|-----------|
| **Sales submission blocked** | Application submit success falls AND underwriting queue backlog rises AND no successful policy issuance events observed | All three conditions true for > 10 min | Single signal may be transient; three signals together confirm end-to-end blockage |
| **Payment pipeline failure** | Payment callback failures rise AND premium posting halted AND duplicate-charge anomaly detected | Two of three conditions true for > 5 min | Prevents paging on transient gateway blips while catching real payment outages |
| **Underwriting stall** | STP rate drops > 5 pts AND oldest case age exceeds SLA AND rules-engine error count rising | First two conditions true for > 30 min | STP dips can be caused by product mix; adding rules-engine errors confirms systemic issue |
| **Portal degradation** | Synthetic check fails AND RUM page load P95 degrades > 50% AND login success drops | Synthetic failure + one of the other conditions | Synthetic-only alerting catches hard down; adding RUM/login catches soft degradation |
| **Batch job chain failure** | GL batch fails AND premium reconciliation shows mismatch AND NAV calculation not started by deadline | Any two conditions true | Batch failures often cascade; composite alert identifies chain failures before downstream impact |

**Implementation**: Composite alerts require the underlying single-metric alerts to exist first (Phase 1-2). Composite logic is layered on top in Phase 2-3 using Alertmanager recording rules or Grafana alert rules with multiple conditions. Use anomaly detection (not static thresholds) for business metrics that vary by time of day, day of week, or season.

> _Detailed composite alert implementation patterns are in Section 23._

#### 5.11.2 Noise Budget

Define a target ratio of actionable alerts to total alerts. Track and review monthly.

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Actionable alert ratio** | > 80% of all alerts result in human action | Weekly review: count alerts that led to investigation or resolution vs total alerts |
| **False positive rate** | < 20% | Weekly review: count alerts that required no action and were not informational |
| **Alerts per on-call shift** | < 10 SEV1/SEV2 alerts per 8-hour shift | PagerDuty/OpsGenie reporting |
| **Flapping alert count** | 0 flapping alerts sustained > 7 days | Alertmanager metrics: alerts that fire and resolve repeatedly |
| **Time to tune** | < 5 business days from identification to threshold adjustment | Track in alert review process |

#### 5.11.3 Monthly Alert Quality Report

Service Quality produces a monthly alert quality report. Template:

| Section | Content |
|---------|---------|
| **Summary** | Total alerts by severity; actionable ratio; false positive count; top 5 noisiest alerts |
| **New alerts deployed** | List of new alert rules added this month; initial performance assessment |
| **Alerts tuned** | Threshold adjustments made; before/after false positive comparison |
| **Alerts retired** | Alert rules removed and rationale |
| **Top incidents detected by alerting** | SEV1/SEV2 incidents first detected by monitoring (vs user-reported) |
| **Missed incidents** | Any SEV1/SEV2 incident NOT detected by monitoring — root cause and gap analysis |
| **Recommendations** | New alerts to create, thresholds to adjust, runbooks to update |

### 5.12 Business Alert Routing

Not all alerts go to engineers. Business anomalies — changes in conversion rates, underwriting mix shifts, collection pattern changes — should route to business stakeholders who can interpret and act on them.

#### 5.12.1 Technical vs Business Alert Distinction

| Alert type | Definition | Routing | Response expectation |
|-----------|-----------|---------|---------------------|
| **Technical alert** | Infrastructure, platform, or application health issue that requires engineering intervention | SRE / DevOps / App Ops on-call via PagerDuty | Immediate (SEV1/2) or business hours (SEV3/4) |
| **Business alert** | Business metric anomaly that requires domain expertise to interpret and act on | Business team queue via Slack channel or email | Business hours review; daily or weekly depending on urgency |

#### 5.12.2 Business Alert Routing Matrix

| Business alert | Routing target | Channel | Frequency |
|---------------|---------------|---------|-----------|
| STP rate dropped > 5 pts vs baseline | Underwriting desk + Rules owner | Slack #underwriting-alerts + email | Real-time during business hours |
| Quote-to-proposal conversion drop > 10 pts | Sales Operations | Slack #sales-ops-alerts | Hourly digest during business hours |
| Auto-debit success rate below threshold | Collections + Finance | Slack #collections-alerts + email | Real-time |
| Lapse rate spike for a cohort | Collections + Actuarial + Sales | Email report | Daily |
| Claims decision mix anomaly (sudden shift in approve/reject ratio) | Claims leadership + Fraud team | Slack #claims-alerts | Real-time during business hours |
| Free-look/early cancellation spike by agent or channel | Sales leadership + Compliance | Email report | Daily |
| Rider attach rate change by product/channel | Product team + Sales Ops | Slack #product-alerts | Daily digest |
| Commission run discrepancy | Sales Operations + Finance | Slack #sales-ops-alerts + email | Immediately after commission run |
| Regulatory report generation at risk | Compliance + IT Manager | Slack #compliance-alerts + email | At T-5 and T-2 days |

#### 5.12.3 Business Alert Format

Business alerts must be understandable by non-technical stakeholders. Include:

- **What changed**: Plain-language description of the metric shift
- **Magnitude**: Current value vs baseline/expected value
- **Since when**: When the anomaly started
- **Affected scope**: Which product, channel, geography, agent group
- **Suggested action**: What the business stakeholder should investigate
- **Dashboard link**: Direct link to the relevant Grafana dashboard

**Example business alert**:
```
ALERT: STP Rate Drop — Underwriting

STP rate for UL product (agency channel) has dropped from 72% to 58%
over the past 2 hours. This is the largest drop in 30 days.

Affected: UL product, agency channel, all provinces
Since: 2026-03-20 10:30
Current: 58% (baseline: 72%)

Suggested action: Check if a rule configuration change was deployed.
Review referral reasons for new referrals in the past 2 hours.

Dashboard: {link}
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

### 7.3 InsureMO Business Event Instrumentation Checklist

Beyond the health prober, TCLife must ensure that business events are emitted at every policy-lifecycle transition — either from InsureMO directly (if configurable) or from the integration layer that calls InsureMO. These events form the foundation of journey monitoring (Section 18).

**Required business events to capture**:

| Event | Key fields | Journey |
|-------|-----------|---------|
| `quote_created` / `quote_saved` | quote_id, product, rider set, premium amount, sum assured, channel | J1, J2 |
| `application_submitted` | application_id, product, rider set, required fields completion %, document completeness | J2 |
| `kyc_passed` / `kyc_failed` | KYC provider, status, retries, OCR confidence, liveness result | J3 |
| `payment_authorized` / `payment_captured` | transaction_id, gateway, amount, authorization result, duplicate-payment flag | J3 |
| `underwriting_referred` / `underwriting_decided` | case_id, STP/manual/referral path, rules triggered, decision, TAT | J4 |
| `policy_issued` | policy_id, issuance timestamp, effective date, schedule creation | J5 |
| `rider_issued` / `rider_activated` | rider_code, rider eligibility result, rider premium, attach/detach status, rider-package version | J5 |
| `document_delivered` | template version, product/rider version, delivery channel, acknowledgement status | J5 |
| `premium_posted` / `premium_collected` | installment schedule, collection attempt result, auto-debit success | J7 |
| `renewal_due` / `lapse_started` / `reinstated` | policy_id, grace status, arrears bucket, lapse/reinstatement status | J7 |
| `claim_registered` / `claim_paid` | claim_id, event type, FNOL timestamp, triage result, payout turnaround | J8 |

**For every InsureMO API call, capture**: endpoint, operation name, business object, request ID, correlation ID, latency, response code, idempotency key, retry count, failure class, vendor/service dependency, release version.

**For rider logic specifically, capture**: rider eligibility decision, premium computation inputs, rider-package version, offer shown, offer accepted, rider issue result, and downstream claimability status.

**For every cross-system update**: store before/after status and reconciliation markers so silent sync failures are visible.

### 7.4 Limitations to Acknowledge

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
| **Auto-debit success rate drop** | Auto-debit success % below threshold or gateway-wide failure | **SEV1 (gateway failure) / SEV2 (success dip)** |

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
| **Insurance business information systems** | Insurance Business Law 08/2022/QH15 (effective 01/01/2023) — requires insurers to establish, maintain, and operate information systems appropriate to scale; support updating, processing, storing, and securing insurance information; provide data to national insurance business database (pending Legal review) | Observability must cover both business process completeness and evidentiary audit trails. Technology use is explicitly framed across product design, risk assessment, underwriting, contracting, policy admin, loss assessment, claims, statistics, reporting, and anti-fraud. |
| **Business continuity** | Circular 125/2018/TT-BTC and related MOF guidance on IT risk management for insurers (pending Legal review) | Must demonstrate system availability measurement and incident response capability |
| **Data protection** | Cybersecurity Law 2018, Decree 13/2023/ND-CP on personal data protection (pending Legal review) | Must detect and report data breaches; monitoring must cover access anomalies and data exfiltration signals; **breach notification timelines, data processing logs, and cross-border data transfer monitoring requirements apply (R-027)**. Must cover consent events, PII/health-data access, export, retention, data deletion, and third-party processing. |
| **Product rules and rider separation** | Decree 46/2023 and Circular 67/2023 — from 1 July 2025, investment-linked life products are expected to separate core benefits from supplementary riders (CI, accident, hospitalization) (pending Legal review) | Monitoring must treat rider attachment, eligibility, pricing, issuance, renewal, and claimability as first-class telemetry dimensions. Rider defects carry regulatory as well as operational risk. |
| **Financial reporting accuracy** | Insurance Law 08/2022/QH15, Circular 50/2017/TT-BTC (pending Legal review) | Must ensure accuracy of financial data processing — monitoring of GL, NAV, premium, and claims calculations |
| **Digital distribution targets** | Decision 07/QD-TTg — Vietnam 2030 insurance market strategy targets average 10% annual growth in insurance products distributed via digital channels (2023-2030) (pending Legal review) | Digital sales-path reliability is a board-level KPI, not just an IT KPI. Portal availability and conversion funnel monitoring are strategic. |
| **Operational risk management** | MOF guidelines on operational risk for financial institutions (pending Legal review) | Must demonstrate operational risk controls including system monitoring and incident management |
| **Outsourcing and vendor management** | MOF guidance on outsourcing of critical functions (pending Legal review) | Must independently monitor vendor-managed systems (Insuremo) and track vendor SLA compliance |
| **IT risk management** | **Circular 09/2020/TT-NHNN or insurance-sector equivalent (pending Legal review) (R-027)** | **IT risk management requirements for financial institutions — may mandate specific monitoring and reporting controls** |
| **Insurance data and reporting** | Circular 67/2023/TT-BTC — insurance data/reporting templates including life-insurance insured-person and risk data dimensions (age, gender, smoking status, insured risks, policy year statistics) (pending Legal review) | Monitoring should ensure data completeness for regulatory reporting templates. Batch monitoring must verify report generation and submission timeliness. |

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
- First 17 alerts from the prioritized list (Section 21) deployed and tested
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
| **Alerts 18-25 deployment** | Deploy remaining alerts from the prioritized list (Section 21): rider mismatch, STP drop, UW backlog, queue backlog, doc generation, delivery success, privileged access, WAF surge | DevOps + App Ops | Alerts 18-25 active and tested |
| **SLO measurement foundation** | Establish SLI measurement for the starter SLO set (Section 20): portal availability, login, quote, submit, payment callback, issuance | DevOps + Service Quality | SLI data being collected; 30-day baselines building |
| **InsureMO business event instrumentation** | Implement business event capture per Section 7.3 checklist for key InsureMO API touchpoints | DevOps + Integration | Business events emitted for quote, submit, payment, issuance, rider activation |

**Phase 2 exit criteria**:
- Application-level alerts detect error rate spikes and latency degradation before users report
- Insuremo health prober running in production with 30-day baseline
- Security events from GuardDuty, WAF, and CloudTrail are centralized and alerting
- Log-based alerting catches critical error patterns
- PII scrubbing active in log pipeline
- RUM baseline data available
- Basic compliance evidence available
- First 25 alerts all deployed (Section 21)
- SLO measurement infrastructure in place; SLI baselines building

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
| **Journey monitoring dashboards** | Build end-to-end journey health views for J2 (sales submission), J4 (underwriting), J5 (policy issuance), J7 (billing/persistency) per Section 18 | Service Quality + DevOps | Journey-level dashboards showing end-to-end flow health |
| **Rider monitoring** | Implement rider lifecycle monitoring per Section 18.3: eligibility, pricing, issuance, quote-to-issue consistency, renewal, claimability | DevOps + App Ops | Rider metrics visible; quote/issue mismatch alerting active |
| **SLO targets and tracking** | Set formal SLO targets per Section 20; configure error budget tracking and burn rate alerts | Service Quality + DevOps | SLO dashboard live; error budget burn alerts active |
| **Domain monitoring matrices** | Implement underwriting/STP, billing/persistency, ops workflow monitoring per Section 19 | App Ops + Service Quality | Domain dashboards operational with alert coverage |
| **Composite alert patterns** | Implement multi-signal alerts per Section 23: sales submission blocked, payment pipeline failure, underwriting stall, portal degradation | DevOps | Composite alerts reduce noise vs. single-metric paging |

**Phase 3 exit criteria**:
- Every daily batch job has automated monitoring with SLA alerting
- Commission batch is tracked and alerted
- Business process KPIs (policy issuance, claims, premium) are visible and trended
- Reconciliation mismatches generate alerts within 2 hours of batch completion
- CIO dashboard provides single-pane view of business + system health
- Regulatory filing countdown active
- Journey-level monitoring operational for J2, J4, J5, J7
- Rider lifecycle monitoring operational with quote-to-issue mismatch alerting
- SLO targets set and error budget tracking active
- Composite alerts deployed for critical business flows

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

## 18. Core Business Journeys to Monitor

> _New section in v2.1. Adapted from insurance-domain monitoring research (see `reference.research.md`)._

### 18.1 Design Principle

Monitor by customer journey first, service second. A healthy microservice estate can still hide a broken submit flow or underwriting queue. Every journey uses a unique journey ID / application ID / policy ID / rider instance ID to stitch events end-to-end across portals, InsureMO services, underwriting engines, payment, messaging, and document services.

### 18.2 Journey Definitions

| Journey | Critical span to trace | Key metrics | Phase |
|---------|----------------------|-------------|-------|
| **J1 Digital acquisition** | Landing > product browse > quote/illustration start > lead capture > agent assignment / digital direct continuation | Lead capture rate, agent assignment latency, quote start rate | Phase 3 |
| **J2 Sales submission** | Illustration > rider selection > proposal save > document upload > declaration > payment init > application submit | Submit success %, save failure %, premium calc latency, rider conflict rate, incomplete submission rate | Phase 2-3 |
| **J3 Identity & payment** | eKYC / liveness / OCR > payment auth/capture > callback > receipt issuance | eKYC pass rate, payment callback success %, duplicate charge count, receipt generation success | Phase 2-3 |
| **J4 Underwriting** | STP rules > referrals > manual underwriting > evidence requests > decision > offer / counter-offer / reject | STP rate by product/channel/rider, decision TAT (P50/P95), referral backlog age, rules-engine error count, decision mix | Phase 3 |
| **J5 Policy issuance** | Policy number generation > schedule/accounting posting > document generation > delivery/acknowledgement > rider activation | Issue success %, duplicate policy number, posting success, document generation success, rider activation success %, rider effective-date mismatch | Phase 3 |
| **J6 After-sales servicing** | Contact changes, beneficiary change, premium mode change, loan/withdrawal/top-up, rider add/drop where allowed | Endorsement completion %, profile change success %, servicing SLA adherence | Phase 3 |
| **J7 Billing & persistency** | Renewal due > debit attempt > grace > arrears > reinstatement / lapse | Auto-debit success %, grace count, aging buckets, lapse rate, reinstatement rate, premium at risk | Phase 3 |
| **J8 Claims & benefits** | FNOL > intake > assessment > fraud checks > approval/reject > payment | FNOL submission success, claims backlog by age, approve/pend/reject mix, payout success, reopen rate | Phase 3-4 |
| **J9 Agent/Ops productivity** | Queue receive > case work > handoff > closure > quality check | Queue backlog, oldest item age, SLA breach count, manual rework rate, exception taxonomy | Phase 3 |

### 18.3 Rider Monitoring as a Cross-Cutting Dimension

For a UL-focused insurer with CI, HI, and MR riders, rider monitoring is not a sub-item of policy monitoring — it is a first-class dimension that cuts across multiple journeys.

| Rider lifecycle stage | Journey | What to monitor | Alert trigger |
|----------------------|---------|----------------|---------------|
| **Eligibility decision** | J2 | Rider eligibility rule error %, mismatch between offer and rules | P2 if eligibility engine errors rise above threshold |
| **Premium computation** | J2 | Rider premium calculation inputs, rider-package version, computation accuracy | P2 if premium calculation errors detected |
| **Offer display** | J2 | Rider offer visibility %, offer acceptance rate by rider type | Business alert if offer visibility drops |
| **Attachment at quote** | J2 | Rider attach rate by product/channel, rider conflict rate | P3 on rising conflict rate |
| **Issuance** | J5 | Rider issue success %, quote-to-issue rider mismatch, rider effective-date mismatch | P1 if quote/issue rider mismatch exceeds threshold |
| **Premium posting** | J7 | Rider premium posting %, rider premium allocation accuracy | P1 on posting failure for riders |
| **Renewal** | J7 | Rider renewal status, rider lapse distinct from base policy | Business alert on rider-specific lapse patterns |
| **Claimability** | J8 | Rider claim events, rider-specific benefit payouts, rider coverage verification | P2 if rider claimability status conflicts with active policy |

---

## 19. Domain-Specific Monitoring Matrices

> _New section in v2.1. Detailed monitoring matrices by operational domain, adapted from insurance-domain monitoring research. These complement the business process monitoring in Section 4.5 and the journey framework in Section 18._

### 19.1 Underwriting and STP Monitoring

| What to monitor | Metric / indicator | Alert trigger | Owner |
|----------------|-------------------|---------------|-------|
| STP rate | % cases auto-decisioned by product/channel/rider | Business alert if STP drops > 5 pts vs baseline for 1h/day | Underwriting / rules owner |
| Decision latency | P50/P95 underwriting TAT from submit to decision | P2 if P95 exceeds SLA; P1 if queue stoppage | Underwriting Ops |
| Referral volume | Manual referral count, age buckets, oldest case age | P2 if backlog age > SLA | Ops manager |
| Rules-engine health | Rule evaluation latency, error count, external-data timeout | P1 if errors > threshold or external dependency timeouts spike | Rules/integration team |
| Medical evidence workflow | APS/lab request success, document turnaround, missing evidence aging | Business/Ops alert by backlog bucket | Underwriting Ops |
| Decision mix anomaly | Approve/refer/decline/counter-offer by product/rider/channel | Business anomaly alert on sudden distribution shift | Chief underwriter |
| Underwriting data quality | Missing declarations, conflicting answers, OCR extraction mismatch | Business alert daily by source/channel | UW governance |

### 19.2 Billing, Collections, and Persistency

| What to monitor | Metric / indicator | Alert trigger | Owner |
|----------------|-------------------|---------------|-------|
| Renewal due pipeline | Policies due next 7/30 days, premium at risk | Daily business alert for abnormal due vs collected gap | Collections / finance |
| Auto-debit success | Bank/card debit success %, retry success, return codes | P1 if gateway/bank-wide failure; P2 if success dips below threshold | Payments / collections |
| Grace and arrears | Grace count, aging buckets, premium in arrears, lapse risk | Business alert daily by cohort/channel | Collections / actuarial / sales |
| Lapse/reinstatement | Lapse rate, reinstatement rate, turnaround time | Weekly alert on abnormal cohort shift | Business owner |
| Collection controls | Duplicate retries, wrong amount posted, premium allocation errors | P1 on financial posting defect; P2 on growing exception queue | Finance systems |

### 19.3 Claims and Benefit Servicing

> _Recommended for Phase 3 planning even if full claims monitoring is Phase 3-4._

| What to monitor | Metric / indicator | Alert trigger | Owner |
|----------------|-------------------|---------------|-------|
| FNOL intake | FNOL submission success, attachment success, P95 latency | P1 if FNOL unavailable | Claims digital team |
| Claims backlog | Open claims by aging bucket, oldest claim age, missing-doc age | P2/P1 depending on breach severity | Claims Ops |
| Decision quality | Approve/pend/reject mix, reopen rate, leakage/fraud flags | Business anomaly alert | Claims leadership |
| Payout execution | Payment success, payout reversal, bank-return rate | P1 if payout channel fails | Claims + finance |

### 19.4 Ops Workflow and Exception Monitoring

| What to monitor | Metric / indicator | Alert trigger | Owner |
|----------------|-------------------|---------------|-------|
| Work queues | Items by queue, oldest item age, SLA breach count | P1 if queue frozen; P2 if oldest age crosses SLA | Ops control tower |
| Stuck cases | No-status-change > N minutes/hours, repeated retries, dead-letter volume | P1 if systemic; P2 if local backlog | Ops + integration |
| Manual rework | Cases touched > 1 time, re-open rate, handoff count | Daily business alert | Process owner |
| Exception taxonomy | Volume by reason code, by product/rider/channel/release | Daily/weekly anomaly alert | Ops excellence |
| Batch / EOD / reconciliations | Job completion, duration, late finish, reconciliation breaks | P1 if failed or incomplete | Platform/Ops/finance |

### 19.5 Security, Fraud, and Compliance Monitoring

> _Extends Section 4.6 with domain-specific detail._

| What to monitor | Metric / indicator | Alert trigger | Owner |
|----------------|-------------------|---------------|-------|
| WAF / edge protection | Blocked requests, allowed vs blocked trend, challenge/captcha metrics | P1 if attack impacts service; P2 on block surge or false-positive spike | SecOps |
| Identity security | Admin login anomalies, MFA bypass attempts, privilege escalation, inactive-account use | P1 for privileged anomalies | IAM/SecOps |
| PII / health data access | Sensitive-data read/export volume, unusual query patterns, after-hours access, mass-download attempts | P1 for confirmed high-risk events | SecOps / DPO |
| Consent & privacy controls | Consent capture success, consent withdrawal processing, data-subject request SLA, deletion completion | P2 if requests miss SLA; P1 if control breaks | Compliance / DPO |
| Audit trail completeness | % critical actions logged with actor/time/object/result | P1 if logging gaps detected on regulated actions | Platform + compliance |
| Fraud indicators | Duplicate identities, repeated failed KYC, payment/card anomalies, suspicious claim/application clusters | P2/P1 depending on severity | Fraud team |

---

## 20. Service Level Objectives (SLOs)

> _New section in v2.1. Formal SLO set as a foundation for error budget management. Adapted from insurance-domain monitoring research._

### 20.1 SLO Design Principles

- Set a small number of top-level SLOs first. Everything else supports them.
- SLOs are internal commitments — they define what "good enough" means before users notice degradation.
- Error budgets (1 - SLO target) give teams freedom to deploy and iterate; burning budget triggers protective action.
- SLO targets below are **starter objectives** that must be calibrated from TCLife's own volume, seasonality, product mix, channel mix, and acceptable business risk.

### 20.2 Starter SLO Set

| Service / Journey | SLI (Service Level Indicator) | Starter objective | Measurement notes |
|------------------|------------------------------|------------------|-------------------|
| Customer portal availability | Successful synthetic runs / total runs | 99.9% monthly | Run from Vietnam + one external region |
| Customer login | Successful login requests / total login requests | 99.5% monthly | Separate OTP provider failures from platform failures |
| Quote create | Successful quote creates / total quote attempts | 99.5% monthly | Segment by product and channel |
| Application submit | Successful submits / total attempts | 99.5% monthly | Track both frontend and backend commit success |
| Payment callback | Successful callbacks / total payment completions | 99.9% monthly | Revenue-protecting operation — tight target |
| Underwriting decision latency | % cases decided within SLA | 95% within agreed SLA | Use separate STP and manual SLA targets |
| Policy issuance | Successful issuance / eligible-to-issue cases | 99.7% monthly | Core fulfillment SLO |
| Billing collection | Successful premium postings / successful collections | 99.9% monthly | Finance-critical |
| Ops work item timeliness | % work items closed within SLA | 95% by queue | Use queue-specific SLA targets |

### 20.3 Relationship to Existing KPIs

The SLOs in Section 20.2 complement the KPIs in Section 10. KPIs measure operational targets (e.g., "policy issuance end-to-end time < 4 hours"). SLOs define availability/reliability commitments that, when breached, indicate the service is failing users.

**Implementation phasing**: SLOs should be introduced in Phase 2-3 alongside the business metrics work. Phase 2 establishes the measurement infrastructure; Phase 3 sets and begins tracking the SLO targets.

---

## 21. First 25 Alerts — Prioritized Implementation List

> _New section in v2.1. A prioritized list of the first alerts to implement, covering Phase 1-2 scope. Adapted from insurance-domain monitoring research._

This list defines the order in which alerts should be built and activated. Alerts 1-17 target Phase 1; alerts 18-25 target Phase 2.

| # | Alert | Category | Phase | Severity |
|---|-------|----------|-------|----------|
| 1 | Public customer portal synthetic failure | Availability | 1 | SEV1 |
| 2 | Sales portal login success below threshold | Availability | 1 | SEV1 |
| 3 | Application submit success below threshold | Business | 1 | SEV1 |
| 4 | Payment callback failures above threshold | Business | 1 | SEV1 |
| 5 | Policy issuance success below threshold | Business | 1 | SEV1 |
| 6 | ALB unhealthy targets > 0 | Infrastructure | 1 | SEV1 |
| 7 | ALB target 5XX sustained | Infrastructure | 1 | SEV1 |
| 8 | ALB P95 target response time breach | Infrastructure | 1 | SEV2 |
| 9 | Compute service desired != running tasks/pods | Infrastructure | 1 | SEV1 |
| 10 | Compute CPU/memory saturation sustained | Infrastructure | 1 | SEV2 |
| 11 | Lambda throttles > 0 for critical functions | Infrastructure | 1 | SEV1 |
| 12 | RDS connection/latency/storage risk | Infrastructure | 1 | SEV1/SEV2 |
| 13 | SQS backlog age or DLQ messages > 0 | Infrastructure | 1 | SEV1 |
| 14 | EventBridge failed invocations rise | Infrastructure | 1 | SEV2 |
| 15 | AWS Health event impacting critical services | Infrastructure | 1 | SEV2 |
| 16 | GuardDuty High-severity finding | Security | 1 | SEV1 |
| 17 | Certificate expiry < 30 days | Infrastructure | 1 | SEV2 |
| 18 | Rider issue mismatch between quote and issue | Business | 2 | SEV1 |
| 19 | Underwriting STP rate sudden drop | Business | 2 | SEV2 |
| 20 | Underwriting oldest case age above SLA | Business | 2 | SEV2 |
| 21 | Work queue backlog age above SLA | Ops | 2 | SEV2 |
| 22 | Document generation halted | Business | 2 | SEV2 |
| 23 | Outbound delivery (email/SMS) success drop | Business | 2 | SEV2 |
| 24 | Privileged access anomaly | Security | 2 | SEV1 |
| 25 | WAF block/challenge surge with customer impact | Security | 2 | SEV2 |

> **Starter thresholds**: Use the thresholds in this document only as initial operating baselines. Final thresholds must be calibrated from TCLife's own volume, seasonality, product mix, channel mix, and acceptable business risk. For life insurance, daily and weekly cohort analysis is as important as minute-level technical alarms.

---

## 22. Canonical Telemetry Data Model

> _New section in v2.1. Defines the minimum telemetry fields to collect per data domain. Adapted from insurance-domain monitoring research._

### 22.1 Design Principles

- Use a unique journey ID / application ID / policy ID / rider instance ID to stitch events end-to-end across portals, InsureMO, underwriting engines, payment, messaging, CRM, and document services.
- Every important action must emit both a **business event** and a **technical event**.
- Every failed customer step must have a machine-readable failure code, human-readable message, and ownership tag.
- Segment all metrics by channel (agency, bancassurance, digital direct, partner), product, rider, sales team, geography, release version, and vendor dependency.
- Keep cardinality controlled: use stable business dimensions, not arbitrary free-text.

### 22.2 Data Domains and Minimum Fields

| Data domain | Minimum telemetry / master data fields |
|------------|---------------------------------------|
| **Customer & prospect** | customer_id, lead_id, segment, acquisition channel, campaign, assigned agent, province, device/browser, consent status, eKYC status, fraud flags |
| **Quote / illustration** | quote_id, product, rider set, premium mode, premium amount, sum assured, benefit illustration version, save/submit timestamps, quote acceptance status |
| **Application / proposal** | application_id, required fields completion %, document completeness, medical question set version, declaration flags, underwriting class requested |
| **eKYC / identity** | KYC provider, status, retries, OCR confidence, liveness result, mismatch reason, document expiry, watchlist/sanctions outcome if used |
| **Payment** | transaction_id, gateway, authorization result, capture result, amount, currency, duplicate-payment flag, refund/void, settlement status |
| **Underwriting / STP** | underwriting_case_id, STP/manual/referral path, rules triggered, score, evidence requested, turnaround time, pending reason, decision, decision owner |
| **Policy issuance** | policy_id, issuance timestamp, effective date, cooling-off state, schedule creation, document generation, delivery status, policy pack acknowledgement |
| **Riders** | rider_code, rider eligibility result, rider premium, attach/detach status, rider issue timestamp, rider renewal status, rider claim events, rider-package version |
| **Billing / collections** | installment schedule, next due date, grace status, collection attempts, auto-debit success, arrears bucket, lapse/reinstatement status |
| **Servicing** | endorsement type, beneficiary change, address/contact change, policy loan, top-up, partial withdrawal, surrender, turnaround time, failure reason |
| **Claims / benefits** | claim_id, event type, FNOL timestamp, document completeness, triage result, fraud flags, adjudication outcome, payout turnaround, repudiation reason |
| **Agent / distribution** | agent_id, activity funnel, login, quote count, proposal count, conversion, cancellation/free-look, persistency by cohort, training/licence status if managed in platform |
| **Ops / workflow** | queue, work item age, backlog volume, SLA breach count, manual touches, handoff count, rework rate, exception reason taxonomy |
| **Compliance / audit** | consent events, policy wording version, disclosure shown/accepted, data export, privileged access, report submission status, immutable audit trail |

### 22.3 Implementation Notes

- Not all fields are required from day one. Phase 1-2 focuses on infrastructure and application telemetry. Phase 3 introduces business-domain fields.
- The data model is a target schema — actual implementation depends on what InsureMO exposes, what the integration layer can capture, and what custom instrumentation is built.
- Cardinality management is critical: channel, product, rider, and geography are stable dimensions. Avoid high-cardinality labels like free-text error messages in Prometheus metrics (use OpenSearch for those).

---

## 23. Composite Alert Patterns

> _New section in v2.1. Multi-signal alerting to reduce noise and increase confidence. Adapted from insurance-domain monitoring research._

### 23.1 Why Composite Alerts

Single-metric alerts generate noise. A brief dip in submit success rate might be a network blip; a brief rise in queue backlog might be a normal batch cycle. Composite alerts combine multiple signals to page only when the evidence of real customer or business harm is strong.

### 23.2 Recommended Composite Alert Patterns

| Composite alert | Signals combined | Page when | Rationale |
|----------------|-----------------|-----------|-----------|
| **Sales submission blocked** | Application submit success falls AND underwriting queue backlog rises AND no successful policy issuance events observed | All three conditions true for > 10 min | Single signal may be transient; three signals together confirm end-to-end blockage |
| **Payment pipeline failure** | Payment callback failures rise AND premium posting halted AND duplicate-charge anomaly detected | Two of three conditions true for > 5 min | Prevents paging on transient gateway blips while catching real payment outages |
| **Underwriting stall** | STP rate drops > 5 pts AND oldest case age exceeds SLA AND rules-engine error count rising | First two conditions true for > 30 min | STP dips can be caused by product mix; adding rules-engine errors confirms systemic issue |
| **Portal degradation** | Synthetic check fails AND RUM page load P95 degrades > 50% AND login success drops | Synthetic failure + one of the other conditions | Synthetic-only alerting catches hard down; adding RUM/login catches soft degradation |
| **Batch job chain failure** | GL batch fails AND premium reconciliation shows mismatch AND NAV calculation not started by deadline | Any two conditions true | Batch failures often cascade; composite alert identifies chain failures before downstream impact |

### 23.3 Implementation Notes

- Composite alerts require the underlying single-metric alerts to exist first (Phase 1-2). Composite logic is layered on top in Phase 2-3.
- Implementation options: Alertmanager recording rules that combine signals, or Grafana alert rules with multiple conditions.
- Use anomaly alerts (not static thresholds) for business metrics that vary by time of day, day of week, or season — e.g., quote-to-submit conversion, rider attach rate, decision mix, free-look rate, early lapse, claims reopen rate.

---

## 24. Appendix: Cross-References to Existing Work

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
| **Insurance-Domain Monitoring Research** | `solutions/monitoring-alerting/reference.research.md` | Comprehensive monitoring blueprint for Vietnam life insurer on eBao InsureMO / AWS. Source for v2.1 additions: journey framework, domain matrices, SLOs, first 25 alerts, data model, composite alerts, regulatory citations, InsureMO instrumentation checklist. |

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
| 2.1 | 2026-03-20 | IT Operations | Added: journey-first monitoring framework (9 core journeys, Sec 18), rider monitoring as cross-cutting dimension (Sec 18.3), domain-specific monitoring matrices for underwriting/STP, billing/persistency, claims, ops workflow, security/fraud/compliance (Sec 19), formal SLO set with starter objectives (Sec 20), prioritized first 25 alerts (Sec 21), canonical telemetry data model across 14 domains (Sec 22), composite multi-signal alert patterns (Sec 23), InsureMO instrumentation checklist (Sec 7.3), strengthened regulatory citations with Insurance Business Law 08/2022/QH15, Decree 46/2023, Circular 67/2023, Decision 07/QD-TTg (Sec 11.1, all pending Legal verification). Reference: `reference.research.md`. |
| 2.2 | 2026-03-20 | IT Operations | Deep expansion of Sections 4 and 5. Section 4: added EKS-specific monitoring (4.2.2), database deep dive with connection pooling and slow query detection (4.2.3), deployment/release health monitoring (4.2.4), expanded platform/middleware with concrete metrics for SQS/EventBridge/cache/API Gateway (4.3), added golden signals framework per service (4.4.2), health check endpoint specification (4.4.4), log level strategy (4.4.5), correlation ID propagation requirements (4.4.6), journey-first business process monitoring with failure detection patterns (4.5), expanded security with AWS-native services integration, SIEM-lite approach, PII access monitoring, fraud indicators (4.6), added RUM SLO targets and segmentation dimensions (4.7), added insurance-specific cost anomaly scenarios (4.8). Section 5: added alert lifecycle management with ITSM integration (5.6), alert runbook template with example (5.7), alert naming convention and label taxonomy (5.8), escalation flowchart with auto-escalation rules (5.9), alert testing strategy including game days (5.10), alert noise management with composite patterns and noise budget (5.11), business alert routing matrix distinguishing technical from business alerts (5.12). |
