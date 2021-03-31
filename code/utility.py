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