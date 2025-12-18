# Dentari User Seeding - K3s

## Overview

This Job creates initial test users in the Dentari database for authentication.

## Users Created

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| `owner` | `owner123` | owner | Admin privileges |
| `courier1` | `courier123` | courier | Courier user |

**⚠️ WARNING**: Change these passwords in production!

## Deployment

### 1. Ensure namespace exists

```bash
kubectl apply -f namespace.yaml
```

### 2. Ensure PVC exists

The Job requires the `dentari-data-pvc` to exist in the `dentari` namespace.

```bash
# Check if PVC exists
kubectl get pvc dentari-data-pvc -n dentari

# If not, apply it first
kubectl apply -f pvc.yaml
```

### 3. Run the seed job

```bash
kubectl apply -f seed-users-job.yaml
```

### 4. Monitor the job

```bash
# Check job status
kubectl get jobs -n dentari

# Watch the job
kubectl get job dentari-seed-users -n dentari -w

# View logs
kubectl logs -n dentari job/dentari-seed-users -f
```

### 5. Verify users were created

```bash
# Get the pod name
POD_NAME=$(kubectl get pods -n dentari -l job-name=dentari-seed-users -o jsonpath='{.items[0].metadata.name}')

# Connect to the database and check users
kubectl exec -n dentari $POD_NAME -- sqlite3 /app/data/dentari.db "SELECT username, email, name, role FROM users;"
```

Or check the application:
```bash
# Port forward to the application
kubectl port-forward -n dentari svc/dentari 8501:8501

# Open browser: http://localhost:8501
# Go to Login page and try credentials
```

## Cleanup

After successful seeding, you can optionally delete the job (the pod will auto-delete after 1 hour):

```bash
kubectl delete job dentari-seed-users -n dentari
```

## Troubleshooting

### Job Failed

```bash
# Check job status
kubectl describe job dentari-seed-users -n dentari

# Check pod logs
kubectl logs -n dentari -l job-name=dentari-seed-users

# Check if PVC is mounted correctly
kubectl describe pod -n dentari -l job-name=dentari-seed-users
```

### Users Already Exist

The script is idempotent - it skips users that already exist:
```
⏭️  User 'owner' already exists, skipping
⏭️  User 'courier1' already exists, skipping
```

### Permission Denied on Database

Check if the PVC has correct permissions:
```bash
# Get a shell in the job pod
kubectl exec -it -n dentari <pod-name> -- bash

# Check permissions
ls -la /app/data/
```

The Job runs as user 1000:1000 (same as the main application).

## Re-running the Job

To re-run the job:

```bash
# Delete the old job
kubectl delete job dentari-seed-users -n dentari

# Apply again
kubectl apply -f seed-users-job.yaml
```

## Integration with ArgoCD

The job is included in the Dentari application manifests. ArgoCD will:
1. Create the namespace
2. Create the PVC
3. Create the seed job
4. The job runs once and completes

To manually trigger via ArgoCD:
```bash
# Delete the job (ArgoCD will recreate it)
kubectl delete job dentari-seed-users -n dentari

# Sync the application
kubectl patch application dentari -n argocd --type merge -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"normal"}}}'
```
