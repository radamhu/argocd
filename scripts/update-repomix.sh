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
