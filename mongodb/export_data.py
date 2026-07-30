from pathlib import Path
import pandas as pd

from mongodb.connect import get_database

OUTPUT_DIR = Path("data/output")

COLLECTIONS = [
    "Student",
    "Course",
    "Enrollment",
]


def export_collection(db, collection_name):

    print(f"Exporting {collection_name}...")

    documents = list(
        # find(filter, projection)
        db[collection_name].find({}, {"_id": 0})
     )

    dataframe = pd.DataFrame(documents)

    output_file = OUTPUT_DIR / f"{collection_name}.csv"

    dataframe.to_csv(output_file, index=False)

    print(f"[OK] {len(dataframe)} rows exported")

    return len(dataframe)


def export_all():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    db = get_database()

    results = {}

    for collection_name in COLLECTIONS:
        results[collection_name] = export_collection(db, collection_name)

    print("\nEXPORT FINISHED\n")

    for collection_name, row_count in results.items():
        print(f"{collection_name:.<15} {row_count}")


if __name__ == "__main__":
    export_all()