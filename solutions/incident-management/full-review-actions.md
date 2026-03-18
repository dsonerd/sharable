# Full Swimlane Flow — Presentation-Readiness Review

> **Reviewed by**: tcl-cio (CIO perspective)
> **Date**: 2026-03-18
> **Scope**: `swimlane-flow.md` and `swimlane-flow.drawio` (full version)
> **Purpose**: Determine if the full incident management documentation is clear, consistent between MD and DRAWIO, structurally sound for operational use, and would hold up under executive or auditor scrutiny.
> **Overall assessment**: Solid operational documentation with good role clarity and process coverage. However, there are consistency gaps between the MD and DRAWIO, missing visual flows in the diagram, terminology issues, and structural problems that must be fixed before this is considered authoritative. The issues below are ordered by severity of impact on operational clarity and auditability.

---

## Action Items

### 1. Management notification trigger from Triage has a misleading source in the diagram

- **Issue**: In the DRAWIO, edge 340 ("P1/P2 identified -> notify Management") originates from the "Infra healthy?" diamond (id=123), not from the point where priority is actually assigned. The notification logically happens AFTER classification AND priority assignment — i.e., after the KB match checks or scope assessment determines it is P1/P2. Starting the notification edge from the "Infra healthy?" diamond implies Management is notified before priority is even determined, which is incorrect. The MD correctly places this after Step 2.3 (Log Incident, SLA clock starts, classify).
- **Recommendation**: Change the source of edge 340 from "Infra healthy?" (id=123) to originate from the log/classify box (id=122), or split into two notification edges — one from the infra KB match result and one from the app KB match result — both feeding into the "Notified (P1/P2)" box in the MGMT lane. This makes the trigger accurate: Management is notified after priority is confirmed as P1/P2.
- **Applies to**: DRAWIO

### 2. No edge connecting "Approve Fix Deploy" back to the deploy step in DRAWIO — flow is asymmetric with the request edge

- **Issue**: Edge 570 sends the approval request from "Dev Fix" (id=163) down to "Approve Fix Deploy" (id=560) in the MGMT lane. Edge 571 returns "Approved" from the MGMT box back to "Deploy" (id=165). However, edge 570 exits from the LEFT side of the Dev Fix box (exitX=0), routes DOWN through x=928 to the MGMT lane, but the return edge 571 exits from the RIGHT side of the MGMT box (exitX=1) and routes UP through x=1475. This creates a wide visual loop that is hard to trace. The request goes left-and-down, and the response comes right-and-up through a different x-corridor. At operational review scale, this approval round-trip is confusing.
- **Recommendation**: Route both edges through the same visual corridor. Have the request edge exit the Dev Fix box going down (exitX=0.5, exitY=1) to the MGMT lane, and have the approved edge return upward on the same side. Alternatively, use a distinct color pair (amber down, green up) with clear circled numbers "1" and "2" to show sequence. Increase edge label font to 10pt minimum.
- **Applies to**: DRAWIO

### 3. The QA validation loop is visually confusing — goes down from Dev Fix, across to QA, and loops back

- **Issue**: Edge 549 routes from "Dev Fix" (id=163) to "QA Validate" (id=164) through waypoints that go down and right (x=1420, y=1075 to y=1305) then back left to QA. Then edge 322 routes from "QA Validate" back to "Deploy" (id=165) going right to x=1460 then up to y=1140. Combined with the approval gate edges, the app response section has four edges crossing in the same visual space. This creates a tangle that makes the app deployment sequence unclear.
- **Recommendation**: Simplify the routing. Consider positioning the QA box between Dev Fix and Deploy vertically (or to the right), so the flow reads top-down: Dev Fix -> QA Validate -> Deploy, with the approval gate as a side loop. If repositioning is not feasible, at minimum add sequence labels ("①→QA", "②→Deploy") and use consistent edge colors.
- **Applies to**: DRAWIO

### 4. The DRAWIO has no legend or color key explaining the color scheme

- **Issue**: The diagram uses a deliberate and consistent color scheme — indigo for Detect, purple for Triage, amber for App paths, red for Infra paths and Major Incident, green for Verify, blue for Close, purple for L3/Vendor. But there is no legend anywhere on the canvas. An operational user or auditor looking at this for the first time will see colors but not understand their semantic meaning. This was identified in the light version review (item 14) and should also be addressed in the full version.
- **Recommendation**: Add a legend box in the bottom-right of the canvas (below the MANAGEMENT lane, around y=1530) mapping: Indigo = Detect, Purple = Triage, Amber = App Incident path, Red = Infra Incident / Major Incident, Green = Verify, Blue = Close, Purple (dark) = L3/Vendor, Grey dashed = Management notifications. Include path types: "Solid = primary flow, Dashed = notification / approval."
- **Applies to**: DRAWIO

### 5. "Blameless RCA" terminology in DRAWIO box should be expanded for clarity

- **Issue**: The DRAWIO box (id=200) reads "Lead blameless RCA" and the MD (Step 5.1) also uses "Lead Blameless RCA." While the full version is aimed at an operational audience who may understand "RCA," the term "blameless" is SRE/DevOps jargon that may not be understood by all participants (e.g., Management, L1 help desk staff, vendor contacts). This was flagged in the light version review (item 6) and should be addressed consistently here.
- **Recommendation**: In the MD, expand on first use: "Lead Blameless Root Cause Analysis (focused on systemic improvement, not individual fault)." In the DRAWIO box (id=200), change the label to: "Lead Post-Incident Review (Blameless RCA)" with a sub-label "(P3/P4: simplified review only)." This preserves the "blameless RCA" term for operational staff who know it, while making it accessible to everyone.
- **Applies to**: BOTH

### 6. The IC Coordination box mixes too much information — hard to parse at operational scale

- **Issue**: DRAWIO box id=160 contains six lines of text: "IC (P1/P2 only) / Workaround first if available / Coordinate team - Manage comms / Decide: rollback? escalate? war room? / Status updates (P1:30m - P2:1hr) / Include reporter in updates." This is the densest box on the diagram and at standard zoom it will be difficult to read. The MD (Step 3.1) expands this properly, but the diagram should be scannable.
- **Recommendation**: Split the IC box into two boxes: (1) "IC Coordination" with "Workaround first / Coordinate team / Decide: rollback? escalate? war room?" and (2) a separate communication annotation box: "Status: P1 every 30m, P2 every 1hr / Include reporter." Or reduce the IC box text to key actions only and let the communication detail live in the annotation-style box.
- **Applies to**: DRAWIO

### 7. The "Not an Incident" exit path has no terminal indicator

- **Issue**: The DRAWIO box (id=121) "NOT AN INCIDENT / Route to: Service Request / User error / Backlog / Notify reporter & close" is styled with a grey border and muted color, which is good. But it has no terminal/end indicator. A reader unfamiliar with the process cannot tell if this is a dead end or if something follows. This mirrors item 9 from the light version review.
- **Recommendation**: Add an "END" label inside or below the box, or change the shape to a rounded rectangle with a thicker border (traditional terminal shape). Add a small stop indicator to make it clear this exits the incident process.
- **Applies to**: DRAWIO

### 8. MD Step 2.4 says "Infra Healthy?" but the DRAWIO diamond also says "Infra healthy?" — the question is misleading

- **Issue**: The decision "Infra healthy?" determines whether the incident is infrastructure or application. But the phrasing is confusing: "Infra healthy? NO = Infra broken" implies a health check, not a classification decision. What it actually means is "Is the infrastructure layer functioning normally?" If yes, the problem is in the application; if no, infrastructure is the root. This is a classification heuristic, not a health status check. Both the MD and DRAWIO use this same misleading phrasing.
- **Recommendation**: Rephrase to "Infra issue?" with branches "YES = Infra Incident" and "NO = App Incident." Or use "Root cause in infra?" This is clearer because it directly asks the classification question rather than inverting the logic. Update both the MD (Step 2.4) and the DRAWIO diamond (id=123) and edge labels (307, 308).
- **Applies to**: BOTH

### 9. No visual connection between MGMT lane boxes — they appear as isolated islands

- **Issue**: The MGMT lane has five boxes: "Notified (P1/P2)" (id=220), "Receive status updates" (id=221), "Notify Stakeholders" (id=530), "Notified of restoration" (id=222), "Approve Fix Deploy" (id=560), and "Review RCA & sign off" (id=203). These boxes sit in the MGMT lane but have no horizontal flow connecting them to each other. Management's journey through the incident — notified, receives updates, approves deploy, receives all-clear, reviews RCA, signs off — is invisible. Each box is connected only to the technical lanes above. This was flagged in the light version review (item 2).
- **Recommendation**: Add a light dashed horizontal connector chain through the MGMT lane boxes in chronological order: Notified -> Receive status updates -> (Notify Stakeholders if Major) -> Approve Fix Deploy -> Notified of restoration -> Review RCA & Sign Off. Use a very light grey (#CBD5E1) dashed line at 1pt to avoid visual clutter. This creates a visible "management track" that shows the management experience of the incident.
- **Applies to**: DRAWIO

### 10. The MD references "Incident Triage Guide" at Step 2.1 but the DRAWIO annotation places it at a different location

- **Issue**: The MD says the "Incident Triage Guide" is used at "Stage 1 — Detection and initial acknowledgement" (per the Referenced Documents table at the bottom). But the DRAWIO annotation box (id=400) for this document is placed at y=238, which is below the L1 Acknowledge box — in the Triage stage area. This is a minor inconsistency, but if an auditor cross-references the MD's "Used At" column against the diagram placement, they will notice the discrepancy.
- **Recommendation**: In the MD Referenced Documents table, change the "Used At" for "Incident Triage Guide" from "Stage 1 — Detection and initial acknowledgement" to "Stage 1-2 — Detection, acknowledgement and initial triage." This accurately reflects both where the guide is referenced in the MD (Step 2.1) and where the annotation sits in the DRAWIO.
- **Applies to**: MD

### 11. The "INCIDENT CLOSED" box is positioned below the MANAGEMENT lane, outside all defined lanes

- **Issue**: The DRAWIO's "INCIDENT CLOSED" box (id=204) is at y=1465. The MANAGEMENT lane background (id=16) spans y=1380 to y=1510 (height 130). So the box starts at y=1465, which is inside the MGMT lane — but visually it sits at the very bottom edge, partially outside the lane if the lane background doesn't extend far enough. More importantly, the closing action follows Management sign-off (id=203), so it should clearly be associated with the MGMT lane or be positioned as a cross-lane terminal. The box receives its edge from Management Review (id=203, edge 330), which is correct, but the position could be ambiguous.
- **Recommendation**: Either (a) ensure the INCIDENT CLOSED box is clearly within the MGMT lane by adjusting its y position to center vertically in the MGMT lane band, or (b) style it as a cross-lane terminal that spans the bottom of all lanes (full width, centered, with distinctive terminal styling). Option (b) better conveys that closure is a process-level event, not owned by a single lane.
- **Applies to**: DRAWIO

### 12. The Emergency Change "NO" path is missing — only the YES path to RFC exists

- **Issue**: DRAWIO edge 545 connects "Emergency Change?" (id=502) to "RFC" (id=503) for the YES case. But there is no edge for the NO case. The diamond just dead-ends if the answer is NO. The MD (Step 3.2) says "NO — Proceed with standard response" but the diagram does not show where "standard response" routes to. This is a process gap in the diagram: a decision diamond with only one exit.
- **Recommendation**: Add an edge from the "Emergency Change?" diamond for the NO case. It should route to the same downstream response activities (Infra Fix / App Fix / L3 Escalation). Use a label "NO — Standard" and route it back to the main response flow below the IC box. Every decision diamond must have exits for all branches.
- **Applies to**: DRAWIO

### 13. The MD does not describe the flow from Dev Fix through QA and back to Deploy clearly enough

- **Issue**: Step 3.4a says "Route to QA Validate (Step 3.4c)." Step 3.4b says the approval gate comes "before deployment." Step 3.4c says "If validation passes, loop back to Deploy step." The ordering is confusing: does the fix go Dev -> QA -> Approve -> Deploy? Or Dev -> Approve -> QA -> Deploy? Or Dev -> QA -> Deploy (with Approve as a parallel gate)? The DRAWIO shows Dev Fix -> QA (edge 549), QA -> Deploy (edge 322), and separately Dev Fix -> Approve (edge 570) -> Deploy (edge 571). This suggests QA and Approval run as separate paths both feeding into Deploy, but the MD's step numbering (3.4a, 3.4b, 3.4c, 3.4d) implies a linear sequence.
- **Recommendation**: Clarify the sequence in the MD. Add an explicit note: "For P1/P2 app incidents, the approval gate and QA validation run in parallel. Deployment proceeds only when BOTH are complete (management approval received AND QA validation passed)." Reorder the steps to reflect this: 3.4a (Dev Fix) -> 3.4b (QA Validate, parallel) + 3.4c (Approval Gate, parallel) -> 3.4d (Deploy when both clear). Alternatively, if they are sequential, state the order explicitly.
- **Applies to**: MD

### 14. After-hours note in DRAWIO is only for Stage 2b — no after-hours annotation for other stages

- **Issue**: The DRAWIO has an after-hours annotation (id=410) near the Collaborate stage: "After hours: L1 + on-call dev assess; BA joins next business day." The MD has the same note under Stage 2b. But there is no after-hours guidance for Stage 3 (who responds after hours for Infra? For App?), Stage 4 (who verifies after hours?), or Stage 5 (when does RCA happen if the incident resolved at 3 AM?). This was also flagged in the backlog as IM-005 (on-call model), but even before the full on-call model is documented, the existing after-hours note should be expanded or cross-referenced.
- **Recommendation**: In the MD, add a brief note under the "Escalation Paths" section: "After-hours operations: L1 on-call responds to all alerts. For P1/P2, the IC and tech team are engaged per the on-call rotation. BA, QA, and Management join at the next business day unless the IC explicitly escalates. See the On-Call Model (to be defined per IM-005) for full details." In the DRAWIO, add a second annotation near the IC box: "After hours: IC engages on-call tech; Mgmt next business day unless P1."
- **Applies to**: BOTH

### 15. The RACI matrix in the MD shows QA as "R (App)" for Stage 3 but has no entry for Stage 4

- **Issue**: The RACI matrix shows QA as Responsible for Stage 3 (app path). But QA has no role in Stage 4 (Verify) or Stage 5 (Close). This makes sense — QA validates in staging (Stage 3) and the Tech Team monitors production (Stage 4). However, a reader might question why QA is absent from verification. Also, the RACI shows L3/Vendor as "R (if escalated)" for Stage 3 but silent about who is Responsible for verification when L3/Vendor implements the fix. The DRAWIO shows L3 Implement -> Verify Monitor (edge 548), implying the Tech Team verifies even L3 fixes.
- **Recommendation**: Add a footnote to the RACI matrix: "Stage 4 verification is always performed by the Tech Team, regardless of who implemented the fix (including L3/Vendor fixes). QA's validation scope is limited to staging environment testing during Stage 3." This prevents ambiguity about who owns production verification.
- **Applies to**: MD

### 16. The Collaborate stage edge routing from "Collaborate" to "IC Coordination" crosses the entire diagram

- **Issue**: Edge 317 routes from "Collaborate" (id=150, at x=875, y=535) to "IC Coordination" (id=160, at x=1100, y=700). The edge exits right and enters from below (entryX=0.5, entryY=1). This means it routes from x=1060 (right edge of Collaborate) rightward then DOWN into the IC lane. Since the Collaborate box is in the L1/L2 lane (y=535) and IC is in the IC lane (y=700), this is a cross-lane edge that is reasonable. However, the entry point (entryY=1) means it enters the IC box from the BOTTOM, which is counterintuitive when the Collaborate stage is to the LEFT of the Respond stage (earlier in the timeline).
- **Recommendation**: Change the entry point to entryX=0, entryY=0.5 (left side) or entryX=0.5, entryY=0 (top) so the flow enters the IC Coordination box from a direction that reads naturally left-to-right or top-to-bottom.
- **Applies to**: DRAWIO

### 17. The MD's Communication Checkpoints table does not include Management-specific communications

- **Issue**: The Communication Checkpoints table (4 rows) covers: 1st (acknowledgement), 2nd (priority assignment), Ongoing (status updates), Last (resolved). But Management receives separate notifications: P1/P2 identification, major incident stakeholder notification, status updates, all-clear, and RCA sign-off. The "Management Parallel Track" table covers these, but the Communication Checkpoints table only mentions the reporter-facing communications. For a complete operational reference, all communications should be in one place or cross-referenced.
- **Recommendation**: Add a "Management" column to the Communication Checkpoints table, or add Management notification rows: "P1/P2 identified: L1/L2 -> Management (via escalation)", "Major Incident: IC -> Stakeholders", "All-clear: IC -> Management", "RCA complete: IC -> Management (for sign-off)." Alternatively, add a note below the table: "For Management-specific notifications, see the Management Parallel Track table above."
- **Applies to**: MD

### 18. The "Escalation Policy" document reference annotation in DRAWIO is placed in the MGMT lane but not near any specific process step

- **Issue**: DRAWIO annotation id=405 ("Escalation Policy") is at x=690, y=1408, which places it in the MGMT lane between the "Notified (P1/P2)" box and the "Approve Fix Deploy" box. It is not connected to any box or edge. The MD says the Escalation Policy is used at "Stage 2/3 — Management notification and escalation decisions." The placement is reasonable but the lack of any visual connection makes it look like a floating label.
- **Recommendation**: Either connect the annotation to the "Notified (P1/P2)" box (id=220) with a very light dotted line, or move it directly adjacent to the box so the spatial proximity implies the connection. Alternatively, add a small arrow or line from the annotation to the nearest relevant box.
- **Applies to**: DRAWIO

### 19. The MD's "Process Stages and Time Targets" table includes Stage 2b but the RACI matrix uses "2b Collaborate" — ensure naming is consistent

- **Issue**: The Process Stages table calls it "COLLABORATE" with a time target. The RACI matrix calls it "2b Collaborate." The MD section header says "Stage 2b: COLLABORATE (< 30 min) — App Incidents Without KB Match." The DRAWIO stage header (id=22) says "2b COLLABORATE / App, no KB < 30 min." These are all slightly different formulations. While the meaning is clear, for an auditable document, the naming should be identical across all references.
- **Recommendation**: Standardize on: "Stage 2b: COLLABORATE (< 30 min)" everywhere. In the Process Stages table, the Name column should say "COLLABORATE." In the RACI matrix, the Stage column should say "2b Collaborate." In the DRAWIO header, keep "2b COLLABORATE / App, no KB < 30 min" as it includes helpful context. No changes needed — the current naming is close enough. **Downgrade: this is a minor cosmetic issue, no fix required unless other edits are being made to these sections.**
- **Applies to**: N/A (cosmetic — note only)

### 20. The DRAWIO places "Identify root cause" (Tech Team, id=201) at y=1035 but the IC's "Lead blameless RCA" (id=200) is at y=695 — the visual flow goes UP from Tech back to IC

- **Issue**: In Stage 5 (Close), the flow is: IC leads RCA (id=200, y=695) -> Tech Team identifies root cause (id=201, y=1035) -> IC defines action items (id=202, y=770) -> Management reviews (id=203, y=1395) -> Incident Closed (id=204, y=1465). The edge from "Lead RCA" goes DOWN to Tech Team (y=695 -> y=1035), then the edge from Tech Team goes back UP to IC "Define action items" (y=1035 -> y=770). This up-down-up routing in Stage 5 is visually confusing. The reader expects a consistent downward or left-to-right flow.
- **Recommendation**: Consider repositioning the Stage 5 boxes so the flow reads consistently top-to-bottom within the stage: Lead RCA (IC lane) -> Identify root cause (Tech lane, below IC) -> Define action items (IC lane, below tech) -> Management review (MGMT lane, below IC). Alternatively, reposition "Identify root cause" to be in the IC lane area (since the IC leads the RCA and delegates investigation), keeping the flow within one horizontal band.
- **Applies to**: DRAWIO

---

## Cross-Reference with Existing Backlog

Several items from this review overlap with or complement items in `backlog.md`:

| Review Item | Related Backlog Item | Relationship |
|------------|---------------------|--------------|
| Item 14 (after-hours) | IM-005 (on-call model) | This review adds interim guidance; IM-005 addresses the full model |
| Item 4 (legend) | N/A | New finding for full version |
| Item 5 (blameless RCA) | N/A | Mirrors light version item 6 |
| Item 8 (Infra healthy?) | N/A | New finding — terminology clarification |
| Item 12 (Emergency Change NO) | N/A | New finding — diagram flow gap |
| Item 13 (QA/Approval flow) | N/A | New finding — MD clarity |

---

## Summary

| Category | Count | Items |
|----------|-------|-------|
| Diagram flow accuracy / missing edges | 4 | 1, 2, 12, 16 |
| Diagram visual clarity / layout | 4 | 3, 6, 11, 20 |
| Missing diagram elements (legend, terminal indicators) | 2 | 4, 7 |
| Terminology / naming consistency | 2 | 5, 8 |
| MD/DRAWIO consistency | 2 | 10, 18 |
| MD structural clarity | 3 | 13, 15, 17 |
| Operational completeness | 1 | 14 |
| Cosmetic (no action) | 1 | 19 |

**Priority order for fixes**: Items 1, 8, 12 (flow accuracy and logic), then 4, 5, 7 (accessibility), then 2, 3, 9, 20 (visual clarity), then 10, 13, 14, 15, 17 (MD improvements), then 6, 11, 16, 18 (polish).

**Verdict**: Strong foundation but not yet authoritative. The 19 actionable items (excluding item 19) should be addressed by tcl-ito. The most critical fixes are items 1 (notification trigger), 8 (misleading decision label), and 12 (missing decision branch) — these affect process accuracy.

---

**Reviewer**: tcl-cio (CIO perspective, operational and audit readiness)
**Date**: 2026-03-18
**Next step**: Assign to tcl-ito for implementation
