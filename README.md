<p align="center">
  <img src="./assets/banner.png" alt="AI Security Platform Banner" width="100%">
</p>

<p align="center"><sub><strong>AI × Cloud × Security — Core DNA</strong></sub></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/FastAPI-async%20API-009688" />
  <img src="https://img.shields.io/badge/Scikit--learn-ML-orange" />
  <img src="https://img.shields.io/badge/Docker-containerization-2496ED" />
  <img src="https://img.shields.io/badge/Kubernetes-orchestration-326CE5" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF" />
  <img src="https://img.shields.io/badge/Security-OWASP%20Top%2010-critical" />
</p>

<p align="center">
  <a href="./ROADMAP.md"><strong>📘 View Full Technical Roadmap</strong></a>
</p>

<p align="center">
  <a href="./README.ja.md">🇯🇵 Japanese Version (日本語版)</a>
</p>

# AI Security Platform: Backend & Infrastructure ▣

An **AI-driven security platform project** focused on building a **production-oriented backend** for **log anomaly detection**, designed with enterprise-grade architecture in mind and a long-term vision toward an **autonomous security agent**.

Key engineering areas include:

- **Inference latency optimization**
- **Model drift monitoring**
- **Kubernetes-based orchestration**
- **OWASP-aligned hardening**

This project serves as a practical showcase of AI backend engineering and cloud-native security design.

---

## 📍 Current Status: [Phase 1 - AI Anomaly Detection & Hybrid Detection 🚧]
The Phase 0 FastAPI foundation is complete, and the project is now progressing through **Phase 1: AI Anomaly Detection & Hybrid Detection**.
The current `POST /analyze` endpoint performs real-time analysis by combining feature engineering, anomaly scoring, rule-based detection, and threshold-based decision logic.

Recently, Regex-based SQL Injection detection and Directory Traversal detection were added to detect known attack patterns.
The rule evaluation flow is also structured with **RuleEvaluationResult** and **RuleMatchInfo**, making it possible to trace which rule matched, which field was evaluated, and which pattern triggered the detection.

### 🔄 Latest Engineering Updates
- **Completed**: Phase 0 (FastAPI foundations, Pydantic v2 validation, and structured logging).
- **Implemented**: Real-time analysis flow via `POST /analyze`.
- **Implemented**: Regex-based **SQL Injection detection** and **Directory Traversal detection**.
- **Implemented**: Structured rule evaluation using `RuleEvaluationResult` / `RuleMatchInfo`.
- **In Progress**: Improving anomaly detection logic, inference latency optimization, and Decision Context expansion.
- **Upcoming**: Request ID propagation, Shadow Mode, and Redis-based stateful detection.

## 💠 Engineering Pillars
This platform is built around four core engineering domains:
- **AI/ML**: Implementing anomaly detection and preparing for future autonomous agent logic.
- **Backend**: High-performance asynchronous APIs with FastAPI.
- **Infrastructure**: Container orchestration (K8s), CI/CD, and Cloud-Native scaling.
- **Security & SRE**: OWASP-aligned hardening and full-stack observability.

### 🧬 Project Evolution (10-Phase Roadmap)
This project ensures enterprise-grade scalability by progressing through these strategic stages:

* **Phases 0-1**: Backend Foundations, AI Anomaly Detection & Hybrid Detection (FastAPI, Scikit-learn, Rule-based Detection)
* **Phases 2-3**: API Hardening & Container Security (JWT, RBAC, Trivy, SBOM)
* **Phases 4-6**: K8s Orchestration & Autonomous Response (Prometheus, Network Policies)
* **Phases 7-10 (Global Scaling)**: 
    * **AWS**: Production IaC with **Terraform** & EKS.
    * **GCP**: Advanced **MLOps** with Vertex AI & BigQuery ML.
    * **Azure**: Enterprise Security & **Azure OpenAI (Advanced LLM)** Integration
    * **Global**: Multi-Region redundancy, Chaos Engineering, and **FinOps**.

> *Detailed tasks for each phase can be found in [**ROADMAP.md**](./ROADMAP.md).*

## 🔭 Long-Term Vision

This project aims to evolve into a **fully autonomous, cloud-native AI Security Platform** capable of:

- **Real-time threat detection and autonomous response**
- **Production-grade availability** across AWS, GCP, and Azure
- **LLM-powered incident summarization and explainability**
- **Global-scale operation** through multi-region redundancy and continuous learning

To translate that long-term vision into a more concrete technical direction,
the following diagram outlines the **target architecture** the project is intended to grow toward over time.

## 📡 Target Architecture

This diagram illustrates the intended end-state design that guides future development across backend services, AI/ML, observability, and platform infrastructure.

<p align="center">
  <img src="assets/ai-security-architecture-2026-06-19.png" width="900" alt="Target System Architecture">
</p>

## 🔍 Architecture Breakdown  (Loosely Coupled Component Design)

- **API Gateway / Ingress**: Serves as the secure L7 entry point, terminating external traffic and routing requests into the internal platform.
- **Backend Services (FastAPI)**: Provides a high‑throughput asynchronous API layer. Centralizes core business logic including request validation, authentication/authorization, and persistence workflows backed by PostgreSQL.
- **AI Security Engine**: A core component responsible for ensuring platform‑wide security in real time. Processes streaming logs, extracts features, and performs integrated anomaly detection and threat scoring.
- **MLOps & Tracking (MLflow / Evidently AI)**: Monitors model behavior, inference latency, and performance drift to maintain a reliable and observable AI lifecycle.
- **Observability Stack**: Delivers end‑to‑end visibility across the system using Prometheus, Grafana, ELK, and Trivy to collect metrics, logs, and security signals.

## 🛠 Tech Stack

**Tech Stack Overview:**  
The stack is designed to support the architecture long‑term while ensuring scalability, extensibility, and flexibility for future feature expansion.

### 🟢 Active (Phases 0–1)
*Core technologies currently used to build the foundation and AI implementation.*

- **Python 3.12**: Core language for backend development, ML pipelines, and security analytics.
- **FastAPI**: Asynchronous, high-performance API framework for request validation, routing, and API orchestration.
- **Pydantic v2**: Schema validation and data integrity for API inputs and outputs.
- **Structured Logging**: JSON-based logging foundation designed for future AI ingestion and observability workflows.
- **AI Security Engine (Isolation Forest-based)**: Core anomaly detection component under active implementation in Phase 1.
- **Rule-based Security Detection**: Detects known attack patterns such as SQL Injection and Directory Traversal using Regex-based rules.
- **Traceable Rule Evaluation**: Uses `RuleEvaluationResult` / `RuleMatchInfo` to preserve detection reasons, matched patterns, and evaluated fields.
- **MLflow**: Experiment tracking and model versioning during Phase 1 training.
- **Pytest**: Testing foundation for future unit and integration tests.
- **Ruff**: Linting and formatting for consistent code quality.
- **GitHub Actions (CI/CD-ready)**: Automated pipelines for testing and linting, designed to expand toward deployment workflows in later phases.

### 🔘 Planned (Phases 2–10)
*Strategic technologies to be integrated in roadmap order as the platform evolves.*

#### Phase 2 — Security & Persistence
- **PostgreSQL**: Persistent relational storage for authentication, CRUD operations, and structured logs.
- **Alembic**: Database migration management for schema evolution.
- **Passlib / JWT**: Secure password hashing and token-based authentication.
- **RBAC**: Role-based access control for secure authorization.

#### Phase 3 — Container Security
- **Trivy**: Container and dependency vulnerability scanning.
- **python:3.12-slim**: Minimal base image to reduce attack surface and improve container efficiency.
- **pip-audit / safety**: Dependency integrity and vulnerability validation.
- **SBOM Tooling**: Software Bill of Materials generation for transparency and supply-chain visibility.
- **Hardened GitHub Actions**: Secure CI pipeline design against supply-chain risks.

#### Phase 4 — SRE & Observability
- **Evidently AI**: Drift detection and inference quality monitoring.
- **Prometheus / Grafana**: Metrics collection, visualization, and alerting.
- **ELK Stack**: Centralized log aggregation and search for operational visibility.

#### Phase 5 — Kubernetes & Cloud Native
- **Kubernetes (kind → EKS / GKE)**: Container orchestration path from local clusters to cloud deployment.
- **Ingress Controller + TLS**: Secure Layer 7 traffic management and HTTPS termination.
- **Network Policies / Pod Security Standards**: Least-privilege runtime hardening.
- **HPA**: Horizontal Pod Autoscaling for scalable inference workloads.
- **Kubernetes Secrets / Vault**: Secret and credential management.

#### Phase 6 — AI Agent Integration
- **Autonomous Response Layer**: AI-driven actions such as IP blocking and Slack alerting.
- **Backend + AI + Infra Integration**: Full operational loop connecting detection, decision-making, and automated response.

#### Phase 7 — AWS Integration
- **Terraform**: Infrastructure as Code for VPC, EKS, and RDS provisioning.
- **ALB Ingress Controller / ACM / IRSA**: Secure production-grade ingress and IAM integration.
- **CloudWatch**: Native AWS logs and metrics integration.

#### Phase 8 — GCP Integration
- **Vertex AI**: Managed model registry and serving.
- **BigQuery ML**: Large-scale analytical workflows for security data.
- **GCS**: Storage for feature vectors and ML-related artifacts.

#### Phase 9 — Azure Integration
- **Azure OpenAI**: LLM-powered log summarization and explainability.
- **Microsoft Entra ID**: Enterprise identity and SSO integration.
- **Microsoft Sentinel**: SIEM integration for threat hunting and investigation.

#### Phase 10 — Global-Scale Architecture
- **Multi-Region Architecture**: Cross-region failover and high availability.
- **Chaos Engineering**: Resilience testing through controlled fault injection.
- **FinOps Tooling**: Cost optimization through spot usage and scaling controls.
- **Continuous Learning Pipelines**: Online feedback loops enabling continuous model improvement and adaptive security.

---

## ⚡ Quick Start

```bash
git clone https://github.com/millalisredyaid/ai-security-platform.git
cd ai-security-platform
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to explore the API.
For detailed local environment setup, refer to the Setup & Usage section below.

## 🧪 Setup & Usage

Detailed setup instructions for local development.

### 1. Set up the local environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables (`.env`)

```bash
cp .env.example .env
```

Then edit the values as needed.

### 3. Start the development server

```bash
python -m uvicorn app.main:app --reload
```

Note: Use --reload for local development. For production or containerized environments, configure the ASGI server according to the deployment environment while pointing to app.main:app.

You can access the API documentation in your browser:

`http://127.0.0.1:8000/docs`

### 4. Optional: Enable development logging

If using environment variables:

```bash
export LOG_LEVEL=DEBUG
export LOG_FORMAT=json
```

If using `.env`:

```bash
LOG_LEVEL=DEBUG
LOG_FORMAT=json
```

### 5. Additional setup (future phases)

Additional setup steps will be added here as the platform evolves.

## 🗺 Roadmap
I manage this project using a strict phase-based roadmap to ensure scalability and security at every step.
See ROADMAP.
- **[ROADMAP.md](./ROADMAP.md)** 
- **[ROADMAP.ja.md (Japanese Roadmap)](./ROADMAP.ja.md)** for technical details on AI implementation and infrastructure.
---
