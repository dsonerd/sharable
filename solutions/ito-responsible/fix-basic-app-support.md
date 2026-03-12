# Application Support Boundary — IT Operation vs Operation Department L1

## Context

In a life insurance company where the Operation Department already runs a **business support line (L1)** for frontline sales users, there is a natural overlap risk when IT Operation also claims "basic application support."

The frontline user does not distinguish between "system usage" and "business process." When a sales agent asks "how do I create a quote?", they mean the full end-to-end act — which involves both clicking buttons (system) and selecting the right product/rider/benefit (business).

If both teams answer overlapping questions, users get confused about who to call, and the two teams risk giving conflicting guidance.

This document defines three approaches to draw a clean boundary, with a recommendation.

---

## Approach A — ITO handles break/fix only (Recommended)

**Principle:** ITO answers "is the system working?" — Operations answers "how do I use the system to do my job?"

| ITO owns | Operations L1 owns |
|---|---|
| System is down / slow / erroring | How to create a quote |
| Login / access / MFA issues | Which product to select |
| Screen won't load (technical failure) | How to fill in proposal fields correctly |
| Upload fails with error | Which documents to attach |
| Integration timeout / payment handoff error | How to track case status and follow up |
| Browser/device/printer issues | How to reprint forms (business workflow) |
| Known bug workarounds | Standard operating procedures |

**Strengths:**
- Clean boundary with no overlap
- Matches the existing structure where Operations L1 already trains and coaches frontline users
- ITO does not need deep product knowledge — focus stays on infrastructure, access, and break/fix
- No risk of ITO giving wrong business guidance

**Risk:**
- If Operations L1 is understaffed or slow, frontline users will call ITO anyway
- Mitigation: ITO routes the user to Operations L1 with a warm transfer, and the cross-team handling protocol applies

**Impact on the capability declaration:**
- Reframe Section 2.4 as "Application break/fix support" — ITO handles technical failures only
- Add to Section 2.1 (single point of contact): "When a user contacts ITO with a business process or system usage question, ITO records the request and routes it to the Operation Department L1 with context."
- Add "system usage guidance and business process support" to the Operation Department's scope

---

## Approach B — ITO supports application usage only from a runbook

**Principle:** ITO can answer "how-to" questions, but only if the answer exists in a **pre-approved runbook** written and maintained by the Operation Department.

| Situation | ITO action |
|---|---|
| User asks "how do I reprint a form?" and there is a runbook entry | ITO follows the runbook and guides the user |
| User asks "how do I reprint a form?" and there is no runbook entry | ITO logs the request and routes to Operations L1 |
| User asks "which rider should I add for this customer?" | ITO routes to Operations L1 (never a runbook topic) |
| User asks "why was my case rejected?" | ITO routes to Operations L1 (business decision) |

**Strengths:**
- ITO can handle some volume of simple how-to calls, reducing load on Operations L1
- The runbook is the boundary — if it is in the runbook, ITO can answer; if not, they route
- Operations controls what is in the runbook, so they control the boundary
- No risk of ITO improvising business answers

**Risk:**
- Runbook maintenance burden — if Operations does not keep it updated, ITO gives stale guidance or routes everything
- ITO agents need training on the runbooks — adds training cost
- Partial overlap remains: user may get different quality answers depending on whether they reach ITO or Operations L1

**Impact on the capability declaration:**
- Rewrite Section 2.4 to: "IT Operation can guide frontline users on standard system procedures when a pre-approved runbook exists. If the question is not covered by a runbook or requires business judgment, ITO routes the request to the Operation Department L1."
- Add a responsibility for Operations: "Maintain and review application runbooks quarterly for ITO consumption"

---

## Approach C — Unified L1 with dual skill tracks (structural change)

**Principle:** Merge ITO L1 and Operations L1 into a single frontline support team with agents trained in both technical and basic business workflows.

| Single L1 team handles | Escalation path |
|---|---|
| Login, access, MFA | ITO L2 (IAM / infrastructure) |
| System errors, slow performance | ITO L2 (application / platform) |
| How to create a quote, upload docs | Operations L2 (product / underwriting) |
| Device, browser, printer | ITO L2 (endpoint) |
| Product rules, compliance questions | Operations L2 (business SME) |

**Strengths:**
- From the user's perspective: one team, one number, one experience
- Eliminates the grey zone at L1 entirely
- Higher first-contact resolution because the agent can handle both "the button doesn't work" and "here's how to use the button"

**Risk:**
- Organizational change — requires agreement from both IT and Operations leadership
- Hiring/training cost — L1 agents need broader skills
- Management ambiguity — who manages the unified L1?
- May not be feasible in the short term

**Impact on the capability declaration:**
- This would be a fundamentally different model — the current declaration becomes the L2+ scope for ITO, and a new "Unified L1" section is added

---

## Comparison

| Criteria | A: Break/fix only | B: Runbook only | C: Unified L1 |
|---|---|---|---|
| Clarity of boundary | High | Medium (depends on runbook coverage) | High (no boundary at L1) |
| User experience | Medium (routing adds delay) | Medium-High (resolves more at first call) | High (one team handles all) |
| Implementation effort | Low (remove scope) | Medium (build + maintain runbooks) | High (org restructure) |
| Risk of conflicting answers | None | Low (runbook-controlled) | None |
| Dependency on Operations | Low | High (runbook maintenance) | High (joint ownership) |
| Fits current org structure | Yes | Yes | No (requires change) |

---

## Recommendation

**Immediate (now):** Adopt **Approach A**. ITO handles application break/fix only. Operations L1 handles all usage guidance. This is the cleanest boundary and requires no new process.

**6-month review:** If ticket volume shows that Operations L1 is overwhelmed by simple how-to questions, evaluate **Approach B** — introduce runbooks for the highest-volume topics to let ITO deflect some of that load.

**12-month strategic option:** If leadership wants to invest in a unified frontline support experience, evaluate **Approach C** as a structural initiative.

---

## Proposed capability statement (Approach A)

> ### Application break/fix support
>
> IT Operation handles **technical failures** in the sales application — situations where the system is not working as designed.
>
> Examples:
> - screen returns an error or does not load
> - submission fails with a system error
> - document upload fails technically
> - integration timeout or data sync failure
> - print function produces corrupted output
> - system performance is degraded
>
> IT Operation does **not** provide guidance on how to use the system for business tasks (e.g., how to create a quote, which product to select, how to fill in proposal fields). Those questions are handled by the **Operation Department L1 business support line**, which owns frontline user training and business process guidance.
>
> When a user contacts IT Operation with a business usage question, IT Operation records the request and routes it to the Operation Department L1 with context.
