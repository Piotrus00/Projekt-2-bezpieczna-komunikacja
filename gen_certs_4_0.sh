#!/usr/bin/env bash
set -euo pipefail

# Create CA
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout ca.key -out ca.crt \
  -days 365 -subj "/CN=Demo-CA"

# Server key and CSR
openssl req -newkey rsa:2048 -nodes \
  -keyout server.key -out server.csr \
  -subj "/CN=localhost"

# Sign server cert
openssl x509 -req -in server.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out server.crt -days 365

# Client key and CSR
openssl req -newkey rsa:2048 -nodes \
  -keyout client.key -out client.csr \
  -subj "/CN=client"

# Sign client cert
openssl x509 -req -in client.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out client.crt -days 365

# Cleanup
rm -f server.csr client.csr ca.srl

echo "Generated ca.crt, server.key, server.crt, client.key, client.crt"
