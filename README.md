# Atom FastAPI Application

Welcome to the Atom FastAPI application repository! This project is a RESTful web service designed to manage to-do items and user accounts. Built with FastAPI, it provides a robust and efficient way to handle CRUD operations for todos and users. The application leverages SQLAlchemy for object-relational mapping and Alembic for database migrations, ensuring smooth database schema evolution.

## Features

- **User Management:** Register, update, and delete user accounts. Retrieve user information by ID or email.
- **To-Do Management:** Create, update, delete, and retrieve to-do items. Each to-do item is associated with a specific user.
- **Database Migrations:** Managed through Alembic, allowing for incremental, reversible changes to the database schema.

## Project Structure

- `alembic/`: Database migrations.
- `atom/`: Main application directory.
- `crud/`: CRUD operations.
- `models/`: SQLAlchemy models.
- `routers/`: API routers.
- `schemas/`: Pydantic models for request and response data validation.
- `tests/`: Unit and integration tests.
- `main.py`: FastAPI application entry point.

## Built With

This section outlines the key technologies and frameworks utilized in developing the Atom FastAPI application. These tools were chosen for their reliability, efficiency, and support in building modern web applications.

- **FastAPI** - The web framework used for building APIs. FastAPI is known for its high performance and ease of use for creating RESTful APIs.
- **SQLAlchemy** - The ORM (Object Relational Mapper) used for database interactions. SQLAlchemy provides a full suite of well-known enterprise-level persistence patterns.
- **Alembic** - Used for database migrations. Alembic allows for version-controlled schema changes and is tightly integrated with SQLAlchemy.
- **Poetry** - Dependency management and packaging made easy. Poetry helps in managing project dependencies and packaging in a consistent, reproducible manner.
- **Docker** - Containerization platform used to package the application and its dependencies into containers for easy deployment and scalability.
- **Docker Compose** - A tool for defining and running multi-container Docker applications. It is used to manage the application services (e.g., web server, database) in development, testing, and production environments.
- **GitHub Actions** - CI/CD platform used to automate the build, test, and deployment pipeline, enabling continuous integration and continuous deployment workflows for the project.
