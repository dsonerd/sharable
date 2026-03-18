# IT Operation Capability Declaration — Supporting Frontline Sales in a Life Insurance Business

## Purpose

This document defines the **support scope and capabilities** of **IT Operation** when supporting **frontline sales users** who use the insurance sales system.

It assumes:
- the **frontline** uses a system to sell life insurance,
- **IT Operation** provides technical and operational system support,
- the **Operation Department** owns deep product/business knowledge and runs its own **L1 business support line** for frontline users,
- **business/product/underwriting/compliance** questions are handled by the Operation Department, not by IT Operation.

A standard service desk model treats first-line support as the **single point of contact** for incidents and service requests, with first-line teams logging, categorizing, diagnosing basic issues, resolving common items, and escalating the rest.  [oai_citation:0‡ServiceNow](https://www.servicenow.com/products/itsm/what-is-a-service-desk.html)

---

## 1) Core mission of IT Operation

IT Operation should help the frontline by making sure the sales system is:
- **available**
- **accessible**
- **usable**
- **stable**
- **supported through a clear ticketing/escalation process**

In practice, that means IT Operation owns the **technical support path** for the sales platform, while the Operation Department owns the **business decision path** and **business usage guidance**. Incident management is meant to restore service quickly after disruption, while service request management handles repeatable requests such as access, permissions, or standard fulfillment items.  [oai_citation:1‡atlassian.com](https://www.atlassian.com/incident-management)

---

## 2) What IT Operation can do in most cases

## 2.1 Single point of contact for frontline users

IT Operation can act as the **first contact point** for sales users when they need help with the system.

Typical intake channels:
- phone
- chat
- email
- support portal
- ticketing system

Typical responsibilities:
- receive the issue/request
- record the ticket
- categorize and prioritize it
- confirm user impact
- communicate status
- resolve simple issues
- escalate complex issues to the right team

When a user contacts IT Operation with a **business process or system usage question** (e.g., how to create a quote, which product to select), IT Operation records the request and **routes it to the Operation Department L1 with context** — not as a redirect, but as a warm transfer with ticket details.

This is a normal service desk responsibility in ITSM and tiered support models.  [oai_citation:2‡ServiceNow](https://www.servicenow.com/products/itsm/what-is-a-service-desk.html)

---

## 2.2 Login, access, and identity support

IT Operation can support the frontline on **identity and access** topics such as:
- password reset
- account unlock
- MFA issues
- access provisioning for approved users
- role/access validation
- removing access for leavers
- updating access after role changes
- checking whether the user has the correct permission set

Identity lifecycle management commonly covers onboarding, role changes, and offboarding, and Microsoft's Entra documentation explicitly describes workflows for onboarding, role changes, offboarding, audit logs, and troubleshooting.  [oai_citation:3‡Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/automate-identity-lifecycle-workflows/?utm_source=chatgpt.com)

**Examples for frontline sales:**
- new sales agent cannot sign in
- agency manager cannot access quotation screen
- user lost MFA device
- transferred staff needs a new role profile
- resigned staff access must be removed

---

## 2.3 Incident logging and first-line troubleshooting

IT Operation can own the first-line handling of **incidents** affecting the sales system.

Typical incident examples:
- cannot log in
- system is slow
- quote page not loading
- proposal submission failed
- document upload error
- printing error
- payment handoff error
- mobile/tablet access problem
- integration seems unavailable
- intermittent timeout

For these, IT Operation can:
- gather evidence
- reproduce basic symptoms
- check known issues
- perform first-line diagnosis
- attempt basic recovery steps
- escalate to L2/application/infrastructure if needed

First-line support is expected to handle initial diagnosis, common issues, and communication while restoring service or routing to the correct team. Incident management focuses on restoring normal service as quickly as possible.  [oai_citation:4‡atlassian.com](https://www.atlassian.com/incident-management)

---

## 2.4 Application break/fix support

IT Operation handles **technical failures** in the sales application — situations where the system is not working as designed.

Examples:
- screen returns an error or does not load
- submission fails with a system error
- document upload fails technically
- integration timeout or data sync failure
- print function produces corrupted output
- system performance is degraded

IT Operation does **not** provide guidance on how to use the system for business tasks (e.g., how to create a quote, which product to select, how to fill in proposal fields). Those questions are handled by the **Operation Department L1 business support line**, which owns frontline user training and business process guidance.

When a user contacts IT Operation with a business usage question, IT Operation records the request and routes it to the Operation Department L1 with context.

This separation avoids overlap between the two L1 support lines: **IT Operation answers "is the system working?"** while the **Operation Department answers "how do I use the system to do my job?"**

---

## 2.5 Service request handling

IT Operation can handle **routine service requests** through a structured process or service catalog.

Common request types:
- request new user access
- request role/profile change
- request printer setup
- request approved software/browser setup
- request device replacement
- request shared mailbox or queue access
- request distribution list access
- request standard report access
- request environment whitelist / VPN / connectivity support

Service request management is a distinct ITSM practice for routine, repeatable, usually low-risk requests, and service catalogs are a standard way to organize those requests.  [oai_citation:6‡ServiceNow](https://www.servicenow.com/products/itsm/what-is-service-request-management.html?utm_source=chatgpt.com)

---

## 2.6 Endpoint, device, and workplace support

If the frontline sells using company-managed laptops, desktops, tablets, printers, or network connections, IT Operation can support the user environment needed to run the sales system.

Typical support scope:
- device readiness
- browser compatibility
- workstation setup
- VPN/connectivity troubleshooting
- printer/scanner setup
- certificate installation
- peripheral support
- stale device cleanup / device offboarding
- reimage or replacement coordination

Microsoft Intune documentation describes device offboarding and cleanup for stale or misaligned devices, which is part of keeping managed endpoints usable and controlled.  [oai_citation:7‡Microsoft Learn](https://learn.microsoft.com/vi-vn/Intune/agents/device-offboarding-agent-use?utm_source=chatgpt.com)

**For frontline sales this matters because** many failures are not true application defects; they are caused by the device, browser, plugin, certificate, printer, or network path.

---

## 2.7 Monitoring, alerting, and early detection

IT Operation can monitor the health of the sales platform and supporting services so problems are found **before or as soon as** the frontline is impacted.

Typical monitoring scope:
- application availability
- response time
- API or integration health
- infrastructure alerts
- queue failures
- storage/network issues
- cloud service incidents
- scheduled maintenance alerts
- dependency outages

Azure Monitor is described by Microsoft as a unified observability service for collecting and acting on telemetry, and Azure Service Health provides alerts on outages, planned maintenance, and advisories. These are standard examples of the monitoring/alerting role IT operations plays.  [oai_citation:8‡Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview?utm_source=chatgpt.com)

**For frontline support, this means IT Operation can:**
- detect degradation early
- confirm whether the issue is user-specific or widespread
- announce major incidents
- reduce duplicate tickets by communicating known outages

---

## 2.8 Major incident coordination and outage communication

When there is a serious issue affecting many sales users, IT Operation can coordinate the **major incident response**.

Typical responsibilities:
- declare the incident
- identify affected users/services
- open bridge/chat war room
- coordinate technical teams
- send user updates
- track workaround status
- confirm recovery
- close and hand over for post-incident review

Incident management best practice emphasizes emergency response, restoration of service, communication, and defined support roles.  [oai_citation:9‡atlassian.com](https://www.atlassian.com/incident-management)

**Example:**
If all agents cannot submit applications from 10:00 AM onward, IT Operation should not wait for many complaints. It should coordinate technical response and communicate status to the frontline fast.

---

## 2.9 Workarounds and continuity support

IT Operation can provide **approved workarounds** when the sales system is partially degraded.

Examples:
- use approved alternate browser
- retry from another network
- save locally and re-upload later
- use manual capture form during outage
- redirect to fallback submission route
- defer noncritical background functions
- advise on planned maintenance windows

This is part of restoring service quickly and minimizing operational impact while the permanent fix is handled.  [oai_citation:10‡atlassian.com](https://www.atlassian.com/incident-management)

---

## 2.10 Ticket routing and escalation management

IT Operation can make sure issues are sent to the **right resolver group** with the **right information**.

Possible escalation paths:
- **L2 Application Support** — defects, configuration issues, interface failures, data mismatches
- **Infrastructure / Platform Team** — servers, network, storage, cloud platform, virtualization
- **Security / IAM Team** — access anomalies, MFA, privileged access, suspicious activity
- **Vendor / External Partner** — third-party platform or integration faults
- **Operation Department** — product rules, sales rules, underwriting/business clarification

Good first-line support improves speed by triaging correctly and escalating only when needed, with enough details for faster resolution.  [oai_citation:11‡atlassian.com](https://www.atlassian.com/incident-management/incident-response/support-levels)

---

## 2.11 Knowledge base and known issue management

IT Operation can maintain a **knowledge base** for common frontline issues.

Useful KB topics:
- login troubleshooting
- common error messages
- browser settings
- document upload checklist
- printer/form setup
- known issue status
- workaround steps
- access request instructions
- outage communication templates

Knowledge management platforms are designed to improve self-service and agent productivity by making answers and procedures easier to find and reuse.  [oai_citation:12‡ServiceNow](https://www.servicenow.com/platform/knowledge-management.html?utm_source=chatgpt.com)

**For this environment, this is one of the highest-value activities**, because many frontline issues repeat.

---

## 2.12 Change support and release readiness

IT Operation can support changes to the sales platform by making sure changes are implemented in a controlled way.

Typical responsibilities:
- review operational impact
- prepare support team for release
- check support documents
- confirm monitoring and alert setup
- communicate maintenance windows
- prepare rollback/support contacts
- watch production after release
- collect early incident feedback from frontline users

Change management is intended to prioritize, approve, schedule, and execute changes with minimal disruption; ITIL-style change enablement focuses on minimizing service risk during changes.  [oai_citation:13‡ServiceNow](https://www.servicenow.com/products/itsm/what-is-it-change-management.html?utm_source=chatgpt.com)

**Example:**
If a new quote engine release goes live, IT Operation should know the change window, expected impact, escalation contacts, and top failure symptoms to watch.

---

## 2.13 Operational reporting and service level tracking

IT Operation can measure and report support quality for the frontline.

Typical metrics:
- volume by ticket type
- top recurring incidents
- first response time
- resolution time
- first-contact resolution
- reopen rate
- outage duration
- availability by service
- access request turnaround
- knowledge article usage
- incident trend by branch/region/channel

Service request management platforms and service desks commonly use workflows and SLAs to manage timeliness and service quality.  [oai_citation:14‡ServiceNow](https://www.servicenow.com/products/request-management.html?utm_source=chatgpt.com)

These reports help show whether the real problem is:
- system defects,
- unstable integrations,
- poor access control,
- device/environment issues,
- or user training gaps.

---

## 2.14 Coordination with cloud and third-party service health

If the sales platform depends on cloud or SaaS components, IT Operation can track provider health and correlate it with frontline issues.

Examples:
- Microsoft 365 service issues
- Azure platform issues
- planned cloud maintenance
- third-party payment/signature/document platform outages

Microsoft documents service health views for active issues, advisories, and issue history, which is exactly the kind of information IT Operation can use to confirm whether the problem is internal or provider-side.  [oai_citation:15‡Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/enterprise/view-service-health?view=o365-worldwide&utm_source=chatgpt.com)

---

## 2.15 Support during onboarding, transfer, and offboarding of sales staff

IT Operation can support the people lifecycle from a technical operations perspective.

### Joiner
- create access
- assign proper role/profile
- prepare device
- confirm MFA
- enable standard tools

### Mover
- update permissions after branch/role change
- add/remove relevant system access
- adjust distribution lists and support groups

### Leaver
- disable access
- remove licenses where needed
- remove from groups
- recover or offboard devices
- confirm closure

This is aligned with identity lifecycle and offboarding practices described in Microsoft Entra documentation.  [oai_citation:16‡Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/automate-identity-lifecycle-workflows/?utm_source=chatgpt.com)

---

## 3) What IT Operation should NOT own

IT Operation should usually **not** own these items:

- product explanation
- benefit interpretation
- premium/business calculation validation
- underwriting decisions
- case acceptance/rejection rationale
- document sufficiency from a business perspective
- compliance interpretation
- exception approval
- sales rule interpretation
- customer advice
- **system usage guidance for business tasks** (how to create a quote, which product to select, how to fill in fields)

Those should go to the **Operation Department** or the proper business owners.

A good support model separates **technical support workstreams** from **business decision workstreams**, while keeping one clear intake path and strong routing. Service request and incident practices are meant to standardize who handles what.  [oai_citation:17‡atlassian.com](https://www.atlassian.com/itsm/service-request-management?utm_source=chatgpt.com)

---

## 4) Cross-team issue handling

Many frontline issues do not fall cleanly into IT Operation or the Operation Department. When ownership is unclear, the risk is that the user gets bounced between teams with no resolution.

### Grey-zone examples

| User reports | Technical angle | Business angle |
|---|---|---|
| "System rejected my proposal with error code UW-403" | Error code → system issue | UW-403 may mean underwriting rule rejection → business logic |
| "The premium calculation looks wrong" | Could be a calculation bug | Could be correct but user misunderstands product rules |
| "I can't find the rider option in the quote screen" | Screen/UI issue | Rider may not be available for this product/channel → business config |
| "Document upload succeeded but case still shows 'pending documents'" | Integration/workflow bug | Operations may not have released the document requirement list |
| "System won't let me backdate this policy" | System validation/block | Backdating may require business exception approval |

### No-Bounce Protocol

**Principle:** the team that receives the ticket owns it until the other team explicitly accepts it. No frontline user should ever be told "that's not us" without a warm handoff.

1. **First receiver owns the ticket.** Whichever team receives the ticket first is responsible for recording the issue, performing initial assessment, and — if they believe it belongs to the other team — transferring the ticket with context. The user never has to re-explain the issue.

2. **Transfer, not redirect.** The correct response is never "please call the other team." It is always: log the ticket, add initial findings, assign to the other team's queue, and notify the user with a ticket reference.

3. **15-minute grey-zone triage.** If the receiving team cannot determine ownership within 15 minutes, the ticket moves to a **shared triage queue** visible to both IT and Operations leads. This queue is jointly triaged **twice daily** (morning and afternoon). Tickets in the shared queue must be claimed within **2 hours**.

4. **Double-rejection escalation.** If a ticket is rejected by both teams, it auto-escalates to the IT Operation Manager and Operations Manager for a joint decision within **4 hours**. The decision is logged and becomes a precedent for future similar tickets.

5. **Monthly boundary review.** Grey-zone tickets are reviewed monthly. Recurring patterns are classified and assigned explicit ownership, so the grey zone shrinks over time.

---

## 5) Recommended support scope

A practical model for this setup is:

### IT Operation owns
- user access, login, and MFA issues
- device/browser/printer readiness
- application break/fix (technical failures)
- incident intake and triage
- monitoring and outage detection
- ticket routing and escalation
- major incident communication
- workaround communication
- knowledge base for technical issues
- support metrics and SLA tracking
- release/change readiness from an operational perspective
- cross-team ticket routing with warm handoff

### Operation Department owns
- product/business rules
- underwriting/product guidance
- sales process exceptions
- required business documents
- policy/business interpretation
- frontline business coaching
- **system usage guidance** (how to use the sales system for business tasks)
- non-technical process clarification

---

## 6) Suggested service catalog for frontline support

Below is a practical catalog IT Operation can publish for sales users:

### A. Access & Identity
- password reset
- account unlock
- MFA issue
- new user access
- role/profile change
- access removal

### B. Sales System — Technical Issues
- cannot log in
- screen/page not loading
- submission failure (system error)
- document upload failure (technical)
- print function error
- performance/slow response
- integration error
- report access issue

### C. Device & Workplace Support
- laptop/tablet issue
- browser setup
- printer/scanner issue
- VPN/network issue
- peripheral setup

### D. Incident & Outage
- system down
- branch-wide issue
- region-wide issue
- integration unavailable
- degraded performance

### E. Standard Requests
- new device request
- software installation
- shared mailbox access
- distribution list update
- approved report request

### F. Business Query Routing
- product rule question
- underwriting clarification
- compliance/process clarification
- system usage / how-to question
  → route these to the Operation Department L1 with context

---

## 7) Priority and SLA guidance

### Priority definitions

| Priority | Impact | Examples |
|---|---|---|
| **P1 — Critical** | Sales cannot sell at all, or many users/branches are blocked | Full login outage, system-wide submission failure, major integration outage |
| **P2 — High** | Important function broken for one team/branch or high-value case blocked | Quote failure in one region, printing unavailable for many users |
| **P3 — Medium** | Single-user or limited issue, workaround available | One user cannot upload, printer setup issue |
| **P4 — Low** | Routine request or cosmetic issue | Access request, minor display issue, standard config |

### ITO first-line SLA targets

| Term | Meaning |
|---|---|
| **Response time** | Time from ticket creation to first meaningful human contact with the user (not an auto-acknowledgment) |
| **Escalation time** | Time from ticket creation to qualified handoff to L2/resolver group (with evidence, diagnosis, and context) |
| **Resolution time** | Time from ticket creation to confirmed resolution (service restored or request fulfilled) |
| **Business hours** | The agreed operating hours for ITO support (e.g., Mon–Fri 08:00–18:00, or as defined) |

| Priority | Response | Escalation (if L1 cannot resolve) | L1 Resolution / Workaround | Measurement |
|---|---|---|---|---|
| **P1** | **15 minutes** | **30 minutes** | **4 hours** | Clock time (24/7 if on-call exists, otherwise business hours) |
| **P2** | **30 minutes** | **1 hour** | **8 business hours** | Business hours |
| **P3** | **2 business hours** | **4 business hours** | **2 business days** | Business hours |
| **P4** | **4 business hours** | **1 business day** | **5 business days** | Business hours |

### Service request fulfillment targets

| Request type | Fulfillment target |
|---|---|
| Password reset / account unlock | **1 business hour** |
| MFA issue | **2 business hours** |
| New user access (with approved request) | **1 business day** |
| Role/profile change | **1 business day** |
| Device setup / replacement | **3 business days** |
| Software installation | **2 business days** |
| Standard report access | **2 business days** |

### SLA boundary conditions

- **Resolution SLA applies to what ITO controls.** If ITO escalates to L2 or a vendor, the L1 resolution clock pauses. ITO's SLA covers response, initial diagnosis, escalation quality, and user communication. End-to-end resolution depends on resolver groups — ITO tracks and reports total elapsed time but does not solely control it.
- **Cross-team tickets.** The response SLA still applies to the first-receiving team. The 15-minute triage rule from the No-Bounce Protocol applies. Transfer to the other team resets the resolution clock for the receiving team, but total elapsed time is still tracked.

---

## 8) Suggested operating workflow

1. Frontline user raises ticket or calls helpdesk
2. IT Operation records the issue
3. IT Operation checks:
   - is it access?
   - is it device/environment?
   - is it a technical failure (break/fix)?
   - is it a known incident?
   - is it a business/usage question?
4. IT Operation either:
   - resolves immediately,
   - provides workaround,
   - routes to Operation Department L1 (with context, as warm handoff),
   - escalates to L2/app/infrastructure/security/vendor
   - moves to shared triage queue if ownership is unclear (No-Bounce Protocol)
5. IT Operation updates the frontline until closure
6. Recurring issues become KB articles, problem records, or change inputs

This workflow matches standard service desk and incident/request fulfillment practices.  [oai_citation:18‡docs.microfocus.com](https://docs.microfocus.com/SM/9.52/Hybrid/Content/BestPracticesGuide_PD/SeviceDeskBestPractice_streamlined/The_service_desk_within_the_ITIL_framework.htm)

---

## 9) Minimum capabilities IT Operation should have

To support frontline sales effectively, IT Operation should have:

- ticketing tool / service portal
- service catalog
- clear routing rules
- user communication templates
- knowledge base
- monitoring / alerting visibility
- resolver group matrix
- contact list for L2 / vendor / business operations
- release calendar / maintenance calendar
- SLA definitions and measurement
- basic reporting dashboard
- shared triage queue with Operation Department (for cross-team issues)

These capabilities line up with standard service desk, request management, monitoring, and knowledge-management practices.  [oai_citation:19‡ServiceNow](https://www.servicenow.com/products/request-management.html?utm_source=chatgpt.com)

---

## 10) Conclusion

In most companies, **IT Operation can absolutely support the frontline**, but the support should be defined as:

> **technical frontline enablement and first-line service support**

not as:

> **owner of all frontline problems**

The model is:
- **IT Operation** for technical support, access, break/fix, incidents, monitoring, communication, and escalation
- **Operation Department** for product/business expertise, system usage guidance, and decision support

Between the two, a **No-Bounce Protocol** ensures that no frontline user is ever bounced without a resolution path — the team that receives the ticket owns it until the other team accepts it.

That split is consistent with normal service desk and tiered support practice, where first-line teams act as the single contact point, resolve common technical issues, and route specialized matters to the correct expert team.  [oai_citation:20‡ServiceNow](https://www.servicenow.com/products/itsm/what-is-a-service-desk.html)
