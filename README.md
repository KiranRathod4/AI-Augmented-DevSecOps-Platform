# AI-Augmented-DevSecOps-Platform

this is just text to undo the changes from the files
# Q: Tell me about a challenging problem you faced during a project and how you solved it. #
# Situation: #
While building a cloud-native DevSecOps platform using FastAPI microservices, Docker, PostgreSQL, GitHub Actions, and Kubernetes, I encountered an issue where my GitHub Actions CI pipeline was failing even though the application was working perfectly on my local machine.

# Task: #
My goal was to make the CI pipeline stable and ensure that automated tests could run successfully in both local and cloud environments without depending on Docker Compose-specific configurations.

# Action: #
I started by analyzing the GitHub Actions logs and compared the CI environment with my local setup. I discovered that the user-service was trying to connect to a PostgreSQL host named "db", which existed only inside the Docker Compose network. Since GitHub Actions did not have that service available, the tests failed during application startup.

To solve this, I introduced a dedicated testing mode using environment variables. I modified the application startup sequence to skip PostgreSQL initialization during test execution and configured the tests to use an isolated SQLite database instead. I then validated the changes by running tests locally and through GitHub Actions.

# Result: #
The CI pipeline became stable, all automated tests passed successfully, and the application could be tested independently of the production database environment. This improved the reliability of the pipeline and reinforced my understanding of environment isolation, automated testing, and systematic debugging in CI/CD workflows.



<!-- ============================================================
     AI-AUGMENTED DEVSECOPS PLATFORM — README
     Replace every [PLACEHOLDER] and screenshot path before publishing
     ============================================================ -->

<div align="center">

# 🛡️ AI-Augmented DevSecOps Platform

### A production-grade cloud-native platform demonstrating end-to-end DevSecOps engineering —
### CI/CD · Kubernetes · IaC · Observability · Security Scanning · LLM-powered Incident Response

<br/>

<!-- ── Badges ── update URLs once repo is public ──────────────── -->
[![CI Pipeline](https://github.com/YOUR_USERNAME/ai-augmented-devsecops-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/ai-augmented-devsecops-platform/actions/workflows/ci.yml)
[![Security Scan](https://github.com/YOUR_USERNAME/ai-augmented-devsecops-platform/actions/workflows/ci.yml/badge.svg?label=security)](https://github.com/YOUR_USERNAME/ai-augmented-devsecops-platform/actions)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=YOUR_PROJECT_KEY&metric=alert_status)](https://sonarcloud.io/summary/YOUR_PROJECT_KEY)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=YOUR_PROJECT_KEY&metric=coverage)](https://sonarcloud.io/summary/YOUR_PROJECT_KEY)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=YOUR_PROJECT_KEY&metric=bugs)](https://sonarcloud.io/summary/YOUR_PROJECT_KEY)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Containerised-blue?logo=docker)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326ce5?logo=kubernetes)](https://kubernetes.io)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7b42bc?logo=terraform)](https://terraform.io)
[![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws)](https://aws.amazon.com)

<br/>

<!-- ── Architecture diagram — replace src once created ─────────── -->
> 📌 **Architecture diagram coming soon** — add `docs/architecture.png` after Phase 5

<!--
<img src="docs/architecture.png" alt="System Architecture" width="900"/>
-->

</div>

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [Project Overview](#-project-overview) |
| 2 | [Why This Project](#-why-this-project) |
| 3 | [System Architecture](#-system-architecture) |
| 4 | [Tech Stack](#-tech-stack) |
| 5 | [Services](#-services) |
| 6 | [CI/CD Pipeline](#-cicd-pipeline) |
| 7 | [Security — DevSecOps](#-security--devsecops) |
| 8 | [Infrastructure as Code](#-infrastructure-as-code-terraform--aws) |
| 9 | [Monitoring & Observability](#-monitoring--observability) |
| 10 | [AI Incident Assistant](#-ai-incident-assistant) |
| 11 | [SLOs & Reliability](#-slos--reliability) |
| 12 | [Project Structure](#-project-structure) |
| 13 | [Prerequisites](#-prerequisites) |
| 14 | [Quick Start — Local](#-quick-start--local) |
| 15 | [Running Tests](#-running-tests) |
| 16 | [Kubernetes Deployment](#-kubernetes-deployment) |
| 17 | [Environment Variables](#-environment-variables) |
| 18 | [Screenshots & Results](#-screenshots--results) |
| 19 | [Runbooks](#-runbooks) |
| 20 | [Roadmap](#-roadmap) |
| 21 | [License](#-license) |

---

## 🎯 Project Overview

This project is a **production-grade DevSecOps platform** built from scratch to demonstrate
the full lifecycle of modern cloud-native software engineering — from local development
through automated CI/CD, cloud infrastructure, real-time observability, and AI-assisted
incident response.

It is not a tutorial clone. Every component is designed, written, and connected end-to-end
to reflect how real platform engineering teams operate at companies like PayPal, Goldman Sachs,
Apple, and Booking Holdings.

### What this platform does

```
Developer pushes code
       │
       ▼
GitHub Actions pipeline
  ├── Lint (ruff)
  ├── Unit tests + coverage (pytest)
  ├── Code quality gate (SonarQube)
  ├── Container security scan (Trivy)
  ├── Push to registry (ghcr.io)
  └── Deploy to Kubernetes (EKS)
       │
       ▼
Three microservices running on AWS EKS
  ├── api-gateway      — routes all traffic, instruments every request
  ├── user-service     — CRUD backed by RDS PostgreSQL
  └── load-simulator   — generates realistic traffic for observability
       │
       ▼
Full observability stack
  ├── Prometheus       — metrics collection
  ├── Grafana          — dashboards and RED metrics
  ├── Loki + Promtail  — log aggregation
  └── Alertmanager     — alert routing
       │
       ▼
AI Incident Assistant (unique feature)
  └── Alert fires → webhook → Claude API → Slack
      "Probable cause: user-service OOMKilled. Steps: ..."
```

---

## 💡 Why This Project

Most DevOps portfolios show a single service deployed to a cloud VM.
This platform deliberately covers **every layer of the stack** a junior SRE/DevOps engineer
would touch in their first year at a real company:

| Skill Area | What This Project Demonstrates |
|------------|-------------------------------|
| CI/CD | 5-job pipeline with security gates, not just "build and push" |
| Containers | Multi-stage Dockerfiles, non-root users, health checks |
| Kubernetes | Deployments, Services, HPA, probes, Helm charts |
| IaC | Terraform modules, remote state, multi-env provisioning |
| Cloud | AWS EKS, VPC, IAM, RDS, S3, DynamoDB |
| Security | Trivy CVE scanning + SonarQube code quality — both as pipeline gates |
| Observability | SLOs defined, RED metrics, alert rules, log aggregation |
| SRE practices | Runbooks, OpDoc, postmortem templates, error budgets |
| AI engineering | LLM integrated into the operational loop, not just as a toy |

---

## 🏗️ System Architecture

> 📌 **Replace this section with your actual diagram after Phase 5**
> Recommended tool: [Excalidraw](https://excalidraw.com) → export as PNG → save to `docs/architecture.png`

**High-level component map:**

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Actions CI/CD                      │
│  push → lint → test → sonarqube → trivy → push → deploy        │
└──────────────────────────────┬──────────────────────────────────┘
                               │ kubectl apply (Helm)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AWS EKS Cluster (Terraform)                  │
│                                                                  │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │ api-gateway  │───▶│ user-service │───▶│  RDS PostgreSQL  │   │
│  │  :8000      │    │   :8001      │    │                  │   │
│  └──────┬──────┘    └──────┬───────┘    └──────────────────┘   │
│         │                  │                                     │
│  ┌──────▼──────────────────▼───────────────────────────────┐   │
│  │              Prometheus (scrapes /metrics)               │   │
│  └──────┬──────────────────┬───────────────────────────────┘   │
│         │                  │                                     │
│  ┌──────▼──────┐   ┌───────▼──────┐   ┌────────────────────┐  │
│  │   Grafana   │   │ Alertmanager │   │   Loki + Promtail  │  │
│  │ dashboards  │   │ alert rules  │   │   log aggregation  │  │
│  └─────────────┘   └───────┬──────┘   └────────────────────┘  │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────── ┘
                              │ webhook
                              ▼
                  ┌───────────────────────┐
                  │  AI Incident Assistant │
                  │  (FastAPI + Claude API)│
                  └───────────┬───────────┘
                              │ Slack Block Kit message
                              ▼
                  ┌───────────────────────┐
                  │      Slack Channel     │
                  │   #incidents-alerts    │
                  └───────────────────────┘
```

**AWS infrastructure (Terraform-provisioned):**

```
AWS Region (ap-south-1)
└── VPC (10.0.0.0/16)
    ├── Public Subnets (10.0.1.0/24, 10.0.2.0/24) — AZ-a, AZ-b
    │   └── Application Load Balancer
    ├── Private Subnets (10.0.3.0/24, 10.0.4.0/24) — AZ-a, AZ-b
    │   ├── EKS Node Group (EC2 worker nodes)
    │   └── RDS PostgreSQL (Multi-AZ)
    └── S3 Bucket (Terraform remote state)
        DynamoDB Table (state locking)
```

---

## 🧰 Tech Stack

### Core engineering

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Language | Python | 3.11 | All service code |
| Web framework | FastAPI | 0.111.0 | REST APIs with async support |
| ORM | SQLAlchemy | 2.0.30 | Database access layer |
| Validation | Pydantic | 2.7.1 | Request/response schemas |
| Server | Uvicorn | 0.29.0 | ASGI server |

### Containerisation & Orchestration

| Category | Technology | Purpose |
|----------|-----------|---------|
| Containers | Docker + Buildx | Multi-stage builds, image creation |
| Local orchestration | docker-compose | Local development environment |
| Container registry | GitHub Container Registry (ghcr.io) | Image storage with SHA tags |
| Kubernetes (local) | Minikube | Local K8s testing |
| Kubernetes (cloud) | AWS EKS | Production cluster |
| K8s packaging | Helm | Parameterised chart deployment |

### CI/CD

| Category | Technology | Purpose |
|----------|-----------|---------|
| Pipeline | GitHub Actions | 5-job automated pipeline |
| Linting | ruff | Python code style enforcement |
| Testing | pytest + pytest-cov | Unit tests + coverage reports |
| Code quality | SonarQube / SonarCloud | Static analysis, bug detection, coverage gate |
| Security scanning | Trivy (Aqua Security) | Container CVE scanning — blocks HIGH/CRITICAL |
| Version control | Git | Branch strategy: main → develop → feature/* |

### Infrastructure as Code

| Category | Technology | Purpose |
|----------|-----------|---------|
| IaC tool | Terraform | All AWS resource provisioning |
| Cloud provider | AWS | Primary cloud |
| Networking | VPC, subnets, SGs | Isolated network topology |
| Cluster | EKS | Managed Kubernetes |
| Database | RDS PostgreSQL | Managed relational DB |
| State backend | S3 + DynamoDB | Remote state with locking |
| Auth (CI) | OIDC federation | Keyless AWS auth from GitHub Actions |

### Monitoring & Observability

| Category | Technology | Purpose |
|----------|-----------|---------|
| Metrics | Prometheus | Time-series scraping and storage |
| Dashboards | Grafana | RED metrics, SLO tracking, custom panels |
| Logs | Loki + Promtail | Log aggregation and querying |
| Alerting | Alertmanager | Alert routing, deduplication, silencing |
| Load testing | K6 | HPA validation, soak testing |

### AI Layer

| Category | Technology | Purpose |
|----------|-----------|---------|
| LLM | Claude API (claude-sonnet) | Root cause analysis generation |
| Trigger | Alertmanager webhook | Alert → AI assistant pipeline |
| Notification | Slack Block Kit | Structured incident messages |

---

## 🔧 Services

### 1. API Gateway (`services/api-gateway/`)

The single entry point for all external traffic.

**Responsibilities:**
- Receives all client requests on port `8000`
- Proxies requests to upstream microservices
- Instruments every request with Prometheus metrics (Counter + Histogram)
- Exposes `/health` (liveness) and `/ready` (readiness) probes
- Returns `503` if upstream is unreachable, `504` on timeout

**Prometheus metrics exposed:**

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `gateway_requests_total` | Counter | method, endpoint, http_status | Total requests through gateway |
| `gateway_request_duration_seconds` | Histogram | method, endpoint | Request latency distribution |

**Endpoints:**

```
GET  /health          → liveness probe
GET  /ready           → readiness probe (checks user-service)
GET  /metrics         → Prometheus scrape endpoint
GET  /api/users       → proxied to user-service
GET  /api/users/{id}  → proxied to user-service
POST /api/users       → proxied to user-service
DEL  /api/users/{id}  → proxied to user-service
GET  /docs            → auto-generated OpenAPI docs
```

---

### 2. User Service (`services/user-service/`)

Owns all user data. Backed by PostgreSQL.

**Responsibilities:**
- Full CRUD for user entities
- Validates and persists data via SQLAlchemy ORM
- Exposes custom Prometheus metrics (Gauge + Counter)
- Handles duplicate email with `409 Conflict`
- Initialises database tables on startup via `lifespan` context

**Prometheus metrics exposed:**

| Metric | Type | Description |
|--------|------|-------------|
| `user_service_users_created_total` | Counter | Total users ever created |
| `user_service_users_deleted_total` | Counter | Total users deleted |
| `user_service_active_users` | Gauge | Current user count (snapshot) |
| `user_service_requests_total` | Counter | Total HTTP requests |
| `user_service_request_duration_seconds` | Histogram | Request latency |

**Database schema:**

```sql
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
```

---

### 3. Load Simulator (`services/load-simulator/`)

Generates continuous realistic traffic so observability dashboards have meaningful data.

**Traffic distribution:**

| Action | Weight | Why |
|--------|--------|-----|
| `POST /api/users` | 25% | Creates users — increments counters |
| `GET  /api/users` | 35% | Most common read pattern |
| `GET  /api/users/{id}` | 25% | Single resource fetch |
| `GET  /health` | 10% | Simulates K8s probe traffic |
| `GET  /ready` | 5% | Simulates readiness checks |

Request interval is jittered (`±0.2s`) to prevent lockstep bursts that produce
artificially clean metrics.

---

### 4. AI Incident Assistant (`services/incident-assistant/`)

> 📌 **Built in Phase 4** — section will be completed then

Receives Alertmanager webhooks, calls the Claude API with alert context, and posts
a structured root cause analysis to Slack.

**Flow:**
```
Alertmanager fires alert
       │
       ▼  POST /webhook
AI Incident Assistant (FastAPI)
       │
       ├── Extracts: alert name, severity, labels, annotations
       ├── Builds prompt with system context
       │
       ▼  Claude API (claude-sonnet)
LLM generates:
  • Probable root cause (1–2 sentences)
  • Immediate mitigation steps (numbered list)
  • kubectl commands to investigate
  • Link to runbook
       │
       ▼  Slack Block Kit
#incidents channel receives structured message
```

**Sample Slack output:**

```
🔴 FIRING: HighErrorRate — api-gateway (devops-platform)
Severity: critical | Started: 2 minutes ago

Probable cause:
The user-service dependency is returning 5xx errors, causing the gateway
proxy to fail. This is consistent with a downstream OOM kill or DB
connection pool exhaustion.

Immediate steps:
1. kubectl logs -n devops-platform -l app=user-service --tail=50
2. kubectl describe pod -n devops-platform -l app=user-service
3. If crashlooping: kubectl rollout undo deployment/user-service

📖 Runbook: docs/runbooks/high-error-rate.md
```

---

## ⚙️ CI/CD Pipeline

Every `git push` to `main` or `develop`, and every Pull Request targeting `main`,
triggers the full pipeline.

```
┌──────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Pipeline                       │
│                                                                   │
│  ┌─────────┐                                                     │
│  │  lint   │  ruff · ~20s · every push                          │
│  └────┬────┘                                                     │
│       │ needs: lint                                              │
│  ┌────▼──────────────────────────┐                              │
│  │  test (matrix: 2 services)    │  pytest · coverage ≥70%      │
│  │  api-gateway ║ user-service   │  ~30s parallel               │
│  └────┬──────────────────────────┘                              │
│       │ needs: test                                              │
│  ┌────▼──────────────────────────┐                              │
│  │  sonarqube                    │  static analysis · bug gate  │
│  └────┬──────────────────────────┘                              │
│       │ needs: sonarqube                                         │
│  ┌────▼──────────────────────────┐                              │
│  │  build-scan (matrix: 2 svcs)  │  Trivy CVE scan             │
│  │  api-gateway ║ user-service   │  blocks HIGH/CRITICAL        │
│  └────┬──────────────────────────┘                              │
│       │ needs: build-scan · main branch only                    │
│  ┌────▼──────────────────────────┐                              │
│  │  push (matrix: 2 services)    │  ghcr.io · :sha + :latest   │
│  └────┬──────────────────────────┘                              │
│       │ needs: push · main branch only                          │
│  ┌────▼──────────────────────────┐                              │
│  │  deploy                       │  kubectl + Helm rollout      │
│  │  Minikube / EKS               │  rollout status + smoke test │
│  └───────────────────────────────┘                              │
└──────────────────────────────────────────────────────────────────┘
```

### Pipeline rules

| Rule | Detail |
|------|--------|
| PRs to `main` | Run lint + test + SonarQube + build-scan. Block merge if any fail. |
| Push to `develop` | Run full pipeline except push and deploy. |
| Push to `main` | Run full pipeline including push to registry and deploy. |
| Coverage gate | Pipeline fails if coverage drops below **70%** |
| SonarQube gate | Pipeline fails if Quality Gate status is not `PASSED` |
| Trivy gate | Pipeline fails on any `HIGH` or `CRITICAL` CVE with an available fix |

### Image tagging strategy

Every image gets two tags on every successful build:

| Tag | Example | Purpose |
|-----|---------|---------|
| `:sha-{7chars}` | `:sha-a1b2c3d` | Immutable — trace any running container to its exact commit |
| `:latest` | `:latest` | Floating — always points to newest successful build |

> **Why SHA tags matter**: During an incident at 3am you can run
> `kubectl describe pod` → see the image tag → `git show sha-a1b2c3d` → know exactly
> what code is running in 10 seconds.

---

## 🔒 Security — DevSecOps

Security is not an afterthought — it is a **mandatory pipeline gate**.
No code reaches production without passing both SonarQube and Trivy.

### SonarQube — Code Quality Gate

SonarQube performs static analysis on every CI run and enforces a Quality Gate before
images are built or pushed.

**What SonarQube checks:**

| Category | What it catches |
|----------|----------------|
| Bugs | Code that will definitely behave incorrectly |
| Vulnerabilities | Security weaknesses (OWASP Top 10) |
| Security hotspots | Code that needs human security review |
| Code smells | Maintainability issues, dead code, complexity |
| Coverage | Ensures test coverage meets the defined threshold |
| Duplications | Copy-paste code that increases maintenance burden |

**Quality Gate conditions (this project):**

| Metric | Threshold | On failure |
|--------|-----------|-----------|
| New bugs | 0 | ❌ Pipeline blocked |
| New vulnerabilities | 0 | ❌ Pipeline blocked |
| New security hotspots reviewed | 100% | ❌ Pipeline blocked |
| New coverage | ≥ 70% | ❌ Pipeline blocked |
| New duplications | ≤ 3% | ❌ Pipeline blocked |

> 📌 **Screenshots** — add SonarQube dashboard screenshots to `docs/screenshots/sonarqube/`

<!--
<img src="docs/screenshots/sonarqube/quality-gate.png" alt="SonarQube Quality Gate" width="800"/>
<img src="docs/screenshots/sonarqube/issues.png" alt="SonarQube Issues" width="800"/>
-->

**CI integration:**

```yaml
# Excerpt from .github/workflows/ci.yml
sonarqube:
  name: SonarQube Analysis
  runs-on: ubuntu-latest
  needs: test
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0          # Full history required for blame and new-code detection
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**sonar-project.properties** (at project root):

```properties
sonar.projectKey=YOUR_PROJECT_KEY
sonar.organization=YOUR_ORG
sonar.sources=services/api-gateway,services/user-service
sonar.tests=services/api-gateway/tests,services/user-service/tests
sonar.python.coverage.reportPaths=coverage-api-gateway.xml,coverage-user-service.xml
sonar.python.version=3.11
sonar.exclusions=**/venv/**,**/__pycache__/**,**/migrations/**
```

---

### Trivy — Container Vulnerability Scanning

Trivy scans every Docker image built in CI for known CVEs (Common Vulnerabilities
and Exposures) before it can be pushed to the registry.

**Configuration:**

| Setting | Value | Reason |
|---------|-------|--------|
| Severity | `HIGH,CRITICAL` | Only block on serious vulnerabilities |
| `ignore-unfixed` | `true` | Only fail on CVEs that have a patched version available |
| `exit-code` | `1` | Non-zero exit fails the pipeline |
| Scope | `os,library` | Scans both base image OS packages and Python dependencies |

**When Trivy blocks a build:**

```bash
# Run locally to see what Trivy found
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  ghcr.io/YOUR_USERNAME/api-gateway:latest

# Fix: update the offending dependency in requirements.txt
# or update the base image: FROM python:3.11-slim → FROM python:3.11.X-slim (latest patch)
```

> 📌 **Screenshots** — add Trivy scan result screenshots to `docs/screenshots/trivy/`

---

### Security best practices applied

| Practice | Where applied |
|----------|--------------|
| Non-root container user | All Dockerfiles — `adduser appuser` |
| Read-only filesystem | Docker layer — `COPY --chown=appuser` |
| No secrets in code | All secrets via environment variables or K8s Secrets |
| Least-privilege IAM | Terraform IAM roles with minimal policy attachments |
| OIDC federation | No long-lived AWS credentials stored in GitHub |
| Private subnets | Database and worker nodes not internet-accessible |
| Security groups | Ingress rules allow only required ports |

---

## 🌍 Infrastructure as Code — Terraform + AWS

> 📌 **Built in Phase 3** — update this section with your actual Terraform module outputs

All AWS infrastructure is defined as code — no manual console clicking.
This means the entire environment can be destroyed and recreated identically in minutes.

### Infrastructure overview

```
terraform/
├── main.tf                    # Root module — calls child modules
├── variables.tf               # Input variables (region, env, etc.)
├── outputs.tf                 # Cluster endpoint, DB URL, etc.
├── backend.tf                 # S3 remote state configuration
├── terraform.tfvars.example   # Example values — never commit .tfvars
└── modules/
    ├── vpc/                   # VPC, subnets, IGW, NAT gateway, route tables
    ├── eks/                   # EKS cluster, node group, OIDC provider
    ├── rds/                   # RDS PostgreSQL, subnet group, parameter group
    └── iam/                   # Service roles, policies, OIDC federation
```

### Key design decisions

| Decision | Rationale |
|----------|-----------|
| Remote state in S3 | Enables team collaboration without state conflicts |
| DynamoDB locking | Prevents concurrent `terraform apply` from corrupting state |
| Private subnets for nodes | Worker nodes not directly internet-accessible |
| Multi-AZ RDS | Automatic failover — no single point of failure for database |
| OIDC federation | GitHub Actions authenticates to AWS without long-lived keys |
| Reusable modules | Same module called with different `tfvars` for dev/staging/prod |

### Workflow

```bash
# First time setup — create remote state bucket
cd terraform/bootstrap
terraform init && terraform apply

# Provision full environment
cd terraform/
terraform init
terraform plan -var-file=environments/dev.tfvars    # review diff
terraform apply -var-file=environments/dev.tfvars   # create resources

# Update kubeconfig to talk to EKS
aws eks update-kubeconfig --name devops-platform-dev --region ap-south-1

# Destroy when done (saves cost)
terraform destroy -var-file=environments/dev.tfvars
```

> 📌 **Screenshots** — add `terraform plan` output and AWS console screenshots to `docs/screenshots/terraform/`

---

## 📊 Monitoring & Observability

The observability stack answers three questions at all times:
- **Is it healthy?** — Grafana dashboards
- **What broke?** — Alertmanager + Loki logs
- **Why did it break?** — AI Incident Assistant + runbooks

### Deployed via Helm

```bash
# Install kube-prometheus-stack (Prometheus + Grafana + Alertmanager)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f helm/monitoring-values.yaml

# Install Loki stack
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack \
  -n monitoring \
  -f helm/loki-values.yaml
```

### Grafana dashboards

| Dashboard | What it shows |
|-----------|--------------|
| **Service Overview** | Request rate, error rate, p50/p95/p99 latency for all services |
| **API Gateway RED** | Rate · Errors · Duration for the gateway specifically |
| **User Service** | Active users gauge, create/delete counters, DB query latency |
| **Kubernetes Health** | Pod status, restarts, CPU/memory per deployment |
| **SLO Tracking** | Availability vs target, error budget burn rate |
| **Load Test Results** | Request rate during K6 soak test, HPA scale-out events |

> 📌 **Screenshots** — add Grafana dashboard screenshots to `docs/screenshots/grafana/`

<!--
<img src="docs/screenshots/grafana/service-overview.png" alt="Service Overview Dashboard" width="800"/>
<img src="docs/screenshots/grafana/slo-tracking.png" alt="SLO Tracking Dashboard" width="800"/>
-->

### Alert rules

| Alert Name | Condition | Severity | Action |
|------------|-----------|----------|--------|
| `HighErrorRate` | `rate(errors[5m]) > 5%` for 2m | critical | AI assistant + on-call |
| `HighLatency` | `p99 latency > 500ms` for 5m | warning | AI assistant |
| `PodCrashLooping` | restart count > 3 in 10m | critical | AI assistant + on-call |
| `LowErrorBudget` | error budget < 50% remaining | warning | Engineering review |
| `ServiceDown` | `/health` returns non-200 | critical | Immediate escalation |
| `HighMemoryUsage` | memory > 80% of limit for 5m | warning | Capacity review |

### PromQL queries used

```promql
# Request rate (requests per second over last 5 minutes)
rate(gateway_requests_total[5m])

# Error rate percentage
rate(gateway_requests_total{http_status=~"5.."}[5m])
/ rate(gateway_requests_total[5m]) * 100

# 99th percentile latency
histogram_quantile(0.99,
  rate(gateway_request_duration_seconds_bucket[5m]))

# Active users current count
user_service_active_users

# Error budget burn rate
1 - (
  sum(rate(gateway_requests_total{http_status!~"5.."}[1h]))
  / sum(rate(gateway_requests_total[1h]))
)
```

---

## 🤖 AI Incident Assistant

> 📌 **Built in Phase 4** — update with real Slack screenshots when complete

The AI Incident Assistant is a Python FastAPI service that connects the monitoring
stack to an LLM, creating an automated first-responder that reduces mean time to
diagnosis (MTTD) for production incidents.

### How it works

```python
# Simplified flow — see services/incident-assistant/main.py for full code

@app.post("/webhook")
async def receive_alert(alert: AlertmanagerPayload):
    for alert in payload.alerts:
        context = build_context(alert)     # extract name, labels, severity
        analysis = await call_claude(context)  # LLM generates root cause
        await post_to_slack(analysis)          # structured Slack message
```

### Claude API prompt design

```
System: You are an expert SRE assisting with a production incident on a
        Kubernetes-based microservices platform. Be concise, specific, and
        actionable. Always include exact kubectl commands.

User:   Alert: {alert_name}
        Severity: {severity}
        Service: {labels.app} in namespace {labels.namespace}
        Labels: {labels}
        Annotations: {annotations}

        Provide:
        1. Probable root cause (2 sentences max)
        2. Immediate mitigation steps (numbered, with exact commands)
        3. Investigation commands (kubectl, logs)
        4. When to escalate
```

> 📌 **Screenshots** — add Slack message screenshots to `docs/screenshots/ai-assistant/`

<!--
<img src="docs/screenshots/ai-assistant/slack-alert.png" alt="AI Assistant Slack Message" width="600"/>
-->

---

## 📈 SLOs & Reliability

Service Level Objectives are formally defined and tracked in Grafana.

| Service | SLI | SLO Target | Error Budget (30 days) |
|---------|-----|-----------|----------------------|
| api-gateway | Availability | ≥ 99.5% | 3.6 hours downtime |
| api-gateway | p99 latency | ≤ 200ms | — |
| user-service | Availability | ≥ 99.0% | 7.2 hours downtime |
| user-service | p95 latency | ≤ 150ms | — |

**Error budget policy:**
- Budget > 50% remaining → normal development velocity
- Budget 25–50% remaining → reduce deployment frequency, review incidents
- Budget < 25% remaining → freeze non-critical deployments, focus on reliability

---

## 📁 Project Structure

```
ai-augmented-devsecops-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # 5-job CI/CD pipeline
│
├── services/
│   ├── api-gateway/
│   │   ├── main.py                   # FastAPI app — routing, metrics, proxy
│   │   ├── requirements.txt
│   │   ├── Dockerfile                # Multi-stage, non-root
│   │   ├── .dockerignore
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_main.py          # Unit tests with mocked upstreams
│   │
│   ├── user-service/
│   │   ├── main.py                   # CRUD endpoints, Prometheus metrics
│   │   ├── models.py                 # SQLAlchemy ORM model
│   │   ├── database.py               # Engine, session, dependency
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_main.py          # Tests with SQLite in-memory DB
│   │
│   ├── load-simulator/
│   │   ├── main.py                   # Weighted async traffic generator
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── incident-assistant/           # Phase 4
│       ├── main.py                   # Alertmanager webhook → Claude → Slack
│       ├── requirements.txt
│       └── Dockerfile
│
├── k8s/                              # Raw Kubernetes manifests (Phase 2)
│   ├── namespace.yaml
│   ├── api-gateway.yaml
│   └── user-service.yaml
│
├── helm/                             # Helm charts (Phase 3)
│   ├── devops-platform/
│   │   ├── Chart.yaml
│   │   ├── values.yaml               # Default values
│   │   ├── values-dev.yaml
│   │   ├── values-prod.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── hpa.yaml
│   │       └── servicemonitor.yaml
│   ├── monitoring-values.yaml        # kube-prometheus-stack overrides
│   └── loki-values.yaml
│
├── terraform/                        # Phase 3
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── backend.tf
│   ├── terraform.tfvars.example
│   ├── environments/
│   │   ├── dev.tfvars
│   │   └── prod.tfvars
│   └── modules/
│       ├── vpc/
│       ├── eks/
│       ├── rds/
│       └── iam/
│
├── docs/
│   ├── architecture.png              # System architecture diagram
│   ├── OPERATIONS.md                 # OpDoc — how to operate the system
│   ├── runbooks/
│   │   ├── high-error-rate.md
│   │   ├── pod-crashlooping.md
│   │   ├── high-latency.md
│   │   └── service-down.md
│   └── screenshots/
│       ├── grafana/
│       ├── sonarqube/
│       ├── trivy/
│       ├── ci-pipeline/
│       └── ai-assistant/
│
├── sonar-project.properties          # SonarQube config
├── pyproject.toml                    # ruff + pytest config
├── docker-compose.yml                # Local development
├── .env.example                      # Environment variable template
├── .gitignore
└── README.md
```

---

## ✅ Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) or `pyenv` |
| Docker Desktop | latest | [docker.com](https://docker.com) — must be **running** before any docker commands |
| Git | any | [git-scm.com](https://git-scm.com) |
| kubectl | 1.28+ | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools) |
| Minikube | 1.33+ | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io) |
| Terraform | 1.7+ | [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform/downloads) |
| AWS CLI | 2.x | [aws.amazon.com/cli](https://aws.amazon.com/cli) |
| Helm | 3.x | [helm.sh](https://helm.sh) |

> ⚠️ **Windows users**: Docker Desktop must be fully started (whale icon in system tray,
> not animating) before running any `docker compose` commands.
> If you see `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file`
> — Docker Desktop is not running.

---

## 🚀 Quick Start — Local

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-augmented-devsecops-platform.git
cd ai-augmented-devsecops-platform

# 2. Copy environment file
cp .env.example .env

# 3. Start Docker Desktop (ensure whale icon is visible in system tray)

# 4. Build all images
docker compose build

# 5. Start all services
docker compose up -d

# 6. Verify everything is running
docker compose ps
```

**Verify the platform is healthy:**

```bash
# Gateway health check
curl http://localhost:8000/health
# → {"status":"healthy","service":"api-gateway","version":"1.0.0"}

# Readiness — checks user-service is reachable
curl http://localhost:8000/ready
# → {"status":"ready","upstreams":{"user-service":"ok"}}

# Create a user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Priya Sharma", "email": "priya@devops.io"}'
# → {"id":1,"name":"Priya Sharma","email":"priya@devops.io","created_at":"..."}

# List all users
curl http://localhost:8000/api/users

# Prometheus metrics
curl http://localhost:8000/metrics | head -20
```

**Auto-generated API docs** (open in browser):
- API Gateway: [http://localhost:8000/docs](http://localhost:8000/docs)
- User Service: [http://localhost:8001/docs](http://localhost:8001/docs)

**Stop everything:**
```bash
docker compose down          # keeps data
docker compose down -v       # wipes database too
```

---

## 🧪 Running Tests

```bash
# Install dependencies
pip install -r services/api-gateway/requirements.txt
pip install -r services/user-service/requirements.txt

# Run linter
ruff check services/

# Auto-fix linting issues
ruff check services/ --fix

# Run all tests with coverage
pytest services/api-gateway/tests/ services/user-service/tests/ -v

# Run with coverage report
pytest services/api-gateway/tests/ services/user-service/tests/ \
  --cov=services \
  --cov-report=html \
  --cov-report=term-missing

# Run a specific service's tests only
pytest services/user-service/tests/ -v -k "TestCreateUser"

# View HTML coverage report
open htmlcov/index.html    # macOS
start htmlcov/index.html   # Windows
```

**Expected output:**

```
================================= test session starts ==================================
collected 20 items

services/api-gateway/tests/test_main.py::TestHealthEndpoints::test_health_returns_200 PASSED
services/api-gateway/tests/test_main.py::TestHealthEndpoints::test_health_response_shape PASSED
...
services/user-service/tests/test_main.py::TestCreateUser::test_create_user_returns_201 PASSED
...
================================= 20 passed in 1.43s ===================================
Coverage: api-gateway 78% | user-service 82%
```

> 📌 **Screenshots** — add test output and coverage report screenshots to `docs/screenshots/ci-pipeline/`

---

## ☸️ Kubernetes Deployment

### Local (Minikube)

```bash
# Start Minikube
minikube start --cpus=2 --memory=2048

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy services
kubectl apply -f k8s/user-service.yaml
kubectl apply -f k8s/api-gateway.yaml

# Verify rollout
kubectl rollout status deployment/user-service -n devops-platform
kubectl rollout status deployment/api-gateway -n devops-platform

# Check pods
kubectl get pods -n devops-platform

# Access gateway (Minikube)
minikube service api-gateway -n devops-platform --url
```

### Cloud (AWS EKS via Helm)

```bash
# Configure kubectl for EKS
aws eks update-kubeconfig --name devops-platform-dev --region ap-south-1

# Deploy with Helm (dev environment)
helm upgrade --install devops-platform ./helm/devops-platform \
  -f helm/devops-platform/values-dev.yaml \
  -n devops-platform --create-namespace

# Verify
kubectl get all -n devops-platform
```

### Useful Kubernetes commands

```bash
# Get all resources in the namespace
kubectl get all -n devops-platform

# Stream logs from a service
kubectl logs -n devops-platform -l app=api-gateway -f

# Describe a deployment (shows events and conditions)
kubectl describe deployment api-gateway -n devops-platform

# Shell into a running container
kubectl exec -it -n devops-platform \
  $(kubectl get pod -n devops-platform -l app=api-gateway -o jsonpath='{.items[0].metadata.name}') \
  -- bash

# Rollback a deployment
kubectl rollout undo deployment/api-gateway -n devops-platform

# Scale manually
kubectl scale deployment api-gateway --replicas=3 -n devops-platform

# Port-forward Grafana dashboard
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` for local development.
**Never commit `.env` to Git.**

```bash
# ── Database ───────────────────────────────────────────────────────────
DATABASE_URL=postgresql://devops:devops123@db:5432/userdb
POSTGRES_DB=userdb
POSTGRES_USER=devops
POSTGRES_PASSWORD=devops123           # change in production

# ── Service URLs ───────────────────────────────────────────────────────
USER_SERVICE_URL=http://user-service:8001
GATEWAY_URL=http://api-gateway:8000

# ── Load simulator ─────────────────────────────────────────────────────
REQUEST_INTERVAL=0.8                  # seconds between requests
STARTUP_DELAY=8                       # wait N seconds before starting traffic

# ── AI Incident Assistant (Phase 4) ────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-...          # from console.anthropic.com
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_CHANNEL=#incidents-alerts

# ── AWS (Phase 3) ──────────────────────────────────────────────────────
AWS_REGION=ap-south-1
# Do NOT put AWS_ACCESS_KEY_ID / SECRET here — use OIDC or aws configure
```

**Kubernetes Secrets (production):**

```bash
# Create secret from .env file
kubectl create secret generic app-secrets \
  --from-env-file=.env \
  -n devops-platform

# Or create individual secrets
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="postgresql://..." \
  -n devops-platform
```

---

## 🖼️ Screenshots & Results

> 📌 **All screenshots will be added after each phase is complete.**
> Replace the placeholder comments with actual `<img>` tags as you progress.

### CI/CD Pipeline

<!-- Add after Phase 2 -->
> 📌 `docs/screenshots/ci-pipeline/pipeline-passing.png` — GitHub Actions all-green run
> 📌 `docs/screenshots/ci-pipeline/pipeline-trivy-block.png` — Trivy blocking a CVE

### SonarQube Quality Gate

<!-- Add after Phase 2 -->
> 📌 `docs/screenshots/sonarqube/quality-gate-passed.png` — SonarQube dashboard showing PASSED
> 📌 `docs/screenshots/sonarqube/coverage-report.png` — Coverage breakdown by file

### Grafana Dashboards

<!-- Add after Phase 4 -->
> 📌 `docs/screenshots/grafana/service-overview.png` — RED metrics with real traffic
> 📌 `docs/screenshots/grafana/slo-dashboard.png` — SLO tracking and error budget
> 📌 `docs/screenshots/grafana/k8s-health.png` — Pod health during load test
> 📌 `docs/screenshots/grafana/load-test-spike.png` — HPA scaling under K6 load

### AI Incident Assistant

<!-- Add after Phase 4 -->
> 📌 `docs/screenshots/ai-assistant/slack-critical-alert.png` — Critical alert Slack message
> 📌 `docs/screenshots/ai-assistant/slack-warning-alert.png` — Warning alert Slack message

### Terraform

<!-- Add after Phase 3 -->
> 📌 `docs/screenshots/terraform/terraform-plan.png` — terraform plan output
> 📌 `docs/screenshots/terraform/eks-cluster.png` — EKS cluster in AWS console

---

## 📖 Runbooks

Runbooks are step-by-step response guides for each alert type.
They are linked in every AI assistant Slack message.

| Runbook | Alert | Location |
|---------|-------|----------|
| High Error Rate | `HighErrorRate` | [docs/runbooks/high-error-rate.md](docs/runbooks/high-error-rate.md) |
| Pod Crashlooping | `PodCrashLooping` | [docs/runbooks/pod-crashlooping.md](docs/runbooks/pod-crashlooping.md) |
| High Latency | `HighLatency` | [docs/runbooks/high-latency.md](docs/runbooks/high-latency.md) |
| Service Down | `ServiceDown` | [docs/runbooks/service-down.md](docs/runbooks/service-down.md) |

**Operations document:** [docs/OPERATIONS.md](docs/OPERATIONS.md)
— Covers deployment procedure, rollback steps, escalation path, and known issues.

---

## 🗺️ Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 — Microservices | ✅ Complete | FastAPI services + Docker + docker-compose |
| Phase 2 — CI/CD | ✅ Complete | GitHub Actions + SonarQube + Trivy + deploy |
| Phase 3 — IaC | 🔄 In progress | Terraform + AWS EKS + Helm charts |
| Phase 4 — Monitoring + AI | ⏳ Upcoming | Prometheus + Grafana + AI incident assistant |
| Phase 5 — Polish | ⏳ Upcoming | Docs, architecture diagram, demo video |

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with purpose. Documented with care. Deployed with confidence.**

*A fresher project built to production standards.*

</div>
