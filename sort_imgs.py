# -*- coding: utf-8 -*-
"""
From a folder of images creates sets of images grouped by their time 
(from exif data). Each set is a new folder consisting of images taken at time
close to each other. A parameter provided by the user, delta, determines the 
maximum time difference allowed for two images to be part of the same set.
Author: Cyril Mergny
Last update : 04/12/2020
"""

### Imports 

import glob
import numpy as np
from PIL import Image
from tqdm import tqdm
from laser_process import BrowseFolder, CreateOutputFolder

### Functions

def SaveImage(image_name, out_dir, im_nbr):
    """
    Save image_name in out_dir directory with new name = im_nbr .
    """
    im = Image.open(image_name)
    exif = im.info["exif"]
    
    res = np.array(im)
    res[::, ::, 0] = 0 # Delete Red Channel
    #res[::, ::, 2] = 0 # Delete Blue Channel
    im = Image.fromarray(res)
    
    im.save(f"{out_dir}/{im_nbr}.JPG", exif=exif)
    return(None)

def GetImageTime(im):
    """
    Returns the time when an image was taken. Hours and seconds are converted 
    in minutes. 
    """
    time = im.getexif()[36867] # date and time
    time = time.split(" ")[1].split(":") # split hours, min and sec
    time = int(time[0])*60 +int(time[1])+int(time[2])/60 # convert to minutes
    return(time)

def GetNamesTimesCtgs(in_dir):
    """
    From a set of images, returns a (n,3) shaped list NamesTimesCtgs,
    where n is the nbr of images in the input directory. 
    Each element of NamesTimesCtgs is a list of lentgh 3 defined by:
        NamesTimesCtgs[i] = [image_name, time, ctg]
    """
    NamesTimesCtgs = [] 
    for image_name in glob.glob(in_dir+'/*.JPG'):
        im = Image.open(image_name)
        time = GetImageTime(im)
        NamesTimesCtgs.append([image_name, time, 0])
        # img with ctg 0 are not sorted yet
    return(NamesTimesCtgs)
        
def SortImages(in_dir, delta):
    """
    From an input directory of images, sort these images by set of similar
    times. Images whose times are seperated by least than delta (in minutes)
    are part of the same set.
        Ex: if delta = 5 (minutes)
            Img1 taken at 14h34 -> set_1
            Img2 talen at 14h37 -> set_1
            Img3 taken at 14h50 -> set_2
    """
    NamesTimesCtgs = GetNamesTimesCtgs(in_dir) 
    # elt[0] = im_name, elt[1] = time, elt[2] = category
    
    # Sort all pictures in categories of similar time
    ctg = 0 # categorie nbr
    for i, elt in enumerate(NamesTimesCtgs):
        time = elt[1]
        if elt[2] == 0 : # Found a new set
            ctg += 1 # create a new category
            # Make a new dir for this ctg
            out_dir = "set_{:03d}".format(ctg)
            out_dir = CreateOutputFolder(False, in_dir, out_dir)
            # Finding all pics of same set
            im_nbr = 0 
            for j in tqdm(range(len(NamesTimesCtgs))): 
                elt2 = NamesTimesCtgs[j]
                t = elt2[1]
                if np.abs(time-t) < delta: 
                    # pics with similar times are in the same set
                    im_nbr += 1 
                    NamesTimesCtgs[j][2] = ctg
                    SaveImage(elt2[0], out_dir, im_nbr)
            print(f"\nSet {ctg} has {im_nbr} images. \n")
    return(None)
    
#### Main

if __name__ == '__main__':
    
    user_friendly = True
    
    if user_friendly:
        ## Find input folder  
        in_dir = BrowseFolder(user_friendly)
        delta = int(input("Minimum time difference to be assigned to a same set ( in minutes) : "))
    else:
        ## Manual Definition 
        in_dir = "C:/Users/Arnaud/micmac_projects/XP0212/Stereo/All_stereo" # input dir
        in_dir = BrowseFolder(user_friendly, in_dir)
        delta = 2 # min time diff required to be assigned to a same set (min)
        
    SortImages(in_dir, delta)
    