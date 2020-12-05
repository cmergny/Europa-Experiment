#!/usr/bin/env python
# coding: utf-8
"""
Image processing for lab experiment.
Input images are pictures of mutiple laser lines following the topography
of the solidified ludox in a dark background.
This script can apply the following transformations on images:
    - crop 
    - substract blue and green channel 
    - rotate 
    - enhance sharpness, contrast 
    - detect edges with a canny algo
    - and remove artefacts from the edges detection
This script helps applying theses transformations to a large number of images.
Although, for testing purposes, single image manipulation is also possible.

Author : Cyril Mergny
Last update : 04/12/2020
"""

### Imports 

import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance 
import os # to create new folder
import glob # to search for files
from tqdm import tqdm # progress bar
#from skimage import feature # for edge detection
from tkinter import Tk  # to open browse file window
from tkinter.filedialog import askdirectory


### Functions 

def ImShowReduced(im, size = (700,700)):
    """Scales an image to a new size and shows it."""
    res = im.copy()
    res.thumbnail(size, Image.ANTIALIAS)
    plt.imshow(res)

def FilterChannel(im, save = False, output = "ImFilterChannel.JPG", show = False):
    """
    Takes an image and return an image of the red channel only.
    Saves it (optional).
    """
    #exif = im.info["exif"]
    res = np.array(im)
    #res[::, ::, 1] = 0 # Delete Green Channel
    #res[::, ::, 2] = 0 # Delete Blue Channel
    res = Image.fromarray(res[::, ::, 0])
    if save:
        res.save(output)
    if show: 
        ImShowReduced(res)
    return(res)

def EnhanceIm(im, save = False, output = "ImEnchanced.JPG", show = False):
    """
    Takes an image and return an enchanced image with more: sharpness, contrast 
    Saves it (optional).
    """
    # Sharpen 
    enhancer = ImageEnhance.Sharpness(im)
    res = enhancer.enhance(1) 
    # Improve contrast
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(4)
    # Save 
    if save:
        res.save(output)
    if show: 
        ImShowReduced(res)
    return(res)

def EdgesDetection(im, save = False, output = "Edges.JPG", show = False ):
    """
    Compute the canny edges detection algo (on the red channel of) an image.
    Returns a binary image of the detected edges.
    """
    # Canny works with grayscale imgs only
    res = np.array(im) #[:,:,0]
    #edges = feature.canny(res, sigma=5, low_threshold=None)
    thresh = 240
    res[res>thresh] = 255
    res[res<=thresh] = 0
    edges = Image.fromarray(res)
    # Save 
    if save:
        edges.save(output)
    # Show
    if show: 
        ImShowReduced(edges)
    return(edges)

def ImproveEdges(im, save = False, output = "ImproveEdges.JPG", show = False ):
    """
    Naive algorithm that looks at each column of a boolean image
    and returns an image where only the top element of each column is taken.
    """
    edges = np.array(im)
    new = np.zeros(edges.shape)
    # Iterate through columns
    for icol, col in enumerate(edges.T):
        found = False
        # Iterate though each elt of a col
        for idx in range(len(col)):
            if col[idx]:
                if not found:
                    # If found the top elt of the col
                    # Color it in white
                    new[idx-1:idx+2, icol] = 255
                    found = True
            else:
                # Color it in black
                new[idx, icol] = 0
    # Convert array back to image
    res = Image.fromarray(new).convert('1')
    # Save 
    if save:
        res.save(output)
    # Show
    if show: 
        ImShowReduced(res)
    return(res)

def BrowseFolder(user_friendly, in_dir = "InputFolder"):
    """
    Open a window dialog to browse for a folder and return the
    selected folder path.
    """
    if user_friendly ==  True: 
        # Open window browse dialog
        print("A window dialog has been opened. ", flush=True)
        print("Waiting for user to select an input folder ... ", flush=True)
        Tk().withdraw() # no root window
        in_dir = askdirectory() # open a browse window and the file path
    print(f"# Input folder path is: {in_dir}", flush=True)
    return(in_dir)

def CreateOutputFolder(user_friendly, in_dir, out_dir = 'OutputFolder'):
    """
    Create an output folder. Folder's name is either given by the out_dir
    argument or asked by a input call if user_friendly is True.
    """
    if user_friendly ==  True: 
        # Ask for ouput folder name  
        out_dir = input('Creating an output directory, please give it a name : ')
    # Output dir path in the same location as input folder
    out_dir = '/'.join(in_dir.split('/')[:-1]) + '/' + out_dir
    # Make dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f"New directory created at : {out_dir}", flush=True)
    else:
        print(f"Warning: directory already exists at {out_dir}. The progam will continue anyway.", flush=True)
    return(out_dir)

### Main
if __name__ == '__main__':
    
    print("\n --- Python Script to process laser images ---- \n")
    
    user_friendly = True
    
    if user_friendly:
        # Find input folder  
        in_dir = BrowseFolder(user_friendly)
        out_dir = CreateOutputFolder(user_friendly, in_dir)
    else:
        # Manual assignement
        in_dir = "C:/Users/Cyril/Documents/EuropaExp/XP0212/Raw"
        BrowseFolder(user_friendly, in_dir)
        out_dir = "RedChannel2"
        out_dir = CreateOutputFolder(user_friendly, in_dir, out_dir)
    # Files to process
    im_nbr = 0
    end_nbr = -1

    ## Process Images
    print("Image processing progress bar: \n", flush=True)
    progressbar = tqdm(glob.glob(in_dir+'/*.JPG')[im_nbr:end_nbr])
    for image_name in progressbar:
        ## Progress bar
        progressbar.set_postfix_str("image: " + image_name.split("\\")[-1])
        ## Open image
        im = Image.open(image_name)
        ## Define saving path
        output = f"{out_dir}/{image_name[len(in_dir)+1:]}"
        # Rotate
        #im = im.rotate(90)
        ## Crop 
        im = im.crop((1500, 500, 2900, im.size[1]-500)) 
        ## Remove Red Channel
        im = FilterChannel(im, False, output, False)
        ## Enhance
        im = EnhanceIm(im, False, output, False)
        ## Extract Edges
        edges = EdgesDetection(im, True, output, True)
        ## Improve Edges
        #edges = ImproveEdges(edges, True, output, True)
    
    print("\n\nDone : all images have been processed.")
    
    
    
