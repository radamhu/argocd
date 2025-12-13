#!/bin/bash
set -e

# Script to create a sealed GHCR secret for the Dentari application
# This script creates a sealed secret that can be safely committed to Git

echo "=== GHCR Sealed Secret Creator ==="
echo ""
echo "This script will create a sealed secret for GitHub Container Registry access."
echo "You will need a GitHub Personal Access Token with 'read:packages' and 'write:packages' scopes."
echo ""
echo "To create a token:"
echo "1. Go to: https://github.com/settings/tokens/new"
echo "2. Set name: 'GHCR Access - Dentari'"
echo "3. Select scopes: read:packages, write:packages"
echo "4. Set expiration: 90 days"
echo "5. Generate and copy the token"
echo ""

# Get inputs
read -p "GitHub Username [radamhu]: " GITHUB_USERNAME
GITHUB_USERNAME=${GITHUB_USERNAME:-radamhu}

read -p "GitHub Token: " -s GITHUB_TOKEN
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GitHub token is required"
    exit 1
fi

# Verify kubectl connection
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot connect to Kubernetes cluster"
    echo "Please ensure kubectl is configured correctly"
    exit 1
fi

# Verify sealed-secrets controller is running
if ! kubectl get deployment sealed-secrets-controller -n kube-system &> /dev/null; then
    echo "❌ Error: sealed-secrets-controller not found in kube-system namespace"
    echo "Please ensure Sealed Secrets is deployed"
    exit 1
fi

echo ""
echo "✓ Connected to Kubernetes cluster"
echo "✓ Sealed Secrets controller found"
echo ""

# Create the sealed secret
echo "Creating sealed secret..."

OUTPUT_FILE="app/demo/dentari/ghcr-sealed-secret.yaml"

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username="$GITHUB_USERNAME" \
  --docker-password="$GITHUB_TOKEN" \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system \
  --format=yaml > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Sealed secret created: $OUTPUT_FILE"
    echo ""
    echo "The sealed secret has been created and can be safely committed to Git."
    echo ""
    echo "Next steps:"
    echo "1. Review the sealed secret: cat $OUTPUT_FILE"
    echo "2. Commit to Git: git add $OUTPUT_FILE && git commit -m 'Add GHCR sealed secret' && git push"
    echo "3. ArgoCD will automatically sync and deploy the secret"
    echo "4. Delete the plain secret template: git rm app/demo/dentari/ghcr-secret.yaml"
    echo ""
    echo "⚠️  IMPORTANT: Clear your shell history to remove the token:"
    echo "   history -c"
else
    echo "❌ Error: Failed to create sealed secret"
    exit 1
fi
