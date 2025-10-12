"""Entrypoint for running the FastAPI application."""

import asyncio

import uvicorn

from app.database import engine
from app.main import app
from app.models import Base
from app.sample_data import create_sample_data


def start() -> None:
    """Start the FastAPI application."""
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Populate the database (only if empty)
    create_sample_data()

    # Run the FastAPI app
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        print("Server shut down.")


if __name__ == "__main__":
    start()
