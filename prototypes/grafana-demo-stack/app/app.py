"""Minimal HTTP server that exposes Prometheus metrics for demo purposes.

Generates self-traffic so metrics flow immediately after deployment.
Configurable via environment variables:
  ERROR_RATE       - probability of 5xx response (default 0.02)
  LATENCY_BASE_MS  - base latency in ms (default 30)
  LATENCY_JITTER_MS - jitter range in ms (default 20)
  TRAFFIC_RPS      - self-generated requests per second (default 5)
"""

import os
import random
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# --- Prometheus metrics (exact names the dashboard expects) ---

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "handler", "status"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 10.0],
)

REQUEST_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "handler", "status"],
)

# --- Configuration from environment ---

ERROR_RATE = float(os.getenv("ERROR_RATE", "0.02"))
LATENCY_BASE = float(os.getenv("LATENCY_BASE_MS", "30")) / 1000.0
LATENCY_JITTER = float(os.getenv("LATENCY_JITTER_MS", "20")) / 1000.0
TRAFFIC_RPS = float(os.getenv("TRAFFIC_RPS", "5"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            output = generate_latest()
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(output)
            return

        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        # Simulate latency
        latency = max(0.001, LATENCY_BASE + random.uniform(-LATENCY_JITTER, LATENCY_JITTER))
        # Occasional spike (1% chance)
        if random.random() < 0.01:
            latency += random.uniform(0.5, 2.0)
        time.sleep(latency)

        # Simulate errors
        if random.random() < ERROR_RATE:
            status = random.choice([500, 502, 503])
        else:
            status = 200

        REQUEST_DURATION.labels(method="GET", handler="/", status=str(status)).observe(latency)
        REQUEST_TOTAL.labels(method="GET", handler="/", status=str(status)).inc()

        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"status={status}\n".encode())

    def log_message(self, format, *args):
        pass  # suppress access logs


def traffic_generator():
    """Background thread that generates self-traffic."""
    time.sleep(5)  # wait for server to start
    interval = 1.0 / max(0.1, TRAFFIC_RPS)
    while True:
        try:
            urllib.request.urlopen("http://localhost:8080/", timeout=10)
        except Exception:
            pass
        time.sleep(interval)


if __name__ == "__main__":
    t = threading.Thread(target=traffic_generator, daemon=True)
    t.start()

    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print(
        f"metrics-app listening on :8080 "
        f"(error_rate={ERROR_RATE:.0%}, "
        f"latency={LATENCY_BASE*1000:.0f}+/-{LATENCY_JITTER*1000:.0f}ms, "
        f"self_traffic={TRAFFIC_RPS:.0f}rps)"
    )
    server.serve_forever()
