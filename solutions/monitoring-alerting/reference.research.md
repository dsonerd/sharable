**Comprehensive Monitoring & Alerting Blueprint**
 **Life Insurance Company in Vietnam (2026)**
 Context: eBao InsureMO core insurance platform, AWS-hosted services, sales portal, customer portal, underwriting/STP, riders



*Prepared as a practical operating document for Engineering, SRE, Operations, Sales Operations, and Business Owners*



| **Scope.** This document defines what to instrument, what to monitor, what to alert on, how to segment dashboards by persona, and what data model to retain for a Vietnam life insurer operating digitally on AWS in 2026. It combines Vietnam regulatory context, life-insurance operating flows, and AWS observability patterns. |
| --- |





**1. Executive summary**



For a Vietnam life insurer in 2026, monitoring cannot stop at CPU, memory, and uptime. It must prove that customers can buy, underwriters can decide, riders can attach correctly, premiums can post, policy servicing can complete, and regulated data is protected and auditable.



The operating model should be built around three layers of telemetry: (1) business outcomes, (2) journey and process health, and (3) platform, security, and dependency health.



The most important design decision is to monitor business journeys end-to-end: lead -> illustration -> quote -> application -> KYC/eKYC -> payment -> underwriting/STP -> policy issuance -> rider activation -> servicing -> renewal/persistency -> claims/benefits.



Alerting should be tiered. Page only for customer harm, revenue leakage, regulatory exposure, or material operational blockage. Route slower-burn anomalies to Ops/Sales Ops/Business queues instead of waking engineers unnecessarily.



**2. Vietnam 2026 context that changes the monitoring design**



Vietnam’s Insurance Business Law 08/2022/QH15 took effect on 1 January 2023. It requires insurers to establish, maintain, and operate information systems appropriate to their scale and to support updating, processing, storing, and securing insurance information. The law also requires insurers to provide insurance data to the national insurance business database and to ensure confidentiality and information security.



The law explicitly frames technology use across product design, risk assessment, underwriting, contracting, policy administration, loss assessment, claims settlement, statistics, reporting, forecasting, and anti-fraud. That means observability must cover both business process completeness and evidentiary audit trails.



Vietnam’s 2030 insurance market strategy targets average annual growth of insurance products distributed on digital channels of 10% during 2023-2030. This makes digital sales-path reliability a board-level KPI, not just an IT KPI.



The market context remains meaningful in 2025: preliminary industry figures reported H1 2025 life premium revenue of VND 67.242 trillion, new business premium of VND 11.728 trillion, more than 11.7 million in-force contracts, and benefit payments of VND 27.468 trillion. In 10M 2025, total market premium across life and non-life was estimated at VND 189.6 trillion. Monitoring should therefore prioritize premium capture, policy persistency, benefit servicing, and trust-preserving customer experience.



Product rules changed materially under Decree 46/2023 and Circular 67/2023. From 1 July 2025, investment-linked life products are expected to separate core benefits from supplementary riders such as critical illness, accident, and hospitalization. Monitoring must therefore treat rider attachment, eligibility, pricing, issuance, renewal, and claimability as first-class telemetry dimensions.



Vietnam personal-data protection rules require organizational and technical measures, system logs for personal-data processing, and breach notification processes. For a life insurer, this affects monitoring of consent, PII/health-data access, export, retention, data deletion, and third-party processing.



| **Implication.** Your observability program must satisfy four goals at once: keep digital sales flowing, keep underwriting/servicing operations moving, protect sensitive customer data, and produce evidence for audit/regulatory reporting. |
| --- |





**3. What life-insurance data you should collect and retain**



At minimum, the insurer should maintain a canonical event and metric model across the following domains. Use a unique journey ID / application ID / policy ID / rider instance ID to stitch events end-to-end across portals, InsureMO services, underwriting engines, payment, messaging, CRM, and document services.



| **Data domain** | **Minimum telemetry / master data fields** |
| --- | --- |
| Customer & prospect | customer_id, lead_id, segment, acquisition channel, campaign, assigned agent, province, device/browser, consent status, eKYC status, fraud flags |
| Quote / illustration | quote_id, product, rider set, premium mode, premium amount, sum assured, benefit illustration version, save/submit timestamps, quote acceptance status |
| Application / proposal | application_id, required fields completion %, document completeness, medical question set version, declaration flags, underwriting class requested |
| eKYC / identity | KYC provider, status, retries, OCR confidence, liveness result, mismatch reason, document expiry, watchlist / sanctions outcome if used |
| Payment | transaction_id, gateway, authorization result, capture result, amount, currency, duplicate-payment flag, refund/void, settlement status |
| Underwriting / STP | underwriting_case_id, straight-through/manual/referral path, rules triggered, score, evidence requested, turnaround time, pending reason, decision, decision owner |
| Policy issuance | policy_id, issuance timestamp, effective date, cooling-off state, schedule creation, document generation, delivery status, policy pack acknowledgement |
| Riders | rider_code, rider eligibility result, rider premium, attach/detach status, rider issue timestamp, rider renewal status, rider claim events |
| Billing / collections | installment schedule, next due date, grace status, collection attempts, auto-debit success, arrears bucket, lapse / reinstatement status |
| Servicing | endorsement type, beneficiary change, address/contact change, policy loan, top-up, partial withdrawal, surrender, turnaround time, failure reason |
| Claims / benefits | claim_id, event type, FNOL timestamp, document completeness, triage result, fraud flags, adjudication outcome, payout turnaround, repudiation reason |
| Agent / distribution | agent_id, activity funnel, login, quote count, proposal count, conversion, cancellation/free-look, persistency by cohort, training/licence status if managed in platform |
| Ops / workflow | queue, work item age, backlog volume, SLA breach count, manual touches, handoff count, rework rate, exception reason taxonomy |
| Compliance / audit | consent events, policy wording version, disclosure shown/accepted, data export, privileged access, report submission status, immutable audit trail |





**4. Design principles for the monitoring model**


- Monitor by customer journey first, service second. A healthy microservice estate can still hide a broken submit flow or underwriting queue.
- Every important action must emit both a business event and a technical event.
- Every failed customer step must have a machine-readable failure code, human-readable message, and ownership tag.
- Use golden signals for every critical API: traffic, latency, errors, saturation. Then add domain signals such as quote saves, STP %, rider attach rate, payment success, and policy issuance success.
- Segment all metrics by channel (agency, bancassurance, digital direct, partner), product, rider, sales team, geography, release version, and vendor dependency.
- Keep cardinality controlled: use stable business dimensions, not arbitrary free-text.
- Route alerts to the team that can act: SRE, platform, app squad, underwriter desk, policy admin Ops, Sales Ops, fraud/compliance, or vendor management.
- Store audit-grade events for regulated and sensitive actions.


**5. Personas and what “good” looks like**



| **Persona** | **Primary goal** | **What good looks like** | **Top risks to surface early** |
| --- | --- | --- | --- |
| End user / customer | Buy, view, pay, service, and claim without friction | Fast page loads, successful login, no broken forms, clear policy documents, payment success, quick servicing | Slow portals, broken eKYC, payment failures, policy pack not delivered, rider mismatch, duplicate charges |
| Sales / agent / partner | Illustrate, quote, submit, and track case status quickly | High quote-to-submit conversion, low dropout, fast proposal save, immediate visibility of case status and missing requirements | Portal outage, quote errors, rider pricing defects, lead assignment delays, case status not updating, high cancellation/free-look |
| OPS user | Work queues stay current and SLA compliant | Backlogs visible, no stuck cases, clean exception taxonomy, predictable TAT, low manual rework | Queue pile-up, integration failures, document/image delays, rules-engine errors, payment posting mismatch |
| Engineering / SRE / platform | Keep systems reliable and recover fast | Clear SLOs, low MTTR, actionable alerts, service dependency visibility | Silent failures, alert fatigue, missing traces, unhealthy targets, database saturation, queue backlog |
| Risk / compliance / audit | Protect data and prove control effectiveness | Complete audit trails, access anomalies surfaced, report completeness, policy wording traceability | Sensitive-data leakage, unlogged access, failed report loads, policy disclosure/version mismatch |





**6. Recommended observability architecture on AWS**


- Use CloudWatch as the operational hub: metrics, logs, alarms, Synthetics, RUM, dashboards, and Application Signals SLOs.
- Instrument portals and APIs with distributed tracing (OpenTelemetry or AWS-native integrations) so a failed application submit can be followed from browser to API gateway/load balancer to app service to InsureMO/core to database/queue.
- Use CloudWatch RUM on customer and sales portals to capture page load time, JavaScript errors, browser/device breakdown, and end-user impact.
- Use CloudWatch Synthetics canaries for the most important flows even when there is no live traffic: public portal landing, login, quote retrieval, application submit, payment callback, customer self-service, and core case-search paths.
- Use Application Signals SLOs for business-critical services and operations: quote create, application submit, underwriting decision, policy issue, premium post, customer login, document download.
- Collect infrastructure metrics from ALB, ECS/EKS/EC2/Lambda, RDS/Aurora, SQS/EventBridge, cache, WAF, and AWS Health events routed through EventBridge to notifications and incident automation.
- Separate dashboards into executive/business, operations/process, application, platform, security/compliance, and vendor dependency views.


**7. Core journeys to monitor end-to-end**



| **Journey** | **Critical span to trace** |
| --- | --- |
| J1 Digital acquisition | Landing -> product browse -> quote/illustration start -> lead capture -> agent assignment / digital direct continuation |
| J2 Sales submission | Illustration -> rider selection -> proposal save -> document upload -> declaration -> payment init -> application submit |
| J3 Identity & payment | eKYC / liveness / OCR -> payment auth/capture -> callback -> receipt issuance |
| J4 Underwriting | STP rules -> referrals -> manual underwriting -> evidence requests -> decision -> offer / counter-offer / reject |
| J5 Policy issuance | Policy number generation -> schedule / accounting posting -> document generation -> delivery / acknowledgement -> rider activation |
| J6 After-sales servicing | Contact changes, beneficiary change, premium mode change, loan/withdrawal/top-up, rider add/drop where allowed |
| J7 Billing & persistency | Renewal due -> debit attempt -> grace -> arrears -> reinstatement / lapse |
| J8 Claims & benefits | FNOL -> intake -> assessment -> fraud checks -> approval/reject -> payment |
| J9 Agent/Ops productivity | Queue receive -> case work -> handoff -> closure -> quality check |





**8. Detailed monitoring matrix by domain**



**8.1 Customer portal / end-user monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Portal availability | synthetic success %, HTTP availability, DNS/TLS health | Protects revenue and trust | P1: core canary fails 2 consecutive runs or availability < 99% over 15 min | SRE / app squad |
| Page performance | p95 page load, p95 LCP-equivalent, JS error rate by page | Slow experience kills conversion and servicing success | P2: p95 load worsens >50% vs baseline for 15 min; P1 if checkout/login pages breach agreed SLO | Digital squad |
| Login and session health | login success %, OTP delivery latency, token refresh failure, forced logout rate | Customers must access policies and servicing | P1 if login success < 95% for 10 min; P2 if OTP latency spikes | Identity team |
| Quote/illustration journey | start-to-complete conversion, save failure %, premium calc latency | Core sales conversion metric | P2 if save failure > 2%; P1 if premium calc errors spike | Sales app team |
| Application submit | submit success %, form validation failure by reason, doc upload failure %, submit latency | Direct indicator of new business blockage | P1 if submit success < 97% for 10 min or zero submits with normal traffic | Sales/app team |
| Payment | payment initiation success %, callback success %, duplicate charge count, receipt generation success | Immediate premium/revenue protection | P1 on duplicate-charge anomaly or payment callback failures; P2 on success drop >3 pts | Payments squad |
| Policy document access | download success %, p95 render/download latency | Impacts trust, service, and compliance | P2 if download success < 98% for 15 min | Customer servicing team |
| Self-service transactions | endorsement completion %, profile change success %, beneficiary-change SLA | Customer-care value and call deflection | P2 if any key servicing flow success < target | Customer service product owner |
| Rider display / eligibility | rider offer visibility %, eligibility rule error %, mismatch between quote and issue | Rider defects create complaints and leakage | P1 if quote/issue rider mismatch > threshold; P2 if eligibility engine errors rise | Product/rules team |





**8.2 Sales portal / agent monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Agent login & MFA | login success, MFA failure, lockout rate | Lost selling time directly hurts NBP | P1 if widespread login issue; P2 if lockouts abnormal | Identity / Sales IT |
| Lead assignment | lead routing latency, unassigned lead count, stuck lead queue age | Prevents lead decay | P2 if queue age > 15 min for hot leads | Sales Ops |
| Quote throughput | quotes created/hour, p95 quote time, quote calculation error rate | Confirms field productivity | P2 if quote throughput drops materially vs baseline with normal logins | Sales app owner |
| Proposal save/resume | draft save success, resume success, draft corruption count | Field teams need resiliency | P2 if save/resume < 99% | Sales app owner |
| Submission quality | incomplete submission rate, missing-doc rate, rider conflict rate | Downstream Ops load signal | Business alert when rate breaches by product/channel for a day | Sales Ops / training |
| Case-status visibility | status update lag from core to portal, stale status count | Agents need accurate next actions | P2 if status sync lag > 5 min on average; P1 if halted | Integration team |
| Post-issue quality | free-look rate, early cancellation, payment bounce after sale | Detects mis-selling or process defects | Business alert daily/weekly by agent/channel | Sales leadership / compliance |





**8.3 Underwriting and STP monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| STP rate | % cases auto-decisioned by product/channel/rider | Primary cost and turnaround metric | Business alert if STP drops >5 pts vs baseline for 1h/day | Underwriting / rules owner |
| Decision latency | p50/p95 underwriting TAT from submit to decision | Customer and sales experience | P2 if p95 exceeds SLA; P1 if queue stoppage causes hard breach | Underwriting Ops |
| Referral volume | manual referral count, age buckets, oldest case age | Detects capacity or rule defects | P2 if backlog age > SLA | Ops manager |
| Rules-engine health | rule evaluation latency, rule error count, external-data timeout | STP depends on stable decisioning | P1 if rule errors > threshold or external dependency timeouts spike | Rules/integration team |
| Medical evidence workflow | APS/lab request success, document turnaround, missing evidence aging | Life underwriting often stalls here | Business/Ops alert by backlog bucket | Underwriting Ops |
| Decision mix anomaly | approve/refer/decline/counter-offer by product/rider/channel | Catches silent misconfiguration | Business anomaly alert on sudden distribution shift | Chief underwriter |
| Underwriting data quality | missing declarations, conflicting answers, OCR extraction mismatch | Bad data creates risk leakage | Business alert daily by source/channel | UW governance |





**8.4 Policy issuance and rider administration**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Policy number generation | issue success %, duplicate policy number, issue latency | Direct fulfillment KPI | P1 if issuance success drops or duplicates occur | Core platform team |
| Accounting / posting | premium posting success, suspense items, posting reconciliation gaps | Finance and policy accuracy | P1 if posting halted; P2 if suspense backlog rises | Finance systems / Ops |
| Document generation | policy pack generation success, render time, template version mismatch | Compliance and customer communications | P1 if pack generation halted; P2 if mismatch detected | Document services owner |
| Rider activation | rider issue success %, rider premium posting %, rider effective-date mismatch | Riders are a major defect hotspot | P1 on quote/issue mismatch or failed activation | Product admin team |
| Outbound delivery | email/SMS delivery success, bounce rate, open/ack rate where relevant | Proof of service and customer communication | P2 if delivery success drops materially | Messaging team |
| Cooling-off / free-look | free-look request volume, processing SLA, reversal success | Protects complaints and accounting correctness | Business + Ops alert if volume spike or reversals fail | Ops / finance |





**8.5 Billing, collections, and persistency**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Renewal due pipeline | policies due next 7/30 days, premium at risk | Forward-looking revenue risk | Daily business alert for abnormal due vs collected gap | Collections / finance |
| Auto-debit success | bank/card debit success %, retry success, return codes | Immediate persistency signal | P1 if gateway/bank-wide failure; P2 if success dips below threshold | Payments / collections |
| Grace and arrears | grace count, aging buckets, premium in arrears, lapse risk | Core life-insurance health metric | Business alert daily by cohort/channel | Collections / actuarial / sales |
| Lapse/reinstatement | lapse rate, reinstatement rate, turnaround time | Tracks policy quality and recoverability | Weekly alert on abnormal cohort shift | Business owner |
| Collection controls | duplicate retries, wrong amount posted, premium allocation errors | Prevents complaints and leakage | P1 on financial posting defect; P2 on growing exception queue | Finance systems |





**8.6 Claims / benefit servicing (recommended even if not phase 1)**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| FNOL intake | FNOL submission success, attachment success, p95 latency | Customer distress moment; must work | P1 if FNOL unavailable | Claims digital team |
| Claims backlog | open claims by aging bucket, oldest claim age, missing-doc age | SLA and complaint driver | P2/P1 depending on breach severity | Claims Ops |
| Decision quality | approve/pend/reject mix, reopen rate, leakage/fraud flags | Operational and risk control | Business anomaly alert | Claims leadership |
| Payout execution | payment success, payout reversal, bank-return rate | Critical benefit promise | P1 if payout channel fails | Claims + finance |





**8.7 Ops workflow and exception monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Work queues | items by queue, oldest item age, SLA breach count | Heart of back-office control | P1 if queue frozen; P2 if oldest age crosses SLA | Ops control tower |
| Stuck cases | no-status-change > N minutes/hours, repeated retries, dead-letter volume | Prevents silent failure | P1 if systemic; P2 if local backlog | Ops + integration |
| Manual rework | cases touched >1 time, re-open rate, handoff count | Measures inefficiency | Daily business alert | Process owner |
| Exception taxonomy | volume by reason code, by product/rider/channel/release | Root-cause lens | Daily/weekly anomaly alert | Ops excellence |
| Batch / EOD / reconciliations | job completion, duration, late finish, reconciliation breaks | Essential for next-day business integrity | P1 if failed or incomplete | Platform/Ops/finance |





**8.8 Platform, application, and AWS monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| Load balancer / ingress | HealthyHostCount, UnHealthyHostCount, TargetResponseTime p95/p99, HTTPCode_Target_5XX_Count, TLS negotiation errors | First external chokepoint | P1 on unhealthy hosts or sustained 5XX; P2 on latency degradation | SRE |
| Compute services | service CPU/memory utilization, desired vs running tasks/pods, restart/crash loop count | Detects saturation and deployment issues | P1 if capacity lost; P2 if sustained saturation > 80% | Platform team |
| Lambda/serverless | Errors, Duration, Throttles, ConcurrentExecutions, iterator age if async/stream triggers | Catches quota and scaling issues | P1 on throttles/errors for critical functions | Serverless squad |
| Databases | CPUUtilization, DatabaseConnections, storage free %, read/write latency, slow query counts, replica lag where relevant | Most common bottleneck in core insurance | P1 on connectivity/storage risk; P2 on sustained latency | DBA/platform |
| Queues and event bus | ApproximateAgeOfOldestMessage, ApproximateNumberOfMessagesVisible, DLQ visible messages, EventBridge invoke failures | Async backbone health | P1 on DLQ growth or backlog age beyond SLA | Integration team |
| Cache/search | latency, hit ratio, evictions, memory pressure, cluster health | Performance and resiliency | P2 on sustained degradation | Platform |
| Deployments | error budget burn after release, 5XX delta, rollback rate, canary health | Fast detection of change failures | P1 if release burns error budget rapidly | Release manager/SRE |
| AWS Health | account-specific service events and public events routed via EventBridge | Catches provider-side impact early | P2/P1 depending on affected workload | Cloud platform |





**8.9 Security, fraud, and compliance monitoring**



| **What to monitor** | **Metric / indicator** | **Why it matters** | **Suggested alert trigger** | **Owner** |
| --- | --- | --- | --- | --- |
| WAF / edge protection | BlockedRequests, allowed vs blocked trend, challenge/captcha metrics, low-reputation denied requests | Detects attacks and false positives | P1 if attack impacts service; P2 on block surge or false-positive spike | SecOps |
| Identity security | admin login anomalies, MFA bypass attempts, privilege escalation, inactive-account use | High-risk control failures | P1 for privileged anomalies | IAM/SecOps |
| PII / health data access | sensitive-data read/export volume, unusual query patterns, after-hours access, mass-download attempts | Life insurers hold sensitive data | P1 for confirmed high-risk events | SecOps / DPO |
| Consent & privacy controls | consent capture success, consent withdrawal processing, data-subject request SLA, deletion completion | Required governance evidence | P2 if requests miss SLA; P1 if control breaks | Compliance / DPO |
| Audit trail completeness | % critical actions logged with actor/time/object/result | No audit trail = control failure | P1 if logging gaps detected on regulated actions | Platform + compliance |
| Fraud indicators | duplicate identities, repeated failed KYC, payment/card anomalies, suspicious claim/application clusters | Early fraud interception | P2/P1 depending on severity | Fraud team |





**9. Recommended SLO set**



Set a small number of top-level SLOs first. Everything else supports them.



| **Service / journey** | **SLI** | **Starter objective** | **Notes** |
| --- | --- | --- | --- |
| Customer portal availability | successful synthetic runs / total runs | 99.9% monthly | Run from Vietnam + one external region |
| Customer login | successful login requests / total login requests | 99.5% monthly | Separate OTP provider failures |
| Quote create | successful quote creates / total quote attempts | 99.5% monthly | Segment by product/channel |
| Application submit | successful submits / total attempts | 99.5% monthly | Track both frontend and backend commit |
| Payment callback | successful callbacks / total payment completions | 99.9% monthly | Revenue-protecting operation |
| Underwriting decision latency | % cases decided within SLA | 95% within agreed SLA | Use separate STP and manual SLA |
| Policy issuance | successful issuance / eligible-to-issue cases | 99.7% monthly | Core fulfillment SLO |
| Billing collection | successful premium postings / successful collections | 99.9% monthly | Finance-critical |
| Ops work item timeliness | % work items closed within SLA | 95% by queue | Use queue-specific SLA |





**10. Alert design: what should page vs what should ticket**



| **Severity** | **Use for** | **Examples** | **Response target** |
| --- | --- | --- | --- |
| P1 / Critical | Immediate customer harm, revenue blockage, regulatory/security risk | customer/sales portal unavailable; application submit down; payment callback halted; issuance halted; privileged-data exfiltration signal | Page on-call immediately |
| P2 / High | Severe degradation with workaround or growing material risk | STP collapse, queue backlog breaching same-day SLA, OTP delays, rising 5XX, RDS latency saturation | Page business-hours / fast response |
| P3 / Medium | Operational inefficiency or localized issue | single channel conversion dip, one product rider mismatch, elevated manual rework, template rendering delays | Create ticket / queue for owner |
| P4 / Low / Insight | Trend watch, optimization, capacity planning | error budget burn watch, cost drift, rising empty receives, low cache hit ratio | Dashboard/report only |




- Every alert should include: business impact, affected product/channel/rider, first seen, current severity, likely owner, linked dashboard, recent deployment/change context, sample trace or failed event IDs, and recommended runbook.
- Use composite alerts for paging. Example: page only when application submit success falls and queue backlog rises and no successful issue events are observed. This cuts noise and increases trust.
- Create anomaly alerts for business metrics that are not well served by static thresholds: quote-to-submit conversion, rider attach rate, decision mix, free-look rate, early lapse, claims reopen rate.


**11. Dashboard design by audience**



| **Dashboard** | **Must-show widgets** |
| --- | --- |
| Executive / command center | NBP today vs target, submissions, issuance, payment success, STP %, backlog by queue, critical incidents, top channels/products, lapse risk, complaints signal |
| Digital channel dashboard | RUM web vitals, portal availability, funnel conversion, page errors, login success, payment success, region/device/browser split |
| Sales Ops dashboard | agent logins, quotes, proposals, incomplete apps, lead routing, case-status lag, free-look/early cancellation by agent/channel |
| Underwriting dashboard | STP %, referrals, decision TAT, evidence aging, rule failures, decision mix by product/rider |
| Policy admin / collections dashboard | issuance success, posting exceptions, delivery success, renewal due, grace, lapse/reinstatement, suspense items |
| Platform / SRE dashboard | SLOs, error budget burn, ALB health, compute saturation, DB latency, queue backlog, deploy health, AWS Health events |
| Security / privacy dashboard | WAF trends, privileged access, anomalous data access, consent metrics, audit trail completeness, DSAR SLA |





**12. Instrumentation checklist for eBao InsureMO-based core**


- Emit business events at every policy-life-cycle transition: quote_created, quote_saved, application_submitted, kyc_passed, payment_authorized, underwriting_referred, underwriting_decided, policy_issued, rider_issued, premium_posted, document_delivered, renewal_due, premium_collected, lapse_started, reinstated, claim_registered, claim_paid.
- For every InsureMO API call, capture: endpoint, operation name, business object, tenant/environment, request ID, correlation ID, latency, response code, idempotency key, retry count, failure class, vendor/service dependency, release version.
- For worklists and queues, capture item create time, owner, queue, SLA due, last status change, retry count, exception reason, and closure reason.
- For rider logic, capture rider eligibility decision, premium computation inputs, rider-package version, offer shown, offer accepted, rider issue result, and downstream claimability status.
- For document generation, capture template version, product/rider version, generation result, delivery channel, and acknowledgement status.
- For every cross-system update, store before/after status and reconciliation markers so silent sync failures are visible.


**13. Suggested phased rollout**



| **Phase** | **Outcome** | **Main deliverables** |
| --- | --- | --- |
| Phase 1: 30-45 days | Golden journeys, core alerts, synthetic checks, top dashboards | Customer portal availability, sales portal login, quote/app submit, payment callback, underwriting queue, policy issuance, ALB/compute/DB/queue alarms, on-call routing |
| Phase 2: 45-90 days | Business observability and SLOs | RUM, Application Signals SLOs, decision-mix anomalies, rider monitoring, collections/persistency, release-health dashboards, better runbooks |
| Phase 3: 90-180 days | Control tower and compliance depth | privacy/access analytics, DSAR telemetry, fraud patterns, executive scorecards, predictive lapse/backlog alerts, automated remediation |





**14. First 25 alerts to implement**


1. Public customer portal synthetic failure
2. Sales portal login success below threshold
3. Application submit success below threshold
4. Payment callback failures above threshold
5. Policy issuance success below threshold
6. Rider issue mismatch between quote and issue
7. Underwriting STP rate sudden drop
8. Underwriting oldest case age above SLA
9. Work queue backlog age above SLA
10. ALB unhealthy targets > 0
11. ALB target 5XX sustained
12. ALB p95 target response time breach
13. Compute service desired != running
14. Compute CPU/memory saturation sustained
15. Lambda throttles > 0 for critical functions
16. RDS connection/latency/storage risk
17. SQS backlog age or DLQ messages > 0
18. EventBridge failed invocations rise
19. Document generation halted
20. Outbound delivery success drop
21. Auto-debit success rate drop
22. Privileged access anomaly
23. Sensitive-data export anomaly
24. WAF block/challenge surge with customer impact
25. AWS Health event impacting critical services




| **Starter thresholds.** Use the thresholds in this document only as initial operating baselines. Final thresholds must be calibrated from your own volume, seasonality, product mix, channel mix, and acceptable business risk. For life insurance, daily and weekly cohort analysis is as important as minute-level technical alarms. |
| --- |





**15. Source notes used for the 2026 tailoring**


- S1. Luật Kinh doanh bảo hiểm 08/2022/QH15 (Vietnam Insurance Business Law), effective 01/01/2023 — provisions on insurance data, IT application, and information-system requirements.
- S2. Circular 67/2023/TT-BTC — insurance data/reporting templates, including life-insurance insured-person and risk data dimensions such as age, gender, smoking status, insured risks, and policy year statistics.
- S3. Government communication on Decision 07/QĐ-TTg — digital insurance distribution target averaging 10% annual growth during 2023-2030.
- S4. Ministry of Finance / finance-sector reporting on 2025 market figures and life-insurance restructuring context.
- S5. Vietnam personal-data protection decree 13/2023/NĐ-CP — organizational/technical protection duties and system-log requirements.
- S6. AWS CloudWatch documentation for Application Signals SLOs, RUM, Synthetics canaries, ALB metrics, ECS metrics, Lambda metrics, RDS metrics, SQS metrics, AWS Health EventBridge integration, and AWS WAF monitoring.


*End of document*
