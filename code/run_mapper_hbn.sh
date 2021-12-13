#!/bin/bash
#SBATCH -t 0:20:00
#SBATCH --output=logs/array_%A_%a.out
#SBATCH --error=logs/array_%A_%a.err
#SBATCH --array=0-945:5
#SBATCH -c 1
#SBATCH --mem=30G
#SBATCH -p use-everything



IFS=$'\n' read -d '' -r -a lines < hbn_ru_subjects.txt
eval "$(conda shell.bash hook)"
conda activate dyneusr

for ((x=$SLURM_ARRAY_TASK_ID; x<$((SLURM_ARRAY_TASK_ID+5)); x++));
do
    sub="${lines[x]}"
    echo $sub
    input_dir='/om/scratch/Thu/jsmentch/hbn_cifti_cleaned/smoothed/filtered/'
    input_file="${input_dir}${sub}/${sub}_clean_task-movieDM_space-fsLR_den-91k_bold.dtseries.nii"
    output_dir='../outputs/mapper/HBN/'
    output_file="${output_dir}degreelist/${sub}_DM.npy"
    python mapper_hbn.py ${input_file} ${output_file}
done
