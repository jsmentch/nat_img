import numpy as np
from scipy import signal
import pandas as pd
from nilearn.image import load_img
from nilearn.image import clean_img
from nilearn.image import smooth_img
from nilearn.image import index_img
from nilearn.signal import clean
from os import walk, mkdir
#from utility import var_to_nan
from pathlib import Path
import nibabel as nib
from nibabel import cifti2
import sys

with open("hbn_ru_subjects.txt") as f:
    subject_list = f.read().splitlines()

subject_list = subject_list[int(sys.argv[1]):int(sys.argv[2])]
#subject_list.reverse()

input_dir=f'/nobackup/scratch/Thu/jsmentch/hbn_cifti_cleaned/smoothed/'
output_path=f'/nobackup/scratch/Thu/jsmentch/hbn_cifti_cleaned/smoothed/filtered/'
for i,sub in enumerate(subject_list):
    print(i+int(sys.argv[1]))
    for task in ['TP', 'DM']:
        brainpath=f'{input_dir}{sub}/{sub}_clean_task-movie{task}_space-fsLR_den-91k_bold.dtseries.nii'
        export_path = f'{output_path}{sub}/'
        exportfile = Path(f'{export_path}{sub}_clean_task-movie{task}_space-fsLR_den-91k_bold.dtseries.nii')
        if not exportfile.is_file(): # if it doesn't exist already, run it
            if Path(brainpath).is_file():
                print(f'running {sub}')
                try:
                    mkdir(export_path)
                except OSError as error:
                    print(error)    
                brainimg = load_img(brainpath) # load func img
                func_data=np.array(brainimg.dataobj)
                #func_data = var_to_nan(func_data,0.5)
                #clean
                func_data_clean = clean(func_data,detrend=False,standardize=False,high_pass=0.009,low_pass=0.08,t_r=0.8)
                func_cln = nib.Cifti2Image(func_data_clean, brainimg.header)
                #export
                func_cln.to_filename(exportfile)
            else:
                print('dne',sub)
        else:
            print(f'skipping {sub}, already ran')