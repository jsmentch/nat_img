# convenience functions for working with hcp data
#
# specifically extend hcp_utils to work with 7T data 

import nibabel as nb
import hcp_utils as hcp

def extract_cortex(image_file):
    img=nb.load(image_file)
    img_fdata = img.get_fdata()
    vertex_info = hcp.get_HCP_vertex_info(img)
    img_fdata_cortex_data = hcp.cortex_data(img_fdata[0], fill=0, vertex_info=vertex_info)
    return img_fdata_cortex_data

def load_meshes(example_filename):
    mesh59k = hcp.load_surfaces(example_filename=example_filename)
    return mesh59k