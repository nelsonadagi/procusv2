#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/generate-prod-vars.sh <public-domain>

Prints shell exports for the three required production variables:
  PUBLIC_DOMAIN
  POSTGRES_PASSWORD
  DJANGO_SECRET_KEY

Example:
  eval "$(scripts/generate-prod-vars.sh marketplace.example.com)"
  make prod

For long-lived production, save these values in your deployment platform's
secret store so redeploys reuse the same database password and Django secret.
USAGE
}

random_secret() {
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -hex 32 | tr -d '\n'
  else
    LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 64
  fi
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -ne 1 ]]; then
  usage
  exit 0
fi

domain="$1"
postgres_password="${POSTGRES_PASSWORD:-$(random_secret)}"
django_secret_key="${DJANGO_SECRET_KEY:-$(random_secret)}"

printf "export PUBLIC_DOMAIN=%q\n" "$domain"
printf "export POSTGRES_PASSWORD=%q\n" "$postgres_password"
printf "export DJANGO_SECRET_KEY=%q\n" "$django_secret_key"
