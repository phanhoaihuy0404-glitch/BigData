"""
MongoDB Export Module
=====================
Exports all MongoDB collections to CSV files for Hadoop processing.

Usage:
    from mongodb.export_data import export_all
    export_all()

Or run directly:
    py -m mongodb.export_data

Output directory: data/output/
"""

import pandas as pd
from pathlib import Path
from mongodb.config import DATABASE_NAME
from mongodb.connect import get_database

# Output directory
OUTPUT_DIR = Path("data/output")

# Collections to export in order
COLLECTIONS = [
    "Department",
    "Class",
    "Teacher",
    "Student",
    "Course",
    "Enrollment",
    "Attendance",
]


def export_collection(db, collection_name: str) -> int:
    """
    Export a single MongoDB collection to CSV.

    Parameters
    ----------
    db : pymongo.database.Database
        Target database.
    collection_name : str
        Name of the collection.

    Returns
    -------
    int
        Number of rows exported.
    """
    print(f"Exporting {collection_name}...")

    # Fetch all documents, exclude MongoDB _id
    cursor = db[collection_name].find({}, {"_id": 0})

    # Convert to DataFrame
    df = pd.DataFrame(list(cursor))

    # Write to CSV
    output_path = OUTPUT_DIR / f"{collection_name}.csv"
    df.to_csv(output_path, index=False)

    count = len(df)
    print(f"✓ {count} rows exported")
    return count


def export_all():
    """
    Export all collections from MongoDB to CSV files.
    """
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Connect to MongoDB
    db = get_database()
    print()

    # Export each collection
    results = {}
    for name in COLLECTIONS:
        count = export_collection(db, name)
        results[name] = count

    # Print final summary
    print()
    print("=" * 24)
    print("EXPORT FINISHED")
    print("=" * 24)
    for name in COLLECTIONS:
        print(f"{name:.<15} {results[name]}")


# ──────────────────────────────────────────────
# Standalone execution
# ──────────────────────────────────────────────
if __name__ == "__main__":
    export_all()