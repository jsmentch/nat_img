#!/bin/bash

FILENAME="budapest_subjects.txt"
LINES=$(cat $FILENAME)


WORKPATH="/nobackup/scratch/Mon/jsmentch/nat_img/sourcedata/data/budapest/brain/ds003017/derivatives/fmriprep/derivatives/cleaned"
cd $WORKPATH

for s in $LINES;
do
    for r in 1 2 3 4 5
    do
	wb_command -cifti-smoothing \
	${s}_run${r}_clean_space-fsLR_den-91k_bold.dtseries.nii \
	4 4 COLUMN \
	smoothed/${s}_run${r}_clean_smooth_space-fsLR_den-91k_bold.dtseries.nii \
	-left-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-L_den-32k_sphere.surf.gii \
	-right-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-R_den-32k_sphere.surf.gii
    done
done
