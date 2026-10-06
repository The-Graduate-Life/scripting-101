#!/usr/bin/env bash
# lib/logging.sh — small logging helpers shared by course scripts.
#
# Use it from another script with:
#     source "$(dirname "${BASH_SOURCE[0]}")/lib/logging.sh"
#
# Set LOG_FILE before calling the functions to also append messages to a file.
# Messages go to STDERR so they never pollute a script's real output (STDOUT).

_log() {
    local level=$1; shift
    local line
    line="$(date '+%Y-%m-%d %H:%M:%S') [$level] $*"
    echo "$line" >&2
    if [[ -n "${LOG_FILE:-}" ]]; then
        echo "$line" >> "$LOG_FILE"
    fi
}

log_info()  { _log INFO  "$@"; }
log_warn()  { _log WARN  "$@"; }
log_error() { _log ERROR "$@"; }

# die "message" [exit_code] — log an error and stop the script
die() {
    log_error "$1"
    exit "${2:-1}"
}

# require_cmd tool... — stop early if a required program is missing
require_cmd() {
    local cmd
    for cmd in "$@"; do
        command -v "$cmd" >/dev/null 2>&1 || die "required command not found: $cmd (is your conda env active?)" 127
    done
}
