# Role-Based-Feedback-Collector-API
A containerized FastAPI application with JWT authentication, user/role management, and feedback submission APIs.


## How to run
```bash
git clone https://github.com/manialm/Feedback-API
cd Feedback-API
docker compose up
```

## Environment Variables

You can generate a `.env` file with the required environment variables using the following script:
```bash
cat <<EOF > .env
JWT_SECRET=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EOF
```



## Features

- **User Signup & Login**: Register and authenticate users with JWT tokens.
- **Role Management**: Admin and regular user roles.
- **Admin Endpoints**: List and update users (admin only).
- **Feedback Submission**: Endpoints for submitting and managing feedback.
- **Containerized**: Easily deployable with Docker Compose.
- **Testing**: Pytest-based test suite.

## API Endpoints

### Authentication Endpoints (`/auth`)

#### `POST /auth/signup`
Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Error Responses:**
- `400 Bad Request`: Username already exists

#### `POST /auth/login`
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

**Error Responses:**
- `404 Not Found`: User not found
- `401 Unauthorized`: Incorrect password

### User Endpoints (`/user`)

*Requires authentication (Bearer token)*

#### `GET /user/profile`
Get current user's profile information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "string"
}
```

#### `POST /user/feedback`
Submit feedback as the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "rating": 5,
  "comment": "Great service!"
}
```

**Response:**
```json
{
  "id": 1,
  "rating": 5,
  "comment": "Great service!",
  "user_id": 1
}
```

**Validation:**
- `rating`: Integer between 1-10 (defaults to 1)
- `comment`: String up to 256 characters (optional)

### Admin Endpoints (`/admin`)

*Requires admin authentication (Bearer token)*

#### `GET /admin/users`
List all users in the system.

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "string",
    "password_hash": "string",
    "is_admin": true
  }
]
```

#### `PATCH /admin/users/{id}`
Update user information.

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "is_admin": true
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "password_hash": "string",
  "is_admin": true
}
```

#### `GET /admin/feedback`
List all feedback submissions.

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "rating": 5,
    "comment": "Great service!",
    "user_id": 1
  }
]
```

#### `PATCH /admin/roles/{user_id}`
Change user's admin role.

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "is_admin": true
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "password_hash": "string",
  "is_admin": true
}
```

### Public Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```
"App is running"
```

#### `GET /feedback/summary`
Get feedback statistics.

**Response:**
```json
{
  "count": 10,
  "average": 7.5
}
```

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

Tokens are obtained by calling the `/auth/login` endpoint and expire after 30 minutes by default.

## Testing

Run the test suite:

```bash
pytest
```