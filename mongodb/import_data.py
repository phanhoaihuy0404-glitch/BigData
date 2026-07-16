"""
MongoDB Import Module
=====================
Imports processed CSV files into MongoDB collections.

Usage:
    from mongodb.import_data import import_all
    import_all()

Or run directly:
    py -m mongodb.import_data

Requires:
    - MongoDB running on localhost:27017
    - Processed CSV files in data/processed/
"""

import pandas as pd
from pathlib import Path
from mongodb.config import MONGO_URI, DATABASE_NAME
from mongodb.connect import get_database

# Path to processed CSV files
PROC_DIR = Path("data/processed")

# Mapping: collection name → CSV filename
COLLECTIONS = [
    "Department",
    "Class",
    "Teacher",
    "Student",
    "Course",
    "Enrollment",
    "Attendance",
]


def import_collection(db, collection_name: str) -> int:
    """
    Import a single CSV file into a MongoDB collection.

    Steps:
      1. Read CSV with pandas
      2. Clear existing documents from the collection
      3. Insert all rows

    Parameters
    ----------
    db : pymongo.database.Database
        Target database.
    collection_name : str
        Name of the collection and CSV file (without extension).

    Returns
    -------
    int
        Number of documents imported.
    """
    csv_path = PROC_DIR / f"{collection_name}.csv"
    print(f"Importing {collection_name}...")

    # Read CSV
    df = pd.read_csv(csv_path)

    # Convert DataFrame rows to list of dictionaries
    # Fill NaN with None so MongoDB stores them as null
    documents = df.where(df.notna(), None).to_dict(orient="records")

    # Clear existing documents
    collection = db[collection_name]
    collection.delete_many({})

    # Insert all documents
    if documents:
        collection.insert_many(documents)

    count = len(documents)
    print(f"✓ {count} documents imported")
    return count


def import_all():
    """
    Import all processed CSV files into MongoDB.

    Prints a summary of imported document counts per collection.
    """
    # Connect to MongoDB
    db = get_database()

    print()

    # Import each collection
    results = {}
    for name in COLLECTIONS:
        count = import_collection(db, name)
        results[name] = count

    # Print final summary
    print()
    print("=" * 24)
    print("IMPORT FINISHED")
    print("=" * 24)
    for name in COLLECTIONS:
        print(f"{name:.<15} {results[name]}")


# Standalone execution
if __name__ == "__main__":
    import_all()