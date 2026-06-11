# LogVerse: Native Django + MongoDB Logging API

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Django](https://img.shields.io/badge/Django-6.x-092E20.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Native-47A248.svg)
![uv](https://img.shields.io/badge/uv-Fast-purple.svg)

**LogVerse** is a modern backend portfolio project demonstrating the power of integrating NoSQL document storage with traditional relational frameworks. It acts as a dynamic API log and webhook inspector, built to capture, store, and analyze unstructured JSON payloads.

## 🚀 Key Features

- **Native MongoDB Integration:** Utilizes `django-mongodb-backend` for direct BSON document storage using standard Django models.
- **Unstructured Data Handling:** Uses Django's `JSONField` to natively store highly variable webhook and traffic log payloads.
- **Built-in Admin Dashboard:** Fully leverages Django's native admin panel to filter, search, and inspect MongoDB collections in real-time.
- **Modern Tooling:** Managed entirely via `uv` for lightning-fast dependency resolution and environment management.
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
# Use 'host.docker.internal' to connect to a Mongo instance running on the host,
# or the service name (e.g., 'db') if running Mongo in the same compose network.
MONGO_HOST=host.docker.internal
MONGO_PORT=27017
MONGO_DB_NAME=logverse_db
MONGO_USER=
MONGO_PASSWORD=

# Traffic Simulator Configurations
INGESTION_API_URL=[http://127.0.0.1:8000/api/v1/mock-log/](http://127.0.0.1:8000/api/v1/mock-log/)
```

---

## 🐳 Running via Docker Compose (Recommended)

To run the application entirely within isolated containers:

1. **Build and start the containers:**

```bash
docker compose up --build -d
```

2. **Apply MongoDB Migrations:**

```bash
docker compose exec web python manage.py migrate
```

3. **Create an Admin User:**

```bash
docker compose exec web python manage.py createsuperuser
```

The API and Admin panel will now be accessible at `http://127.0.0.1:8000/admin/`.

---

## 💻 Running Locally (Terminal & uv)

If you prefer to run the Django server directly on your host machine while pointing to a separate MongoDB instance:

1. **Install dependencies using uv:**

```bash
uv sync
```

2. **Run MongoDB Migrations:**

```bash
uv run python manage.py migrate
```

3. **Create an Admin User:**

```bash
uv run python manage.py createsuperuser
```

4. **Start the Development Server:**

```bash
uv run python manage.py runserver
```

---

## 🚦 Traffic Simulator

To demonstrate the application's ability to ingest and structure dynamic data, this project includes a traffic simulator. The simulator blasts mock network requests (complete with varied status codes, execution times, and unstructured JSON metadata) directly into your API.

With the server running (either via Docker or locally), open a new terminal window and execute:

```bash
uv run python main.py
```

_Watch the terminal as it fires mock logs. Once complete, refresh your Django Admin panel to see the data instantly indexed in MongoDB._
