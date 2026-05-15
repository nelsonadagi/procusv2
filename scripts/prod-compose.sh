#!/usr/bin/env bash
set -euo pipefail

SECRETS_FILE=".deploy/prod-vars.sh"

if [[ ! -f "$SECRETS_FILE" ]]; then
  echo "Missing $SECRETS_FILE. Creating production variables for paanguzo.iqsaccodigital.com..." >&2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/prod-env.sh"

load_prod_env "$DEFAULT_PUBLIC_DOMAIN"
write_prod_env

COMPOSE_DISABLE_ENV_FILE=1 docker compose -f docker-compose.yml -f docker-compose.prod.yml "$@"
