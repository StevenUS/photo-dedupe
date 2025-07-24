import os
import sys
import shutil
import sqlite3


def move_files_from_db(db_path, new_dir: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, path, new_file_name FROM file_metadata where path like '%photos_app%'")
    rows = cursor.fetchall()

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for row_id, original_path, new_file_name in rows:
        if not original_path or not new_file_name:
            print(f"[{row_id}] Skipping missing path or filename.")
            continue

        if not os.path.exists(original_path):
            print(f"[{row_id}] File not found: {original_path} — skipping.")
            continue

        dest_path = os.path.join(new_dir, new_file_name)

        # Ensure unique name in destination
        base, ext = os.path.splitext(dest_path)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = f"{base}_{counter}{ext}"
            counter += 1

        try:
            print(f"[{row_id}] Moving: {original_path} → {dest_path}")
            shutil.move(original_path, dest_path)
        except Exception as e:
            print(f"[{row_id}] Error moving file: {e}")

    conn.close()


if __name__ == "__main__":
    # python move_files.py /Volumes/external/moved_photos image_metadata.db
    if len(sys.argv) != 3:
        print("Usage: python seed_db.py <root_directory> <db_path>")
        sys.exit(1)

    DEST_DIR = os.path.abspath(sys.argv[1])
    DB_PATH = os.path.abspath(sys.argv[2])

    move_files_from_db(DB_PATH, DEST_DIR)
