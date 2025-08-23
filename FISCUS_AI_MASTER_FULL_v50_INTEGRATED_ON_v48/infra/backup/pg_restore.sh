#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <s3://bucket/path.dump> <DATABASE_URL>"
  exit 1
fi
SRC="$1"; export DATABASE_URL="$2"
TMP="$(mktemp)"
echo "[*] Downloading $SRC ..."
aws s3 cp "$SRC" "$TMP"
echo "[*] Restoring to $DATABASE_URL ..."
pg_restore --clean --if-exists --no-owner --no-privileges --dbname="$DATABASE_URL" "$TMP"
rm -f "$TMP"
echo "[✓] Restore completed"
