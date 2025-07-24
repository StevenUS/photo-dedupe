import sqlite3
import json
from datetime import datetime
import os


def get_camera_name(metadata):
    make = metadata.get("Make", "").strip()
    model = metadata.get("Model", "").strip()

    if not make and not model:
        return ""

    # Normalize spacing and dash join
    cleaned = f"{make}-{model}".replace(" ", "_").replace("__", "_").strip("-_")
    return cleaned


def update_camera_model(conn, row_id, name):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE file_metadata SET camera_model = ? WHERE id = ?",
            (name, row_id)
        )
    except Exception as e:
        print(f"[{row_id}] Failed to update camera_model: {e}")


def get_min_date_from_metadata(metadata):
    dates = []
    for key, value in metadata.items():
        # ProfileDateTime is when the color profile was defined (it is ignored)
        if 'date' in key.lower() and key != 'ProfileDateTime' and isinstance(value, str):
            raw = value.split('-')[0].split('+')[0].strip()
            try:
                dt = datetime.strptime(raw, "%Y:%m:%d %H:%M:%S")
                if dt.year >= 2000:
                    dates.append(dt)
            except ValueError:
                continue
    return min(dates) if dates else None


def update_indexed_date(conn, row_id, dt):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE file_metadata SET indexed_date = ? WHERE id = ?",
            (dt.isoformat(), row_id)
        )
    except Exception as e:
        print(f"[{row_id}] Failed to update indexed_date: {e}")


def build_new_file_name(indexed_date, camera_model, path):
    if not indexed_date or not path:
        return None

    # print(indexed_date)
    # date_part = indexed_date.split("T")[0]  # just the YYYY-MM-DD
    date_part = indexed_date.date().isoformat()
    camera_part = camera_model or ""
    filename = os.path.basename(path)

    # Normalize camera name to avoid spaces or slashes
    camera_part = camera_part.replace(" ", "_").replace("/", "_")

    return f"{date_part}_{camera_part}_{filename}"


def update_new_file_name(conn, row_id, new_name):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE file_metadata SET new_file_name = ? WHERE id = ?",
            (new_name, row_id)
        )
    except Exception as e:
        print(f"[{row_id}] Failed to update new_file_name: {e}")


def loop_over_db(db_path, dry_run=True):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, path, camera_model, metadata FROM file_metadata where path like '/Volumes/T7/photos_app%'"
    )
    for row_id, path, camera_model, metadata_json in cursor.fetchall():
        try:
            metadata = json.loads(metadata_json)
        except json.JSONDecodeError:
            print(f"[{row_id}] Invalid JSON, skipping")
            continue

        min_date = get_min_date_from_metadata(metadata)
        if min_date:
            update_indexed_date(conn, row_id, min_date)
            # print(f"[{row_id}] Updated with {min_date}")
        else:
            print(f"[{row_id}] No valid date found")

        camera_model = get_camera_name(metadata)
        if camera_model:
            update_camera_model(conn, row_id, camera_model)

        if min_date:
            nfn = build_new_file_name(min_date, camera_model, path)
            if nfn:
                update_new_file_name(conn, row_id, nfn)

    if dry_run:
        conn.rollback()
    else:
        conn.commit()
    conn.close()


# This script reads the metadata column, and populates the remaining columns from that metadata
if __name__ == "__main__":
    DB_PATH = os.path.abspath("image_metadata.db")

    # dry_run_indexed_dates(DB_PATH)
    loop_over_db(DB_PATH, False)
