#!/bin/bash
#SBATCH -t 1:30:00
#SBATCH -c 1
#SBATCH --mem=50G
# #SBATCH -p use-everything


cmd1="module load openmind/singularity/3.9.5"

cmd2="singularity exec -B /om2,/nese /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image python cneuromod_encoding.py $1"

#cmd="singularity shell -B /om,/om2,/om4,/nobackup,/nese /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image"


#echo Submitted job for: ${s}
echo $'Command :\n'${cmd1}
${cmd1}

cd /om2/user/jsmentch/projects/nat_img/code/

echo $'Command :\n'${cmd2}
${cmd2}
# cd /om2/user/jsmentch/projects/nat_img/code/
# pwd
