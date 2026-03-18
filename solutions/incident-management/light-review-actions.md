# Lightweight Swimlane Flow — Presentation-Readiness Review

> **Reviewed by**: tcl-cio (CIO perspective)
> **Date**: 2026-03-18
> **Scope**: `swimlane-flow.light.md` and `swimlane-flow.light.drawio`
> **Purpose**: Determine if the lightweight flow is clear and effective for a non-technical management/stakeholder audience in a presentation setting.
> **Overall assessment**: Good foundation, but requires targeted fixes before it is presentation-ready. The issues below are ordered by impact on audience comprehension.

---

## Action Items

### 1. P1/P2 notification trigger is invisible in the diagram

- **Issue**: In the markdown, Step 3.3 says "Management is notified when a P1/P2 incident is identified during triage." But in the drawio diagram, there is no visible arrow or connector from the Triage stage to the MGMT lane "Notified (P1/P2)" box. The "Notified" box sits in the MGMT lane at roughly the Triage/Respond boundary, but it has no incoming edge. A stakeholder looking at the diagram will not understand what triggers that notification.
- **Recommendation**: Add an explicit dashed edge from the "Classify" decision diamond (or from the Triage stage boundary) down to the "Notified (P1/P2)" box in the MGMT lane, labeled "P1/P2 identified." This makes the trigger visible and connects the MGMT lane to the main flow.
- **Applies to**: DRAWIO

### 2. Missing edge from "Notified" to "Approve Deploy" in MGMT lane

- **Issue**: The MGMT lane has three boxes (Notified, Approve Deploy, Review & Sign Off) but they appear as isolated islands. There is no horizontal flow connecting them, which makes the MGMT lane feel like disconnected annotations rather than an active participant in the process. A stakeholder will not understand Management's journey through the incident.
- **Recommendation**: Add a light connecting edge (dashed or dotted) from "Notified (P1/P2)" to "Approve Deploy (P1/P2 App Incident)" to "Review & Sign Off (P1/P2)" within the MGMT lane. This creates a visible management track that parallels the technical track. Even though these are triggered at different times, a lightweight connector shows progression.
- **Applies to**: DRAWIO

### 3. The "Classify" decision implies only two options — unclear what drives the choice

- **Issue**: The "Classify" diamond routes to either INFRA or APP. For a non-technical audience, the basis for this classification is not obvious. A board member or business stakeholder will ask: "How does L1 know if it is infrastructure or application?" The markdown says "Classify the incident type" but gives no criteria.
- **Recommendation**: In the markdown, add a one-sentence clarification under Step 2.3, e.g., "L1/L2 determines whether the root issue is in infrastructure (network, servers, storage, cloud services) or in the application (software bugs, data errors, business logic). The classification guide provides decision criteria." In the drawio, add a small annotation or tooltip near the Classify diamond: "See classification guide for criteria."
- **Applies to**: BOTH

### 4. No indication of what happens for P3/P4 incidents

- **Issue**: The entire flow — including management notification, approval gates, and RCA sign-off — is structured around P1/P2. A stakeholder will ask: "What about lower-priority incidents? Do they just... disappear?" The markdown does not address P3/P4 at all. The full version notes that P3/P4 have simplified handling, but the light version is silent.
- **Recommendation**: Add a brief callout box or note in the markdown (e.g., under Process Stages or as a footer note): "P3/P4 incidents follow the same Detect-Triage-Respond-Verify-Close flow but skip Management notification, the approval gate, and the formal RCA sign-off. They are handled by L1/L2 and the Response Team directly." In the drawio, add a small annotation near the bottom or a legend note: "P3/P4: same flow, no MGMT gates."
- **Applies to**: BOTH

### 5. The approval gate flow is hard to follow visually

- **Issue**: The approval gate between "Application Response" and "Approve Deploy" uses dashed lines with "request" and "approved" labels. The routing (down from App Response to MGMT, then back up) crosses visual space in a way that is confusing at presentation scale. The dashed lines are thin (1.5pt) and the labels are 9pt font — they will be barely visible when projected.
- **Recommendation**: Increase the stroke width of the approval edges to 2pt. Increase the label font size to at least 10pt. Consider using a distinct color for the approval round-trip (e.g., a single bold amber/gold color for both edges) and adding small directional annotations like circled numbers (1: request, 2: approved) to make the sequence explicit.
- **Applies to**: DRAWIO

### 6. The "Blameless RCA" box uses internal jargon

- **Issue**: "Blameless RCA" is industry jargon that a non-technical board member or business stakeholder may not understand. "RCA" is an abbreviation, and "blameless" is a cultural term from SRE/DevOps practices. In a presentation to senior management, this needs to be immediately understandable.
- **Recommendation**: Change the label to "Post-Incident Review" in both the diagram and the markdown. Explain "blameless" as a parenthetical on first use in the markdown: "Post-Incident Review (blameless — focused on systemic improvement, not individual fault)." The drawio box should read "Post-Incident Review" with a sub-label "Root cause, Actions, Update KB."
- **Applies to**: BOTH

### 7. "ANYONE" lane label is ambiguous for an executive audience

- **Issue**: "ANYONE" as a lane label is unclear. In a boardroom, this will prompt the question: "Anyone? Including customers? External parties?" The intent is any internal person or monitoring system, but the label does not convey that.
- **Recommendation**: Change the lane label to "DETECTOR" or "REPORTER / MONITORING" in both the markdown and the drawio. The description in the markdown already clarifies "Any person or system that detects an issue" — the lane label should reflect that.
- **Applies to**: BOTH

### 8. No SLA or time indication anywhere

- **Issue**: The light version deliberately omits time targets (per the Key Differences table). However, for a management audience, the single most important question is "how fast?" Presenting a process with zero time context will immediately draw the question: "What is our response time commitment?" A presentation that cannot answer this loses credibility.
- **Recommendation**: Add a simple time-bar or annotation above the stage headers showing high-level targets: "DETECT: <5 min | TRIAGE: <15 min | RESPOND: priority-dependent | VERIFY: <30 min | CLOSE: <48 hrs (P1/P2)." In the markdown, add a one-line SLA summary table after the Process Stages table. This does not need the full SLA breakdown — just top-line numbers.
- **Applies to**: BOTH

### 9. The "Service Request" exit has no visual distinction as a terminal state

- **Issue**: In the drawio, the "Service Request" box is styled with a grey border and muted text, which is good — but it has no terminal indicator. Visually, it looks like it could flow into something else. A viewer unfamiliar with the process might think the flow continues.
- **Recommendation**: Add a small "END" label below or inside the Service Request box, or style it with a stop/terminal shape (rounded rectangle with double border, or add a small "x" or stop indicator). This makes it visually clear that this is an exit from the incident process.
- **Applies to**: DRAWIO

### 10. "INCIDENT CLOSED" terminal box is in the RESPONSE TEAM lane, not MGMT

- **Issue**: The drawio places "INCIDENT CLOSED" at coordinates that put it in the Response Team lane (y=348, which falls within the 275-490 Response Team band). However, the last step before closure is "Review & Sign Off" by Management. The visual implication is that the Response Team closes the incident, when in reality Management signs off and then it is closed. This subtlety matters for an audience that cares about accountability and governance.
- **Recommendation**: Either (a) move the "INCIDENT CLOSED" box to span both lanes or position it on the lane boundary between Response Team and MGMT, or (b) add a connecting edge from "Review & Sign Off" (MGMT lane) back up to "INCIDENT CLOSED" to show that closure follows Management sign-off. Option (b) is already partially implemented (edge 321 goes from Review & Sign Off to INCIDENT CLOSED), but the box position creates a visual contradiction.
- **Applies to**: DRAWIO

### 11. The flow summary ASCII art in the markdown does not match the diagram exactly

- **Issue**: The ASCII flow summary (lines 127-163 in the markdown) shows "Infra Response" going directly to "Verify & Confirm" without the approval gate, which is correct. But it shows "App Response" going to "Mgmt: Approve Deploy" for all app incidents. The text above says the approval is only for P1/P2 app incidents, but the ASCII diagram does not include that qualifier.
- **Recommendation**: Add "(P1/P2)" annotation on the "request" edge in the ASCII diagram, e.g., `App Response ---(P1/P2)---> Mgmt: Approve Deploy`. This keeps the ASCII flow consistent with the described logic.
- **Applies to**: MD

### 12. The "Key Differences from Full Version" table should not be in a presentation document

- **Issue**: The markdown includes a detailed comparison table listing 10 things the light version omits (KB checks, QA validation, L3/vendor, etc.). This table is useful for internal version control but is counterproductive in a presentation document. Showing a stakeholder everything you left out invites the question "why did you remove that?" and undermines confidence. It also makes the document look like a derivative work rather than a complete artifact.
- **Recommendation**: Move the "Key Differences" table to a separate internal reference document or to the main `swimlane-flow.md` as an appendix. The light markdown should stand on its own as a complete presentation document. If a brief note is needed, a single line at the bottom: "A detailed operational version with additional roles, time targets, and procedural steps exists for the response team" is sufficient.
- **Applies to**: MD

### 13. The drawio diagram canvas is too wide for a single presentation slide

- **Issue**: The drawio diagram has a page width of 1550px and uses content all the way to x=1450. When projected on a standard 16:9 slide, the rightmost elements (Close stage) will be compressed or require zooming, and text at 9-10pt will be unreadable. The diagram needs to work at presentation scale.
- **Recommendation**: Review the diagram at 60-70% zoom (simulating projection). If text is not legible, increase base font sizes: node labels to 12pt minimum, sub-labels to 10pt minimum, edge labels to 11pt minimum. Consider reducing canvas width to 1200px and tightening horizontal spacing, or split the diagram into two slides (Detect-Triage-Respond on slide 1, Verify-Close on slide 2).
- **Applies to**: DRAWIO

### 14. No legend or color key

- **Issue**: The diagram uses a deliberate color scheme — purple for Triage, red for Respond, green for Verify, blue for Close, amber for App path, red for Infra path. But there is no legend explaining the color coding. A stakeholder will see colors but not understand their semantic meaning.
- **Recommendation**: Add a small legend box in the bottom-right corner of the diagram mapping colors to stages (e.g., "Purple = Triage, Red = Respond & Fix, Green = Verify, Blue = Close") and path types ("Red border = Infrastructure, Amber border = Application").
- **Applies to**: DRAWIO

### 15. The "Management Involvement" table in the markdown is excellent — surface it more prominently

- **Issue**: The "Management Involvement" table (3 rows showing triggers and actions) is exactly what a management audience wants to see. But it is buried below the step-by-step flow and the ASCII diagram. In a presentation setting, this should be front and center.
- **Recommendation**: Move the "Management Involvement" table to appear immediately after the "Swimlane Participants" section, before the step-by-step flow. This puts the "what does this mean for us" information early, which is how executives consume documents. Alternatively, add a "MGMT Summary" callout box at the top of the document.
- **Applies to**: MD

---

## Summary

| Category | Count | Items |
|----------|-------|-------|
| Diagram connectivity / flow clarity | 3 | 1, 2, 10 |
| Terminology / audience appropriateness | 2 | 6, 7 |
| Missing context for non-technical audience | 3 | 3, 4, 8 |
| Visual readability at presentation scale | 3 | 5, 13, 14 |
| Document structure for presentation use | 3 | 11, 12, 15 |
| Terminal state clarity | 1 | 9 |

**Verdict**: Not yet presentation-ready. The 15 items above are all fixable by tcl-ito. Items 1, 2, 6, 7, 8, and 12 should be addressed first as they will have the most impact on stakeholder comprehension.

---

**Reviewer**: tcl-cio (CIO perspective, stakeholder/presentation readiness)
**Date**: 2026-03-18
**Next step**: Assign to tcl-ito for implementation
