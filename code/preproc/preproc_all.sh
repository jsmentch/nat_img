#!/bin/bash
# #SBATCH -t 1:00:00
# #SBATCH -c 1
# #SBATCH --mem=8G
# #SBATCH --output=logs/array_%A_%a.out
# #SBATCH --error=logs/array_%A_%a.err

source /om2/user/jsmentch/anaconda/bin/activate nilearn
module load openmind/hcp-workbench/1.2.3

IN_DIR=$1
WRK_DIR=$2
OUT_DIR=$3

SPACE="space-fsLR_den-91k_bold"
mkdir -p $WRK_DIR
mkdir -p $OUT_DIR

#FIND ALL DTSERIES IN THE FOLDER
for F in $(find $IN_DIR -name "*bold.dtseries.nii"); do
    printf "\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
    printf " ~ ~ ~ ~ ~ ~  processing $F \n"
    printf "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n\n"
    
    #SETUP VARIABLES
    F_BASE=$(basename "$F")
    #F_BASE=${F_BASE/./_}
    D1=$(dirname "$F")
    func=$(basename "$D1")
    D2=$(dirname "$D1")
    SES=$(basename "$D2")
    D3=$(dirname "$D2")
    SUB=$(basename "$D3")
    F_BASE_BASE=${F_BASE%.*.*} # filename with no extensions
    TASK="${F_BASE_BASE#*$SUB\_$SES\_}"
    TASK="${TASK%%_$SPACE}"
    WRK_DIR_SES=$WRK_DIR/$SUB/$SES
    mkdir -p $WRK_DIR_SES
    # cd $IN_DIR
    # echo "datalad get the file"
    # datalad get ${F}
    # cd ~-
    mkdir -p $OUT_DIR/$SUB/$SES

    #SMOOTH with workbench
    echo "----------------------SMOOTHING----------------------"
    date
    SMOOTHED="$WRK_DIR_SES/smooth_temp.dtseries.nii"
    WORKBENCH_CMD="wb_command -cifti-smoothing \
    ${F} \
    4 4 COLUMN \
    ${SMOOTHED} \
    -left-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-L_den-32k_sphere.surf.gii \
    -right-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-R_den-32k_sphere.surf.gii"
    echo $'Command :\n'${WORKBENCH_CMD}
    ${WORKBENCH_CMD}
    cd $IN_DIR
    echo "datalad drop the file"
    datalad drop ${F}
    cd ~-
    date
    
    #REMOVE CONFOUNDS with nilearn
    echo "----------------------CONFOUNDS----------------------"
    date
    CONFOUNDS=$D1/$SUB\_$SES\_$TASK\_desc-confounds_timeseries.tsv
    # cd $IN_DIR
    # echo "datalad get the confounds"
    # datalad get $D1/$SUB\_$SES\_$TASK\_desc-confounds_timeseries.*
    # cd -
    CLEAN=$OUT_DIR/$SUB/$SES/$SUB\_$SES\_$TASK\_$SPACE\_clean.dtseries.nii
    CLEAN_CMD="python preproc_all_confounds.py $SMOOTHED $CLEAN $CONFOUNDS"
    echo $'Command :\n'${CLEAN_CMD}
    ${CLEAN_CMD}
    cd $IN_DIR
    echo "datalad drop the confounds"
    datalad drop $D1/$SUB\_$SES\_$TASK\_desc-confounds_timeseries.*
    cd -
    date
    
    #PARCELLATE mmp
    echo "----------------------PARCELLATE----------------------"
    date
    PARCELLATED=$OUT_DIR/$SUB/$SES/$SUB\_$SES\_$TASK\_$SPACE\_clean_mmp.ptseries.nii
    PARCEL_CMD="wb_command -cifti-parcellate \
    $CLEAN \
    /om2/user/jsmentch/projects/nat_img/sourcedata/data/parcellations/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii \
    COLUMN \
    $OUTPATH$ss"
    echo $'Command :\n'${PARCEL_CMD}
    ${CLEAN_CMD}
    date
done
echo "completed!"


#./preproc_all.sh /om2/user/jsmentch/projects/nat_img/sourcedata/data/cneuromod/friends.fmriprep/sub-01/ses-001/func/ /om2/scratch/Wed/jsmentch/scratch /om2/scratch/Wed/jsmentch/output

#./preproc_all.sh /om2/scratch/Thu/jsmentch/fmriprep_hbn100/derivatives/sub-NDARAC904DMU/ses-HBNsiteRU/func/ /om2/scratch/Wed/jsmentch/scratch /om2/scratch/Wed/jsmentch/scratch


# cd /om2/user/jsmentch/projects/nat_img/code

# module load openmind/singularity/3.9.5
# #echo Submitted job for: ${sub}

# #preproc remove confounds
# input_file="${smoothed_dir}${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold.dtseries.nii"
# output_dir="${scratch_dir}"
# output_file="${output_dir}${sub}_task-movie_run-${r}_space-fsLR_den-91k_bold_deconfound.dtseries.nii"
# input_confounds="/om4/group/gablab/data/jsmentch/ds003017/derivatives/fmriprep/${sub}/func/${sub}_task-movie_run-${r}_desc-confounds_timeseries.tsv"
# cmd1="singularity exec -B /om,/om2,/om4,/nobackup /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image python ./preproc_confounds.py $input_file $output_file $input_confounds"

# echo $'Command :\n'${cmd1}
# ${cmd1}