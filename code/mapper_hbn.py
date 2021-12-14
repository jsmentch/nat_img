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

"""
Calculates each node's coreness value, as described by Stephen Borgatti
"""

__author__ = """Alex Levenson (alex@isnontinvain.com)"""

#	(C) Reya Group: http://www.reyagroup.com
#	Alex Levenson (alex@isnotinvain.com)
#	BSD license.

__all__ = ["triadic_census"]



from scipy import optimize
from scipy.stats.stats import pearsonr
import numpy
import networkx as nx


def core_correlation(A,C):
	"""
	returns the pearson correlation between A and
	the ideal coreness matrix created from C
	
	A: ajacency matrix (valued or unvalued)
	C: 1D matrix representing the coreness of each node
	"""
	cMat = numpy.matrix(C)
	Cij = numpy.multiply(cMat,cMat.transpose())
	return pearsonr(A.flat,Cij.flat)
	
def _core_fitness(C,*args):
	"""
	converts coreCorrelation(A,C) to something useable
	with scipy.optimize (which aims to MINIMIZE a function)
	Need to express highest positive correlation as function
	to be minimized
	"""
	return core_correlation(args[0],C)[0] * -1.0


def coreness(G,return_correlation=False):
	"""
	Calculates each node's coreness value, as described by Stephen Borgatti
	
	Coreness describes to what degree a node is a member of the graph's core
	Parameters
	----------
	G : graph
		A networkx graph
	
	return_correlation : whether to return the final correlation to the ideal core / periphery structure
	Returns
	-------
	census : dictionary
			 Dictionary with nodes as keys and coreness as values
			 *if return_correlation is set, then returns a tuple (dict with nodes as keys and coreness as values,correlation)* 
	Refrences
	---------	
	.. [1] Models of Core/Periphery Structures
	   Stephen P. Borgatti, Boston College
	   http://dx.doi.org/10.1016/S0378-8733(99)00019-2
	"""
	
	A = nx.to_numpy_matrix(G)
	
	# need a starting point for the optimizer, for now using a random starting point.
	initialC = numpy.random.rand(len(A)) # can we do better? Is it important? Maybe use constraint or centrality? 
	
	# run a bfgs optimizers that optimizes correlation between calculated coreness scores and the ideal model
	best = optimize.fmin_l_bfgs_b(_core_fitness, initialC,args=(A,None),approx_grad=True,bounds=[(0.0,1.0) for i in range(len(A))])	
	
	part = {}
	for node in G:
		part[node] = best[0][list(G.nodes()).index(node)]
	# return correlation to ideal if return_correlation is set
	if return_correlation: 
		return part,best[1] * -1.0
	return part


input_file = str(sys.argv[1])
output_file= str(sys.argv[2])
output_file2= str(sys.argv[3])

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
        cover = km.Cover(n_cubes=30,perc_overlap=0.1)
        graph = mapper.map(projected_data, data, cover=cover, clusterer=optimize_dbscan(data, k=3, p=100.0))
        graph_nx = km.adapter.to_nx(graph)
        degrees=graph_nx.degree
        degreelist = np.zeros(data.shape[0])
        nodes = graph['nodes']
        for node in list(graph['nodes']):
            for point in nodes[node]:
                if degreelist[point]<degrees[node]:
                    degreelist[point]=degrees[node]
        np.save(f'{output_file}',degreelist)
        
        
        cs=coreness(graph_nx)
        corenesslist = np.zeros(data.shape[0])
        nodes = graph['nodes']
        for node in list(graph['nodes']):
            for point in nodes[node]:
                if corenesslist[point]<cs[node]:
                    corenesslist[point]=cs[node]
        np.save(f'{output_file2}',corenesslist)
        
        
        print(f'saved {output_file}')