# Fix: SLA Response and Resolution Targets

## The problem

The current Section 7 defines P1–P4 priorities with good examples but **no time commitments**. A priority without an SLA is just a label — it doesn't drive behavior or accountability.

For a life insurance sales system, the stakes are concrete: if agents can't submit proposals, policies don't get issued, and revenue stops.

---

## Proposed SLA model

This is scoped to **IT Operation's first-line responsibility** — what ITO commits to from ticket receipt to either resolution or qualified escalation.

### Definitions

| Term | Meaning |
|---|---|
| **Response time** | Time from ticket creation to first meaningful human contact with the user (not an auto-acknowledgment) |
| **Escalation time** | Time from ticket creation to qualified handoff to L2/resolver group (with evidence, diagnosis, and context) |
| **Resolution time** | Time from ticket creation to confirmed resolution (service restored or request fulfilled) |
| **Business hours** | The agreed operating hours for ITO support (e.g., Mon–Fri 08:00–18:00, or as defined) |

### Proposed targets

| Priority | Response | Escalation (if L1 cannot resolve) | L1 Resolution target | Measurement |
|---|---|---|---|---|
| **P1 — Critical** | **15 minutes** | **30 minutes** | **4 hours** (restore or workaround) | Clock time (24/7 if on-call exists, otherwise business hours) |
| **P2 — High** | **30 minutes** | **1 hour** | **8 business hours** | Business hours |
| **P3 — Medium** | **2 business hours** | **4 business hours** | **2 business days** | Business hours |
| **P4 — Low** | **4 business hours** | **1 business day** | **5 business days** | Business hours |

### Why these numbers

- **P1 at 15 min response**: When sales floor is down, every minute counts. 15 minutes is aggressive but achievable if ITO has proper monitoring and staffing. This is about *acknowledging* the issue, not solving it.
- **P1 escalation at 30 min**: If L1 can't diagnose a critical outage in 30 minutes, it's almost certainly not an L1 issue. Fast escalation with good notes is more valuable than slow L1 troubleshooting.
- **P1 resolution at 4 hours**: This includes workarounds. Full root cause fix may take longer, but sales must be unblocked within 4 hours.
- **P2–P4 are standard** for mid-size IT operations and align with common ITSM benchmarks.

---

## Important caveats to state in the capability declaration

### 1. Resolution SLA applies to what ITO controls

If ITO escalates to L2 Application Support or a vendor, the **L1 resolution clock pauses**. ITO's SLA covers:
- response
- initial diagnosis
- escalation quality
- user communication

The end-to-end resolution depends on resolver groups. ITO should track and report total resolution time, but cannot commit to it alone.

### 2. SLA for grey-zone tickets

For tickets that need to transfer between IT and Operations:
- The **response SLA** still applies to the first-receiving team
- The **15-minute triage rule** from the grey-zone protocol applies
- Transfer to the other team resets the *resolution* clock for the receiving team but the *total elapsed time* is still tracked

### 3. SLA for service requests vs. incidents

Service requests (access, device setup, role change) should have separate fulfillment targets:

| Request type | Fulfillment target |
|---|---|
| Password reset / account unlock | **1 business hour** |
| MFA issue | **2 business hours** |
| New user access (with approved request) | **1 business day** |
| Role/profile change | **1 business day** |
| Device setup / replacement | **3 business days** |
| Software installation | **2 business days** |
| Standard report access | **2 business days** |

These are simpler to commit to because they are repeatable and predictable.

---

## Suggested text to replace current Section 7

> ### 7) Priority and SLA guidance
>
> #### Priority definitions
>
> | Priority | Impact | Examples |
> |---|---|---|
> | **P1 — Critical** | Sales cannot sell at all, or many users/branches are blocked | Full login outage, system-wide submission failure, major integration outage |
> | **P2 — High** | Important function broken for one team/branch or high-value case blocked | Quote failure in one region, printing unavailable for many users |
> | **P3 — Medium** | Single-user or limited issue, workaround available | One user cannot upload, printer setup issue |
> | **P4 — Low** | Routine request or cosmetic issue | Access request, minor display issue, standard config |
>
> #### ITO first-line SLA targets
>
> | Priority | Response | Escalation | L1 Resolution / Workaround |
> |---|---|---|---|
> | P1 | 15 min | 30 min | 4 hours |
> | P2 | 30 min | 1 hour | 8 business hours |
> | P3 | 2 business hours | 4 business hours | 2 business days |
> | P4 | 4 business hours | 1 business day | 5 business days |
>
> #### Service request fulfillment targets
>
> | Request | Target |
> |---|---|
> | Password reset / account unlock | 1 business hour |
> | MFA issue | 2 business hours |
> | New user access | 1 business day |
> | Role/profile change | 1 business day |
> | Device setup / replacement | 3 business days |
> | Software installation | 2 business days |
>
> **Note:** These targets cover ITO's first-line scope. End-to-end resolution for escalated issues depends on resolver group performance, which ITO tracks and reports but does not solely control.
