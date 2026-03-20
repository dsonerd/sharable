# CIO Review — Monitoring & Alerting Roadmap v2.3

> **Reviewer**: CIO
> **Date**: 2026-03-20
> **Documents reviewed**: `monitoring-alerting-roadmap-overview.md` v2.3, `monitoring-alerting-roadmap-detail.md` v2.3
> **Previous reviews**: v1.0 review (43 findings), v2.1 review (4 medium, 4 low findings)
> **Research sources reviewed**: `deep-research-report.md`, `reference.research.md`
> **Review type**: Delta review (v2.1 to v2.3)
> **Status**: Review complete

---

## Overall Verdict: APPROVED FOR EXECUTION

This is the third review of this roadmap. v2.3 represents a material improvement over the already-strong v2.1 in three areas: regulatory precision, alerting maturity, and vendor integration strategy. The deep research findings have been integrated with the same discipline observed in v2.1 -- adopted where they strengthen the plan, adapted to TCLife's context, and properly caveated where Legal verification is still required.

I am upgrading the verdict from "Approved for Execution Planning" to **Approved for Execution**. The four medium-severity items from v2.1 are all addressed or rendered non-blocking (see Part 1 below). No new blocking issues were introduced. Phase 1 can begin immediately upon completing the pre-Phase 1 discovery tasks and securing budget approvals.

---

## Part 1: Resolution of v2.1 Findings

### Medium-Severity Items

| v2.1 ID | Finding | v2.3 Status | Assessment |
|---------|---------|-------------|------------|
| V2-004 | Actuarial stakeholder missing from overview | **Partially addressed.** The overview now routes lapse rate spikes to "Collections + Actuarial + Sales" in the business alert routing matrix (Section 5.13.2 of detail). Actuarial is acknowledged as a data consumer. However, no explicit Actuarial note appears in the overview stakeholder section. | Acceptable. The routing matrix covers the operational need. A formal Actuarial stakeholder section remains a Phase 3-4 item when business metric dashboards are built. Downgraded to low. |
| V2-006 | DevOps protected time needs formal operating agreement | **Not explicitly addressed in the documents.** The staffing plan (Section 2.3) still notes the risk but does not describe a formal operating agreement. | This remains a valid concern, but it is an execution management item, not a document item. It does not block Phase 1 start. The IT Manager must address this operationally. Moved to execution checklist. |
| V2-007 | Payment callback SLO (99.9%) should be validated with Finance early | **Addressed.** Section 5.5.3 now shows worked burn-rate alert examples for the payment callback SLO, and the SLO section continues to flag all targets as pending validation. The burn-rate approach actually makes early validation less critical -- burn-rate alerts detect abnormal consumption regardless of the exact target. | Satisfactory. The burn-rate approach reduces the risk of an incorrectly-set threshold causing either missed detection or false positives. Closed. |
| V2-008 | Phase 1 business alerts (3, 5) may require instrumentation not available until Phase 2-3 | **Not explicitly resolved**, but the expanded InsureMO integration section (7.2.0) provides a credible path: eBaoCloud native API gateway telemetry may surface enough data to support basic policy issuance and application submit rate signals in Phase 1-2, before full business process instrumentation in Phase 3. | Acceptable with caveat. Whether this works depends on what eBaoCloud actually exposes -- the Phase 2 prerequisite to inventory native telemetry will determine whether alerts 3 and 5 can fire in Phase 1 or must wait. Moved to execution checklist. |

### Low-Severity Items

| v2.1 ID | Finding | v2.3 Status |
|---------|---------|-------------|
| V2-001 | Version number "v2.0" in overview next steps | **Resolved.** Overview restructured for Confluence; next steps section removed (covered by other pages). |
| V2-002 | Cross-reference "Section 10" should be "Section 11" | **Resolved.** Same structural change. |
| V2-003 | Annual cost range could be rounded for board presentation | **Resolved.** Cost section removed from overview (covered by separate investment page). |
| V2-005 | Management journey health view not described | **Addressed.** Overview Section 2 now shows the Management/CIO metrics table with "Journey health summary" and a concrete example: "J2 Sales submission: green; J4 Underwriting: yellow (STP dip)." |

**Assessment**: All four low-severity items are resolved. The overview restructuring for Confluence elegantly eliminated three of them.

---

## Part 2: Regulatory Maturity Assessment

The deep research brought significantly more precise regulatory references. This is one of the strongest improvements in v2.3.

### What improved

1. **Personal Data Protection Law 91/2025/QH15** replaces the previously referenced Decree 13/2023/ND-CP as the primary data protection framework. This is a newer, more authoritative law. The three operational requirements are now precisely stated: 72-hour breach notification, 60-day cross-border transfer impact assessment dossier, and the recognition that observability data itself is regulated personal data. This last point -- that logs, traces, and canary artifacts containing PII are subject to the same protection as production customer data -- is a critical insight that many monitoring programs miss.

2. **AML Law 14/2022/QH15** is now cited with its effective date (1 March 2023) and with life-insurance-specific suspicious activity indicators. This connects AML obligations to concrete monitoring requirements (Section 4.6.6), not just a generic compliance checkbox.

3. **Insurance Business Law 08/2022/QH15** treatment is more nuanced. The document now correctly identifies it as imposing "outcome-based" requirements (demonstrable continuity, security, auditability) rather than prescriptive tooling mandates. This is the right interpretation and protects TCLife from over-engineering compliance monitoring.

4. **Circular 70/2022/TT-BTC** (risk management/internal control) and **Decree 53/2022/ND-CP** (cybersecurity/data locality) are added, broadening the regulatory landscape.

### Assessment

The regulatory section (Section 11.1) is now the most comprehensive regulatory mapping I have seen in a monitoring roadmap for a Vietnam insurer. The critical caveat -- "PENDING VERIFICATION" -- is consistently applied. The action item to send to Legal/Compliance is clear.

One observation: the volume of regulatory references has grown significantly. When this goes to Legal for verification, provide a prioritized list of which citations need verification first. My recommendation: (1) PDPL 91/2025/QH15 (highest operational impact -- drives PII scrubbing timeline and cross-border transfer assessment), (2) AML Law 14/2022/QH15 (drives fraud detection monitoring requirements), (3) Insurance Business Law 08/2022/QH15 (foundational but outcome-based, lower urgency for verification).

| ID | Severity | Finding |
|----|----------|---------|
| V3-001 | Low | When sending Section 11.1 to Legal, include a cover note prioritizing which citations need verification first, in the order above. This helps Legal focus rather than treating all 12+ citations as equal priority. |

---

## Part 3: Privacy-Incident Alerting (72-Hour Workflow)

Section 4.6.5 adds a dedicated privacy-incident alerting category. This is a material addition.

### Strengths

- **Distinct category, not a subset of security.** The decision to treat privacy incidents as a separate alert domain (with their own naming prefix `privacy_*` and routing to DPO/Compliance in addition to SecOps) is architecturally correct. Privacy incidents require a different response workflow than security incidents.
- **72-hour clock support.** The requirement to capture detection timestamp, scope, evidence trail, and containment actions is exactly what the DPO needs to decide whether notification is required and to prepare the notification if it is.
- **Observability data as regulated data.** The explicit inclusion of Macie scanning on S3 buckets storing Synthetics canary screenshots, trace exports, and RUM session replays demonstrates that the team understood the deep research finding about observability data being regulated. This is not obvious and many teams miss it.
- **Cross-border transfer alerting.** Alerting on data leaving designated data zones or routing to non-approved regions (VPC Flow Logs + CloudTrail) is a practical implementation of the PDPL cross-border transfer requirements.

### Concerns

| ID | Severity | Finding |
|----|----------|---------|
| V3-002 | Medium | The 72-hour clock starts when a breach is "detected," but the document does not define what constitutes "detection" in an alerting context. If Macie finds PII in a log bucket at 03:00 on Saturday and the SEV2 alert sits in the queue until Monday morning, has the 72-hour clock already started? **Recommend defining "detection" as the timestamp the alert fires, not when a human acknowledges it.** This has implications for after-hours privacy-incident routing -- privacy incidents may need SEV1-equivalent routing (immediate page) rather than SEV2 (which allows after-hours deferral for some scenarios per Section 5.10.3). |
| V3-003 | Low | The privacy-incident workflow says "Phase 2 for basic detection; Phase 3 for full workflow." Given the 72-hour notification obligation exists from day one of operations, consider whether the Phase 2 basic detection should include at minimum a manual escalation procedure and DPO notification template, even before the full automated workflow is in place in Phase 3. A manual interim process is better than no process. |

---

## Part 4: SLO Burn-Rate Alerting Assessment

### Is this the right sophistication level for a 7-person team?

Yes, with the phasing as designed. Here is my reasoning:

1. **The concept is sound.** Burn-rate alerting is the industry standard for reducing alert fatigue on customer-facing services. The alternative -- simple threshold alerting ("error rate > X% for Y minutes") -- generates either too many false positives (threshold too low) or misses gradual degradation (threshold too high). For a 7-person team, alert fatigue is an existential threat to the on-call program. Burn-rate alerting directly addresses this.

2. **The phasing is correct.** Burn-rate alerting is placed in Phase 3, after Phase 2 establishes SLI measurement. This is the right sequence. You cannot alert on burn rate without reliable SLI data, and you cannot get reliable SLI data without the instrumentation work in Phase 1-2.

3. **The worked examples are practical.** Section 5.5.3 shows concrete burn-rate calculations for three TCLife SLOs (Customer Portal availability, application submit success, payment callback success). The Prometheus recording rule example (Section 5.5.4) gives the DevOps team a copy-and-adapt starting point.

4. **The three-tier approach (fast/slow/gradual burn) matches the severity model.** Fast burn maps to SEV1, slow burn to SEV2, gradual burn to SEV3. This aligns with the existing severity levels and escalation rules without creating a parallel system.

5. **The relationship to other alert types is clearly articulated.** Burn-rate alerts complement -- do not replace -- hard threshold alerts for infrastructure. The document correctly states that both strategies coexist: hard thresholds for binary failures, burn-rate for gradual degradation.

### Concern

| ID | Severity | Finding |
|----|----------|---------|
| V3-004 | Low | The burn-rate examples use monthly error budgets. For a team new to SLO-driven alerting, monthly windows may be hard to reason about initially. Consider starting with weekly error budgets in Phase 3, then extending to monthly in Phase 4 once the team has developed intuition for burn rates. This is a training consideration, not a design flaw. |

---

## Part 5: InsureMO Native Telemetry Strategy

### Is leveraging eBaoCloud's existing gateway telemetry before building custom probers the right strategy?

This is one of the smartest changes in v2.3. Unequivocally yes, this is the right strategy. Here is why:

1. **It reduces Phase 2 delivery risk.** Building a custom Health Prober is engineering work that requires vendor coordination on probe frequency, test data, and endpoint access (Sections 7.2.2, 7.2.5, 7.2.7). If eBaoCloud already provides response time and success/failure metrics per API, TCLife gets immediate observability with zero custom development.

2. **It changes the vendor conversation.** Instead of asking EbaoTech "please allow us to probe your system" (which puts TCLife in a requesting position), the conversation becomes "please help us access the telemetry your platform already provides" (which is a reasonable customer request). This is a better negotiating posture.

3. **It layers correctly.** Native telemetry gives TCLife "what the vendor says is happening." The custom Health Prober gives TCLife "what we independently verify is happening." Both are needed, but the native telemetry is faster to obtain and covers more APIs than a prober can reach.

4. **The five-question table in Section 7.2.0** gives the team a concrete agenda for the EbaoTech conversation. This is actionable, not aspirational.

### Concern

| ID | Severity | Finding |
|----|----------|---------|
| V3-005 | Medium | The document does not address what happens if eBaoCloud's native telemetry is unavailable or restricted. The Phase 2 prerequisite says "document eBaoCloud native telemetry capabilities and agree on data sharing approach before finalizing Health Prober design." If this discovery reveals that native telemetry is vendor-internal-only or requires a contract amendment, Phase 2 timelines could slip. **Recommend adding a fallback plan**: if native telemetry access is not available within Month 4, proceed directly with the Health Prober design from v2.1 (which was already a sound approach). Do not let the better strategy block the good strategy. |

---

## Part 6: Data Sovereignty Assessment

### Are the Hanoi Local Zone and cross-border transfer considerations adequately addressed?

Section 12.3 is now substantively stronger. The key additions:

1. **Hanoi Local Zone is correctly characterized.** The document states that it is "not the same as a full in-country AWS region" and that data is "managed under the parent Singapore region." This is factually correct and important -- teams frequently misunderstand Local Zones as providing data residency guarantees they do not provide.

2. **Cross-border transfer scope is clearly defined.** The document identifies that if logs, traces, or session metadata containing PII flow to the Singapore region, this may constitute a cross-border transfer under PDPL 91/2025/QH15. This is the critical connection between observability architecture and regulatory compliance.

3. **The Phase 1 action items are practical.** (a) Document AWS regions for all monitoring components, (b) inventory which data streams contain PII, (c) assess whether Hanoi Local Zone can reduce cross-border transfer scope, (d) engage Legal on whether a transfer impact assessment dossier is required. These are concrete, achievable, and properly sequenced.

4. **The Phase 2 connection to PII scrubbing is insightful.** Aggressive PII redaction at the source reduces the scope of what constitutes "personal data" in the cross-border transfer. This gives TCLife a technical lever to reduce regulatory burden -- if all PII is stripped before data leaves Vietnam, the argument that the transfer involves "personal data" is substantially weakened.

### Concern

| ID | Severity | Finding |
|----|----------|---------|
| V3-006 | Medium | The document does not address the timeline pressure. If PDPL 91/2025/QH15 requires a cross-border transfer impact assessment dossier within 60 days of starting the transfer, and TCLife is already transferring observability data containing PII to the Singapore region today (via existing OpenSearch, AMP, and Grafana services), the 60-day clock may have already started or may be running. **Recommend adding this to the Phase 1 discovery tasks as a priority item**: determine with Legal whether the existing monitoring data pipeline constitutes a cross-border transfer that requires an impact assessment dossier. If the answer is yes, the dossier preparation must begin immediately and cannot wait for Phase 2. |

---

## Part 7: Document Structure Assessment

### Is the Confluence-focused overview the right approach?

Yes. The v2.3 overview removes executive summary, team details, cost details, risk section, and next steps -- all of which are covered by other Confluence pages. What remains is the substance: what we monitor, what each stakeholder sees, the tool landscape, and the roadmap summary.

This is the correct approach for a Confluence-hosted document. A Confluence page should contain exactly one topic's content. Cross-cutting concerns (team, budget, risks, governance) belong on their own pages. The overview now focuses on its core job: explaining the monitoring scope and roadmap to a non-technical audience.

The addition of the cross-cutting domains (Data Protection and Privacy, Rider Monitoring, AML/Fraud Production Telemetry) in the architecture diagram is a good structural choice -- it communicates that these are not separate monitoring programs but dimensions that cut across all eight monitoring domains.

No findings.

---

## Part 8: New Content Quality Assessment

### v2.2 additions (Sections 4 and 5 deep dive)

The v2.2 expansion of Monitoring Strategy and Alerting Strategy is thorough and implementation-grade. Specific highlights:

- **EKS deep dive (4.2.2)**: HPA scaling ceiling alerts, CoreDNS latency, and pod eviction monitoring are exactly the metrics that catch capacity problems before they manifest as application-layer symptoms. Well chosen.
- **Database deep dive (4.2.3)**: Connection pool monitoring at both the application level (HikariCP) and database level (RDS connections) is important. The distinction between pool exhaustion and database connection limits is one that many monitoring designs miss.
- **Deployment health (4.2.4)**: The error budget burn post-deploy rule (2x baseline error rate within 15 min of deploy) is a practical, implementable detection pattern.
- **Alert lifecycle management (5.7)**: The ITSM integration -- auto-creating tickets for SEV1/SEV2, requiring human confirmation before closure -- is operationally sound.
- **Alert naming convention (5.9)**: The `{domain}_{service}_{condition}` pattern with `privacy_*` and `aml_*` prefixes for the new domains is clean and extensible.
- **Business alert routing (5.13)**: Distinguishing technical alerts (engineering on-call) from business alerts (business stakeholder queues) is essential. The business alert format example (Section 5.13.3) is well-designed for non-technical recipients.

### v2.3 additions (from deep research)

- **AML/fraud as production telemetry (4.6.6)**: Correctly scoped to Phase 3-4 with an explicit requirement for Compliance/AML officer calibration before activation. The four detection categories (premium anomalies, early surrender, unusual beneficiary changes, agent anomalies) map well to industry AML guidance for life insurance.
- **CloudWatch RUM vs Grafana Faro evaluation (4.7)**: Presenting both options with decision criteria (data sovereignty, trace correlation, operational overhead) is the right approach for Phase 2 evaluation. The data sovereignty angle -- CloudWatch RUM keeps data within AWS ecosystem -- is a relevant consideration given the cross-border transfer discussion.
- **OTel instrumentation at InsureMO boundary (7.4)**: The PII redaction requirement for trace attributes is well-specified. The stable business correlation ID approach (tokenized policy/application IDs with a secure lookup table) balances investigative utility with data protection.

---

## Summary of Findings

### Medium (address during Phase 1)

| ID | Summary | Action |
|----|---------|--------|
| V3-002 | Privacy-incident "detection" timestamp is undefined; after-hours routing for privacy alerts may be insufficient for the 72-hour clock | Define "detection" as alert firing timestamp; consider SEV1-equivalent routing for privacy incidents |
| V3-005 | No fallback plan if eBaoCloud native telemetry is unavailable or restricted | Add fallback: if native telemetry not accessible by Month 4, proceed with Health Prober from v2.1 |
| V3-006 | Existing monitoring data pipeline to Singapore may already constitute a cross-border transfer requiring an impact assessment dossier within 60 days | Add to Phase 1 discovery: engage Legal immediately to assess whether current monitoring data pipeline requires PDPL dossier |

### Low (address during normal refinement)

| ID | Summary |
|----|---------|
| V3-001 | Prioritize regulatory citations when sending to Legal (PDPL first, then AML, then Insurance Business Law) |
| V3-003 | Phase 2 basic privacy detection should include a manual escalation procedure and DPO notification template even before Phase 3 automation |
| V3-004 | Consider starting with weekly error budgets for burn-rate alerting in Phase 3, extending to monthly in Phase 4, as a training aid |

---

## Execution Checklist (from v2.1 carryover)

These items from v2.1 are not document issues -- they are execution management items for the IT Manager and Phase leads:

| Item | Source | Action |
|------|--------|--------|
| DevOps protected time | V2-006 | IT Manager to formalize operating agreement between App Ops and DevOps leads before Phase 1 start |
| Business alert instrumentation | V2-008 | Phase 2 eBaoCloud telemetry inventory will determine whether alerts 3 and 5 can fire in Phase 1 or must wait |

---

## Commendations

1. **Regulatory precision.** The upgrade from generic "data protection regulation" references to specific law numbers, effective dates, and concrete operational requirements (72-hour notification, 60-day dossier, observability-data-as-personal-data) demonstrates genuine research depth. This positions TCLife ahead of most insurers in the region on compliance-aware monitoring design.

2. **Observability data as regulated data.** Recognizing that logs, traces, and canary artifacts are themselves subject to data protection law -- not just the production data they monitor -- is a sophisticated insight. Most monitoring programs treat observability data as purely operational. The PDPL makes clear it is not.

3. **InsureMO native telemetry strategy.** Flipping the vendor integration approach from "build probers first" to "leverage what the platform already provides first" is both pragmatically smart and strategically sound. It reduces engineering effort, improves time to value, and creates a better vendor relationship dynamic.

4. **Burn-rate alerting with worked examples.** Introducing SLO burn-rate alerting as a Phase 3 addition (not a Phase 1 requirement) demonstrates phasing discipline. The worked examples with actual TCLife SLO numbers make this implementable rather than aspirational.

5. **Overview restructuring for Confluence.** Removing content that belongs on other Confluence pages (team, budget, risks, next steps) and keeping only monitoring-specific content makes the overview a focused, maintainable document. This is the kind of structural discipline that keeps documentation current over time.

6. **Testing strategy expansion.** The addition of canary fail-on-demand tests, escalation routing drills, trace completeness tests, security simulations, and privacy tabletop exercises to the alert testing strategy (Section 5.11.2) transforms testing from "did the rule fire?" to "did the end-to-end response work?" This is the maturity level needed for a regulated insurer.

---

## Verdict for tcl-orch

**APPROVED FOR EXECUTION.** The monitoring and alerting roadmap v2.3 is ready for Phase 1 execution, pending completion of pre-Phase 1 discovery tasks, budget approvals, and the DevOps/App Ops operating agreement.

Three medium-severity findings (V3-002, V3-005, V3-006) should be addressed during Phase 1. V3-006 (cross-border transfer assessment for existing monitoring pipeline) is the most time-sensitive -- if PDPL 91/2025/QH15 applies to the current monitoring data flow to Singapore, the 60-day dossier clock may already be running. Engage Legal immediately.

The roadmap has improved materially across three review cycles: from 43 findings in v1.0, to 4 medium and 4 low in v2.1, to 3 medium and 3 low in v2.3. The team has demonstrated consistent ability to absorb feedback, integrate research, and produce implementation-grade documentation.

**Recommended next actions** (priority order):
1. **Immediately**: Engage Legal on PDPL 91/2025/QH15 applicability to existing monitoring data pipeline (V3-006)
2. **Before Phase 1 start**: Complete pre-Phase 1 discovery tasks; secure budget approvals; formalize DevOps/App Ops operating agreement
3. **Phase 1 Month 1**: Define "detection" timestamp for privacy incidents (V3-002); prepare prioritized regulatory citation list for Legal (V3-001)
4. **Phase 2 Month 4**: If eBaoCloud native telemetry not accessible, activate Health Prober fallback plan (V3-005)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-20 | CIO | Initial review of monitoring-alerting-roadmap.md v1.0 (43 findings) |
| 2.0 | 2026-03-20 | CIO | Review of v2.1 (4 medium, 4 low findings). Verdict: Approved for Execution Planning. |
| 3.0 | 2026-03-20 | CIO | Delta review of v2.3 (3 medium, 3 low findings). Verdict: Approved for Execution. |
