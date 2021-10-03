def plot_folder_gif(img_dir,dur):
    from PIL import Image, ImageDraw
    import os
    img_list=os.listdir(img_dir)
    img_list=img_list[1:]

    img1 = Image.open(img_dir+img_list[0])

    append_images=[]
    for i,im in enumerate(img_list[1:]):
        img2 = Image.open(img_dir+img_list[i])
        append_images.append(img2)
    img1.save(f'{img_dir}.gif', save_all=True, append_images=append_images, duration=dur, loop=0)
    
    

def var_to_nan(fdata,var_thresh):
    import numpy as np
    fdata_var=np.var(fdata,axis=0) #calculate variance
    if var_thresh==0:
        to_nan = np.where(fdata_var==var_thresh,True,False) #nan places w zero variance
    else:
        to_nan = np.where(fdata_var<var_thresh,True,False) #nan voxels w variance less than var_thresh
    fdata[:,to_nan]=float("NaN") #set to nan
    return fdata