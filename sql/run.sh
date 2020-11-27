#!/bin/bash -
opt="$1"
case "${opt}" in
    "j" | "js" | "jso" | "json")
        cat ./resource/source.txt | ./sql_parser.py | grep -v SUCCESS | python -mjson.tool
        ;;
    *)
        cat ./resource/source.txt | ./sql_parser.py
        ;;
esac
