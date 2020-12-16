# Europa-Experiment
Analog experiments with ludox to understand Europa litosphere.

### laser_process.py 
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

### sort_imgs.py
From a folder of images creates sets of images grouped by their time 
(from exif data). Each set is a new folder consisting of images taken at time
close to each other. A parameter provided by the user, delta, determines the 
maximum time difference allowed for two images to be part of the same set.

### use_ffmpeg.py
Convert a set of images to a movie file using ffmpeg via python.

### call_mm3d.py
Calling mic mac command from python.
