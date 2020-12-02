# -*- coding: utf-8 -*-
"""
Convert a set of images to a movie file using ffmpeg via python.
Images in the working_dir folder will be converted to a movie, if their name
Author: Cyril Mergny
Last update : 02/12/2020
"""

### Imports
import os
import subprocess

### Set Variables
working_dir = "laser_2611edges" # Dir of input images
movie_name = "../LaserEdgesMov.mp4"
imgs_names = "_DSC%04d.JPG" # Image name format (e.g. _DSC4342.JPG)
start_nbr = 4414 # Image number to start the movie

## Change os dir to working directory
path = f"C:/Users/Arnaud/micmac_projects/Laser/2611/{working_dir}"
os.chdir(path)

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
## Calling cmd via terminal shell 
call_result = subprocess.run(cmd, capture_output=True,text=True)
print(call_result.stderr)
## Change back
os.chdir("C:/Users/Arnaud/micmac_projects/")


## Merge 3movies
# topmov = "hey.mp4"
# midmov = 'ho.mp4'
# botmov = 'ha.mp4'
# outmov = 'hi.mp4'
# cmd = f'ffmpeg  -i {topmov} -i {midmov} -i {botmov} -filter_complex "[0:v][1:v][2:v]vstack=inputs=3[v]" -map "[v]" {outmov}'
# print(cmd)

