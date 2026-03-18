# Incident Triage Scenarios

> Worked examples showing how real-world reports flow through the triage process.
> Each scenario walks through L1's decision path step by step.
>
> Related: [`classification.md`](classification.md) · [`incident-knowledge-base.md`](incident-knowledge-base.md)

---

## Scenario 1: Customer Cannot Log In to Portal

### The Report

> "A customer called — they can't log in to the portal. They need to submit a claim today."

### L1 Triage Walkthrough

**Step 1 — Is this an incident?**

Don't answer yet. A customer portal login failure sounds urgent, but L1 must verify scope first.

**Step 2 — Quick verification (before classifying)**

| Check | How | Why |
|-------|-----|-----|
| Can L1 reproduce the failure? | Try logging in as a test user | If L1 can't log in either → wider problem |
| Is the customer's account the issue? | Check account status, lockout, expiry | Account-specific = service request |
| Are other customers also affected? | Check recent tickets, ask call center | One report could be the tip of the iceberg |
| Did a deployment happen recently? | Check release log / change calendar | Post-deployment failure = likely incident |
| Any auth-related alerts firing? | Check monitoring dashboard | Auth errors spiking = confirmed incident |

**Step 3 — Route based on findings**

| Finding | Classification | Route |
|---------|---------------|-------|
| Customer forgot password / account locked | **Service Request** | Help desk resets password, no incident |
| Customer's account is fine, but login fails for them only | **Investigate further** — could be browser, network, or early sign of wider issue | Check 2 more customers before closing |
| L1 can't log in either / multiple customers affected | **Incident** | Continue to step 4 |
| Auth errors spiking in monitoring | **Incident** | Continue to step 4 |

**Step 4 — Classify the incident**

*Is infrastructure healthy?*

| What's broken | Type | P | Reasoning |
|---------------|------|---|-----------|
| Portal server / load balancer down | Infra Incident | P1 | All customers blocked from transacting |
| Auth / SSO service unreachable | Infra Incident | P1 | Authentication infrastructure failed |
| DB connections exhausted on auth DB | Infra Incident | P1-P2 | Infra-level resource exhaustion |
| Login succeeds but app redirects to error page | App Incident | P1-P2 | App logic broken post-auth |
| New logins fail but existing sessions work (after release) | App Incident | P2 | Deployment broke auth flow |
| One customer type can't log in (e.g., corporate accounts) | App Incident | P2-P3 | Partial scope — check blast radius with tech team |

**Step 5 — Check Knowledge Base**

If the KB has a matching entry (e.g., "Login fails after deployment → rollback auth service"), L1 assigns P from KB and executes the documented response immediately.

If no KB match, follow standard path — escalate infra incidents immediately, collaborate with tech team for app incidents within 30 min.

### Why This Scenario Matters

A customer portal is a **revenue channel**. Unlike internal user login issues, a customer login failure directly blocks business transactions. L1 should default to investigating rather than dismissing as a service request — especially if the customer says their credentials are correct.

The trap: treating every "I can't log in" as a password reset. One customer reporting is often the first signal that many are affected but haven't called yet.

---

## Scenario 2: Nightly Batch Completes but Output Is Wrong

### The Report

> "Finance team says this morning's premium report has numbers that don't match. The batch ran fine — no errors — but the totals are off by about 12%."

### L1 Triage Walkthrough

**Step 1 — Is this an incident?**

Yes. Financial data is potentially incorrect in production. This is not a feature request or a UAT bug — it's affecting real output that business relies on.

**Step 2 — Classify**

*Is infrastructure healthy?*

The batch ran successfully. No errors in logs. Scheduler worked. DB is up. Servers are fine. → **Infrastructure is healthy.**

This is an **Application Incident** — the most dangerous kind. The system did exactly what it was told to do, but the output is wrong. No alerts fired. No errors logged. It was detected by **people**, not monitoring.

**Step 3 — Check Knowledge Base**

Search KB for: "batch output wrong", "premium mismatch", "calculation error".

| KB Result | Action |
|-----------|--------|
| **Match found** (e.g., "Premium batch 12% off → formula coefficient was changed in last config update") | Assign P from KB. Execute response: stop downstream processing, notify finance, check config change log. Notify tech team. |
| **No match** | Assign preliminary P. This is new territory — collaborate with tech team immediately. |

**Step 4 — Assign priority**

This is P1 or P2 regardless of path:
- Financial data may be incorrect → **P1 trigger** (per decision questions)
- How many policies are affected? If the whole batch → P1
- If only one product line → P2 (but still urgent)

**Step 5 — Collaborate with tech team (within 30 min)**

L1 cannot assess this alone. Questions for tech team:

| Question | Why It Matters |
|----------|---------------|
| How many policies / customers are affected? | Determines blast radius |
| Was there a config change or deployment recently? | Most common root cause |
| Has the downstream data (statements, payments) already been sent? | If yes → P1 escalation, customer impact is real |
| Is this a calculation error or a reporting/display error? | Calculation error = data is wrong. Display error = data is fine, report is wrong (lower severity) |

### Why This Scenario Matters

This is the **silent killer** in IT operations. Infrastructure monitoring is green. Application logs show no errors. The batch "succeeded." But the output is wrong, and if nobody catches it, wrong premiums go to customers, wrong numbers go to regulators, and wrong payments go to banks.

These incidents are always detected late — by finance during reconciliation, by customers who notice their premium changed, or by auditors. The longer it takes to detect, the bigger the blast radius.

**L1 lesson**: "Batch completed successfully" does not mean "batch produced correct output."

---

## Scenario 3: System Slow During Business Hours

### The Report

> "Agents are complaining the core system is very slow since 10 AM. Pages take 20-30 seconds to load. They can't serve customers at the counter."

### L1 Triage Walkthrough

**Step 1 — Is this an incident?**

Yes. Service is degraded. Multiple users are affected during business hours. Agents can't serve customers → revenue and customer experience impact.

**Step 2 — Classify**

*Is infrastructure healthy?* — This is the **ambiguous case**. Slowness can be infra or app.

| Check | Finding | Points to |
|-------|---------|-----------|
| CPU / memory on app servers | CPU at 95% | Could be infra (undersized) or app (memory leak, runaway query) |
| Database response time | DB queries taking 10x longer than normal | Infra if DB server is overloaded; App if a bad query was deployed |
| Network latency | Normal | Rules out network |
| Recent deployment? | Yes, release went out at 9:45 AM | Strong signal → likely App Incident |
| Is only one function slow, or everything? | Everything | If everything → likely infra. If one function → likely app |

**The decision**: If a deployment happened 15 minutes before slowness started, this is almost certainly an **Application Incident** (new code introduced a performance regression). If no deployment and infra metrics show resource exhaustion with no code change, it's an **Infrastructure Incident**.

**Step 3 — Check Knowledge Base**

Search KB for: "slow after deployment", "high CPU", "page load timeout".

If KB has: "System slow after release → check for N+1 query regression, rollback if confirmed" → assign P from KB, execute rollback, notify tech team.

**Step 4 — Assign priority**

- Many users affected + business hours → **P2** minimum
- Agents can't serve customers at the counter → this is effectively an outage for walk-in customers → could be **P1**
- If it's degraded but agents can still work (slowly) → **P2**

**Step 5 — Response**

| If Infra Incident | If App Incident |
|-------------------|-----------------|
| Scale up / restart servers | Rollback the deployment |
| Check DB connection pool, restart if needed | Identify the slow query / code path |
| Check if a scheduled job is consuming resources | Fix, test, redeploy |
| Failover to standby if available | Monitor after rollback |

### Why This Scenario Matters

Slowness is the most common **misclassified** incident type. L1 often defaults to "it's an infra problem" because slowness feels like a server issue. But in most organizations, the majority of performance incidents are caused by **application changes** — a bad query, a missing index that only matters at scale, or a memory leak introduced in the latest release.

**L1 lesson**: Always check the change calendar. If a release happened in the last 2 hours, assume app incident until proven otherwise.

---

## Scenario 4: Third-Party Payment Gateway Not Responding

### The Report

> "Online payments are failing. Customers are getting 'Payment could not be processed' errors. This started about 20 minutes ago."

### L1 Triage Walkthrough

**Step 1 — Is this an incident?**

Yes. A core business function (collecting payments) is broken. Customers are unable to complete transactions.

**Step 2 — Classify**

*Is infrastructure healthy?* — Our infra is fine. The problem is the third-party payment gateway. But from the customer's perspective, **our service is broken**.

This is an **Infrastructure Incident** — even though the failure is external. The dependency is part of our service delivery. We own the customer experience, not the vendor.

**Step 3 — Verify and scope**

| Check | How | Why |
|-------|-----|-----|
| Is it the gateway or our integration? | Check gateway status page / call vendor support | Determines who can fix it |
| Are ALL payment methods affected? | Test credit card, bank transfer, etc. | Maybe only one channel is down |
| Is our integration code throwing errors? | Check app logs for timeout / connection refused | If our code changed recently → could be us |
| Did the vendor notify us of maintenance? | Check vendor communications / email | Planned maintenance we missed = our oversight |

**Step 4 — Check Knowledge Base**

Search KB for: "payment gateway timeout", "payment failed", vendor name.

If KB has: "Gateway X returns 503 → check vendor status page, enable retry queue, switch to fallback gateway if available" → assign P from KB, execute immediately.

**Step 5 — Assign priority**

- All online payments failing → **P1** (revenue directly impacted)
- Only one payment method failing, others work → **P2** (degraded, workaround exists)
- Intermittent failures (10% of transactions) → **P2**

**Step 6 — Response**

| Action | Who | When |
|--------|-----|------|
| Contact vendor support, open a ticket | L1 | Immediately |
| Activate fallback payment gateway (if available) | Infra / DevOps | Within 15 min |
| Enable payment retry queue (if designed) | Dev team | Within 15 min |
| Notify business: "online payments are degraded" | IC | Within 15 min |
| Communicate to customers (portal banner / SMS) | Comms | Within 30 min |
| Monitor vendor status page for updates | L1 | Ongoing |

### Why This Scenario Matters

Third-party failures are **the incidents L1 feels most helpless about** — we can't fix the vendor's system. But that doesn't mean we can't respond:

1. **Detect fast** — don't wait for customers to call. Monitor the integration.
2. **Have a fallback** — if the payment gateway is critical, architect for failover.
3. **Communicate proactively** — customers are more forgiving when they know you know.
4. **Track vendor SLA** — if this happens repeatedly, it's a vendor management problem.

**L1 lesson**: "It's the vendor's fault" is not a valid reason to do nothing. We own the service, we own the response.

---

## Scenario 5: Business Discovers Data Discrepancy During Month-End

### The Report

> "Finance flagged during month-end close: 347 policies show a surrender value of zero, but these are active policies with 5+ years of premium payments. This data is being used for the regulatory report due in 3 days."

### L1 Triage Walkthrough

**Step 1 — Is this an incident?**

Yes — and this is **high priority** even though nothing is "down." Financial data is incorrect in production, and it's heading to a regulatory report.

**Step 2 — Classify**

*Is infrastructure healthy?*

Servers are up. DB is running. No errors in logs. The data is simply **wrong**. → **Application Incident.**

But L1 must flag this immediately — this isn't a normal application incident. Financial data + regulatory reporting = P1 triggers.

**Step 3 — Check Knowledge Base**

Search KB for: "surrender value zero", "policy value incorrect", "data corruption", "month-end discrepancy".

If KB has a match from a previous RCA → assign P from KB, execute response (e.g., "Run recalculation batch for affected policies, hold regulatory report").

**Step 4 — Assign priority**

Two P1 triggers hit simultaneously:
- **Financial data may be incorrect** → P1
- **Regulatory deadline at risk** → P1 (even if not in the standard decision questions, L1 should escalate regulatory risk)

This is **P1** — not because the system is down, but because the data is wrong and the blast radius includes the regulator.

**Step 5 — Collaborate with tech team (within 30 min)**

This needs immediate cross-functional investigation:

| Question | Who Answers | Why |
|----------|------------|-----|
| When did the data go wrong? Since when are surrender values zero? | DBA / Dev | Determines blast radius — is it 347 policies or more? |
| Was there a calculation batch change recently? | Dev | Most likely root cause |
| Was there a data migration or DB maintenance? | DBA / Infra | Data-level root cause |
| Are other calculated values also wrong (e.g., cash value, maturity value)? | BA / Actuary | If surrender value is wrong, other values from the same formula might also be wrong |
| Can we regenerate the correct values? | Dev / Actuary | Determines fix path — recalculate vs restore from backup |
| Can we delay the regulatory report? | Compliance / Management | Buys time if fix is complex |

**Step 6 — Response path**

```
Immediate (< 1 hour):
├── Hold the regulatory report — do NOT submit with wrong data
├── Identify the root cause (when + why did values become zero)
├── Scope the blast radius (is it 347 policies or more?)
└── Notify management + compliance

Short-term (< 24 hours):
├── Fix root cause (code fix, config fix, or data repair)
├── Recalculate correct surrender values for all affected policies
├── QA validates recalculated values against expected figures
└── Update regulatory report with corrected data

Post-incident:
├── RCA — how did wrong data exist for days/weeks without detection?
├── Add monitoring: alert if calculated values are zero for active policies
└── Add KB entry for future reference
```

### Why This Scenario Matters

This is the scenario that **keeps CTOs up at night**. Nothing was "down." No alerts fired. No customers called. The system produced wrong data silently, and it was only caught because a finance analyst noticed during month-end reconciliation.

Key lessons:

1. **Monitoring is not enough.** You can have 100% uptime and still have a P1 incident. Business validation checks (reconciliation, spot checks, reasonableness tests) are your last line of defense.
2. **"No errors in logs" ≠ "everything is correct."** The most dangerous bugs don't throw errors — they produce wrong output confidently.
3. **Regulatory deadlines change the priority calculus.** A data error that would normally be P2 becomes P1 when a regulatory submission is at stake.
4. **The blast radius is rarely what it first appears.** 347 policies with zero surrender value might mean thousands more with slightly-off values that haven't been noticed yet.

**L1 lesson**: When finance or compliance reports a data discrepancy, treat it as urgent until proven otherwise. The blast radius almost always turns out to be larger than the initial report suggests.

---

## Summary — Scenario Comparison

| # | Report | Incident? | Type | P | Key Trap |
|---|--------|-----------|------|---|----------|
| 1 | Customer can't log in | Depends on scope | Infra or App | P1-P3 | Dismissing as "password reset" when it's a wider outage |
| 2 | Batch output is wrong | Yes | App Incident | P1-P2 | "Batch completed successfully" ≠ correct output |
| 3 | System slow during hours | Yes | Infra or App | P1-P2 | Assuming "slow = infra" when it's usually a code change |
| 4 | Payment gateway failing | Yes | Infra Incident | P1-P2 | "Vendor's fault" is not a reason to do nothing |
| 5 | Data discrepancy at month-end | Yes | App Incident | P1 | Silent data errors — no alerts, no errors, just wrong numbers |

### Pattern: What Makes Incidents Hard to Triage

| Challenge | Scenarios | How to Handle |
|-----------|-----------|---------------|
| **Scope unclear** — one report could mean one user or thousands | 1, 3 | Verify before classifying. Check 2-3 more data points. |
| **Silent failure** — system looks healthy but output is wrong | 2, 5 | Don't trust "no errors." Validate output, not just process. |
| **Ambiguous type** — could be infra or app | 3 | Check the change calendar. Recent deployment → assume app first. |
| **External dependency** — vendor is down, not us | 4 | We own the service. Detect, failover, communicate. |
| **Late detection** — discovered days/weeks after the problem started | 2, 5 | Build reconciliation checks. The earlier you catch it, the smaller the blast radius. |
