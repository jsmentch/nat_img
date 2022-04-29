#!/bin/bash
cd /om2/user/jsmentch/projects/nat_img/sourcedata/data/merlin/brain/merlin_cifti_clean_smooth
for filename in /om2/user/jsmentch/projects/nat_img/sourcedata/data/merlin/brain/merlin_cifti_clean_smooth/*; do
    wb_command -cifti-parcellate \
        $filename \
        /om2/user/jsmentch/projects/nat_img/sourcedata/data/parcellations/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii \
        COLUMN \
        ../parcellated_$(basename "$filename" .dtseries.nii).ptseries.nii
done
