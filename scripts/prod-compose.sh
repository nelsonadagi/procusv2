#!/usr/bin/env bash
set -euo pipefail

SECRETS_FILE=".deploy/prod-vars.sh"

if [[ ! -f "$SECRETS_FILE" ]]; then
  echo "Missing $SECRETS_FILE." >&2
  echo "Run: scripts/deploy-prod.sh paanguzo.iqsaccodigital.com --config" >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$SECRETS_FILE"

COMPOSE_DISABLE_ENV_FILE=1 docker compose -f docker-compose.yml -f docker-compose.prod.yml "$@"
