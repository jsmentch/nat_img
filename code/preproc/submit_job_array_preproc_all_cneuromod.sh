#!/bin/bash

# Submit subjects to be run through. all jobs will share the
# same JOBID, only will differentiate by their array number.
# Example output file: slurm-<JOBID>_<ARRAY>.out

# bash submit_job_array.sh 


subjs=($(ls /om2/user/jsmentch/projects/nat_img/sourcedata/data/cneuromod/friends.fmriprep/sub-0*/ses-* -d))
# excluding pilots
#subjs=($(ls sub-leap[0-9]* -d))


# take the length of the array
# this will be useful for indexing later
len=$(expr ${#subjs[@]} - 1) # len - 1

echo Spawning ${#subjs[@]} sub-jobs.

sbatch --array=0-$len%500 preproc_all.sh /om2/user/jsmentch/projects/nat_img/sourcedata/data/cneuromod/brain/friends_clean ${subjs[@]}
