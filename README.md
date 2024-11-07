# Advanced REST API with Django, Docker, and TDD

A RESTful API built with Django REST Framework and Docker using Test Driven Development (TDD).

## Features
- **Docker Integration**: Runs development server in isolated containers.
- **Test Driven Development (TDD)**: Ensures stability with comprehensive tests.
- **Advanced API Features**: Upload and view images, manage authentication, etc.
- **CI/CD**: Travis CI integrated for automated checks.

## Development environment
1. Install docker and docker compose.
2. Create a virtual environment and install the local dependencies.
3. Make some changes.
4. Create a .env files based on `.env.example`.
5. Use the commands bellow inside of the `/recipe_api` directory:

### Prerequisites

- Python 3.10+
- Django 4.0+
- Pytest
- PostgreSQL (or any other preferred database)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/doostiyan/-Online-shop
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements/local.txt
    ```
4. **First change directory:**

    ```bash
    cd recipe_api
    ```

5. **Run tests:**

    ```bash
    pytest
    ```
6. **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

7. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

9. **Visit the site:**

    Open your browser and go to `http://127.0.0.1:8000/`.
