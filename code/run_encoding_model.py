import argparse
import os
import analysis
import hrf_tools
import numpy as np
#import matplotlib
#matplotlib.rcParams['figure.figsize'] = (6, 4)
# this is run by run_datalad_run_encoding_model.sh
# "python ./run_encoding_model.py $sub $2"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", type=str, help="input subject id file")
    parser.add_argument("feature", type=str, help="which feature to use")
    parser.add_argument("dataset", type=str, help="which dataset to use")
    args = parser.parse_args()
    subject = args.subject
    feature = args.feature
    dataset = args.dataset
    print(subject,feature,dataset)
    #temp_dir = '../../tmp'
    #if not os.path.exists(temp_dir):
    #    os.mkdir(temp_dir)
    if dataset == 'HCP_7T':
        n_movies=[1,2,3,4]
        X,Y,vertex_info = analysis.load_data_HCP(subject,feature,n_movies)
        X = hrf_tools.apply_optimal_hrf_10hz(X,1)
        scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)
        np.save(f'../outputs/encoding_model/HCP_7T/{feature}/ridgeCV_{subject}_{feature}_scores.npy',scores_mean)
        np.save(f'../outputs/encoding_model/HCP_7T/{feature}/ridgeCV_{subject}_{feature}_corr.npy',corr_mean)
        np.save(f'../outputs/encoding_model/HCP_7T/{feature}/ridgeCV_{subject}_{feature}_weights.npy',weights_mean)
        #np.save(f'{temp_dir}/r_{subject}_{feature}.npy',corr_mean)
        #np.save(f'{temp_dir}/w_{subject}_{feature}.npy',weights_mean)
        analysis.plot_results(scores_mean,'r2','59k',vertex_info,subject,feature,dataset,'ridgeCV')
    elif dataset == 'merlin':
        X,Y,vertex_info = analysis.load_data_merlin(subject,feature)
        X = hrf_tools.apply_optimal_hrf_10hz(X,(1/1.5))
        scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)
        #np.save(f'{temp_dir}/r2_{subject}_{feature}.npy',scores_mean)
        #np.save(f'{temp_dir}/r_{subject}_{feature}.npy',corr_mean)
        #np.save(f'{temp_dir}/w_{subject}_{feature}.npy',weights_mean)
        analysis.plot_results(scores_mean,'r2','32k',vertex_info,subject,'as_scores',dataset,'ridgeCV')
        
if __name__ == "__main__":
    main()