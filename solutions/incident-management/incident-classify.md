# Incident Classification Matrix

> Comprehensive priority-by-category matrix for classifying incidents.
> Defines priority levels, SLA targets, escalation paths, and major incident criteria.
>
> **Usage**: L1 uses the [classification.md](classification.md) decision tree to determine priority, then consults this matrix for response targets, escalation paths, and handling requirements.
>
> Related: [`classification.md`](classification.md) -- [`incident-knowledge-base.md`](incident-knowledge-base.md) -- [`swimlane-flow.md`](swimlane-flow.md) -- [`scenarios.md`](scenarios.md)

---

## Executive Summary

This document provides the operational reference matrix for incident classification at TCLife. It maps every combination of **Priority (P1--P4)** and **Category (HW, SW, SEC, CLD, DB, ACC, OTH)** to specific indicators, downtime thresholds, SLA targets, escalation paths, and initial response actions.

The matrix is designed for a life insurance platform running on AWS, serving three user groups: policyholders (24/7 digital channels), sales agents/brokers (quoting and proposal systems), and in-house staff (underwriting, claims, actuarial, back-office). Classification decisions reflect the regulated nature of life insurance operations, where data correctness and availability carry financial and regulatory consequences.

---

## 1. Definitions

### 1.1 Priority Levels

| Priority | Name | Definition |
|----------|------|-----------|
| **P1** | Critical | Full outage of a Tier 1 or Tier 2 system, confirmed or suspected data breach, financial data corruption affecting customers, or any event that prevents core business operations (policy issuance, claims payment, premium collection). The business cannot operate normally. |
| **P2** | High | Significant degradation of a Tier 1 or Tier 2 system, key business function unavailable but workarounds partially exist, or a contained security event. Multiple user groups are affected and business throughput is materially reduced. |
| **P3** | Medium | Partial impact on a non-critical function or limited user group. A workaround exists and business operations continue with minor inconvenience. Single-user or single-function issues where the blast radius is confirmed small. |
| **P4** | Low | Cosmetic defects, minor inconveniences, documentation errors, or issues with no measurable business impact. Normal operations are unaffected. |

### 1.2 Incident Categories

| Code | Category | Scope | Examples |
|------|----------|-------|---------|
| **HW** | Hardware | Physical or virtual compute failures, storage, peripheral devices | EC2 host degradation, EBS volume failure, on-premises printer/scanner failure, workstation hardware fault |
| **SW** | Software (Application) | Application crashes, logic errors, calculation defects, UI failures, workflow bugs | Premium miscalculation, claims auto-approval defect, application OOM, unhandled exception, batch producing wrong output |
| **SEC** | Security | Confidentiality, integrity, or availability events with a security dimension | Data breach, credential compromise, ransomware, DDoS, unauthorized access, phishing exploitation, WAF bypass |
| **CLD** | Cloud Infrastructure | AWS managed services, networking, DNS, load balancing, serverless | AWS regional degradation, VPC connectivity loss, Route 53 failure, ALB misconfiguration, Lambda throttling, S3 access issue |
| **DB** | Database | Database engine failures, replication, data corruption, connection pool exhaustion, backup failures | RDS crash, DynamoDB throttling, replication lag, connection pool exhaustion, backup job failure, storage full |
| **ACC** | Access / Identity | Authentication, authorization, IAM, SSO, MFA, certificate issues | SSO outage, mass account lockouts, IAM policy misconfiguration, SSL certificate expiry, MFA service failure |
| **OTH** | Other | Third-party integrations, scheduled jobs, external dependencies, unclassified | Payment gateway failure, reinsurer API timeout, batch scheduler failure, ETL pipeline error, vendor system outage |

### 1.3 System Tiers

| Tier | Classification | Systems | Availability Target | User Group |
|------|---------------|---------|-------------------|------------|
| **Tier 1** | Customer-Facing | Policyholder portal, mobile app, online payment, customer self-service, digital onboarding | 99.9% (24/7) | Policyholders / Customers |
| **Tier 1** | Agent-Facing | Agent portal, quoting engine, proposal submission, commission dashboard, e-application | 99.5% (extended hours: 7am--10pm) | Sales Agents / Brokers |
| **Tier 2** | Internal Business-Critical | Core policy admin (PAS), claims processing, underwriting workbench, billing engine, actuarial systems, compliance reporting | 99.5% (business hours: 8am--6pm Mon--Sat) | In-house Users |
| **Tier 3** | Back-Office / Batch | Nightly batch processing, regulatory report generation, data warehouse ETL, commission calculation batch, premium allocation, document archival | Batch completion by 6:00 AM daily | Internal / Regulatory |

---

## 2. Priority Auto-Elevation Rules

Certain categories carry inherent risk that may automatically elevate priority regardless of initial assessment.

| Condition | Minimum Priority | Rationale |
|-----------|-----------------|-----------|
| **SEC** -- Any confirmed data breach involving PII (policyholder, beneficiary, insured) | P1 | Regulatory reporting obligation, reputational risk, potential legal liability |
| **SEC** -- Any confirmed credential compromise of production systems | P1 | Active threat to data integrity and availability |
| **SEC** -- DDoS attack actively degrading service | P1 | Availability impact on customer-facing systems |
| **DB** -- Suspected data corruption in financial tables (premiums, claims, policy values) | P1 | Financial data integrity is a P1 trigger per classification policy |
| **DB** -- Primary database unresponsive / failover triggered | P1 | Core systems depend on database availability |
| **SW** -- Calculation error affecting policyholder financial values (surrender, premium, claim amount) | P1 | Financial data correctness -- regulatory and customer trust implications |
| **ACC** -- Mass authentication failure (>10% of user base cannot log in) | P1 | Effectively a full outage for affected users |
| **CLD** -- AWS regional service degradation affecting multiple core systems | P1 | Multi-system impact requiring DR activation assessment |
| **OTH** -- Payment gateway failure (all payment channels down) | P1 | Revenue collection halted |
| **Any category** -- Regulatory reporting system unavailable within 48 hours of submission deadline | P2 minimum | Regulatory compliance risk |
| **Any category** -- Batch processing failure for premium allocation, commission calculation, or regulatory feeds | P2 minimum | Financial and regulatory downstream impact |

---

## 3. Classification Matrix

### 3.1 P1 -- Critical

**General Indicators**: Complete service unavailability for a Tier 1 or Tier 2 system. All or most users of the affected system cannot perform their primary function. Financial data is or may be incorrect. Security breach confirmed. Regulatory obligation triggered.

**Downtime Threshold**: Zero tolerance for unplanned downtime on Tier 1 systems. Maximum 2-hour containment window to restore usable (even degraded) service. Full resolution within 24 hours.

**Major Incident**: YES -- all P1 incidents are declared Major Incidents.

**MTTA (Mean Time to Acknowledge)**: 15 minutes (24/7 for Tier 1; business hours for Tier 2 unless on-call coverage exists).

**MTTR Target (Containment)**: 2 hours. **MTTR Target (Full Resolution)**: 24 hours.

| Category | Impact Description | Urgency | System-Level | Escalation | Reaction (Initial Response) |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Compute host failure causing complete outage of core insurance platform. Agents cannot quote, customers cannot access portal, or claims processing halted. | Immediate. Every minute of downtime is lost revenue and customer trust. | Tier 1 (portal/agent systems) or Tier 2 (PAS, claims) depending on which systems run on affected host. | 0 min: On-call engineer auto-paged. 15 min: CTO/IT Manager notified. 30 min: IC activated, war room opened. 1 hr: CEO briefed if customer-facing. | 1. Confirm scope (which systems affected). 2. Failover to standby instance/AZ. 3. IC coordinates response. 4. Status updates every 30 min. 5. Post-incident review mandatory. |
| **SW** | Application defect causing incorrect financial calculations (premiums, claims, surrender values) across multiple policies, OR complete application crash preventing core business function. Silent data corruption discovered affecting policyholder records. | Immediate. Financial data errors compound over time -- every hour of delay increases remediation cost. | Tier 2 (PAS, billing, claims engine) with downstream Tier 1 impact (customers see wrong values in portal). Tier 3 if batch output is corrupted. | 0 min: Dev on-call paged. 15 min: CTO notified. 30 min: IC activated. If financial data affected: Finance and Actuarial heads notified within 1 hr. | 1. STOP further data writes/processing if corruption suspected. 2. Identify blast radius (how many policies/customers). 3. If deployment-related: immediate rollback. 4. If data corruption: isolate affected records, hold downstream outputs. 5. Notify Finance. 6. Hold any regulatory reports using affected data. |
| **SEC** | Confirmed data breach exposing PII of policyholders (name, ID, health data, financial records). Ransomware detected. Credential compromise of production database or admin accounts. Active exploitation in progress. | Immediate. Regulatory clock starts ticking. Attacker may still be active -- containment is time-critical. | All tiers potentially affected. Tier 1 systems may need to be taken offline for containment. | 0 min: Security lead paged. 15 min: CTO + Legal notified. 30 min: CEO briefed. 1 hr: Assess regulatory notification obligation (data protection authority, insurance regulator). External incident response retainer activated if needed. | 1. Isolate compromised systems (network segmentation). 2. Preserve forensic evidence (do NOT reboot or wipe). 3. Revoke compromised credentials. 4. Activate security incident playbook. 5. Assess regulatory reporting obligation. 6. Engage legal counsel. 7. Do NOT communicate externally until legal advises. |
| **CLD** | AWS regional outage or multi-AZ failure affecting core insurance platform. Multiple systems down simultaneously. DR activation may be required. | Immediate. Cloud infrastructure is foundational -- nothing works until this is resolved. | All tiers. Tier 1 and Tier 2 systems share cloud infrastructure. | 0 min: Infra on-call paged. 15 min: CTO notified. 30 min: IC activated. 1 hr: Assess DR activation (failover to secondary region if RTO exceeded). AWS Enterprise Support case opened (Severity 1). | 1. Confirm AWS Health Dashboard status. 2. Verify scope (which AZs/services affected). 3. Activate multi-AZ failover if available. 4. If regional: initiate DR plan (pilot light/warm standby). 5. Open AWS support case (Critical). 6. Monitor AWS status for ETA. 7. Enable maintenance mode on customer-facing apps. |
| **DB** | Primary production database unreachable or confirmed data corruption in financial tables. RDS failover failed. Connection pool exhausted across all application instances. | Immediate. Database is the single most critical dependency -- all business logic requires it. | Tier 2 (PAS, claims, billing all depend on DB) with cascading Tier 1 impact. | 0 min: DBA on-call paged. 15 min: CTO notified. 30 min: IC activated. If data corruption: Actuarial and Finance notified. | 1. Attempt RDS failover to standby. 2. If failover fails: assess point-in-time recovery options. 3. If corruption: STOP all writes immediately. 4. Identify last known good state (backup/snapshot). 5. Quantify data loss window. 6. Switch apps to read-only mode if possible. |
| **ACC** | Complete authentication failure -- SSO/IAM outage preventing all users from logging in. SSL certificate expiry on production domain. Mass account lockout affecting agents during business hours. | Immediate. If nobody can log in, the system is effectively down even though infrastructure is running. | Tier 1 (customer and agent portals) and Tier 2 (internal systems) -- all depend on authentication. | 0 min: Infra on-call paged. 15 min: CTO notified. 30 min: IC activated. If certificate-related: immediate remediation path (no investigation needed). | 1. Identify root cause (SSO provider, IAM policy, certificate, MFA service). 2. If certificate expiry: deploy renewed certificate immediately. 3. If SSO: check provider status, failover to backup auth if available. 4. If IAM policy change: revert immediately. 5. Communicate to agents and internal users with ETA. |
| **OTH** | Payment gateway complete failure -- all premium collection channels down. Core reinsurer integration failure during treaty renewal window. Regulatory feed system down within 24 hours of submission deadline. | Immediate. Revenue collection halted or regulatory deadline at risk. | Tier 1 (payment affects customers/agents) or Tier 3 (regulatory feeds) with P1 regulatory risk. | 0 min: On-call paged. 15 min: IT Manager notified. 30 min: IC activated. Vendor support contacted. If regulatory: Compliance officer notified. | 1. Contact vendor/third-party support immediately. 2. Activate fallback channel if available (backup payment gateway, manual submission). 3. Enable queuing/retry mechanism. 4. Communicate to affected users (portal banner, agent notification). 5. Monitor vendor status for ETA. 6. If regulatory: assess deadline extension options. |

---

### 3.2 P2 -- High

**General Indicators**: Significant degradation of a Tier 1 or Tier 2 system. A key business function is unavailable but the system is partially operational. Many users affected during business hours. Performance degradation severe enough to impede normal work speed. Batch processing failure with financial downstream impact.

**Downtime Threshold**: Maximum 4-hour containment window. Full resolution within 5 business days.

**Major Incident**: CONDITIONAL -- declared Major Incident if: (a) degradation persists beyond 2 hours during business hours, (b) more than 30% of a user group is affected, or (c) financial/regulatory impact is identified during investigation.

**MTTA**: 30 minutes (business hours; 1 hour after-hours if on-call coverage exists).

**MTTR Target (Containment)**: 4 hours. **MTTR Target (Full Resolution)**: 5 business days.

| Category | Impact Description | Urgency | System-Level | Escalation | Reaction (Initial Response) |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Partial compute degradation -- system running but on reduced capacity. Failover to secondary succeeded but running on single instance (no redundancy). Storage I/O degradation slowing transactions. | High. Redundancy is lost -- a second failure would cause P1. | Tier 1 or Tier 2 running on degraded hardware. | 0 min: On-call engineer notified. 30 min: IT Manager notified. 2 hr: Escalate to CTO if no resolution path. | 1. Confirm redundancy status. 2. Provision replacement instance. 3. Migrate workload. 4. Restore redundancy. 5. Validate performance. |
| **SW** | Key feature unavailable (e.g., agents cannot submit new proposals, but can view existing policies). Application intermittently crashing (5--30% of requests). Performance regression after deployment -- pages loading 10x slower. Batch completed but output for one product line is incorrect. | High. Business throughput is reduced but not halted. Revenue leakage or delayed processing is occurring. | Tier 1 (degraded agent/customer experience) or Tier 2 (partial function unavailable) or Tier 3 (batch output partially wrong). | 0 min: Dev on-call notified. 30 min: IT Manager notified. 1 hr: Team lead escalation if no root cause identified. 4 hr: CTO if containment not achieved. | 1. If post-deployment: assess rollback (rollback first if intermittent crash). 2. Identify affected function and user scope. 3. Apply workaround if available. 4. Communicate to affected user group. 5. If batch output wrong: hold downstream processing for affected product line. |
| **SEC** | Suspected but unconfirmed security event. Anomalous access patterns detected by GuardDuty. Single account compromise (non-admin). WAF blocking elevated attack traffic but service is degraded. Phishing campaign targeting employees detected. | High. May escalate to P1 if confirmed. Investigation is time-sensitive -- attackers move fast. | Varies. Security events can affect any tier. | 0 min: Security lead notified. 30 min: IT Manager notified. 1 hr: CTO if scope expands. | 1. Investigate and scope (is it real? is it contained?). 2. Isolate suspected compromised account. 3. Review GuardDuty/CloudTrail findings. 4. Reset credentials for affected accounts. 5. If confirmed breach: ESCALATE TO P1 immediately. |
| **CLD** | Single AWS service degraded (e.g., elevated Lambda latency, S3 intermittent errors). One AZ experiencing issues but multi-AZ deployment absorbing impact. CloudFront edge degradation affecting some regions. | High. Service is degraded and single-AZ resilience is being consumed -- second AZ failure would be P1. | Tier 1 (customer experience degraded) or Tier 2 (internal systems slower). | 0 min: Infra on-call notified. 30 min: IT Manager notified. 2 hr: Escalate if AWS has no ETA. | 1. Confirm AWS Health Dashboard status. 2. Verify multi-AZ failover is absorbing traffic. 3. Route traffic away from degraded AZ/edge. 4. Open AWS support case (High). 5. Monitor and prepare DR activation if degradation spreads. |
| **DB** | Database replication lag exceeding threshold (read replicas stale). Connection pool at 80%+ utilization. Backup job failed (RPO at risk). Single read replica down (capacity reduced but functional). | High. Data availability or protection is degraded. A second failure would cause P1. | Tier 2 (applications experiencing slower queries) with potential Tier 1 impact if lag causes stale data display. | 0 min: DBA on-call notified. 30 min: IT Manager notified. 2 hr: Escalate if replication gap widening. | 1. Investigate replication lag cause (long-running query, write spike, network). 2. Kill long-running queries if safe. 3. For backup failure: trigger manual backup immediately. 4. Scale read replicas if capacity issue. 5. Monitor connection pool trend. |
| **ACC** | SSO intermittently failing (some users affected, others not). MFA service degraded -- users experiencing delays. New user provisioning broken (existing users unaffected). Certificate expiring within 7 days (not yet expired). | High. Not all users blocked, but the authentication system is unreliable. Degrades confidence and may worsen. | Tier 1 and Tier 2 (intermittent login failures across systems). | 0 min: Infra on-call notified. 30 min: IT Manager notified. 2 hr: Escalate if not stabilizing. | 1. Identify pattern (which users, which IdP, timing). 2. Check SSO provider status. 3. Restart auth service components if applicable. 4. For expiring certificate: initiate renewal immediately. 5. Communicate workaround to affected users (retry, alternative browser, clear cache). |
| **OTH** | Payment gateway intermittent failures (60--70% success rate). Third-party API responding slowly causing timeout in agent quoting tool. Batch scheduler ran late -- downstream processing delayed but not yet missed deadline. Commission calculation batch failed (agent payments at risk). | High. Business function degraded, revenue or agent satisfaction impacted. Deadline pressure may exist. | Tier 1 (payment/quoting degraded for agents/customers) or Tier 3 (batch delayed). | 0 min: On-call notified. 30 min: IT Manager notified. If commission batch: notify agency operations. 2 hr: Escalate if vendor unresponsive. | 1. Contact vendor/third-party. 2. Implement retry logic or manual fallback. 3. For batch failure: assess rerun window (can it complete before 6 AM?). 4. Communicate to affected business units. 5. For payment: route to backup gateway if available. |

---

### 3.3 P3 -- Medium

**General Indicators**: Partial impact on a non-critical function. A workaround exists and is known. Limited user group affected (single team, single product line, single region). No financial data at risk. Service is operational but inconvenient.

**Downtime Threshold**: Degradation acceptable for up to 1 business day. Full resolution within 10 business days.

**Major Incident**: NO -- unless investigation reveals hidden financial/data impact (then re-classify).

**MTTA**: 2 business hours.

**MTTR Target (Containment)**: 1 business day. **MTTR Target (Full Resolution)**: 10 business days.

| Category | Impact Description | Urgency | System-Level | Escalation | Reaction (Initial Response) |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Non-critical peripheral failure (printer, scanner at branch). Workstation issue affecting individual user. Non-production server degradation. | Normal. User can use alternative equipment or workstation. | Tier 2 (individual workstation) or support infrastructure. | 2 hr: Team lead if no progress. 1 business day: IT Manager if unresolved. | 1. Provide alternative equipment. 2. Log hardware support ticket. 3. Schedule replacement/repair. |
| **SW** | Single report displaying incorrect formatting. One non-critical feature broken (e.g., policy document preview fails but download works). UI rendering issue on specific browser. Error in non-financial data field. | Normal. Business continues with minor inconvenience. | Tier 2 (internal tool minor defect) or Tier 1 (cosmetic/non-blocking customer-facing issue). | 2 hr: Team lead if no progress. 4 hr: Dev lead if diagnostic assistance needed. | 1. Document the issue with reproduction steps. 2. Confirm workaround works and communicate to affected users. 3. Assign to development sprint for fix. |
| **SEC** | Phishing email reported but no credentials compromised. Vulnerability scan finding requiring patching (no active exploitation). Single user account suspicious activity (contained). | Moderate. Should be addressed promptly but no active threat. | Any tier (vulnerability patching) or individual account. | 4 hr: Security lead review. 1 business day: Patch scheduling. | 1. Block/quarantine phishing email. 2. Alert affected user(s). 3. For vulnerability: assess severity (CVSS), schedule patching window. 4. Monitor for escalation indicators. |
| **CLD** | Non-production environment issue (staging, dev). CloudWatch alarm for non-critical metric. S3 lifecycle policy not executing (no immediate impact). | Normal. No production impact. Operational hygiene issue. | Tier 3 or non-production. | 4 hr: Team lead awareness. 1 business day: Infra team schedules fix. | 1. Confirm no production impact. 2. Log and schedule remediation. 3. Monitor for pattern (may indicate emerging issue). |
| **DB** | Slow query affecting one non-critical report. Non-production database issue. Query optimization needed (performance below optimal but within SLA). Minor replication delay on read replica used for reporting only. | Normal. Production operations unaffected. | Tier 3 (reporting/analytics) or non-production. | 4 hr: DBA awareness. 1 business day: Schedule optimization. | 1. Confirm production is unaffected. 2. Identify the slow query. 3. Apply quick index or query optimization if low risk. 4. Schedule proper fix. |
| **ACC** | Single user cannot log in (account-specific issue). New user provisioning delayed but not blocked. Role/permission misconfiguration affecting non-critical function for individual. | Normal. Individual user inconvenience, not systemic. | Individual user account. | 2 hr: L1 resolution expected. 4 hr: Escalate if systemic cause suspected. | 1. Verify account status (locked, expired, MFA). 2. Reset credentials if needed. 3. If pattern emerges (multiple individuals): re-assess as P2. |
| **OTH** | Non-critical third-party integration failing (e.g., analytics data feed). Scheduled job for non-urgent report ran late. Minor vendor API version deprecation warning. Email notification service delayed. | Normal. No business function blocked. | Tier 3 (analytics, non-critical feeds). | 4 hr: Team lead awareness. 1 business day: Vendor contact if needed. | 1. Confirm no downstream business impact. 2. Apply workaround if available. 3. Contact vendor if external dependency. 4. Schedule fix. |

---

### 3.4 P4 -- Low

**General Indicators**: Cosmetic issues, minor UI inconsistencies, documentation errors, feature requests misreported as incidents, or issues with no measurable user or business impact. "Nice to fix" items that do not affect anyone's ability to work.

**Downtime Threshold**: Not applicable -- no downtime or degradation associated.

**Major Incident**: NO.

**MTTA**: Next business day.

**MTTR Target (Full Resolution)**: 15 business days (or scheduled into next development sprint).

| Category | Impact Description | Urgency | System-Level | Escalation | Reaction (Initial Response) |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Cosmetic hardware issue (e.g., sticky keyboard, monitor color calibration). Spare equipment request. | Low. No impact on ability to work. | Support infrastructure. | None unless recurs 3+ times. | 1. Log request. 2. Schedule replacement in next procurement cycle. |
| **SW** | Wrong font on one screen. Tooltip text incorrect. Minor alignment issue in generated PDF. Outdated copyright year in footer. Feature works correctly but label is misleading. | Low. Cosmetic. No business logic affected. | Tier 1 or Tier 2 (cosmetic layer). | None. Added to development backlog. | 1. Log with screenshot. 2. Add to backlog, prioritize in sprint planning. |
| **SEC** | Informational security advisory with no applicability. False positive from security scanner. Routine patching notification. | Low. No threat. | N/A. | None. Track for compliance record. | 1. Log for audit trail. 2. Close or schedule routine action. |
| **CLD** | Unused resource cleanup notification. Cost optimization recommendation. Tagging non-compliance on non-production resource. | Low. Operational hygiene. | Non-production or cost management. | None. Review in next FinOps cycle. | 1. Log for tracking. 2. Schedule in next operational review. |
| **DB** | Minor schema documentation out of date. Non-critical index recommendation. Test database cleanup needed. | Low. No operational impact. | Non-production or documentation. | None. Schedule in maintenance window. | 1. Log. 2. Add to DBA maintenance backlog. |
| **ACC** | Single user requesting additional non-urgent permission. Display name incorrect in directory. | Low. Service request that was misrouted as incident. | Individual user. | None. Reclassify as Service Request if applicable. | 1. Reclassify to Service Request if appropriate. 2. Process through normal access management. |
| **OTH** | Non-critical vendor notification. Minor log format inconsistency. Test data cleanup request. | Low. No business impact. | Non-production or operational hygiene. | None. | 1. Log. 2. Schedule in next maintenance window or sprint. |

---

## 4. Major Incident Declaration Criteria

A **Major Incident** triggers the full incident command structure: Incident Commander (IC), war room, periodic status communications, management notification chain, and mandatory Post-Incident Review.

### Automatic Declaration (No Judgment Required)

| Criterion | Applies When |
|-----------|-------------|
| All P1 incidents | Always a Major Incident |
| Confirmed data breach involving PII | Regardless of initial priority assessment |
| Financial data corruption confirmed | Policyholder financial values, premium calculations, claim amounts |
| Complete outage of any Tier 1 system | Customer portal, agent portal, payment processing |
| DR activation initiated | Any incident requiring failover to secondary region |
| Regulatory reporting obligation triggered | Events requiring notification to insurance regulator or data protection authority |

### Conditional Declaration (IC or IT Manager Judgment)

| Criterion | Declare Major If... |
|-----------|-------------------|
| P2 incident duration | Degradation persists beyond 2 hours during business hours |
| P2 user impact scope | More than 30% of any user group affected |
| P2 with financial angle | Investigation reveals financial data may be affected (reclassify to P1) |
| P3 incident with emerging scope | Blast radius discovered to be larger than initial assessment (reclassify) |
| Any incident during regulatory submission window | Within 48 hours of regulatory report deadline |
| Reputational risk | Social media / press attention, or customer complaint volume spike |

---

## 5. SLA Summary by Priority

| Metric | P1 Critical | P2 High | P3 Medium | P4 Low |
|--------|------------|---------|-----------|--------|
| **MTTA** | 15 min | 30 min | 2 business hours | Next business day |
| **First Update** | 30 min | 1 hour | At triage | At triage |
| **Status Update Frequency** | Every 30 min | Every 1 hour | On request | On request |
| **Containment Target** | 2 hours | 4 hours | 1 business day | N/A |
| **Full Resolution Target** | 24 hours | 5 business days | 10 business days | 15 business days |
| **SLA Clock** | 24/7 (clock time) | Business hours (8am--6pm Mon--Sat) | Business hours | Business hours |
| **Post-Incident Review** | Mandatory (within 48 hrs) | Mandatory (within 5 business days) | Simplified note in ticket (within 5 business days) | Not required (unless recurs 3+ times) |
| **Knowledge Base Update** | Mandatory | Mandatory | If likely to recur | Only if pattern emerges |

### Business Hours vs After-Hours Handling

| Priority | Business Hours (8am--6pm Mon--Sat) | After Hours (nights, Sundays, holidays) |
|----------|-----------------------------------|----------------------------------------|
| **P1** | Full response. All hands. IC activated. War room. Management notified. | On-call engineer responds. IC activated remotely. Management notified by phone. Same containment targets. |
| **P2** | Full response. On-call team plus escalation to specialists. | On-call engineer assesses. If Tier 1 impact: full response. If Tier 2 only: contain and schedule fix for next business day unless degradation is worsening. |
| **P3** | Assigned engineer works during business hours. | No after-hours response. Logged for next business day. |
| **P4** | Backlog. Scheduled into sprint. | No after-hours response. |

---

## 6. Escalation Matrix

### Escalation by Priority and Time

| Elapsed Time | P1 Action | P2 Action | P3 Action | P4 Action |
|-------------|-----------|-----------|-----------|-----------|
| **0 min** | On-call engineer auto-paged | On-call engineer notified | -- | -- |
| **15 min** | CTO/IT Manager notified. IC assigned. | -- | -- | -- |
| **30 min** | IC activated. War room opened. First status update. | IT Manager notified | -- | -- |
| **1 hour** | CEO briefed (if customer-facing or regulatory). Management bridge call if needed. | Team lead escalation if no root cause | -- | -- |
| **2 hours** | If not contained: reassess approach. Consider DR activation. External specialist/vendor escalation. | -- | Team lead if no progress | -- |
| **4 hours** | If not resolved: executive escalation. Vendor CEO-to-CEO escalation if vendor-caused. | CTO notified if not contained. Reassess: should this be P1? | -- | -- |
| **8 hours** | Continuous response with crew rotation. Board notification if customer data compromised. | IT Manager re-review. Assess resource needs. | -- | -- |
| **1 business day** | Still unresolved: crisis management protocol. | -- | IT Manager if unresolved | Team lead if recurrent |

### Escalation by Role

| Role | Contacted For | Contact Method |
|------|--------------|----------------|
| **On-Call Engineer** | All P1, P2 incidents. Initial technical response. | Automated page (PagerDuty/OpsGenie) + phone |
| **Team Lead** | P2 if no root cause in 1 hr. P3 if no progress in 2 hrs. Technical guidance. | Chat + phone |
| **IT Manager** | All P1 at 15 min. P2 at 30 min. P3 at 1 business day if unresolved. Resource decisions. | Phone + chat |
| **DBA On-Call** | All DB category incidents P1/P2. DB involvement in other categories. | Automated page + phone |
| **Security Lead** | All SEC category incidents. Any incident with security dimension. | Phone (P1 immediate) + chat |
| **CTO** | P1 at 15 min. P2 at 4 hrs if not contained. DR activation decisions. | Phone |
| **CEO** | P1 at 1 hr if customer-facing or regulatory. Data breach involving PII. | Phone (via CTO) |
| **Compliance Officer** | Any incident with regulatory reporting implications. Data breach. Financial data corruption. | Phone (P1) + email (P2) |
| **Vendor Support** | External dependency failures. L3 escalation for vendor products. | Vendor support portal + phone. Pre-arranged contacts for critical vendors. |

---

## 7. Communication Requirements

| Priority | Internal Communication | Customer Communication | Agent Communication | Regulatory Communication |
|----------|----------------------|----------------------|--------------------|-----------------------|
| **P1** | War room channel. Status every 30 min. Management bridge call. All-hands email for extended outages (>2 hrs). | Portal maintenance banner. SMS/email for payment system outages. Customer service briefed with talking points. | Agent hotline briefed. Agent portal banner. SMS blast for system outage. Provide offline workaround instructions. | Assess within 1 hour. Notify if data breach (PII), extended outage (>4 hrs customer-facing), or financial transaction errors above threshold. |
| **P2** | Incident channel update. Status every 1 hr. Affected business unit notified. | Portal banner if customer-facing feature degraded. FAQ update if customer-visible. | Agent notification if agent-facing feature affected. Workaround communicated. | Assess if trending toward regulatory trigger. No proactive notification unless threshold met. |
| **P3** | Team channel. Affected users notified directly. | No external communication. | No communication unless agents specifically affected. | None. |
| **P4** | Ticket update only. | None. | None. | None. |

---

## 8. Insurance-Specific Scenarios and Classification

These scenarios illustrate how the matrix applies to common life insurance operational situations. For full worked-through triage examples, see [scenarios.md](scenarios.md).

### Tier 1 -- Customer-Facing Scenarios

| Scenario | Category | Priority | Major? | Key Consideration |
|----------|----------|----------|--------|-------------------|
| Policyholder portal completely down | CLD/HW | P1 | Yes | Customers cannot access policies, submit claims, or make payments. Revenue and trust impact. |
| Online premium payment failing for all customers | OTH | P1 | Yes | Payment gateway failure halts revenue collection. Activate backup gateway. |
| Customer mobile app crashing on launch | SW | P1 | Yes | High-visibility. App store reviews will reflect this within hours. |
| Policyholder portal slow (15s page load) | CLD/SW | P2 | Conditional | Degraded but functional. P1 if during enrollment/renewal peak. |
| Customer e-claim submission error for one product | SW | P2 | No | Workaround: call center can submit. Monitor volume. |
| Policy document download shows wrong beneficiary name | SW | P1 | Yes | Data integrity issue -- could be display only or data corruption. Investigate immediately. |

### Tier 1 -- Agent-Facing Scenarios

| Scenario | Category | Priority | Major? | Key Consideration |
|----------|----------|----------|--------|-------------------|
| Agent portal down during open enrollment season | CLD/HW | P1 | Yes | Revenue-critical window. Every hour of downtime is lost sales. |
| Quoting engine returning incorrect premiums | SW | P1 | Yes | Agents quoting wrong prices to customers. Immediate stop. Financial and regulatory risk. |
| Agent commission dashboard unavailable | SW | P2 | No | Agents frustrated but can still sell. Fix within business day. |
| Proposal submission failing intermittently | SW | P2 | Conditional | If >30% failure rate during business hours: declare Major. |
| Agent SSO failing for specific branch office | ACC | P2 | No | Limited scope. Provide temporary credentials as workaround. |
| Agent portal slow during evening hours | CLD/SW | P3 | No | Agents work evenings but volume is lower. Schedule fix for next day. |

### Tier 2 -- Internal Business Scenarios

| Scenario | Category | Priority | Major? | Key Consideration |
|----------|----------|----------|--------|-------------------|
| Core policy admin system (PAS) down | CLD/HW/SW | P1 | Yes | All underwriting, policy servicing, and claims processing halted. |
| Claims processing engine producing wrong auto-adjudication results | SW | P1 | Yes | Incorrect claim payments. Financial loss and regulatory exposure. Stop auto-adjudication immediately. |
| Underwriting workbench unavailable | SW | P2 | Conditional | New business processing delayed. Major if queue exceeds 4 hours during peak. |
| Billing engine failed to generate monthly premium notices | SW/OTH | P2 | No | Premium collection at risk. Must be resolved before next collection cycle. |
| Actuarial calculation system slow | DB/SW | P3 | No | Actuaries delayed but no customer impact. Workaround: run calculations off-peak. |
| Compliance reporting tool formatting error | SW | P3 | No | Report content correct, formatting wrong. Manual fix possible. |

### Tier 3 -- Batch/Back-Office Scenarios

| Scenario | Category | Priority | Major? | Key Consideration |
|----------|----------|----------|--------|-------------------|
| Nightly premium allocation batch failed | OTH/DB | P2 | Conditional | Must complete before 6 AM. Major if rerun window is insufficient. |
| Commission calculation batch produced wrong amounts | SW | P1 | Yes | Financial data corruption. Agent payments at risk. Hold payment run. |
| Regulatory report generation failed, due in 3 days | OTH/SW | P2 | No | Deadline pressure. Escalate if not resolved within 24 hours. |
| Regulatory report generation failed, due tomorrow | OTH/SW | P1 | Yes | Regulatory deadline imminent. All-hands remediation. |
| Data warehouse ETL delayed by 4 hours | OTH/DB | P3 | No | Analytics delayed but no operational impact. |
| Document archival batch failed | OTH | P3 | No | No immediate impact. Schedule rerun. Monitor for recurrence. |

---

## 9. Priority Re-Classification Guidelines

Priority is not static. It must be re-assessed as new information emerges.

### Upgrade Triggers (Increase Priority)

| Current | Upgrade To | When |
|---------|-----------|------|
| P2 | P1 | Degradation worsens to full outage. Financial data impact discovered. Duration exceeds 2 hours during business hours. Scope discovered to be larger than initial assessment. |
| P3 | P2 | Blast radius larger than expected (more users/systems affected). Business hours impact confirmed. Workaround fails. |
| P3 | P1 | Investigation reveals financial data corruption. Regulatory deadline at risk. |
| P4 | P3 | Pattern emerges (3+ occurrences). Underlying cause suggests larger systemic issue. |

### Downgrade Triggers (Decrease Priority)

| Current | Downgrade To | When |
|---------|-------------|------|
| P1 | P2 | Service restored to degraded but usable state (containment achieved). Scope confirmed smaller than feared. |
| P2 | P3 | Effective workaround deployed. Impact limited to small user group. |
| P3 | P4 | Confirmed cosmetic only. No business impact. |

### Re-Classification Authority

| Action | Who Can Do It |
|--------|--------------|
| Upgrade to P1 | Anyone (any team member can escalate to P1 -- err on the side of caution) |
| Upgrade to P2 | L1 on-call, Team Lead, IC, IT Manager |
| Downgrade from P1 | IC or IT Manager only (with documented rationale) |
| Downgrade from P2 | IC, Team Lead, or IT Manager |
| Downgrade P3/P4 | Assigned engineer with Team Lead awareness |

---

## 10. Regulatory Reporting Quick Reference

Certain incident conditions may trigger mandatory reporting to the insurance regulator or data protection authority. This is a quick-reference checklist -- detailed procedures should be maintained by the Compliance team.

| Trigger Condition | Reporting Obligation | Timeline | Responsible |
|------------------|---------------------|----------|-------------|
| Personal data breach (PII of policyholders, insureds, beneficiaries exposed or lost) | Data protection authority notification. Potentially affected individuals notification. | Assess within 1 hour. Report within 72 hours of confirmation (or per local regulation). | Compliance Officer + Legal |
| Financial transactions incorrectly processed above defined threshold | Insurance regulator notification | Per regulatory requirement (assess within 24 hours) | Compliance Officer + Finance |
| Core customer-facing systems unavailable >4 hours during business hours | Insurance regulator notification (if required by local regulation) | Within 24 hours of incident close | Compliance Officer + IT Manager |
| Event affecting policyholder rights or benefits (delayed claims payment, incorrect policy values issued to customers) | Insurance regulator notification | Per regulatory requirement | Compliance Officer |
| Cyber security incident of material significance | Insurance regulator and relevant authorities | Assess within 1 hour. Report per regulatory timeline. | Security Lead + Compliance + Legal |

**Note**: Specific reporting timelines and thresholds must be confirmed against current Vietnamese insurance and data protection regulations. This table provides the framework -- the Compliance team must populate exact thresholds and contact details.

---

## 11. Cross-Reference: Category Impact on Priority Assignment

This table shows how each category tends to influence priority. It does not override the decision tree in [classification.md](classification.md) -- it provides guidance for borderline cases.

| Category | Tendency to Elevate Priority | Reasoning |
|----------|-------|-----------|
| **SEC** | Strong upward pressure | Security incidents have unpredictable blast radius and regulatory implications. Unknown scope should be treated as worst-case until confirmed otherwise. |
| **DB** | Moderate-to-strong upward pressure | Database issues affect all applications. Data corruption is irreversible without backups. |
| **ACC** | Moderate upward pressure | Authentication failures have broad user impact -- effectively an outage even when systems are running. |
| **CLD** | Depends on scope | Single-service degradation may be P2/P3. Multi-service or regional issues are P1. |
| **SW** | Depends on data impact | Cosmetic bugs are P4. Calculation errors affecting financial data are P1. Wide range. |
| **HW** | Depends on redundancy | If redundancy absorbs the failure: P2. If single point of failure: P1. |
| **OTH** | Depends on dependency criticality | Payment gateway: P1. Analytics feed: P3. Varies by the third-party's role in the value chain. |

---

## 12. Operational Notes

### For L1 / Service Desk

- **When in doubt, escalate up, not down.** It is always better to declare a higher priority and downgrade than to underestimate and lose response time. Nobody gets blamed for a false P1. People get blamed for a missed one.
- **Check the Knowledge Base first.** If a known scenario matches, use the documented priority and response. Do not re-invent the triage.
- **Application incidents are tricky.** If infrastructure looks healthy but something is wrong, and there is no KB match, assign a preliminary priority and loop in the tech team within 30 minutes. Do not try to diagnose application logic alone.
- **"It's the vendor's fault" is not a resolution.** We own the service to our users. Escalate to the vendor AND activate our contingency plan simultaneously.

### For Incident Commanders

- **P1/P2: Contain first, investigate second.** Rollback the deployment, failover to standby, enable maintenance mode -- then figure out root cause.
- **Manage communications actively.** Designate one person for all external updates. Engineers should not be pulled into status calls during active response.
- **Watch for scope creep.** A P2 that has been degraded for 3 hours during business hours may need reclassification to P1. Reassess at each status update.
- **Document everything.** Every decision, every action, every timeline entry. This feeds the Post-Incident Review and builds institutional knowledge.

### For Management

- **Trust the classification.** The matrix exists so that on-call staff can make priority decisions at 3 AM without calling management. If the team consistently misclassifies, fix the matrix and training -- do not add approval gates.
- **P3/P4 incidents do not need your attention.** The full war-room machinery is reserved for P1 and conditional P2. Over-escalation burns out the team and devalues the Major Incident declaration.
- **Post-Incident Reviews are investments, not overhead.** Every RCA action item that prevents a future incident saves multiples of the time invested. Protect the team's time to do them properly.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| **MTTA** | Mean Time to Acknowledge -- elapsed time from incident detection to first human response |
| **MTTR** | Mean Time to Resolve -- elapsed time from detection to service restoration (containment) or full root-cause fix (full resolution) |
| **Containment** | Service restored to a usable state, even if degraded. The bleeding has stopped. |
| **Full Resolution** | Root cause fixed, data remediated, monitoring confirms stability. Incident is truly over. |
| **Blast Radius** | Scope of impact: how many users, policies, transactions, or systems are affected |
| **IC** | Incident Commander -- coordinates response for P1/P2. Manages people and communication, not technical debugging. |
| **War Room** | Dedicated communication channel (Slack/Teams) for active P1/P2 incident response. Single source of truth during the incident. |
| **Major Incident** | An incident triggering the full response structure: IC, war room, management notification, mandatory Post-Incident Review. All P1 and qualifying P2 incidents. |
| **RCA** | Root Cause Analysis -- the "why" investigation conducted during Post-Incident Review |
| **PII** | Personally Identifiable Information -- policyholder name, ID number, health data, financial records, beneficiary details |
| **RPO** | Recovery Point Objective -- maximum acceptable data loss measured in time (e.g., RPO of 1 hour means we can lose up to 1 hour of data) |
| **RTO** | Recovery Time Objective -- maximum acceptable downtime before service must be restored |
| **SLI** | Service Level Indicator -- the metric used to measure service health (e.g., error rate, latency P99) |
| **KB** | Knowledge Base -- library of known incident scenarios and documented responses, built from RCAs |

---

## Appendix B: Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-03-19 | tcl-ito | Initial comprehensive classification matrix |

---

**Review Required**: This document should be reviewed by **tcl-cio** before implementation.
**Prepared by**: tcl-ito (IT Operations)
**Date**: 2026-03-19
