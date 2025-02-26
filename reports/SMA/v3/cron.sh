#!/bin/bash
echo "-----------------------------------------------------"
echo "Date: $(date)"
DIR=$(cd "$(dirname "$0")"; pwd)
cd $DIR
cd ../../..
#echo $PWD
if [[ $1 = 'buy' ]]
then
  venv/bin/python reports/SMA/v3/LiveRunning.py
elif [[ $1 = 'sell' ]]
then
  venv/bin/python reports/SMA/v3/SellSignal.py
else
  echo "not-sell-not-buy"
fi
