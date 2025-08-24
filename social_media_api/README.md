# Social Media API

This project contains the foundational setup for a social media API built with Django and Django REST Framework. The primary focus of this initial phase is setting up the project environment, creating a custom user model, and implementing a robust token-based authentication system.

---

## Project Setup and Installation

Follow these steps to set up the project locally.

### Prerequisites

Ensure you have Python and `pip` installed.

-   **Python 3.8+**
-   **pip**

### Installation Steps

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Emane-11/Alx_DjangoLearnLab.git](https://github.com/Emane-11/Alx_DjangoLearnLab.git)
    cd social_media_api
    ```

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install django djangorestframework pillow
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Start the Development Server**:
    ```bash
    python manage.py runserver
    ```

The API will now be running on `http://127.0.0.1:8000/`.

---

## API Endpoints for User Authentication

The `accounts` app handles all user-related functionalities, including registration and authentication.

### User Model Overview

The custom `User` model extends Django's `AbstractUser` and includes the following fields:
-   `bio`: A text field for the user's biography.
-   `profile_picture`: An image field to store a user's profile picture.
-   `followers`: A many-to-many relationship to itself, allowing users to follow each other.

### Authentication Endpoints

-   **Register a New User**:
    -   **URL**: `/api/auth/register/`
    -   **Method**: `POST`
    -   **Request Body**:
        ```json
        {
          "username": "your_username",
          "email": "your_email@example.com",
          "password": "your_password"
        }
        ```
    -   **Success Response**: Returns the newly created user's data.

-   **Log in and Get a Token**:
    -   **URL**: `/api/auth/login/`
    -   **Method**: `POST`
    -   **Request Body**:
        ```json
        {
          "username": "your_username",
          "password": "your_password"
        }
        ```
    -   **Success Response**: Returns a unique authentication token. This token must be included in subsequent authenticated requests.
        ```json
        {
          "token": "your_unique_auth_token",
          "user_id": 1
        }
        ```

-   **Access User Profile**:
    -   **URL**: `/api/auth/profile/`
    -   **Method**: `GET`, `PUT`, `PATCH`
    -   **Authentication**: Requires a valid **Token** in the `Authorization` header.
    -   **Header**: `Authorization: Token <your_unique_auth_token>`
    -   **Success Response**: Returns or updates the profile of the authenticated user.

---

## Testing with Postman

You can use Postman or a similar API testing tool to interact with the endpoints.

1.  **Register**: Send a `POST` request to `/api/auth/register/` with user details.
2.  **Login**: Send a `POST` request to `/api/auth/login/` with the username and password to get a token.
3.  **Authenticate**: Use the received token for accessing protected endpoints like `/api/auth/profile/` by setting the `Authorization` header.

## API Endpoints for Posts and Comments

The `posts` app provides functionality for creating, managing, and interacting with posts and comments.

### Posts Endpoints

-   **List and Create Posts**:
    -   **URL**: `/api/posts/`
    -   **Method**: `GET` (List all posts, paginated) or `POST` (Create a new post)
    -   **Authentication**: `GET` is public, `POST` requires a valid token.
    -   **Filtering**: Supports searching by title or content (`?search=<query>`) and filtering by author (`?author=<user_id>`).

-   **Retrieve, Update, and Delete a Post**:
    -   **URL**: `/api/posts/<id>/`
    -   **Method**: `GET`, `PUT`, `PATCH`, `DELETE`
    -   **Authentication**: Required for all methods. `PUT`, `PATCH`, `DELETE` are restricted to the post's author.

### Comments Endpoints

-   **List and Create Comments**:
    -   **URL**: `/api/posts/<post_id>/comments/`
    -   **Method**: `GET` (List comments for a specific post) or `POST` (Create a new comment)
    -   **Authentication**: `GET` is public, `POST` requires a valid token.

-   **Retrieve, Update, and Delete a Comment**:
    -   **URL**: `/api/posts/<post_id>/comments/<id>/`
    -   **Method**: `GET`, `PUT`, `PATCH`, `DELETE`
    -   **Authentication**: Required for all methods. `PUT`, `PATCH`, `DELETE` are restricted to the comment's author.