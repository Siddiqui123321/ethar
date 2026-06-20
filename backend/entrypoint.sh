#!/bin/sh
set -e

# Wait for DB to be reachable (best-effort)
python wait_for_db.py

# Run Alembic migrations (if any)
if command -v alembic >/dev/null 2>&1; then
  alembic -c alembic.ini upgrade head || echo "Alembic upgrade failed or no migrations"
fi

# Exec the container CMD
exec "$@"
