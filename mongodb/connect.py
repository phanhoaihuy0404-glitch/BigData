"""
MongoDB Connection Module
=========================
Reusable module for connecting to MongoDB.

Usage:
    from mongodb.connect import get_database
    db = get_database()

Requirements:
    - pymongo must be installed (pip install pymongo)
    - MongoDB must be running on localhost:27017
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from mongodb.config import MONGO_URI, DATABASE_NAME


def get_database(timeout_ms: int = 5000):
    """
    Connect to MongoDB and verify the connection.

    Parameters
    ----------
    timeout_ms : int
        Server selection timeout in milliseconds (default 5000).

    Returns
    -------
    pymongo.database.Database
        The target database object.

    Raises
    ------
    ConnectionFailure
        If MongoDB is unreachable or connection fails.
    """
    # Create client with server selection timeout
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=timeout_ms
    )

    # Ping the server to verify the connection is alive
    try:
        client.admin.command("ping")
        print("Connected to MongoDB successfully.")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

    # Select and return the target database
    db = client[DATABASE_NAME]
    print(f"Database:\n{DATABASE_NAME}")

    return db


# ──────────────────────────────────────────────
# Standalone execution
# ──────────────────────────────────────────────
if __name__ == "__main__":
    db = get_database()
    print("\nConnection established. No collections were created.")