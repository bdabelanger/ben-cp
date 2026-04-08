#!/usr/bin/env bash
# Platform Weekly Status — cron/manual wrapper
# Usage:  ./run_pipeline.sh [--force] [--open]
#
# Loads credentials from .env (sibling of this file), then runs the pipeline.
# Logs are appended to logs/run.log.
#
# Crontab example (every Monday at 8am):
#   0 8 * * 1 /path/to/ben-cp/project-status-reports/run_pipeline.sh --force >> /dev/null 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env"
LOG_FILE="$SCRIPT_DIR/logs/run.log"

mkdir -p "$SCRIPT_DIR/logs"

# Load .env if present
if [[ -f "$ENV_FILE" ]]; then
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
fi

# Validate credentials
if [[ -z "${ATLASSIAN_USER_EMAIL:-}" || -z "${ATLASSIAN_API_TOKEN:-}" ]]; then
    echo "❌ ATLASSIAN_USER_EMAIL or ATLASSIAN_API_TOKEN not set. Add them to $ENV_FILE." >&2
    exit 1
fi
if [[ -z "${ASANA_API_TOKEN:-}" ]]; then
    echo "❌ ASANA_API_TOKEN not set. Add it to $ENV_FILE." >&2
    exit 1
fi

echo "========================================"  >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] run_pipeline.sh starting" >> "$LOG_FILE"

python3 "$SCRIPT_DIR/scripts/full_run.py" "$@" 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] run_pipeline.sh done" >> "$LOG_FILE"
