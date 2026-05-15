#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/deploy-prod.sh [public-domain] [--config]

Examples:
  scripts/deploy-prod.sh --config
  scripts/deploy-prod.sh
  scripts/deploy-prod.sh marketplace.example.com --config

The script generates missing production variables for the current process:
  PUBLIC_DOMAIN
  POSTGRES_PASSWORD
  DJANGO_SECRET_KEY

It does not create or require a .env file. For local Docker deployments, it
  persists generated values in .deploy/prod-vars.sh so redeploys and follow-up
  docker compose commands reuse the same domain, database password, and Django
  secret.

Optional environment overrides:
  POSTGRES_PASSWORD      Use an existing database password instead of generating one.
  DJANGO_SECRET_KEY      Use an existing Django secret instead of generating one.
  POSTGRES_DB            Defaults to marketplace.
  POSTGRES_USER          Defaults to postgres.
  DATABASE_URL           Use an external database URL instead of the Docker Postgres URL.
  ALLOWED_HOSTS          Override the domain-derived host list.
  CORS_ALLOWED_ORIGINS   Override the domain-derived HTTPS origin.
  CSRF_TRUSTED_ORIGINS   Override the domain-derived HTTPS origin.
  VITE_API_URL           Override https://PUBLIC_DOMAIN/api.
  VITE_WS_URL            Override wss://PUBLIC_DOMAIN/ws/notifications/.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/prod-env.sh"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

PUBLIC_DOMAIN_ARG="$DEFAULT_PUBLIC_DOMAIN"
MODE="--deploy"

if [[ "${1:-}" == "--config" || "${1:-}" == "--deploy" || $# -eq 0 ]]; then
  MODE="${1:---deploy}"
elif [[ $# -ge 1 ]]; then
  PUBLIC_DOMAIN_ARG="$1"
  MODE="${2:---deploy}"
fi

if [[ "$MODE" != "--deploy" && "$MODE" != "--config" ]]; then
  echo "Unknown mode: $MODE" >&2
  usage >&2
  exit 2
fi

POSTGRES_PASSWORD_WAS_PROVIDED="${POSTGRES_PASSWORD:+1}"
DJANGO_SECRET_KEY_WAS_PROVIDED="${DJANGO_SECRET_KEY:+1}"
load_prod_env "$PUBLIC_DOMAIN_ARG"
write_prod_env

echo "Production variables prepared for $PUBLIC_DOMAIN"
echo "PUBLIC_DOMAIN=$PUBLIC_DOMAIN"
echo "POSTGRES_DB=${POSTGRES_DB:-marketplace}"
echo "POSTGRES_USER=${POSTGRES_USER:-postgres}"
echo "POSTGRES_PASSWORD=<from environment or $SECRETS_FILE>"
echo "DJANGO_SECRET_KEY=<from environment or $SECRETS_FILE>"
echo "Postgres will create the database automatically on first container boot if the postgres volume is empty."

if [[ "$MODE" == "--config" ]]; then
  echo "Validating production Compose config..."
  COMPOSE_DISABLE_ENV_FILE=1 docker compose -f docker-compose.yml -f docker-compose.prod.yml config --quiet
  echo "Production Compose config is valid."
else
  if [[ -z "$POSTGRES_PASSWORD_WAS_PROVIDED" || -z "$DJANGO_SECRET_KEY_WAS_PROVIDED" ]]; then
    echo "Generated secrets were saved to $SECRETS_FILE for repeatable redeploys."
    echo "Back up this file or move these values into your deployment platform's secret store before relying on this server long term."
  fi
  echo "Preparing Postgres role and database..."
  "$SCRIPT_DIR/prepare-postgres.sh"
  echo "Starting production stack..."
  COMPOSE_DISABLE_ENV_FILE=1 docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
  echo "Configuring host Nginx if available..."
  "$SCRIPT_DIR/install-host-nginx.sh" || echo "Host Nginx install needs attention; Docker stack is still deployed."
fi
