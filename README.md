# DrugAI Intelligence Platform

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/Ishwarij032005/DrugAI-Intelligence-Platform)
![GitHub stars](https://img.shields.io/github/stars/Ishwarij032005/DrugAI-Intelligence-Platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ishwarij032005/DrugAI-Intelligence-Platform?style=social)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB)
![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-009688)
![ML](https://img.shields.io/badge/ML-PyTorch%20%2F%20RDKit%20%2F%20XGBoost-FF6F00)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Infra](https://img.shields.io/badge/Infra-Docker%20%2B%20Redis%20%2B%20Celery-2496ED)

</div>

<div align="center">

**An enterprise-grade AI drug discovery platform for toxicity prediction, drug–target interaction, ADMET analysis, side effect prediction, molecular similarity search, explainable AI, batch screening, and ML experiment tracking.**

</div>

---

## 📌 Overview

DrugAI Intelligence Platform is a full-stack, production-style AI SaaS built for computational drug discovery and molecular intelligence. It combines a modern React frontend with a scalable FastAPI backend, PostgreSQL database, Celery workers, Redis caching, and MLflow-powered model tracking.

The platform is designed to help researchers and teams:

- predict molecular toxicity
- estimate drug–target interactions
- analyze ADMET properties
- identify possible side effects
- search for similar compounds
- generate recommendations
- inspect model explanations
- compare experiments and model runs
- run batch screening jobs
- track predictions and reports

---

## ✨ Key Features

### AI & ML
- Drug Toxicity Prediction
- Drug–Target Interaction Prediction
- ADMET Prediction
- Side Effect Prediction
- Drug Similarity Search
- Drug Recommendation Engine
- Explainable AI with SHAP and LIME
- Model Comparison Dashboard
- Batch Prediction Workflow
- Experiment Tracking with MLflow

### Product & Platform
- Premium SaaS-style dashboard
- Auth system with JWT and RBAC
- Responsive dark-first UI
- Animated charts and analytics
- Real-time status updates
- Prediction history and reports
- Admin dashboard
- WebSocket-based live progress tracking
- Dockerized deployment
- CI/CD-ready project structure

---

## 🧬 Scientific Capabilities

This platform includes molecular intelligence workflows such as:

- SMILES validation
- Morgan fingerprints
- MACCS keys
- RDKit-based molecular property extraction
- Molecular similarity scoring using Tanimoto coefficient
- Batch molecule screening
- Model confidence and explanation views
- Structured ML training and inference pipelines

---

## 🏗️ System Architecture

```text
React Frontend
      ↓
FastAPI Backend
      ↓
PostgreSQL + Redis
      ↓
Celery Workers
      ↓
MLflow / Model Registry
      ↓
RDKit + ML Models


🛠️ Tech Stack
Frontend
React 18+
TypeScript
Vite
Tailwind CSS
Shadcn UI
Framer Motion
TanStack Query
React Hook Form
Zod
Lucide React
Backend
Python 3.12+
FastAPI
Pydantic v2
SQLAlchemy 2.0
Alembic
JWT Authentication
WebSockets
Celery
Redis
MLflow
Uvicorn
AI / ML
RDKit
Scikit-learn
XGBoost
PyTorch
Optuna
SHAP
LIME
NumPy
Pandas
Database / DevOps
PostgreSQL
Docker
Docker Compose
Nginx
GitHub Actions
📂 Project Structure
DrugAI-Intelligence-Platform/
├── backend/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── ml/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── middleware/
│   ├── tasks/
│   ├── tests/
│   └── migrations/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── layouts/
├── nginx/
├── docker-compose.yml
└── README.md
🚀 Getting Started
Prerequisites
Node.js 20+
Python 3.12+
PostgreSQL
Redis
Docker and Docker Compose
1) Clone the repository
git clone https://github.com/Ishwarij032005/DrugAI-Intelligence-Platform.git
cd DrugAI-Intelligence-Platform
2) Run with Docker
docker compose up --build

This starts the backend, frontend, Redis, PostgreSQL, Celery workers, and supporting services.

3) Run backend locally
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
4) Run frontend locally
cd frontend
npm install
npm run dev
🔐 Environment Variables
Backend

Create backend/.env:

DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/drugai
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

REDIS_URL=redis://localhost:6379/0
MLFLOW_TRACKING_URI=http://localhost:5000
CORS_ORIGINS=http://localhost:5173

EMAIL_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_app_password
Frontend

Create frontend/.env:

VITE_API_BASE_URL=http://localhost:8000/api/v1
📡 API Highlights
Authentication
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
Predictions
POST /api/v1/predict/toxicity
POST /api/v1/predict/dti
POST /api/v1/predict/admet
POST /api/v1/predict/side-effects
Molecular Intelligence
POST /api/v1/molecules/similarity
POST /api/v1/molecules/recommendations
POST /api/v1/molecules/explain
Batch & Analytics
POST /api/v1/batch/predict
GET /api/v1/analytics/overview
GET /api/v1/analytics/model-comparison
GET /api/v1/predictions/history
Model & Operations
GET /api/v1/models
GET /api/v1/mlflow/runs
GET /api/v1/reports
GET /api/v1/ws/progress
🧪 Models Used
XGBoost for toxicity and side effects
Random Forest for ADMET
Similarity search using Tanimoto coefficient
Explanation layer with SHAP / LIME
Real-time progress tracking for heavy jobs
MLflow for experiment logging and comparison
📸 Screenshots

Replace these with your actual screenshots from the app.

Landing Page

Dashboard

Toxicity Prediction

Drug–Target Interaction

Analytics

📊 What Makes This Project Special

Most student AI projects stop at a single model.

This project goes much further by combining:

a premium frontend experience
a production-grade backend
real ML deployment patterns
experiment tracking
asynchronous jobs
molecular feature engineering
explainable AI
analytics and reporting
concurrency-safe design
scalable architecture

That makes it suitable for:

hackathons
internships
research demonstrations
AI portfolio showcases
final-year capstone projects
🔮 Future Improvements
Graph Neural Networks for molecular graphs
DeepChem integration
ChemBERTa / MolBERT embeddings
Better protein encoders for DTI
Model uncertainty estimation
Active learning loop
External chemical database integrations
Public demo deployment
Multi-tenant organization support
🧪 Testing

Run backend tests:

cd backend
pytest

Run frontend checks:

cd frontend
npm run lint
npm run build
📜 License

This project is licensed under the MIT License.

👩‍💻 Author

Ishwari Jamadade
