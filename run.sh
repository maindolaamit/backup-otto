#!/bin/bash

# Run the application
# $1: run mode - backup or restore
#
echo $1
# if input argument is null or backup then run in backup mode
if [ -z "$1" ] || ["$1" == "backup" ]; then
    echo "Running in backup mode"
    python3 app.py backup
else
    echo "Running in restore mode"
    python3 app.py restore
fi
