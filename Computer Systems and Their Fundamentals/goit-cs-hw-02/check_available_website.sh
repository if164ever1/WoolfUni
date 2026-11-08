#!/bin/bash

urls=("https://google.com" "https://facebook.com" "https://twitter.com")
logfile="website_status.log"

> "$logfile"

for url in "${urls[@]}"; do
    status_code=$(curl -L -s -o /dev/null -w "%{http_code}" --max-time 5 "$url")
    if [[ "$status_code" == "200" ]]; then
        echo "$url is UP" >> "$logfile"
    else
        echo "$url is DOWN" >> "$logfile"
    fi
done

echo "Results have been