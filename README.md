# Project Documentation

## Project Overview

This project is designed to scrape data from various websites. Each parser is implemented as a separate class responsible for handling a specific website. Data scraping is performed using asynchronous requests and frameworks like **Playwright** and **httpx**.

The project is containerized using **Docker** to ensure easy deployment and execution across different environments.

---

## Requirements

- **Docker**
- **Docker Compose**
- **Python 3.10+**

---

## Getting Started

### 1. Clone the Repository

Start by cloning the project repository to your local machine:

```bash
 git clone https://bitbucket.org/likebus/likebus-dynamic-pricing-system/src/main/
 cd likebus-dynamic-pricing-system
```

### 3. Configure Environment Variables

Before running the project, make sure to configure your environment variables. 

Create a .env file in the root directory of the project and define the necessary variables. For example:

```aiignore
# Production Database
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=

# Test Database
TEST_POSTGRES_USER=
TEST_POSTGRES_PASSWORD=
TEST_POSTGRES_DB=
TEST_POSTGRES_HOST=
TEST_POSTGRES_PORT=

# PGadmin
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
```

### Start the Docker Containers

```
docker-compose up --build
```

## Project Documentation: Running Without Docker (with Playwright)

## 1. Prerequisites

Before running the project, ensure you have the following software installed:

- **Python 3.10+**: Make sure Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
- **Playwright**: We use Playwright for browser automation. Follow these steps to install it.
  - Install the Playwright package:
    ```bash
    pip install playwright
    ```
  - Install the necessary browsers:
    ```bash
    playwright install
    ```

- **PostgreSQL (or other database)**: If you're using a local PostgreSQL database, ensure it's installed and running. You can follow the [installation guide](https://www.postgresql.org/download/) for your operating system.


## 2. Install Dependencies
Create a virtual environment and install the required dependencies:

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

