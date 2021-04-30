import argparse
import os
import analysis
import hrf_tools
import numpy as np
#import matplotlib
#matplotlib.rcParams['figure.figsize'] = (6, 4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", type=str, help="input subkect id file")
    parser.add_argument("feature", type=str, help="which feature to use")
    args = parser.parse_args()
    subject = args.subject
    feature = args.feature
    temp_dir = '../../tmp'
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
        
    n_movies=[1]
    X,Y,vertex_info = analysis.load_data_HCP(subject,feature,n_movies)
    X = hrf_tools.apply_optimal_hrf_10hz(X,1)
    scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)
    #np.save(f'{temp_dir}/r2_{subject}_{feature}.npy',scores_mean)
    #np.save(f'{temp_dir}/r_{subject}_{feature}.npy',corr_mean)
    #np.save(f'{temp_dir}/w_{subject}_{feature}.npy',weights_mean)
    analysis.plot_results(scores_mean,'r2','59k',vertex_info,100610,'as_scores','HCP_7T','ridgeCV')

if __name__ == "__main__":
    main()