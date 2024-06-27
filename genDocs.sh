#!/usr/bin/env bash
set -xe

if [ -d "docs" ] 
    then
        rm -rf docs/
fi

pycco -i ./**/*.py