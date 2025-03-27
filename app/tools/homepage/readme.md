
# Homepage

## This is a bjw's helm based application :)

https://bjw-s.github.io/helm-charts/docs/app-template/

https://gethomepage.dev/main/installation/k8s/

## Creating Sealed secrets

```bash
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

kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml --secret-file mysecret.yaml --sealed-secret-file tools-ns-sealed-secret.yaml

kubectl create -f tools-ns-sealed-secret.yaml

kubectl get secret -n tools tools-ns-sealed-secret -o yaml

```

## Apply Sealed secrets

```bash
TODO e.g. in homepage-cm.yaml
```


