#!/bin/bash

# Submit subjects to be run through fmriprep. Each subject
# will be run as a separate job, but all jobs will share the
# same JOBID, only will differentiate by their array number.
# Example output file: slurm-<JOBID>_<ARRAY>.out

# Usages:
# - specify specific subjects to run:

# bash submit_job_array.sh sub-MIND3036 sub-MIND5099 sub-MIND5094

# - run all subjects in project base:

# bash submit_job_array.sh


subjs=$@

base=/om4/group/gablab/data/HBN/

if [[ $# -eq 0 ]]; then
    # first go to data directory, grab all subjects,
    # and assign to an array
    pushd $base
    # including pilots
    subjs=($(ls sub-* -d))
    # excluding pilots
    #subjs=($(ls sub-leap[0-9]* -d))
    popd
fi


# take the length of the array
# this will be useful for indexing later
len=$(expr ${#subjs[@]} - 1) # len - 1

echo Spawning ${#subjs[@]} sub-jobs.

sbatch --array=0-$len%100 $base/code/fmriprep_movie/ss_fmriprep_DM.sh $base ${subjs[@]}
