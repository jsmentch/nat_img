#!/bin/bash
# given a feature, and dataset, run datalad containers-run the GLM python script
#inputs: subject id (str), feature name (str)
#usage: ./run_datalad_run_GLM.sh rms HCP_7T

echo "running datalad containers-run on the encoding model python script"
echo "feature = " $1
echo "dataset = " $2

title=glm

while IFS= read -r sub; do
    FILE="../outputs/figures/$2/${title}_${sub}_$1_z.png"
    if test -e "$FILE"; then
        echo "$FILE exists, skipping."
    else
        echo "$FILE does not exist."
        echo "running ${sub} $1"
        
        if [ "$2" = "HCP_7T" ]; then
            datalad containers-run -m "run $2 ${title} subject $sub" \
            --container-name analysis \
            -i "../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/$sub/MNINonLinear/Results/*/*" \
            -i "../sourcedata/data/HCP_7T_movie_FIX/features/" \
            -i "../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/*" \
            -o "../outputs/figures/HCP_7T/${title}_${sub}_$1_z.png" \
            -o "../outputs/glm/HCP_7T/rms/${title}_${sub}_$1_z.npy" \
            -o "../tmp/*" \
            "python ./run_GLM.py $sub $1 $2"
        elif [ "$2" = "merlin" ]; then
            datalad containers-run -m "run $2 ${title} subject $sub" \
            --container-name analysis \
            -i "../sourcedata/data/$2/brain/merlin_cifti_clean_smooth/${sub}_clean_smooth_task-MerlinMovie_space-fsLR_den-91k_bold.dtseries.nii" \
            -i "../sourcedata/data/merlin/features/" \
            -o "../outputs/figures/$2/${title}_${sub}_$1_r2.png" \
            -o "../tmp/*" \
            "python ./run_encoding_model.py $sub $1 $2"
        fi
        datalad save -m 'clean dataset after run'
        datalad drop "../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/$sub/MNINonLinear/Results/*/*"
    fi
done < "$2_subjects.txt"

