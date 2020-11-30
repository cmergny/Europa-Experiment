# -*- coding: utf-8 -*-
"""
Convert a set of images to a movie file using ffmpeg via python.
Images in the working_dir folder will be converted to a movie, if their name
Author: Cyril Mergny
Last update : 26/11/2020
"""

### Imports
import os
import subprocess

### Set Variables
working_dir = "laser_2411edges" # Dir of input images
movie_name = "../LaserEdgesMov.mp4"
imgs_names = "_DSC%04d.JPG" # Image name format (e.g. _DSC4342.JPG)
start_nbr = 3521 # Image number to start the movie

### Writing Command
## visual effects
vf = "" # means no vf
#vf = '-vf "transpose=1, eq=contrast=1, crop=2500:in_h/6:2000:in_h/2"'
#vf = '-vf crop=2500:in_h/6+1:2000:in_h/2'
## ffmpeg command arguments
args = '-y -r 12 -start_number {0} -i {1} {2} -vcodec mjpeg -qscale:v 1 -b:v 6000k {3} '.format(start_nbr, imgs_names, vf, movie_name)
## Final bash command
cmd = 'C:/Ffmpeg/bin/ffmpeg.exe {}'.format(args)

### Call Command

## Change os dir to working directory
path = f"C:/Users/Arnaud/micmac_projects/Laser/{working_dir}"
os.chdir(path)
## Calling cmd via terminal shell 
call_result = subprocess.run(cmd, capture_output=True,text=True)
print(call_result.stderr)
## Change back
os.chdir("C:/Users/Arnaud/micmac_projects/")




# ffmpeg  -i LaserEdgesMov.mp4 -i Laser+Mov.mp4 -i LaserEdges+Mov.mp4 -filter_complex "[0:v][1:v][2:v]vstack=inputs=3[v]" -map "[v]" Laser3Mov.mp4

# from tkinter import Tk     # from tkinter import Tk for Python 3.x
# from tkinter.filedialog import askopenfilename

# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)

# Laser+Mov.mp4
# LaserEdgesMov.mp4
# LaserEdges+Mov.mp4

# ffmpeg -i input0 -i input1 -filter_complex vstack=inputs=2 output

# ffmpeg -i Laser+Mov.mp4 -i LaserEdges+Mov.mp4 -i LaserEdgesMov.mp4 -filter_complex "[0:v][1:v][2:v]hstack=inputs=3[v]" -map "[v]" Laser3Mov.mp4