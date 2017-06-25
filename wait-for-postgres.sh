#!/bin/bash
# wait-for-postgres.sh

(echo >/dev/tcp/db/5432) &>/dev/null && echo "DB Open" || echo "DB Close"

exec python src/manage.py test