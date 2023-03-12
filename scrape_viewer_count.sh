#!/bin/bash

HISTORY_FILE="./history.csv"

if [ ! -f "$HISTORY_FILE" ]; then
	echo "timestamp,count" > $HISTORY_FILE
fi

CURRENT_TIMESTAMP=$(date +"%s")
VIEWER_COUNT=$(curl -s https://twitchtracker.com/statistics/viewers | grep -m 1 "g-x-s-value to-number" | grep -oe '\([0-9]*\)')

echo $CURRENT_TIMESTAMP,$VIEWER_COUNT >> $HISTORY_FILE

