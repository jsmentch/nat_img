#!/bin/bash

WORKPATH="/nobackup/scratch/Mon/jsmentch/hbn_cifti_cleaned/smoothed/"
cd $WORKPATH

OUTPATH="/nobackup/scratch/Mon/jsmentch/hbn_cifti_cleaned/smoothed/parcellated/"
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
        wb_command -cifti-parcellate \
        $ss \
        "../sourcedata/data/parcellations/Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.59k_fs_LR.dlabel.nii" \
        COLUMN
        $OUTPATH$ss
    done
done
