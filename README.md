# source of * arr apps
- https://gitlab.com/k3s-media/k3s-media-server/-/tree/main/media-server?ref_type=heads

# source of plex
- kustomize https://git.tdude.co/tristan/infrastructure/-/blob/master/k8s-235/apps/mediaserver/base/resources/kube-plex.yaml?ref_type=heads
- kustomize https://github.com/bjw-s/home-ops/blob/main/kubernetes/main/apps/media/plex/app/helmrelease.yaml
- helm plex https://artifacthub.io/packages/helm/alekc/plex

# optional helm chart source
- https://github.com/bjw-s/helm-charts

# kustomize deployemnt 
```bash
kubectl kustomize ./app/tools/ --enable-helm | kubectl apply -f -
```

# argocd k8s manifest deployment
```bash
TBD k3s-proxmox-terraform-ansible/roles/postconfig/base_argocd/tasks/argocd-cm.yaml 
sh ./argocd.sh
```

# argocd openfaas functions deployment sample

```bash
https://www.openfaas.com/blog/bring-gitops-to-your-openfaas-functions-with-argocd/
https://rpi4cluster.com/k3s-openfaas/

arkade install openfaas
PASSWORD=$(kubectl get secret -n tools basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin

Create new functions
faas-cli template pull
faas-cli template store pull python3-http
faas-cli new --lang python3 hello-python

Build functions
faas-cli build

Publish functions
faas-cli publish

argocd app create argocd-apps-of-apps -f "app/openfaas/argocd-apps-of-apps.yaml --upsert


```