# Dentari Application - Sealed Secrets Setup

This directory contains Kubernetes manifests for the Dentari application deployment, including sealed secrets for secure credential management.

## Sealed Secrets

This deployment uses [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) for secure secret management. The sealed-secrets controller is already deployed in the cluster via ArgoCD (`app/k3s-system/sealed-secrets`).

### Current Secrets

1. **ghcr-sealed-secret.yaml** - GitHub Container Registry credentials (to be created)
2. **secret.yaml** - OpenTelemetry configuration template

## Setup Instructions

### Prerequisites

- kubectl configured and connected to the cluster
- kubeseal CLI installed (installed automatically by the script)
- GitHub Personal Access Token with `read:packages` and `write:packages` scopes

### Creating the GHCR Sealed Secret

#### Option 1: Using the provided script (Recommended)

```bash
cd /home/ferko/Documents/argocd
./scripts/create-ghcr-sealed-secret.sh
```

The script will:
1. Prompt for your GitHub username and token
2. Verify cluster connectivity
3. Create the sealed secret
4. Save it to `app/demo/dentari/ghcr-sealed-secret.yaml`

#### Option 2: Manual creation

```bash
# Create the sealed secret manually
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<your-github-username> \
  --docker-password=<your-github-token> \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  --format=yaml > app/demo/dentari/ghcr-sealed-secret.yaml
```

### Deploying the Sealed Secret

Once created, commit and push the sealed secret:

```bash
cd /home/ferko/Documents/argocd

# Add the sealed secret
git add app/demo/dentari/ghcr-sealed-secret.yaml

# Remove the template (optional, after sealed secret is working)
git rm app/demo/dentari/ghcr-secret.yaml

# Commit and push
git commit -m "Add GHCR sealed secret for Dentari deployment"
git push
```

ArgoCD will automatically:
1. Detect the new sealed secret
2. Apply it to the cluster
3. The sealed-secrets controller will decrypt it
4. Create the actual Kubernetes secret
5. The deployment will use it for pulling images

### Verification

```bash
# Check if the sealed secret was created
kubectl get sealedsecret ghcr-secret -n default

# Check if the actual secret was created by the controller
kubectl get secret ghcr-secret -n default

# Verify the deployment can pull images
kubectl get pods -n default | grep dentari
kubectl describe pod <dentari-pod-name> -n default
```

## How Sealed Secrets Work

1. **Encryption**: The `kubeseal` CLI encrypts secrets using the controller's public key
2. **Safe Storage**: Encrypted secrets (SealedSecret resources) can be safely committed to Git
3. **Automatic Decryption**: The controller watches for SealedSecret resources and decrypts them
4. **Secret Creation**: The controller creates standard Kubernetes secrets from the decrypted data
5. **Application Use**: Applications use the standard secrets normally

### Security Benefits

- ✅ Secrets encrypted client-side before committing to Git
- ✅ Only the cluster's sealed-secrets controller can decrypt
- ✅ No plaintext secrets in Git history
- ✅ GitOps-friendly - secrets managed declaratively
- ✅ Audit trail through Git commits

## Deployment Architecture

```
┌─────────────────────────────────────────────┐
│ GitHub Repository (argocd)                  │
│ ├── app/demo/dentari/                       │
│ │   ├── deployment.yaml                     │
│ │   ├── ghcr-sealed-secret.yaml (encrypted) │
│ │   ├── service.yaml                        │
│ │   └── ingress.yaml                        │
└─────────────────┬───────────────────────────┘
                  │
                  │ ArgoCD syncs
                  ↓
┌─────────────────────────────────────────────┐
│ Kubernetes Cluster                          │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Sealed Secrets Controller               │ │
│ │ (kube-system namespace)                 │ │
│ │                                         │ │
│ │ Watches: SealedSecret resources         │ │
│ │ Decrypts → Creates: Secret resources    │ │
│ └─────────────────────────────────────────┘ │
│                  │                          │
│                  │ Creates                  │
│                  ↓                          │
│ ┌─────────────────────────────────────────┐ │
│ │ Secret: ghcr-secret (default namespace) │ │
│ │ Type: kubernetes.io/dockerconfigjson    │ │
│ └─────────────────────────────────────────┘ │
│                  │                          │
│                  │ Referenced by            │
│                  ↓                          │
│ ┌─────────────────────────────────────────┐ │
│ │ Deployment: dentari                     │ │
│ │ - imagePullSecrets: ghcr-secret         │ │
│ │ - Pulls: ghcr.io/radamhu/dentari:latest │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Troubleshooting

### Sealed Secret Won't Decrypt

```bash
# Check controller logs
kubectl logs -n kube-system -l name=sealed-secrets-controller

# Check if the SealedSecret exists
kubectl get sealedsecret ghcr-secret -n default -o yaml

# Check events
kubectl get events -n default --sort-by='.lastTimestamp'
```

### Image Pull Errors

```bash
# Verify the secret exists and has correct type
kubectl get secret ghcr-secret -n default -o yaml

# Check pod events
kubectl describe pod <dentari-pod-name> -n default

# Test the secret manually
kubectl run test-pull --image=ghcr.io/radamhu/dentari:latest --image-pull-policy=Always --overrides='{"spec":{"imagePullSecrets":[{"name":"ghcr-secret"}]}}' --restart=Never
kubectl logs test-pull
kubectl delete pod test-pull
```

### Re-sealing After Secret Change

```bash
# Delete the old sealed secret
kubectl delete sealedsecret ghcr-secret -n default

# Recreate with new credentials
./scripts/create-ghcr-sealed-secret.sh

# Commit and push
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "Update GHCR sealed secret"
git push
```

## Secret Rotation

Rotate the GHCR token every 90 days:

1. Create new GitHub token with same scopes
2. Run the creation script with new token: `./scripts/create-ghcr-sealed-secret.sh`
3. Commit and push the updated sealed secret
4. ArgoCD will sync automatically
5. Revoke the old token in GitHub settings

## Files Reference

- **deployment.yaml** - Main application deployment
  - Uses `imagePullSecrets: ghcr-secret` for pulling images
  - References `dentari-otel-secret` for OpenTelemetry config

- **ghcr-sealed-secret.yaml** - Sealed secret for GHCR access (to be created)
  - Type: `kubernetes.io/dockerconfigjson`
  - Encrypted with sealed-secrets controller public key

- **ghcr-secret.yaml** - Template file (can be removed after sealed secret is created)
  - Contains documentation only
  - Should NOT contain actual credentials

- **secret.yaml** - OpenTelemetry configuration template
  - Needs to be sealed similar to GHCR secret if used

## Additional Resources

- [Sealed Secrets Documentation](https://github.com/bitnami-labs/sealed-secrets)
- [ArgoCD Sealed Secrets Application](../../../app/k3s-system/sealed-secrets/argocd-sealed-secrets.yaml)
- [Security Incident Response Guide](../../../SECURITY_INCIDENT_RESPONSE.md)
- [Secrets Management Best Practices](../../../SECRETS_MANAGEMENT.md)
