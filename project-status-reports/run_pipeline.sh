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
ENV_FILE="$SCRIPT_DIR/.env"
LOG_FILE="$SCRIPT_DIR/logs/run.log"

mkdir -p "$SCRIPT_DIR/logs"

# Load .env if present
if [[ -f "$ENV_FILE" ]]; then
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
fi

# Validate credentials
if [[ -z "${JIRA_USER_EMAIL:-}" || -z "${JIRA_API_TOKEN:-}" ]]; then
    echo "❌ JIRA_USER_EMAIL or JIRA_API_TOKEN not set. Copy .env.example to .env and fill in values." >&2
    exit 1
fi

echo "========================================"  >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] run_pipeline.sh starting" >> "$LOG_FILE"

python3 "$SCRIPT_DIR/scripts/full_run.py" "$@" 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] run_pipeline.sh done" >> "$LOG_FILE"
