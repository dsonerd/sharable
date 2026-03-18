# AWS Cost Explorer Budget Reporting Script

## Topic Decomposition

Breaking this problem into sub-areas using **functional decomposition**:

| # | Sub-area | Description |
|---|----------|-------------|
| 1 | **API Strategy** | How to call AWS Cost Explorer API cost-efficiently (single call) |
| 2 | **Library Constraint** | What "default library" means in a strict environment |
| 3 | **Cost Pool Mapping** | How to define account-to-cost-pool relationships |
| 4 | **Data Processing** | Transform raw API response into cost-pool-grouped data |
| 5 | **Output Format** | CSV structure and generation |
| 6 | **CLI Interface** | Parameters, validation, error handling |
| 7 | **Operational Concerns** | Credentials, logging, scheduling |

Completeness check: API call -> raw data -> mapping -> processing -> output. Plus: input params, config, error handling. Covered.

---

## Ideas per Sub-area

### 1. API Strategy — Single Call Optimization

The AWS Cost Explorer `GetCostAndUsage` API supports filtering by multiple accounts and grouping by `LINKED_ACCOUNT` in a single call. This is the key to the "call once, process locally" requirement.

**Idea A: Single call with GROUP_BY LINKED_ACCOUNT**
- Call `GetCostAndUsage` once with `GroupBy=[{"Type":"DIMENSION","Key":"LINKED_ACCOUNT"}]`
- Collect ALL account IDs from ALL cost pools into one filter
- API returns cost per account — script then maps accounts to cost pools locally
- Feasibility: High. This is the intended usage pattern.

**Idea B: Single call with NO filter, GROUP_BY LINKED_ACCOUNT**
- Don't filter by accounts at all — pull the entire org's cost grouped by account
- Map locally
- Feasibility: High. Simpler call but returns more data. Useful if the mapping covers most/all accounts anyway.
- Trade-off: May return data for accounts not in any cost pool. Slightly more data transferred but simpler API call.

**Idea C: Single call with GROUP_BY LINKED_ACCOUNT + SERVICE**
- Get cost broken down by account AND service in one call
- Allows more granular reporting if needed in the future
- Trade-off: More data, potentially paginated responses, more complex processing
- Feasibility: Medium. Over-engineering for current requirements.

**Recommendation: Idea A or B** depending on how many accounts are in the org vs. how many are mapped. If most accounts are mapped, go with B (simpler). If only a fraction, go with A (less data).

### 2. Library Constraint — "Default Library"

Critical clarification needed. Two interpretations:

**Interpretation 1: Python stdlib + boto3**
- In most AWS environments (Lambda, EC2 with AWS CLI, SSM), `boto3` is pre-installed
- "Strictly controlled" likely means "no pip install" but boto3 is already there
- This is the most common scenario
- Feasibility: High. boto3 is the natural choice.

**Interpretation 2: Pure Python stdlib only (no boto3)**
- Would require either:
  - **Option 2a**: Shell out to AWS CLI via `subprocess` — parse JSON response
  - **Option 2b**: Raw HTTP with SigV4 signing using `urllib`, `hmac`, `hashlib` (all stdlib)
- Option 2a is pragmatic; Option 2b is painful but possible
- Feasibility: 2a is Medium (depends on AWS CLI being installed), 2b is Low (complex, error-prone)

**Recommendation: Design for boto3 (Interpretation 1) with a fallback to subprocess+AWS CLI (Option 2a).** The script can detect boto3 availability and fall back:

```python
try:
    import boto3
    USE_BOTO3 = True
except ImportError:
    USE_BOTO3 = False  # fallback to subprocess + aws cli
```

### 3. Cost Pool Mapping

**Idea A: JSON mapping file**
```json
{
  "cost_pools": {
    "landingzone-prod": ["111111111111", "222222222222"],
    "landingzone-nonprod": ["333333333333"],
    "core-prod": ["444444444444", "555555555555"],
    "core-nonprod": ["666666666666"],
    "api-mgmt-prod": ["777777777777"],
    "api-mgmt-nonprod": ["888888888888"]
  }
}
```
- Pros: Standard format, parseable with `json` (stdlib), widely understood
- Cons: No comments allowed in JSON

**Idea B: CSV mapping file**
```csv
cost_pool,account_id,account_name
landingzone-prod,111111111111,lz-prod-network
landingzone-prod,222222222222,lz-prod-security
core-prod,444444444444,core-prod-main
```
- Pros: Editable in Excel, human-readable, supports extra metadata (account name)
- Cons: More verbose, requires parsing with `csv` module

**Idea C: INI/config file**
```ini
[landingzone-prod]
accounts = 111111111111, 222222222222

[landingzone-nonprod]
accounts = 333333333333
```
- Pros: Parseable with `configparser` (stdlib), supports comments
- Cons: Less structured than JSON for this use case

**Recommendation: Idea A (JSON)** — simplest, cleanest, stdlib-supported, matches the mental model described by the user ("cost_pool = [acc1, acc2, ...]").

### 4. Data Processing

**Flow:**
1. Load mapping file -> build reverse lookup: `{account_id: cost_pool_name}`
2. Call API -> get cost per account per time period
3. For each result, look up account -> cost pool
4. Aggregate (sum) costs by cost pool
5. Handle unmapped accounts (log warning, optionally include as "unmapped")

**Granularity considerations:**
- **Monthly totals**: One row per cost pool, single amount column. Simplest.
- **Daily breakdown within month**: One row per cost pool per day. More granular but may not be needed for budget reporting.
- **Monthly with service breakdown**: One row per cost pool per service. Useful for drill-down.

**Recommendation: Monthly totals per cost pool** (matches "this is use for month"). Optionally support daily if the date range spans multiple months.

### 5. Output Format — CSV Structure

**Option A: Simple flat CSV**
```csv
cost_pool,start_date,end_date,amount,currency
landingzone-prod,2026-01-01,2026-02-01,12345.67,USD
landingzone-nonprod,2026-01-01,2026-02-01,3456.78,USD
core-prod,2026-01-01,2026-02-01,8901.23,USD
```
- Pros: Simple, easy to import into any tool
- Good for single-month reports

**Option B: Pivot-style CSV (multi-month)**
```csv
cost_pool,2026-01,2026-02,2026-03
landingzone-prod,12345.67,13000.00,12800.00
landingzone-nonprod,3456.78,3600.00,3500.00
```
- Pros: Compact for multi-month comparison
- Cons: Dynamic columns, harder to parse programmatically

**Option C: Detailed CSV with account breakdown**
```csv
cost_pool,account_id,start_date,end_date,amount,currency
landingzone-prod,111111111111,2026-01-01,2026-02-01,8000.00,USD
landingzone-prod,222222222222,2026-01-01,2026-02-01,4345.67,USD
```
- Pros: Full traceability
- Cons: More rows, harder to read for budget summary

**Recommendation: Option A as default.** Consider adding a `--detail` flag for Option C if needed later. Option B is nice but harder to produce with stdlib `csv` writer.

### 6. CLI Interface

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--start-date` | YYYY-MM-DD | Yes | Start of billing period |
| `--end-date` | YYYY-MM-DD | Yes | End of billing period |
| `--mapping` | file path | No | Path to mapping JSON (default: `cost_pool_mapping.json`) |
| `--output` | file path | No | Output CSV path (default: stdout or auto-named) |
| `--profile` | string | No | AWS profile name |
| `--region` | string | No | AWS region (default: us-east-1, Cost Explorer is global) |

Use `argparse` (stdlib). No external dependencies needed.

**Date validation:**
- Ensure start < end
- Cost Explorer requires dates as YYYY-MM-DD
- For monthly reporting, typical usage: `--start-date 2026-01-01 --end-date 2026-02-01` (exclusive end date, matching AWS API convention)

### 7. Operational Concerns

**Credentials:**
- Rely on standard AWS credential chain (env vars, ~/.aws/credentials, instance profile)
- Never hardcode credentials in the script
- Support `--profile` for multi-account setups (management account or delegated access)

**AWS Cost Explorer access:**
- Cost Explorer API must be called from the **management account** (or a delegated administrator account)
- IAM permission needed: `ce:GetCostAndUsage`
- Cost Explorer API has its own cost: **$0.01 per API request** — hence the "call once" optimization

**Logging:**
- Use `logging` module (stdlib)
- Log: API call parameters, number of results, unmapped accounts, total cost per pool
- Output logs to stderr so stdout can be piped for CSV

---

## Top Candidates — Trade-off Summary

### Candidate 1: boto3 + JSON mapping + flat CSV (Recommended)

| Criterion | Assessment |
|-----------|------------|
| Simplicity | High — straightforward boto3 call, JSON load, CSV write |
| Stdlib compliance | Near-complete — only external dep is boto3 (typically pre-installed) |
| Cost optimization | Excellent — single API call ($0.01) |
| Maintainability | High — mapping file is easy to update |
| Extensibility | Good — easy to add service breakdown, multi-month pivot |
| Reversibility | Two-way door — easy to change approach |

**What you give up:** Pure stdlib; requires boto3.

### Candidate 2: subprocess + AWS CLI + JSON mapping + flat CSV

| Criterion | Assessment |
|-----------|------------|
| Simplicity | Medium — subprocess parsing adds complexity |
| Stdlib compliance | Full — 100% stdlib |
| Cost optimization | Excellent — single CLI call |
| Maintainability | Medium — fragile if CLI output format changes |
| Extensibility | Lower — harder to add features cleanly |
| Reversibility | Two-way door |

**What you give up:** Clean API interface; dependent on AWS CLI being installed and configured.

### Candidate 3: Dual-mode (boto3 with CLI fallback)

| Criterion | Assessment |
|-----------|------------|
| Simplicity | Lower — two code paths |
| Stdlib compliance | Full in fallback mode |
| Cost optimization | Excellent |
| Maintainability | Lower — two paths to maintain |
| Extensibility | Medium |
| Reversibility | Two-way door |

**What you give up:** Simplicity. Two code paths means double the testing surface.

### Verdict

**Go with Candidate 1 (boto3).** If boto3 is truly unavailable, pivot to Candidate 2 (subprocess+CLI). Do NOT build Candidate 3 — it's over-engineering. Pick one and commit to it.

---

## Risk Assessment

| Risk | Likelihood | Impact | Response |
|------|-----------|--------|----------|
| boto3 not available in environment | Medium | High | **Mitigate**: Verify before development. If unavailable, use subprocess+CLI approach. |
| Cost Explorer not enabled on the account | Low | High | **Mitigate**: Document prerequisite. Script should detect and give clear error. |
| Paginated API response (many accounts) | Low | Medium | **Mitigate**: Handle `NextPageToken` in the API call loop. Single logical call but may need pagination. |
| Unmapped accounts inflate "missing" bucket | Medium | Low | **Mitigate**: Log warnings for unmapped accounts. Optionally add "unmapped" cost pool. |
| Date format confusion (inclusive vs exclusive) | Medium | Medium | **Mitigate**: Follow AWS convention (end date is exclusive). Document clearly. Add validation. |
| Script run from wrong account (not management) | Medium | High | **Mitigate**: Clear error message when `AccessDeniedException` occurs. Document that it must run from management or delegated admin account. |
| Cost Explorer API cost ($0.01/request) | Low | Low | **Accept**: $0.01 per run is negligible. Single-call design already optimized. |

### Cascading risk
If boto3 is unavailable AND AWS CLI is not installed -> script cannot function at all. **Pre-mortem**: verify the environment has at least one of these before investing development time.

---

## Creative Challenges

### Assumption Audit

1. **Assumption: The mapping is static.** What if accounts are added/removed frequently? Consider: should the script auto-discover accounts from AWS Organizations and flag unmapped ones?

2. **Assumption: Monthly granularity is sufficient.** What if finance needs daily amortization for accrual-based accounting? The API supports `DAILY` granularity — worth exposing as an option.

3. **Assumption: Costs are only grouped by account.** What if a single account hosts workloads for multiple cost pools (e.g., shared services account)? This breaks the account-based mapping model. Would need tag-based allocation instead.

### Devil's Advocate

**Against the script approach entirely:** AWS Budgets + AWS Cost and Usage Report (CUR) already exists. CUR delivers detailed billing data to S3 daily. Why build a custom script?

Counter-argument: CUR is massive (GB-level CSVs), requires Athena/Glue to query, and has setup overhead. For a simple monthly cost pool summary, a lightweight script calling Cost Explorer is the right tool. CUR is overkill for this use case.

**Against JSON mapping:** If you already have AWS Organizations with OUs structured by cost pool, you could derive the mapping dynamically. But this adds complexity and requires Organizations API access.

### Unasked Questions

1. **Who runs this script and where?** Local laptop? A scheduled Lambda? An EC2 instance? This affects credential management and scheduling.

2. **Does anyone need to approve or review the output before it goes to finance?** If yes, consider emailing the CSV or posting to a shared location.

3. **Should the script compare current cost against budget targets?** A budget reporting script that only reports actuals without comparing to budget limits is half the picture.

4. **What about credits, refunds, and tax?** Cost Explorer can return `UnblendedCost`, `BlendedCost`, `AmortizedCost`, or `NetAmortizedCost`. Which metric does finance expect?

5. **Multi-currency?** If accounts are in different billing currencies, costs need normalization.

### The Simplest Version

The absolute minimum viable script:

```
~80 lines of Python:
- argparse for dates + mapping file
- json.load for mapping
- boto3 ce.get_cost_and_usage() with GroupBy LINKED_ACCOUNT
- dict comprehension to sum by cost pool
- csv.writer to stdout
```

No classes, no frameworks, no config complexity. Just a function that reads, calls, maps, and writes. This is the right starting point — add complexity only when proven necessary.

---

## Proposed Script Architecture

```
aws-cost-report.py          # Single script file (~100-150 lines)
cost_pool_mapping.json       # Mapping configuration

Usage:
  python aws-cost-report.py \
    --start-date 2026-01-01 \
    --end-date 2026-02-01 \
    --mapping cost_pool_mapping.json \
    --output cost_report_2026_01.csv
```

### Mapping File Template

```json
{
  "cost_pools": {
    "landingzone-prod": {
      "accounts": ["111111111111", "222222222222"],
      "description": "Landing Zone Production accounts"
    },
    "landingzone-nonprod": {
      "accounts": ["333333333333"],
      "description": "Landing Zone Non-Production accounts"
    },
    "core-prod": {
      "accounts": ["444444444444", "555555555555"],
      "description": "Core Platform Production"
    },
    "core-nonprod": {
      "accounts": ["666666666666"],
      "description": "Core Platform Non-Production"
    },
    "api-mgmt-prod": {
      "accounts": ["777777777777"],
      "description": "API Management Production"
    },
    "api-mgmt-nonprod": {
      "accounts": ["888888888888"],
      "description": "API Management Non-Production"
    }
  }
}
```

### Output CSV Template

```csv
cost_pool,start_date,end_date,amount,currency
landingzone-prod,2026-01-01,2026-02-01,12345.67,USD
landingzone-nonprod,2026-01-01,2026-02-01,3456.78,USD
core-prod,2026-01-01,2026-02-01,8901.23,USD
core-nonprod,2026-01-01,2026-02-01,4567.89,USD
api-mgmt-prod,2026-01-01,2026-02-01,2345.67,USD
api-mgmt-nonprod,2026-01-01,2026-02-01,1234.56,USD
```

---

## Next Steps

1. **Clarify**: Confirm boto3 is available in the target environment
2. **Clarify**: Which cost metric? (UnblendedCost vs AmortizedCost vs NetAmortizedCost)
3. **Clarify**: Where will this run? (local, Lambda, scheduled job)
4. **Build**: Start with the ~80-line minimal version
5. **Test**: With real mapping file against actual accounts
6. **Iterate**: Add features only when needed (daily granularity, service breakdown, budget comparison)
