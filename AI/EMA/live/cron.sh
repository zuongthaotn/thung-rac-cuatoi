#!/bin/bash
echo "-----------------------------------------------------"
echo "Date: $(date)"
DIR=$(cd "$(dirname "$0")"; pwd)
cd $DIR
cd ../../..
venv/bin/python AI/EMA/live/run.py