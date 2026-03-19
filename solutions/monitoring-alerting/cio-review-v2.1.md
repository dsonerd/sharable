# CIO Review — Monitoring & Alerting Roadmap v2.1

> **Reviewer**: CIO
> **Date**: 2026-03-20
> **Documents reviewed**: `monitoring-alerting-roadmap-overview.md` v2.1 (primary), `monitoring-alerting-roadmap-detail.md` v2.1 (secondary)
> **Previous review**: `cio-review-monitoring-roadmap.md` (v1.0 review, 43 findings)
> **Status**: Review complete

---

## Overall Verdict: APPROVED FOR EXECUTION PLANNING

This is a significant improvement over v1.0. The team has addressed all 43 findings from my previous review — every high-severity item has been resolved or has a credible resolution plan in place. The split into overview and detail documents was the right structural decision. The new content — journey-first monitoring, rider monitoring, SLOs, first 25 alerts, composite patterns, and the canonical data model — transforms this from a solid infrastructure monitoring plan into a genuine insurance observability program.

I am upgrading the verdict from "conditionally approved" to **approved for execution planning**. Phase 1 can begin, provided the pre-Phase 1 discovery tasks are completed and the two remaining conditions noted below are met.

---

## Part 1: Overview Document Review

### Presentation Quality

**Verdict**: APPROVED — Board-ready with minor adjustments

The overview document is suitable for presentation to the CEO, board, or department heads. It tells the story clearly: here is the problem, here is who solves it, here is what we monitor, here is what each department sees, here is what it costs, here is the timeline.

**Strengths**:
- The executive summary is tight. The problem/solution/target-state structure is exactly what a board expects. The sentence "Today, most incidents are discovered by users before IT detects them" is the kind of concrete framing that gets executive attention.
- The journey table (Section 3.1) translates technical monitoring into business language. A CEO reads "J2 Sales submission" and understands this is about revenue flow. That is the right level of abstraction.
- The stakeholder metrics section (Section 4) is the strongest part of the overview. Each persona has a clear goal, a table of what they see, concrete examples, and risk callouts. This demonstrates that the team understands its audience.
- The cost section is transparent. The wide range on OpenSearch and the note about pre-Phase 1 discovery to refine it builds credibility rather than undermining it.
- The regulatory citation caveat (Section 4, Compliance note) is honest and appropriate. Better to flag uncertainty than to present unverified legal references.

**Issues**:

| ID | Severity | Finding |
|----|----------|---------|
| V2-001 | Low | Section 9, item 1: "Approve this roadmap (v2.0)" should read "v2.1" — version number not updated in the next steps table. |
| V2-002 | Low | The overview references "Section 10 of detail doc" in the next steps for regulatory verification, but the detail document reorganized sections. The compliance section is now Section 11. Update the cross-reference. |
| V2-003 | Low | The Investment section (Section 7) shows annual estimate of $30,000-111,600. For board presentation, consider rounding: "$30K-$112K annually" reads more cleanly. The precise figures are appropriate for the detail document. |

### Completeness

**Verdict**: APPROVED

The overview covers all critical dimensions: team, monitoring scope, stakeholder views, tools, roadmap, investment, risks, dependencies, and next steps. Nothing material is missing for the target audience.

The stakeholder coverage is now comprehensive. The addition of Underwriting and Compliance/Risk personas addresses gaps from v1.0. The seven stakeholder views (Operations, Sales, Customer, Underwriting, Finance, Management, Compliance) map well to TCLife's organizational structure.

One observation: the overview does not include a dedicated "Engineering/SRE" stakeholder view. This is correct for the overview's target audience (CIO, Board, Department Heads) — engineering-facing metrics belong in the detail document, and they are there.

### Clarity

**Verdict**: APPROVED

The document is well-written. Technical jargon is minimal and appropriately placed. The ASCII architecture diagrams are clear without requiring specialized tools to render. The tables are consistently formatted.

The journey-first framing (Section 3.1) is an excellent clarity device. It translates "we monitor Prometheus metrics and OpenSearch logs" into "we trace the path from a customer browsing products to a policy being issued." That is the level of translation the board audience needs.

### Journey-First Approach

**Verdict**: APPROVED — Well integrated

The nine journeys (J1-J9) are well-chosen and cover the full insurance lifecycle: acquisition, submission, identity/payment, underwriting, issuance, servicing, billing, claims, and operations. The overview presents them at the right level of abstraction; the detail document provides the per-journey metrics, alert triggers, and phase assignments.

The cross-cutting treatment of riders (Section 3.2) is particularly strong. For a UL-focused insurer with CI, HI, and MR riders, rider defects are a genuine source of customer complaints, financial leakage, and regulatory risk. Elevating rider monitoring to a first-class dimension rather than burying it inside policy monitoring shows domain maturity.

### Stakeholder Metrics

**Verdict**: APPROVED WITH MINOR OBSERVATIONS

The metrics-by-stakeholder section is the standout contribution of the overview. Specific observations:

- **Operations**: The "exception taxonomy by reason/product/rider" metric is excellent — it gives Ops a root-cause lens that most monitoring plans omit.
- **Sales**: The inclusion of "post-issue quality (free-look, early cancellation)" is a sophisticated metric. It detects mis-selling or process defects at the monitoring level, before they become complaints.
- **Customer**: The "rider display and eligibility accuracy" metric is well-placed. Rider mismatch between quote and policy is a real complaint driver.
- **Underwriting**: "Decision mix by product/rider/channel" catching silent misconfiguration is the kind of second-order thinking that separates good monitoring from great monitoring.
- **Finance**: The "renewal due pipeline (7/30 day view)" is forward-looking, not just reactive. This gives Finance a risk view, not just a status view.
- **Compliance**: "Audit trail completeness" as a percentage metric is actionable — it can be measured and improved. Many compliance dashboards show binary pass/fail; a percentage gives nuance.

| ID | Severity | Finding |
|----|----------|---------|
| V2-004 | Medium | The overview omits **Actuarial** as a stakeholder persona. For a UL insurer, Actuarial has monitoring interests: NAV accuracy, fund price freshness, mortality/morbidity experience signals (claim frequency/severity vs. pricing assumptions), and persistency data (lapse rates by cohort feed valuation models). This does not need to be a full section in the overview, but a note acknowledging Actuarial as a Phase 3-4 consumer of monitoring data would be appropriate. The detail document's data model (Section 22) captures some of these fields, but the stakeholder connection is not made explicit. |
| V2-005 | Low | The "Management / CIO" stakeholder section shows "Journey health summary" as a metric, but the overview document does not describe what the journey health view looks like at the management level. Is it a traffic-light rollup of all nine journeys? A subset of the most critical? The detail document's Phase 3 deliverables mention "journey monitoring dashboards for J2, J4, J5, J7" — clarify whether all nine or a priority subset are surfaced to Management. |

### Team Feasibility

**Verdict**: APPROVED WITH ONE CONCERN

The 7-person team allocation is realistic. The staffing percentages per phase are honest — DevOps at 60% in Phase 1 is heavy but achievable if App Ops covers daily operations. The on-call model (6-week rotation, once every 6 weeks per person) is sustainable.

| ID | Severity | Finding |
|----|----------|---------|
| V2-006 | Medium | The overview correctly notes "DevOps engineers will need protected time — daily operations must be covered by App Ops to avoid Phase 1 stalling." This is the single biggest execution risk for Phase 1. It needs to be more than a note — it needs to be an explicit agreement between the App Ops and DevOps leads, documented and endorsed by the IT Manager. If an unplanned P1 incident in month 1 pulls two DevOps engineers into firefighting for a week, Phase 1 is immediately behind schedule. **Recommend formalizing this as a Phase 1 operating agreement, not just a note.** |

### Investment Case

**Verdict**: APPROVED

The cost model is complete. AWS services ($1,700-4,200/month) plus human costs ($800-5,100/month) gives a total of $2,500-9,300/month or $30K-112K annually. The ROI justification (faster detection, batch failure prevention, vendor accountability, regulatory readiness, operational efficiency) is qualitative but compelling for the investment size.

The wide range is honestly presented with the OpenSearch log volume explanation. The pre-Phase 1 discovery task to refine this is the right approach — ask for a budget range now, narrow it with data before committing.

For a company operating a life insurance platform with all the downstream financial and regulatory consequences of undetected failures, $30K-112K/year for comprehensive monitoring is a sound investment. The alternative — discovering incidents from user complaints, manually tracking batch jobs, relying on vendor self-reporting — carries higher cost in terms of operational risk, regulatory exposure, and customer trust erosion.

---

## Part 2: Detail Document — Previous Findings Resolution

### Resolution of Top 10 High-Severity Items

| ID | Finding | Resolution Status | Assessment |
|----|---------|-------------------|------------|
| **R-003** | Missing: Real User Monitoring | **RESOLVED.** Section 4.7 adds RUM with Grafana Faro. Phase 2 foundation, Phase 3 full. Metrics include page load, JS errors, geographic performance. | Satisfactory. Phasing is appropriate — RUM is not needed before infrastructure monitoring is solid. |
| **R-004** | Missing: AWS Cost Monitoring | **RESOLVED.** Section 4.8 adds cost monitoring. Phase 1 for billing alarms and Cost Anomaly Detection. | Satisfactory. Simple to implement, immediate value — correctly placed in Phase 1. |
| **R-016** | Missing: Commission batch monitoring | **RESOLVED.** Added to batch job landscape (Section 8.1), alert rules (Section 8.3), reconciliation (Section 8.5). Classified as High criticality with SEV2 alert. | Satisfactory. Commission failure is now treated with appropriate urgency. |
| **R-023** | Business KPI targets need validation | **RESOLVED.** Section 10.3 marks all targets as "pending validation." Business conversations start Phase 1-2, Phase 3 blocked until sign-off. | Satisfactory. The gating mechanism (Phase 3 blocked) ensures unvalidated thresholds do not become production alerts. |
| **R-026** | Regulatory citations need Legal verification | **RESOLVED.** Section 11.1 marks all citations "PENDING VERIFICATION" in bold. Action item to send to Legal/Compliance. | Satisfactory. The document no longer presents unverified citations as authoritative. Additional regulatory references (Insurance Business Law 08/2022/QH15, Decree 46/2023, Circular 67/2023, Decision 07/QD-TTg) strengthened from reference research — all properly flagged as pending verification. |
| **R-027** | Missing regulatory references | **RESOLVED.** Added Decree 13/2023/ND-CP on personal data protection, IT risk management references, and insurance data reporting requirements. All pending verification. | Satisfactory. The regulatory landscape is now more complete, with the appropriate caveat that Legal must validate. |
| **R-031** | No staffing plan | **RESOLVED.** Section 2 provides full team structure (7 people by role), per-phase allocation percentages, on-call rotation, external support needs, and a no-new-hires assumption with escalation path. | Well done. This is exactly what was needed. |
| **R-032** | Training must be Phase 1 deliverable | **RESOLVED.** Section 13 is a dedicated training plan. Skills gap assessment, training schedule in Month 1, budget estimate ($3,600-7,200), ongoing learning plan. | Well done. Training is no longer buried in a risk section — it is a first-class Phase 1 deliverable. |
| **R-036** | Human costs missing from cost model | **RESOLVED.** Section 15.3 adds human costs: on-call allowances, training (amortized), external support. Section 15.4 shows total program cost combining AWS and human. | Satisfactory. The opportunity cost of staff time is acknowledged as a note rather than quantified — this is pragmatic. |
| **R-040** | Missing risk: PII in monitoring data | **RESOLVED.** Entire new section (Section 12) on Data Protection and PII Policy. Covers the risk, scrubbing policy (Phase 1 design, Phase 2 implement), data sovereignty, and AWS region strategy. | Well done. This is now a properly treated concern, not an afterthought. |

**Assessment**: All 10 high-severity items are resolved. The resolutions are substantive, not cosmetic. The team did not merely acknowledge the findings — they integrated them into the architecture and phasing.

### Resolution of Medium and Low Severity Items

I have verified the resolution matrix in Section 17 of the detail document. All 21 medium-severity and 12 low-severity findings have documented resolutions with section cross-references. Spot-checking several:

- **R-009** (CTO vs CIO escalation): Corrected throughout. Verified in Section 5.2.
- **R-018** (Pushgateway anti-pattern): Batch Job Monitor now uses pull-based `/metrics` endpoint. Pushgateway reserved for ephemeral Lambda jobs only. Correct.
- **R-028** (Compliance dashboard too late): Basic compliance dashboard moved to Phase 2. Full dashboard remains Phase 4. This is the right balance.
- **R-035** (IaC from Phase 1): IaC foundation added to Phase 1 deliverables. Full migration remains Phase 4. Pragmatic and correct.
- **R-042** (Steering Committee): Governance section (16.3) defines committee structure, cadence, and membership.

**Assessment**: Medium and low severity items are all addressed. No regressions observed.

---

## Part 3: Detail Document — New Content Quality

### 18. Core Business Journeys (Section 18)

**Verdict**: APPROVED

The nine journeys are well-defined. Each has a critical span to trace, key metrics, and a phase assignment. The journey framework is clearly adapted from the reference research but contextualized for TCLife — the metrics map to TCLife's specific product mix and operational structure.

The rider monitoring cross-cutting table (Section 18.3) is excellent. It traces the rider lifecycle through eight stages across multiple journeys, with specific alert triggers at each stage. This is exactly the level of specificity needed for a UL insurer.

### 19. Domain-Specific Monitoring Matrices (Section 19)

**Verdict**: APPROVED

Five domain matrices (Underwriting/STP, Billing/Persistency, Claims, Ops Workflow, Security/Fraud/Compliance) provide implementation-grade detail. Each entry has a metric, alert trigger, and owner. These complement the journey framework — journeys show the horizontal flow, domain matrices show the vertical depth.

### 20. Service Level Objectives (Section 20)

**Verdict**: APPROVED

The SLO set is appropriately scoped — nine starter objectives covering the most critical service interactions. The SLI definitions are clean (ratio-based, measurable). The relationship between SLOs and KPIs (Section 20.3) is well-articulated — SLOs define reliability commitments, KPIs measure operational targets.

| ID | Severity | Finding |
|----|----------|---------|
| V2-007 | Medium | The SLO for "Payment callback" is set at 99.9% monthly. Given that payment callbacks are revenue-protecting and duplicate charge prevention depends on callback reliability, consider whether this target should be even tighter (99.95%) or whether the 99.9% is appropriate for a starter objective. This is a business judgment — validate with Finance. The detail document correctly notes "Revenue-protecting operation — tight target." I am satisfied with 99.9% as a starter, but flag it for early review once baseline data is available. |

### 21. First 25 Alerts (Section 21)

**Verdict**: APPROVED

The prioritized alert list is excellent. It demonstrates clear thinking about what matters most:

- Alerts 1-5 are all business-impacting: portal availability, login, submit, payment, issuance. These are the alerts that prevent P1 incidents from being discovered by users.
- Alerts 6-17 cover the infrastructure foundation that supports those business flows.
- Alerts 18-25 extend into business-specific domains (rider mismatch, STP, queue backlogs, security).

The split between Phase 1 (alerts 1-17) and Phase 2 (alerts 18-25) is clean and maps well to the roadmap phasing.

| ID | Severity | Finding |
|----|----------|---------|
| V2-008 | Medium | Alerts 3 (application submit below threshold) and 5 (policy issuance below threshold) are categorized as Phase 1 and SEV1, but these are business process metrics that Section 4.5 places in Phase 3 (Business Process Monitoring). This creates a sequencing question: how will alerts 3 and 5 fire in Phase 1 if the business process instrumentation is not in place until Phase 3? If these alerts are based on the Insuremo health prober or integration-layer metrics (which are Phase 2), they cannot be Phase 1. **Clarify whether these Phase 1 business alerts rely on existing instrumentation or require new instrumentation.** If the latter, either move them to Phase 2 or identify what minimal instrumentation is needed in Phase 1 to support them. |

### 22. Canonical Telemetry Data Model (Section 22)

**Verdict**: APPROVED

The data model spans 14 domains with minimum telemetry fields. The implementation notes correctly acknowledge that not all fields are needed from day one and that the model is a target schema dependent on what InsureMO exposes.

The cardinality management guidance (Section 22.3) is important: use stable business dimensions, avoid high-cardinality labels in Prometheus. This prevents a common failure mode where monitoring cost spirals due to metric explosion.

### 23. Composite Alert Patterns (Section 23)

**Verdict**: APPROVED

Five composite patterns (sales submission blocked, payment pipeline failure, underwriting stall, portal degradation, batch job chain failure) demonstrate mature alerting design. The principle — page only when multiple signals confirm real harm — is exactly right for reducing alert fatigue while maintaining detection confidence.

The implementation note that composite alerts require single-metric alerts to exist first (Phase 1-2) is correct. This ensures the foundation is in place before layering complexity.

### 7.3 InsureMO Instrumentation Checklist (Section 7.3)

**Verdict**: APPROVED

The business event checklist maps required events to journeys and specifies key fields. The guidance on rider-specific capture (eligibility decision, premium computation inputs, rider-package version, offer shown/accepted, issue result, claimability status) is thorough and reflects the cross-cutting rider monitoring theme.

### Rider Monitoring

**Verdict**: APPROVED

Rider monitoring is now treated as a first-class dimension throughout the document:
- Section 4.5: Rider lifecycle in business process monitoring
- Section 7.3: Rider-specific InsureMO instrumentation
- Section 18.3: Rider monitoring cross-cutting table across journeys
- Stakeholder metrics (overview): Rider pricing/eligibility accuracy for Sales, rider display accuracy for Customer, STP rate by rider for Underwriting

This is comprehensive and appropriate for TCLife's product mix.

---

## Part 4: Remaining Issues

### Issues Requiring Attention

| ID | Severity | Finding | Action Needed |
|----|----------|---------|---------------|
| V2-004 | Medium | Actuarial stakeholder missing from overview. NAV accuracy, fund price freshness, mortality experience, and persistency data feed actuarial models. | Add a note in the overview acknowledging Actuarial as a Phase 3-4 data consumer. Does not need a full section. |
| V2-006 | Medium | DevOps protected time in Phase 1 is a note, not a formal agreement. Execution risk. | Formalize as a Phase 1 operating agreement between App Ops and DevOps leads, endorsed by IT Manager. |
| V2-007 | Medium | Payment callback SLO (99.9%) should be validated with Finance early. | Flag for review once 30-day baseline data is available in Phase 2. |
| V2-008 | Medium | Alerts 3 and 5 (business process alerts) are assigned to Phase 1 but business process instrumentation is Phase 3. Sequencing mismatch. | Clarify what existing instrumentation supports these alerts in Phase 1, or move them to Phase 2. |
| V2-001 | Low | Version number "v2.0" in overview next steps should be "v2.1". | Update. |
| V2-002 | Low | Cross-reference "Section 10 of detail doc" should be "Section 11". | Update. |
| V2-003 | Low | Annual cost range ($30,000-111,600) could be rounded for board presentation. | Consider presentation formatting. |
| V2-005 | Low | Management journey health view not described in overview. | Clarify whether all nine journeys or a priority subset are surfaced to Management. |

### Conditions for Phase 1 Start

Phase 1 may begin once:

1. **Pre-Phase 1 discovery tasks complete**: OpenSearch inventory, log volume measurement, Prometheus cardinality check, EKS version verification (already defined in detail document Section 3.4).
2. **Budget approvals secured**: On-call allowances, training budget, PagerDuty/OpsGenie procurement, and Phase 1 AWS cost allocation.

The four medium-severity findings above (V2-004, V2-006, V2-007, V2-008) should be addressed during Phase 1 — they do not block Phase 1 start.

The regulatory citation verification (sending Section 11 to Legal/Compliance) must happen in parallel with Phase 1, as already documented in the next steps.

---

## Part 5: Assessment of Reference Research Integration

The reference research document (`reference.research.md`) is a comprehensive monitoring blueprint for a Vietnam life insurer on eBao InsureMO and AWS. The v2.1 documents demonstrate disciplined use of this research:

- **Journey framework**: Adopted intact. The nine journeys map directly from the research.
- **Domain monitoring matrices**: Adapted and contextualized. The research provides generic matrices; the detail document maps them to TCLife-specific roles and phasing.
- **SLO set**: Adopted as "starter objectives" with the correct caveat that thresholds need calibration from TCLife's own data. This is the right approach — the research provides reasonable defaults, not gospel.
- **First 25 alerts**: The detail document's list is substantively the same as the research's list, reordered to align with TCLife's phase structure and severity model.
- **Composite alerts**: Adopted with implementation guidance specific to TCLife's Prometheus/Alertmanager stack.
- **Data model**: Adopted as a target schema with appropriate implementation caveats.
- **Regulatory context**: The research's Vietnam-specific regulatory references (Insurance Business Law 08/2022/QH15, Decree 46/2023, Circular 67/2023, Decree 13/2023/ND-CP on personal data protection) have been incorporated into Section 11 — all properly flagged as pending Legal verification.
- **InsureMO instrumentation**: The research's instrumentation checklist has been adapted into Section 7.3 with TCLife-specific field mappings.

The team used the research as source material, not copy-paste. The integration shows judgment about what to adopt, what to adapt, and what to phase for later.

---

## Summary of Findings

### Medium (address during Phase 1)

| ID | Summary |
|----|---------|
| V2-004 | Actuarial stakeholder missing from overview |
| V2-006 | DevOps protected time needs formal operating agreement, not just a note |
| V2-007 | Payment callback SLO target should be validated with Finance early |
| V2-008 | Phase 1 business alerts (3, 5) may require instrumentation not available until Phase 2-3 |

### Low (address during normal refinement)

| ID | Summary |
|----|---------|
| V2-001 | Version number "v2.0" should be "v2.1" in overview next steps |
| V2-002 | Cross-reference to "Section 10" should be "Section 11" |
| V2-003 | Annual cost range could be rounded for board presentation |
| V2-005 | Management journey health view not described in overview |

---

## Commendations

1. **Document structure decision.** Splitting into overview and detail was exactly right. The overview is presentable to the board without dumbing down the content. The detail document is a technical reference that an engineer can implement from. Neither document tries to serve both audiences, which is why both succeed.

2. **Research integration discipline.** The team sourced a comprehensive external research document and integrated it with judgment — adopting frameworks (journeys, SLOs, data model), adapting specifics (alert thresholds, role assignments, phasing), and flagging where TCLife-specific calibration is needed. This is how research should inform practice.

3. **Previous review response quality.** All 43 findings addressed. The resolution matrix (Section 17) maps every finding to its resolution with section cross-references. The resolutions are substantive, not cosmetic. This demonstrates professional responsiveness to review feedback.

4. **Rider monitoring elevation.** Treating rider monitoring as a first-class cross-cutting dimension — not a sub-item of policy monitoring — shows genuine understanding of where life insurance operations go wrong. Rider defects cause complaints, financial leakage, and regulatory risk. The monitoring design now catches these at every lifecycle stage.

5. **Composite alerting.** The five composite alert patterns represent mature alerting design. Single-metric alerts are noisy; composite alerts that require multiple corroborating signals before paging give the on-call team higher confidence that each page represents real harm. This will directly contribute to the goal of reducing alert fatigue.

6. **Honest uncertainty handling.** Regulatory citations are flagged as pending verification. Business KPI targets are flagged as pending validation. Cost estimates are flagged as ranges requiring refinement. The document distinguishes between what the team knows, what it believes, and what it needs to verify. This builds credibility with every audience.

---

## Verdict for tcl-orch

**APPROVED FOR EXECUTION PLANNING.** The monitoring and alerting roadmap v2.1 is ready for Phase 1 initiation, pending completion of pre-Phase 1 discovery tasks and budget approvals. The four medium-severity findings (V2-004, V2-006, V2-007, V2-008) should be addressed during Phase 1 but do not block start.

The overview document is board-ready. The detail document is implementation-ready. The team has demonstrated professional competence, domain understanding, and responsiveness to review feedback.

This roadmap, when executed, will transform TCLife's monitoring from reactive (users discover incidents) to proactive (monitoring detects incidents before users notice). That is the correct trajectory for a regulated life insurer.

**Recommended next action**: Proceed with the next steps table in the overview document (Section 9). Priority items: budget approvals (items 1-2), regulatory citation verification (item 3), on-call tool selection (item 4), and pre-Phase 1 discovery (item 6).

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | CIO | Initial review of monitoring-alerting-roadmap.md v1.0 (43 findings) |
| 2.0 | 2026-03-20 | CIO | Review of v2.1 — overview and detail documents. Verdict upgraded to Approved for Execution Planning. 4 medium, 4 low findings. All previous high-severity items resolved. |
