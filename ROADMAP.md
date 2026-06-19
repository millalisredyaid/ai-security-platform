
---

###  `ROADMAP.md` (Detailed - English)

# 🧭 Technical Evolution Roadmap

This roadmap tracks the evolution of this project toward a **production-grade, autonomous AI security agent** that integrates **AI x Backend x Infrastructure x Security**.

Each phase is architected with a strict focus on **Scalability, Security, and Observability**, designed with a real-world production environment in mind.

---

## 📶 Phase-based Status

| Phase | Milestone | Status | Key Engineering Focus |
| :--- | :--- | :--- | :--- |
| **Phase 0** | **RESTful Foundations** | ✅ **Done** | FastAPI, Pydantic, Structured Logging |
| **Phase 1** | **AI Anomaly Detection & Rule-based Detection** | 🚧 **Active** | Feature Engineering, SQLi/Traversal Detection, Traceability, Inference Latency |
| **Phase 2** | **Secure Auth & Database** | 📅 **Planned** | JWT, PostgreSQL, RBAC, OWASP |
| **Phase 3** | **Container Security** | 📅 **Planned** | **Trivy**, SBOM, Minimal Base Images |
| **Phase 4** | **SRE & Model Observability** | 📅 **Planned** | **Model Drift**, Error Rates, Prometheus |
| **Phase 5** | **K8s & Cloud Native** | 📅 **Planned** | Kubernetes, Network Policies, HPA |
| **Phase 6** | **AI Security Agent** | 📅 **Planned** | **Autonomous Incident Response** |
| **Phase 7** | **AWS & IaC** | 📅 **Planned** | **Terraform**, EKS, IRSA, CloudWatch |
| **Phase 8** | **GCP & MLOps** | 📅 **Planned** | Vertex AI, BigQuery ML, Model Registry |
| **Phase 9** | **Azure & Enterprise AI** | 📅 **Planned** | **Azure OpenAI (LLM)**, Entra ID, Sentinel |
| **Phase 10**| **Global-Scale Platform** | 📅 **Planned** | Multi-Region, Chaos Engineering, FinOps |

---

## 📋 Milestone Details

### ✅ Phase 0: Foundations (Completed)
- [x] High-performance asynchronous API with FastAPI.
- [x] Data integrity via Pydantic v2 schemas.
- [x] Structured logging for future AI ingestion.
- [x] Automated API documentation.

### 🚧 Phase 1: AI Anomaly Detection & Rule-based Detection (Current)
**Goal:** Build a hybrid detection foundation that combines machine learning-based anomaly detection with rule-based detection for known attack patterns.
- [x] Endpoint: `POST /analyze` for real-time scoring.
- [x] Feature engineering for log vectors, including IP frequency and request path signals.
- [x] Rule-based security detection engine.
- [x] Regex-based SQL Injection detection.
- [x] Regex-based Directory Traversal detection.
- [x] Structured rule evaluation with `RuleEvaluationResult`.
- [x] Traceable detection reasons with `RuleMatchInfo`.
- [ ] Training an **Anomaly Detection Model**.
- [ ] Optimization for **low-latency inference**.
- [ ] End-to-end traceability with Decision Context / Request ID.
- [ ] Safe evaluation of detection results using Shadow Mode.

### 📅 Phase 2: Security & Persistence
**Goal:** Hardening the API and data storage.
- [ ] Secure password hashing (Passlib) and JWT.
- [ ] Persistent storage with PostgreSQL & Alembic (Migrations).
- [ ] Implementing **RBAC** (Role-Based Access Control).

### 📅 Phase 3: Container Security
**Goal:** Secure the containerized environment and ensure supply-chain integrity.
- [ ] **Image Scanning (Trivy)**: Scan for CVEs, misconfigurations, and secrets.
- [ ] **Minimal Base Images**: Use `python:3.12-slim` to reduce attack surface.
- [ ] **Non-root Containers**: Enforce non-root user execution to prevent escalation.
- [ ] **Dependency Integrity**: Validate dependencies with `pip-audit` or `safety`.
- [ ] **SBOM Generation**: Generate Software Bill of Materials for transparency.
- [ ] **Secure Build Pipeline**: Harden GitHub Actions to prevent supply-chain attacks.

### 📅 Phase 4: SRE & Observability (Critical for AI)
**Goal:** Monitoring "AI in Production."
- [ ] Tracking **Model Drift**: Detection of accuracy degradation over time.
- [ ] Monitoring **Inference Time** & **API Error Rates**.
- [ ] Automated alerting for high-risk anomalies via Prometheus/Grafana.

### 📅 Phase 5: Kubernetes & Cloud Native
**Goal:** Deploy a production-ready, secure, scalable AI security backend.
- [ ] **K8s Deployment**: Start with local **kind** cluster, migrate to EKS/GKE.
- [ ] **Network Policies**: Restrict pod-to-pod communication (Least-privilege).
- [ ] **Pod Security Standards (PSS)**: Enforce *restricted* profiles  
  - No privileged containers  
  - No hostPath mounts  
  - Read-only root filesystem  
  - Non-root user execution  
- [ ] **Horizontal Pod Autoscaling (HPA)**: Scale inference API based on CPU/latency.
- [ ] **Secret Management**: Use K8s Secrets or external secret stores (Vault).
- [ ] **Ingress + TLS**: Secure external traffic with HTTPS termination.

### 📅 Phase 6: AI Agent Integration
**Goal:** Closing the loop between detection and action.
- [ ] Implementing **Autonomous Response**: AI-driven IP blocking or Slack alerts.
- [ ] Final integration of AI, Backend, and Infrastructure.

---

## 🌐 Scaling to Cloud & Enterprise

### 📅 Phase 7: AWS Integration (Production IaC)
**Goal:** Build a hardened production environment using Infrastructure as Code.
- [ ] **Terraform**: Provisioning VPC, EKS, and RDS via IaC.
- [ ] **Security**: ALB Ingress Controller + ACM (HTTPS) and IRSA (IAM Roles for Service Accounts).
- [ ] **Monitoring**: Integration with CloudWatch Logs & Metrics.

### 📅 Phase 8: GCP Integration (Advanced AI & MLOps)
**Goal:** Automate ML lifecycles using Google Cloud's AI suite.
- [ ] **Vertex AI**: Implementing Model Registry and Serving.
- [ ] **BigQuery ML**: Analyzing massive log data for pattern recognition.
- [ ] **Data Pipeline**: Storing feature vectors in GCS for high-speed retrieval.

### 📅 Phase 9: Azure Integration (Enterprise AI & LLM)
**Goal:** Integrate LLMs and enterprise-grade security tools.
- [ ] **Azure OpenAI**: Use GPT-4 for natural language log summarization and explainability.
- [ ] **Identity**: Integration with Microsoft Entra ID (Azure AD) for SSO.
- [ ] **Security SIEM**: Connecting logs to Microsoft Sentinel for threat hunting.

### 📅 Phase 10: Global-Scale Security Platform (Final Form)
**Goal:** Complete a self-healing, globally distributed AI security system.
- [ ] **Multi-Region**: High availability via cross-region failover and Global Accelerator.
- [ ] **Chaos Engineering**: Testing resilience by injecting faults into the K8s cluster.
- [ ] **FinOps**: Optimizing costs using Spot Instances and automated scaling.
- [ ] **Continuous Learning**: Online model training based on real-time feedback loops.

---

## 🧩 Summary

This roadmap outlines a unified growth trajectory:

**Local development → AI anomaly detection → Secure APIs → Docker → Kubernetes →  
Cloud production (AWS) → MLOps (GCP) → Enterprise AI & LLM (Azure) → Global-scale architecture**

Phases 0–6 represent the “learning and foundation-building” stages,  
while Phases 7–10 form the “cloud expansion and enterprise integration” stages.

Together, they lead to the final goal:  
a **fully autonomous, cloud-native AI Security Platform**.

## 📘 Related Documents
- [README.md (English)](./README.md)
- [README.ja.md (Japanese)](./README.ja.md)
- [ROADMAP.ja.md (Japanese Roadmap)](./ROADMAP.ja.md)
