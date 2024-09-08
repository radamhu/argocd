https://colinwilson.uk/2022/08/22/secrets-management-with-external-secrets-argo-cd-and-gitops/#create-a-secret-containing-your-secret-managers-credentials

helm repo add external-secrets https://charts.external-secrets.io

helm install external-secrets \
   external-secrets/external-secrets \
  -n external-secrets \
  --create-namespace \
  --set installCRDs=true

add helm repo to argocd on GUI

argocd login argocd.local
Username: admin
Password:
'admin:login' logged in successfully
Context 'argocd.local' updated


argocd app create external-secrets \
 --repo https://charts.external-secrets.io \
 --helm-chart external-secrets \
 --revision 0.5.9 \
 --dest-namespace external-secrets \
 --sync-option CreateNamespace=true \
 --dest-server https://kubernetes.default.svc

argocd app sync external-secrets

