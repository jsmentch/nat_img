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

from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr

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

clean_path = '/nobackup/scratch/Mon/jsmentch/nat_img/sourcedata/data/budapest/brain/ds003017/derivatives/fmriprep/derivatives/cleaned/smoothed/'
subject_flist = list(walk(clean_path))[0][2:][0]
#subject_flist

#method to find the index of nearest value in an array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx,array[idx]

segment_lengths = []
for r in np.arange(1,6):
    run=f'sub-sid000055_run{r}_clean_smooth_space-fsLR_den-91k_bold.dtseries.nii'
    img = load_img(f'{clean_path}{run}')
    segment_lengths.append(img.shape[0])
    
optic_flow_list = []
for i,r in enumerate(np.arange(2,7)):
    optic_flow = pd.read_pickle(f'../sourcedata/data/budapest/features/budapest_part{r}_optic_flow_4.pkl')
    #plt.plot(optic_flow['total_flow'])

    flow = np.array(optic_flow.total_flow.tolist())
    onset = np.array(optic_flow.onset.tolist())

    flow_10hz = np.zeros(segment_lengths[int(r)-2])

    # downsample  with 1d max pooling essentially. We take the max because we don't want to miss a spike/peak
    previous_ind=0
    for i,f in enumerate(flow_10hz):
        t=i #i/10 for 10hz
        nearest_ind,nearest_val = find_nearest(onset, t)
        flow_bin = np.append( flow[previous_ind:nearest_ind]  , 0 )
        flow_10hz[i] = max(flow_bin)
        previous_ind = nearest_ind
    optic_flow_list.append(flow_10hz)
    
    
clean_path = '/nobackup/scratch/Mon/jsmentch/nat_img/sourcedata/data/budapest/brain/ds003017/derivatives/fmriprep/derivatives/cleaned/smoothed/'
subject_flist = list(walk(clean_path))[0][2:][0]

for s in subject_flist:
    #print(f'working on sub {sub} run {run}')
    sub = s[0:13]
    run = s[17]
    print(f'working on sub {sub} run {run}')
    flow = optic_flow_list[int(run)-1]
    img = load_img(f'{clean_path}{s}')
    img_data = img.get_fdata()
    img_data[np.isnan(img_data)] = 0
    
    data = img_data
    mapper = km.KeplerMapper(verbose=1)
    projected_data = mapper.fit_transform(data, projection=umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1)) #umap default
    #projected_data = mapper.fit_transform(data, projection=TSNE(2))
    graph = mapper.map(projected_data, data, clusterer=optimize_dbscan(data, k=3, p=100.0))
    '''
    fig, axes = visualize_mapper_stages(data, np.arange(data.shape[0]), lens=projected_data, graph=graph, cover=mapper.cover, layout="spectral")
    fig.patch.set_facecolor('xkcd:white')
    plt.savefig(f'../outputs/mapper/budapest{run}_{sub}.png')
    plt.close()
    '''

    graph_nx = km.adapter.to_nx(graph)

    degrees=graph_nx.degree

    degreelist = np.zeros(segment_lengths[int(run)-1])
    nodes = graph['nodes']
    for node in list(graph['nodes']):
        for point in nodes[node]:
            if degreelist[point]<degrees[node]:
                degreelist[point]=degrees[node]
    
    pr,_ = pearsonr(flow/max(flow), degreelist/max(degreelist))
    #sr,_ = spearmanr(flow_10hz/max(flow_10hz), degreelist/max(degreelist))
    
    np.save(f'../outputs/mapper/degree/budapest{run}_{sub}_umap.npy', degreelist)
    '''                
    plt.figure(figsize=(20, 5),facecolor='white')
    plt.plot(flow/max(flow),label='optic flow')
    plt.plot(degreelist/max(degreelist),label = 'degree',c='r')
    plt.xlabel('normalized value')
    plt.ylabel('seconds')
    plt.legend()
    plt.title(f'Budapest part 1, r={pr:.3f} umap nn=15 md=0.1')
    plt.savefig(f'../outputs/mapper/budapest{run}_{sub}_degree.png')
    plt.close()
    '''
