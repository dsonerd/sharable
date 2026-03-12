# SLA Response and Resolution Targets — IT Operation First-Line Support

## Scope

This document defines the service level targets for IT Operation's first-line support of the frontline sales system. These targets cover what ITO commits to from ticket receipt to either resolution or qualified escalation.

---

## Definitions

| Term | Meaning |
|---|---|
| **Response time** | Time from ticket creation to first meaningful human contact with the user (not an auto-acknowledgment) |
| **Escalation time** | Time from ticket creation to qualified handoff to L2/resolver group (with evidence, diagnosis, and context) |
| **Resolution time** | Time from ticket creation to confirmed resolution (service restored or request fulfilled) |
| **Business hours** | The agreed operating hours for ITO support (e.g., Mon–Fri 08:00–18:00, or as defined) |

---

## Incident SLA targets

| Priority | Response | Escalation (if L1 cannot resolve) | L1 Resolution target | Measurement |
|---|---|---|---|---|
| **P1 — Critical** | **15 minutes** | **30 minutes** | **4 hours** (restore or workaround) | Clock time (24/7 if on-call exists, otherwise business hours) |
| **P2 — High** | **30 minutes** | **1 hour** | **8 business hours** | Business hours |
| **P3 — Medium** | **2 business hours** | **4 business hours** | **2 business days** | Business hours |
| **P4 — Low** | **4 business hours** | **1 business day** | **5 business days** | Business hours |

### Rationale

- **P1 at 15 min response**: When the sales floor is down, every minute counts. 15 minutes is aggressive but achievable with proper monitoring and staffing. This is about acknowledging the issue, not solving it.
- **P1 escalation at 30 min**: If L1 cannot diagnose a critical outage in 30 minutes, it is almost certainly not an L1 issue. Fast escalation with good notes is more valuable than slow L1 troubleshooting.
- **P1 resolution at 4 hours**: This includes workarounds. Full root cause fix may take longer, but sales must be unblocked within 4 hours.
- **P2–P4**: Standard targets for mid-size IT operations, aligned with common ITSM benchmarks.

---

## Service request fulfillment targets

Service requests are repeatable and predictable, so they carry separate fulfillment targets:

| Request type | Fulfillment target |
|---|---|
| Password reset / account unlock | **1 business hour** |
| MFA issue | **2 business hours** |
| New user access (with approved request) | **1 business day** |
| Role/profile change | **1 business day** |
| Device setup / replacement | **3 business days** |
| Software installation | **2 business days** |
| Standard report access | **2 business days** |

---

## SLA boundary conditions

### Resolution SLA applies to what ITO controls

If ITO escalates to L2 Application Support or a vendor, the **L1 resolution clock pauses**. ITO's SLA covers:
- response
- initial diagnosis
- escalation quality
- user communication

End-to-end resolution depends on resolver groups. ITO tracks and reports total resolution time, but does not solely control it.

### SLA for cross-team tickets

For tickets that transfer between IT Operation and the Operation Department:
- The **response SLA** still applies to the first-receiving team
- The **15-minute triage rule** from the cross-team handling protocol applies
- Transfer to the other team resets the resolution clock for the receiving team, but total elapsed time is still tracked

---

## Summary

| Priority | Response | Escalation | L1 Resolution / Workaround |
|---|---|---|---|
| P1 | 15 min | 30 min | 4 hours |
| P2 | 30 min | 1 hour | 8 business hours |
| P3 | 2 business hours | 4 business hours | 2 business days |
| P4 | 4 business hours | 1 business day | 5 business days |

These targets cover ITO's first-line scope. End-to-end resolution for escalated issues depends on resolver group performance, which ITO tracks and reports but does not solely control.
