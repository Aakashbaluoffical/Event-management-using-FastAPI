Event Management System
======================

An Event Management System built using FastAPI, SQLAlchemy, PostgreSQL, Redis, JWT, and Docker.

🚀 Features
==============
🏷️ User Features

* User can register and login.
* View all available events.
* Select an event and register.
* View all registrations with user ID validation.
* Cancel a registered event.

🎟️ Event Hosting Features
==========================

* Create, Edit, and Cancel events.
* Manage event Check-in/Check-out (as an event in-charge, manage check-in/check-out for registered users).
* Insert bulk data through .csv uploads.

🔑 Role-Based Access
=====================

* User: Can view events and register for events.
* Superuser: Can create, edit, cancel events.

⚡ Caching with Redis
====================

Reduces database calls and improves performance.

✅ Validation & Security
========================
Uses Pydantic for API request validation.
Implements JWT-based authentication for secure access.

📂 Database Schema
=====================

The project uses three tables:

* user_tbl - Stores user information.
* event_tbl - Stores event details.
* attendee_tbl - Manages event registrations.

📌 Sample Data
==================
# User Table (`user_tbl`)

| ID  | First Name | Last Name | Phone       | Email            | Role      | Password  | Active |
|-----|-----------|-----------|------------|------------------|-----------|-----------|--------|
| 1   | John      | Doe       | 1234567890 | john@example.com | user      | secret123 | True   |
| 2   | Alice     | Smith     | 9876543210 | alice@example.com | superuser | pass456   | True   |

# Event Table (`event_tbl`)

| ID  | Name         | Description          | Start Time          | End Time            | Location  | Max Attendees | Status   |
|-----|-------------|----------------------|---------------------|---------------------|-----------|---------------|----------|
| 1   | Tech Meetup | Networking event     | 2025-02-20 10:00:00 | 2025-02-20 12:00:00 | New York  | 100           | Scheduled   |
| 2   | AI Workshop | AI & ML Discussions  | 2025-03-01 14:00:00 | 2025-03-01 16:00:00 | Online    | 50            | Ongoing |

# Attendee Table (`attendee_tbl`)

| ID  | Event ID | User ID | Check-in Status | Active | Created By ID |
|-----|---------|---------|-----------------|--------|---------------|
| 1   | 1       | 1       | True            | True   | 1             |
| 2   | 2       | 1       | False           | True   | 2             |



## 🚀 Tech Stack
- **FastAPI** (Backend Framework)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM for database interactions)
- **Redis** (Caching layer to reduce database calls)
- **Docker** (Containerization)
- **JWT** (Authentication & Authorization)
- **Pydantic** (Data validation)

---

## 🛠️ API Endpoints

Detailed API documentation using Swagger UI

    http://127.0.0.1:5200/docs

## 🧪 Testing Phases
- **Phase 1**: Manual testing.
- **Phase 2**: Automated testing using `pytest`.

---

## 🐳 Running the Project with Docker
### 1️⃣ Clone the repository:
```sh
git clone https://github.com/your-repo/event-management.git
cd event-management
```

### 2️⃣ Configure Environment Variables:
Create a `.env` file and add the following values:
```ini
POSTGRES_USERNAME=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_SCHEMA=your_database_name

CACHE_ALL_EVENTS=CACHE_ALL_EVENTS
CACHE_ALL_REGISTRATED_EVENTS=CACHE_ALL_REGISTRATED_EVENTS

CLIENT=TEST_CLIENT
CACHE_EXPIRY_IN_SECONDS=1800

REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_DB=0
REDIS_SOCKET_TIMEOUT=5
REDIS_PASSWORD=your_redis_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
(Fill in required values in `.env` file.)

### 3️⃣ Build and Run using Docker:
```sh
docker-compose up --build
```

### 4️⃣ Access API Documentation:
- Open **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
## 🔐 Token Authentication in Swagger UI
1. Login via `POST /token` with email & password.
2. Copy the `access_token` from the response.
3. Click **Authorize (🔓)** in Swagger UI.
4. Enter: `Bearer YOUR_ACCESS_TOKEN`.
5. Now you can access protected routes.

---

## 📂 Project Structure
```
Event-management-using-FastAPI/
├── cache/
│   ├── cache_reset.py
│   ├── cache_set.py
│   ├── connect.py
│   ├── utility.py
├── configuration/
│   ├── connection.py
├── model/
│   ├── model.py
├── routers/
│   ├── bulk_insert.py
│   ├── event_activities.py
│   ├── event_controls.py
│   ├── logins.py
├── schemas/
│   ├── schema.py
├── storage/
│   ├── database.py
│   ├── query_data.py
├── stub/
│   ├── sample_data_100_updated.csv
├── tokenization/
│   ├── auth.py
├── .env
├── .gitignore
├── DockerFile
├── main.py
├── README.md
├── requirement.txt
```

---

## 🎯 Future Enhancements
- 🔒 Add role-based permissions.
- 📩 Enable email notifications for registrations.
- 🚀 Improve performance with background tasks.

---



Enhance UI with a frontend (React/Next.js).

💡 Built with ❤️ using FastAPI & PostgreSQL
