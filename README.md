# FastAPI Posts API

A RESTful API built with FastAPI for managing posts with user authentication and voting functionality.

## Tech Stack

- **FastAPI** — Modern Python web framework
- **SQLAlchemy** — ORM for database operations
- **PostgreSQL** — Relational database
- **Alembic** — Database migrations
- **PyJWT** — JWT-based authentication
- **Pydantic** — Data validation

## Prerequisites

- Python 3.10+
- PostgreSQL database

## Local Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastapi
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=your_database
   DATABASE_USERNAME=your_username
   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

6. **Start the server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## Database Migrations

This project uses Alembic for database schema management.

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "migration description"

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Authenticate user and get JWT token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/{id}` | Get user by ID |

### Posts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/posts/` | Get current user's posts with vote counts | Required |
| POST | `/posts/` | Create a new post | Required |
| GET | `/posts/all` | Get all posts with vote counts | — |
| GET | `/posts/{id}` | Get post by ID | Required |
| PUT | `/posts/{id}` | Update a post | Required |
| DELETE | `/posts/{id}` | Delete a post | Required |

### Votes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/vote/` | Vote on a post (dir: 1 to add vote, 0 to remove vote) | Required |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

1. Create a user via `POST /users/`
2. Login via `POST /login` with form data (`username` = email, `password`)
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```

## API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
├── app/
│   ├── main.py          # Application entry point
│   ├── config.py        # Environment settings
│   ├── databases.py     # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schema.py        # Pydantic schemas
│   ├── oauth2.py        # JWT authentication
│   ├── utils.py         # Password hashing utilities
│   └── routers/
│       ├── auth.py      # Authentication routes
│       ├── posts.py     # Post CRUD routes
│       ├── users.py     # User routes
│       └── vote.py      # Voting routes
├── alembic_db/          # Alembic migrations
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not in repo)
```

## License

This project is provided as-is for educational and development purposes.
