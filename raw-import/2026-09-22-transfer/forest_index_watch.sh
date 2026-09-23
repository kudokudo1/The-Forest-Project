#!/bin/bash

VAULT="/home/user/Downloads/The Forest Project/The Forest Project"

python3 "$HOME/forest_index.py"

inotifywait \
  -m \
  -r \
  -e close_write,create,delete,move \
  --exclude 'forest-index\.json$' \
  "$VAULT" |
while read -r directory events filename
do
    case "$filename" in
        *.md)
            python3 "$HOME/forest_index.py"
            ;;
    esac
done
