#!/bin/bash

FILENAME="budapest_subjects.txt"
LINES=$(cat $FILENAME)

for s in $LINES;
do
    sbatch ./run_preproc_budapest.sh ${s}
done
