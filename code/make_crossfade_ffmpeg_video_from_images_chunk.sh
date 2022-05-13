#!/bin/bash
# edited by jsmentch 5/10/22
# downloaded from https://gist.github.com/anguyen8/d0630b6aef6c1cd79b9a1341e88a573e#file-make_crossfade_ffmpeg_video_from_images-sh
#
# Anh Nguyen <anh.ng8@gmail.com>
# 2016-04-30
# MIT License

# This script takes in images from a folder and make a crossfade video from the images using ffmpeg.
# Make sure you have ffmpeg installed before running.

# The output command looks something like the below, but for as many images as you have in the folder.
# See the answer by LordNeckbeard at:
# http://superuser.com/questions/833232/create-video-with-5-images-with-fadein-out-effect-in-ffmpeg/1071748#1071748
#
#
# ffmpeg \
# -loop 1 -t 1 -i 001.png \
# -loop 1 -t 1 -i 002.png \
# -loop 1 -t 1 -i 003.png \
# -loop 1 -t 1 -i 004.png \
# -loop 1 -t 1 -i 005.png \
# -filter_complex \
# "[1:v][0:v]blend=all_expr='A*(if(gte(T,0.5),1,T/0.5))+B*(1-(if(gte(T,0.5),1,T/0.5)))'[b1v]; \
# [2:v][1:v]blend=all_expr='A*(if(gte(T,0.5),1,T/0.5))+B*(1-(if(gte(T,0.5),1,T/0.5)))'[b2v]; \
# [3:v][2:v]blend=all_expr='A*(if(gte(T,0.5),1,T/0.5))+B*(1-(if(gte(T,0.5),1,T/0.5)))'[b3v]; \
# [4:v][3:v]blend=all_expr='A*(if(gte(T,0.5),1,T/0.5))+B*(1-(if(gte(T,0.5),1,T/0.5)))'[b4v]; \
# [0:v][b1v][1:v][b2v][2:v][b3v][3:v][b4v][4:v]concat=n=9:v=1:a=0,format=yuv420p[v]" -map "[v]" out.mp4

#----------------------------------------------------------------
# SETTINGS
input_dir="/om2/user/jsmentch/projects/nat_img/outputs/figures/budapest_pre_qual/budapest"  # Replace this by a path to your folder /path/to/your/folder
scratch_dir="/om2/scratch/Thu/jsmentch/ffmpeg_scratch"

mkdir -p $scratch_dir
chunk_size=100                        # Replace this by a number of images per chunk
c=0
ls ${input_dir}/plot_gif*_sid000005_raw_raw.png | while readarray -tn ${chunk_size} chunkfiles && ((${#chunkfiles[@]}))
do
    ((c+=1))
    echo "outer loop chunk $c"
    echo "chunk files: ${chunkfiles[@]}"
    echo "n_files chunk length: ${#chunkfiles[@]}"
    n_files=${#chunkfiles[@]} 
    echo "n_files in chunk = $n_files"
    files=`ls ${input_dir}/plot_gif*_sid000005_raw_raw.png | head -${n_files}`  # Change the file type to the correct type of your images
    files=${chunkfiles[@]}
    echo "files= $files"
    output_file='${scratch_dir}/budapest_chunk_${c}.mp4'           # Name of output video
    crossfade=1                     # Crossfade duration between two images
    #----------------------------------------------------------------

    # Making an ffmpeg script...
    input=""
    filters=""
    #output="[0:v]"
    output=""
    
    i=0
    
    for f in ${files}; do
	echo "~~~~~~~~~~~~${f}~~~~~~~~~~~~~~~"
	input+=" -loop 1 -t 1 -i $f"
	
	next=$((i+1))
	if [ "${i}" -ne "$((n_files-1))" ]; then
	    filters+=" [${next}:v][${i}:v]blend=all_expr='A*(if(gte(T,${crossfade}),1,T/${crossfade}))+B*(1-(if(gte(T,${crossfade}),1,T/${crossfade})))'[b${next}v];"
	fi
	
	if [ "${i}" -gt "0" ]; then
	    #output+="[b${i}v][${i}:v]"
	    output+="[b${i}v]"
	fi
	
	i=$((i+1))
    done
    #if (($n_files < $chunk_size)); then
    if (($n_files < (($chunk_size +1)) )); then
	output+="[$((i-1)):v]"
	output+="concat=n=$((i)):v=1:a=0,format=yuv420p[v]\" -map \"[v]\" ${output_file}"
    else
	output+="concat=n=$((i-1)):v=1:a=0,format=yuv420p[v]\" -map \"[v]\" ${output_file}"
    fi
    #script="ffmpeg -hide_banner -loglevel error -threads 1 ${input} -filter_complex \"${filters} ${output}"
    script="< /dev/null ffmpeg -threads 1 ${input} -filter_complex \"${filters} ${output}"
    echo ${script}
    
    # Run it
    eval "${script}"
done

printf "file '%s'\n" ${scratch_dir}/*.mp4 > ${scratch_dir}/mp4list.txt
ffmpeg -f concat -safe 0 -i ${scratch_dir}/mp4list.txt -c copy ${input_dir}/output.mp4
