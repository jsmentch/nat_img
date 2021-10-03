from os import walk
import numpy as np
import pandas as pd

#from nilearn.datasets import fetch_haxby
from nilearn.input_data import NiftiMasker

from kmapper import KeplerMapper, Cover
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN

import nilearn as nl
from nilearn.image import load_img

from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN

from dyneusr import DyNeuGraph
from dyneusr.tools import visualize_mapper_stages

import kmapper as km
from kmapper import jupyter # Creates custom CSS full-size Jupyter screen
import umap
import sklearn

#from dyneusr
from sklearn.cluster import DBSCAN
def optimize_dbscan(X, k=3, p=100.0, min_samples=2, **kwargs):
    """ Get dbscan based on eps determined by data.
    """
    eps = optimize_eps(X, k=k, p=p)
    dbscan = DBSCAN(
        eps=eps, min_samples=min_samples, 
        metric='minkowski', p=2, leaf_size=15,
        **kwargs
        )
    return dbscan

def optimize_eps(X, k=3, p=100.0, **kwargs):
    """ Get optimized value for eps based on data. 
    Parameters
    ----------
    k: int
        * calculate distance to k-th nearest neighbor
    p: float 
        * threshold percentage to keep
    Returns
    -------
    eps: float
        * a parameter for DBSCAN
    """
    from sklearn.neighbors import KDTree

    # Use 'minkowski', p=2 (i.e. euclidean metric)
    tree = KDTree(X, metric='minkowski', p=2, leaf_size=15)

    # Query k nearest-neighbors for X, not including self
    dist, ind = tree.query(X, k=k+1)

    # Find eps s.t. % of points within eps of k nearest-neighbor 
    eps = np.percentile(dist[:, k], p)
    return eps

clean_path = '/nobackup/scratch/Mon/jsmentch/hbn_cifti_cleaned/smoothed/'
subject_flist = list(walk(clean_path))[0][1]
length = len(subject_flist)
middle_index = length//2
subject_flist= subject_flist[:middle_index]
subject_flist.reverse()


import os.path
output_dir='../outputs/mapper/HBN/'
for s in subject_flist:
    sub = s[-16:]
    print(sub)
    file=f'{clean_path}{s}/{sub}_clean_task-movieDM_space-fsLR_den-91k_bold.dtseries.nii'
    print(file)
    if os.path.isfile(file):
        img=load_img(file)
        img_data = img.get_fdata()
        img_data[np.isnan(img_data)] = 0
        title = 'wb_umap_HBN_'
        data = img_data
        mapper = km.KeplerMapper()
        # Fit to and transform the data
        #lens
        #projected_data = mapper.fit_transform(data, projection=TSNE(2), distance_matrix=True)
        #projected_data = mapper.fit_transform(data, projection=umap.UMAP(n_components=2))
        projected_data = mapper.fit_transform(data, projection=TSNE(2))
        # Create dictionary called 'graph' with nodes, edges and meta-information
        #graph = mapper.map(projected_data, data, clusterer=sklearn.cluster.DBSCAN(eps=0.5,min_samples=3))
        graph = mapper.map(projected_data, data, clusterer=optimize_dbscan(data, k=3, p=100.0))
        graph_nx = km.adapter.to_nx(graph)
        degrees=graph_nx.degree
        degreelist = np.zeros(data.shape[0])
        nodes = graph['nodes']
        for node in list(graph['nodes']):
            for point in nodes[node]:
                if degreelist[point]<degrees[node]:
                    degreelist[point]=degrees[node]
        np.save(f'{output_dir}degreelist/{sub}.npy',degreelist)
