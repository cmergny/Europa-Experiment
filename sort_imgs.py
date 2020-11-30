# -*- coding: utf-8 -*-
"""
Sort by time
Author: Cyril Mergny
Last update : 26/11/2020
"""

import glob
import os
import numpy as np
from PIL import Image

os.chdir("C:/Users/Arnaud/micmac_projects/")


def sort_image(image_name, folder_name, idx):
    im = Image.open(image_name)
    exif = im.info["exif"]
    im = np.array(im)
    #im[::, ::, 0] = 0 # Delete Red Channel
    im = Image.fromarray(im)
    im.save("{0}/{1}.JPG".format(folder_name, idx), exif=exif)
    return()

def make_folder(folder_name):
    """Creates a new directory only if it does not already exists."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print('Created folder "{}".'.format(folder_name))
    else:
        print('Warning: folder "{}" already exists.'.format(folder_name))
    return()




# Find names and times of all pictures
folder = 'photos'
Names_Times = []
for image_name in glob.glob(folder+'/*.JPG'):
    im = Image.open(image_name)
    time = im.getexif()[36867] # date and time
    time = time.split(" ")[1].split(":") # split hours, min and sec
    time = int(time[0])*60 +int(time[1])+int(time[2])/60 # convert to minutes
    Names_Times.append([image_name, time, 0])


# Sort all pictures in categories of similar time
delta = 3 # minimum time difference required to be assigned to a same set  
ctg = 0 # categorie nbr
for i, elt in enumerate(Names_Times):
    time = elt[1]
    # Finding a new set
    if elt[2] == 0 :
        ctg += 1
        folder_name = "set_{}".format(ctg)
        make_folder(folder_name)
        # Finding all pics of same set
        idx = 0 
        for j, elt2 in enumerate(Names_Times):
            t = elt2[1]
            if np.abs(time-t) < delta:
                idx += 1 
                Names_Times[j][2] = ctg
                sort_image(elt2[0], folder_name, idx)
                
