#!/bin/bash

for i in $(seq 320 30 350);
do
    sbatch ./run_filter_cifti_hbn_ru.sh ${i} $((i +30))
done

