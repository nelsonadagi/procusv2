#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Waiting for postgres..."

# Using a simple check for postgres. 
# While this isn't perfect, it's a common pattern.
until python manage.py check > /dev/null 2>&1; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing migrations"
python manage.py migrate --noinput

echo "Seeding descriptive users..."
python create_users.py

echo "Starting server"
exec "$@"
