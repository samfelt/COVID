#! /usr/bin/env bash

FILENAME='WA-data.json'
URL='https://covidtracking.com/api/states/daily?state=WA'

curr_sha=$(shasum $FILENAME | cut -d " " -f1)
new_sha=$(curl -s $URL | shasum | cut -d " " -f1)

if [ "$curr_sha" == "$new_sha" ]; then
    echo "No new changes"
    exit
fi

mv "$FILENAME" "$FILENAME.bak"
curl -s $URL > $FILENAME
