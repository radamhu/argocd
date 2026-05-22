# AGENTS.md

Canonical repo rules.

If anything conflicts with this file, this file wins.

## 1. Scope

Applies to:

* humans
* AI agents
* all branches
* all phases

This file defines repo-wide invariants only.
Task workflows, debugging playbooks, tool-specific usage, and step-by-step procedures belong in `SKILL.md`.

## 2. Architecture

GitOps monorepo. Git is the source of truth for cluster state.

Rules:

* single git repository
* k3s is the target cluster
* ArgoCD drives all deployments — no manual `kubectl apply` in production
* Kustomize is the preferred composition tool
* HelmChart (k3s built-in) for upstream charts
* Sealed Secrets for all secret material committed to Git
* no over-engineering
* no new platform component without ADR

Hard constraints:

* no plain Kubernetes Secret manifests committed to Git
* only SealedSecret manifests are committed
* sealed secrets are cluster-specific — regenerate on cluster rebuild
* no manual schema/infra changes outside Git
* no TODO without issue reference
* no silent breaking changes to ArgoCD Application specs

Repo layout:

```
app/
  k3s-system/         # cluster-level ArgoCD Applications and manifests
    <component>/      # one folder per component (argocd, cert-manager, fission, …)
  fission-fn/         # Fission serverless function source + deploy manifests
  openfaas-fn/        # OpenFaaS serverless function source + stack.yaml
scripts/              # operational helper scripts (sealed secret creation, etc.)
```

## 3. Manifest Contracts

ArgoCD Application manifests (`argocd-<name>.yaml`) must:

* live under `app/k3s-system/<component>/`
* specify `spec.project`, `spec.source`, and `spec.destination`
* use a `syncPolicy` consistent with the component's criticality

Kustomization files must:

* list all resources explicitly — no glob patterns
* be placed beside the manifests they compose

When adding a new component:

1. Create `app/k3s-system/<component>/` folder
2. Add ArgoCD Application manifest `argocd-<component>.yaml`
3. Add any supporting manifests (Namespace, Certificate, Ingress, etc.)
4. Add Kustomization if composing multiple resources
5. Register the Application with ArgoCD via `argocd.sh` or `kubectl apply`

Breaking changes to an existing Application (source repo, path, destination namespace) require:

* deliberate review — ArgoCD may delete and recreate managed resources
* `CHANGELOG.md` update

## 4. Dependencies

* upstream charts pinned via `HelmChart.spec.version`
* Renovate manages version bumps (`renovate.json`)
* serverless function dependencies declared in `requirements.txt` (OpenFaaS) or equivalent
* no hidden imports in function handlers

## 5. Configuration and Secrets

* no plain secrets in Git — ever
* all secret material goes through Sealed Secrets (`kubeseal`)
* sealed secrets are namespace-scoped and cluster-scoped — document scope in the manifest
* helper scripts in `scripts/` handle interactive secret creation
* `.envrc` (direnv) is the local credentials store — already in `.gitignore`
* cluster-level config (endpoints, namespaces) belongs in manifests, not in scripts

## 6. Cluster Components

Current managed components:

| Component       | Namespace      | Managed by         |
| --------------- | -------------- | ------------------ |
| argocd          | argocd         | HelmChart / manual |
| cert-manager    | cert-manager   | ArgoCD             |
| sealed-secrets  | kube-system    | ArgoCD             |
| reflector       | kube-system    | ArgoCD             |
| reloader        | kube-system    | ArgoCD             |
| eraser          | kube-system    | ArgoCD             |
| fission         | fission        | ArgoCD             |
| openfaas        | openfaas       | ArgoCD             |

Rules:

* each component owns its namespace — no cross-namespace resource ownership
* cert-manager issues all TLS certificates via `Certificate` + `ClusterIssuer`
* Traefik is the ingress controller — all Ingress manifests use `ingressClassName: traefik`
* HTTP → HTTPS redirect implemented via Traefik `Middleware` + dual Ingress pattern

## 7. Build and Release

* changes merged to default branch trigger ArgoCD sync
* CI (GitHub Actions) runs pre-commit checks on every push
* linting enforced via pre-commit

Linting baseline:

* YAML: `yamllint` (via pre-commit)
* Shell: `shellcheck` (via pre-commit)
* general: `pre-commit/pre-commit-hooks` (trailing whitespace, end-of-file, etc.)

Serverless functions:

* OpenFaaS: `faas-cli build/push/deploy` against `app/openfaas-fn/stack.yaml`
* Fission: `kubectl apply -f app/fission-fn/function.yaml` after re-encoding source

## 8. Runtime

* readiness and liveness probes defined by upstream Helm charts — do not override without justification
* `Certificate` resources must reference a valid `ClusterIssuer`
* TLS secrets managed by cert-manager — do not create manually
* all workloads run as non-root where chart permits

## 9. Logging

* logs consumed via `kubectl logs` or forwarded to Grafana Cloud via OTEL collector
* OTEL collector credentials stored as SealedSecret
* no ephemeral debug logging committed to manifests

## 10. Testing

Test what can break silently:

* serverless function handlers — unit tests beside the handler (`handler_test.py`, `tox.ini`)
* sealed secret creation scripts — manual smoke test after cluster changes

Do not test:

* ArgoCD sync behavior — that is ArgoCD's job
* Helm chart rendering — upstream responsibility
* manifest YAML syntax — handled by pre-commit linting

## 11. GitOps Delivery Chain

Delivery chain (Git → cluster):

1. **Git commit**: manifest change merged to default branch
2. **ArgoCD sync**: detects drift, applies manifests to cluster
3. **Kustomize/Helm**: ArgoCD renders the final manifests
4. **Kubernetes**: reconciles desired state
5. **cert-manager / sealed-secrets**: react to Certificate / SealedSecret resources

When modifying the chain:

* verify ArgoCD Application `source.path` matches folder layout
* verify `targetRevision` is intentional (branch vs tag vs SHA)
* verify namespace exists before ArgoCD tries to apply resources
* SealedSecret must be re-sealed if cluster sealed-secrets key rotates

## 12. AI Guardrails

Be concise. Sacrifice grammar for the sake of consision.

AI may not invent:

* cluster components
* namespaces
* ArgoCD Applications
* SealedSecret values

AI must:

* follow repo structure (`app/k3s-system/<component>/`, `app/fission-fn/`, `app/openfaas-fn/`)
* ask for clarification when required context is missing
* not guess cluster-specific values (endpoints, namespaces, chart versions)
* use subagents when an agent is actively working on the repo and delegation materially helps progress
* capture recurring project-specific workflows in `.github/skills/` for future reuse instead of re-deriving them repeatedly

## 13. MCP Usage

`context7` MCP is the default source for external library and framework docs. Any documentation lookup, cross-repo coordination, library API reference

Use it when:

* verifying library APIs or config
* checking current framework conventions
* confirming version-specific behavior
* looking up official examples before implementation

Rules:

* prefer `context7` over memory for non-trivial external APIs
* use `context7` before adding or changing dependency-specific code
* do not use `context7` to invent repo-specific architecture or behavior
* repo code and this `AGENTS.md` win over external examples

`microsoft/playwright-mcp` MCP may be used for browser testing only.

Use it when:

* running E2E tests
* validating user flows in browser
* reproducing UI bugs
* checking selectors, navigation, forms, dialogs, and network-driven UI behavior

Rules:

* use `microsoft/playwright` only for testing use cases
* do not use it as a source of business logic or architecture decisions
* prefer it for E2E and browser-level verification, not unit testing
* if UI behavior conflicts with backend contract, OpenAPI and backend tests remain the source of truth

## 14. Repomix

`repomix` is the default repo-packing tool for AI context export.

Rules:

* repo-local `repomix.config.json` is the source of truth for default repomix behavior
* prefer `repomix .` from repo root over ad hoc one-off defaults
* when using repomix-based AI analysis, regenerate repomix output after meaningful repo changes before asking the AI to analyze current code
* prefer scoped `--include` patterns for task-specific packs instead of packing the whole monorepo when not needed
* do not weaken ignore rules in ways that include secrets, local env files, caches, logs, or bulky generated artifacts
* treat repomix output files as disposable artifacts unless a task explicitly requires committing them
* operational repomix workflow belongs in `.github/skills/repomix-sync/SKILL.md`
* if repomix output conflicts with repo reality, repo code and this `AGENTS.md` win
