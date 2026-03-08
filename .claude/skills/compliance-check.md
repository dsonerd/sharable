# Skill: Compliance Check

Verify alignment with regulatory requirements and internal policies for regulated industries.

## MUST — Guardrails

- **Data residency is non-negotiable.** Understand where data is stored and processed. Vietnamese regulations may require certain data (especially customer PII, financial records) to be stored within Vietnam or within approved jurisdictions. If in doubt, flag it.
- **PII must be classified and protected.** Personally identifiable information requires: access controls, encryption, audit trails, retention policies, and breach notification procedures. Every system handling PII must address all five.
- **Regulatory reporting must survive any change.** Before modifying any system that feeds regulatory reports, verify: What reports depend on this? What's the reporting frequency? Who's accountable? A system change that breaks a regulatory report is a compliance incident.
- **Retain evidence.** Compliance requires proof. Audit trails, approval records, change logs, test results — if you can't prove you did it, regulators assume you didn't.

## SHOULD — Frameworks

### Compliance Assessment Checklist

For any system, process, or change in regulated environment:

1. **Identify applicable regulations** — Which laws, decrees, circulars apply? (Reference `vietnam-insurance-regulatory` or `vietnam-banking-regulatory` skills)
2. **Map requirements to controls** — For each requirement, what control exists or is needed?
3. **Assess current compliance state** — Compliant / Partially compliant / Non-compliant / Not assessed
4. **Gap analysis** — Where are the gaps? What's needed to close them?
5. **Timeline** — Are there regulatory deadlines? Transitional periods?
6. **Approval requirements** — Who needs to sign off? (Compliance officer, regulator, board?)

### Data Handling Requirements

- **Classification**: Public, Internal, Confidential, Restricted. Define per data element.
- **Collection**: Consent requirements, purpose limitation, data minimization
- **Storage**: Encryption, access control, backup, retention period
- **Processing**: Authorized purposes, processing agreements with third parties
- **Transfer**: Cross-border transfer restrictions, data sharing agreements
- **Deletion**: Right to deletion, retention period enforcement, secure destruction

### Audit Trail Requirements

Every regulated action should capture:
- **Who** — Authenticated identity
- **What** — Action performed, data affected
- **When** — Timestamp (NTP-synced)
- **Where** — System, IP, location
- **Why** — Business reason or approval reference
- **Outcome** — Success/failure

## COULD — Open Space

- **Anticipate the next audit.** What questions will auditors ask? Is there evidence ready? Thinking like an auditor reveals gaps that daily operations miss.
- **Compliance as enabler.** Reframe compliance from "constraint" to "trust signal." Strong compliance posture enables partnerships, licenses, and customer trust that non-compliant competitors can't access.
- **Regulatory technology (RegTech).** Are there tools or automation that can reduce compliance burden? Automated reporting, continuous monitoring, policy-as-code.
- **Cross-regulation conflicts.** Sometimes regulations from different bodies conflict (e.g., data retention vs data minimization). Flag these tensions rather than ignoring them.
