# ArgoCD Homelab - K3s GitOps Repository

This repository contains ArgoCD applications and configurations for managing a K3s cluster using GitOps principles.

## Sources & References
- https://gitlab.com/k3s-media/k3s-media-server/-/tree/main/media-server\?ref_type\=heads
- https://github.com/bjw-s/helm-charts
- https://github.com/gruberdev/homelab
- https://github.com/acelinkio/argocd-homelab
- https://github.com/crkochan/argocd-homelab
- https://community-scripts.github.io/ProxmoxVE/
- https://rpi4cluster.com/
- https://kubesearch.dev/

---

## Repository Structure

```
argocd/
├── app/
│   ├── demo/                    # Demo applications
│   │   ├── dentari/             # Dentari app deployment
│   │   ├── hello-flask/         # Flask demo app
│   │   ├── helm-guestbook/      # Helm guestbook example
│   │   └── openfaas-fn/         # OpenFaaS function examples
│   └── k3s-system/              # System components
│       ├── cert-manager/
│       ├── eraser/
│       ├── external-dns/
│       ├── external-secrets-operator/
│       ├── metallb/
│       ├── openfaas/            # OpenFaaS platform
│       ├── reflector/
│       ├── reloader/
│       ├── sealed-secrets/
│       └── traefik/
└── argocd-apps/                 # ArgoCD Application manifests
    └── demo/
```

---

## ArgoCD Deployment

### Initial Setup

```bash
# Deploy ArgoCD to k3s cluster
sh ./argocd.sh

# Get ArgoCD admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Login to ArgoCD CLI
ARGOCD_PASS=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
argocd login <ARGOCD_IP> --username admin --password "$ARGOCD_PASS" --insecure
```

### Kustomize Deployment

```bash
kubectl kustomize ./app/tools/ --enable-helm | kubectl apply -f -
```

### Apply ArgoCD Applications

```bash
# Apply system applications
kubectl apply -f app/k3s-system/openfaas/argocd-openfaas.yaml
kubectl apply -f app/k3s-system/metallb/argocd-metallb.yaml
# ... etc

# Sync applications
argocd app sync <app-name>
```

---

## OpenFaaS Deployment

OpenFaaS is deployed via ArgoCD Helm chart with the following configuration:

### Access Details

| Item | Value |
|------|-------|
| **UI URL** | `http://192.168.0.101/openfaas/ui/` |
| **API URL** | `http://192.168.0.101/openfaas/` |
| **Username** | `admin` |
| **Password** | See command below |

```bash
# Get OpenFaaS password
kubectl get secret -n openfaas basic-auth -o jsonpath='{.data.basic-auth-password}' | base64 -d && echo
```

### Configuration

The OpenFaaS ArgoCD application is defined in `app/k3s-system/openfaas/argocd-openfaas.yaml`:

- **Chart**: `openfaas` from `https://openfaas.github.io/faas-netes`
- **Version**: `14.2.131`
- **Namespace**: `openfaas`
- **Functions Namespace**: `openfaas-fn`
- **Service Type**: ClusterIP (exposed via Traefik IngressRoute)

### Traefik IngressRoute

OpenFaaS is exposed via path-based routing at `/openfaas`:

```yaml
# app/k3s-system/openfaas/ingress.yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: openfaas
  namespace: openfaas
spec:
  entryPoints:
    - web
  routes:
    - match: PathPrefix(`/openfaas`)
      kind: Rule
      middlewares:
        - name: openfaas-stripprefix
      services:
        - name: gateway
          port: 8080
```

---

## OpenFaaS Functions Development

### Prerequisites

```bash
# Install faas-cli
curl -sSL https://cli.openfaas.com | sudo sh

# Login to OpenFaaS
echo "<password>" | faas-cli login --gateway http://192.168.0.101/openfaas --username admin --password-stdin
```

### Create a New Python Function

```bash
# Pull templates
faas-cli template store pull python3-flask

# Create new function
faas-cli new hello-python --lang python3-flask

# Edit the handler
cat > hello-python/handler.py << 'EOF'
import json
from datetime import datetime

def handle(req):
    """Simple Python function for OpenFaaS"""
    name = req.strip() if req else "World"
    response = {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "platform": "OpenFaaS on k3s"
    }
    return json.dumps(response, indent=2)
EOF
```

### Build, Push & Deploy

```bash
# Update stack.yaml with your registry
cat > stack.yaml << 'EOF'
version: 1.0
provider:
  name: openfaas
  gateway: http://192.168.0.101/openfaas
functions:
  hello-python:
    lang: python3-flask
    handler: ./hello-python
    image: <dockerhub-user>/hello-python:latest
EOF

# Build the function
faas-cli build -f stack.yaml

# Push to registry
faas-cli push -f stack.yaml

# Deploy to OpenFaaS
faas-cli deploy -f stack.yaml
```

### Invoke Function

```bash
# With data
curl -u admin:<password> http://192.168.0.101/openfaas/function/hello-python -d "Your Name"

# Without data
curl -u admin:<password> http://192.168.0.101/openfaas/function/hello-python

# Using faas-cli
echo "Your Name" | faas-cli invoke hello-python --gateway http://192.168.0.101/openfaas
```

### Example Function (app/demo/openfaas-fn/)

The repository includes a sample Python function in `app/demo/openfaas-fn/`:

```
openfaas-fn/
├── hello-python/
│   ├── handler.py          # Function logic
│   └── requirements.txt    # Python dependencies
└── stack.yaml              # OpenFaaS stack definition
```

---

## Useful Commands

### ArgoCD

```bash
# List all applications
argocd app list

# Sync an application
argocd app sync <app-name>

# Get application details
argocd app get <app-name>

# Hard refresh (re-read from Git)
argocd app get <app-name> --hard-refresh
```

### OpenFaaS

```bash
# List deployed functions
faas-cli list --gateway http://192.168.0.101/openfaas

# Get function info
faas-cli describe hello-python --gateway http://192.168.0.101/openfaas

# View function logs
faas-cli logs hello-python --gateway http://192.168.0.101/openfaas

# Remove a function
faas-cli remove hello-python --gateway http://192.168.0.101/openfaas
```

### Kubernetes

```bash
# Check OpenFaaS pods
kubectl get pods -n openfaas
kubectl get pods -n openfaas-fn

# Check services
kubectl get svc -n openfaas

# View function logs
kubectl logs -n openfaas-fn -l faas_function=hello-python
```

---

## GitOps Workflow

1. **Modify** application manifests in this repository
2. **Commit & Push** changes to GitHub
3. **ArgoCD detects** changes automatically (or manual sync)
4. **Kubernetes** resources are updated

For OpenFaaS functions with GitOps:
- Store function source in `app/demo/openfaas-fn/`
- Use CI/CD to build and push images on commit
- ArgoCD syncs the function CRDs (if using operator mode)

### References
- https://www.openfaas.com/blog/bring-gitops-to-your-openfaas-functions-with-argocd/
- https://rpi4cluster.com/k3s-openfaas/
