import analysis
import hrf_tools
import matplotlib
matplotlib.rcParams['figure.figsize'] = (6, 4)
subject=100610
feature='as_scores'
n_movies=[1]
X,Y,vertex_info = analysis.load_data_HCP(subject,feature,n_movies)
# X = hrf_tools.apply_optimal_hrf_10hz(X,1)
# scores_mean,corr_mean,weights_mean = analysis.simple_ridgeCV(X,Y)

analysis.plot_results(Y[0,:],'r2','59k',vertex_info,100610,'as_scores','HCP_7T','ridgeCV')
