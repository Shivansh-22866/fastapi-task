# Task Management API

A FastAPI-based Task Management application with MongoDB as the database, providing user and task management, authentication, and task analytics.

## Features

- User registration and login
- Task creation, retrieval, update and deletion
- Analytics on task status and priority distribution
- Secure authentication using OAuth2 tokens

## Installation

Follow these steps to get the project up and running on your local machine.

### 1. Clone the repository

bash
```
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

### 2. Set Up Virtual Environment
It's recommended to use a virtual environment to manage dependencies. Create and activate the virtual environment:

bash
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install the required dependencies using pip:

bash
```
pip install -r requirements.txt
```

### 4. Set Up MongoDB
Ensure that MongoDB is running locally or use a MongoDB service like Atlas. Update the MONGO_URL in your configuration files if necessary to point to your MongoDB instance.

### 5. Run the application
Once everything is set up, run the FastAPI application using uvicorn:

bash
```
uvicorn app.main:app --reload
```
The application will start running on http://127.0.0.1:8000.

### 6. Swagger documentation

The FastAPI application automatically generates interactive API documentation. You can access it at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc UI: http://127.0.0.1:8000/redoc

## Project Structure

```
app/
├── __init__.py              # Initializes the app package
├── main.py                  # Main FastAPI application entry point
├── config.py                # Configuration settings (e.g., MongoDB connection)
├── models/                  # Data models
│   ├── __init__.py
│   ├── user.py              # User model
│   └── task.py              # Task model
├── database/                # MongoDB database connection
│   ├── __init__.py
│   └── mongodb.py           # MongoDB connection and helpers
├── auth/                    # Authentication logic
│   ├── __init__.py
│   └── security.py          # OAuth2 token creation and security
└── api/                     # API route handlers
    ├── __init__.py
    ├── users.py             # User routes
    ├── tasks.py             # Task routes
    └── analytics.py         # Task analytics routes
```

## API Endpoints

### User Endpoints
- `POST /users`: Register a new user
- `POST /token`: Log in and receive an OAuth2 token

### Task Endpoints
- `POST /tasks`: Create a new task
- `GET /tasks`: Get a list of tasks assigned to the current user (supports filtering by status and priority)
- `GET /tasks/{task_id}`: Retrieve a specific task by its ID
- `PATCH /tasks/{task_id}`: Update a task by its ID
- `DELETE /tasks/{task_id}`: Delete a task by its ID

### Analytics Endpoints
- `GET /analytics/task-status`: Get a breakdown of task statuses for the current user
- `GET /analytics/priority-distribution`: Get a breakdown of task priority distribution for the current user

### Authentication
The API uses OAuth2 password flow for user authentication:

Users must first register via `/users` and then log in via `/token` to obtain a bearer token.
The token must be included in the `Authorization` header as `Bearer <token>` for endpoints that require authentication.