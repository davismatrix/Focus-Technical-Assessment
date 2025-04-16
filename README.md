# DevOps Tech Lead — Technical Assessment (Kubernetes & Co-Lo Infra)

## Overview

This project simulates an on-prem Kubernetes environment with no cloud dependencies. It includes a secure deployment pipeline, HAProxy Ingress, local TLS via cert-manager, and observability features.

---

## 1. Sample Application

- Language: python
- Endpoints:
  - `/` — returns `{"status":"ok"}`
  - `/healthz` — liveness probe
  - `/ready` — readiness probe
  - `/metrics` — Prometheus-compatible custom metric
- Logs structured to stdout (JSON)

---

## 2. Kubernetes Infrastructure

- Local cluster ( kind )
- HAProxy Ingress controller (via Helm)
- MetalLB (L2 mode) for external IP
- cert-manager with a CFSSL-based local CA
- TLS via Ingress + auto-renewing Certificate

---

## 3. CI/CD Pipeline

- Implemented with GitHub Actions:
  - Lints, tests, builds Python app
  - Builds + pushes Docker image to Dockerhub
  - Applies manifests (`kubectl`)
  - Waits for `/ready`


> See `.github/workflows/ci-cd.yaml`

---

## 4. Deployment Steps

```bash
# Create cluster and install tools (MetalLB, cert-manager, HAProxy) using kind
kind create cluster --name fta-k8-cluster --config ./ca/kind-cluster.yml

# Install tools (ca, cert-manager, MetalLB, HAProxy, map domain to external IP) using make to automate the installations and configurations
Make -C ./ca install all

# Build image locally and push app image docker hub
docker build -t MY_DOCKER_USERNAME/statusapp:latest .
docker push MY_DOCKER_USERNAME/statusapp:latest

# Deploy app
kubectl apply -f manifests/


