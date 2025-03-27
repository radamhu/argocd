
# Sealed secrets + kubeseal

https://rpi4cluster.com/k3s-sealed-secrets/

https://jaehong21.com/posts/k3s/06-sealed-secrets/

Install, kubeseal controller on k3s

```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update
helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets
helm status -n kube-system sealed-secrets
```

let’s create an example secret with kubectl command

```bash
kubectl create secret generic secret-sql-password -n test --dry-run=client --from-literal=MYSQL_PASSWORD=password -o yaml > secret-sql-password.yaml

```

Using kubeseal command for encryption

```bash
kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml --secret-file secret-sql-password.yaml --sealed-secret-file mysealed-secret-sql-password.yaml


---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: secret-sql-password
  namespace: test
spec:
  encryptedData:
    MYSQL_PASSWORD: AgBiU7yk7bFThHU0Tq+uHzFQ/R6T6RS1b6lylLPDfFy4Xvk0YS+Ou6rED1FxE1ShhziLE8a7am0fbiA2YuJMSCMLAqc2VYcU3p3LS0QKXdWKelao7h5kLwue7rEnCnuKLSZXHuU6DV/yCBYIcCCz88dBmzE8ga1TARLsFRrZmq2EWgU/ON57tIexCEAyztW1Fj7MJ4Z06pcSSAwY2v0yZ8UNo1qzdmTfkOg0sMXdaFwF9Nga83MPeXfyKdfiH6kAW+LjUbpWi4JHEK7elZswRCBtU6caKt2sxfmue38UbQw8AXL5TmECqwttuKADWictIfWWhCYnyaO7DQm7+a2kfKUaUHZlw8X3vJtoiXAO/G2ByJBc6sR6w1eRZKDySgK8MqhGi8GCD5oOaE4thKwnx31gGWcVTTDjaD0/YgnneLYmKoogJdMP6NdjzZ6BM84qRlB9LreJi1Qnf0uJZE56Zg3x/cEFJv2+X29gmwvX24gixgD6yrnxpA+GBbjeKXfPSjqlTpXSxJWwFWd1+H1Fb4FWVs6m1PxehsrHDbVTk8kGVXDzV1KK9EjF+CIxQPhGEQTUVq4qMmLAnPKw8HQYmh73v1K/0dU5WkioCdZyFVlEkN/BmfOCddIUh0wufm5QYSq3nlXYL4Ogw0VVcqNiKIeHb6++tgA1t1EbwXz9gfojnd9Ue6T+85SfZVNZI6Xkc/MpEGEqX29/p2M=
  template:
    data: null
    metadata:
      creationTimestamp: null
      name: secret-sql-password
      namespace: test
```

Let’s deploy the generated YAML file using kubectl.

```bash
kubectl apply -f mysealedsecret-1.yaml
```

Let’s using secret in k8s resources, e.g. job below:

```bash
apiVersion: batch/v1
kind: Job
metadata:
  name: kubeseal-demo-job
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: mysql-client
          image: mysql:5.7
          env:
            - name: MYSQL_HOST
              value: demo-server-udhan.mysql.database.azure.com
            - name: MYSQL_ROOT_USER
              value: testuser@demo-server-udhan
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: secret-sql-password
                  key: MYSQL_PASSWORD
          command: 
            - "bin/bash"
            - "-c"
            - "mysql -h $MYSQL_HOST -u $MYSQL_ROOT_USER -p${MYSQL_ROOT_PASSWORD} -e 'SHOW databases;'"
```