# Choreo App Backend

FastAPI backend with database connectivity, environment variables loading, and CORS support.

## Features

- FastAPI CRUD API with proper route organization
- SQLAlchemy ORM for database operations
- Environment variable configuration
- CORS middleware
- Automatic table creation on startup
- No authentication (as requested)

## Setup

1. Clone the repository

2. Create a virtual environment
```
python -m venv venv
```

3. Activate the virtual environment
- Windows:
```
venv\Scripts\activate
```
- macOS/Linux:
```
source venv/bin/activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Configure the database
- Create a database in PostgreSQL or MySQL
- Configure the `.env` file with your database connection details

## Running the Application

Start the server:
```
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── core/               # Core application code
│   └── config.py       # Environment variable configuration
├── db/                 # Database handling
│   └── database.py     # Database connection
├── models/             # SQLAlchemy models
│   └── example.py      # Example model
├── routers/            # API route modules
│   └── example.py      # Example router
├── schemas/            # Pydantic schemas
│   └── example.py      # Example schema
└── main.py             # Main application entry point
.env                    # Environment variables
.env.example            # Example environment variables
requirements.txt        # Python dependencies
``` 