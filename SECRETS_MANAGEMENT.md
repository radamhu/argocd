# Secret Management Best Practices for ArgoCD

## Overview

This guide establishes secure secret management practices for the ArgoCD repository to prevent credential exposure.

## Core Principles

1. **Never commit actual secrets to Git**
2. **Use secret management tools** (Sealed Secrets, External Secrets, Vault)
3. **Commit only templates** with documentation
4. **Automate prevention** with pre-commit hooks
5. **Monitor continuously** for exposed secrets

## Secret Templates Structure

All secret files in this repository should follow this pattern:

```yaml
---
# [Secret Name] Template
# This file should NOT contain actual credentials.
#
# Instructions for creating this secret:
#   [specific commands or steps]
#
# For production, use one of these secure methods:
# 1. Sealed Secrets
# 2. External Secrets Operator
# 3. ArgoCD Vault Plugin
#
apiVersion: v1
kind: Secret
metadata:
  name: [secret-name]
  labels:
    app: [app-name]
type: [secret-type]
data:
  # DO NOT commit actual credentials here!
  [key]: ""
```

## Recommended Solution: Sealed Secrets

Sealed Secrets is the recommended approach for this ArgoCD setup.

### Why Sealed Secrets?

- ✅ Secrets encrypted client-side
- ✅ Safe to commit to Git
- ✅ Works seamlessly with ArgoCD
- ✅ No external dependencies
- ✅ Simple to use

### Setup Instructions

#### 1. Install Sealed Secrets Controller

```bash
# Add to ArgoCD apps
cat > argocd-apps/k3s-system/argocd-sealed-secrets.yaml <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sealed-secrets
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://bitnami-labs.github.io/sealed-secrets
    chart: sealed-secrets
    targetRevision: 2.14.0
  destination:
    server: https://kubernetes.default.svc
    namespace: kube-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

#### 2. Install kubeseal CLI

```bash
# macOS
brew install kubeseal

# Linux
KUBESEAL_VERSION='0.24.0'
wget "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

#### 3. Create Sealed Secrets

```bash
# For Docker registry secrets
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=<token> \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > app/demo/dentari/ghcr-sealed-secret.yaml

# For generic secrets (OTEL example)
kubectl create secret generic dentari-otel-secret \
  --from-literal=endpoint='http://otel-collector:4317' \
  --from-literal=headers='Authorization=Bearer <token>' \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > app/demo/dentari/otel-sealed-secret.yaml
```

#### 4. Update Deployment

```yaml
# app/demo/dentari/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dentari
spec:
  template:
    spec:
      imagePullSecrets:
        - name: ghcr-secret  # References sealed secret
      containers:
        - name: dentari
          envFrom:
            - secretRef:
                name: dentari-otel-secret  # References sealed secret
```

## Alternative Solutions

### External Secrets Operator

For multi-cloud environments with existing secret managers:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ghcr-secret
spec:
  secretStoreRef:
    name: aws-parameter-store
    kind: SecretStore
  target:
    name: ghcr-secret
  data:
    - secretKey: .dockerconfigjson
      remoteRef:
        key: /dentari/ghcr-credentials
```

**Setup:** See [app/k3s-system/external-secrets-operator/](app/k3s-system/external-secrets-operator/)

### ArgoCD Vault Plugin

For HashiCorp Vault users:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ghcr-secret
stringData:
  username: <path:secret/data/dentari/ghcr#username>
  password: <path:secret/data/dentari/ghcr#password>
```

**Setup:** [ArgoCD Vault Plugin Documentation](https://argocd-vault-plugin.readthedocs.io/)

## Secret Types and Examples

### Docker Registry Secrets

```bash
# Template location: app/demo/[app-name]/[registry]-secret.yaml.template
# Sealed secret: app/demo/[app-name]/[registry]-sealed-secret.yaml

kubectl create secret docker-registry <name> \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password> \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > <output-file>
```

### Generic Secrets

```bash
# Template location: app/demo/[app-name]/[secret-name]-secret.yaml.template
# Sealed secret: app/demo/[app-name]/[secret-name]-sealed-secret.yaml

kubectl create secret generic <name> \
  --from-literal=key1=value1 \
  --from-literal=key2=value2 \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > <output-file>
```

### TLS Secrets

```bash
kubectl create secret tls <name> \
  --cert=path/to/cert.crt \
  --key=path/to/key.key \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > <output-file>
```

## Pre-commit Hooks

Prevent secrets from being committed:

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Initialize in repository
pre-commit install
```

### Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: .*/tests/.*

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
```

### Usage

```bash
# Run manually
pre-commit run --all-files

# Runs automatically on git commit
git commit -m "your message"
```

## GitHub Secret Scanning

Enable in repository settings to automatically detect exposed secrets:

1. Go to: `https://github.com/[org]/[repo]/settings/security_analysis`
2. Enable "Secret scanning"
3. Enable "Push protection" (prevents pushes with detected secrets)

## .gitignore Rules

Add to `.gitignore`:

```gitignore
# Secrets - DO NOT COMMIT
*secret.yaml
!*sealed-secret.yaml
!*-secret.yaml.template
*.env
*.env.local
.env
credentials.json
*-credentials.json
**/secrets/
**/*-key.pem
**/*.key
```

## Secret Rotation

### Regular Rotation Schedule

- **GitHub tokens:** Every 90 days
- **API keys:** Every 90 days
- **TLS certificates:** Based on expiration
- **Database passwords:** Every 180 days

### Rotation Process

1. Generate new secret
2. Create new sealed secret
3. Update in Git
4. ArgoCD auto-syncs
5. Verify application functionality
6. Revoke old secret

### Automation

```bash
#!/bin/bash
# scripts/rotate-ghcr-secret.sh

echo "Rotating GHCR secret..."
echo "1. Create new GitHub token at: https://github.com/settings/tokens/new"
read -p "Enter new token: " -s NEW_TOKEN
echo

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=radamhu \
  --docker-password=$NEW_TOKEN \
  --dry-run=client -o yaml | \
  kubeseal --format=yaml > app/demo/dentari/ghcr-sealed-secret.yaml

git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "chore: rotate GHCR secret"
git push

echo "Secret rotated and committed. ArgoCD will sync automatically."
echo "Don't forget to revoke the old token!"
```

## Troubleshooting

### Sealed Secret Won't Decrypt

```bash
# Check controller logs
kubectl logs -n kube-system -l name=sealed-secrets-controller

# Verify secret exists
kubectl get sealedsecret
kubectl get secret

# Re-seal if needed
kubectl delete sealedsecret <name>
# Re-run kubeseal command
```

### ArgoCD Not Syncing Secrets

```bash
# Check ArgoCD logs
kubectl logs -n argocd deployment/argocd-repo-server

# Force sync
argocd app sync <app-name>

# Check application status
argocd app get <app-name>
```

## Checklist for New Secrets

When adding a new secret to the repository:

- [ ] Create template file with documentation
- [ ] Add to .gitignore if needed
- [ ] Generate sealed secret (not plain secret)
- [ ] Test in development environment
- [ ] Document in this guide
- [ ] Update deployment references
- [ ] Run pre-commit hooks
- [ ] Review with security team
- [ ] Commit only sealed/encrypted version
- [ ] Verify ArgoCD sync

## Security Contact

For security issues or questions:

- **Security incidents:** Create private GitHub security advisory
- **Questions:** [maintainer email]
- **Emergency:** [emergency contact]

## References

- [Sealed Secrets Documentation](https://github.com/bitnami-labs/sealed-secrets)
- [ArgoCD Declarative Setup](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- [Kubernetes Secrets Best Practices](https://kubernetes.io/docs/concepts/configuration/secret/)
- [GitGuardian Secret Detection](https://www.gitguardian.com/)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
