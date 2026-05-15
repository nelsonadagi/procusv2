#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/prod-env.sh"

load_prod_env "$DEFAULT_PUBLIC_DOMAIN"
write_prod_env

NGINX_SOURCE="$REPO_ROOT/infra/nginx/paanguzo.iqsaccodigital.com.conf"
NGINX_AVAILABLE="/etc/nginx/sites-available/paanguzo.iqsaccodigital.com.conf"
NGINX_ENABLED="/etc/nginx/sites-enabled/paanguzo.iqsaccodigital.com.conf"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Skipping host Nginx install: run as root to write /etc/nginx." >&2
  exit 0
fi

if ! command -v nginx >/dev/null 2>&1; then
  echo "Skipping host Nginx install: nginx is not installed." >&2
  echo "Install it with: apt-get update && apt-get install -y nginx" >&2
  exit 0
fi

if [[ ! -f "$NGINX_SOURCE" ]]; then
  echo "Missing Nginx source config: $NGINX_SOURCE" >&2
  exit 1
fi

echo "Installing host Nginx config for $PUBLIC_DOMAIN..."
install -m 0644 "$NGINX_SOURCE" "$NGINX_AVAILABLE"
ln -sfn "$NGINX_AVAILABLE" "$NGINX_ENABLED"

nginx -t
systemctl reload nginx || service nginx reload

echo "Host Nginx is proxying:"
echo "  http://$PUBLIC_DOMAIN -> frontend on 127.0.0.1:5173"
echo "  http://$PUBLIC_DOMAIN/api/ -> backend on 127.0.0.1:8007"
echo "For HTTPS, run: certbot --nginx -d $PUBLIC_DOMAIN"
