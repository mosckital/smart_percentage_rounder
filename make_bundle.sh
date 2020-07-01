#!/usr/bin/env sh

# store the calling path
original_path=$( pwd -P )
# cd into the script's directory
cd "$(dirname "${BASH_SOURCE[0]}")"
# clear all existing bundles
rm -r bundles
mkdir -p bundles
# copy codes into the bundle folder
cp -r rounders bundles/
# adjust __main__.py location
mv bundles/rounders/__main__.py bundles
# create the zip file
cd bundles
zip -r csv_rounder.zip * -x '*__pycache__*'
# clean up
rm -r rounders
rm __main__.py
# return to the calling path
cd $original_path