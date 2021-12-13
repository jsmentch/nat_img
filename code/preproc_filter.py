import numpy as np
from nilearn.image import load_img
from nilearn.signal import clean
from os import mkdir
#from utility import var_to_nan
from pathlib import Path
import nibabel as nib
import sys

#hbn for mapper high_pass=0.009,low_pass=0.08,t_r=0.8)
input_file=str(sys.argv[1])
output_file=str(sys.argv[2])
high_pass=sys.argv[3]
low_pass=sys.argv[4]
t_r=sys.argv[5]

if not Path(output_file).is_file(): # if output doesn't exist already, run it
    if Path(input_file).is_file(): # if input doesn't exist, skip
        print(f'running {input_file}')
        brainimg = load_img(brainpath) # load func img
        func_data=np.array(brainimg.dataobj)
        #clean
        func_data_clean = clean(func_data,detrend=False,standardize=False,high_pass=high_pass,low_pass=low_pass,t_r=t_r)
        func_cln = nib.Cifti2Image(func_data_clean, brainimg.header)
        #export
        func_cln.to_filename(exportfile)
    else:
        print('input dne ',input_file)
else:
    print(f'skipping {output_file}, already ran')