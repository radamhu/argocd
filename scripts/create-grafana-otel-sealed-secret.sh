#!/bin/bash

# ==============================================================================
# Create Grafana Cloud Sealed Secret for OTEL Collector
# ==============================================================================
#
# This script creates a sealed secret for Grafana Cloud credentials used by
# the OpenTelemetry Collector to export telemetry data.
#
# Prerequisites:
# - kubectl installed and configured
# - kubeseal installed (https://github.com/bitnami-labs/sealed-secrets)
# - sealed-secrets controller running in k3s cluster
# - Grafana Cloud account with OTLP access
#
# Usage:
#   ./create-grafana-otel-sealed-secret.sh
#
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${NAMESPACE:-default}"
SECRET_NAME="otel-collector-secret"
SEALED_SECRET_FILE="app/demo/dentari/otel-collector-sealed-secret.yaml"

echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}Grafana Cloud OTEL Collector - Sealed Secret Creator${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl not found. Please install kubectl.${NC}"
    exit 1
fi

if ! command -v kubeseal &> /dev/null; then
    echo -e "${RED}Error: kubeseal not found. Please install kubeseal.${NC}"
    echo "Install: https://github.com/bitnami-labs/sealed-secrets#kubeseal"
    exit 1
fi

# Check if sealed-secrets controller is running
if ! kubectl get deployment sealed-secrets-controller -n kube-system &> /dev/null; then
    echo -e "${RED}Error: sealed-secrets controller not found in cluster.${NC}"
    echo "Install it first: kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Get Grafana Cloud information
echo -e "${YELLOW}==================================================================${NC}"
echo -e "${YELLOW}Grafana Cloud Configuration${NC}"
echo -e "${YELLOW}==================================================================${NC}"
echo ""
echo "To get your Grafana Cloud OTLP credentials:"
echo "1. Go to: https://grafana.com/orgs/YOUR_ORG/stacks"
echo "2. Click on your stack"
echo "3. Go to: Connections → Add new connection → OpenTelemetry"
echo "4. Copy the Instance ID and generate a new API token"
echo ""

# Get endpoint
echo -e "${YELLOW}Enter Grafana Cloud OTLP endpoint:${NC}"
echo "Format: https://otlp-gateway-prod-{region}.grafana.net/otlp"
echo "Example: https://otlp-gateway-prod-eu-west-0.grafana.net/otlp"
read -r GRAFANA_ENDPOINT

if [[ -z "$GRAFANA_ENDPOINT" ]]; then
    echo -e "${RED}Error: Endpoint cannot be empty${NC}"
    exit 1
fi

# Get instance ID
echo ""
echo -e "${YELLOW}Enter Grafana Cloud Instance ID:${NC}"
read -r GRAFANA_INSTANCE_ID

if [[ -z "$GRAFANA_INSTANCE_ID" ]]; then
    echo -e "${RED}Error: Instance ID cannot be empty${NC}"
    exit 1
fi

# Get token
echo ""
echo -e "${YELLOW}Enter Grafana Cloud API Token:${NC}"
read -rs GRAFANA_TOKEN

if [[ -z "$GRAFANA_TOKEN" ]]; then
    echo -e "${RED}Error: Token cannot be empty${NC}"
    exit 1
fi

echo ""

# Create authorization header
echo -e "${YELLOW}Creating authorization header...${NC}"
GRAFANA_CREDENTIALS="${GRAFANA_INSTANCE_ID}:${GRAFANA_TOKEN}"
GRAFANA_AUTH_HEADER="Basic $(echo -n "$GRAFANA_CREDENTIALS" | base64 -w 0)"

echo -e "${GREEN}✓ Authorization header created${NC}"
echo ""

# Create temporary secret
echo -e "${YELLOW}Creating Kubernetes secret...${NC}"
kubectl create secret generic "$SECRET_NAME" \
  --from-literal=grafana-endpoint="$GRAFANA_ENDPOINT" \
  --from-literal=grafana-headers="$GRAFANA_AUTH_HEADER" \
  --namespace="$NAMESPACE" \
  --dry-run=client \
  -o yaml > /tmp/otel-collector-secret.yaml

echo -e "${GREEN}✓ Kubernetes secret created${NC}"
echo ""

# Seal the secret
echo -e "${YELLOW}Sealing secret with kubeseal...${NC}"
kubeseal --format=yaml \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  < /tmp/otel-collector-secret.yaml \
  > "$SEALED_SECRET_FILE"

echo -e "${GREEN}✓ Sealed secret created${NC}"
echo ""

# Cleanup
rm /tmp/otel-collector-secret.yaml

# Summary
echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}Success!${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo ""
echo "Sealed secret created: $SEALED_SECRET_FILE"
echo ""
echo "Next steps:"
echo "1. Review the sealed secret file"
echo "2. Commit to Git (it's safe - encrypted for your cluster only)"
echo "3. Apply to cluster:"
echo "   kubectl apply -f $SEALED_SECRET_FILE"
echo ""
echo "Or let ArgoCD sync it automatically."
echo ""
echo -e "${YELLOW}Note: The sealed secret can only be decrypted by your k3s cluster.${NC}"
echo -e "${YELLOW}If you rebuild the cluster, you'll need to regenerate it.${NC}"
echo ""
