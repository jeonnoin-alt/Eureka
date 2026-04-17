#!/bin/bash
# freshness-hash.sh — compute canonical freshness hashes for Eureka artifacts
#
# Purpose: Produce deterministic SHA-256 hashes of the manuscript and the
# results directory for the `manuscript_hash` and `results_hash` fields in
# Eureka artifact YAML frontmatter. Without deterministic hashes, the
# freshness protocol defined in `skills/using-eureka/SKILL.md` is purely
# documentary; with them, `verification-before-publication` and
# `submission-readiness` can detect drift between upstream artifacts
# (claims-audit, research-reviewer, novelty-competitive-audit) and the
# current manuscript/results state.
#
# Usage:
#   hooks/freshness-hash.sh manuscript <path-to-manuscript>
#       → emits sha256 of the manuscript file
#
#   hooks/freshness-hash.sh results <path-to-results-directory>
#       → recursively hashes all files in the directory, sorts by path,
#         and emits sha256 of the concatenated per-file hashes (directory
#         content digest — deterministic regardless of filesystem order)
#
#   hooks/freshness-hash.sh both <manuscript> <results-dir>
#       → emits two lines ready for YAML frontmatter:
#           manuscript_hash: sha256:<hex>
#           results_hash: sha256:<hex>
#
# Exit codes:
#   0 — success, hash(es) on stdout
#   1 — missing argument or unreadable path
#   2 — sha256sum not available
#
# Dependencies: sha256sum (standard on Linux/macOS-via-coreutils),
# find, sort. No non-standard tools.
#
# Design notes:
#   - Results hash hashes FILE CONTENTS, not filesystem metadata (mtime,
#     permissions). Reordering/renaming the directory tree doesn't drift
#     the hash unless file contents change.
#   - The hash is a content digest: `sha256(concat(sorted(file_hashes)))`.
#     Adding a file changes the hash; renaming a file changes the hash
#     (because the path string is part of each per-file entry); changing
#     whitespace in a result file changes the hash.
#   - LaTeX auxiliary files (.aux, .log, .out, .toc, .synctex.gz) are
#     excluded from the hash because they drift with every recompile
#     without representing result changes. Similarly, common build
#     artifact extensions are excluded.
#   - This is a soft-warning protocol. Hash mismatch ≠ actual divergence
#     (trivial whitespace edits trigger it); hash match = strong
#     guarantee of unchanged content. Soft-warn semantics intentional.

set -euo pipefail

# -------- helpers -----------------------------------------------------------

err() {
    echo "freshness-hash.sh: $*" >&2
}

require_sha256sum() {
    if ! command -v sha256sum >/dev/null 2>&1; then
        err "sha256sum not available. Install coreutils (Linux) or gnu-coreutils (macOS via homebrew)."
        exit 2
    fi
}

hash_manuscript() {
    local path="$1"
    if [[ ! -f "$path" ]]; then
        err "manuscript not found: $path"
        exit 1
    fi
    sha256sum "$path" | awk '{print $1}'
}

hash_results_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        err "results directory not found: $dir"
        exit 1
    fi

    # Excluded extensions: LaTeX build artifacts, OS metadata, editor swap files
    local exclude_pattern='(\.aux|\.log|\.out|\.toc|\.synctex\.gz|\.fdb_latexmk|\.fls|\.bbl|\.blg|\.DS_Store|~$|\.swp)$'

    # Find all files, exclude build artifacts, compute per-file hashes,
    # sort by path for determinism, then hash the concatenation.
    # Each line of the intermediate: <file-sha256>  <relative-path>
    # Deterministic across filesystems because we sort by relative path.

    ( cd "$dir" && find . -type f | grep -vE "$exclude_pattern" | LC_ALL=C sort | \
        while IFS= read -r file; do
            sha256sum "$file"
        done
    ) | sha256sum | awk '{print $1}'
}

# -------- dispatch ----------------------------------------------------------

require_sha256sum

case "${1:-}" in
    manuscript)
        if [[ $# -ne 2 ]]; then
            err "usage: $0 manuscript <path-to-manuscript>"
            exit 1
        fi
        hash_manuscript "$2"
        ;;
    results)
        if [[ $# -ne 2 ]]; then
            err "usage: $0 results <path-to-results-directory>"
            exit 1
        fi
        hash_results_dir "$2"
        ;;
    both)
        if [[ $# -ne 3 ]]; then
            err "usage: $0 both <manuscript> <results-dir>"
            exit 1
        fi
        echo "manuscript_hash: sha256:$(hash_manuscript "$2")"
        echo "results_hash: sha256:$(hash_results_dir "$3")"
        ;;
    -h|--help|help|"")
        cat <<'HELP'
freshness-hash.sh — compute Eureka artifact freshness hashes

Usage:
  freshness-hash.sh manuscript <path>
      Output: hex sha256 of the manuscript file

  freshness-hash.sh results <dir>
      Output: hex sha256 digest of all files under dir (excluding build artifacts)

  freshness-hash.sh both <manuscript> <results-dir>
      Output: two YAML lines ready for Eureka artifact frontmatter:
          manuscript_hash: sha256:<hex>
          results_hash: sha256:<hex>

Examples:
  $ freshness-hash.sh manuscript paper/main.tex
  $ freshness-hash.sh results results/
  $ freshness-hash.sh both paper/main.tex results/ >> docs/eureka/audits/2026-04-17-claims-audit.md.frontmatter

See skills/using-eureka/SKILL.md (Canonical output paths + freshness protocol)
and docs/references/registration-lifecycle.md for usage context.
HELP
        ;;
    *)
        err "unknown command: $1 (try 'help')"
        exit 1
        ;;
esac
