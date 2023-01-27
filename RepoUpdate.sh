#!/bin/bash
# Perform a git pull on all directories that are one directory below the organizing directories.

find . -mindepth 2 -maxdepth 2 -type d -print -exec git -C {} pull \;
