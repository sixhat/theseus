#!/usr/bin/env bash

for f in `find . -name "*.py" ! -name "__*"`
    do
    pycco -p $f
done

