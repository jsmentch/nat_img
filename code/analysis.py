import numpy as np
import nibabel as nb
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from nilearn_plotting_custom import plot_surf
from PIL import Image
from PIL import ImageDraw
import npp
import hcp_utils as hcp
from hcp_tools import load_flatmaps_59k
from hcp_tools import load_meshes
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import resample
from sklearn.preprocessing import StandardScaler
sns.set("paper", "white")
#%matplotlib inline
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'


#make colormaps
import matplotlib.colors as mcolors
cmap = plt.cm.get_cmap('RdBu')
cmap.set_bad(color='gray')

colors = cmap(np.linspace(-1, 1, 256))
colors[128:] = np.array([26/256,255/256,26/256, 1])
colors[:128] = np.array([95/256,0,185/256, 1])

pigr = mcolors.ListedColormap(colors)
pigr_r = mcolors.ListedColormap(np.flip(colors,axis=0))

colors = cmap(np.linspace(-1, 1, 256))
colors[128:] = np.array([255/256,194/256,10/256, 1])
colors[:128] = np.array([12/256,123/256,220/256, 1])

yebl = mcolors.ListedColormap(colors)
yebl_r = mcolors.ListedColormap(np.flip(colors,axis=0))


# rcParams = np.load('rcParams.npy', allow_pickle=True)
# plt.rcParams = rcParams

def load_data_HCP(subject,feature,n_movies):
    # Inputs: subject = HCP id eg 100610
    #         feature='mfs'
    #         n_movies is a list of movie indices 1 thru 4
    # Returns: X feature data (2D; time x feature)
    #          Y brain data (2D; time x grayordinate)
    scaler = StandardScaler()
    y_l=[]
    x_l=[]
    stim = ['tfMRI_MOVIE1_7T_AP','tfMRI_MOVIE2_7T_PA','tfMRI_MOVIE3_7T_PA','tfMRI_MOVIE4_7T_AP']
    stim_feat = ['7T_MOVIE1_CC1_v2', '7T_MOVIE2_HO1_v2', '7T_MOVIE3_CC2_v2', '7T_MOVIE4_HO2_v2']
    slice_starts = [
        [20,284, 526,734],
        [20,267,545],
        [20,221,425,649],
        [20,272,522]]
    slice_stops =  [
        [264,506,714,798],
        [247,525,795],
        [201,405,629,792],
        [252,502,777]]
    for i in n_movies:
        i=i-1
        exclude_final=slice_stops[i][-1] #trim the final movie since it is in all scans
        #load brain image
        im_file = f'../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/{str(subject)}/MNINonLinear/Results/{stim[i]}/{stim[i]}_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries.nii'
        img = nb.load(im_file)
        img_y = img.get_fdata()
        img_y = scaler.fit_transform(img_y)
        #load feature
        feat_x = np.load(f'../sourcedata/data/HCP_7T_movie_FIX/features/{stim_feat[i]}_{feature}.npy')
        feat_x = resample(feat_x, img_y.shape[0], axis=0) #resample to 1hz for now 
        #feat_x=feat_x.T
        #trim final movies
        img_y = img_y[:exclude_final,:]
        feat_x = feat_x[:exclude_final,:]
        y_l.append(img_y)
        x_l.append(feat_x)
    Y=np.vstack(y_l)
    X=np.vstack(x_l)
    #X = scaler.fit_transform(X)
    vertex_info = hcp.get_HCP_vertex_info(img)
    return X,Y,vertex_info

def load_data_HCP_MMP(subject,feature,n_movies):
    # Inputs: subject = HCP id eg 100610
    #         feature='mfs'
    #         n_movies is a list of movie indices 1 thru 4
    # Returns: X feature data (2D; time x feature)
    #          Y brain data (2D; time x grayordinate)
    scaler = StandardScaler()

    y_l=[]
    x_l=[]
    stim = ['tfMRI_MOVIE1_7T_AP','tfMRI_MOVIE2_7T_PA','tfMRI_MOVIE3_7T_PA','tfMRI_MOVIE4_7T_AP']
    stim_feat = ['7T_MOVIE1_CC1_v2', '7T_MOVIE2_HO1_v2', '7T_MOVIE3_CC2_v2', '7T_MOVIE4_HO2_v2']
    slice_starts = [
        [20,284, 526,734],
        [20,267,545],
        [20,221,425,649],
        [20,272,522]]
    slice_stops =  [
        [264,506,714,798],
        [247,525,795],
        [201,405,629,792],
        [252,502,777]]
    for i in n_movies:
        i=i-1
        exclude_final=slice_stops[i][-1] #trim the final movie since it is in all scans
        #load brain image
        im_file = f'../sourcedata/data/HCP_7T_movie_FIX/brain/parcellations/parcellated/{str(subject)}/sub{str(subject)}_{stim[i]}.ptseries.nii'
        img = nb.load(im_file)
        img_y = img.get_fdata()
        img_y = scaler.fit_transform(img_y)

        #load feature
        feat_x = np.load(f'../sourcedata/data/HCP_7T_movie_FIX/features/{stim_feat[i]}_{feature}.npy')
        feat_x = resample(feat_x, img_y.shape[0], axis=0) #resample to 1hz for now 
        #feat_x=feat_x.T
        #trim final movies
        img_y = img_y[:exclude_final,:]
        feat_x = feat_x[:exclude_final,:]
        y_l.append(img_y)
        x_l.append(feat_x)
    Y=np.vstack(y_l)
    X=np.vstack(x_l)
    #X = scaler.fit_transform(X)
    #vertex_info = hcp.get_HCP_vertex_info(img)
    return X,Y




def load_data_no_rest(subject,feature,n_movies):
    from sklearn.preprocessing import StandardScaler
    # Inputs: subject = HCP id eg 100610
    #         feature='mfs'
    #         n_movies is a list of movie indices 1 thru 4
    # Returns: X feature data (2D; time x feature)
    #          Y brain data (2D; time x grayordinate)
    #          where the rest time periods have been removed
    scaler = StandardScaler()
    y_l=[]
    x_l=[]
    stim = ['tfMRI_MOVIE1_7T_AP','tfMRI_MOVIE2_7T_PA','tfMRI_MOVIE3_7T_PA','tfMRI_MOVIE4_7T_AP']
    stim_feat = ['7T_MOVIE1_CC1_v2', '7T_MOVIE2_HO1_v2', '7T_MOVIE3_CC2_v2', '7T_MOVIE4_HO2_v2']
    slice_starts = [
        [20,284, 526,734],
        [20,267,545],
        [20,221,425,649],
        [20,272,522]]
    slice_stops =  [
        [264,506,714,798],
        [247,525,795],
        [201,405,629,792],
        [252,502,777]]
    for i in n_movies:
        i=i-1
        im_file = f'../sourcedata/data/HCP_7T_movie_FIX/brain/HCP_7T_movie_FIX/{str(subject)}/MNINonLinear/Results/{stim[i]}/{stim[i]}_Atlas_1.6mm_MSMAll_hp2000_clean.dtseries.nii'
        img = nb.load(im_file)
        img_y = img.get_fdata()
        img_y = scaler.fit_transform(img_y)
        #load feature
        feat_x = np.load(f'../sourcedata/data/HCP_7T_movie_FIX/features_hrf/{stim_feat[i]}_{feature}_hrf.npy')
        #feat_x=feat_x.T
        for ii,sl in enumerate(slice_starts[i]):
            y_l.append(img_y[sl:slice_stops[i][ii],:])
            x_l.append(feat_x[sl:slice_stops[i][ii],:])
    Y=np.vstack(y_l)
    X=np.vstack(x_l)
    #X = scaler.fit_transform(X)
    vertex_info = hcp.get_HCP_vertex_info(img)
    return X,Y,vertex_info

def load_data_merlin(subject,feature):
    # Inputs: subject = id eg 'sub-19'
    #         feature='as_scores'
    # Returns: X feature data (2D; time x feature)
    #          Y brain data (2D; time x grayordinate)
    im_file = f'../sourcedata/data/merlin/brain/merlin_cifti_clean_smooth/{str(subject)}_clean_smooth_task-MerlinMovie_space-fsLR_den-91k_bold.dtseries.nii'
    img = nb.load(im_file)
    Y = img.get_fdata()
    Y = Y[17:] #trim beginning, first 17 TRs
    Y = Y[:1009] #trim end to end of film    braintrain.append(s_brain[:-200,:]) #roughly 80 20 split, trim the last 200 TRs of each subject to save as test set
    Y = np.nan_to_num(Y)
    #load feature
    X = np.load(f'../sourcedata/data/merlin/features/Merlin_{feature}.npy')
    X = resample(X, Y.shape[0], axis=0) #resample to 1hz for now 
    #feat_x=feat_x.T
    #trim final movies
    vertex_info = hcp.get_HCP_vertex_info(img)
    return X,Y,vertex_info



def simple_ridgeCV(X,Y,n_splits):
    estimator = RidgeCV(alphas=[0.1, 1.0, 10.0, 100])
    cv = KFold(n_splits=n_splits)
    scores = []
    corr = []
    weights=[]
    for train, test in cv.split(X=X):
        train = train[3:-3] #remove the first and last 3 seconds of each test and train partition
        test = test[3:-3]
        # print(f'training... {train}')
        # we train the Ridge estimator on the training set
        # and predict the fMRI activity for the test set
        predictions = estimator.fit(X.reshape(-1, X.shape[1])[train], Y[train]).predict(
            X.reshape(-1, X.shape[1])[test])
        # we compute how much variance our encoding model explains in each voxel
        scores.append(r2_score(Y[test], predictions,multioutput='raw_values'))
        corr.append(npp.mcorr(Y[test], predictions))
        weights.append(estimator.coef_)
    scores_mean = np.mean(scores, axis=0)
    corr_mean = np.mean(corr, axis=0)
    weights_mean = np.mean(weights, axis=0)
    return scores_mean,corr_mean,weights_mean

def plot_results(scores,score_type,data_type,vertex_info,subject,feature,dataset,title):
    '''Inputs:
        scores = data to plot
        score_type = r2, r, p, z, d, raw, weights
        data_type = 32k (3T) or 59k (7T)
        vertex info = None or the vertex info if it is 59k data beacuse hcp_utils doesnt by default
        subject = eg 100610 subject id for file naming
        feature = eg as_scores plotted feature for file naming
        dataset = eg merlin or HCP_7T which dataset?
        title = 
    '''
    scratch_dir = '../tmp'
#     scratch_dir = '/scratch/scratch/Fri/jsmentch/tmp'
#     if not os.path.exists(scratch_dir):
#         os.mkdir(scratch_dir)
    if score_type == 'r2':
        v=[0,0.05]
        threshold=0.005
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'r':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'p':
        v=[0,0.05]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'z':
        v=[-10,10]
        threshold=3
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'd':
        v=[0,10]
        threshold=3
        symmetric_cmap=True
        cmap='inferno'
    if score_type == 'raw':
        v=[-10,10]
        threshold=1
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights':
        v=[-0.1,0.1]
        threshold=0.01
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights_ind':
        v=[-0.3,0.3]
        threshold=0.05
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'c_weights':
        v=[-.003,.003]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'nmf_weights':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'tensor_decomp':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 'tensor_decomp_inv':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr_r
    if score_type == 'tensor_decomp_raw':
        v=[None,None]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'tensor_decomp_par':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 's_average':
        v=[0,8]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'yibei':
        v=[0.1,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'a_v':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='bwr'
    if score_type == 'a_v_diff':
        v=[-1,1]
        threshold=None
        symmetric_cmap=False
        cmap='bwr'
    save_dir=f'../outputs/figures/{dataset}/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)    
    if data_type == '59k':
        flatmeshes=load_flatmaps_59k() #load flatmaps
        surf_path_msm = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
        mesh59k_msm = load_meshes(example_filename=surf_path_msm) #load other meshes
        # get data from results in plotting format
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0, vertex_info=vertex_info)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0, vertex_info=vertex_info)
        # sulcal depth paths
        sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
        sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
        # params for view to plot
        params = [('flat_L',score_cortex_dataL,flatmeshes.flat_left,sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,flatmeshes.flat_right,sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,mesh59k_msm.very_inflated_left,sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,mesh59k_msm.very_inflated_right,sulc_right,'right'),\
        ]
    elif data_type == '32k':
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0)
    #     # sulcal depth paths
    #     sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
    #     sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
    #     # params for view to plot
        params = [('flat_L',score_cortex_dataL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right'),\
        ]
    # plot each hemi and mesh, save to outputs dir
    for name, data, mesh, sulc, hemi in params:
        #figure, axes = plt.subplots(subplot_kw=dict(projection="3d"), figsize=(6,4))
        plot_surf(mesh,\
                data, \
                  cmap=cmap,symmetric_cmap=symmetric_cmap, avg_method='median',#figure=fig,\
                bg_map=sulc, colorbar=True, vmin=v[0], vmax=v[1], threshold=threshold, hemi=hemi, \
#                 data_alpha=np.where(data>0,1,0),\
#                 data_alpha=np.ones(data.shape),\
                data_alpha=np.ones(data.shape),\
                  data_remove=np.zeros(data.shape),output_file=f'{scratch_dir}/{name}.png')
#combine saved maps into one with PIL
#     if notebook==True:
    area = (75, 140, 635, 560) #area to crop from each image
#     else:
#         area = (105, 190, 880, 780)
        
    img = Image.open(f'{scratch_dir}/flat_L.png',mode='r')
    img = img.resize((770,720))
    cropped = img.crop(area)
    fL=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = img.size
    c_area = (690, 0, w-10, h) # area of colorbar to crop
    cbar = img.crop(c_area)

    img = Image.open(f'{scratch_dir}/flat_R.png',mode='r')
    img = img.resize((770,720))
    fR = img.crop(area)

    img = Image.open(f'{scratch_dir}/vinf_L.png',mode='r')
    img = img.resize((770,720))
    iL = img.crop(area)
    #iL=cropped.transpose(Image.FLIP_LEFT_RIGHT)

    img = Image.open(f'{scratch_dir}/vinf_R.png',mode='r')
    img = img.resize((770,720))
    iR = img.crop(area)

    w,h=iR.size

    new_im = Image.new('RGB', ( (w*2)+70 , h*2) ,(255, 255, 255, 1))
    new_im.paste(fL,(0,h))
    new_im.paste(fR,(w,h))
    new_im.paste(iL,(0,0))
    new_im.paste(iR,(w,0))
    new_im.paste(cbar,(w*2,int(round(h/4))))

    w,h=new_im.size

    draw = ImageDraw.Draw(new_im)
    #draw.text((0,0),f"{title}_{subject}_{feature}_{score_type}",(0,0,0)) #UNCOMMENT TO PRINT TITLE TOP LEFT

    new_im.save(f'{save_dir}{title}_{subject}_{feature}_{score_type}.png')
#     os.remove(f'{scratch_dir}/flat_L.png')
#     os.remove(f'{scratch_dir}/flat_R.png')
#     os.remove(f'{scratch_dir}/vinf_L.png')
#     os.remove(f'{scratch_dir}/vinf_R.png')

def plot_results_inputalpha(scores,scores_alpha,score_type,data_type,vertex_info,subject,feature,dataset,title):
    '''Inputs:
        scores = data to plot
        score_type = r2, r, p, z, d, raw, weights
        data_type = 32k (3T) or 59k (7T)
        vertex info = None or the vertex info if it is 59k data beacuse hcp_utils doesnt by default
        subject = eg 100610 subject id for file naming
        feature = eg as_scores plotted feature for file naming
        dataset = eg merlin or HCP_7T which dataset?
        title = 
    '''
    scratch_dir = '../tmp'
#     scratch_dir = '/scratch/scratch/Fri/jsmentch/tmp'
#     if not os.path.exists(scratch_dir):
#         os.mkdir(scratch_dir)
    if score_type == 'r2':
        v=[0,0.5]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'r':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'p':
        v=[0,0.05]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'z':
        v=[-10,10]
        threshold=3
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'd':
        v=[0,10]
        threshold=3
        symmetric_cmap=True
        cmap='inferno'
    if score_type == 'raw':
        v=[-10,10]
        threshold=1
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'c_weights':
        v=[-.003,.003]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'nmf_weights':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'tensor_decomp':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 'tensor_decomp_inv':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr_r
    if score_type == 'tensor_decomp_raw':
        v=[None,None]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'tensor_decomp_par':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 's_average':
        v=[0,8]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'a_v':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='bwr'
    if score_type == 'a_v_diff':
        v=[-1,1]
        threshold=None
        symmetric_cmap=False
        cmap='bwr'
    save_dir=f'../outputs/figures/{dataset}/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)    
    if data_type == '59k':
        flatmeshes=load_flatmaps_59k() #load flatmaps
        surf_path_msm = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
        mesh59k_msm = load_meshes(example_filename=surf_path_msm) #load other meshes
        # get data from results in plotting format
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0, vertex_info=vertex_info)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0, vertex_info=vertex_info)
        # sulcal depth paths
        sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
        sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
        # params for view to plot
        params = [('flat_L',score_cortex_dataL,flatmeshes.flat_left,sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,flatmeshes.flat_right,sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,mesh59k_msm.very_inflated_left,sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,mesh59k_msm.very_inflated_right,sulc_right,'right'),\
        ]
    elif data_type == '32k':
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0)
        scores_alphaL = hcp.left_cortex_data(scores_alpha, fill=0)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0)
        scores_alphaR = hcp.right_cortex_data(scores_alpha, fill=0)

    #     # sulcal depth paths
    #     sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
    #     sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
    #     # params for view to plot
        params = [('flat_L',score_cortex_dataL,scores_alphaL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,scores_alphaR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,scores_alphaL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,scores_alphaR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right'),\
        ]
    # plot each hemi and mesh, save to outputs dir
    for name, data, scores_alpha, mesh, sulc, hemi in params:
        #figure, axes = plt.subplots(subplot_kw=dict(projection="3d"), figsize=(6,4))
        plot_surf(mesh,\
                data, \
                  cmap=cmap,symmetric_cmap=symmetric_cmap, avg_method='median',#figure=fig,\
                bg_map=sulc, colorbar=True, vmin=v[0], vmax=v[1], threshold=threshold, hemi=hemi, \
#                 data_alpha=np.where(data>0,1,0),\
#                 data_alpha=np.ones(data.shape),\
#                data_alpha=np.abs(data),\
                data_alpha=scores_alpha,\
                data_remove=np.zeros(data.shape),output_file=f'{scratch_dir}/{name}.png')
#combine saved maps into one with PIL
#     if notebook==True:
    area = (75, 140, 635, 560) #area to crop from each image
#     else:
#         area = (105, 190, 880, 780)
        
    img = Image.open(f'{scratch_dir}/flat_L.png',mode='r')
    img = img.resize((770,720))
    cropped = img.crop(area)
    fL=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = img.size
    c_area = (690, 0, w-10, h) # area of colorbar to crop
    cbar = img.crop(c_area)

    img = Image.open(f'{scratch_dir}/flat_R.png',mode='r')
    img = img.resize((770,720))
    fR = img.crop(area)

    img = Image.open(f'{scratch_dir}/vinf_L.png',mode='r')
    img = img.resize((770,720))
    iL = img.crop(area)
    #iL=cropped.transpose(Image.FLIP_LEFT_RIGHT)

    img = Image.open(f'{scratch_dir}/vinf_R.png',mode='r')
    img = img.resize((770,720))
    iR = img.crop(area)

    w,h=iR.size

    new_im = Image.new('RGB', ( (w*2)+70 , h*2) ,(255, 255, 255, 1))
    new_im.paste(fL,(0,h))
    new_im.paste(fR,(w,h))
    new_im.paste(iL,(0,0))
    new_im.paste(iR,(w,0))
    new_im.paste(cbar,(w*2,int(round(h/4))))

    w,h=new_im.size

    draw = ImageDraw.Draw(new_im)
    #draw.text((0,0),f"{title}_{subject}_{feature}_{score_type}",(0,0,0)) #UNCOMMENT TO PRINT TITLE TOP LEFT

    new_im.save(f'{save_dir}{title}_{subject}_{feature}_{score_type}.png')
#     os.remove(f'{scratch_dir}/flat_L.png')
#     os.remove(f'{scratch_dir}/flat_R.png')
#     os.remove(f'{scratch_dir}/vinf_L.png')
#     os.remove(f'{scratch_dir}/vinf_R.png')



def plot_results_medial(scores,score_type,data_type,vertex_info,subject,feature,dataset,title):
    '''Inputs:
        scores = data to plot
        score_type = r2, r, p, z, d, raw, weights
        data_type = 32k (3T) or 59k (7T)
        vertex info = None or the vertex info if it is 59k data beacuse hcp_utils doesnt by default
        subject = eg 100610 subject id for file naming
        feature = eg as_scores plotted feature for file naming
        dataset = eg merlin or HCP_7T which dataset?
        title = 
    '''
    scratch_dir = '../tmp'
#     scratch_dir = '/scratch/scratch/Fri/jsmentch/tmp'
#     if not os.path.exists(scratch_dir):
#         os.mkdir(scratch_dir)
    if score_type == 'r2':
        v=[0,0.5]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'r':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'p':
        v=[0,0.05]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'z':
        v=[-10,10]
        threshold=3
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'd':
        v=[0,10]
        threshold=3
        symmetric_cmap=True
        cmap='inferno'
    if score_type == 'raw':
        v=[-10,10]
        threshold=1
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'c_weights':
        v=[-.003,.003]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'nmf_weights':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'tensor_decomp':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 'tensor_decomp_inv':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr_r
    if score_type == 'tensor_decomp_raw':
        v=[None,None]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'tensor_decomp_par':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 's_average':
        v=[0,8]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    save_dir=f'../outputs/figures/{dataset}/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)    
    if data_type == '59k':
        flatmeshes=load_flatmaps_59k() #load flatmaps
        surf_path_msm = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
        mesh59k_msm = load_meshes(example_filename=surf_path_msm) #load other meshes
        # get data from results in plotting format
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0, vertex_info=vertex_info)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0, vertex_info=vertex_info)
        # sulcal depth paths
        sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
        sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
        # params for view to plot
        params = [('flat_L',score_cortex_dataL,flatmeshes.flat_left,sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,flatmeshes.flat_right,sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,mesh59k_msm.very_inflated_left,sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,mesh59k_msm.very_inflated_right,sulc_right,'right'),\
        ]
    elif data_type == '32k':
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0)
    #     # sulcal depth paths
    #     sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
    #     sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
    #     # params for view to plot
        params = [('flat_L',score_cortex_dataL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right'),\
        ]
        params = [('vinf_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left','lateral'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right','lateral'),\
         ('flat_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left','medial'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right','medial'),\
        ]
    # plot each hemi and mesh, save to outputs dir
    for name, data, mesh, sulc, hemi, view in params:
        #figure, axes = plt.subplots(subplot_kw=dict(projection="3d"), figsize=(6,4))
        plot_surf(mesh,\
                data, \
                  cmap=cmap,symmetric_cmap=symmetric_cmap, avg_method='median',#figure=fig,\
                bg_map=sulc, colorbar=True, vmin=v[0], vmax=v[1], threshold=threshold, hemi=hemi, \
                  view=view, \
#                 data_alpha=np.where(data>0,1,0),\
                data_alpha=np.ones(data.shape), \
#                   data_alpha=np.ones(data.shape), \
                  data_remove=np.zeros(data.shape),output_file=f'{scratch_dir}/{name}.png')
#combine saved maps into one with PIL
#     if notebook==True:
    area = (75, 140, 635, 560) #area to crop from each image
#     else:
#         area = (105, 190, 880, 780)
        
    img = Image.open(f'{scratch_dir}/flat_L.png',mode='r')
    img = img.resize((770,720))
    fL = img.crop(area)
    #fL=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = img.size
    c_area = (690, 0, w-10, h) # area of colorbar to crop
    cbar = img.crop(c_area)

    img = Image.open(f'{scratch_dir}/flat_R.png',mode='r')
    img = img.resize((770,720))
    fR = img.crop(area)

    img = Image.open(f'{scratch_dir}/vinf_L.png',mode='r')
    img = img.resize((770,720))
    iL = img.crop(area)
    #iL=cropped.transpose(Image.FLIP_LEFT_RIGHT)

    img = Image.open(f'{scratch_dir}/vinf_R.png',mode='r')
    img = img.resize((770,720))
    iR = img.crop(area)

    w,h=iR.size

    new_im = Image.new('RGB', ( (w*2)+70 , h*2) ,(255, 255, 255, 1))
    new_im.paste(fL,(0,h))
    new_im.paste(fR,(w,h))
    new_im.paste(iL,(0,0))
    new_im.paste(iR,(w,0))
    new_im.paste(cbar,(w*2,int(round(h/4))))

    w,h=new_im.size

    draw = ImageDraw.Draw(new_im)
    #draw.text((0,0),f"{title}_{subject}_{feature}_{score_type}",(0,0,0)) #UNCOMMENT TO PRINT TITLE TOP LEFT

    new_im.save(f'{save_dir}{title}_{subject}_{feature}_{score_type}.png')
#     os.remove(f'{scratch_dir}/flat_L.png')
#     os.remove(f'{scratch_dir}/flat_R.png')
#     os.remove(f'{scratch_dir}/vinf_L.png')
#     os.remove(f'{scratch_dir}/vinf_R.png')



def plot_results_medial_midthickness_alpha(scores,score_type,data_type,vertex_info,subject,feature,dataset,title):
    '''Inputs:
        scores = data to plot
        score_type = r2, r, p, z, d, raw, weights
        data_type = 32k (3T) or 59k (7T)
        vertex info = None or the vertex info if it is 59k data beacuse hcp_utils doesnt by default
        subject = eg 100610 subject id for file naming
        feature = eg as_scores plotted feature for file naming
        dataset = eg merlin or HCP_7T which dataset?
        title = 
    '''
    scratch_dir = '../tmp'
#     scratch_dir = '/scratch/scratch/Fri/jsmentch/tmp'
#     if not os.path.exists(scratch_dir):
#         os.mkdir(scratch_dir)
    if score_type == 'r2':
        v=[0,0.5]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'r':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'p':
        v=[0,0.05]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'z':
        v=[-10,10]
        threshold=3
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'd':
        v=[0,10]
        threshold=3
        symmetric_cmap=True
        cmap='inferno'
    if score_type == 'raw':
        v=[-10,10]
        threshold=1
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'c_weights':
        v=[-.003,.003]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'nmf_weights':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'tensor_decomp':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 'tensor_decomp_inv':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr_r
    if score_type == 'tensor_decomp_raw':
        v=[None,None]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'tensor_decomp_par':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 's_average':
        v=[0,8]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    save_dir=f'../outputs/figures/{dataset}/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)    
    if data_type == '59k':
        flatmeshes=load_flatmaps_59k() #load flatmaps
        surf_path_msm = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
        mesh59k_msm = load_meshes(example_filename=surf_path_msm) #load other meshes
        # get data from results in plotting format
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0, vertex_info=vertex_info)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0, vertex_info=vertex_info)
        # sulcal depth paths
        sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
        sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
        # params for view to plot
        params = [('flat_L',score_cortex_dataL,flatmeshes.flat_left,sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,flatmeshes.flat_right,sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,mesh59k_msm.very_inflated_left,sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,mesh59k_msm.very_inflated_right,sulc_right,'right'),\
        ]
    elif data_type == '32k':
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0)
    #     # sulcal depth paths
    #     sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
    #     sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
    #     # params for view to plot
        params = [('flat_L',score_cortex_dataL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right'),\
        ]
        params = [('vinf_L',score_cortex_dataL,hcp.mesh.inflated_left,hcp.mesh.sulc_left,'left','lateral'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.inflated_right,hcp.mesh.sulc_right,'right','lateral'),\
         ('flat_L',score_cortex_dataL,hcp.mesh.inflated_left,hcp.mesh.sulc_left,'left','medial'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.inflated_right,hcp.mesh.sulc_right,'right','medial'),\
        ]
        params = [('vinf_L',score_cortex_dataL,hcp.mesh.midthickness_left,hcp.mesh.sulc_left,'left','lateral'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.midthickness_right,hcp.mesh.sulc_right,'right','lateral'),\
         ('flat_L',score_cortex_dataL,hcp.mesh.midthickness_left,hcp.mesh.sulc_left,'left','medial'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.midthickness_right,hcp.mesh.sulc_right,'right','medial'),\
        ]
    # plot each hemi and mesh, save to outputs dir
    for name, data, mesh, sulc, hemi, view in params:
        #figure, axes = plt.subplots(subplot_kw=dict(projection="3d"), figsize=(6,4))
        plot_surf(mesh,\
                data, \
                  cmap=cmap,symmetric_cmap=symmetric_cmap, avg_method='median',#figure=fig,\
                bg_map=sulc, colorbar=True, vmin=v[0], vmax=v[1], threshold=threshold, hemi=hemi, \
                  view=view, \
#                 data_alpha=np.where(np.abs(data)>0,1,0),\
#                 data_alpha=np.where(np.abs(data)>0.1,1,np.abs(data)*10),\
#                data_alpha=np.abs(data),\
                 data_alpha=np.ones(data.shape), \
                  data_remove=np.zeros(data.shape),output_file=f'{scratch_dir}/{name}.png')
#combine saved maps into one with PIL
#     if notebook==True:
    area = (75, 140, 635, 560) #area to crop from each image
#     else:
#         area = (105, 190, 880, 780)
        
    img = Image.open(f'{scratch_dir}/flat_L.png',mode='r')
    img = img.resize((770,720))
    fL = img.crop(area)
    #fL=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = img.size
    c_area = (690, 0, w-10, h) # area of colorbar to crop
    cbar = img.crop(c_area)

    img = Image.open(f'{scratch_dir}/flat_R.png',mode='r')
    img = img.resize((770,720))
    fR = img.crop(area)

    img = Image.open(f'{scratch_dir}/vinf_L.png',mode='r')
    img = img.resize((770,720))
    iL = img.crop(area)
    #iL=cropped.transpose(Image.FLIP_LEFT_RIGHT)

    img = Image.open(f'{scratch_dir}/vinf_R.png',mode='r')
    img = img.resize((770,720))
    iR = img.crop(area)

    w,h=iR.size

    new_im = Image.new('RGB', ( (w*2)+70 , h*2) ,(255, 255, 255, 1))
    new_im.paste(fL,(0,h))
    new_im.paste(fR,(w,h))
    new_im.paste(iL,(0,0))
    new_im.paste(iR,(w,0))
    new_im.paste(cbar,(w*2,int(round(h/4))))

    w,h=new_im.size

    draw = ImageDraw.Draw(new_im)
    #draw.text((0,0),f"{title}_{subject}_{feature}_{score_type}",(0,0,0)) #UNCOMMENT TO PRINT TITLE TOP LEFT

    new_im.save(f'{save_dir}{title}_{subject}_{feature}_{score_type}.png')
#     os.remove(f'{scratch_dir}/flat_L.png')
#     os.remove(f'{scratch_dir}/flat_R.png')
#     os.remove(f'{scratch_dir}/vinf_L.png')
#     os.remove(f'{scratch_dir}/vinf_R.png')










def plot_results_medial_midthickness_alpha_ventralflat(scores,score_type,data_type,vertex_info,subject,feature,dataset,title):
    '''Inputs:
        scores = data to plot
        score_type = r2, r, p, z, d, raw, weights
        data_type = 32k (3T) or 59k (7T)
        vertex info = None or the vertex info if it is 59k data beacuse hcp_utils doesnt by default
        subject = eg 100610 subject id for file naming
        feature = eg as_scores plotted feature for file naming
        dataset = eg merlin or HCP_7T which dataset?
        title = 
    '''
    scratch_dir = '../tmp'
#     scratch_dir = '/scratch/scratch/Fri/jsmentch/tmp'
#     if not os.path.exists(scratch_dir):
#         os.mkdir(scratch_dir)
    if score_type == 'r2':
        v=[0,0.5]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'r':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'p':
        v=[0,0.05]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'z':
        v=[-10,10]
        threshold=3
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'd':
        v=[0,10]
        threshold=3
        symmetric_cmap=True
        cmap='inferno'
    if score_type == 'raw':
        v=[-10,10]
        threshold=1
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'weights':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'c_weights':
        v=[-.003,.003]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'nmf_weights':
        v=[0,1]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    if score_type == 'tensor_decomp':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 'tensor_decomp_inv':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr_r
    if score_type == 'tensor_decomp_raw':
        v=[None,None]
        threshold=None
        symmetric_cmap=True
        cmap='cold_hot'
    if score_type == 'tensor_decomp_par':
        v=[-1,1]
        threshold=None
        symmetric_cmap=True
        cmap=pigr
    if score_type == 's_average':
        v=[0,8]
        threshold=None
        symmetric_cmap=False
        cmap='inferno'
    save_dir=f'../outputs/figures/{dataset}/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)    
    if data_type == '59k':
        flatmeshes=load_flatmaps_59k() #load flatmaps
        surf_path_msm = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/T1w/fsaverage_LR59k/100610.L.inflated_1.6mm_MSMAll.59k_fs_LR.surf.gii'
        mesh59k_msm = load_meshes(example_filename=surf_path_msm) #load other meshes
        # get data from results in plotting format
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0, vertex_info=vertex_info)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0, vertex_info=vertex_info)
        # sulcal depth paths
        sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
        sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
        # params for view to plot
        params = [('flat_L',score_cortex_dataL,flatmeshes.flat_left,sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,flatmeshes.flat_right,sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,mesh59k_msm.very_inflated_left,sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,mesh59k_msm.very_inflated_right,sulc_right,'right'),\
        ]
    elif data_type == '32k':
        score_cortex_dataL = hcp.left_cortex_data(scores, fill=0)
        score_cortex_dataR = hcp.right_cortex_data(scores, fill=0)
    #     # sulcal depth paths
    #     sulc_left = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.L.sulc.59k_fs_LR.shape.gii'
    #     sulc_right = '../sourcedata/data/human-connectome-project-openaccess/HCP1200/100610/MNINonLinear/fsaverage_LR59k/100610.R.sulc.59k_fs_LR.shape.gii'
    #     # params for view to plot
        params = [('flat_L',score_cortex_dataL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right'),\
         ('vinf_L',score_cortex_dataL,hcp.mesh.very_inflated_left,hcp.mesh.sulc_left,'left'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.very_inflated_right,hcp.mesh.sulc_right,'right'),\
        ]
        params = [('vinf_L',score_cortex_dataL,hcp.mesh.inflated_left,hcp.mesh.sulc_left,'left','lateral'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.inflated_right,hcp.mesh.sulc_right,'right','lateral'),\
         ('flat_L',score_cortex_dataL,hcp.mesh.inflated_left,hcp.mesh.sulc_left,'left','medial'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.inflated_right,hcp.mesh.sulc_right,'right','medial'),\
        ]
        params = [('vinf_L',score_cortex_dataL,hcp.mesh.midthickness_left,hcp.mesh.sulc_left,'left','ventral'),\
         ('vinf_R',score_cortex_dataR,hcp.mesh.midthickness_right,hcp.mesh.sulc_right,'right','ventral'),\
         ('flat_L',score_cortex_dataL,hcp.mesh.flat_left,hcp.mesh.sulc_left,'left','lateral'),\
         ('flat_R',score_cortex_dataR,hcp.mesh.flat_right,hcp.mesh.sulc_right,'right','lateral'),\
        ]
    # plot each hemi and mesh, save to outputs dir
    for name, data, mesh, sulc, hemi, view in params:
        #figure, axes = plt.subplots(subplot_kw=dict(projection="3d"), figsize=(6,4))
        plot_surf(mesh,\
                data, \
                  cmap=cmap,symmetric_cmap=symmetric_cmap, avg_method='median',#figure=fig,\
                bg_map=sulc, colorbar=True, vmin=v[0], vmax=v[1], threshold=threshold, hemi=hemi, \
                  view=view, \
#                 data_alpha=np.where(np.abs(data)>0,1,0),\
#                 data_alpha=np.where(np.abs(data)>0.1,1,np.abs(data)*10),\
#                data_alpha=np.abs(data),\
                 data_alpha=np.ones(data.shape), \
                  data_remove=np.zeros(data.shape),output_file=f'{scratch_dir}/{name}.png')
#combine saved maps into one with PIL
#     if notebook==True:
    area = (75, 140, 635, 560) #area to crop from each image
#     else:
#         area = (105, 190, 880, 780)
        
    img = Image.open(f'{scratch_dir}/flat_L.png',mode='r')
    img = img.resize((770,720))
    cropped = img.crop(area)
    fL=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = img.size
    c_area = (690, 0, w-10, h) # area of colorbar to crop
    cbar = img.crop(c_area)

    img = Image.open(f'{scratch_dir}/flat_R.png',mode='r')
    img = img.resize((770,720))
    fR = img.crop(area)

    img = Image.open(f'{scratch_dir}/vinf_L.png',mode='r')
    img = img.resize((770,720))
    cropped = img.crop(area)
    cropped_flipped=cropped.transpose(Image.FLIP_LEFT_RIGHT)
    iL=cropped_flipped.transpose(Image.FLIP_TOP_BOTTOM)

    img = Image.open(f'{scratch_dir}/vinf_R.png',mode='r')
    img = img.resize((770,720))
    adjust=80
    area2 = (75, 140-adjust, 635, 560-adjust) #area to crop from each image Left, Top, Right, Botton
    iR = img.crop(area2)

    w,h=iR.size

    new_im = Image.new('RGB', ( (w*2)+70 , h*2) ,(255, 255, 255, 1))
    new_im.paste(fL,(0,h))
    new_im.paste(fR,(w,h))
    new_im.paste(iL,(0,0))
    new_im.paste(iR,(w,0))
    new_im.paste(cbar,(w*2,int(round(h/4))))

    w,h=new_im.size

    draw = ImageDraw.Draw(new_im)
    #draw.text((0,0),f"{title}_{subject}_{feature}_{score_type}",(0,0,0)) #UNCOMMENT TO PRINT TITLE TOP LEFT

    new_im.save(f'{save_dir}{title}_{subject}_{feature}_{score_type}.png')
#     os.remove(f'{scratch_dir}/flat_L.png')
#     os.remove(f'{scratch_dir}/flat_R.png')
#     os.remove(f'{scratch_dir}/vinf_L.png')
#     os.remove(f'{scratch_dir}/vinf_R.png')


def get_vertex_info_59k():
#     import nibabel as nb
#     import hcp_utils as hcp
    im_file = f'/om2/user/jsmentch/projects/nat_img/sourcedata/data/parcellations/combined_Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.59k_fs_LR.dlabel.nii'
    img = nb.load(im_file)
    vertex_info = hcp.get_HCP_vertex_info(img)
    return vertex_info


# def get_vertex_info_32k():
# #     import nibabel as nb
# #     import hcp_utils as hcp
#     im_file = f'/om2/user/jsmentch/projects/nat_img/sourcedata/data/parcellations/combined_Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.59k_fs_LR.dlabel.nii'
#     img = nb.load(im_file)
#     vertex_info = hcp.get_HCP_vertex_info(img)
#     return vertex_info

def model_FIR(X):
# input: a time x feature array
# output: a time x feature(x4) array for FIR model 
    X1=np.insert(X,0,0,axis=0)[:-1,:]
    X2=np.insert(X1,0,0,axis=0)[:-1,:]
    X3=np.insert(X2,0,0,axis=0)[:-1,:]
    X4=np.insert(X3,0,0,axis=0)[:-1,:]
    X_FIR=np.concatenate((X1,X2,X3,X4),axis=1)
    return X_FIR