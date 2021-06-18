#!/bin/bash
#SBATCH -t 80:00:00
#SBATCH -c 8
#SBATCH --mem=25G

# script to run fmriprep on the budapest data by subject
# usage:
# sbatch fmriprep_budapest.sh {participant id} {bids dir}
# sbatch fmriprep_budapest.sh sid000025 /om4/group/gablab/data/jsmentch/ds003017/

# fmriprep singularity image
IMG=/om2/user/jsmentch/fmriprep.simg
# assign working directory
scratch=/om/scratch/Mon/$(whoami)/fmriprep
# assign BIDS directory
bids_dir=$2
# assign output directory
output_dir=${bids_dir}/derivatives

mkdir -p ${scratch}
# mkdir -p "${base}/derivatives"
mkdir -p ${output_dir}

s=$1

module add openmind/singularity/3.6.3

cmd="singularity run --cleanenv -B /om2 -B ${scratch}:/workdir -B ${bids_dir} $IMG \
${bids_dir} ${output_dir} \
participant \
-w /workdir \
--participant-label ${s} \
--cifti-output \
--nthreads 8 \
--output-spaces MNI152NLin6Asym:res-2 \
--resource-monitor \
--skip_bids_validation \
--omp-nthreads 8 \
--mem_mb 24000
--fs-license-file /om2/user/jsmentch/data/freesurfer_license.txt"


echo Submitted job for: ${s}
echo $'Command :\n'${cmd}
${cmd}
