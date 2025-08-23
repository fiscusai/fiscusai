#!/usr/bin/env bash
set -euo pipefail
DATE=$(date +%Y-%m-%d_%H-%M-%S)
: "${DATABASE_URL:?DATABASE_URL required}"
OUT=${1:-"./backups"}
mkdir -p "$OUT"
pg_dump "$DATABASE_URL" | gzip > "$OUT/fiscus_${DATE}.sql.gz"
echo "Backup completed: $OUT/fiscus_${DATE}.sql.gz"
