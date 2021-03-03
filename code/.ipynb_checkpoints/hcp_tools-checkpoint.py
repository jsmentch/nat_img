# convenience functions for working with hcp data
# jsm 3/3/21
# specifically, extend hcp_utils to work with 7T data for HCP movie viewing

import nibabel as nb
import hcp_utils as hcp

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