# Ion Mill Predictive Maintenance System

A full-stack predictive maintenance platform built using the PHM 2022 Data Challenge dataset. The system continuously ingests industrial ion mill telemetry, performs anomaly detection and Remaining Useful Life (RUL) estimation, stores telemetry in PostgreSQL, and visualizes equipment health through a React-based fleet monitoring dashboard.

---

## Overview

Industrial ion milling equipment generates large volumes of sensor telemetry during operation. Unexpected failures can lead to costly downtime, production delays, and maintenance expenses.

This project aims to predict equipment degradation before failure by combining:

* Real industrial telemetry data
* Machine learning-based anomaly detection
* Time-to-Failure (TTF) prediction
* Fleet-level monitoring and alerting
* Containerized deployment using Docker

The system simulates multiple ion mill tools operating concurrently and provides real-time visibility into equipment health.

---

## Key Features

### Fleet Monitoring

* Monitor multiple ion mill tools simultaneously
* View overall fleet health
* Compare health across equipment
* Identify tools requiring attention

### Anomaly Detection

* Isolation Forest-based anomaly detection
* Real-time anomaly scoring
* Equipment health score generation
* Early warning indicators

### Remaining Useful Life Prediction

* Time-to-Failure prediction model
* Continuous estimation of remaining equipment life
* Predictive maintenance support

### Telemetry Ingestion

* Concurrent multi-tool simulation
* Streaming sensor telemetry into the platform
* Historical telemetry storage

### Containerized Deployment

* Dockerized frontend
* Dockerized backend
* Dockerized PostgreSQL database
* One-command deployment with Docker Compose

---

## System Architecture
## Data Flow

```text
PHM Dataset
     │
     ▼
Multi-Tool Simulator
     │
     ▼
Django REST API
     │
     ├── Stores telemetry in PostgreSQL
     ├── Runs Isolation Forest anomaly detection
     └── Generates TTF predictions
     | 
     ▼
React Fleet Dashboard
     │
     ▼
Operators and Maintenance Engineers
```


---

## Technology Stack

### Frontend

* React
* Vite
* Axios
* Recharts

### Backend

* Django
* Django REST Framework

### Database

* PostgreSQL

### Machine Learning

* Scikit-learn
* Isolation Forest
* Random Forest Regressor
* Pandas
* NumPy

### Deployment

* Docker
* Docker Compose

---

## Dataset

This project is built using the PHM 2022 Data Challenge dataset containing telemetry collected from industrial ion milling equipment.

Example sensor streams include:

* Ion Gauge Pressure
* Flowcool Pressure
* Flowcool Flowrate
* Etch Beam Voltage
* Etch Beam Current
* Rotation Speed
* Source Usage
* Process Duration

The dataset also provides:

* Failure information
* Time-to-Failure labels
* Tool identifiers
* Process metadata

---

## Machine Learning Pipeline

### Anomaly Detection

Sensor telemetry is processed using an Isolation Forest model.

Pipeline:

1. Receive sensor readings
2. Generate anomaly score
3. Detect abnormal operating conditions
4. Convert anomaly score into equipment health score

Outputs:

* Anomaly Score
* Health Score
* Anomaly Flag

### Remaining Useful Life Prediction

A Random Forest Regressor is trained on PHM telemetry and Time-to-Failure labels.

Outputs:

* Predicted Time-to-Failure
* Remaining Useful Life estimation

---

## Project Structure

```text
ion-mill-predictive/
│
├── backend/
│   ├── api/
│   ├── config/
│   ├── ml/
│   └── manage.py
│
├── frontend/
│
├── data/
│   ├── raw/
│   └── simulator/
│
├── scripts/
│
├── docs/
│
├── docker-compose.yml
│
└── README.md
```

## API Endpoints

### Equipment List

```http
GET /api/equipment/
```

### Equipment Health

```http
GET /api/equipment/{id}/health/
```

### Recent Readings

```http
GET /api/equipment/{id}/readings/
```

### Fleet Health

```http
GET /api/fleet-health/
```

### Alerts

```http
GET /api/alerts/
```

### Sensor Data Ingestion

```http
POST /api/sensor-readings/
```

---

## Running with Docker

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

### Stop

```bash
docker compose down
```

---

## Current Capabilities

* Multi-tool monitoring
* Concurrent telemetry simulation
* Fleet health tracking
* Anomaly detection
* Health scoring
* Time-to-Failure prediction
* PostgreSQL persistence
* Docker deployment

---

## Future Improvements

* Additional sensor feature engineering
* Multi-failure prediction models
* Advanced Remaining Useful Life estimation
* Fleet-level analytics
* Real-time streaming architecture
* Role-based access control
* Cloud deployment
* Enhanced dashboard visualizations

---

## Author

Aryan Sheikh

MIT Manipal

Artificial Intelligence & Machine Learning



