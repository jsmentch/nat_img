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

        n_scans = Y.shape[0]
        frame_times= np.arange(n_scans)

        from nilearn.glm.first_level import make_first_level_design_matrix
        design_matrix = make_first_level_design_matrix(frame_times, None,
                                  add_regs=X, hrf_model=None, drift_model=None)

    #     from nilearn.plotting import plot_design_matrix
    #     plot_design_matrix(design_matrix)

        from nilearn.glm.first_level import run_glm
        labels,results = run_glm(Y,design_matrix.values)

        from nilearn.glm.contrasts import compute_contrast
        contrast = compute_contrast(labels=labels, \
                                    regression_result=results, \
                                    con_val=np.array([1,0]).T, \
                                    contrast_type='t')
        #from analysis import plot_59k_results
        np.save(f'../outputs/glm/HCP_7T/rms/glm_{subject}_rms_z.npy',contrast.z_score())

        analysis.plot_results(contrast.z_score(),'z','59k',vertex_info,subject,feature,'HCP_7T',f'glm')

        #scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)
        #np.save(f'{temp_dir}/r2_{subject}_{feature}.npy',scores_mean)
        #np.save(f'{temp_dir}/r_{subject}_{feature}.npy',corr_mean)
        #np.save(f'{temp_dir}/w_{subject}_{feature}.npy',weights_mean)
        #analysis.plot_results(scores_mean,'r2','59k',vertex_info,subject,'as_scores',dataset,'ridgeCV')
#     elif dataset == 'merlin':
#         X,Y,vertex_info = analysis.load_data_merlin(subject,feature)
#         X = hrf_tools.apply_optimal_hrf_10hz(X,(1/1.5))
#         scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)
#         #np.save(f'{temp_dir}/r2_{subject}_{feature}.npy',scores_mean)
#         #np.save(f'{temp_dir}/r_{subject}_{feature}.npy',corr_mean)
#         #np.save(f'{temp_dir}/w_{subject}_{feature}.npy',weights_mean)
#         analysis.plot_results(scores_mean,'r2','32k',vertex_info,subject,'as_scores',dataset,'ridgeCV')
        
if __name__ == "__main__":
    main()