#!/bin/bash

# ./find_dupes.sh /Volumes/external/photos > dupes.txt
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

FOLDER="$1"

fdupes -r "$FOLDER"