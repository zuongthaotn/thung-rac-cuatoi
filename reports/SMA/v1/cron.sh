#!/bin/bash
echo "-----------------------------------------------------"
echo "Date: $(date)"
DIR=$(cd "$(dirname "$0")"; pwd)
cd $DIR
cd ../../..
#echo $PWD
venv/bin/python reports/SMA/v1/LiveRunning.py
