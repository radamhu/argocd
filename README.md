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

# argocd deployment
```bash
TBD k3s-proxmox-terraform-ansible/roles/postconfig/base_argocd/tasks/argocd-cm.yaml 
sh ./argocd.sh
```