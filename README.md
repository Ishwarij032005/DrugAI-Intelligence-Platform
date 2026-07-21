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
