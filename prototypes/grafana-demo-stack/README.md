# Grafana TV Dashboard — Demo Stack

Local demo of the EKS Platform Observability dashboard running on a Kind cluster.

## Quick Start

```bash
./setup.sh
```

Then in another terminal:

```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open http://localhost:3000/d/eks-platform-observability (admin / admin)

For TV mode: append `?kiosk` to the URL.

Metrics take ~2 minutes to populate after setup.

## What It Deploys

- **Kind cluster** (1 node) with kube-prometheus-stack (Prometheus, Grafana, kube-state-metrics)
- **4 namespaces** (`system-a-prod` through `system-d-prod`) each with a metrics app that generates self-traffic
- The Grafana dashboard from `solutions/dashboards/grafana-dashboard.json`, auto-adapted for provisioning

Each system has different characteristics:

| System | Replicas | Error Rate | Latency | Traffic |
|--------|----------|------------|---------|---------|
| A | 3 | 1% | 30ms | 10 rps/pod |
| B | 3 | 3% | 80ms | 5 rps/pod |
| C | 2 | 5% | 150ms | 3 rps/pod |
| D | 2 | 8% | 60ms | 2 rps/pod |

## Teardown

```bash
./teardown.sh
```

## Prerequisites

Docker, kind, kubectl, helm, python3.
