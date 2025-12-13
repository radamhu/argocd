# Quick Reference - Sealed Secrets for Dentari

## ⚡ Quick Start

```bash
cd /home/ferko/Documents/argocd
./scripts/create-ghcr-sealed-secret.sh
```

Follow the prompts, then:

```bash
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "Add GHCR sealed secret"
git push
```

## 📋 Prerequisites Checklist

- [ ] Sealed Secrets controller running in cluster (already deployed via ArgoCD)
- [ ] kubeseal CLI installed (script installs it automatically)
- [ ] kubectl configured and connected to cluster
- [ ] GitHub Personal Access Token ready
  - Scopes: `read:packages`, `write:packages`
  - Create at: https://github.com/settings/tokens/new

## 🔐 Creating GitHub Token

1. Go to: https://github.com/settings/tokens/new
2. Token name: `GHCR Access - Dentari`
3. Expiration: `90 days`
4. Select scopes:
   - ✅ `read:packages`
   - ✅ `write:packages`
5. Click "Generate token"
6. Copy the token (you won't see it again!)

## 🛠️ Manual Commands

### Create Sealed Secret

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=radamhu \
  --docker-password=<YOUR_TOKEN_HERE> \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  --format=yaml > app/demo/dentari/ghcr-sealed-secret.yaml
```

### Verify Deployment

```bash
# Check sealed secret
kubectl get sealedsecret ghcr-secret -n default

# Check actual secret (created by controller)
kubectl get secret ghcr-secret -n default

# Check deployment
kubectl get deployment dentari -n default
kubectl get pods -n default | grep dentari

# Check if pod can pull image
kubectl describe pod <dentari-pod-name> -n default
```

## 🔄 Rotation (Every 90 Days)

```bash
# 1. Create new GitHub token
# 2. Run script with new token
./scripts/create-ghcr-sealed-secret.sh

# 3. Commit and push
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "chore: rotate GHCR token"
git push

# 4. Revoke old token
# Go to: https://github.com/settings/tokens
```

## 🐛 Troubleshooting

### Controller Logs
```bash
kubectl logs -n kube-system -l name=sealed-secrets-controller
```

### Image Pull Errors
```bash
# Check pod events
kubectl describe pod <dentari-pod-name> -n default

# Check secret contents
kubectl get secret ghcr-secret -n default -o yaml
```

### Re-seal Secret
```bash
# Delete existing
kubectl delete sealedsecret ghcr-secret -n default

# Recreate
./scripts/create-ghcr-sealed-secret.sh

# Push changes
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "fix: re-seal GHCR secret"
git push
```

## 📁 File Locations

- **Script**: `scripts/create-ghcr-sealed-secret.sh`
- **Sealed Secret**: `app/demo/dentari/ghcr-sealed-secret.yaml` (to be created)
- **Template**: `app/demo/dentari/ghcr-secret.yaml` (remove after sealed secret works)
- **Deployment**: `app/demo/dentari/deployment.yaml` (already configured)
- **Controller**: `app/k3s-system/sealed-secrets/argocd-sealed-secrets.yaml`

## 📚 Documentation

- [Full Setup Guide](app/demo/dentari/README.md)
- [Secrets Management](SECRETS_MANAGEMENT.md)
- [Security Incident Response](SECURITY_INCIDENT_RESPONSE.md)

## ✅ Success Indicators

After creating and deploying the sealed secret:

1. ✅ SealedSecret resource exists: `kubectl get sealedsecret ghcr-secret -n default`
2. ✅ Secret resource exists: `kubectl get secret ghcr-secret -n default`
3. ✅ Pod is running: `kubectl get pods -n default | grep dentari`
4. ✅ No ImagePullBackOff errors: `kubectl describe pod <pod-name> -n default`
5. ✅ Application is accessible via ingress

## 🚨 Emergency - Token Exposed

If a token is accidentally committed:

```bash
# 1. Revoke token immediately
# https://github.com/settings/tokens

# 2. Remove from Git history
cd /home/ferko/Documents/argocd
git filter-repo --path app/demo/dentari/ghcr-secret.yaml --invert-paths
git push origin --force --all

# 3. Create new sealed secret
./scripts/create-ghcr-sealed-secret.sh

# 4. Follow SECURITY_INCIDENT_RESPONSE.md
```

## 💡 Tips

- **Clear history**: Run `history -c` after entering tokens in terminal
- **Use script**: The script handles complexity and validation
- **Test first**: Verify in dev before production
- **Document rotation**: Note rotation dates in calendar
- **Monitor alerts**: GitGuardian will alert on exposed secrets
