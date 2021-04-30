#!/bin/bash
# run wb_command
#inputs: subject number, movie title
#usage: ./cifti-parcellate.sh 100610 tfMRI_MOVIE1_7T_AP

echo "running wb_command -cifti-parcellate"
echo "subject = " $1
echo "feature = " $2


datalad containers-run -m "run ridgecv subject $1" \
--container-name feature-extraction \
-i "sourcedata/data/HCP_7T_movie_FIX/features/*.npy" -o "sourcedata/data/HCP_7T_movie_FIX/features_hrf/*" "python code/hrf_tools.py sourcedata/data/HCP_7T_movie_FIX/features/ sourcedata/data/HCP_7T_movie_FIX/features_hrf -d"











wb_command -cifti-parcellate "../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/$1/MNINonLinear/Results/$2/$2_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries.nii" "../sourcedata/data/parcellations/Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.59k_fs_LR.dlabel.nii" COLUMN "sub$1_$2.ptseries.nii"