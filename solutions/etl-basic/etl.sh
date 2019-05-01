#!/usr/bin/env bash

python etl-basic/stream_twitter_timed.py

echo "Completed extraction starting cleaning"

python etl-basic/analyse_twitter.py