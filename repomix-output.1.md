This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: .venv/**, .direnv/**, repomix-output*, .env*, .codex*
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.agents/
  skills/
    repomix-explorer/
      SKILL.md
.github/
  ISSUE_TEMPLATE/
    bug_report.yml
    feature_request.yml
  skills/
    repomix-sync/
      agents/
        openai.yaml
      SKILL.md
  workflow/
    main.yml
  PULL_REQUEST_TEMPLATE.md
app/
  fission-fn/
    hello-python/
      user
    function.yaml
    README.md
  k3s-system/
    argocd/
      certificate.yaml
      ingress.yaml
      install.yaml
      selfsigned-issuer.yaml
    cert-manager/
      argocd-cert-manager.yaml
    eraser/
      argocd-eraser.yaml
    fission/
      argocd-fission-crds.yaml
      argocd-fission.yaml
      certificate.yaml
      ingress-http-redirect.yaml
      ingress.yaml
      kustomization.yaml
      namespaces.yaml
    openfaas/
      argocd-openfaas.yaml
      certificate.yaml
      ingress.yaml
      kustomization.yaml
      namespaces.yaml
    reflector/
      argocd-reflector.yaml
    reloader/
      argocd-reloader.yaml
    sealed-secrets/
      argocd-sealed-secrets.yaml
  openfaas-fn/
    hello-python/
      __init__.py
      handler_test.py
      handler.py
      requirements.txt
      tox.ini
    stack.yaml
scripts/
  create-ghcr-sealed-secret.sh
  create-grafana-otel-sealed-secret.sh
  README.md
  update-repomix.sh
.cz.toml
.editorconfig
.gitignore
.pre-commit-config.yaml
AGENTS.md
argocd.sh
LICENSE
README.md
renovate.json
repomix.config.json
skills-lock.json
test.json
```

# Files

## File: .agents/skills/repomix-explorer/SKILL.md
````markdown
---
name: repomix-explorer
description: "Use this skill when the user wants to analyze or explore a codebase (remote repository or local repository) using Repomix. Triggers on: 'analyze this repo', 'explore codebase', 'what's the structure', 'find patterns in repo', 'how many files/tokens'. Runs repomix CLI to pack repositories, then analyzes the output."
---

You are an expert code analyst specializing in repository exploration using Repomix CLI. Your role is to help users understand codebases by running repomix commands, then reading and analyzing the generated output files.

## User Intent Examples

The user might ask in various ways:

### Remote Repository Analysis
- "Analyze the yamadashy/repomix repository"
- "What's the structure of facebook/react?"
- "Explore https://github.com/microsoft/vscode"
- "Find all TypeScript files in the Next.js repo"
- "Show me the main components of vercel/next.js"

### Local Repository Analysis
- "Analyze this codebase"
- "Explore the ./src directory"
- "What's in this project?"
- "Find all configuration files in the current directory"
- "Show me the structure of ~/projects/my-app"

### Pattern Discovery
- "Find all authentication-related code"
- "Show me all React components"
- "Where are the API endpoints defined?"
- "Find all database models"
- "Show me error handling code"

### Metrics and Statistics
- "How many files are in this project?"
- "What's the token count?"
- "Show me the largest files"
- "How much TypeScript vs JavaScript?"

## Your Responsibilities

1. **Understand the user's intent** from natural language
2. **Determine the appropriate repomix command**:
   - Remote repository: `npx repomix@latest --remote <repo>`
   - Local directory: `npx repomix@latest [directory]`
   - Choose output format (xml is default and recommended)
   - Decide if compression is needed (for repos >100k lines)
3. **Execute the repomix command** via shell
4. **Analyze the generated output** using pattern search and file reading
5. **Provide clear insights** with actionable recommendations

## Workflow

### Step 1: Pack the Repository

**For Remote Repositories:**
```bash
npx repomix@latest --remote <repo> --output /tmp/<repo-name>-analysis.xml
```

**IMPORTANT**: Always output to `/tmp` for remote repositories to avoid polluting the user's current project directory.

**For Local Directories:**
```bash
npx repomix@latest [directory] [options]
```

**Common Options:**
- `--style <format>`: Output format (xml, markdown, json, plain) - **xml is default and recommended**
- `--compress`: Enable Tree-sitter compression (~70% token reduction) - use for large repos
- `--include <patterns>`: Include only matching patterns (e.g., "src/**/*.ts,**/*.md")
- `--ignore <patterns>`: Additional ignore patterns
- `--output <path>`: Custom output path (default: repomix-output.xml)
- `--remote-branch <name>`: Specific branch, tag, or commit to use (for remote repos)

**Command Examples:**
```bash
# Basic remote pack (always use /tmp)
npx repomix@latest --remote yamadashy/repomix --output /tmp/repomix-analysis.xml

# Basic local pack
npx repomix@latest

# Pack specific directory
npx repomix@latest ./src

# Large repo with compression (use /tmp)
npx repomix@latest --remote facebook/react --compress --output /tmp/react-analysis.xml

# Include only specific file types
npx repomix@latest --include "**/*.{ts,tsx,js,jsx}"
```

### Step 2: Check Command Output

The repomix command will display:
- **Files processed**: Number of files included
- **Total characters**: Size of content
- **Total tokens**: Estimated AI tokens
- **Output file location**: Where the file was saved (default: `./repomix-output.xml`)

Always note the output file location for the next steps.

### Step 3: Analyze the Output File

**Start with structure overview:**
1. Search for file tree section (usually near the beginning)
2. Check metrics summary for overall statistics

**Search for patterns:**
```bash
# Pattern search (preferred for large files)
grep -iE "export.*function|export.*class" repomix-output.xml

# Search with context
grep -iE -A 5 -B 5 "authentication|auth" repomix-output.xml
```

**Read specific sections:**
Read files with offset/limit for large outputs, or read entire file if small.

### Step 4: Provide Insights

- **Report metrics**: Files, tokens, size from command output
- **Describe structure**: From file tree analysis
- **Highlight findings**: Based on grep results
- **Suggest next steps**: Areas to explore further

## Best Practices

### Efficiency
1. **Always use `--compress` for large repos** (>100k lines)
2. **Use pattern search (grep) first** before reading entire files
3. **Use custom output paths** when analyzing multiple repos to avoid overwriting
4. **Clean up output files** after analysis if they're very large

### Output Format
- **XML (default)**: Best for structured analysis, clear file boundaries
- **Plain**: Simpler to grep, but less structured
- **Markdown**: Human-readable, good for documentation
- **JSON**: Machine-readable, good for programmatic analysis

**Recommendation**: Stick with XML unless user requests otherwise.

### Search Patterns
Common useful patterns:
```bash
# Functions and classes
grep -iE "export.*function|export.*class|function |class " file.xml

# Imports and dependencies
grep -iE "import.*from|require\\(" file.xml

# Configuration
grep -iE "config|Config|configuration" file.xml

# Authentication/Authorization
grep -iE "auth|login|password|token|jwt" file.xml

# API endpoints
grep -iE "router|route|endpoint|api" file.xml

# Database/Models
grep -iE "model|schema|database|query" file.xml

# Error handling
grep -iE "error|exception|try.*catch" file.xml
```

### File Management
- Default output: `./repomix-output.xml`
- Use `--output` flag for custom paths
- Clean up large files after analysis: `rm repomix-output.xml`
- Or keep for future reference if space allows

## Communication Style

- **Be concise but comprehensive**: Summarize findings clearly
- **Use clear technical language**: Code, file paths, commands should be precise
- **Cite sources**: Reference file paths and line numbers
- **Suggest next steps**: Guide further exploration

## Example Workflows

### Example 1: Basic Remote Repository Analysis
```text
User: "Analyze the yamadashy/repomix repository"

Your workflow:
1. Run: npx repomix@latest --remote yamadashy/repomix --output /tmp/repomix-analysis.xml
2. Note the metrics from command output (files, tokens)
3. Grep: grep -i "export" /tmp/repomix-analysis.xml (find main exports)
4. Read file tree section to understand structure
5. Summarize:
   "This repository contains [number] files.
   Main components include: [list].
   Total tokens: approximately [number]."
```

### Example 2: Finding Specific Patterns
```text
User: "Find authentication code in this repository"

Your workflow:
1. Run: npx repomix@latest (or --remote if specified)
2. Grep: grep -iE -A 5 -B 5 "auth|authentication|login|password" repomix-output.xml
3. Analyze matches and categorize by file
4. Read the file to get more context if needed
5. Report:
   "Authentication-related code found in the following files:
   - [file1]: [description]
   - [file2]: [description]"
```

### Example 3: Structure Analysis
```text
User: "Explain the structure of this project"

Your workflow:
1. Run: npx repomix@latest ./
2. Read file tree from output (use limit if file is large)
3. Grep for main entry points: grep -iE "index|main|app" repomix-output.xml
4. Grep for exports: grep "export" repomix-output.xml | head -20
5. Provide structural overview with ASCII diagram if helpful
```

### Example 4: Large Repository with Compression
```text
User: "Analyze facebook/react - it's a large repository"

Your workflow:
1. Run: npx repomix@latest --remote facebook/react --compress --output /tmp/react-analysis.xml
2. Note compression reduced token count (~70% reduction)
3. Check metrics and file tree
4. Grep for main components
5. Report findings with note about compression used
```

### Example 5: Specific File Types Only
```text
User: "I want to see only TypeScript files"

Your workflow:
1. Run: npx repomix@latest --include "**/*.{ts,tsx}"
2. Analyze TypeScript-specific patterns
3. Report findings focused on TS code
```

## Error Handling

If you encounter issues:

1. **Command fails**:
   - Check error message
   - Verify repository URL/path
   - Check permissions
   - Suggest appropriate solutions

2. **Large output file**:
   - Use `--compress` flag
   - Use `--include` to narrow scope
   - Read file in chunks with offset/limit

3. **Pattern not found**:
   - Try alternative patterns
   - Check file tree to verify files exist
   - Suggest broader search

4. **Network issues** (for remote):
   - Verify connection
   - Try again
   - Suggest using local clone instead

## Help and Documentation

If you need more information:
- Run `npx repomix@latest --help` to see all available options
- Check the official documentation at https://github.com/yamadashy/repomix
- Repomix automatically excludes sensitive files based on security checks

## Important Notes

1. **Output file management**: Track where files are created, clean up if needed
2. **Token efficiency**: Use `--compress` for large repos to reduce token usage
3. **Incremental analysis**: Don't read entire files at once; use grep first
4. **Security**: Repomix automatically excludes sensitive files; trust its security checks

## Self-Verification Checklist

Before completing your analysis:

- Did you run the repomix command successfully?
- Did you note the metrics from command output?
- Did you use pattern search (grep) efficiently before reading large sections?
- Are your insights based on actual data from the output?
- Have you provided file paths and line numbers for references?
- Did you suggest logical next steps for deeper exploration?
- Did you communicate clearly and concisely?
- Did you note the output file location for user reference?
- Did you clean up or mention cleanup if output file is very large?

Remember: Your goal is to make repository exploration intelligent and efficient. Run repomix strategically, search before reading, and provide actionable insights based on real code analysis.
````

## File: .cz.toml
````toml
[tool.commitizen]
name = "cz_conventional_commits"
tag_format = "$version"
version_scheme = "semver"
version = "0.0.1"
update_changelog_on_bump = true
major_version_zero = true
````

## File: .editorconfig
````
# EditorConfig is awesome: http://EditorConfig.org
# Uses editorconfig to maintain consistent coding styles

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
charset = utf-8
end_of_line = lf
indent_size = 2
indent_style = space
insert_final_newline = true
max_line_length = 80
trim_trailing_whitespace = true

[*.{tf,tfvars}]
indent_size = 2
indent_style = space

[*.md]
max_line_length = 0
trim_trailing_whitespace = false

[Makefile]
tab_width = 2
indent_style = tab

[COMMIT_EDITMSG]
max_line_length = 0
````

## File: .github/ISSUE_TEMPLATE/bug_report.yml
````yaml
name: "🐛 Bug Report"
description: "Submit a bug report to help us improve"
title: "🐛 Bug Report: "
labels: ["type: bug"]
body:
  - type: markdown
    attributes:
      value: We value your time and effort to submit this bug report. 🙏
  - type: textarea
    id: description
    validations:
      required: true
    attributes:
      label: "📜 Description"
      description: "A clear and concise description of what the bug is."
      placeholder: "It bugs out when ..."
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    validations:
      required: true
    attributes:
      label: "👟 Reproduction steps"
      description: "How do you trigger this bug? Please walk us through it step by step."
      placeholder: "1. Go to '...'
                    2. Click on '....'
                    3. Scroll down to '....'
                    4. See error"
  - type: textarea
    id: expected-behavior
    validations:
      required: true
    attributes:
      label: "👍 Expected behavior"
      description: "What did you think should happen?"
      placeholder: "It should ..."
  - type: textarea
    id: actual-behavior
    validations:
      required: true
    attributes:
      label: "👎 Actual Behavior with Screenshots"
      description: "What did actually happen? Add screenshots, if applicable."
      placeholder: "It actually ..."
  - type: dropdown
    id: operating-system
    attributes:
      label: "💻 Operating system"
      description: "What OS is your app running on?"
      options:
        - Linux
        - MacOS
        - Windows
        - Something else
    validations:
      required: true
  - type: input
    id: node-version
    validations:
      required: true
    attributes:
      label: "🤖 Node Version"
      description: >
        What Node version are you using?
  - type: textarea
    id: additional-context
    validations:
      required: false
    attributes:
      label: "📃 Provide any additional context for the Bug."
      description: "Add any other context about the problem here."
      placeholder: "It actually ..."
  - type: checkboxes
    id: no-duplicate-issues
    attributes:
      label: "👀 Have you spent some time to check if this bug has been raised before?"
      options:
        - label: "I checked and didn't find similar issue"
          required: true
  - type: dropdown
    attributes:
      label: Are you willing to submit PR?
      description: This is absolutely not required, but we are happy to guide you in the contribution process. Find us in help-needed channel on [Discord](https://discord.gitroom.com)!
      options:
        - "Yes I am willing to submit a PR!"
````

## File: .github/ISSUE_TEMPLATE/feature_request.yml
````yaml
name: 🚀 Feature
description: "Submit a proposal for a new feature"
title: "🚀 Feature: "
labels: [feature]
body:
  - type: markdown
    attributes:
      value: |
        We value your time and efforts to submit this Feature request form. 🙏
  - type: textarea
    id: feature-description
    validations:
      required: true
    attributes:
      label: "🔖 Feature description"
      description: "A clear and concise description of what the feature is."
      placeholder: "You should add ..."
  - type: textarea
    id: pitch
    validations:
      required: true
    attributes:
      label: "🎤 Why is this feature needed ?"
      description: "Please explain why this feature should be implemented and how it would be used. Add examples, if applicable."
      placeholder: "In my use-case, ..."
  - type: textarea
    id: solution
    validations:
      required: true
    attributes:
      label: "✌️ How do you aim to achieve this?"
      description: "A clear and concise description of what you want to happen."
      placeholder: "I want this feature to, ..."
  - type: textarea
    id: alternative
    validations:
      required: false
    attributes:
      label: "🔄️ Additional Information"
      description: "A clear and concise description of any alternative solutions or additional solutions you've considered."
      placeholder: "I tried, ..."
  - type: checkboxes
    id: no-duplicate-issues
    attributes:
      label: "👀 Have you spent some time to check if this feature request has been raised before?"
      options:
        - label: "I checked and didn't find similar issue"
          required: true
  - type: dropdown
    id: willing-to-submit-pr
    attributes:
      label: Are you willing to submit PR?
      description: This is absolutely not required, but we are happy to guide you in the contribution process. Find us in help-needed channel on [Discord](https://discord.gitroom.com)!
      options:
        - "Yes I am willing to submit a PR!"
````

## File: .github/skills/repomix-sync/agents/openai.yaml
````yaml
interface:
  display_name: "Repomix Sync"
  short_description: "Keep repomix output aligned with current ArgoCd code."
  default_prompt: "Use this skill when ArgoCd repomix output must be regenerated or scoped for AI-assisted analysis."
````

## File: .github/skills/repomix-sync/SKILL.md
````markdown
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
````

## File: .github/workflow/main.yml
````yaml
name: GitHub Actions Demo
run-name: ${{ github.actor }} is testing out GitHub Actions 🚀
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - name: Discord notification
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        uses: Ilshidur/action-discord@master
        with:
          args: 'The project {{ EVENT_PAYLOAD.repository.full_name }} has been deployed.'
````

## File: .github/PULL_REQUEST_TEMPLATE.md
````markdown
- **What kind of change does this PR introduce?** (Bug fix, feature, docs update, ...)

- **Why was this change needed?** (You can also link to an open issue here)

- **Other information**:
````

## File: AGENTS.md
````markdown
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
````

## File: app/k3s-system/cert-manager/argocd-cert-manager.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://charts.jetstack.io
    chart: cert-manager
    targetRevision: v1.19.2
    helm:
      values: |
        crds:
          enabled: true
        prometheus:
          enabled: false
  destination:
    server: https://kubernetes.default.svc
    namespace: cert-manager
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
````

## File: app/k3s-system/reflector/argocd-reflector.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: reflector
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://emberstack.github.io/helm-charts
    chart: reflector
    targetRevision: 9.1.44
    helm:
      values: |
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            memory: 128Mi
  destination:
    server: https://kubernetes.default.svc
    namespace: reflector
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
````

## File: argocd.sh
````bash
#!/bin/bash

# Prompt for ArgoCD admin user password
read -p "Login to ARGOCD, type your password, otherwise type no: " ARGOCD_ADMIN_PWD

if [[ "$ARGOCD_ADMIN_PWD" != "no" ]]; then
    # Login to ArgoCd
    argocd login argocd.home.adaminformatika.hu --skip-test-tls --grpc-web --insecure --username admin --password "$ARGOCD_ADMIN_PWD"
fi

# Define the ArgoCD repository path
ARGOCD_REPO_PATH="$HOME/Github/argocd"  # Change this to the actual path

# Navigate to the ArgoCD repository
if [[ ! -d "$ARGOCD_REPO_PATH" ]]; then
    echo "Error: ArgoCD repository directory does not exist at $ARGOCD_REPO_PATH."
    exit 1
fi

cd "$ARGOCD_REPO_PATH" || { echo "Failed to enter ArgoCD repository directory."; exit 1; }

# Check if it's a valid Git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Error: Not a valid Git repository. Please check the directory."
    exit 1
fi

echo "Successfully navigated to ArgoCD repository."

# Prompt for ArgoCD app name
read -p "Enter ARGOCD_APP_NAME: " ARGOCD_APP_NAME

# Prompt for folder name
read -p "Enter NS_FOLDER_NAME: " NS_FOLDER_NAME

# Ask if the user has already pushed changes to Git
read -p "Have you already done 'git push'? (yes/no): " GIT_PUSHED


if [[ "$GIT_PUSHED" != "yes" ]]; then
    echo "You need to commit and push your changes before proceeding."

    # Ask for a commit message
    read -p "Enter a commit message: " COMMIT_MSG

    # Add, commit, and push the changes
    git add .
    git commit -m "$COMMIT_MSG"
    git push

    echo "Changes pushed to Git."
fi

# Create ArgoCD app with provided inputs
argocd app create "$ARGOCD_APP_NAME" -f "app/$NS_FOLDER_NAME/$ARGOCD_APP_NAME/argocd-$ARGOCD_APP_NAME.yaml" --upsert
````

## File: LICENSE
````
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "{}"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright {yyyy} {name of copyright owner}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
````

## File: renovate.json
````json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "baseBranches": ["main"],
  "extends": [
    "config:recommended"
  ],
  "flux": { "enabled": true },
  "kubernetes": { "enabled": true },
  "kustomize": { "enabled": true },
  "packageRules": [
    {
      "matchPackagePatterns": ["*"],
      "automerge": true
    }
  ]
}
````

## File: repomix.config.json
````json
{
  "output": {
    "filePath": "repomix-output.md",
    "style": "markdown",
    "splitOutput": 12000000
  },
  "ignore": {
    "customPatterns": [
      ".venv/**",
      ".direnv/**",
      "repomix-output*",
      ".env*",
      ".codex*"
    ]
  }
}
````

## File: scripts/update-repomix.sh
````bash
#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v repomix >/dev/null 2>&1; then
  echo "repomix is not installed or not on PATH" >&2
  echo "Install it first, then rerun this command." >&2
  exit 1
fi

# Remove prior generated packs so stale split parts do not linger.
rm -f repomix-output*.md repomix-output*.xml repomix-output*.json repomix-output*.txt

repomix .
````

## File: skills-lock.json
````json
{
  "version": 1,
  "skills": {
    "repomix-explorer": {
      "source": "yamadashy/repomix",
      "sourceType": "github",
      "skillPath": ".claude/skills/repomix-explorer/SKILL.md",
      "computedHash": "13eb769ba1b7446d46304e02ae77ea416eb49def9b651954957808d181ec9298"
    }
  }
}
````

## File: test.json
````json
"customManagers": [
  {
    "datasourceTemplate": "docker",
    "fileMatch": [
      "^app/(.*)-deployment.yaml$"
    ],
    "matchStrings": [
      "image: (.*)/(?<depName>.*?)/(?<currentValue>[^@]+)(@(?<currentDigest>sha256:[a-f0-9]+))?"
    ],
    "autoReplaceStringTemplate": "image: {{{depName}}}:{{{newValue}}}{{#if newDigest}}@{{{newDigest}}}{{/if}}"
  }
],
"hostRules": [
  {
    "hostType": "docker",
    "matchHost": "docker.io",
    "username": "radam",
    "encrypted": {
      "password": "wcFMA/xDdHCJBTolAQ//WaqpylYRhtzuxOB6X+oPtELp4NklyGdRKEqtf2BdT4JwO7un2eVOUqcBc87AnUmkBvKCGcn72Rua0BookR5GFan3mTXgH+8X6tDa7JVNFMl+rDUjJeZK4QHAVW/IBd5FA1UvuTPMve3FJ2kd5qCs5Ce2e4LjN/D1T+V0xOeWavnsl/h8PgvOK2vAt1n0kdcbt8OCdTkpznTlW8UeRt+90dzAv4b5qzafN6IDBMMuarekYjTLpHqWxG9mOOnV0vs6BrtwVJAzr9Da/ZIgMCNnsszL+jQUnVq5Xan8NPiyuCoGCOunZWUc9NIHH2MMNzUWjwvuDslr9n4X1pxuN4PHKF4uWgkzx574LQ6jPBwq3QKYCD5l6/sce92zpNklJW/frCH0G0yvUIXw+BqWTu9eodxxPIx1RbP+5XTw5A/RvDmaY0dePZyx9+xg1AW15rIQeiVRdtgL6nY8PmnVb2q7SpsCgX0xnnERQQSVJhDliNZ3WkS9l5ODP0vsn9IPDL2DgAXJgDf6+5ogyBlyaBAsnHj1cNO6/WmQkrMBv4jHMnrbDJIpsLQ9oDISzdgFaj+ON2musm9t6y0DcQwbC1aFNLOKLJLc3plkxXApwkUbLjIQ4sB9BFUBuq0q7/93MSt6T4/SNSMff5hndgYLGQZzbIBIFLuBMDdzYwUqsOxiNUbSYAHzZ90gpChWx6r4v6WXLAYrlN142sw5uOdvl4BBYnEji8R5uBxhM8dJIJz7+l+pqgKbAPzlqnJFSggARs6QQXwFeTl+03ZzNoGNDwMx10vDxvL95C1lKr+8SF61V7pejg"
    },
  }
],
````

## File: .pre-commit-config.yaml
````yaml
repos:
  # Ruff - Fast Python linter and formatter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      # Run the linter with auto-fix
      - id: ruff
        args: [--fix]
      # Run the formatter
      - id: ruff-format

  # Standard pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-toml
      - id: detect-private-key
        name: Detect private keys
      - id: check-added-large-files
        name: Check for large files
        args: ["--maxkb=500"]
      - id: check-yaml
        name: Check YAML syntax
        exclude: 'templates/.*\.yaml$'
      - id: check-json
        name: Check JSON syntax
      - id: end-of-file-fixer
        name: Fix end of files
      - id: trailing-whitespace
        name: Trim trailing whitespace
      - id: check-merge-conflict
        name: Check for merge conflicts

  # ESLint for JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$ # *.js, *.jsx, *.ts, *.tsx
        types: [file]
        additional_dependencies:
          - eslint@^8.0.0
          - "@typescript-eslint/parser@^6.0.0"
          - "@typescript-eslint/eslint-plugin@^6.0.0"

  # Prettier for code formatting
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml]

  - repo: local
    hooks:
      - id: repomix-sync
        name: repomix-sync
        entry: scripts/update-repomix.sh
        language: script
        pass_filenames: false
        files: ^(apps/|libs/|alembic/|tests/|docs/|bruno/|config/|scripts/|pyproject\.toml|package\.json|package-lock\.json|alembic\.ini|repomix\.config\.json|AGENTS\.md|\.github/skills/)
````

## File: app/fission-fn/hello-python/user
````
def main():
    return "Hello from Fission!"
````

## File: app/fission-fn/function.yaml
````yaml
apiVersion: fission.io/v1
kind: Environment
metadata:
  name: python
  namespace: fission-function
spec:
  poolsize: 1
  runtime:
    image: ghcr.io/fission/python-env
  version: 1
---
apiVersion: fission.io/v1
kind: Package
metadata:
  name: hello-python-pkg
  namespace: fission-function
  annotations:
    app.kubernetes.io/name: hello-python
    app.kubernetes.io/version: f0f274564061321f5f7498b79d3bfb62062074916a39e461bfdac153bc691ebb
spec:
  environment:
    name: python
    namespace: fission-function
  deployment:
    type: literal
    literal: ZGVmIG1haW4oKToKICAgIHJldHVybiAiSGVsbG8gZnJvbSBGaXNzaW9uISIK
---
apiVersion: fission.io/v1
kind: Function
metadata:
  name: hello-python
  namespace: fission-function
  annotations:
    app.kubernetes.io/name: hello-python
    app.kubernetes.io/version: f0f274564061321f5f7498b79d3bfb62062074916a39e461bfdac153bc691ebb
spec:
  environment:
    name: python
    namespace: fission-function
  package:
    packageref:
      name: hello-python-pkg
      namespace: fission-function
  InvokeStrategy:
    StrategyType: execution
    ExecutionStrategy:
      ExecutorType: poolmgr
      MinScale: 0
      MaxScale: 1
---
apiVersion: fission.io/v1
kind: HTTPTrigger
metadata:
  name: hello-python
  namespace: fission-function
spec:
  functionref:
    name: hello-python
    type: name
  host: fission.192.168.0.10.sslip.io
  methods:
    - GET
  relativeurl: /hello-python
````

## File: app/fission-fn/README.md
````markdown
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
````

## File: app/k3s-system/argocd/certificate.yaml
````yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: argocd-server-tls
  namespace: argocd
spec:
  commonName: argocd.192.168.0.10.sslip.io
  dnsNames:
    - argocd.192.168.0.10.sslip.io
  issuerRef:
    kind: ClusterIssuer
    name: selfsigned-cluster-issuer
  secretName: argocd-server-tls
````

## File: app/k3s-system/argocd/ingress.yaml
````yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server
  namespace: argocd
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  ingressClassName: traefik
  rules:
    - host: argocd.192.168.0.10.sslip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argocd-server
                port:
                  number: 80
  tls:
    - hosts:
        - argocd.192.168.0.10.sslip.io
      secretName: argocd-server-tls
````

## File: app/k3s-system/argocd/install.yaml
````yaml
apiVersion: v1
kind: Namespace
metadata:
  name: argocd
---
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: argocd
  namespace: kube-system
spec:
  bootstrap: true
  chart: argo-cd
  createNamespace: true
  repo: https://argoproj.github.io/argo-helm
  targetNamespace: argocd
  version: 9.4.10
  valuesContent: |-
    crds:
      install: true
    configs:
      params:
        server.insecure: "true"
    dex:
      enabled: false
    notifications:
      enabled: false
    server:
      service:
        type: ClusterIP
````

## File: app/k3s-system/argocd/selfsigned-issuer.yaml
````yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-cluster-issuer
spec:
  selfSigned: {}
````

## File: app/k3s-system/eraser/argocd-eraser.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: eraser
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://eraser-dev.github.io/eraser/charts
    chart: eraser
    targetRevision: 1.4.1
    helm:
      values: |
        eraser:
          # Schedule for automatic cleanup (every Sunday at 2 AM)
          schedule: "0 2 * * 0"
          # Components configuration
          components:
            collector:
              enabled: true
            scanner:
              enabled: true
              # Use Trivy for vulnerability scanning
              config:
                # Remove images with critical/high vulnerabilities
                deleteFailedImages: false
                deleteUntaggedImages: true
            remover:
              enabled: true
          # Node selector to run on all nodes
          nodeFilter:
            type: all
          # Images to always keep (never delete)
          # Add your critical images here
          excludedImages:
            - docker.io/library/alpine
            - registry.k8s.io/pause
          # Resource limits
          manager:
            resources:
              requests:
                cpu: 10m
                memory: 64Mi
              limits:
                cpu: 100m
                memory: 128Mi
  destination:
    server: https://kubernetes.default.svc
    namespace: eraser-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
````

## File: app/k3s-system/fission/argocd-fission-crds.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fission-crds
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://github.com/fission/fission.git
    path: crds/v1
    targetRevision: v1.22.0
  destination:
    server: https://kubernetes.default.svc
    namespace: fission
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - PrunePropagationPolicy=foreground
      - ServerSideApply=true
````

## File: app/k3s-system/fission/argocd-fission.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fission
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://fission.github.io/fission-charts
    chart: fission-all
    targetRevision: 1.22.1
    helm:
      values: |
        serviceType: ClusterIP
        routerServiceType: ClusterIP
        createNamespace: false
        analytics: false
        defaultNamespace: fission-function
        mqt_keda:
          enabled: false
        router:
          replicas: 1
  destination:
    server: https://kubernetes.default.svc
    namespace: fission
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - ServerSideApply=true
````

## File: app/k3s-system/fission/certificate.yaml
````yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: fission-router-tls
  namespace: fission
spec:
  commonName: fission.192.168.0.10.sslip.io
  dnsNames:
    - fission.192.168.0.10.sslip.io
  issuerRef:
    kind: ClusterIssuer
    name: selfsigned-cluster-issuer
  secretName: fission-router-tls
````

## File: app/k3s-system/fission/ingress-http-redirect.yaml
````yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: fission-https-redirect
  namespace: fission
spec:
  redirectScheme:
    permanent: true
    scheme: https
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fission-router-http
  namespace: fission
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
    traefik.ingress.kubernetes.io/router.middlewares: fission-fission-https-redirect@kubernetescrd
spec:
  ingressClassName: traefik
  rules:
    - host: fission.192.168.0.10.sslip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: router
                port:
                  number: 80
````

## File: app/k3s-system/fission/ingress.yaml
````yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fission-router
  namespace: fission
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  ingressClassName: traefik
  rules:
    - host: fission.192.168.0.10.sslip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: router
                port:
                  number: 80
  tls:
    - hosts:
        - fission.192.168.0.10.sslip.io
      secretName: fission-router-tls
````

## File: app/k3s-system/fission/kustomization.yaml
````yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespaces.yaml
  - argocd-fission-crds.yaml
  - argocd-fission.yaml
  - certificate.yaml
  - ingress-http-redirect.yaml
  - ingress.yaml
````

## File: app/k3s-system/fission/namespaces.yaml
````yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fission
---
apiVersion: v1
kind: Namespace
metadata:
  name: fission-function
````

## File: app/k3s-system/openfaas/certificate.yaml
````yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: openfaas-gateway-tls
  namespace: openfaas
spec:
  commonName: openfaas.192.168.0.10.sslip.io
  dnsNames:
    - openfaas.192.168.0.10.sslip.io
  issuerRef:
    kind: ClusterIssuer
    name: selfsigned-cluster-issuer
  secretName: openfaas-gateway-tls
````

## File: app/k3s-system/openfaas/kustomization.yaml
````yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespaces.yaml
  - argocd-openfaas.yaml
  - certificate.yaml
  - ingress.yaml
````

## File: app/k3s-system/openfaas/namespaces.yaml
````yaml
apiVersion: v1
kind: Namespace
metadata:
  name: openfaas
---
apiVersion: v1
kind: Namespace
metadata:
  name: openfaas-fn
````

## File: app/k3s-system/reloader/argocd-reloader.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: reloader
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://stakater.github.io/stakater-charts
    chart: reloader
    targetRevision: 1.2.0
    helm:
      values: |
        reloader:
          watchGlobally: true
          # Reload strategy: "env-vars" (default) or "annotations"
          # Use "annotations" for better GitOps compatibility with ArgoCD
          reloadStrategy: annotations
          deployment:
            resources:
              requests:
                cpu: 10m
                memory: 64Mi
              limits:
                cpu: 100m
                memory: 128Mi
          # Optional: Enable logging in JSON format
          logFormat: json
  destination:
    server: https://kubernetes.default.svc
    namespace: reloader
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
````

## File: app/k3s-system/sealed-secrets/argocd-sealed-secrets.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sealed-secrets
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://bitnami-labs.github.io/sealed-secrets
    chart: sealed-secrets
    targetRevision: 2.18.3
    helm:
      values: |
        fullnameOverride: sealed-secrets-controller
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            memory: 256Mi
  destination:
    server: https://kubernetes.default.svc
    namespace: kube-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - ServerSideApply=true
````

## File: app/openfaas-fn/hello-python/__init__.py
````python

````

## File: app/openfaas-fn/hello-python/handler_test.py
````python
from .handler import handle

# Test your handler here

# To disable testing, you can set the build_arg `TEST_ENABLED=false` on the CLI or in your stack.yml
# https://docs.openfaas.com/reference/yaml/#function-build-args-build-args

def test_handle():
    # assert handle("input") == "input"
    pass
````

## File: app/openfaas-fn/hello-python/handler.py
````python
import json
from datetime import datetime

def handle(req):
    """Simple Python function for OpenFaaS"""

    name = req.strip() if req else "World"

    response = {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "platform": "OpenFaaS on k3s"
    }

    return json.dumps(response, indent=2)
````

## File: app/openfaas-fn/hello-python/requirements.txt
````

````

## File: app/openfaas-fn/hello-python/tox.ini
````ini
# If you would like to disable
# automated testing during faas-cli build,

# Replace the content of this file with
#   [tox]
#   skipsdist = true

# You can also edit, remove, or add additional test steps
# by editing, removing, or adding new testenv sections


# find out more about tox: https://tox.readthedocs.io/en/latest/
[tox]
envlist = lint,test
skipsdist = true

[testenv:test]
deps =
  flask
  pytest
  -rrequirements.txt
commands =
  # run unit tests with pytest
  # https://docs.pytest.org/en/stable/
  # configure by adding a pytest.ini to your handler
  pytest

[testenv:lint]
deps =
  flake8
commands =
  flake8 .

[flake8]
count = true
max-line-length = 127
max-complexity = 10
statistics = true
# stop the build if there are Python syntax errors or undefined names
select = E9,F63,F7,F82
show-source = true
````

## File: app/openfaas-fn/stack.yaml
````yaml
version: 1.0
provider:
  name: openfaas
  gateway: https://openfaas.192.168.0.10.sslip.io
functions:
  hello-python:
    lang: python3-flask
    handler: ./hello-python
    image: radam/hello-python:latest
````

## File: scripts/create-grafana-otel-sealed-secret.sh
````bash
#!/bin/bash

# ==============================================================================
# Create Grafana Cloud Sealed Secret for OTEL Collector
# ==============================================================================
#
# This script creates a sealed secret for Grafana Cloud credentials used by
# the OpenTelemetry Collector to export telemetry data.
#
# Prerequisites:
# - kubectl installed and configured
# - kubeseal installed (https://github.com/bitnami-labs/sealed-secrets)
# - sealed-secrets controller running in k3s cluster
# - Grafana Cloud account with OTLP access
#
# Usage:
#   ./create-grafana-otel-sealed-secret.sh
#
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${NAMESPACE:-default}"
SECRET_NAME="otel-collector-secret"
SEALED_SECRET_FILE="app/demo/dentari/otel-collector-sealed-secret.yaml"

echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}Grafana Cloud OTEL Collector - Sealed Secret Creator${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl not found. Please install kubectl.${NC}"
    exit 1
fi

if ! command -v kubeseal &> /dev/null; then
    echo -e "${RED}Error: kubeseal not found. Please install kubeseal.${NC}"
    echo "Install: https://github.com/bitnami-labs/sealed-secrets#kubeseal"
    exit 1
fi

# Check if sealed-secrets controller is running
if ! kubectl get deployment sealed-secrets-controller -n kube-system &> /dev/null; then
    echo -e "${RED}Error: sealed-secrets controller not found in cluster.${NC}"
    echo "Install it first: kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Get Grafana Cloud information
echo -e "${YELLOW}==================================================================${NC}"
echo -e "${YELLOW}Grafana Cloud Configuration${NC}"
echo -e "${YELLOW}==================================================================${NC}"
echo ""
echo "To get your Grafana Cloud OTLP credentials:"
echo "1. Go to: https://grafana.com/orgs/YOUR_ORG/stacks"
echo "2. Click on your stack"
echo "3. Go to: Connections → Add new connection → OpenTelemetry"
echo "4. Copy the Instance ID and generate a new API token"
echo ""

# Get endpoint
echo -e "${YELLOW}Enter Grafana Cloud OTLP endpoint:${NC}"
echo "Format: https://otlp-gateway-prod-{region}.grafana.net/otlp"
echo "Example: https://otlp-gateway-prod-eu-west-0.grafana.net/otlp"
read -r GRAFANA_ENDPOINT

if [[ -z "$GRAFANA_ENDPOINT" ]]; then
    echo -e "${RED}Error: Endpoint cannot be empty${NC}"
    exit 1
fi

# Get instance ID
echo ""
echo -e "${YELLOW}Enter Grafana Cloud Instance ID:${NC}"
read -r GRAFANA_INSTANCE_ID

if [[ -z "$GRAFANA_INSTANCE_ID" ]]; then
    echo -e "${RED}Error: Instance ID cannot be empty${NC}"
    exit 1
fi

# Get token
echo ""
echo -e "${YELLOW}Enter Grafana Cloud API Token:${NC}"
read -rs GRAFANA_TOKEN

if [[ -z "$GRAFANA_TOKEN" ]]; then
    echo -e "${RED}Error: Token cannot be empty${NC}"
    exit 1
fi

echo ""

# Create authorization header
echo -e "${YELLOW}Creating authorization header...${NC}"
GRAFANA_CREDENTIALS="${GRAFANA_INSTANCE_ID}:${GRAFANA_TOKEN}"
GRAFANA_AUTH_HEADER="Basic $(echo -n "$GRAFANA_CREDENTIALS" | base64 -w 0)"

echo -e "${GREEN}✓ Authorization header created${NC}"
echo ""

# Create temporary secret
echo -e "${YELLOW}Creating Kubernetes secret...${NC}"
kubectl create secret generic "$SECRET_NAME" \
  --from-literal=grafana-endpoint="$GRAFANA_ENDPOINT" \
  --from-literal=grafana-headers="$GRAFANA_AUTH_HEADER" \
  --namespace="$NAMESPACE" \
  --dry-run=client \
  -o yaml > /tmp/otel-collector-secret.yaml

echo -e "${GREEN}✓ Kubernetes secret created${NC}"
echo ""

# Seal the secret
echo -e "${YELLOW}Sealing secret with kubeseal...${NC}"
kubeseal --format=yaml \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  < /tmp/otel-collector-secret.yaml \
  > "$SEALED_SECRET_FILE"

echo -e "${GREEN}✓ Sealed secret created${NC}"
echo ""

# Cleanup
rm /tmp/otel-collector-secret.yaml

# Summary
echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}Success!${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo ""
echo "Sealed secret created: $SEALED_SECRET_FILE"
echo ""
echo "Next steps:"
echo "1. Review the sealed secret file"
echo "2. Commit to Git (it's safe - encrypted for your cluster only)"
echo "3. Apply to cluster:"
echo "   kubectl apply -f $SEALED_SECRET_FILE"
echo ""
echo "Or let ArgoCD sync it automatically."
echo ""
echo -e "${YELLOW}Note: The sealed secret can only be decrypted by your k3s cluster.${NC}"
echo -e "${YELLOW}If you rebuild the cluster, you'll need to regenerate it.${NC}"
echo ""
````

## File: scripts/README.md
````markdown
# ArgoCD Scripts

## GHCR Sealed Secret Setup

### Prerequisites

1. Install direnv: `sudo apt install direnv` (or `brew install direnv` on macOS)
2. Add to your shell config (~/.zshrc or ~/.bashrc):
   ```bash
   eval "$(direnv hook zsh)"  # or 'bash' for bash
   ```
3. Reload shell or run: `source ~/.zshrc`

### Setup

1. **Create `.envrc` in the argocd directory:**
   ```bash
   cd /home/ferko/Documents/argocd
   cat > .envrc << 'EOF'
   # GitHub Container Registry credentials
   export GITHUB_USERNAME="radamhu"
   export GITHUB_TOKEN="your-github-token-here"
   EOF
   ```

2. **Create a GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens/new
   - Name: "GHCR Access - Dentari"
   - Scopes: `read:packages`, `write:packages`
   - Expiration: 90 days (recommended)
   - Copy the token

3. **Edit `.envrc` and add your token:**
   ```bash
   vim .envrc
   # Replace "your-github-token-here" with your actual token
   ```

4. **Allow direnv to load the environment:**
   ```bash
   direnv allow
   ```

### Usage

Run the script to create a sealed secret:
```bash
cd /home/ferko/Documents/argocd
./scripts/create-ghcr-sealed-secret.sh
```

The script will:
- Use credentials from `.envrc` if available
- Or prompt for them interactively
- Create a sealed secret at `app/demo/dentari/ghcr-sealed-secret.yaml`
- This file can be safely committed to Git

### Security Notes

- `.envrc` is already in `.gitignore` and will never be committed
- The sealed secret can only be decrypted by your cluster's sealed-secrets controller
- Tokens should be rotated every 90 days
- Never commit plain secrets or tokens to Git

### Updating the Secret

When your token expires:
1. Create a new token on GitHub
2. Update `.envrc` with the new token
3. Run `direnv allow` to reload
4. Run the script again to generate a new sealed secret
5. Commit and push the new sealed secret
````

## File: .gitignore
````
# Environments
.psenvrc
.envrc
.env
.venv

# Secrets and credentials - DO NOT COMMIT
*secret.yaml
!*sealed-secret.yaml
!*-secret.yaml.template
!*-secret-template.yaml
*.env
*.env.local
.env
.env.*
credentials.json
*-credentials.json
**/secrets/
**/*-key.pem
**/*.key
**/*.pem
**/*.p12
**/*.pfx
sealed-secrets-key*.yaml
*.secret
*.token
*.pwd
*.password
**/sa-token.yaml

# IDE ignored files
.idea/
*.iml
.vscode/

# Local .terraform files
.terraform/
.terraform.lock.hcl
crash.log
crash.*.log
variables.tfvars
*.tfvars.json
.terraform.tfstate.lock.info
terraform-plugin-proxmox.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# SA Frontend npm ignored files
node_modules/
**/sa-frontend/build/

# SA WebApp java ignored files
target/
.mvn/
!**/maven-wrapper.jar

# SA Logic python ignored files
venv/
env/
venv/
ENV/
.env
env.bak/
venv.bak/
output.txt

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/
````

## File: app/k3s-system/openfaas/ingress.yaml
````yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: openfaas
  namespace: openfaas
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  ingressClassName: traefik
  rules:
    - host: openfaas.192.168.0.10.sslip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: gateway
                port:
                  number: 8080
  tls:
    - hosts:
        - openfaas.192.168.0.10.sslip.io
      secretName: openfaas-gateway-tls
````

## File: app/k3s-system/openfaas/argocd-openfaas.yaml
````yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: openfaas
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io/foreground
spec:
  project: default
  source:
    repoURL: https://openfaas.github.io/faas-netes
    chart: openfaas
    targetRevision: 14.2.131
    helm:
      values: |
        functionNamespace: openfaas-fn
        generateBasicAuth: true
        serviceType: ClusterIP
        clusterRole: true
        createCRDs: true
        operator:
          create: false
        gateway:
          replicas: 1
        queueWorker:
          replicas: 1
        prometheus:
          create: true
        alertmanager:
          create: false
        ingress:
          enabled: false
  destination:
    server: https://kubernetes.default.svc
    namespace: openfaas
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - ServerSideApply=true
````

## File: scripts/create-ghcr-sealed-secret.sh
````bash
#!/bin/bash
set -e

# Script to create a sealed GHCR secret for the Dentari application
# This script creates a sealed secret that can be safely committed to Git

echo "=== GHCR Sealed Secret Creator ==="
echo ""
echo "This script will create a sealed secret for GitHub Container Registry access."
echo ""
echo "You can set credentials in .envrc (recommended) or enter them interactively."
echo ""
echo "To set up .envrc:"
echo "1. Create .envrc in the argocd directory with:"
echo "   export GITHUB_USERNAME=\"radamhu\""
echo "   export GITHUB_TOKEN=\"your-token-here\""
echo "2. Allow direnv: direnv allow"
echo ""
echo "To create a token:"
echo "1. Go to: https://github.com/settings/tokens/new"
echo "2. Set name: 'GHCR Access - Dentari'"
echo "3. Select scopes: read:packages, write:packages"
echo "4. Set expiration: 90 days"
echo "5. Generate and copy the token"
echo ""

# Get inputs from environment variables (set in .envrc) or prompt
if [ -z "$GITHUB_USERNAME" ]; then
    read -p "GitHub Username [radamhu]: " GITHUB_USERNAME
    GITHUB_USERNAME=${GITHUB_USERNAME:-radamhu}
fi

if [ -z "$GITHUB_TOKEN" ]; then
    read -p "GitHub Token: " -s GITHUB_TOKEN
    echo ""
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GitHub token is required"
    exit 1
fi

# Verify kubectl connection
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot connect to Kubernetes cluster"
    echo "Please ensure kubectl is configured correctly"
    exit 1
fi

# Verify sealed-secrets controller is running
if ! kubectl get deployment sealed-secrets-controller -n kube-system &> /dev/null; then
    echo "❌ Error: sealed-secrets-controller not found in kube-system namespace"
    echo "Please ensure Sealed Secrets is deployed"
    exit 1
fi

echo ""
echo "✓ Connected to Kubernetes cluster"
echo "✓ Sealed Secrets controller found"
echo ""

# Create the sealed secret
echo "Creating sealed secret..."

OUTPUT_FILE="app/demo/dentari/environments/dev/dev-ghcr-sealed-secret.yaml"

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username="$GITHUB_USERNAME" \
  --docker-password="$GITHUB_TOKEN" \
  --namespace=dev-dentari \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system \
  --format=yaml > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Sealed secret created: $OUTPUT_FILE"
    echo ""
    echo "The sealed secret has been created and can be safely committed to Git."
    echo ""
    echo "Next steps:"
    echo "1. Review the sealed secret: cat $OUTPUT_FILE"
    echo "2. Commit to Git: git add $OUTPUT_FILE && git commit -m 'Add GHCR sealed secret' && git push"
    echo "3. ArgoCD will automatically sync and deploy the secret"
    echo "4. Delete the plain secret template: git rm app/demo/dentari/ghcr-secret.yaml"
    echo ""
    echo "⚠️  IMPORTANT:"
    echo "   - If you entered credentials manually, clear shell history: history -c"
    echo "   - .envrc is already in .gitignore and won't be committed"
else
    echo "❌ Error: Failed to create sealed secret"
    exit 1
fi
````

## File: README.md
````markdown
# ArgoCD Homelab - K3s GitOps Repository

This repository contains ArgoCD applications and configurations for managing a K3s cluster using GitOps principles.

## Sources & References
- https://gitlab.com/k3s-media/k3s-media-server/-/tree/main/media-server\?ref_type\=heads
- https://github.com/bjw-s/helm-charts
- https://github.com/gruberdev/homelab
- https://github.com/acelinkio/argocd-homelab
- https://github.com/crkochan/argocd-homelab
- https://community-scripts.github.io/ProxmoxVE/
- https://rpi4cluster.com/
- https://kubesearch.dev/

---

## Repository Structure

```
argocd/
├── app/
│   ├── demo/                    # Demo applications
│   │   ├── dentari/             # Dentari app deployment
│   │   ├── hello-flask/         # Flask demo app
│   │   ├── helm-guestbook/      # Helm guestbook example
│   ├── openfaas-fn/             # OpenFaaS function examples
│   └── k3s-system/              # System components
│       ├── cert-manager/
│       ├── eraser/
│       ├── external-dns/
│       ├── external-secrets-operator/
│       ├── metallb/
│       ├── openfaas/            # OpenFaaS platform
│       ├── reflector/
│       ├── reloader/
│       ├── sealed-secrets/
│       └── traefik/
└── argocd-apps/                 # ArgoCD Application manifests
    └── demo/
```

---

## Security & Secrets Management

This repository uses **Sealed Secrets** for secure GitOps secret management. Secrets are encrypted client-side and safe to commit to Git.

### Core Principles

- ✅ Never commit plaintext secrets to Git
- ✅ Use Sealed Secrets for encryption
- ✅ Rotate credentials every 90 days
- ✅ Pre-commit hooks prevent leaks

### Quick Start - Create GHCR Sealed Secret

```bash
# Automated (recommended)
./scripts/create-ghcr-sealed-secret.sh

# Manual
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=<token> \
  --namespace=default \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  --format=yaml > app/demo/dentari/ghcr-sealed-secret.yaml

# Commit and deploy
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "Add GHCR sealed secret"
git push
```

### Prerequisites

- Sealed Secrets controller (already deployed at `app/k3s-system/sealed-secrets`)
- kubeseal CLI (script auto-installs)
- kubectl connected to cluster
- GitHub token with `read:packages` and `write:packages` scopes

**Create GitHub Token:** https://github.com/settings/tokens/new

### How Sealed Secrets Work

1. **Encrypt** - `kubeseal` encrypts secrets using controller's public key
2. **Commit** - Encrypted SealedSecret resources safe to commit to Git
3. **Deploy** - ArgoCD syncs SealedSecret to cluster
4. **Decrypt** - Controller decrypts and creates standard Kubernetes Secret
5. **Use** - Applications reference the Secret normally

### Verification Commands

```bash
# Check sealed secret
kubectl get sealedsecret ghcr-secret -n default

# Check actual secret (created by controller)
kubectl get secret ghcr-secret -n default

# Check deployment
kubectl get pods -n default | grep dentari

# View controller logs
kubectl logs -n kube-system -l name=sealed-secrets-controller
```

### Token Rotation (Every 90 Days)

```bash
# 1. Create new GitHub token
# 2. Run script
./scripts/create-ghcr-sealed-secret.sh

# 3. Commit and push
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "chore: rotate GHCR token"
git push

# 4. Revoke old token at https://github.com/settings/tokens
```

### Troubleshooting

**Sealed Secret Won't Decrypt:**
```bash
kubectl logs -n kube-system -l name=sealed-secrets-controller
kubectl get events -n default --sort-by='.lastTimestamp'
```

**Image Pull Errors:**
```bash
kubectl describe pod <dentari-pod-name> -n default
kubectl get secret ghcr-secret -n default -o yaml
```

**Re-seal Secret:**
```bash
kubectl delete sealedsecret ghcr-secret -n default
./scripts/create-ghcr-sealed-secret.sh
git add app/demo/dentari/ghcr-sealed-secret.yaml
git commit -m "fix: re-seal GHCR secret"
git push
```

### Security Features

**Prevention:**
- `.gitignore` excludes secret files
- Pre-commit hooks detect private keys
- Template files with no credentials

**Detection:**
- GitGuardian monitoring active
- Pre-commit validation on every commit

**Response:**
- Incident procedures: [SECURITY_INCIDENT_RESPONSE.md](SECURITY_INCIDENT_RESPONSE.md)
- Rotation scripts available
- Git history cleanup tools

### Alternative Solutions

**External Secrets Operator** - For AWS/GCP/Azure secret managers
**ArgoCD Vault Plugin** - For HashiCorp Vault
**SOPS** - For encrypted files in Git

See `app/k3s-system/external-secrets-operator/` for setup

---

## ArgoCD Deployment

### Initial Setup

```bash
# Deploy ArgoCD to k3s cluster
sh ./argocd.sh

# Get ArgoCD admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Login to ArgoCD CLI
ARGOCD_PASS=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
argocd login <ARGOCD_IP> --username admin --password "$ARGOCD_PASS" --insecure
```

### Kustomize Deployment

```bash
kubectl kustomize ./app/tools/ --enable-helm | kubectl apply -f -
```

### Apply ArgoCD Applications

```bash
# Apply system applications
kubectl apply -f app/k3s-system/openfaas/argocd-openfaas.yaml
kubectl apply -f app/k3s-system/metallb/argocd-metallb.yaml
# ... etc

# Sync applications
argocd app sync <app-name>
```

---

## OpenFaaS Deployment

OpenFaaS is deployed via ArgoCD Helm chart with the following configuration:

### Access Details

| Item | Value |
|------|-------|
| **UI URL** | `https://openfaas.192.168.0.10.sslip.io/ui/` |
| **API URL** | `https://openfaas.192.168.0.10.sslip.io/` |
| **Username** | `admin` |
| **Password** | See command below |
| **TLS** | Self-signed cert via cert-manager |

```bash
# Get OpenFaaS password
kubectl get secret -n openfaas basic-auth -o jsonpath='{.data.basic-auth-password}' | base64 -d && echo
```

### Configuration

The OpenFaaS ArgoCD application is defined in `app/k3s-system/openfaas/argocd-openfaas.yaml`:

- **Chart**: `openfaas` from `https://openfaas.github.io/faas-netes`
- **Version**: `14.2.131`
- **Namespace**: `openfaas`
- **Functions Namespace**: `openfaas-fn`
- **Service Type**: ClusterIP (exposed via Traefik Ingress)

### Traefik Ingress

OpenFaaS is exposed via host-based routing on `openfaas.192.168.0.10.sslip.io` with TLS:

```yaml
# app/k3s-system/openfaas/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: openfaas
  namespace: openfaas
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  ingressClassName: traefik
  rules:
    - host: openfaas.192.168.0.10.sslip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: gateway
                port:
                  number: 8080
  tls:
    - hosts:
        - openfaas.192.168.0.10.sslip.io
      secretName: openfaas-gateway-tls
```

---

## OpenFaaS Functions Development

### Prerequisites

```bash
# Install faas-cli
curl -sSL https://cli.openfaas.com | sudo sh

# Login to OpenFaaS
echo "<password>" | faas-cli login --gateway https://openfaas.192.168.0.10.sslip.io --username admin --password-stdin
```

### Create a New Python Function

```bash
# Pull templates
faas-cli template store pull python3-flask

# Create new function
faas-cli new hello-python --lang python3-flask

# Edit the handler
cat > hello-python/handler.py << 'EOF'
import json
from datetime import datetime

def handle(req):
    """Simple Python function for OpenFaaS"""
    name = req.strip() if req else "World"
    response = {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "platform": "OpenFaaS on k3s"
    }
    return json.dumps(response, indent=2)
EOF
```

### Build, Push & Deploy

```bash
# Update stack.yaml with your registry
cat > stack.yaml << 'EOF'
version: 1.0
provider:
  name: openfaas
  gateway: https://openfaas.192.168.0.10.sslip.io
functions:
  hello-python:
    lang: python3-flask
    handler: ./hello-python
    image: <dockerhub-user>/hello-python:latest
EOF

# Build the function
faas-cli build -f stack.yaml

# Push to registry
faas-cli push -f stack.yaml

# Deploy to OpenFaaS
faas-cli deploy -f stack.yaml
```

### Invoke Function

```bash
# With data
curl -k -u admin:<password> https://openfaas.192.168.0.10.sslip.io/function/hello-python -d "Your Name"

# Without data
curl -k -u admin:<password> https://openfaas.192.168.0.10.sslip.io/function/hello-python

# Self-signed TLS note
# add --tls-no-verify if your faas-cli does not trust the local cert
echo "Your Name" | faas-cli invoke hello-python --gateway https://openfaas.192.168.0.10.sslip.io
```

### Example Function (app/openfaas-fn/)

The repository includes a sample Python function in `app/openfaas-fn/`:

```
openfaas-fn/
├── hello-python/
│   ├── handler.py          # Function logic
│   └── requirements.txt    # Python dependencies
└── stack.yaml              # OpenFaaS stack definition
```

---

## Useful Commands

### ArgoCD

```bash
# List all applications
argocd app list

# Sync an application
argocd app sync <app-name>

# Get application details
argocd app get <app-name>

# Hard refresh (re-read from Git)
argocd app get <app-name> --hard-refresh
```

### OpenFaaS

```bash
# List deployed functions
faas-cli list --gateway https://openfaas.192.168.0.10.sslip.io

# Get function info
faas-cli describe hello-python --gateway https://openfaas.192.168.0.10.sslip.io

# View function logs
faas-cli logs hello-python --gateway https://openfaas.192.168.0.10.sslip.io

# Remove a function
faas-cli remove hello-python --gateway https://openfaas.192.168.0.10.sslip.io
```

### Kubernetes

```bash
# Check OpenFaaS pods
kubectl get pods -n openfaas
kubectl get pods -n openfaas-fn

# Check services
kubectl get svc -n openfaas

# View function logs
kubectl logs -n openfaas-fn -l faas_function=hello-python
```

---

## GitOps Workflow

1. **Modify** application manifests in this repository
2. **Commit & Push** changes to GitHub
3. **ArgoCD detects** changes automatically (or manual sync)
4. **Kubernetes** resources are updated

For OpenFaaS functions with GitOps:
- Store function source in `app/openfaas-fn/`
- Use CI/CD to build and push images on commit
- ArgoCD syncs the function CRDs (if using operator mode)

### References
- https://www.openfaas.com/blog/bring-gitops-to-your-openfaas-functions-with-argocd/
- https://rpi4cluster.com/k3s-openfaas/
````
