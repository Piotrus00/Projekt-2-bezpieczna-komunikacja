#!/usr/bin/env bash
set -euo pipefail

# Self-signed server certificate for localhost
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout server.key -out server.crt \
  -days 365 -subj "/CN=localhost"

echo "Generated server.key and server.crt"
