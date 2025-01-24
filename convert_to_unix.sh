#!/bin/bash

# Convert all files recursively from DOS to Unix
find . -type f -exec dos2unix {} \;