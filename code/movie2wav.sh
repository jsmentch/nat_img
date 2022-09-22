#!/bin/bash
# Converting movie files in dir1 to wav files in dir2 with ffmpeg
#usage:
# ./movie2wav.sh '../inputs/data/HCP_7T_movie_FIX/stimuli/hcp-7T_Movies/movie/unzip/Post_20140821_version/*' \
#'../inputs/data/HCP_7T_movie_FIX/stimuli/'
echo "convert movie file to wav file in dir2 with ffmpeg"
echo "files = " $1
echo "dir2 = " $2

for filename in $1; do
    b=$(basename "$filename" | cut -d. -f1)
    echo "converting " $b" to "$2$b'.wav'
    ffmpeg -i $filename -ac 1 -ar 16000 $2$b'.wav'
done
