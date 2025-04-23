#!/bin/bash

# Create directories if they don't exist
mkdir -p ./certs
mkdir -p ./traefik_dynamic

# Generate a configuration file for the certificate
cat > ./certs/openssl.cnf << EOF
[ req ]
default_bits       = 2048
default_keyfile    = key.pem
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

[ req_distinguished_name ]
C                  = US
ST                 = State
L                  = Locality
O                  = Organization
OU                 = Organizational Unit
CN                 = localhost

[ req_ext ]
subjectAltName     = @alt_names

[alt_names]
DNS.1   = localhost
DNS.2   = *.localhost
DNS.3   = *.sslip.io
DNS.4   = *.nip.io
DNS.5   = *.localtest.me
EOF

# Generate a self-signed certificate with the configuration
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./certs/key.pem \
  -out ./certs/cert.pem \
  -config ./certs/openssl.cnf

# Set appropriate permissions
chmod 600 ./certs/key.pem
chmod 644 ./certs/cert.pem

echo "Certificates have been generated successfully with support for *.sslip.io and *.nip.io"
echo "You can now start your Docker Compose environment"
