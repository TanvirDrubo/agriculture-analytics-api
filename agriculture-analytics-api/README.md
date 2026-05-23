#  Agriculture Analytics API

This project is a FastAPI + Pandas + MySQL based analytics system for agricultural data.

---

## Features

### Crops API (3 endpoints)
- Yield Efficiency
- Seasonal Trend
- Quality Breakdown

### Farms API (4 endpoints)
- Farm Summary
- Single Farm Performance
- Top Farms
- Loss Analysis

### Markets API (1 endpoint)
- Market Price Comparison

---

##  Setup Instructions

### 1. Clone Repo

git clone https://github.com/your-username/agri-api.git
cd agri-api


### 2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate # Windows


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Setup Environment Variables (env)

HOST=localhost
PORT=3306
USER=root
PASSWORD=your_password
DB=your_database


### 5. Run Server

uvicorn app.main:app --reload


---

##  API Docs

http://127.0.0.1:8000/docs


---

##  Docker (Bonus)


docker build -t agri-api .
docker run -p 8000:8000 agri-api


# project structure



```bash
agriculture-analytics-api/
│── app/
│   ├── api/
│   │   ├── crops.py
│   │   ├── farms.py
│   │   ├── markets.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── db.py
│   │
│   ├── data/
│   │   ├── data_loader.py
│   │
│   ├── repositories/
│   │   ├── crops_repo.py
│   │   ├── farms_repo.py
│   │
│   ├── services/
│   │   ├── crops_service.py
│   │   ├── farms_service.py
│   │   ├── markets_service.py
│   │
│   ├── utils/
│   │   ├── filters.py
│   │   ├── validators/
│   │       ├── crops_validator.py
│   │       ├── farms_validator.py
│   │       ├── common_validator.py
│
│── main.py
│── requirements.txt
│── README.md
│── README_Docker.md
│── Dockerfile
│── .gitignore
│── .dockerignore
│── env.sample
```