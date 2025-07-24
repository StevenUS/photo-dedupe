import os
import shutil
import sys


def iterate_groups(filepath):
    group = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                if group:
                    yield group
                    group = []
            else:
                group.append(line)
        if group:
            yield group  # yield last group if file doesn't end with newline


def move_all_but_first(input_file, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for group in iterate_groups(input_file):
        for dup_path in group[1:]:  # skip the first
            if os.path.exists(dup_path):
                try:
                    shutil.move(dup_path, target_dir)
                    print(f"Moved: {dup_path}")
                except Exception as e:
                    print(f"Error moving {dup_path}: {e}")


def move_non_matched(input_file, target_dir, match_folder):
    os.makedirs(target_dir, exist_ok=True)
    for group in iterate_groups(input_file):
        to_keep = [p for p in group if match_folder in p]
        to_delete = [p for p in group if p not in to_keep]

        if not to_keep and to_delete:
            to_keep.append(to_delete.pop(0))

        for path in to_delete:
            if os.path.exists(path):
                try:
                    shutil.move(path, target_dir)
                    print(f"Moved: {path}")
                except Exception as e:
                    print(f"Error moving {path}: {e}")


if __name__ == '__main__':
    # Usage:
    # python script.py <mode> <input_file> <target_dir> [match_folder]
    if len(sys.argv) not in (4, 5):
        print("Usage: python script.py <mode> <input_file> <target_dir> [match_folder]")
        sys.exit(1)

    mode = sys.argv[1]
    _input_file = sys.argv[2]
    _target_dir = sys.argv[3]

    if mode == 'all_but_first':
        move_all_but_first(_input_file, _target_dir)
    # deletes all but dir matching string, otherwise deletes the first
    elif mode == 'delete_all_but_match':
        if len(sys.argv) != 5:
            print("Error: 'match_folder' argument is required for 'delete_all_but_match' mode.")
            sys.exit(1)
        _match_folder = sys.argv[4]
        move_non_matched(_input_file, _target_dir, _match_folder)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
