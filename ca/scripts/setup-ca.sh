#!/bin/bash
set -e

mkdir -p certs

cat > certs/ca-csr.json <<EOF
{
  "CN": "Local Kubernetes CA",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "Local",
      "O": "Kubernetes",
      "OU": "Local CA",
      "ST": "CA"
    }
  ]
}
EOF

cat > certs/ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "kubernetes": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}
EOF

brew install cfssl    
cfssl gencert -initca certs/ca-csr.json | cfssljson -bare certs/ca
