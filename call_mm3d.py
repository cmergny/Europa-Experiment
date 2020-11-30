# -*- coding: utf-8 -*-
"""
call mm3d (Micmac) commands
Author: Cyril Mergny
Last update : 26/11/2020
"""

import glob
import os
import subprocess

def call_cmd(cmd):
    """Type the cmd argument in a terminal shell and print the output"""
    print("--- Calling command : {} ---".format(cmd))
    call_result = subprocess.run(cmd, capture_output=True,text=True)
    print(call_result.stderr)
    print(call_result.stdout)
    return()

# Change to folder path
path = "C:/Users/Arnaud/micmac_projects/"

master_nbr = 3



# for folder_name in glob.glob(path + 'set_*')[:1]:
#     print('Moving to folder : "{}".'.format(folder_name))
#     os.chdir(folder_name)
    
#     # Call command
#     cmd = 'mm3d SaisieMasqQT {}.JPG'.format(master_nbr)
#     call_cmd(cmd)
#     os.chdir("C:/Users/Arnaud/micmac_projects/")
    

for folder_name in glob.glob(path + 'set_*')[:1]:
    print('Moving to folder : "{}".'.format(folder_name))
    os.chdir(folder_name)

    # cmd = 'mm3d Tapioca All ".*JPG" -1'
    # call_cmd(cmd)
    
    # cmd = 'mm3d Tapas FraserBasic ".*JPG" Out=Folder'
    # call_cmd(cmd)
    
    # cmd = 'mm3d AperiCloud ".*JPG" Folder '
    # call_cmd(cmd)
    
    # cmd = 'mm3d Malt GeomImage ".*JPG" Folder Master={}.JPG ZoomF=2'.format(master_nbr)
    # call_cmd(cmd)
    
    # cmd = 'mm3d Nuage2Ply "MM-Malt-Img-{0}/NuageImProf_STD-MALT_Etape_7.xml" Attr="{0}.JPG" Out=7.ply RatioAttrCarte=2'.format(master_nbr)
    # call_cmd(cmd)
    
    # cmd = 'mm3d GrShade MM-Malt-Img-{}/Z_Num7_DeZoom2_STD-MALT.tif ModeOmbre=IgnE Mask=AutoMask_STD-MALT_Num_6.tif FZ=2 Out=depth7.tif'.format(master_nbr)
    # call_cmd(cmd)
    
    cmd = 'meshlabserver -i 7.ply -o output.ply -s script.mlx'
    call_cmd(cmd)

os.chdir("C:/Users/Arnaud/micmac_projects/")


