
This is a bjw's helm based application :)
https://bjw-s.github.io/helm-charts/docs/app-template/

-- https://gethomepage.dev/main/installation/k8s/

Install with Helm

-- Create sealed-secrets first
k create secret generic tools-ns-sealed-secret --namespace=tools --dry-run=client --from-literal=sonarr-api=
--from-literal=radarr-api=
--from-literal=qbittorrent-pwd=
--from-literal=proxmox_api_token_id= 
--from-literal=proxmox_api_token_secret=
--from-literal=pihole_key=
--from-literal=unifi_username=
--from-literal=unifi_password=
--from-literal=argocd_homepage_user_token=
--from-literal=grafana_key=
--from-literal=hassio_access_token=
 -o yaml > ./mysecret.yaml

wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.16.0/kubeseal-linux-amd64 -O /usr/local/bin/kubeseal
chmod 755 /usr/local/bin/kubeseal

kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml --secret-file mysecret.yaml --sealed-secret-file tools-ns-sealed-secret.yaml

kubectl create -f tools-ns-sealed-secret.yaml

kubectl get secret -n tools tools-ns-sealed-secret -o yaml

rm ./mysecret.yaml

-- https://akuity.io/blog/argo-cd-helm-values-files/

- Solution 1: Helm Umbrella Chart
  - add repo https://github.com/jameswynn/helm-charts/tree/main manually to argocd project
  - values.yaml
  - Charts.yaml
- Solution 2: App of Apps Pattern with Values in Application Manifest
- Solution 3: Multiple Sources for Applications (Beta Feature)


-- Install with Kubernetes Manifests

https://gethomepage.dev/latest/configs/kubernetes/#automatic-service-discovery



