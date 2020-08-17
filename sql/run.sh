#!/bin/bash -
opt="$1"
case "${opt}" in
    "j"|"js"|"jso"|"json")
        cat source.txt | ./sql_parser.py | grep -v SUCCESS | python -mjson.tool
        ;;
    *)
        cat source.txt | ./sql_parser.py
        ;;
esac
