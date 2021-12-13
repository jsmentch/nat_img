#!/bin/bash

WORKPATH="/nobackup/scratch/Thu/jsmentch/hbn_cifti_cleaned/"
cd $WORKPATH

OUTPATH="/nobackup/scratch/Thu/jsmentch/hbn_cifti_cleaned/smoothed/"
echo "mkdir $OUTPATH"
mkdir $OUTPATH

for s in */ ;
do
    echo "mkdir $OUTPATH$s"
    mkdir "$OUTPATH$s"
    for ss in $s* ;
    do
	echo "running wb_command -cifti-smoothing"
	echo "input $ss"
	echo "output $OUTPATH$ss"
	now=$(date)
        echo "$now"
	wb_command -cifti-smoothing \
        ${ss} \
        4 4 COLUMN \
        $OUTPATH$ss \
        -left-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-L_den-32k_sphere.surf.gii \
        -right-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-R_den-32k_sphere.surf.gii
    done
done
