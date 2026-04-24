#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

log_step() {
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

wait_for_database() {
  python - <<'PY'
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, "/app")

import django

django.setup()

from django.db import connections

connections["default"].cursor()
PY
}

log_step "⏳ Waiting for postgres"

# Wait specifically for the database so other startup failures remain visible.
until wait_for_database > /dev/null 2>&1; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

if [ "${RUN_BOOTSTRAP_TASKS:-0}" = "1" ]; then
  log_step "🧪 Postgres is up - checking migrations"
  python manage.py makemigrations --check --dry-run

  log_step "🛠️ Applying database migrations"
  # Reused Postgres volumes may already contain tables from initial Django apps
  # even when migration history is incomplete. `--fake-initial` safely marks
  # matching initial migrations as applied instead of trying to recreate tables.
  python manage.py migrate --noinput --fake-initial

  log_step "🔐 Seeding RBAC roles and permissions"
  python manage.py seed_roles

  log_step "🌍 Seeding platform core data"
  python seed_platform_core.py

  log_step "🏗️ Seeding marketplace workflow data"
  python seed_marketplace_workflow.py

  log_step "👥 Seeding descriptive users"
  python create_users.py

  log_step "🏠 Seeding property workflow samples"
  python seed_property_workflow.py
else
  log_step "↪️ Skipping bootstrap tasks for this service"
fi

log_step "🚀 Starting server"
exec "$@"
