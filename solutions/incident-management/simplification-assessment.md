# ITO Assessment: Incident Management Swimlane Simplification

> **Context**: The user has raised five concerns about the current full swimlane diagram (`swimlane-flow.drawio`) being overcomplicated for operational use. This document provides the ITO assessment of each concern and a recommended simplified flow.

---

## Executive Summary

The user's concerns are valid. The current diagram tries to model every possible decision branch and loop, which makes it a **process design artifact** rather than an **operational response tool**. An L1 engineer at 2am during a P1 should be able to trace their path in under 10 seconds. Today's diagram requires studying to understand. The recommended simplifications below preserve all necessary governance without sacrificing usability.

---

## Assessment of Each Concern

### Concern 1: "Major Incident?" Diamond is Redundant

**Verdict: AGREE -- remove it.**

The current flow:
```
Infra KB match/no-match -> Assign priority -> Major Incident? (P1)
                                                  |           |
                                                 YES         NO
                                                  |           |
                                           Activate MI   IC Coordination
                                                  |
                                           IC Coordination
```

Both YES and NO end at IC Coordination. The only difference is that YES activates a War Room first. But the priority was already assigned in the step before. The IC Coordination box already says "Decide: rollback? escalate? war room?" -- so the IC already has the authority to activate a war room based on the priority they see.

**Operationally correct simplification**: After priority assignment, flow directly to IC Coordination. Add a note/annotation to the IC Coordination box: "P1: Activate War Room / Bridge Call immediately." This makes it a **behavior within IC Coordination driven by priority**, not a separate decision gate.

The "Activate Major Incident" box (id 500) with its War Room / Bridge Call / Assign IC content becomes a sub-action within IC Coordination, not a separate routing decision. Priority already tells the IC what to do.

**Why this is safe**: The IC still activates the war room for P1. The process outcome is identical. We just eliminated a diamond that didn't actually change the routing.

---

### Concern 2: "Emergency Change?" Diamond is Circular

**Verdict: AGREE -- remove the diamond, fold into IC Coordination.**

The current flow:
```
IC Coordination -> Emergency Change?
                      |           |
                     YES         NO
                      |           |
                     RFC      (loops back)
                      |
                (loops back to IC Coordination)
```

Both paths return to IC Coordination. The RFC is a documentation artifact, not a routing decision. Creating an RFC does not change what the IC does next -- they still coordinate the response.

**Operationally correct simplification**: Remove the "Emergency Change?" diamond entirely. Add to IC Coordination box: "Create RFC if change needed (all P1/P2 changes are emergency by default)." Reference the Change Management Policy from the IC Coordination box.

**Why this is safe**: RFC creation is a parallel activity, not a gate. In practice, during a P1, the IC says "someone file the RFC" while continuing to coordinate. It is not a decision that halts or reroutes the flow. Furthermore, as the user correctly points out, P1/P2 incidents are by definition emergencies -- there is no scenario where a P1/P2 incident requires a change but that change is somehow "non-emergency."

---

### Concern 3: App Incident Path Confusion

**Verdict: AGREE on all three sub-points.**

**3a. Connection between "Root cause & develop fix" (163) and "Deploy via CI/CD" (165):**

In the current diagram, 163 (Dev Team: Root cause & develop fix) does NOT connect directly to 165 (Dev/DBA: Deploy via CI/CD). Instead, 163 goes to QA (164), and only on QA Pass does it reach 165. There is also a parallel path from 163 to Management Approval (560). This means the connection between "develop a fix" and "deploy the fix" is mediated through QA and approval -- which is correct, but the diagram makes it hard to trace because the arrows go down to QA, back up to deploy, and simultaneously down to management and back up.

**3b. QA fail/rework loop:**

The user is right. The QA fail/rework loop (edge 580: QA -> Dev Team "QA Fail Rework") adds visual noise without operational value. In practice:
- Dev develops fix
- QA tests in staging
- If it fails, of course it goes back to dev -- this is understood by everyone
- Showing the loop explicitly does not help the L1/L2 reading the diagram

**Recommendation**: Remove the QA Fail loop arrow. The diagram should show the **happy path**: Dev -> QA -> Deploy. A note on the QA box can say "Rework until pass" if needed.

**3c. Management approval for hotfix deployment:**

The user is right that this is the more important flow to highlight. Currently, the approval arrow from 163 to 560 (Approve Fix Deploy) and back from 560 to 165 is present but visually competing with the QA loop and other arrows, making it hard to see.

**Recommendation**: Make the app path linear and clear:
```
Dev: Root cause & develop fix
        |
        |---> (parallel) QA: Validate in staging
        |---> (parallel, P1/P2 only) Mgmt: Approve deploy
        |
        v  (both must pass)
Dev/DBA: Deploy via CI/CD
```

---

### Concern 4: RFC / Emergency Change Can Be Simplified

**Verdict: AGREE -- this is the same issue as Concern 2, with an additional insight.**

The user's point is sharp: if it is P1/P2, it IS an emergency change by definition. There is no P1/P2 incident where the IC would say "no, this is a standard change, let's wait for the CAB." That scenario does not exist in a life insurance production environment at 2am.

**Recommendation**: Eliminate the "Emergency Change?" diamond. State in the IC Coordination box or an annotation: "All P1/P2 changes are emergency changes. RFC created automatically." Reference Change Management Policy for details.

For P3/P4 where it is genuinely ambiguous: those do not go through IC Coordination in practice (the document already says P3/P4 are handled by senior L1 or team lead). So the Emergency Change diamond was never relevant for the cases where it might have been meaningful.

---

### Concern 5: Add Step Numbers and Scenario Paths

**Verdict: AGREE -- this is the highest-value improvement.**

Step numbers transform the diagram from a visual map into an operational reference. When the L1 calls the IC at 2am and says "I'm at step 7," everyone immediately knows the state. It also enables:
- Training scenarios: "Walk me through path A"
- Runbook references: "At step 5, execute runbook RB-003"
- Audit trail: "INC-4521 followed path B, steps 1-2-3-6-7-8-12-13-14-15"

---

## Recommended Simplified Flow

### Step Numbering and Layout

Here is the proposed simplified flow with numbered steps. Every box in the diagram gets a number. Diamonds get a number too.

```
STEP  LANE              BOX/DIAMOND                                    STAGE
----  ----              -----------                                    -----
 1    ANYONE            Alert / User Report / Health Check Fails       DETECT
 2    L1/L2             Receive & Acknowledge (ITSM ticket, 1st msg)  TRIAGE
 3    L1/L2             [Diamond] Real Incident?                       TRIAGE
      -> NO:            Route to SR / User Error / Backlog -- END
 4    L1/L2             Log INC-xxxx, SLA starts, Classify             TRIAGE
 5    L1/L2             [Diamond] Infra or App?                        TRIAGE
      -> INFRA: go to 6
      -> APP:   go to 8
 6    L1/L2             [Diamond] KB Match? (Infra)                    TRIAGE
      -> YES: Assign P from KB, execute documented response -> go to 10
      -> NO:  Assign P by scope -> go to 10
 7    --                (reserved / unused)
 8    L1/L2             [Diamond] KB Match? (App)                      TRIAGE
      -> YES: Assign P from KB, execute first response,               TRIAGE
              notify tech team -> go to 10
      -> NO:  Assign preliminary P -> go to 9
 9    L1/L2 + Tech/BA   Collaborate: Assess blast radius,             COLLABORATE
                         Confirm/adjust priority -> go to 10
10    IC                IC Coordination (P1/P2)                        RESPOND
                        - P1: Activate War Room immediately
                        - Apply workaround if available
                        - Coordinate team, manage comms
                        - Create RFC (all P1/P2 = emergency change)
                        - Dispatch to 11 (Infra), 12 (App), or 14 (L3)
11    TECH TEAM         Infra: Rollback / Restart / Failover           RESPOND
                        -> Apply infrastructure fix -> go to 15
12    TECH TEAM         Dev: Root cause & develop fix                  RESPOND
                        -> Parallel: send to 13a (QA) and 13b (Mgmt)
13a   QA                Validate fix in staging                        RESPOND
13b   MANAGEMENT        Approve fix deploy (P1/P2 App only)            RESPOND
                        -> Both 13a + 13b must pass -> go to 12b
12b   TECH TEAM         Dev/DBA: Deploy via CI/CD, remediate data      RESPOND
                        -> go to 15
14    L3 / VENDOR       Specialist investigation                       RESPOND
                        -> Implement specialist fix -> go to 15
15    TECH TEAM         Monitor 15 min for regression                  VERIFY
16    IC                [Diamond] Reporter confirms?                    VERIFY
      -> YES: go to 17
      -> NOT RESOLVED: loop back to 10
17    IC                Confirm service restored (final comms)          VERIFY
18    IC                Post-Incident Review (Blameless RCA)            CLOSE
19    TECH TEAM         Identify root cause                            CLOSE
20    IC                Define action items, update KB                  CLOSE
21    MANAGEMENT        Review RCA & sign off (P1/P2 only)             CLOSE
22    --                INCIDENT CLOSED                                CLOSE
```

### What Was Removed
1. **"Major Incident?" diamond** -- absorbed into IC Coordination (step 10) as a P1 behavior
2. **"Emergency Change?" diamond** -- absorbed into IC Coordination (step 10) as standard P1/P2 practice
3. **RFC box** -- absorbed into IC Coordination annotation
4. **QA Fail/Rework loop** -- removed, implicit (note on QA box)
5. **"Activate Major Incident" box** -- absorbed into IC Coordination step 10

### What Was Added
1. **Step numbers on every box**
2. **Clearer parallel gate** for App path (13a + 13b both required before 12b)

### Net Effect
- Removed: 2 diamonds, 2 boxes, 1 loop arrow, and 4 edges (routing from/to removed elements)
- Added: Step numbers (visual only, no new shapes)
- Result: **The flow is shorter, has fewer branches, and every box has a number for reference**

---

## Recommended Scenario Paths

These should go in the updated `swimlane-flow.md` document.

### Path A: Infra Incident, KB Match, P1 (Major Incident -- Happy Path)
```
1 -> 2 -> 3(YES) -> 4 -> 5(INFRA) -> 6(YES) -> 10 -> 11 -> 15 -> 16(YES) -> 17 -> 18 -> 19 -> 20 -> 21 -> 22
```
**Narrative**: Alert fires. L1 acknowledges, confirms real incident, logs it. Classified as infra. KB has a match -- L1 assigns P1, executes documented response. IC takes over: activates war room, coordinates. Infra team rolls back. Monitor 15 min, reporter confirms. Service restored. RCA, management sign-off, closed.

### Path B: Infra Incident, No KB Match, P2
```
1 -> 2 -> 3(YES) -> 4 -> 5(INFRA) -> 6(NO) -> 10 -> 11 -> 15 -> 16(YES) -> 17 -> 18 -> 19 -> 20 -> 21 -> 22
```
**Narrative**: Same as Path A, but no KB match. L1 assigns priority by scope assessment. IC coordinates response. Same resolution flow.

### Path C: App Incident, KB Match, P1 (with Mgmt Approval)
```
1 -> 2 -> 3(YES) -> 4 -> 5(APP) -> 8(YES) -> 10 -> 12 -> 13a + 13b -> 12b -> 15 -> 16(YES) -> 17 -> 18 -> 19 -> 20 -> 21 -> 22
```
**Narrative**: User reports issue. L1 acknowledges, confirms real incident, logs it. Classified as app. KB match -- L1 assigns P1, executes first response, notifies dev. IC coordinates. Dev develops fix. QA validates in staging while management approves deploy (parallel). Both pass. Deploy via CI/CD. Monitor, confirm. RCA with management sign-off, closed.

### Path D: App Incident, No KB Match, P2 (with Collaboration)
```
1 -> 2 -> 3(YES) -> 4 -> 5(APP) -> 8(NO) -> 9 -> 10 -> 12 -> 13a + 13b -> 12b -> 15 -> 16(YES) -> 17 -> 18 -> 19 -> 20 -> 21 -> 22
```
**Narrative**: Same as Path C, but no KB match so L1 collaborates with Tech Team + BA to assess blast radius and confirm priority before IC takes over.

### Path E: L3/Vendor Escalation (any type)
```
1 -> 2 -> 3(YES) -> 4 -> 5(either) -> 6 or 8 -> 10 -> 14 -> 15 -> 16(YES) -> 17 -> 18 -> 19 -> 20 -> 21 -> 22
```
**Narrative**: After IC coordination, internal teams cannot resolve. IC escalates to L3/vendor. Specialist investigates and implements fix. Same verification and closure flow.

### Path F: Verification Fails (Loop Back)
```
... -> 15 -> 16(NOT RESOLVED) -> 10 -> (dispatch again) -> 15 -> 16(YES) -> 17 -> ...
```
**Narrative**: After fix and monitoring, reporter says not resolved. Flow loops back to IC Coordination for another round.

### Path G: Not an Incident
```
1 -> 2 -> 3(NO) -> END
```
**Narrative**: Alert received, L1 determines it is not a real incident. Routes to service request / user error. Notifies reporter. Done.

### Path H: App Incident, P3/P4 (No Mgmt Approval Needed)
```
1 -> 2 -> 3(YES) -> 4 -> 5(APP) -> 8(YES or NO) -> [9 if NO] -> 10* -> 12 -> 13a -> 12b -> 15 -> 16(YES) -> 17 -> 18(simplified) -> 19 -> 20 -> 22
```
*Note*: For P3/P4, step 10 is handled by senior L1 or team lead (no formal IC). Step 13b (Mgmt approval) is skipped. Step 21 (Mgmt RCA sign-off) is skipped. Step 18 is a simplified review.

---

## What Needs to Change

### 1. Diagram (`swimlane-flow.drawio`)
- Remove: "Major Incident?" diamond (id 133), "Activate Major Incident" box (id 500), "Emergency Change?" diamond (id 502), "RFC" box (id 503)
- Remove: QA Fail/Rework loop arrow (edge 580)
- Remove: All edges connecting to/from removed elements
- Update: IC Coordination box (id 160) to include P1 war room activation and RFC creation
- Add: Step numbers as small labels on each box
- Reconnect: Infra KB paths flow directly to IC Coordination instead of through Major Incident diamond
- Reconnect: App paths flow to IC Coordination as they do now (no change needed there)

### 2. Document (`swimlane-flow.md`)
- Update step-by-step to match new numbering
- Add the scenario paths section
- Remove references to removed diamonds
- Fold Major Incident activation and Emergency Change/RFC into IC Coordination description

### 3. Related documents
- `classification.md` -- no change needed
- `incident-knowledge-base.md` -- no change needed
- Light version (`swimlane-flow.light.md` / `.light.drawio`) -- already simplified, likely no change needed

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Removing "Major Incident?" diamond may cause P1 to not activate war room | High | IC Coordination box explicitly states "P1: Activate War Room immediately" |
| Removing RFC decision may cause emergency changes to go undocumented | Medium | IC Coordination annotation says "Create RFC (all P1/P2 = emergency change)". Reference Change Management Policy |
| Removing QA fail loop may give impression that QA always passes | Low | Note on QA box: "Rework until pass." This is obvious to anyone in the process |
| Step numbers may need to change if future process changes occur | Low | Numbers are labels, not constraints. Can be re-numbered |

---

## Summary of Recommendations

| # | Change | Effort | Impact | Priority |
|---|--------|--------|--------|----------|
| 1 | Remove "Major Incident?" diamond, fold into IC Coordination | Small | High (simplifies routing) | P1 |
| 2 | Remove "Emergency Change?" diamond + RFC box, fold into IC Coordination | Small | High (eliminates circular loop) | P1 |
| 3 | Remove QA Fail/Rework loop | Small | Medium (reduces visual noise) | P2 |
| 4 | Add step numbers to all boxes | Medium | High (enables scenario references) | P1 |
| 5 | Add scenario paths to swimlane-flow.md | Medium | High (enables training & audit) | P1 |
| 6 | Clarify App path: Dev -> parallel QA + Mgmt -> Deploy | Small | Medium (clearer approval flow) | P2 |

---

**Review Required**: This document should be reviewed by **tcl-cio** before implementation.
**Prepared by**: tcl-ito (IT Operations)
**Date**: 2026-03-19
