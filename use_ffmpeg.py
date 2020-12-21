# -*- coding: utf-8 -*-
"""
Convert a set of images to a movie file using ffmpeg via python.
Images in the in_dir folder will be converted to a movie, if their name 
is well formatted.
Author: Cyril Mergny
Last update : 04/12/2020
"""

### Imports
import os
import glob # to search for files
import subprocess
# Set path to the script 
os.chdir(os.path.dirname(__file__))
from laser_process import BrowseFolder

### Functions 

def GetImageNameFormat(image_name):
    """
    Guess the ffmpeg format name of multiple files using one example:
        ex 1: image_name = 'Image001.JPG' -> format_name = 'Image%03d.JPG'
        ex 2: image_name = 'DSC_5136.JPG' -> format_name = 'DSC_%04d.JPG'
    """
    count = 0
    start = -1
    for i, letter in enumerate(image_name):
        if letter in [str(k) for k in range(10)]:
            count += 1
            if start == -1:
                start = i
    format_name = image_name[:start] + f"%0{count}d" + image_name[start+count:]
    print(f"# Detected ffpemg format name {format_name} from image {image_name}\n")
    return(format_name)


def WriteFfmpegCmd(start_nbr, imgs_names, movie_name):
    """ Returns a string that is a command line calling ffmpeg"""    
    ## visual effects
    vf = '' # means no vf
    #vf = '-vf "transpose=1, eq=contrast=1, crop=2500:in_h/6:2000:in_h/2"'
    #vf = '-vf crop=2500:in_h/6+1:2000:in_h/2'
    ## ffmpeg command arguments
    args = f'-y -r 15 -start_number {start_nbr} -i {imgs_names} {vf}'
    args += f' -vcodec libx265 -crf 28 {movie_name}'
    ## Call ffmpeg with args from its location
    cmd = f"C:\\Ffmpeg\\bin\\ffmpeg.exe {args}"
    return(cmd)
   

def CallShellCmd(cmd, stdout = True, stderr = True, print_cmd = False):
    """
    Calling a command via terminal shell
    """
    print("# Calling command line ...")
    ## Change os dir to input directory
    os.chdir(in_dir)
    print(f"\t # Changed os path to {in_dir}")  
    # Calling command
    if print_cmd:
        print(f"Calling: {cmd}")
    call_result = subprocess.run(cmd, capture_output=True,text=True)
    if stdout:
        print('\n' + call_result.stdout)
    if stderr:
        print('\n' + call_result.stderr)
    ## Change back
    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)
    print(f" \t # Change os path back to {script_dir}")
    return(None)

def Stack3Movies(topmov, midmov, botmov, outmov):
    """" Write the ffmpeg command for stacking three movies into one."""
    cmd = f'ffmpeg  -i {topmov} -i {midmov} -i {botmov} -filter_complex '
    cmd += '"[0:v][1:v][2:v]vstack=inputs=3[v]" -map "[v]" {outmov}'
    print(cmd)
    return(cmd)


#### Main

if __name__ == '__main__':
    
    print("\n --- Python Script using ffmpeg ---- \n")
    
    user_friendly = False
    
    if user_friendly:
        ## Find input folder  
        in_dir = BrowseFolder(user_friendly)
        ## Ask user
        movie_name = input("# Enter the output movie name: ")
        start_nbr = int(input("# Enter starting number: "))
    else:
        ## Manual Definition 
        in_dir = "C:/Users/Arnaud/EuropaExp/XP1612/LaserContrast2" # input dir
        in_dir = BrowseFolder(user_friendly, in_dir)
        movie_name = "../OscillationsPart2.mp4"
        start_nbr = 1 # Image number to start the movie
        
    ## Find format name
    #print(glob.glob(in_dir))
    image_name = glob.glob(in_dir+'/*.JPG')[0].split('\\')[-1]
    imgs_names = GetImageNameFormat(image_name) # Image name format
    #imgs_names = "" # if smth went wrong enter it manually
    

    ### Write Ffmpeg Command
    cmd = WriteFfmpegCmd(start_nbr, imgs_names, movie_name)

    ### Call Command
    CallShellCmd(cmd, stdout = False, stderr = True, print_cmd = False)
    print(f"\t # Created movie {movie_name}")
    
    
    ## Merge 3movies
    # topmov = "hey.mp4"
    # midmov = 'ho.mp4'
    # botmov = 'ha.mp4'
    # outmov = 'hi.mp4'
    # Stack3Movies(topmov, midmov, botmov, outmov)
    
