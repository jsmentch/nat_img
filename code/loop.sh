#!/bin/bash
while IFS= read -r line; do
    echo "Text read from file: $line"
done < "$1"