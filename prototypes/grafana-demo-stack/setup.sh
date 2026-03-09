#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLUSTER_NAME="grafana-demo"
MONITORING_NS="monitoring"
HELM_RELEASE="monitoring"
DASHBOARD_SRC="$SCRIPT_DIR/../../solutions/dashboards/grafana-dashboard.json"

# name:namespace:error_rate:latency_base_ms:latency_jitter_ms:replicas:traffic_rps
SYSTEMS=(
  "system-a:system-a-prod:0.01:30:15:3:10"
  "system-b:system-b-prod:0.03:80:40:3:5"
  "system-c:system-c-prod:0.05:150:80:2:3"
  "system-d:system-d-prod:0.08:60:50:2:2"
)

echo "=========================================="
echo " Grafana Demo Stack Setup"
echo "=========================================="
echo ""

# --- Step 1: Kind cluster ---
echo "[1/6] Creating Kind cluster '${CLUSTER_NAME}'..."
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "  Cluster already exists, reusing."
else
  kind create cluster --name "$CLUSTER_NAME" --config "$SCRIPT_DIR/kind-config.yaml"
fi
kubectl cluster-info --context "kind-${CLUSTER_NAME}" >/dev/null 2>&1

# --- Step 2: Build and load app image ---
echo "[2/6] Building metrics-app image..."
docker build -t metrics-app:latest "$SCRIPT_DIR/app/" --quiet
echo "  Loading image into Kind..."
kind load docker-image metrics-app:latest --name "$CLUSTER_NAME"

# --- Step 3: kube-prometheus-stack ---
echo "[3/6] Installing kube-prometheus-stack (takes ~2-3 min)..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts --force-update >/dev/null 2>&1
helm repo update >/dev/null 2>&1
kubectl create namespace "$MONITORING_NS" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
helm upgrade --install "$HELM_RELEASE" prometheus-community/kube-prometheus-stack \
  --namespace "$MONITORING_NS" \
  --values "$SCRIPT_DIR/grafana/helm-values.yaml" \
  --wait --timeout 5m

# --- Step 4: Deploy sample apps ---
echo "[4/6] Deploying sample apps to 4 namespaces..."
for sys in "${SYSTEMS[@]}"; do
  IFS=':' read -r name namespace error_rate latency_base latency_jitter replicas traffic_rps <<< "$sys"
  echo "  -> ${name} (${namespace}) replicas=${replicas} err=${error_rate} lat=${latency_base}+-${latency_jitter}ms rps=${traffic_rps}"
  sed -e "s/__SYSTEM__/${name}/g" \
      -e "s/__NAMESPACE__/${namespace}/g" \
      -e "s/__ERROR_RATE__/${error_rate}/g" \
      -e "s/__LATENCY_BASE__/${latency_base}/g" \
      -e "s/__LATENCY_JITTER__/${latency_jitter}/g" \
      -e "s/__REPLICAS__/${replicas}/g" \
      -e "s/__TRAFFIC_RPS__/${traffic_rps}/g" \
      "$SCRIPT_DIR/k8s/app-template.yaml" | kubectl apply -f -
done

# --- Step 5: Provision dashboard ---
echo "[5/6] Provisioning Grafana dashboard..."
python3 "$SCRIPT_DIR/adapt-dashboard.py" "$DASHBOARD_SRC" > /tmp/_grafana-demo-dashboard.json

kubectl create configmap grafana-dashboard-eks \
  --from-file=eks-platform-observability.json=/tmp/_grafana-demo-dashboard.json \
  --namespace "$MONITORING_NS" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl label configmap grafana-dashboard-eks \
  grafana_dashboard=1 \
  --namespace "$MONITORING_NS" --overwrite

rm -f /tmp/_grafana-demo-dashboard.json

# Restart Grafana so the sidecar picks up the new ConfigMap
kubectl rollout restart deployment "${HELM_RELEASE}-grafana" -n "$MONITORING_NS" >/dev/null

# --- Step 6: Wait for readiness ---
echo "[6/6] Waiting for pods..."
echo "  Grafana..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana \
  -n "$MONITORING_NS" --timeout=120s >/dev/null 2>&1

for sys in "${SYSTEMS[@]}"; do
  IFS=':' read -r name namespace _ <<< "$sys"
  echo "  ${name}..."
  kubectl rollout status deployment/metrics-app -n "$namespace" --timeout=60s >/dev/null 2>&1 || true
done

echo ""
echo "=========================================="
echo " Setup Complete"
echo "=========================================="
echo ""
echo " Start port-forward (run in another terminal):"
echo "   kubectl port-forward svc/${HELM_RELEASE}-grafana 3000:80 -n ${MONITORING_NS}"
echo ""
echo " Open in browser:"
echo "   Dashboard : http://localhost:3000/d/eks-platform-observability"
echo "   TV Mode   : http://localhost:3000/d/eks-platform-observability?kiosk"
echo "   Login     : admin / admin"
echo ""
echo " Metrics need ~2 minutes to start flowing."
echo ""
