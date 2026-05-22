---
name: repomix-sync
description: Keep argocd repomix output aligned with the current repo state for AI-assisted analysis. Use when manifests or scripts changed materially and repomix-based workflows need fresh context, or when a scoped repomix pack is needed for cluster, functions, or scripts review.
---

# Repomix Sync

Use this skill when repomix output must reflect current code.
This is workflow, not architecture.

## Key Files

* `repomix.config.json`
* generated `repomix-output*.md`
* changed manifest or script paths that need to be represented in the pack

## Workflow

1. Decide whether full repo or scoped pack is needed.
   Prefer the default repo-local config for general analysis.
   Prefer scoped `--include` patterns when the task is limited to one area.

2. Regenerate repomix output after meaningful changes.
   Meaningful changes include:
   * new manifests or components
   * deleted manifests or components
   * renamed resources or files
   * changed ArgoCD Application specs
   * structural refactors

3. Use repo root as working directory.
   Default command:
   * `repomix .`

4. Use scoped commands when smaller context is better.
   Examples:
   * cluster manifests: `repomix . --include "app/k3s-system/**" -o repomix-cluster.md`
   * serverless functions: `repomix . --include "app/fission-fn/**,app/openfaas-fn/**" -o repomix-functions.md`
   * scripts: `repomix . --include "scripts/**" -o repomix-scripts.md`

5. Treat generated packs as disposable snapshots.
   They are current only for the repo state at generation time.
   Regenerate instead of assuming they stay fresh.

## Repo-Specific Notes

* `repomix.config.json` intentionally excludes noisy or sensitive paths such as env files, direnv cache, and generated repomix outputs.
* The default repo pack is optimized to open reliably in editors by using split output.

## What To Avoid

* trusting stale `repomix-output*.md` after manifests changed
* weakening ignore rules to include secrets or local env files
* using full-repo packs when a narrow scoped pack would be clearer
* committing generated repomix output unless the task explicitly requires it

## Validation

After regeneration:

* confirm the expected `repomix-output*.md` files exist
* if the output is unusually large, prefer a scoped command
* if repomix output and repo code disagree, trust the repo and regenerate
