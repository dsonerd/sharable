# Grafana TV Dashboard — Technical Feasibility Review

## Data Sources (EKS Stack)

| Source | Purpose |
|--------|---------|
| Prometheus (AMP or self-hosted) | Application & container metrics |
| kube-state-metrics | Pod status, deployment replicas, node conditions |
| cAdvisor (kubelet) | Container CPU / memory usage |
| CloudWatch | EKS control plane, ALB, RDS (if applicable) |
| Alertmanager | Alert state (firing / resolved) |

---

## Column-by-Column Feasibility

### 1. Health Status — NEEDS REWORK

**Mock shows:** Animated pulsing dot + "HEALTHY" text + pod count

**Problem:**
- No single "health" metric exists. "Health" is a composite concept.
- Animated pulsing CSS dots are NOT possible in native Grafana.
- Grafana Stat panel cannot render a colored dot above the value.

**What Grafana CAN do:**
- **Stat panel** with value mappings: query `kube_deployment_status_replicas_ready / kube_deployment_status_replicas` → map 1 = "HEALTHY", <1 = "DEGRADED", 0 = "DOWN"
- Thresholds drive the value color (green/yellow/red) — this works natively.
- Pod count as description text → NOT directly supported in Stat panel. Would need a separate panel or use the stat panel's "Name" field override.

**Revised approach:**
- Use **Stat panel** showing pod readiness ratio with value mappings.
- OR use **Polystat panel** (community plugin) which shows a colored hexagon per system — better for health-at-a-glance.
- Drop the animated dot — Grafana cannot do CSS animations.

---

### 2. Uptime / SLA — PARTIALLY ACHIEVABLE

**Mock shows:** Circular gauge ring with 99.97%, SLA target line, "MET/BREACH" label

**Problems:**
- Grafana **Gauge panel** renders a semicircle (180°), not a full ring (360°). The mock's full-circle ring is not a native Grafana visualization.
- "MET/BREACH" conditional text below the gauge — not natively possible. Grafana thresholds change color, not text labels.
- SLA is typically calculated over 30 days. Showing "last 1h" uptime is misleading for SLA. Need to decide: is this instantaneous availability or rolling SLA?

**What Grafana CAN do:**
- **Gauge panel** (semicircle arc) with thresholds at SLA target — works perfectly.
- Use `avg_over_time(up{job="system-a"}[30d])` or synthetic monitoring probe success rate for the value.
- Thresholds: green ≥ 99.95, red < 99.95 — colors the gauge natively.

**Revised approach:**
- Use Grafana's native **Gauge panel** (semicircle). Accept it won't be a full ring.
- Drop "MET/BREACH" text — let the color tell the story (green = met, red = breach).
- Use a 30-day window for the query regardless of dashboard time range (use `$__range` override or hardcode).

---

### 3. Latency P95 — FULLY ACHIEVABLE ✓

**Mock shows:** Big number + unit + P50 subtitle + trend arrow + sparkline

**Grafana reality:**
- **Stat panel** with sparkline background — native since Grafana 9.
- Query: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{namespace="system-a"}[5m])) by (le))`
- Sparkline renders automatically from the time series data.
- Thresholds: green <100ms, yellow <500ms, red ≥500ms — native.

**Issues:**
- P50 as secondary text — Stat panel doesn't support a second query as subtitle. Would need a separate panel or accept showing only P95.
- Trend arrows ("rising"/"falling") — NOT native. Grafana Stat can show a percentage change with "Graph mode: Area" but not custom trend text.
- The bottom threshold color bar — not native Grafana. Thresholds change the value/background color, not add a footer bar.

**Revised approach:**
- **Stat panel** with graph mode = area (sparkline) — keep this.
- Drop P50 subtitle and trend arrows.
- Rely on sparkline direction + value color for trend information.

---

### 4. Error Rate — FULLY ACHIEVABLE ✓

**Mock shows:** Percentage + sparkline + trend arrow

**Grafana reality:**
- Same as latency — **Stat panel** with sparkline.
- Query: `sum(rate(http_requests_total{status=~"5..", namespace="system-a"}[5m])) / sum(rate(http_requests_total{namespace="system-a"}[5m])) * 100`
- Thresholds for coloring — native.

**Issues:**
- Same as latency: trend arrows and subtitle text not natively supported.
- Bottom threshold bar — not native.

**Revised approach:**
- **Stat panel** with sparkline. Drop trend text. Drop bottom bar.

---

### 5. Throughput — FULLY ACHIEVABLE ✓

**Mock shows:** Big number (RPM) + sparkline + trend

**Grafana reality:**
- **Stat panel** with sparkline.
- Query: `sum(rate(http_requests_total{namespace="system-a"}[5m])) * 60`
- Unit override: set to "rpm" or "reqps" in field config.

**Issues:**
- Same trend arrow issue — drop it.

**Revised approach:**
- **Stat panel** with sparkline. Clean and simple.

---

### 6. Resources (CPU / Memory) — NEEDS REWORK

**Mock shows:** Two horizontal progress bars (CPU + Memory) with labels in one panel

**Problems:**
- Grafana has **Bar Gauge panel** which can show horizontal bars — but it renders all queries as stacked bars in the same visual style, not as two labeled rows with percentage text on the right.
- You cannot put custom labels like "CPU" / "Memory" to the left of each bar inside a Bar Gauge — it uses the series name.
- Having two distinct bar gauges with different thresholds in one panel is awkward.

**What Grafana CAN do:**
- **Bar Gauge panel** (horizontal, LCD mode or basic mode) with two queries:
  - CPU: `sum(rate(container_cpu_usage_seconds_total{namespace="system-a"}[5m])) / sum(kube_pod_container_resource_limits{resource="cpu", namespace="system-a"}) * 100`
  - Memory: `sum(container_memory_working_set_bytes{namespace="system-a"}) / sum(kube_pod_container_resource_limits{resource="memory", namespace="system-a"}) * 100`
- Series names become the bar labels — rename queries to "CPU" and "Memory" using alias.
- Thresholds apply to ALL bars equally (can't have different thresholds per query in one panel).

**Revised approach:**
- **Bar Gauge panel** in horizontal/basic mode. Two queries aliased "CPU" and "Memory".
- Accept that both bars share the same threshold config (60/80 works for both anyway).
- OR split into two separate **Stat panels** (1 for CPU, 1 for Memory) — but this doubles the column count.

---

### 7. Active Alerts — NEEDS REWORK

**Mock shows:** Big number + severity breakdown badges (P1/P2/P3)

**Problems:**
- Grafana can query Alertmanager for alert counts using the Alertmanager datasource.
- But: the severity breakdown badges (P1, P2, P3 with colored backgrounds) inside a Stat panel are NOT possible. Stat panel shows a single value, not inline badges.
- You'd need a **Table panel** to show breakdown, which looks completely different.

**What Grafana CAN do:**
- **Stat panel** showing total firing alerts: `count(ALERTS{alertstate="firing", namespace="system-a"})` — just the number.
- Color via threshold (0=green, 1+=yellow, any critical=red) — but Grafana thresholds are value-based, not label-based. Can't color by severity.
- **Alternative:** Use `ALERTS{alertstate="firing", namespace="system-a", severity="critical"}` as query and show only critical alert count — simpler and more actionable for leadership.

**Revised approach:**
- Show **critical alert count only** as a Stat panel — this is what leadership cares about.
- If you need breakdown, use a **Table panel** with severity column — but it takes more space and doesn't fit the "big number at a glance" pattern.
- OR show the total count with the threshold tied to "any critical firing" using a separate query.

---

### Row Headers — NEEDS REWORK

**Mock shows:** Grafana collapsible row with health tag, cluster info, pod count inline

**Problem:**
- Grafana row headers only support a **title string**. No tags, no colored badges, no pod counts, no metadata inline.
- They are just collapsible section dividers.

**Revised approach:**
- Row title: `"System A — eks-prod-apse1"` (plain text, that's all you get).
- Move any metadata (pod count, health tag) into the panels themselves.

---

### Bottom Threshold Bars — NOT POSSIBLE

The mock shows a 3px colored bar at the bottom of every panel matching the threshold color.

- Grafana does NOT render colored bars at panel bottoms.
- Thresholds change the **value text color** or **panel background color** — not a footer stripe.
- Drop this from the design entirely.

---

### Three-dot Menu on Panels

The mock shows `⋮` menu appearing on hover.

- This IS native Grafana behavior ✓ — panels have a dropdown menu on hover.

---

## Revised Achievable Design

```
ROW: System A — eks-prod-apse1
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Health       │ Uptime       │ Latency P95  │ Error Rate   │ Throughput   │ CPU / Mem    │ Crit Alerts  │
│              │              │              │              │              │              │              │
│   Stat       │   Gauge      │   Stat       │   Stat       │   Stat       │  Bar Gauge   │   Stat       │
│  "HEALTHY"   │  ╭───╮       │   42ms       │   0.02%      │   3.4K rpm   │  CPU ██░ 45% │     0        │
│  12/12 pods  │  │99.97│     │   ~~~~       │   ~~~~       │   ~~~~       │  MEM ███ 62% │  "ALL CLEAR" │
│  [green]     │  ╰───╯       │   [green]    │   [green]    │   [blue]     │  [green]     │  [green]     │
│              │  [green]     │              │              │              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### Panel Type Summary

| Column | Grafana Panel Type | Visualization | Notes |
|--------|--------------------|---------------|-------|
| Health | Stat | Value mapping | Map pod ratio → text |
| Uptime | Gauge | Semicircle arc | 30-day rolling window |
| Latency P95 | Stat + sparkline | Big number + area | Drop P50 subtitle |
| Error Rate | Stat + sparkline | Big number + area | Drop trend text |
| Throughput | Stat + sparkline | Big number + area | Drop trend text |
| CPU / Memory | Bar Gauge | Horizontal bars | Two queries, shared thresholds |
| Critical Alerts | Stat | Big number | Show critical count only |

### What We Dropped From the Mock

1. ~~Animated pulsing dots~~ → Not possible in Grafana
2. ~~Full-circle SLA ring~~ → Grafana gauge is semicircle only
3. ~~"MET/BREACH" text~~ → Threshold colors tell the story
4. ~~P50 subtitle~~ → Stat panel doesn't support secondary values
5. ~~Trend arrows ("rising"/"falling")~~ → Not native; sparkline shows trend
6. ~~Bottom threshold color bars~~ → Not a Grafana feature
7. ~~Row header badges/tags/metadata~~ → Rows only support title text
8. ~~Severity breakdown badges (P1/P2/P3)~~ → Stat panel shows one value only
9. ~~Custom colored dots in panels~~ → Not available in Stat/Gauge panels

### What We Keep

1. ✓ Dark theme (native Grafana dark)
2. ✓ Left sidebar (native, collapsed mode)
3. ✓ Top navbar with breadcrumbs (native)
4. ✓ TV / Kiosk mode (native `?kiosk` parameter)
5. ✓ Time picker + auto-refresh (native)
6. ✓ Stat panels with sparkline backgrounds (native since Grafana 9)
7. ✓ Gauge panel for SLA (native, semicircle)
8. ✓ Bar Gauge for resources (native)
9. ✓ Threshold-driven coloring (native)
10. ✓ Panel hover menu (native)
11. ✓ Collapsible row headers (native, title only)
12. ✓ Value mappings (number → "HEALTHY" text) (native)

---

## TV Readability Considerations (55-inch at 3-5m)

- 28 panels on screen is dense. At 5m viewing distance, text below 18px will be hard to read.
- Consider reducing to **5 columns** if readability is an issue:
  - Health + Uptime (merge into one gauge)
  - Latency
  - Error Rate
  - Throughput
  - Alerts
- Resources can go to a separate "drill-down" dashboard (not TV-facing).

---

## PromQL Quick Reference for Implementation

```promql
# Health (pod readiness ratio)
kube_deployment_status_replicas_ready{namespace="$namespace"}
  / kube_deployment_status_replicas{namespace="$namespace"}

# Uptime (30-day probe success)
avg_over_time(probe_success{job="$system"}[30d]) * 100

# Latency P95
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket{namespace="$namespace"}[5m])) by (le))

# Error Rate
sum(rate(http_requests_total{namespace="$namespace", status=~"5.."}[5m]))
  / sum(rate(http_requests_total{namespace="$namespace"}[5m])) * 100

# Throughput (RPM)
sum(rate(http_requests_total{namespace="$namespace"}[5m])) * 60

# CPU Usage %
sum(rate(container_cpu_usage_seconds_total{namespace="$namespace"}[5m]))
  / sum(kube_pod_container_resource_limits{namespace="$namespace", resource="cpu"}) * 100

# Memory Usage %
sum(container_memory_working_set_bytes{namespace="$namespace"})
  / sum(kube_pod_container_resource_limits{namespace="$namespace", resource="memory"}) * 100

# Critical Alerts Firing
count(ALERTS{alertstate="firing", namespace="$namespace", severity="critical"}) OR vector(0)
```
