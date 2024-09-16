
# https://jaehong21.com/posts/k3s/06-sealed-secrets/

## Install, kubeseal controller on k3s
```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update

helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets

helm status -n kube-system sealed-secrets
```

## irst, let’s create an example secret with kubectl command, with value below, and create an file named mysecret-1.yaml.

```bash
kubectl create secret generic mysecret-1 --dry-run=client --from-literal=dbpassword=password --from-literal=secondkey=secondValue --from-literal=thirdkey=thirdValue -o yaml > mysecret-1.yaml

```

## When using kubeseal command, it must be the environment with kubectl master. Then, it will fetch the certificate(public key) for encryption and export with sealed secret yaml file.

```bash
kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml --secret-file mysecret-1.yaml --sealed-secret-file mysealedsecret-1.yaml
```

## Created encrypted mysealedsecret-1.yaml file will be like below. As it is encrypted, it is not possible to decode it with base64, and also safe to store on git.

```bash
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: mysecret-1
  namespace: default
spec:
  encryptedData:
    dbpassword: AgBpKKeEP7xHvP1oj/5Bc/6kzCTf91+xBl+LzZLsTrzwKkwDIXE2nuCRt/eSeSl04CvD8EOiZsmlPemZ3dbN6JXrLtilYdSL/QDWv0/6ijGfce5NC+zneGFrY+f9skqJWzhG4hQcwGvwJ/NpEO5TlPy9DVEmhXHouAK7/jSZMzO60GVP+dNgMAIknXWZFx4oVk9wbVUmmTCJG/LdFAaNCNxKtpVc1NCr6PxPE9pugroZ3BtpsAwdd7juDHYWqyVw9MW+fWNOw9ZRcScpxX1LXc5vQS9o3CuZpKTsJXe/fGxRAl9gsa+QOXK1bp2Yh7ODhCJBpM6GW7kxOncspn/O0ATiKoq4M3HiXOmsE6pJWx6K5cesW5Tf1/BGUMzkba8cglEo3GrP9acVot59+oT0mwNLnArPygR0ZRQyLX4e+eFv3rkKFm7Z2wFq+5YrATZ+LO/0qTzbdztk/iUwcLXg4kPK3df8vZlw36wsQ175jo33alkI+B6XwBvSjJVlK9nWTp5Bz4dthbEvsU8Jm78FMspF/6uxoF/Sa8Rf0u473aJawRAUYuBvw7Ay3y6K9WhIkf814Yenw4gYIQ+O+zHEbCT+0gTNWttApEqqBTPwLQtorhjnJUCmDQxECbuzUxehoO/948xTEULu6f+sC5IBbkPM9KNY3hu+f39DfRC6+M44QKaiUzyE8FXgt2D7xgvB0UTCzRSXpj55FQ==
    secondkey: AgAdg/xWDmTWfT11DdAbMvD19R9/tCL96P1iAws/0+KZaTVEc4+yuZrCHqgIwoc4fbkIOl9n9lzYn7CuRcptt9s+zXUHg/7RR22XHUmS0TuLmjv1mnqdVST3L2BZfBzLb6tXy0SVPFohe+c9G6UbOavMNrELhTYd1RMqicg88kGSVb5vp4kOUQ6E9DLEls/G9O8WyoQSowqVK5tA0vPSMjdTjV7fcfaaiR1a4uKSxUWvLf+eloEOWTsW3bPW06YwQ6hkLNX/hlQ2/NpOih0OxhOr8FqKfBTlHfri6xzPXQ38qXSvZFjDCYdCFQ7R7InW1jJWoqISNMHG5NK77G33wCaQ2Zp+k12d8YWBh/lWNoLTIzO560HvRUr414KtSOMnxg+HEZgkLMUWus/JULVMB8lCtk+5eXHuhFIwM9s4pCCbQBobv9Jltm+Og5ppTk/LFQLAUoLqQyMQVmaz4ugV/peiXAT5jw4T5aIwqS9AQx/kiUD5b+1mXSapl1lsyEypCkTNjkGpAleRJUvzjU66nRV/nJBLdNT23c1sFgJ9ZJZ3IAb9MBGi6ix62qlN1FEQsXLMEckX99jDKw2dpZJNQyERwNOB9CzkjM4cYAsjXqCYfAS7rsHin+VybZKcez3wkPKl9PXswEzqjOfTbVS8fISU7ZvWn4rRqC9Yrcg7JWC0Abv+f2yO8x524fw/hGTvJ4SubQe6HD+H9Md7yg==
    thirdkey: AgB0BNkNJ6Iop5GEUTkFs7G7WberMH6EKzvjcbb4KaSMcTA0vR093srJueifK81ZJoKDqlJJQJoETrcmopZhRATW9xMx+ANYPcWhvthNMEYfPSENgvUHtRR7rJHhfkwGfWfWdrGV1WYz61uLSHL6gxAOa4NNiWF373VX52NyT9EZAFIjSw1M2BKW9C0kJ+MO5ziDstkfYx8a0VJfvLJ5s4bKhj86SNAWPisCgRzUCCbQfIKBS1w7XTU5jTDISdnnmVVOqb4icqLBxi6TNKhDeCqGJtOcwMNVh36H5nNub/1GW64uNvnHGpP1tNbI3MlsBGJ3FNkoR18GKTKIgrQwatQzTKJZdILzo7WCtnn+SwwXbKS54wPTqGX3ZQak/l3kbqlkJixWOEIz4EF6UbsLuldFlZFy32HBdVO8+Nurb8b4bXVapEef6Ik739ykKKMzFioxuEnp3BZjKUNbKfvoDdH3+gpObF0FmKRFMB2AU+OZZV2aaJHBMR0C3nrGyKDvbvlt7J0IIwgrd/RaOTZas+mLAKY5DXMuy9S8nvWyF2C7asntbnmpjI3YZ46LGiDEYihexJUpcJTHyIMQ2hpKGKNxR9RIZf4AUvz4T6Osn+vIbd0slos7aibiObDY2e8iVjfVtUPGe6HsOh4BJ1mc/YL3+0App8EV6FIxxe4fo+nchUff8iKA44RrRDf5MSvQFFQhptmwvk16JM9t
  template:
    metadata:
      creationTimestamp: null
      name: mysecret-1
      namespace: default
```

```bash
kubectl create -f mysealedsecret-1.yaml

# you can check decrypted secret also
kubectl get secret mysecret-1 -o yaml

+) or you can create an sealed secret in one command like below

kubectl create secret generic mysecret-1 --namespace=default --dry-run=client --from-literal=dbpassword=password --from-literal=secondkey=secondValue --from-literal=thirdkey=thirdValue -o yaml | \
    kubeseal \
      --controller-name=sealed-secrets-controller \
      --controller-namespace=kube-system \
      --format yaml > mysealedsecret-1.yaml

# you can check decrypted secret also
kubectl get secret mysecret-1 -o yaml

```

# backup n restore

https://rpi4cluster.com/k3s-sealed-secrets/

