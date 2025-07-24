import os
import sys
import sqlite3
import json
import subprocess


def get_metadata(path):
    try:
        result = subprocess.run(
            ["exiftool", "-j", path],
            capture_output=True,
            text=True,
            check=True
        )
        json_data = json.loads(result.stdout)
        return json_data[0] if json_data else {}
    except subprocess.CalledProcessError as e:
        print(f"Error reading metadata for {path}: {e}")
        return {}


def store_raw_metadata(cursor, filepath, metadata):
    try:
        cursor.execute("""
            INSERT INTO file_metadata (path, metadata) VALUES (?, ?)
        """, (filepath, json.dumps(metadata)))
    except sqlite3.IntegrityError:
        print(f"Conflict: entry for '{filepath}' already exists")


def walk_and_store_metadata(root_dir, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for fname in filenames:
                full_path = os.path.join(dirpath, fname)
                metadata = get_metadata(full_path)
                if not metadata:
                    continue
                store_raw_metadata(cursor, full_path, metadata)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    # python seed_db.py /Volumes/external/photos image_metadata.db
    if len(sys.argv) != 3:
        print("Usage: python seed_db.py <root_directory> <db_path>")
        sys.exit(1)

    root_directory = os.path.abspath(sys.argv[1])
    DB_PATH = os.path.abspath(sys.argv[2])

    walk_and_store_metadata(root_directory, DB_PATH)
