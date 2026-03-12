# Fix: Grey Zone Between IT Operation and Operation Department

## The problem

The current capability declaration draws a clean line:
- **IT Operation** → technical support
- **Operation Department** → business decisions

In practice, many frontline issues sit in the middle. The user calls IT, IT says "that's business," Operations says "that's a system issue," and the user gets bounced. This is the single biggest source of frustration in dual-support models.

### Real grey-zone examples

| User reports | Looks like IT | Looks like Operations |
|---|---|---|
| "I submitted a proposal but the system rejected it with error code UW-403" | Error code → system issue | UW-403 might mean underwriting rule rejection → business logic |
| "The premium calculation looks wrong" | Could be a calculation bug | Could be correct but user misunderstands product rules |
| "I can't find the rider option in the quote screen" | Screen/UI issue | Rider may not be available for this product/channel → business config |
| "Document upload succeeded but case still shows 'pending documents'" | Integration/workflow bug | Operations may not have released the document requirement list |
| "Customer portal shows different benefits than what I quoted" | Data sync issue | Could be different product version or interpretation |
| "System won't let me backdate this policy" | System validation/block | Backdating may require business exception approval |

These are not edge cases. They are **everyday cases** in a life insurance sales system.

---

## Proposed approach: No-Bounce Protocol

The principle is simple: **the team that receives the ticket owns it until it is accepted by the other team.** No user should ever be told "that's not us" without a warm handoff.

### Rule 1 — First receiver owns the ticket

Whichever team (IT or Operations) receives the ticket first is responsible for:
- recording the issue
- performing their own initial assessment
- if they believe it belongs to the other team, they **transfer the ticket with context**, not redirect the user

The user never has to re-explain the issue.

### Rule 2 — Transfer, not redirect

| Bad (redirect) | Good (transfer) |
|---|---|
| "Please call Operations at ext 500" | IT logs the ticket, adds initial findings, assigns to Operations queue, notifies the user: "I've transferred your case to the Operations team with the details. Your ticket number is X." |
| "That's a business question, not IT" | "I've checked and the system is working correctly for this scenario. I'm transferring this to Operations because it may involve a product rule. They'll contact you." |

### Rule 3 — 15-minute grey-zone triage

For tickets that are ambiguous:

1. The receiving team has **15 minutes** to perform initial assessment
2. If they can resolve it, they resolve it — regardless of which team "owns" the domain
3. If they cannot determine ownership within 15 minutes, they **escalate to the Grey Zone queue** (a shared queue visible to both IT and Operations leads)
4. The IT lead and Operations lead jointly triage the Grey Zone queue **twice daily** (morning and afternoon)
5. Tickets in the Grey Zone queue must be claimed within **2 hours**

### Rule 4 — If both teams reject, it escalates up

If a ticket bounces between IT and Operations more than once:
- It auto-escalates to the **IT Operation Manager** and **Operations Manager**
- They jointly decide ownership within **4 hours**
- The decision is logged and becomes a precedent for future similar tickets

### Rule 5 — Build the boundary map from real tickets

After 30 days, review all Grey Zone tickets and:
- Classify them into patterns
- Update the responsibility declaration with explicit ownership for each pattern
- Add these to both teams' knowledge bases

This is how the grey zone **shrinks over time** instead of staying ambiguous.

---

## Suggested text to add to the capability declaration

Add as a new section **2.4A** (between current 2.4 and 2.5), or as a standalone section after Section 3:

> ### Grey-zone issue handling
>
> Some frontline issues fall between technical support and business support. For these cases:
>
> 1. The team that receives the ticket first owns it until it is accepted by the other team.
> 2. Transfer is always done as a warm handoff with ticket context — never as a redirect.
> 3. If ownership is unclear after 15 minutes of initial assessment, the ticket moves to a shared triage queue reviewed jointly by IT and Operations leads twice daily.
> 4. If a ticket is rejected by both teams, it escalates to the IT Operation Manager and Operations Manager for a joint decision within 4 hours.
> 5. Grey-zone patterns are reviewed monthly and converted into explicit ownership rules to reduce ambiguity over time.
>
> The goal is: **no frontline user is ever bounced between teams without a resolution path.**

---

## What this requires

- A shared "Grey Zone" queue or tag in the ticketing system
- Agreement from both IT and Operations managers to co-triage
- A twice-daily 10-minute sync (can be async in the ticketing system)
- A monthly review to update the boundary map
