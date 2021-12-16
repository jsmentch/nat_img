#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -c 1
#SBATCH --mem=8G
#SBATCH --output=logs/array_%A_%a.out
#SBATCH --error=logs/array_%A_%a.err

sub=$1

smoothed_dir='/om/scratch/Thu/jsmentch/budapest_smoothed/'
scratch_dir='/om/scratch/Thu/jsmentch/budapest_smoothed/cleaned/'

cd /om2/user/jsmentch/projects/nat_img/code

module load openmind/singularity/3.6.3
#echo Submitted job for: ${sub}

for r in 1 2 3 4 5
do
    #preproc remove confounds
    input_file="${smoothed_dir}${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold.dtseries.nii"
    output_dir="${scratch_dir}"
    output_file="${output_dir}${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold_deconfound.dtseries.nii"
    input_confounds="/om4/group/gablab/data/jsmentch/ds003017/derivatives/fmriprep/${sub}/func/${sub}_task-movie_run-${r}_desc-confounds_timeseries.tsv"
    cmd1="singularity exec -B /om,/om2,/om4,/nobackup /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image python ./preproc_confounds.py $input_file $output_file $input_confounds"

    echo $'Command :\n'${cmd1}
    ${cmd1}
    
done
    #wb smooth
    
