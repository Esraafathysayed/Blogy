# Blogy - Backend for a Simple Social Media Site

## Introduction
**Blogy** is a backend service for a simple social media platform built using FastAPI. It provides users with the ability to register, log in, manage profiles, create posts, comment on posts, and like/dislike them. The service is built with security in mind, employing JWT for user authentication and leveraging PostgreSQL for robust data storage.

The project is designed to showcase core backend development skills, such as creating and managing RESTful APIs, handling user authentication, and implementing CRUD functionalities.

---

## Features
- **User Registration and Authentication**:
  - JWT-based authentication for secure login and session management.
- **Profile Management**:
  - View, edit, and delete user profiles.
- **Post Creation and Management**:
  - Create, edit, and delete posts.
  - Like and comment on posts.
- **Commenting System**:
  - Comment on posts and view comments.
- **Liking System**:
  - Like and unlike posts.

---

## Installation

### Prerequisites
- **Python 3.8+**
- **PostgreSQL** (for database)
- **FastAPI** (for the backend framework)
- **SQLAlchemy** (for ORM)
- **Alembic** (for database migrations)

### Steps to Set Up

1. **Clone the repository**:
    ```bash
    https://github.com/Esraafathysayed/Blogy.git
    cd blogy
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/MacOS
    # or
    venv\Scripts\activate  # Windows
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL**:
   - Create a PostgreSQL database:
     ```bash
     createdb blogy_db
     ```
   - Update the `DATABASE_URL` in your environment or config file to point to your local PostgreSQL instance:
     ```
     DATABASE_URL=postgresql://username:password@localhost/blogy_db
     ```

5. **Run Alembic migrations**:
    ```bash
    alembic upgrade head
    ```

6. **Run the FastAPI server**:
    ```bash
    python3 -m app.app
    ```

7. **Test the APIs using Postman**:
    - Import the Postman collection found in the `/postman` directory to start testing the APIs.

---

## Usage

Once the server is running, you can interact with the APIs. Some key endpoints are:

- **User Registration**:
  - `POST /register`: Register a new user.
  
- **User Login**:
  - `POST /login`: Authenticate and receive a JWT token.
  
- **Profile Management**:
  - `GET /profile/{user_id}`: View a user's profile.
  - `PUT /profile/{user_id}`: Edit your profile.
  - `DELETE /profile/{user_id}`: Delete your profile.
  
- **Post Management**:
  - `POST /posts`: Create a new post.
  - `GET /posts`: Get all posts.
  - `GET /posts/{post_id}`: View a specific post.
  - `PUT /posts/{post_id}`: Edit a post.
  - `DELETE /posts/{post_id}`: Delete a post.
  
- **Commenting and Liking**:
  - `POST /posts/{post_id}/comments`: Comment on a post.
  - `POST /posts/{post_id}/like`: Like or unlike a post.

> Make sure to include the JWT token in the `Authorization` header for any protected routes:


---

## Contributing

Contributions are welcome! If you'd like to improve Blogy, follow these steps:

1. Fork the repository.
2. Create a new feature branch:
  ```bash
  git checkout -b feature/my-feature
  ```
3. Commit your changes:
  ```bash
  git commit -m "Add some feature"
  ```
4. Push the branch:
  ```bash
  git push origin feature/my-feature
  ```
5. Open a pull request.

---

## Contact

For any questions, feel free to reach out to the project maintainer:

- **Email**: esraafathy79295@gmail.com
- **LinkedIn**: [Esraa Fathy](https://www.linkedin.com/in/esraa-fathy-sayed/)

---

**Blogy** is a simple demonstration of FastAPI's capabilities in building a backend service. Feel free to fork and build on this foundation!
