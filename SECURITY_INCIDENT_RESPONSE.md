# Security Incident Response - Exposed GitHub Token

**Date:** December 13, 2025
**Incident:** Kubernetes Docker Secret exposed containing GitHub Personal Access Token
**Severity:** CRITICAL

## Exposed Token Information

- **Token:** `ghp_eHvrMWu7***[REDACTED]***XBaYf` (already revoked)
- **Location:** `app/demo/dentari/ghcr-secret.yaml`
- **Repository:** radamhu/argocd
- **Detection Date:** December 10, 2025, 17:58:02 UTC
- **Detector:** GitGuardian

## Immediate Actions (Complete These NOW)

### 1. Revoke the Exposed Token ⚠️ URGENT

```bash
# Go to GitHub and revoke the token immediately:
# https://github.com/settings/tokens
# Or use GitHub CLI:
gh auth token | xargs -I {} gh api -X DELETE /applications/{client_id}/token -f access_token={}
```

**Manual Steps:**
1. Go to https://github.com/settings/tokens
2. Find the token ending in `...1XBaYf`
3. Click "Delete" or "Revoke"
4. Confirm the revocation

### 2. Remove Secret from Git History

The token was committed to the repository and needs to be completely removed from Git history:

```bash
cd /home/ferko/Documents/argocd

# Option 1: Using git-filter-repo (recommended)
# Install: pip install git-filter-repo
git filter-repo --path app/demo/dentari/ghcr-secret.yaml --invert-paths

# Option 2: Using BFG Repo-Cleaner
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files ghcr-secret.yaml

# Option 3: Manual rewrite (if above tools not available)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch app/demo/dentari/ghcr-secret.yaml" \
  --prune-empty --tag-name-filter cat -- --all
```

### 3. Force Push Changes

```bash
# Verify the secret is removed from history
git log --all --full-history -- app/demo/dentari/ghcr-secret.yaml

# Force push to remote (WARNING: This rewrites history)
git push origin --force --all
git push origin --force --tags
```

### 4. Notify Collaborators

All collaborators must re-clone the repository:

```bash
# Send this message to all team members:
# "Security incident: Please delete your local clone and re-clone the repository"
# git clone https://github.com/radamhu/argocd.git
```

## Assess Impact

### Check Token Usage

```bash
# Check GitHub audit log for unauthorized access:
# https://github.com/settings/security-log

# Check for suspicious activities:
# - New repositories created
# - Repository access changes
# - Package registry access
# - Actions runs
```

### Generate New Token

```bash
# Create a new token with minimal required permissions:
# 1. Go to https://github.com/settings/tokens/new
# 2. Set name: "GHCR Access - Dentari App"
# 3. Select scopes: read:packages, write:packages
# 4. Set expiration: 90 days
# 5. Click "Generate token"
# 6. SAVE IT SECURELY (you won't see it again)
```

## Implement Secure Secret Management

### Option 1: Sealed Secrets (Recommended)

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Install kubeseal CLI
brew install kubeseal  # macOS
# or
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-linux-amd64
chmod +x kubeseal-linux-amd64
sudo mv kubeseal-linux-amd64 /usr/local/bin/kubeseal

# Create sealed secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=radamhu \
  --docker-password=<NEW_TOKEN> \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > app/demo/dentari/ghcr-sealed-secret.yaml

# Commit the sealed secret (safe to commit)
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "Add sealed GHCR secret"
git push
```

### Option 2: External Secrets Operator

```bash
# Install External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace

# Store secret in a secret manager (AWS Secrets Manager, GCP Secret Manager, etc.)
# Then create ExternalSecret resource
cat > app/demo/dentari/ghcr-external-secret.yaml <<EOF
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ghcr-secret
spec:
  secretStoreRef:
    name: aws-secretsmanager  # or your secret store
    kind: SecretStore
  target:
    name: ghcr-secret
    creationPolicy: Owner
  data:
  - secretKey: .dockerconfigjson
    remoteRef:
      key: dentari/ghcr-credentials
EOF
```

### Option 3: ArgoCD Vault Plugin

```bash
# Install ArgoCD Vault Plugin
# https://argocd-vault-plugin.readthedocs.io/

# Store secret in Vault
vault kv put secret/dentari/ghcr \
  username=radamhu \
  password=<NEW_TOKEN>

# Reference in secret.yaml
cat > app/demo/dentari/ghcr-secret.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: ghcr-secret
type: kubernetes.io/dockerconfigjson
stringData:
  .dockerconfigjson: |
    {
      "auths": {
        "ghcr.io": {
          "username": "<path:secret/data/dentari/ghcr#username>",
          "password": "<path:secret/data/dentari/ghcr#password>",
          "auth": "<path:secret/data/dentari/ghcr#username | base64encode>"
        }
      }
    }
EOF
```

## Prevent Future Incidents

### 1. Add .gitignore Rules

```bash
cat >> .gitignore <<EOF

# Secrets and credentials
*secret*.yaml
*-secret.yaml
*.env
*.env.local
.env
credentials.json
*-credentials.json
**/secrets/
EOF
```

### 2. Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks
EOF

# Install hooks
pre-commit install
pre-commit run --all-files
```

### 3. Enable GitHub Secret Scanning

1. Go to repository settings: https://github.com/radamhu/argocd/settings/security_analysis
2. Enable "Secret scanning"
3. Enable "Push protection" (prevents pushes with secrets)

### 4. Use GitHub Environments with Secrets

For CI/CD, use GitHub Actions secrets instead of committing credentials:

```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

## Monitoring and Alerts

### Set up GitGuardian (Already Active)

- ✅ Already detected this incident
- Configure email notifications
- Review other repositories

### Additional Monitoring

```bash
# Set up GitHub webhook for security events
# https://docs.github.com/en/webhooks/webhook-events-and-payloads#security_and_analysis

# Monitor with Falco for k8s secret access
# https://falco.org/
```

## Lessons Learned

1. **Never commit secrets to Git** - Use secret management solutions
2. **Use template files** - Commit example/template files with empty values
3. **Automate prevention** - Use pre-commit hooks and GitHub push protection
4. **Rotate secrets regularly** - Set expiration dates on tokens
5. **Apply least privilege** - Grant minimum required permissions
6. **Monitor continuously** - Use secret scanning tools

## Checklist

- [ ] Revoked exposed GitHub token
- [ ] Generated new token with minimal permissions
- [ ] Removed secret from Git history
- [ ] Force pushed cleaned history
- [ ] Notified all collaborators to re-clone
- [ ] Reviewed GitHub audit log for suspicious activity
- [ ] Implemented sealed-secrets or equivalent
- [ ] Added .gitignore rules
- [ ] Installed pre-commit hooks
- [ ] Enabled GitHub secret scanning and push protection
- [ ] Documented incident and response
- [ ] Updated deployment documentation with secure practices

## References

- [GitHub Token Security Best Practices](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [External Secrets Operator](https://external-secrets.io/)
- [ArgoCD Vault Plugin](https://argocd-vault-plugin.readthedocs.io/)
- [GitGuardian](https://www.gitguardian.com/)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
