import os.path
import numpy as np
import pandas as pd
from pathlib import Path


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

import sys

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

input_file = str(sys.argv[1])
output_file= str(sys.argv[2])
print(f'checking {input_file}')
if not Path(output_file).is_file(): # if output doesn't exist already, run it
    if os.path.isfile(input_file):
        print(f'processing {input_file}')
        img=load_img(input_file)
        img_data = img.get_fdata()
        img_data[np.isnan(img_data)] = 0
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
        np.save(f'{output_file}',degreelist)
        print(f'saved {output_file}')