# Cross-Team Issue Handling — IT Operation and Operation Department

## Context

IT Operation owns technical support. The Operation Department owns business support. However, many frontline issues do not fall cleanly into one side. When ownership is unclear, the risk is that the user gets bounced between teams with no resolution.

This document defines the handling protocol for issues that sit between technical and business support.

---

## Grey-zone examples

| User reports | Technical angle | Business angle |
|---|---|---|
| "System rejected my proposal with error code UW-403" | Error code → system issue | UW-403 may mean underwriting rule rejection → business logic |
| "The premium calculation looks wrong" | Could be a calculation bug | Could be correct but user misunderstands product rules |
| "I can't find the rider option in the quote screen" | Screen/UI issue | Rider may not be available for this product/channel → business config |
| "Document upload succeeded but case still shows 'pending documents'" | Integration/workflow bug | Operations may not have released the document requirement list |
| "Customer portal shows different benefits than what I quoted" | Data sync issue | Could be different product version or interpretation |
| "System won't let me backdate this policy" | System validation/block | Backdating may require business exception approval |

These are everyday cases in a life insurance sales system, not edge cases.

---

## No-Bounce Protocol

**Principle:** the team that receives the ticket owns it until the other team explicitly accepts it. No frontline user should ever be told "that's not us" without a warm handoff.

### Rule 1 — First receiver owns the ticket

Whichever team receives the ticket first is responsible for:
- recording the issue
- performing their own initial assessment
- if they believe it belongs to the other team, **transferring the ticket with context** — not redirecting the user

The user never has to re-explain the issue.

### Rule 2 — Transfer, not redirect

| Redirect (wrong) | Transfer (correct) |
|---|---|
| "Please call Operations at ext 500" | IT logs the ticket, adds initial findings, assigns to Operations queue, notifies the user: "I've transferred your case to the Operations team with the details. Your ticket number is X." |
| "That's a business question, not IT" | "I've checked and the system is working correctly for this scenario. I'm transferring this to Operations because it may involve a product rule. They'll contact you." |

### Rule 3 — 15-minute grey-zone triage

For tickets where ownership is ambiguous:

1. The receiving team has **15 minutes** to perform initial assessment
2. If they can resolve it, they resolve it — regardless of which team "owns" the domain
3. If they cannot determine ownership within 15 minutes, they **escalate to the shared triage queue** visible to both IT and Operations leads
4. The IT lead and Operations lead jointly triage the shared queue **twice daily** (morning and afternoon)
5. Tickets in the shared queue must be claimed within **2 hours**

### Rule 4 — Double-rejection escalation

If a ticket is rejected by both teams:
- It auto-escalates to the **IT Operation Manager** and **Operations Manager**
- They jointly decide ownership within **4 hours**
- The decision is logged and becomes a precedent for future similar tickets

### Rule 5 — Build the boundary map from real tickets

After the first 30 days, review all shared-queue tickets and:
- Classify them into patterns
- Assign explicit ownership for each pattern
- Add these to both teams' knowledge bases

This is how the grey zone **shrinks over time** instead of staying ambiguous. The review repeats monthly.

---

## Prerequisites

- A shared triage queue or tag in the ticketing system
- Agreement from both IT and Operations managers to co-triage
- A twice-daily 10-minute sync (can be async in the ticketing system)
- A monthly review to update the boundary map

---

## Summary

> Some frontline issues fall between technical support and business support. For these cases:
>
> 1. The team that receives the ticket first owns it until it is accepted by the other team.
> 2. Transfer is always done as a warm handoff with ticket context — never as a redirect.
> 3. If ownership is unclear after 15 minutes of initial assessment, the ticket moves to a shared triage queue reviewed jointly by IT and Operations leads twice daily.
> 4. If a ticket is rejected by both teams, it escalates to the IT Operation Manager and Operations Manager for a joint decision within 4 hours.
> 5. Grey-zone patterns are reviewed monthly and converted into explicit ownership rules to reduce ambiguity over time.
>
> **No frontline user is ever bounced between teams without a resolution path.**
