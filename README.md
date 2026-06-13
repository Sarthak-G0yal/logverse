# LogVerse: Native Django + MongoDB Logging API

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Django](https://img.shields.io/badge/Django-6.x-092E20.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Native-47A248.svg)
![Traefik](https://img.shields.io/badge/Traefik-v3-blue.svg)
![Vector](https://img.shields.io/badge/Vector-Log_Shipper-black.svg)
![uv](https://img.shields.io/badge/uv-Fast-purple.svg)

**LogVerse** is a modern backend portfolio project demonstrating the power of integrating NoSQL document storage with traditional relational frameworks. It acts as a dynamic API log and webhook inspector, built to capture, store, and analyze unstructured JSON payloads.

## 🚀 Key Features

- **Native MongoDB Integration:** Utilizes `django-mongodb-backend` for direct BSON document storage using standard Django models.
- **Automated Log Pipeline:** Features a fully containerized network sandbox using **Traefik** as a reverse proxy and **Vector** to dynamically transform and ship access logs.
- **API Token Security:** Secures ingestion endpoints with Bearer token authentication to prevent unauthorized network spam.
- **Unstructured Data Handling:** Uses Django's `JSONField` to natively store highly variable webhook and traffic log payloads.
- **Built-in Admin Dashboard:** Fully leverages Django's native admin panel to filter, search, and inspect MongoDB collections in real-time.
- **Containerized Infrastructure:** Fully orchestrated via Docker Compose for identical local and production environments.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Python 3.13+](https://www.python.org/downloads/) (if running locally without Docker)
- [uv](https://github.com/astral-sh/uv) (Astral's fast Python package manager)

---

## ⚙️ Configuration (.env)

Create a `.env` file at the root of the project. This file securely configures both your Django application and the Docker Compose network.

```env
# Django Configurations
# To generate a random key: openssl rand -base64 32
DJANGO_SECRET_KEY=CUn9u24oIK82iW9OZ0HtjtFEk33XAsCMzwIgajVhHWU=
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web
DJANGO_DEBUG=True

# MongoDB Configurations
# Set to 'mongo' to use the internal Docker compose database network
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB_NAME=logverse_db
MONGO_USER=
MONGO_PASSWORD=

# Security & Traffic Configurations
API_INGESTION_TOKEN=sandbox-token-secret-123
INGESTION_API_URL=[http://127.0.0.1:8000/api/v1/mock-log/](http://127.0.0.1:8000/api/v1/mock-log/)
```

---

## 🐳 Running the All-In-One Sandbox (Docker Compose)

The Docker Compose stack spins up the entire infrastructure: Django, MongoDB, Traefik, Vector, and a dummy target app to simulate a production network.

1. **Build and start the containers:**

```bash
docker compose up --build -d
```

2. **Apply MongoDB Migrations:**

```bash
docker compose exec web uv run python manage.py migrate
```

3. **Create an Admin User:**

```bash
docker compose exec web uv run python manage.py createsuperuser
```

**Dashboard Access:**

- The LogVerse Admin panel will now be accessible at: `http://127.0.0.1:8000/admin/`
- The Traefik routing dashboard can be accessed at: `http://127.0.0.1:8080/dashboard/`

---

## 🚦 Testing the Pipeline

To demonstrate the application's ability to ingest and structure dynamic data, you can trigger real-world proxy traffic through Traefik.

**Option A: Live Network Routing (Traefik -> Vector -> Django -> Mongo)**
Trigger a request through the Traefik reverse proxy to the dummy application:

```bash
curl http://dummy.localhost/
```

_Vector will instantly intercept the Traefik access log, format it, and POST it securely to LogVerse._

**Option B: Python Traffic Simulator**
To blast the API with 50+ mock network requests (varied status codes, execution times, etc.), run the simulator script:

```bash
uv run python main.py
```

_Refresh your Django Admin panel to see the data instantly indexed in MongoDB._

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

