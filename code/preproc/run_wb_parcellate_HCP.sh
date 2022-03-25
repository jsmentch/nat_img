#!/bin/bash

FILENAME="HCP_7T_subjects.txt"
LINES=$(cat $FILENAME)

#"/nobackup/scratch/Mon/jsmentch/nat_img/sourcedata/data/budapest/brain/ds003017/derivatives/fmriprep/derivatives/cleaned"
#WORKPATH="/om4/group/gablab/data/jsmentch/ds003017/derivatives/fmriprep"
#cd $WORKPATH

for s in $LINES;
do
    for m in tfMRI_MOVIE1_7T_AP tfMRI_MOVIE2_7T_PA tfMRI_MOVIE3_7T_PA tfMRI_MOVIE4_7T_AP
    do
	par_dir=../../sourcedata/data/HCP_7T_movie_FIX/brain/parcellations/parcellated/
	mkdir -p $par_dir$s
	wb_command -cifti-parcellate \
	    ../../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/$s/MNINonLinear/Results/${m}/${m}_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries.nii \
	    ../../sourcedata/data/parcellations/Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.59k_fs_LR.dlabel.nii \
	    COLUMN \
	    $par_dir$s/sub${s}_${m}.ptseries.nii
	done
done
