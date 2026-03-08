# Skill: Insurance Domain Model

Core business concepts, processes, and terminology for life insurance operations.

## MUST — Guardrails

- **Use correct insurance terminology.** Don't use casual substitutes that create ambiguity. "Policyholder" ≠ "insured" ≠ "beneficiary" — these are distinct roles.
- **Respect the product lifecycle.** Insurance products move through defined stages: design → pricing → filing/approval → distribution → issuance → servicing → claims → closure. Don't skip stages in analysis.
- **Acknowledge actuarial complexity.** If a topic involves pricing, reserving, or risk modeling, flag that actuarial expertise is required. Don't oversimplify actuarial concepts.

## SHOULD — Frameworks

### Core Domain Concepts

**Product structure:**
- Life insurance categories: term, whole life, endowment, universal life, unit-linked (investment-linked), riders
- Product components: base plan + riders, sum assured, premium, policy term, benefits, exclusions
- Pricing elements: mortality tables, interest rates, expense loading, profit margin

**Key processes:**
- **New business**: Quotation → Application → Underwriting → Policy issuance → First premium collection
- **Underwriting**: Risk assessment → Medical requirements → Financial underwriting → Decision (standard/rated/declined/deferred)
- **Policy servicing**: Premium collection → Policy changes (endorsements) → Loans → Surrenders → Renewals → Lapses → Reinstatements
- **Claims**: Notification → Documentation → Investigation → Assessment → Decision → Payment
- **Reinsurance**: Treaty vs facultative, proportional vs non-proportional, retention limits

**Key entities:**
- Policy, Policyholder, Insured, Beneficiary, Agent/Advisor
- Premium, Sum Assured, Cash Value, Policy Loan
- Claim, Benefit, Exclusion, Waiting Period
- Commission, Persistency, Lapse Rate

**Key metrics:**
- APE (Annual Premium Equivalent), NBV (New Business Value), VNB (Value of New Business)
- Persistency rates (13th month, 25th month)
- Claims ratio, expense ratio, combined ratio
- Embedded value, solvency margin

### System Landscape (typical)

- **Core policy admin system** — Master record of all policies and transactions
- **Underwriting system** — Rules engine + workflow for risk assessment
- **Claims management system** — Claims lifecycle tracking
- **Billing/collection system** — Premium collection, receipting, allocation
- **Agency management system** — Agent licensing, hierarchy, commissions
- **CRM** — Customer interactions, leads, service requests
- **Data warehouse / BI** — Regulatory reporting, management reporting, analytics
- **Digital channels** — Customer portal, mobile app, agent portal

## COULD — Open Space

- **Challenge the legacy process.** Life insurance processes were designed for paper and face-to-face. Which steps are genuinely necessary vs carried over from a pre-digital era?
- **Cross-industry patterns.** Insurance underwriting is a classification problem. Claims is a workflow/state-machine problem. Policy servicing is an event-sourcing problem. What can be borrowed from other domains?
- **Customer journey lens.** The internal process view (new business, underwriting, servicing, claims) is not how customers experience insurance. What does the customer journey actually look like, and where are the pain points?
- **Data as a product.** Insurance generates rich longitudinal data. Beyond reporting obligations, what value could this data unlock?
