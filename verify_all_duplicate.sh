#!/bin/bash

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <folder_A> <folder_B>"
  exit 1
fi

FOLDER_A="$1"
FOLDER_B="$2"

# Output files
DUPES_RAW="dupes_raw.txt"
MATCHED_A="matched_from_A.txt"
ALL_A="all_a.txt"

# Step 1: Find all duplicates between A and B
fdupes -r "$FOLDER_A" "$FOLDER_B" > "$DUPES_RAW"

# Step 2: Extract unique matched files from A only
grep "$FOLDER_A" "$DUPES_RAW" | sort -u > "$MATCHED_A"

# Step 3: Get all files in A
find "$FOLDER_A" -type f | sort -u > "$ALL_A"

# Step 4: Compare — check if all A files are matched
if diff -q "$MATCHED_A" "$ALL_A" > /dev/null; then
  echo "All files in $FOLDER_A are duplicated in $FOLDER_B — safe to delete."
  rm -f "$DUPES_RAW" "$MATCHED_A" "$ALL_A"
  exit 0
else
  echo "Some files in $FOLDER_A were NOT found in $FOLDER_B:"
  comm -23 "$ALL_A" "$MATCHED_A"
  rm -f "$DUPES_RAW" "$MATCHED_A" "$ALL_A"
  exit 1
fi


