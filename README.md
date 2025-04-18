# Car Parser

Car Parser is a web scraper project with a RESTful API backend built using **FastAPI** and **MongoDB**. It is designed to scrape car listings and serve them via an API. The project is containerized using **Docker** and **Docker Compose**.

---

## 🚀 Requirements

- Docker & Docker Compose
- Python 3.11+ (for development outside containers)
- MongoDB
- Redis (used for caching or task queue if integrated)
- Optional: Mongo Express for easy DB visualization

---

## ⚙️ Environment Configuration

Create your `.env` file using the provided `.env.example` as a template:

```env
# MongoDB settings
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB=car_listings
MONGODB_COLLECTION=cars

# Redis settings
HOST_REDIS=redis
PORT_REDIS=6379
DB_REDIS=0

# Mongo Express settings
ME_CONFIG_MONGODB_SERVER=mongodb
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=your_password_here

# Proxy server settings
PROXY=your_proxy_server_here
```

---

## 🐳 Running with Docker

### Build and run containers

```bash
docker-compose up --build
```

The FastAPI backend will be accessible at: [http://localhost:8000](http://localhost:8000)

Mongo Express (if configured) will be available at: [http://localhost:8081](http://localhost:8081)

### Run the scraper

To start the scraper manually:

```bash
docker exec -it car_parser bash
python app/scraper/main.py
```

---

## 📘 API Reference

### 🔹 Cars

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/cars/`                  | Get all cars (with pagination)       |
| GET    | `/cars/{car_id}`          | Get a specific car by ID             |
| GET    | `/cars/make/{make}`       | Get cars filtered by make            |
| GET    | `/cars/year/{year}`       | Get cars filtered by production year |
| POST   | `/cars/`                  | Create a new car                     |
| PUT    | `/cars/{car_id}`          | Update car details by ID             |
| DELETE | `/cars/{car_id}`          | Delete a car by ID                   |

### 🔹 Users

| Method | Endpoint                  | Description                |
|--------|---------------------------|----------------------------|
| POST   | `/users/`                 | Create a new user          |
| GET    | `/users/`                 | Get all users              |
| GET    | `/users/{user_id}`        | Get a user by ID           |
| PUT    | `/users/{user_id}`        | Update user info by ID     |
| DELETE | `/users/{user_id}`        | Delete a user by ID        |

---
