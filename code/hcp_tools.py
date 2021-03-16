# convenience functions for working with hcp data
# 1) extend hcp_utils to work with 7T data for HCP movie viewing
# 2) load matching data from 7t movie features and cifti data

import nibabel as nb
import hcp_utils as hcp
import numpy as np

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

def load_flatmaps_59k():
    from nilearn import surface
    from sklearn.utils import Bunch
    surf_path_msm_L = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.flat.59k_fs_LR.surf.gii'
    surf_path_msm_R = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.flat.59k_fs_LR.surf.gii'
    meshes = Bunch()
    for hemisphere, hemisphere_name, hemisphere_path in [('L', 'left', surf_path_msm_L), ('R', 'right', surf_path_msm_R)]:
        coord, faces = surface.load_surf_mesh(hemisphere_path)
        coordnew = np.zeros_like(coord)
        coordnew[:, 1] = coord[:, 0]
        coordnew[:, 2] = coord[:, 1]
        coordnew[:, 0] = 0
        coord = coordnew
        meshes['flat'+'_'+hemisphere_name] = coord, faces
    coordl, facesl = meshes['flat_left']
    coordr, facesr = meshes['flat_right']
    coordlnew = coordl.copy()
    coordlnew[:, 1] = coordl[:, 1] - 250.0
    coordrnew = coordr.copy()
    coordrnew[:, 1] = coordr[:, 1] + 250.0
    meshes['flat'] = hcp.combine_meshes( (coordlnew, facesl), (coordrnew, facesr) )
    return meshes