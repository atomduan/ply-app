#!/bin/bash -
rm -f *.pyc parsetab.py parser.out *.class
cat source.txt | ./sql_parser.py
