#!/bin/bash
#SBATCH -t 0:15:00
#SBATCH -c 1
#SBATCH --mem=10G
#SBATCH -p use-everything

source /om2/user/jsmentch/anaconda/bin/activate nilearn
module load openmind/hcp-workbench/1.2.3

args=($@)
subjs=(${args[@]:1})

# index slurm array to grab subject
#SLURM_ARRAY_TASK_ID=0
IN_DIR=${subjs[${SLURM_ARRAY_TASK_ID}]}
WRK_DIR=/om2/scratch/Wed/jsmentch/working
OUT_DIR=$1


# IN_DIR=$1
# WRK_DIR=$2
# OUT_DIR=$3

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
    SMOOTHED="$WRK_DIR_SES/$SUB\_$SES\_$TASK\_smooth_temp.dtseries.nii"
    if [ ! -f $SMOOTHED ]
    then
        WORKBENCH_CMD="wb_command -cifti-smoothing \
        ${F} \
        4 4 COLUMN \
        ${SMOOTHED} \
        -left-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-L_den-32k_sphere.surf.gii \
        -right-surface /om2/user/jsmentch/data/datalad/templateflow/tpl-fsLR/tpl-fsLR_hemi-R_den-32k_sphere.surf.gii"
        echo $'Command :\n'${WORKBENCH_CMD}
        ${WORKBENCH_CMD}
    else
        echo "already ran, skip"
    fi
    # cd $IN_DIR
    # echo "datalad drop the file"
    # datalad drop ${F}
    # cd ~-
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
    if [ ! -f $CLEAN ]
    then
        CLEAN_CMD="python preproc_all_confounds.py $SMOOTHED $CLEAN $CONFOUNDS"
        echo $'Command :\n'${CLEAN_CMD}
        ${CLEAN_CMD}
        # cd $IN_DIR
        # echo "datalad drop the confounds"
        # datalad drop $D1/$SUB\_$SES\_$TASK\_desc-confounds_timeseries.*
        # cd -
    else
        echo "already cleaned, skip"
    fi
    date
    
    #PARCELLATE mmp
    echo "----------------------PARCELLATE----------------------"
    date
    PARCELLATED=$OUT_DIR/$SUB/$SES/$SUB\_$SES\_$TASK\_$SPACE\_clean_mmp.ptseries.nii
    
    if [ ! -f $PARCELLATED ]
    then
        PARCEL_CMD="wb_command -cifti-parcellate \
        $CLEAN \
        /om2/user/jsmentch/projects/nat_img/sourcedata/data/parcellations/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii \
        COLUMN \
        $PARCELLATED"
        echo $'Command :\n'${PARCEL_CMD}
        ${PARCEL_CMD}
        date
    else
        echo "already parcellated, skip"
    fi
done
echo "completed!"


#n./preproc_all.sh /om2/user/jsmentch/projects/nat_img/sourcedata/data/cneuromod/friends.fmriprep/sub-01/ses-001/func/ /om2/scratch/Wed/jsmentch/scratch /om2/scratch/Wed/jsmentch/output

#./preproc_all.sh /om2/scratch/Thu/jsmentch/fmriprep_hbn100/derivatives/sub-NDARAC904DMU/ses-HBNsiteRU/func/ /om2/scratch/Wed/jsmentch/scratch /om2/scratch/Wed/jsmentch/hbn_output
