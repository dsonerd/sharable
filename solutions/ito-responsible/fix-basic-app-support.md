# Fix: Basic Application Support — Resolving the IT vs Operations L1 Conflict

## The problem

Section 2.4 currently says IT Operation can help with "how to use the system at a basic level, as long as the issue is about system usage, not business interpretation."

This sounds clean on paper. In reality, it creates a **direct conflict** with the Operation Department's L1 business support line, because:

1. **The frontline user doesn't distinguish between "system usage" and "business process."** When a sales agent asks "how do I create a quote?", they mean the full end-to-end act — which involves both clicking buttons (system) and selecting the right product/rider/benefit (business).

2. **The Operation Department L1 already supports frontline users** on how to do their job, which *includes* using the system as part of business processes. If ITO also claims "basic application support," both teams answer overlapping questions, confuse users about who to call, and potentially give conflicting guidance.

3. **"Basic" is undefined.** What's basic to IT (navigate to screen, click submit) is inseparable from what's basic to Operations (choose the right product, fill in the right fields). The boundary moves depending on who you ask.

---

## Three approaches to consider

### Approach A: ITO does NOT do application "how-to" support (Recommended)

**Principle:** ITO handles "is the system working?" — Operations handles "how do I use the system to do my job?"

| ITO owns | Operations L1 owns |
|---|---|
| System is down / slow / erroring | How to create a quote |
| Login / access / MFA issues | Which product to select |
| Screen won't load (technical failure) | How to fill in proposal fields correctly |
| Upload fails with error | Which documents to attach |
| Integration timeout / payment handoff error | How to track case status and follow up |
| Browser/device/printer issues | How to reprint forms (business workflow) |
| Known bug workarounds | Standard operating procedures |

**Why this works:**
- Clean, no overlap. ITO answers "is it broken?" — Operations answers "how do I use it?"
- Matches the real-world structure where Operations L1 already trains and coaches frontline users
- ITO doesn't need deep product knowledge — they focus on infrastructure, access, and break/fix
- No risk of ITO giving wrong business guidance

**The risk:**
- If Operations L1 is understaffed or slow, frontline users will call ITO anyway and ITO will have to say "that's not us" — which frustrates users
- Mitigation: ITO should still be able to **route** the user to Operations L1 with a warm transfer, and the grey-zone protocol applies

**What changes in the capability declaration:**
- Remove Section 2.4 entirely
- Add a line in Section 2.1 (single point of contact): "When a user contacts ITO with a business process or system usage question, ITO records the request and routes it to the Operation Department L1 with context."
- Add "system usage guidance and business process support" to the Operation Department's scope in Section 4

---

### Approach B: ITO does application support ONLY from a runbook (Limited scope)

**Principle:** ITO can answer "how-to" questions, but ONLY if the answer exists in a pre-approved runbook written and maintained by the Operation Department.

| Situation | ITO action |
|---|---|
| User asks "how do I reprint a form?" and there's a runbook entry | ITO follows the runbook and guides the user |
| User asks "how do I reprint a form?" and there's no runbook entry | ITO logs the request and routes to Operations L1 |
| User asks "which rider should I add for this customer?" | ITO routes to Operations L1 (never a runbook topic) |
| User asks "why was my case rejected?" | ITO routes to Operations L1 (business decision) |

**Why this works:**
- ITO can handle some volume of simple how-to calls, reducing load on Operations L1
- The runbook is the boundary — if it's in the runbook, ITO can answer; if not, they route
- Operations controls what's in the runbook, so they control the boundary
- No risk of ITO improvising business answers

**The risk:**
- Runbook maintenance burden. If Operations doesn't keep it updated, ITO gives stale guidance or routes everything anyway
- ITO agents need training on the runbooks — adds training cost
- Still creates partial overlap: user might get different quality answers depending on whether they reach ITO or Operations L1

**What changes in the capability declaration:**
- Rewrite Section 2.4 to: "IT Operation can guide frontline users on standard system procedures when a pre-approved runbook exists. If the question is not covered by a runbook or requires business judgment, ITO routes the request to the Operation Department L1."
- Add a responsibility for Operations: "Maintain and review application runbooks quarterly for ITO consumption"

---

### Approach C: Unified L1 with dual skill tracks (Long-term, structural change)

**Principle:** Merge ITO L1 and Operations L1 into a single frontline support team with agents trained in both technical and basic business workflows.

| Single L1 team handles | Escalation path |
|---|---|
| Login, access, MFA | ITO L2 (IAM / infrastructure) |
| System errors, slow performance | ITO L2 (application / platform) |
| How to create a quote, upload docs | Operations L2 (product / underwriting) |
| Device, browser, printer | ITO L2 (endpoint) |
| Product rules, compliance questions | Operations L2 (business SME) |

**Why this works:**
- From the user's perspective: one team, one number, one experience
- Eliminates the grey zone at L1 entirely
- Higher first-contact resolution because the agent can handle both "the button doesn't work" and "here's how to use the button"

**The risk:**
- Organizational change — requires agreement from both IT and Operations leadership
- Hiring/training cost — L1 agents need broader skills
- Management ambiguity — who manages the unified L1?
- May not be feasible in the short term

**What changes in the capability declaration:**
- This would be a fundamentally different model. The current declaration would become the L2+ scope for ITO, and a new "Unified L1" section would be added.

---

## Comparison summary

| Criteria | A: ITO = break/fix only | B: ITO = runbook only | C: Unified L1 |
|---|---|---|---|
| Clarity of boundary | High | Medium (depends on runbook coverage) | High (no boundary at L1) |
| User experience | Medium (routing adds delay) | Medium-High (resolves more at first call) | High (one team handles all) |
| Implementation effort | Low (remove scope) | Medium (build + maintain runbooks) | High (org restructure) |
| Risk of conflicting answers | None | Low (runbook-controlled) | None |
| Dependency on Operations | Low | High (runbook maintenance) | High (joint ownership) |
| Fits current org structure | Yes | Yes | No (requires change) |

---

## My recommendation

**Start with Approach A** (ITO = break/fix only, Operations = all usage guidance) as the immediate fix for the capability declaration. It's the cleanest boundary and requires no new process to build.

**Plan Approach B** as a 6-month enhancement if ticket volume shows that Operations L1 is overwhelmed by simple how-to questions that could be deflected by runbooks.

**Consider Approach C** as a 12-month strategic option if leadership wants to invest in a unified support experience. This is the best model for the user but the hardest to implement.

---

## Suggested replacement for Section 2.4

> ### 2.4 Application break/fix support
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
