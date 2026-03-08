# Skill: Risk Assessment

Identify what could go wrong and plan for it. Prevent happy-path-only thinking.

## MUST — Guardrails

- **Never present a plan without risks.** Every proposal, architecture, or solution has risks. If you can't find any, you haven't looked hard enough.
- **Distinguish risk from issue.** A risk is something that *might* happen. An issue is something that *has* happened. Don't conflate them.
- **Every identified risk needs a response.** Even if the response is "accept it." The four responses: Mitigate (reduce likelihood/impact), Transfer (insurance, SLA, contract), Avoid (change approach), Accept (acknowledge and monitor).
- **Consider cascading failure.** Don't assess risks in isolation. Ask: "If risk A materializes, does it trigger risk B?"

## SHOULD — Frameworks

- **Likelihood × Impact matrix** — Score each risk on two axes (e.g., 1-5 each). Plot on a grid. Focus attention on high-likelihood + high-impact quadrant. Simple, communicable, sufficient for most cases.
  - Likelihood: Rare (1) → Almost Certain (5)
  - Impact: Negligible (1) → Catastrophic (5)
- **Pre-mortem** — Imagine the project has failed. Work backwards: "What went wrong?" This surfaces risks that forward-looking analysis misses because it bypasses optimism bias.
- **FMEA (Failure Mode and Effects Analysis)** — For technical/infrastructure risks. Identify failure modes, their effects, and detection mechanisms. Add a "detectability" score to the standard likelihood × impact.
- **Risk register** — For ongoing tracking. Columns: Risk ID, Description, Category, Likelihood, Impact, Score, Response, Owner, Status. Use when risks need to be monitored over time.

## COULD — Open Space

- **Spot normalized risks.** What risks has the team been living with so long they no longer see them? (e.g., "we've always done manual deployments" — the risk of human error is invisible to them but real.)
- **Second-order effects.** If your mitigation works, what new risks does it introduce? (e.g., adding a circuit breaker mitigates cascade failure but introduces the risk of premature service isolation.)
- **Black swan thinking.** Beyond the probable risks, what low-probability event would be catastrophic? Not to plan for every unlikely scenario, but to ask: "Do we have any existential exposure?"
- **Risk as opportunity.** Some risks, if managed well, become competitive advantages. A complex regulatory requirement that's hard to comply with is also hard for competitors to comply with.
