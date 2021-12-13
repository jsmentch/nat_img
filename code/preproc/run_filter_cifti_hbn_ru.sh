#!/bin/bash
#SBATCH -t 2:00:00
#SBATCH -c 1
#SBATCH --mem=10G

cmd1="module load openmind/singularity/3.6.3"
cmd2="singularity exec -B /om,/om2,/om4,/nobackup,/nese /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image python ./filter_cifti_hbn_ru.py $1 $2"

#cmd="singularity shell -B /om,/om2,/om4,/nobackup,/nese /om2/user/jsmentch/projects/nat_img/.datalad/environments/analysis/image"


#echo Submitted job for: ${s}
echo $'Command :\n'${cmd1}
${cmd1}

echo $'Command :\n'${cmd2}
${cmd2}
which python
pwd