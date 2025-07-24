import sys
import os
import sqlite3


def setup_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("DROP TABLE file_metadata")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_metadata (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE NOT NULL,
                metadata TEXT NOT NULL,
                indexed_date TEXT,
                camera_model TEXT,
                new_file_name TEXT
            );
        """)

        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    # python create_db.py image_metadata.db
    if len(sys.argv) != 2:
        print("Usage: python create_db.py <db_path>")
        sys.exit(1)

    DB_PATH = os.path.abspath("image_metadata.db")
    setup_database(DB_PATH)
    print(f"DB created at {DB_PATH}")
