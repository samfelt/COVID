#! /usr/bin/env bash

FILENAME='WA-data.json'
mv "$FILENAME" "$FILENAME.bak"
curl https://covidtracking.com/api/states/daily?state=WA > $FILENAME
