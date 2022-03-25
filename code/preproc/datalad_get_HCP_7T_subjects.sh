#!/bin/bash

FILENAME="HCP_7T_subjects.txt"
LINES=$(cat $FILENAME)

#"/nobackup/scratch/Mon/jsmentch/nat_img/sourcedata/data/budapest/brain/ds003017/derivatives/fmriprep/derivatives/cleaned"
#WORKPATH="/om4/group/gablab/data/jsmentch/ds003017/derivatives/fmriprep"
#cd $WORKPATH

for s in $LINES;
do
    datalad get /om/scratch/Tue/jsmentch/nat_img/sourcedata/data/human-connectome-project-openaccess/HCP1200/$s -n
done



