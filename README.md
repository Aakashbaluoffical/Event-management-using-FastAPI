Event Management System

An Event Management System built using FastAPI, SQLAlchemy, PostgreSQL, Redis, JWT, and Docker.

🚀 Features

🏷️ User Features

User can register and login.

View all available events.

Select an event and register.

View all registrations with user ID validation.

Cancel a registered event.

🎟️ Event Hosting Features

Create, Edit, and Cancel events.

Manage event Check-in/Check-out (as an event in-charge, manage check-in/check-out for registered users).

Insert bulk data through .csv uploads.

🔑 Role-Based Access

User: Can view events and register for events.

Superuser: Can create, edit, cancel events.

⚡ Caching with Redis

Reduces database calls and improves performance.

✅ Validation & Security

Uses Pydantic for API request validation.

Implements JWT-based authentication for secure access.

📂 Database Schema

The project uses three tables:

user_tbl - Stores user information.

event_tbl - Stores event details.

attendee_tbl - Manages event registrations.

📌 Sample Data

User Table (user_tbl)

id

first_name

last_name

email

role

1

John

Doe

john@example.com

user

2

Alice

Smith

alice@example.com

superuser

Event Table (event_tbl)

id

name

start_time

end_time

location

1

Tech Meetup

2025-02-20 10:00:00

2025-02-20 12:00:00

New York

2

AI Workshop

2025-03-01 14:00:00

2025-03-01 16:00:00

Online

Attendee Table (attendee_tbl)

id

event_id

user_id

check_in_status

1

1

1

True

2

2

1

False

🔥 Tech Stack

FastAPI (Backend Framework)

PostgreSQL (Database)

SQLAlchemy (ORM for database interactions)

Redis (Caching layer to reduce database calls)

Docker (Containerization)

JWT (Authentication & Authorization)

Pydantic (Data validation)

🛠️ API Endpoints

📌 Authentication

POST /register - User registration.

POST /token - Login and generate JWT token.

📌 Event Management

GET /events - Fetch all events.

POST /events - Create a new event (Superuser only).

PUT /events/{event_id} - Edit an event (Superuser only).

DELETE /events/{event_id} - Cancel an event (Superuser only).

📌 User Event Actions

POST /register-event/{event_id} - Register for an event.

GET /my-registrations - View all registered events.

DELETE /cancel-registration/{event_id} - Cancel event registration.

📌 Event Check-In/Out

POST /check-in/{event_id}/{user_id} - Check-in a user (Event In-Charge only).

POST /check-out/{event_id}/{user_id} - Check-out a user (Event In-Charge only).

📌 Bulk Data Upload

POST /upload-events - Upload events in bulk using .csv.

🧪 Testing Phases

Phase 1: Manual testing.

Phase 2: Automated testing using pytest.

🐳 Running the Project with Docker

Clone the repository:

git clone https://github.com/your-repo/event-management.git
cd event-management

Copy the .env.example to .env and fill in required values:

cp .env.example .env

Build and run using Docker:

docker-compose up --build

Access Swagger UI at:

http://127.0.0.1:8000/docs

🔐 How to Use Token Authentication in Swagger UI

Login via POST /token with email & password.

Copy the access_token from the response.

Click Authorize (🔓) in Swagger UI.

Enter: Bearer YOUR_ACCESS_TOKEN.

Now you can access protected routes.

🎯 Future Enhancements

Add role-based permissions.

Enable email notifications for registrations.

Improve performance with background tasks.

Enhance UI with a frontend (React/Next.js).

💡 Built with ❤️ using FastAPI & PostgreSQL