# convenience functions for working with hcp data
# 1) extend hcp_utils to work with 7T data for HCP movie viewing
# 2) load matching data from 7t movie features and cifti data

import nibabel as nb
import hcp_utils as hcp
import numpy as np
from sklearn.preprocessing import StandardScaler

# extract cortex data from image file for plotting in nilearn 
def extract_cortex(image_file):
    img=nb.load(image_file)
    img_fdata = img.get_fdata()
    vertex_info = hcp.get_HCP_vertex_info(img)
    img_fdata_cortex_data = hcp.cortex_data(img_fdata[0], fill=0, vertex_info=vertex_info)
    return img_fdata_cortex_data

# get all meshes from a folder in hcp format for plotting in nilearn
def load_meshes(example_filename=None):
    if example_filename is None:
        example_filename='/om2/user/jsmentch/data/datalad/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
    mesh59k = hcp.load_surfaces(example_filename=example_filename)
    return mesh59k

def load_data(subject,feature,n_movies):
    # Inputs: subject = HCP id eg 100610
    #         feature='mfs'
    #         n_movies is a number 1-4
    # Returns: X feature data (2D; time x feature)
    #          Y brain data (2D; time x grayordinate)
    scaler = StandardScaler()
    y_l=[]
    x_l=[]
    stim = ['tfMRI_MOVIE1_7T_AP','tfMRI_MOVIE2_7T_PA','tfMRI_MOVIE3_7T_PA','tfMRI_MOVIE4_7T_AP']
    stim_feat = ['7T_MOVIE1_CC1_v2', '7T_MOVIE2_HO1_v2', '7T_MOVIE3_CC2_v2', '7T_MOVIE4_HO2_v2']
    slice_starts = [
        [20,284, 526,734],
        [20,267,545],
        [20,221,425,649],
        [20,272,522]]
    slice_stops =  [
        [264,506,714,798],
        [247,525,795],
        [201,405,629,792],
        [252,502,777]]
    for i in np.arange(n_movies):
        #load brain image
        im_file = f'../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/{str(subject)}/MNINonLinear/Results/{stim[i]}/{stim[i]}_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries.nii'
        img = nb.load(im_file)
        img_y = img.get_fdata()
        img_y = scaler.fit_transform(img_y)
        #load feature
        feat_x = np.load(f'../sourcedata/data/HCP_7T_movie_FIX/features_hrf/{stim_feat[i]}_{feature}_hrf.npy')
        feat_x=feat_x.T
        for ii,sl in enumerate(slice_starts[i]):
            y_l.append(img_y[sl:slice_stops[i][ii],:])
            x_l.append(feat_x[sl:slice_stops[i][ii],:])
    Y=np.vstack(y_l)
    X=np.vstack(x_l)
    X = scaler.fit_transform(X)
    return X,Y