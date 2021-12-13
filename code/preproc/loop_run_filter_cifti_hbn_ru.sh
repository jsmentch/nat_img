#!/bin/bash

for i in $(seq 520 10 950);
do
    sbatch ./run_filter_cifti_hbn_ru.sh ${i} $((i +10))
done

