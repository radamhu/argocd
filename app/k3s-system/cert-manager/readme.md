# TODO

## OPTION 1 : not used

https://dev.to/ileriayo/adding-free-ssltls-on-kubernetes-using-certmanager-and-letsencrypt-a1l

```bash
    solvers:
    - http01:
        ingress:
          class: traefik 
```

## OPTION 2 : its used 

https://nolifelover.medium.com/create-cert-manager-clustterissuer-with-cloudflare-for-automate-issue-and-renew-lets-encrypt-ssl-4877d3f12b44

```bash
    solvers:
    - dns01:
        cloudflare:
          email: <Your Email>
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token
```

the argocd-cert-manager.yaml is not used

because cert-manager is deployed by iac repo