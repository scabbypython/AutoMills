#!/bin/bash

for py_file in $(find ../one -name *.py)
do
    python $py_file
done