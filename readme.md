# Manage duplicates
See license.txt

A collection of helper scripts to remove duplicate files, and rename files based on metadata.
Do not use without reviewing all scripts.

`create_db.py` - creates the sqlite schema

`seed_db.py` - add files to the db, with accompanying metadata, this is a read heavy operation

`populate_columns.py` - populate columns, including new file names

`move_files.py` - move files w/ new name to directory

`iterate_fdupes_results.py` - iterates over the groups output by fdupes command, and moves dupes to specified directory.
This file contains options that should be reviewed or expanded upon.

`print_exif.py` - prints exif data of given file

## Prerequisites
- [fdupes](https://github.com/adrianlopezroche/fdupes)

## Move duplicates to directory to be delete
```shell
pip install -r requirements.txt
# identify duplicates
./find_dupes.sh /Volumes/external/photos > dupes.txt
# move duplicates to specified dir (read script to choose option)
# You may want to modify this if you wish to keep a certain directory structure
python iterate_fdupes_results all_but_first dupes.txt '/Volumes/external/to_delete'
```

## Rename files to YYYY_MM_DD_camera_original_file_name_w_extension
This process is iterative, so files and db can be analyzed in between
```shell
# creates sqlite db w/ schema
python create_db.py image_metadata.db
# create a sqlite db of metadata for files 
python seed_db.py > seed_out.txt
# populate the columns in the table
python populate_columns.py > populate_out.txt
# move original files to new destination with new file name
python move_files.py /Volumes/external/moved_photos image_metadata.db move_out.txt
```

## Ensure to_delete dir doesn't have unique files within
First directory is directory that should be free of originals
```shell
./verify_all_duplicate.sh /Volumes/external/to_delete /Volumes/external/moved_photos > verify_out.txt
```
