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
- **Feedback Submission**: (Assumed) Endpoints for submitting and managing feedback.
- **Containerized**: Easily deployable with Docker Compose.
- **Testing**: Pytest-based test suite.

## API Endpoints

### Auth

- `POST /auth/signup`  
  Register a new user.  
  **Body:**  
  ```json
  {
    "username": "yourname",
    "password": "yourpassword"
  }
  ```

- `POST /auth/login`  
  Login and receive a JWT token.  
  **Body:**  
  ```json
  {
    "username": "yourname",
    "password": "yourpassword"
  }
  ```
  **Response:**  
  ```json
  {
    "access_token": "jwt_token",
    "token_type": "bearer"
  }
  ```

### User

- `GET /user/profile`  
  Get the current user's profile.  
  **Headers:**  
  `Authorization: Bearer <access_token>`

### Admin

- `GET /admin/users`  
  List all users (admin only).  
  **Headers:**  
  `Authorization: Bearer <admin_access_token>`

- `PATCH /admin/users/{user_id}`  
  Update a user's information (admin only).  
  **Body:**  
  ```json
  {
    "username": "newusername"
  }
  ```
