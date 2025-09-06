# FastAPI Project

This is a FastAPI project that implements a RESTful API with support for JWT authentication, SQLAlchemy for database interactions, and Pydantic for data validation. The project is structured to facilitate easy development and deployment.

## Project Structure

```
fastapi-app
├── .env                  # Environment variables for the application
├── .gitignore            # Files and directories to ignore in version control
├── alembic.ini           # Configuration for Alembic migrations
├── database.py           # Database connection setup and models
├── gunicorn.conf.py      # Configuration for Gunicorn server
├── main.py               # Entry point of the application
├── README.md             # Project documentation
├── render.yaml           # Deployment configuration for Render
├── requirements.txt      # Project dependencies
├── app                   # Application modules
│   ├── crud              # CRUD operations
│   ├── models            # SQLAlchemy models
│   ├── routes            # API routes
│   └── schemas           # Pydantic schemas
└── alembic               # Alembic migration files
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your database connection string and secret key:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ```

5. **Run database migrations:**
   ```
   alembic upgrade head
   ```

6. **Start the application:**
   ```
   gunicorn -c gunicorn.conf.py main:app
   ```

## Usage

- The API is accessible at `http://localhost:8000`.
- Use tools like Postman or curl to interact with the API endpoints defined in the `app/routes` directory.

## Deployment

This project is ready for deployment on Render. Ensure that the `render.yaml` file is configured with the correct settings for your environment.

## License

This project is licensed under the MIT License. See the LICENSE file for details.