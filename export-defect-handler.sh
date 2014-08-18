#!/bin/sh

# SCRIPT_DIR contains the absolute path to the directory where the
# export-defect-handler.py script is located.

SCRIPT_DIR=/home/demo/sample-scripts

# Set these values to something appropriate for your installation.

USER=admin
PASSWORD=coverity
HOST=localhost
PORT=8080

cd $SCRIPT_DIR
/usr/bin/python export-defect-handler.py --inputfile=$1 --user=$USER --password=$PASSWORD --host=$HOST --port=$PORT
