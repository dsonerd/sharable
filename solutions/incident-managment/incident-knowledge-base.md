# Incident Knowledge Base

> Known incident scenarios built from real incidents and RCAs. Used by L1/L2 during triage to match symptoms to known patterns.
>
> **How to use**: When triaging, search this page for matching symptoms. If a match is found:
> 1. **Assign priority (P)** from the KB entry — no need for a preliminary P
> 2. **Execute the documented first response** immediately
> 3. **Notify the tech team** (inform, don't wait) — they can re-evaluate P in their session if investigation reveals something different
>
> If no match is found, follow the standard triage path (see [incident-triage-guideline.md](incident-triage-guideline.md)).
>
> **How to grow**: After every RCA, add one entry. This is not a separate task — it's part of closing the incident.

---

## Infrastructure Incidents

| ID | Symptom | Likely Cause | Type | Priority | First Response | Added From |
|----|---------|-------------|------|----------|---------------|------------|
| I-001 | _Example: HTTP 503 on all endpoints after deployment_ | _Bad deployment / config push_ | Infra | P1 | _Rollback deployment immediately_ | _RCA-xxx_ |
| I-002 | | | Infra | | | |
| I-003 | | | Infra | | | |

---

## Application Incidents

| ID | Symptom | Likely Cause | Type | Priority | First Response | Added From |
|----|---------|-------------|------|----------|---------------|------------|
| A-001 | _Example: Premium amounts 15% higher than expected in batch output_ | _Formula bug in calculation engine_ | App | P1 | _Stop batch, notify finance, escalate to claims dev_ | _RCA-xxx_ |
| A-002 | | | App | | | |
| A-003 | | | App | | | |

---

## Detection Signatures

Alert-to-incident mapping. When a specific alert fires, L1 knows what it means without investigating.

| Alert / Signal | What It Means | Type | Priority | Contact |
|---------------|--------------|------|----------|---------|
| _Example: CloudWatch alarm "PolicyDB-ConnectionsExhausted"_ | _DB connection pool full — likely connection leak in app_ | App | P2 | _Backend dev team_ |
| | | | | |
| | | | | |

---

## How to Add an Entry

After every RCA, add one row:

1. **Symptom**: What L1 would see (alert name, user report, dashboard signal)
2. **Likely Cause**: What the investigation found
3. **Type**: Infra or App
4. **Priority**: What priority this should get next time
5. **First Response**: The first action L1/L2 should take
6. **Added From**: Link to the RCA that produced this knowledge

Keep entries short — one line each. If a scenario needs a full runbook, create one and link to it.
