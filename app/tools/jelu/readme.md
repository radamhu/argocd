Kubernetes (Helm)
An unofficial Helm-Chart to deploy Jelu to Kubernetes is available here:

https://artifacthub.io/packages/helm/tibuntu/jelu

-- https://akuity.io/blog/argo-cd-helm-values-files/

- Solution 1: Helm Umbrella Chart
  - add repo https://github.com/jameswynn/helm-charts/tree/main manually to argocd project
  - values.yaml
  - Charts.yaml
- Solution 2: App of Apps Pattern with Values in Application Manifest
- Solution 3: Multiple Sources for Applications (Beta Feature)


-- Install with Kubernetes Manifests

https://gethomepage.dev/latest/configs/kubernetes/#automatic-service-discovery



