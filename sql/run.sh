#!/bin/bash -
rm -f *.pyc parsetab.py parser.out *.class
cat source.txt | ./parser.py
