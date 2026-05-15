#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/prod-env.sh"

load_prod_env "$DEFAULT_PUBLIC_DOMAIN"
write_prod_env

POSTGRES_DB="${POSTGRES_DB:-marketplace}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

compose() {
  COMPOSE_DISABLE_ENV_FILE=1 docker compose -f docker-compose.yml -f docker-compose.prod.yml "$@"
}

echo "Starting Postgres and Redis..."
compose up -d postgres redis

echo "Waiting for Postgres container health..."
for i in $(seq 1 60); do
  if compose exec -T postgres pg_isready -U "$POSTGRES_USER" >/dev/null 2>&1; then
    break
  fi
  if [[ "$i" -eq 60 ]]; then
    echo "Postgres did not become ready in time." >&2
    exit 1
  fi
  sleep 2
done

echo "Creating/updating Postgres role and database..."
compose exec -T postgres psql -U "$POSTGRES_USER" -d postgres \
  -v db_name="$POSTGRES_DB" \
  -v db_user="$POSTGRES_USER" \
  -v db_password="$POSTGRES_PASSWORD" <<'SQL'
ALTER USER :"db_user" WITH PASSWORD :'db_password';
SELECT format('CREATE DATABASE %I OWNER %I', :'db_name', :'db_user')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'db_name')\gexec
SQL

echo "Verifying Django database connection..."
compose run --rm --no-deps --build \
  -e RUN_BOOTSTRAP_TASKS=0 \
  backend python - <<'PY'
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, "/app")

import django

django.setup()

from django.db import connections

with connections["default"].cursor() as cursor:
    cursor.execute("SELECT 1")
    cursor.fetchone()
PY

echo "Postgres is prepared for Django."
