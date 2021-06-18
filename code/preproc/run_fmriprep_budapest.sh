#!/bin/bash
# run script to run all subjects of budapest through fmriprep

cd /om4/group/gablab/data/jsmentch/ds003017/

subjs=($(ls sub-* -d))

cd -

for s in "${subjs[@]}"; do
    sbatch fmriprep_budapest.sh ${s:4} /om4/group/gablab/data/jsmentch/ds003017/
    echo sbatch fmriprep_budapest.sh ${s:4} /om4/group/gablab/data/jsmentch/ds003017/
done
