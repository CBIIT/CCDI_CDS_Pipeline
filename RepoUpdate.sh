#!/bin/bash
# Perform a git pull on all directories that are one directory below the organizing directories.

find . -mindepth 3 -maxdepth 3 -type d -print -exec git -C {} pull \;
