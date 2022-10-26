import numpy as np
#for combine_bids_tsvs:
import pandas as pd
from pathlib import Path
import os


def plot_folder_gif(img_dir,dur):
    from PIL import Image, ImageDraw
    import os
    img_list=os.listdir(img_dir)
    img_list=img_list[1:]

    img1 = Image.open(img_dir+img_list[0])

    append_images=[]
    for i,im in enumerate(img_list[1:]):
        img2 = Image.open(img_dir+img_list[i])
        append_images.append(img2)
    img1.save(f'{img_dir}.gif', save_all=True, append_images=append_images, duration=dur, loop=0)
    
    

def var_to_nan(fdata,var_thresh):
    import numpy as np
    fdata_var=np.var(fdata,axis=0) #calculate variance
    if var_thresh==0:
        to_nan = np.where(fdata_var==var_thresh,True,False) #nan places w zero variance
    else:
        to_nan = np.where(fdata_var<var_thresh,True,False) #nan voxels w variance less than var_thresh
    fdata[:,to_nan]=float("NaN") #set to nan
    return fdata

def mask_cifti(mask,arr_in):
    #mask and array_in should be the same shape in the second dimension and in the same space
    mask_ind=np.argwhere(mask==1)[:,1]
    masked=arr_in[:,mask_ind]
    return(masked) #return a time X brainordinate array
    
def unmask_cifti(mask,arr_in):
    #unmask 1d results
    mask_ind=np.argwhere(mask==1)[:,1]
    unmasked=np.zeros( mask.shape[1] )
    unmasked[mask_ind]=arr_in[:]
    return(unmasked) 


def combine_bids_tsvs(in_dir):
    # input = a directory of .tsv files 
    # eg '/nobackup/scratch/Tue/jsmentch/fitlins/merlin/'
    # with:
        # 3 columns: onset, duration, value
        # title=feature name
    # output = a combined tsv with an additional column 'trial_type' with the feature name
    files = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]

    #first make an empty df with the columns
    df_out= pd.DataFrame(columns=['onset', 'duration', 'value', 'trial_type'])

    for f in files:
        f_base = os.path.splitext(f)[0]
        df=pd.read_csv(f'{in_dir}/{f}', sep='\t')
        df['trial_type'] = pd.Series([f_base for x in range(len(speech.index))])
        df_out = df_out.append(df)

    df_out.to_csv(f'{in_dir}combined.tsv', sep="\t")

    

def downsample(array, npts):
    from scipy.interpolate import interp1d
    interpolated = interp1d(np.arange(len(array)), array, axis = 0, fill_value = 'extrapolate')
    downsampled = interpolated(np.linspace(0, len(array), npts))
    return downsampled