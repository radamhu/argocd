# Dentari Application - K3s Deployment

This directory contains Kubernetes manifests for the Dentari application deployment with OpenTelemetry observability.

## Architecture

```
┌─────────────────┐
│   Dentari App   │
│   (Streamlit)   │
└────────┬────────┘
         │ OTLP (gRPC:4317)
         ▼
┌─────────────────┐
│ OTEL Collector  │
│  (in cluster)   │
└────────┬────────┘
         │ OTLP/HTTPS
         ▼
┌─────────────────┐
│ Grafana Cloud   │
│  (Loki, Tempo)  │
└─────────────────┘
```

## Components

### Application Resources
- **deployment.yaml** - Dentari application deployment
- **service.yaml** - LoadBalancer service (MetalLB)
- **pvc.yaml** - Persistent volume claims (data, cache, logs)
- **ingress.yaml** - Ingress configuration (Traefik)

### OpenTelemetry Resources
- **otel-collector-deployment.yaml** - OTEL Collector deployment
- **otel-collector-service.yaml** - OTEL Collector service (ClusterIP)
- **otel-collector-configmap.yaml** - OTEL Collector configuration
- **otel-collector-secret.yaml** - Grafana Cloud credentials template
- **otel-collector-sealed-secret.yaml** - Sealed secret (to be created)

### Sealed Secrets
- **ghcr-sealed-secret.yaml** - GitHub Container Registry credentials (to be created)
- **secret.yaml** - Legacy OTEL configuration template (deprecated)

## Sealed Secrets

This deployment uses [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) for secure secret management. The sealed-secrets controller is already deployed in the cluster via ArgoCD (`app/k3s-system/sealed-secrets`).

## Setup Instructions

### Prerequisites

- kubectl configured and connected to the cluster
- kubeseal CLI installed
- GitHub Personal Access Token with `read:packages` scope
- Grafana Cloud account (optional, for observability)

### Step 1: Create GHCR Sealed Secret

```bash
cd /home/ferko/Documents/argocd
./scripts/create-ghcr-sealed-secret.sh
```

This creates: `app/demo/dentari/ghcr-sealed-secret.yaml`

### Step 2: Create Grafana Cloud Sealed Secret (Optional)

If you want observability with Grafana Cloud:

```bash
cd /home/ferko/Documents/argocd
./scripts/create-grafana-otel-sealed-secret.sh
```

This creates: `app/demo/dentari/otel-collector-sealed-secret.yaml`

**Note**: If you skip this step, you can still deploy but OpenTelemetry will be disabled.

### Step 3: Deploy to K3s

#### Option A: Using ArgoCD (Recommended)

```bash
# Create ArgoCD application
kubectl apply -f ../../argocd-apps/demo/argocd-dentari.yaml

# ArgoCD will automatically sync and deploy all resources
```

#### Option B: Manual kubectl apply

```bash
cd app/demo/dentari

# Apply in order:
kubectl apply -f pvc.yaml
kubectl apply -f ghcr-sealed-secret.yaml

# Apply OTEL resources (if using Grafana Cloud)
kubectl apply -f otel-collector-sealed-secret.yaml  # or otel-collector-secret.yaml (template)
kubectl apply -f otel-collector-configmap.yaml
kubectl apply -f otel-collector-deployment.yaml
kubectl apply -f otel-collector-service.yaml

# Apply application resources
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### Step 4: Commit Sealed Secrets to Git

```bash
cd /home/ferko/Documents/argocd

# Add the sealed secrets
git add app/demo/dentari/ghcr-sealed-secret.yaml
git add app/demo/dentari/otel-collector-sealed-secret.yaml  # if created

# Commit and push
git commit -m "Add sealed secrets for Dentari deployment"
git push
```

ArgoCD will automatically sync and apply the changes.

## Verification

### Check Deployment Status

```bash
# Check all resources
kubectl get all -l app=dentari
kubectl get all -l app=otel-collector

# Check pods are running
kubectl get pods | grep -E 'dentari|otel-collector'

# Check logs
kubectl logs -l app=dentari --tail=50 -f
kubectl logs -l app=otel-collector --tail=50 -f
```

### Verify OpenTelemetry

```bash
# Check OTEL collector health
kubectl exec -it deployment/otel-collector -- wget -O- http://localhost:13133/

# Check OTEL collector metrics
kubectl port-forward svc/otel-collector 8888:8888
curl http://localhost:8888/metrics

# Verify Dentari can reach collector
kubectl exec -it deployment/dentari -- wget -O- http://otel-collector:4317
```

## Database Migrations

The Dentari application uses an automated database migration system to ensure the database schema is always up-to-date.

### How It Works

**Init Container Pattern:**
- Every pod starts with an `init-migrations` container
- Runs `scripts/run_migrations.py` before the main app starts
- Executes all pending migrations from `scripts/migrations/` directory
- Fails fast if migrations error (prevents app from starting with broken schema)

**Migration Tracking:**
- Applied migrations are recorded in `schema_migrations` table
- Contains: `id`, `filename`, `applied_at` timestamp
- Prevents duplicate migration execution
- Provides audit trail of schema changes

**Deployment Flow:**
```
PVC Created → seed-users-job → Init Container (Migrations) → Main App
                 ↓                      ↓                        ↓
              User Data          Schema Creation          Application Ready
```

### Adding New Migrations

1. **Create migration file** in `scripts/migrations/`:
   ```bash
   # Naming convention: NNN_description.py
   002_add_new_feature.py
   ```

2. **Implement migration function**:
   ```python
   def run_migration(db_path: str = "data/dentari.db") -> None:
       """Migration description"""
       conn = sqlite3.connect(db_path)
       cursor = conn.cursor()

       # Your migration logic here
       cursor.execute("ALTER TABLE ...")

       conn.commit()
       conn.close()
   ```

3. **Test locally**:
   ```bash
   cd /path/to/Dentari
   python scripts/run_migrations.py
   ```

4. **Commit and deploy**:
   ```bash
   git add scripts/migrations/002_add_new_feature.py
   git commit -m "feat: add new feature migration"
   git push
   # Migration auto-applies on next pod start
   ```

### Migration Troubleshooting

#### Init Container Failed

```bash
# Check init container logs
kubectl logs -n dentari <pod-name> -c init-migrations

# Common issues:
# - SQL syntax error in migration file
# - Missing schema file referenced by migration
# - Database file permissions
```

#### Verify Applied Migrations

```bash
# Connect to database in running pod
kubectl exec -it -n dentari deployment/dentari -- sqlite3 /app/data/dentari.db

# Query migration history
sqlite> SELECT * FROM schema_migrations ORDER BY applied_at;

# Check table structure
sqlite> .schema dental_work_log
sqlite> .quit
```

#### Manual Migration Execution

If you need to run migrations manually:

```bash
# Copy migration runner to pod
kubectl exec -it -n dentari deployment/dentari -- python scripts/run_migrations.py

# Or run specific migration
kubectl exec -it -n dentari deployment/dentari -- \
  python scripts/migrations/001_create_dental_work_log.py
```

#### Rolling Back Migrations

**Warning:** Migrations are forward-only. No automatic rollback.

To rollback manually:
1. Write reverse SQL statements
2. Execute via `kubectl exec`
3. Remove migration record from `schema_migrations` table

Example:
```bash
kubectl exec -it -n dentari deployment/dentari -- sqlite3 /app/data/dentari.db <<EOF
-- Reverse the migration
DROP TABLE IF EXISTS dental_work_log;

-- Remove from tracking
DELETE FROM schema_migrations WHERE filename = '001_create_dental_work_log.py';
EOF
```

#### Database Recovery

If database is corrupted or lost:

1. **Delete PVC** (destroys all data):
   ```bash
   kubectl delete pvc dentari-data-pvc -n dentari
   ```

2. **Recreate PVC**:
   ```bash
   kubectl apply -f pvc.yaml
   ```

3. **Restart pod** (init container recreates schema):
   ```bash
   kubectl delete pod -l app=dentari -n dentari
   ```

4. **Re-run seed job** (restores initial users):
   ```bash
   kubectl delete job dentari-seed-users -n dentari
   kubectl apply -f seed-users-job.yaml
   ```

### Migration Best Practices

- ✅ Use `CREATE TABLE IF NOT EXISTS` for safety
- ✅ Test migrations with production data dumps locally
- ✅ Keep migrations small and focused
- ✅ Use transactions for multi-step changes
- ✅ Add indexes after bulk inserts, not before
- ❌ Don't modify existing migrations (create new ones)
- ❌ Don't delete migration files (breaks tracking)
- ❌ Don't use `DROP TABLE` without backups

### Access Application

```bash
# Via LoadBalancer (if MetalLB configured)
echo "http://$(kubectl get svc dentari -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8501"

# Via Ingress (if configured)
echo "http://dentari.local"  # or your ingress host
```

## Configuration

### OpenTelemetry Options

#### Option 1: Disabled (No Observability)

Set in [deployment.yaml](deployment.yaml):

```yaml
env:
  - name: OTEL_ENABLED
    value: "false"
```

No OTEL collector needed. Application uses file and console logging only.

#### Option 2: Local Collector → Grafana Cloud (Recommended)

This is the **current configuration**:

```yaml
env:
  - name: OTEL_ENABLED
    value: "true"
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://otel-collector:4317"
```

Requires:
- OTEL collector deployed (otel-collector-*.yaml)
- Grafana Cloud credentials in otel-collector-secret

Benefits:
- Centralized telemetry processing
- Batching and retry logic
- Multiple apps can share one collector
- Reduced memory in application pods

#### Option 3: Direct to Grafana Cloud

Alternative configuration (not recommended):

```yaml
env:
  - name: OTEL_ENABLED
    value: "true"
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "https://otlp-gateway-prod-eu-west-0.grafana.net/otlp"
  - name: OTEL_EXPORTER_OTLP_HEADERS
    valueFrom:
      secretKeyRef:
        name: dentari-grafana-secret
        key: authorization
```

Requires:
- Grafana Cloud credentials in application secret
- No OTEL collector needed

Drawbacks:
- Each pod connects directly (more connections)
- No batching/retry in collector
- Credentials duplicated per app

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
│ │   ├── otel-collector-deployment.yaml      │
│ │   ├── ghcr-sealed-secret.yaml (encrypted) │
│ │   ├── otel-sealed-secret.yaml (encrypted) │
│ │   └── ...                                 │
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
│ │ Decrypts → Creates Secrets              │ │
│ └─────────────────────────────────────────┘ │
│                  │                          │
│                  ↓                          │
│ ┌──────────────┐   ┌─────────────────────┐ │
│ │ ghcr-secret  │   │ otel-collector-     │ │
│ │              │   │ secret              │ │
│ └──────────────┘   └─────────────────────┘ │
│         │                     │             │
│         │                     │             │
│         ↓                     ↓             │
│ ┌─────────────┐       ┌──────────────────┐ │
│ │  Dentari    │──────→│ OTEL Collector   │ │
│ │  (app)      │ :4317 │                  │ │
│ └─────────────┘       └────────┬─────────┘ │
│                                │           │
└────────────────────────────────┼───────────┘
                                 │
                                 │ OTLP/HTTPS
                                 ↓
                        ┌─────────────────┐
                        │ Grafana Cloud   │
                        │ (Loki, Tempo)   │
                        └─────────────────┘
```

## Troubleshooting

### Sealed Secret Won't Decrypt

```bash
# Check controller logs
kubectl logs -n kube-system -l name=sealed-secrets-controller

# Check if the SealedSecret exists
kubectl get sealedsecret -n default

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
