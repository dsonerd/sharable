#!/usr/bin/env python3
"""Adapt the Grafana dashboard JSON for Kubernetes provisioning.

Transforms the portable import-format dashboard into one that works
with Grafana's file-based provisioning (sidecar ConfigMap):
  1. Removes __inputs / __requires (import-UI only)
  2. Replaces ${DS_PROMETHEUS} with a known datasource UID
  3. Shortens [30d] SLA window to [5m] (no history in fresh demo)
  4. Removes job= filter from up{} queries (ServiceMonitor job names differ)
"""

import json
import sys


def fix_datasources(obj):
    """Recursively replace ${DS_PROMETHEUS} with the provisioned UID."""
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key == "datasource" and isinstance(val, dict):
                if val.get("uid") == "${DS_PROMETHEUS}":
                    val["uid"] = "prometheus"
            else:
                fix_datasources(val)
    elif isinstance(obj, list):
        for item in obj:
            fix_datasources(item)


def fix_queries(dashboard):
    """Fix PromQL expressions for the demo environment."""
    job_map = {
        'job="system-a", namespace="system-a-prod"': 'namespace="system-a-prod"',
        'job="system-b", namespace="system-b-prod"': 'namespace="system-b-prod"',
        'job="system-c", namespace="system-c-prod"': 'namespace="system-c-prod"',
        'job="system-d", namespace="system-d-prod"': 'namespace="system-d-prod"',
    }
    for panel in dashboard.get("panels", []):
        for target in panel.get("targets", []):
            expr = target.get("expr", "")
            # Shorten 30d window
            expr = expr.replace("[30d]", "[5m]")
            # Remove job= filter from up{} queries
            for old, new in job_map.items():
                expr = expr.replace(old, new)
            target["expr"] = expr


def adapt(input_path):
    with open(input_path) as f:
        dashboard = json.load(f)

    # Strip import-only fields
    dashboard.pop("__inputs", None)
    dashboard.pop("__requires", None)

    fix_datasources(dashboard)
    fix_queries(dashboard)

    return dashboard


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input-dashboard.json>", file=sys.stderr)
        sys.exit(1)

    result = adapt(sys.argv[1])
    json.dump(result, sys.stdout, indent=2)
    print()
