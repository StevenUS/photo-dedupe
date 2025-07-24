#!/bin/bash

# ./dupes_between.sh /Volumes/external/photos /Volumes/external/photos_2
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <folder1> <folder2>"
  exit 1
fi

fdupes -r "$1" "$2" > duplicates_between.txt