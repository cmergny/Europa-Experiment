# -*- coding: utf-8 -*-
"""
Change channel of images
"""
import glob
import os
import numpy as np
from PIL import Image

os.chdir("C:/Users/Arnaud/micmac_projects/")

folder = 'older/with_laser'
new_folder = folder + "NNored"
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
    

for image_name in glob.glob(folder+'/*.JPG'):

    im = Image.open(image_name)
    exif = im.info["exif"]
    im = np.array(im)
    im[::, ::, 0] = 0 # Delete Red Channel
    im = Image.fromarray(im)
    im.save(new_folder+"/"+image_name[len(folder)+1:], exif=exif)

