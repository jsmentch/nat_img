import nilearn as nl
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import glob
import os
import numpy as np
import seaborn as sns
sns.set("paper", "white")
import sys

#%matplotlib inline

from nilearn import plotting
import hcp_utils as hcp
import nibabel as nb
# from plotting import decompose_dscalar, plot_dscalar
import matplotlib as mpl
import matplotlib.pyplot as plt
import analysis
import utility
mpl.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

sub=str(sys.argv[1])

data_type='dtseries'
n_splits=2
cleanpath='../sourcedata/data/cneuromod/brain/friends_clean/'
# subject_flist = list(os.walk(cleanpath))[0][1]
# for sub in subject_flist:
sub_folder=f'../sourcedata/data/cneuromod/brain/friends_clean/{sub}/'
for ses_folder in glob.glob(f'{sub_folder}*'):
    for run in glob.glob(f'{ses_folder}/*.{data_type}.nii'):
        run_file=os.path.basename(run)
        ses=run_file[7:14]
        task=run_file[20:27]
        season=task[2:3]
        print(sub,ses,task)
        output_file=f'../outputs/encoding_model/cneuromod/friends/as_encoding/{sub}_{ses}_{task}'

        if os.path.exists(f'{output_file}_weights.npy'):
            print(f'found {output_file}, skipping')
        else:
            try:
                img = nb.load(f'{run}')
                Y = img.get_fdata()
    #                 scaler = StandardScaler()
    #                 Y = scaler.fit_transform(Y)
                X_as = np.load(f'../sourcedata/data/cneuromod/features/s{season}/s{season}friends_{task}_as_scores.npy')
                X= utility.downsample(X_as, Y.shape[0])
                # scaler = StandardScaler()
                # X = scaler.fit_transform(X)
                #X.shape
                X=analysis.model_FIR(X)
                X = X[6:] #remove the first 6 TRs
                Y = Y[6:]
                scores_mean,corr_mean,weights_mean=analysis.simple_ridgeCV(X,Y,n_splits)
                np.save(f'{output_file}_scores.npy', scores_mean, allow_pickle=True)
                np.save(f'{output_file}_weights.npy', weights_mean, allow_pickle=True)
            except:
                print('something went wrong, skipping')

            #analysis.plot_results(scores_mean,'r2','32k',vertex_info=None,subject=sub,feature='as_scores',dataset='friends_as_encoding',title=f'RidgeCV_FIR_{task}')