# 🧬 DrugAI Intelligence Platform

<div align="center">

### 🚀 Enterprise-Grade AI Platform for Drug Discovery & Molecular Intelligence

**Predict • Analyze • Explain • Discover**

<p>

![Repo Size](https://img.shields.io/github/repo-size/Ishwarij032005/DrugAI-Intelligence-Platform?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/Ishwarij032005/DrugAI-Intelligence-Platform?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/Ishwarij032005/DrugAI-Intelligence-Platform?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

<p>

![React](https://img.shields.io/badge/React-TypeScript-61DAFB?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-RDKit-XGBoost-orange?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Redis-Celery-2496ED?style=flat-square)

</p>

</div>

---

# 📖 Overview

**DrugAI Intelligence Platform** is a modern full-stack AI platform designed for computational drug discovery and molecular intelligence.

It combines a **React + TypeScript frontend**, a **FastAPI backend**, **PostgreSQL**, **Redis**, **Celery**, **MLflow**, and advanced machine learning models to provide an end-to-end workflow for molecular analysis, toxicity prediction, drug–target interaction, ADMET prediction, similarity search, explainable AI, and experiment tracking.

---

# 🎯 What Can DrugAI Do?

✔ Predict molecular toxicity

✔ Analyze Drug–Target Interactions (DTI)

✔ Estimate ADMET properties

✔ Predict possible side effects

✔ Search chemically similar molecules

✔ Generate intelligent drug recommendations

✔ Explain AI predictions using SHAP & LIME

✔ Compare model experiments with MLflow

✔ Run batch molecule screening

✔ Track predictions, reports, and analytics

---

# ✨ Features

## 🤖 AI & Machine Learning

- 🧪 Drug Toxicity Prediction
- 🧬 Drug–Target Interaction Prediction
- 💊 ADMET Prediction
- ⚠ Side Effect Prediction
- 🔍 Drug Similarity Search
- 💡 Drug Recommendation Engine
- 📊 Explainable AI (SHAP & LIME)
- 📈 MLflow Experiment Tracking
- ⚡ Batch Prediction Workflow
- 📉 Model Comparison Dashboard

---

## 💻 Platform Features

- 🔐 JWT Authentication & RBAC
- 🌙 Premium Dark Dashboard
- 📱 Responsive UI
- 📊 Interactive Analytics
- 🔄 WebSocket Live Updates
- 📜 Prediction History
- 📄 Report Generation
- 👨‍💼 Admin Dashboard
- 🐳 Docker Deployment
- 🚀 CI/CD Ready Architecture

---

# 🧬 Scientific Capabilities

DrugAI includes a complete molecular intelligence pipeline.

- ✅ SMILES Validation
- ✅ Morgan Fingerprints
- ✅ MACCS Keys
- ✅ RDKit Molecular Descriptors
- ✅ Tanimoto Similarity Search
- ✅ Batch Molecule Screening
- ✅ Confidence Estimation
- ✅ Explainable AI
- ✅ ML Training & Inference Pipelines

---

# 🏗 System Architecture

```text
                 React + TypeScript
                         │
                         ▼
                  FastAPI Backend
                         │
        ┌────────────────┴───────────────┐
        ▼                                ▼
 PostgreSQL Database                 Redis Cache
        │                                │
        └──────────────┬─────────────────┘
                       ▼
                 Celery Workers
                       │
                       ▼
            MLflow Model Registry
                       │
                       ▼
          RDKit + Machine Learning Models
```

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, Shadcn UI, Framer Motion |
| **Backend** | FastAPI, Python, SQLAlchemy, Alembic, JWT, WebSockets |
| **AI / ML** | RDKit, PyTorch, XGBoost, Scikit-learn, SHAP, LIME, Optuna |
| **Database** | PostgreSQL |
| **Background Jobs** | Celery, Redis |
| **MLOps** | MLflow |
| **DevOps** | Docker, Docker Compose, GitHub Actions |

---

# 📂 Project Structure

```text
DrugAI-Intelligence-Platform/
│
├── backend/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── ml/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── middleware/
│   ├── tasks/
│   ├── schemas/
│   ├── tests/
│   └── migrations/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── pages/
│
├── nginx/
├── docker-compose.yml
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Node.js 20+
- Python 3.12+
- PostgreSQL
- Redis
- Docker & Docker Compose

---

## Clone Repository

```bash
git clone https://github.com/Ishwarij032005/DrugAI-Intelligence-Platform.git

cd DrugAI-Intelligence-Platform
```

---

## Run Using Docker

```bash
docker compose up --build
```

This starts:

- Frontend
- Backend
- PostgreSQL
- Redis
- Celery
- MLflow

---

## Run Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Run Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔐 Environment Variables

## Backend

```env
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
REDIS_URL=
MLFLOW_TRACKING_URI=
SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=
```

---

## Frontend

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

# 📡 API Highlights

## Authentication

- Register
- Login
- Logout
- Refresh Token

---

## AI Predictions

- Toxicity Prediction
- Drug–Target Interaction
- ADMET Prediction
- Side Effect Prediction

---

## Molecular Intelligence

- Similarity Search
- Drug Recommendation
- Explainable AI

---

## Analytics

- Batch Prediction
- Prediction History
- Model Comparison
- Reports
- MLflow Runs

---

# 🧪 Machine Learning Models

| Module | Model |
|----------|-------|
| Toxicity Prediction | XGBoost |
| Side Effect Prediction | XGBoost |
| ADMET Prediction | Random Forest |
| Similarity Search | RDKit + Tanimoto |
| Explainable AI | SHAP + LIME |
| Experiment Tracking | MLflow |

---

# 📸 Screenshots

> Replace these placeholders with actual screenshots.

🖼 Landing Page

🖼 Dashboard

🖼 Toxicity Prediction

🖼 Drug–Target Interaction

🖼 Analytics

---

# 🌟 Why This Project?

Unlike many student AI projects that demonstrate a single predictive model, DrugAI combines:

- Modern SaaS-style frontend
- Production-oriented backend
- AI model deployment
- MLOps with MLflow
- Asynchronous processing
- Explainable AI
- Molecular feature engineering
- Analytics and reporting
- Scalable system architecture

This makes it suitable for:

- 🏆 Hackathons
- 💼 Internship portfolios
- 🔬 Research demonstrations
- 🎓 Final-year capstone projects
- 🤝 Open-source contributions

---

# 🚀 Future Roadmap

- Graph Neural Networks (GNNs)
- DeepChem Integration
- ChemBERTa / MolBERT
- Advanced Protein Encoders
- Uncertainty Estimation
- Active Learning Pipeline
- External Chemical Database Integration
- Public Cloud Deployment
- Multi-tenant Workspace Support

---

# 🧪 Testing

Backend

```bash
pytest
```

Frontend

```bash
npm run lint

npm run build
```

---

# 📜 License

Licensed under the **MIT License**.

---

# 👩‍💻 Author

**Ishwari Jamadade**

🔗 GitHub: https://github.com/Ishwarij032005

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

**Happy Coding 🚀**

</div>
