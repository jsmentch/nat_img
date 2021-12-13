#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -c 1
#SBATCH --mem=8G

sub=$1

fmriprep_dir='/om4/group/gablab/data/jsmentch/ds003017/derivatives/fmriprep/'
scratch_dir='/om/scratch/Thu/jsmentch/budapest/'
high_pass='None'
low_pass='0.1'
t_r=1

module load openmind/singularity/3.6.3
#echo Submitted job for: ${sub}

for r in 1 2 3 4 5
do
    #preproc deconfound
    input_file="${fmriprep_dir}${sub}/func/${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold.dtseries.nii"
    output_dir="${scratch_dir}${sub}"
    mkdir -p "${output_dir}"
    output_file="${output_dir}${sub}/${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold_deconfound.dtseries.nii"
    input_confounds="${scratch_dir}${sub}/func/${sub}_task-movie_run-${run}_desc-confounds_timeseries.tsv"

    cmd1="singularity exec -B /om,/om2,/om4,/nobackup /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image python ./preproc_confounds.py $input_file $output_file $input_confounds"

    echo $'Command :\n'${cmd1}
    ${cmd1}
    
done
    #wb smooth
    
