import sys
import subprocess
import json


def print_date_fields(file_path):
    try:
        result = subprocess.run(
            ["exiftool", "-j", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        metadata = json.loads(result.stdout)
        if not metadata:
            print("No metadata found.")
            return

        date_fields = {k: v for k, v in metadata[0].items() if "date" in k.lower()}
        if date_fields:
            print(json.dumps(date_fields, indent=4))
        else:
            print("No date fields found in metadata.")
    except subprocess.CalledProcessError as e:
        print(f"Error reading metadata: {e}")
    except FileNotFoundError:
        print("exiftool is not installed or not found in PATH.")


# Helper script for printing metadata of a file
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python print_exif.py <path_to_file>")
        sys.exit(1)

    _file_path = sys.argv[1]
    print_date_fields(_file_path)
