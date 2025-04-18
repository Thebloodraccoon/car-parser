# Car Parser

Car Parser is a web scraper project with a RESTfull API backend built using **FastAPI** and **MongoDB**.
It is designed to scrape car listings and serve them via an API. 
The project is containerized using **Docker** and **Docker Compose**.

---
## 🚀 Requirements

- Docker & Docker Compose
- Python 3.11+ 
- MongoDB
- Optional: Mongo Express for easy DB visualization

---

## ⚙️ Environment Configuration

Create your `.env` file using the provided `.env.example` as a template:

```aiignore
# MongoDB settings
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB=car_listings
MONGODB_COLLECTION=cars

# Mongo Express settings
ME_CONFIG_MONGODB_SERVER=mongodb
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=your_password_here

# Proxy settings
PROXY=your_proxy_here
```

---

## 🐳 Running with Docker

### Build and run containers

```bash
 python -m venv venv
 source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
 pip install -r requirements.txt
```


## 3. Run the Database Migrations

```bash
 alembic upgrade head
```

## 4. Running the Application

```bash
 python main.py
```

