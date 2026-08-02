#!/usr/bin/env bash
# Run on the VPS, from the project root, after `git pull`.
# Order matters: tailwind build must run before collectstatic, so the
# freshly compiled CSS is what gets copied into STATIC_ROOT.
set -euo pipefail

source venv/bin/activate

pip install -r requirements.txt

# Compiles theme/static_src/src/styles.css -> theme/static/css/dist/styles.css
# using the standalone tailwindcss binary (pytailwindcss). On first run on a
# fresh machine this downloads the Linux binary from GitHub releases, so the
# server needs outbound HTTPS access to github.com. It's cached afterwards in
# venv/lib/.../site-packages/pytailwindcss/bin/, so it only re-downloads if
# the venv is recreated or the pinned tailwind version changes.
python manage.py tailwind build

python manage.py collectstatic --noinput
python manage.py migrate --noinput

sudo systemctl restart gunicorn
