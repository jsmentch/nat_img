#!/bin/bash
# given a subject id and feature string, run datalad containers-run the encoding model python script
#inputs: subject id (str), feature name (str)
#usage: ./run_datalad_run_encoding_model.sh 100610 as_scores

echo "running datalad containers-run on the encoding model python script"
echo "subject = " $1
echo "feature = " $2

while IFS= read -r sub; do
    FILE="../outputs/figures/HCP_7T/ridgeCV_${sub}_$2_r2.png"
    if test -e "$FILE"; then
        echo "$FILE exists, skipping."
    else
        echo "$FILE does not exist."
        echo "running ${sub} $2"
        datalad containers-run -m "run ridgecv subject $sub" \
        --container-name analysis \
        -i "../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/$sub/MNINonLinear/Results/*/*" \
        -i "../sourcedata/data/HCP_7T_movie_FIX/features/" \
        -i "../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/*" \
        -o "../outputs/figures/HCP_7T/ridgeCV_${sub}_$2_r2.png" \
        -o "../tmp/*" \
        "python ./run_encoding_model.py $sub $2"
        datalad save -m 'clean dataset after run'
    fi
done < "subjects.txt"

