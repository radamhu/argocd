# Fission Hello App

Simple repo-local Fission example.

Pattern matches `app/openfaas-fn/`:

* keep source code in this folder
* keep one deploy manifest beside it
* apply with `kubectl`

## Files

```text
app/fission-fn/
├── hello-python/
│   └── user
└── function.yaml
```

`hello-python/user` is the Python source file.

`function.yaml` creates:

* `Environment` named `python`
* `Package` named `hello-python-pkg`
* `Function` named `hello-python`
* `HTTPTrigger` on `/hello-python`

## Deploy

```bash
kubectl apply -f app/fission-fn/function.yaml
```

## Invoke

Plain HTTP redirects to HTTPS:

```bash
curl -i http://fission.192.168.0.10.sslip.io/hello-python
```

Real function response:

```bash
curl -k https://fission.192.168.0.10.sslip.io/hello-python
```

Expected response:

```text
Hello from Fission!
```

## Update Code

1. Edit `app/fission-fn/hello-python/user`.
2. Re-encode the file:

```bash
base64 -w0 app/fission-fn/hello-python/user
```

3. Replace `spec.deployment.literal` in `app/fission-fn/function.yaml`.
4. Update the checksum annotation in the manifest so code changes are obvious in Git:

```bash
sha256sum app/fission-fn/hello-python/user
```

5. Re-apply:

```bash
kubectl apply -f app/fission-fn/function.yaml
```

## Verify

```bash
kubectl get environment,package,function,httptrigger -n fission-function
kubectl get pods -n fission-function
curl -k https://fission.192.168.0.10.sslip.io/hello-python
```
