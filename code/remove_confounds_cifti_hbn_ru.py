import numpy as np
from scipy import signal
import pandas as pd
from nilearn.image import load_img
from nilearn.image import clean_img
from nilearn.image import smooth_img
from nilearn.image import index_img
from nilearn.signal import clean
from os import walk, mkdir
from utility import var_to_nan
from pathlib import Path
import nibabel as nib
from nibabel import cifti2

with open("hbn_ru_subjects.txt") as f:
    subject_list = f.read().splitlines()
    
for sub in subject_list:
    for task in ['TP', 'DM']:
        brainpath=f'/om4/group/gablab/data/HBN/derivatives/fmriprep/{sub}/func/{sub}_task-movie{task}_space-fsLR_den-91k_bold.dtseries.nii'
        confound_path=f'/om4/group/gablab/data/HBN/derivatives/fmriprep/{sub}/func/{sub}_task-movie{task}_desc-confounds_timeseries.tsv'
        export_path = f'/nobackup/scratch/Mon/jsmentch/hbn_cifti_cleaned/{sub}'
        exportfile = Path(f'{export_path}/{sub}_clean_task-movie{task}_space-fsLR_den-91k_bold.dtseries.nii')
        if not exportfile.is_file(): # if it doesn't exist already, run it
            if Path(brainpath).is_file():
                print(f'running {sub}')
                try:
                    mkdir(export_path)
                except OSError as error:
                    print(error)    
                #load confounds
                data = pd.read_csv(confound_path, sep='\t')
                try:
                    confounds=data[['global_signal', 'csf', 'white_matter', 'framewise_displacement', 'a_comp_cor_00', 'a_comp_cor_01', 'a_comp_cor_02', 'a_comp_cor_03', 'a_comp_cor_04', 'a_comp_cor_05', 'rot_x','rot_y','rot_z','trans_x','trans_y','trans_z']].to_numpy()
                except:
                    continue
                confounds = np.nan_to_num(confounds)
                #confounds=data[['global_signal', 'csf', 'white_matter','rot_x','rot_y','rot_z','trans_x','trans_y','trans_z']].to_numpy()
                #load brain data
                brainimg = load_img(brainpath) # load func img
                func_data=np.array(brainimg.dataobj)
                func_data = var_to_nan(func_data,0.5)
                #clean
                #func_cln = clean_img(func,detrend=True,confounds=confounds,low_pass=0.1,t_r=1.5)
                func_data_clean = clean(func_data,detrend=True,standardize='zscore',confounds=confounds,low_pass=0.1,t_r=0.8)
                func_cln = nib.Cifti2Image(func_data_clean, brainimg.header)
                #export
                func_cln.to_filename(exportfile)
            else:
                print('dne',sub)
        else:
            print(f'skipping {sub}, already ran')
